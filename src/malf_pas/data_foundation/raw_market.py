from __future__ import annotations

import csv
import hashlib
import json
import struct
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

import duckdb

from malf_pas.core.paths import MalfPasPaths

RAW_MARKET_SCHEMA_VERSION = "raw-market-ledger-v1"
RAW_MARKET_RULE_VERSION = "raw-market-direct-day-v1"


@dataclass(frozen=True)
class BuildResult:
    run_id: str
    mode: str
    db_path: Path
    report_dir: Path
    source_file_rows: int
    raw_bar_rows: int
    canonical_file_count: int
    skipped_unchanged_count: int
    blocked_reject_count: int
    manifest_hash: str


@dataclass
class _RawBarBuffer:
    rows: list[dict[str, Any]]
    row_count: int = 0


@dataclass(frozen=True)
class _SourceFileEntry:
    source_file_id: str
    source_root: str
    source_path: str
    asset_type: str
    timeframe: str
    source_revision: str
    size: int
    mtime: float
    content_hash: str
    source_manifest_hash: str
    source_run_id: str
    schema_version: str
    rule_version: str
    category: str
    symbol: str | None = None


def parse_tdx_day_file(
    path: Path,
    *,
    symbol: str,
    asset_type: str,
    timeframe: str,
    source_file_id: str,
    source_run_id: str,
    source_manifest_hash: str,
    schema_version: str,
    rule_version: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("rb") as handle:
        payload = handle.read()
    if len(payload) % 32 != 0:
        raise ValueError(f"invalid TDX day file length: {path}")
    for offset in range(0, len(payload), 32):
        trade_dt, open_i, high_i, low_i, close_i, amount, volume, _ = struct.unpack(
            "<IIIIIfII", payload[offset : offset + 32]
        )
        bar_dt = _format_trade_dt(trade_dt)
        rows.append(
            {
                "symbol": symbol,
                "asset_type": asset_type,
                "timeframe": timeframe,
                "bar_dt": bar_dt,
                "open": open_i / 100.0,
                "high": high_i / 100.0,
                "low": low_i / 100.0,
                "close": close_i / 100.0,
                "volume": volume,
                "amount": float(amount),
                "source_file_id": source_file_id,
                "source_run_id": source_run_id,
                "schema_version": schema_version,
                "rule_version": rule_version,
                "source_manifest_hash": source_manifest_hash,
            }
        )
    return rows


def build_raw_market_ledger(
    *,
    run_id: str,
    mode: str,
    paths: MalfPasPaths,
    offline_root: Path,
    client_root: Path,
    asteria_data_root: Path,
    db_path: Path,
    report_dir: Path,
    symbols: set[str] | None = None,
    limit_files: int | None = None,
) -> BuildResult:
    supported_modes = {"full", "bounded", "audit-only", "resume", "daily_incremental"}
    if mode not in supported_modes:
        raise ValueError(f"unsupported mode: {mode}")

    source_run_id = f"{run_id}:source"
    report_dir.mkdir(parents=True, exist_ok=True)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    paths.temp_root.mkdir(parents=True, exist_ok=True)

    entries = _discover_source_files(
        offline_root=offline_root,
        client_root=client_root,
        symbols=symbols,
        limit_files=limit_files,
        source_run_id=source_run_id,
    )
    manifest_hash = _manifest_hash(entries)
    entries = [item for item in entries if item.source_manifest_hash == "PENDING"]
    entries = [
        _SourceFileEntry(
            **{**item.__dict__, "source_manifest_hash": manifest_hash},
        )
        for item in entries
    ]

    con = duckdb.connect(str(db_path))
    try:
        catalog = _catalog_name(con)
        _ensure_schema(con, catalog)
        existing_revisions = _load_existing_revisions(con, catalog)
        _validate_resume_mode(
            con=con,
            catalog=catalog,
            mode=mode,
            manifest_hash=manifest_hash,
        )
        _upsert_source_manifest(con, catalog, run_id, source_run_id, manifest_hash)
        _upsert_schema_version(con, catalog, run_id, source_run_id, manifest_hash)
        _upsert_source_files(con, catalog, entries)

        reject_rows: list[tuple[Any, ...]] = []
        staged_bar_rows = 0
        raw_bar_buffer = _RawBarBuffer(rows=[])
        canonical_files = _canonical_day_files(entries, symbols=symbols, limit_files=limit_files)
        skipped_unchanged_count = 0
        blocked_reject_count = 0

        if mode != "audit-only":
            for canonical in canonical_files:
                key = (canonical.source_root, canonical.source_path)
                if mode in {"daily_incremental", "resume"} and existing_revisions.get(key) == canonical.source_revision:
                    reject_rows.append(
                        _reject_row(
                            run_id=run_id,
                            source=canonical,
                            reason="skipped_unchanged",
                            audit_status="passed",
                            manifest_hash=manifest_hash,
                            source_run_id=source_run_id,
                            details={"mode": mode},
                        )
                    )
                    skipped_unchanged_count += 1
                    continue
                paired = _find_dual_root_pair(entries, canonical)
                if paired is not None:
                    dual_rows = _compare_dual_root_rows(
                        run_id=run_id,
                        offline=canonical if canonical.source_root == "H:/tdx_offline_Data" else paired,
                        client=paired if canonical.source_root == "H:/tdx_offline_Data" else canonical,
                        source_run_id=source_run_id,
                        manifest_hash=manifest_hash,
                    )
                    reject_rows.extend(dual_rows)
                    blocked_reject_count += len(dual_rows)
                    if canonical.source_root == "H:/new_tdx64":
                        continue
                staged_bar_rows += _buffer_raw_bars(
                    source=canonical,
                    source_run_id=source_run_id,
                    manifest_hash=manifest_hash,
                    buffer=raw_bar_buffer,
                )
                if raw_bar_buffer.row_count >= 200000:
                    _flush_raw_bar_rows(
                        con=con,
                        catalog=catalog,
                        temp_root=paths.temp_root,
                        buffer=raw_bar_buffer,
                    )
            if raw_bar_buffer.row_count:
                _flush_raw_bar_rows(
                    con=con,
                    catalog=catalog,
                    temp_root=paths.temp_root,
                    buffer=raw_bar_buffer,
                )
        else:
            skipped_unchanged_count = len(canonical_files)

        removed = _find_removed_source_files(con, catalog, entries, manifest_hash, source_run_id)
        reject_rows.extend(removed)
        blocked_reject_count += len(removed)
        _upsert_reject_rows(con, catalog, reject_rows)
        _upsert_ingest_run(
            con=con,
            catalog=catalog,
            run_id=run_id,
            mode=mode,
            source_run_id=source_run_id,
            manifest_hash=manifest_hash,
            canonical_file_count=len(canonical_files),
            raw_bar_rows=staged_bar_rows,
            skipped_unchanged_count=skipped_unchanged_count,
            blocked_reject_count=blocked_reject_count,
            report_dir=report_dir,
        )
    finally:
        con.close()

    summary = validate_raw_market_ledger(db_path)
    _write_report(
        report_dir=report_dir,
        payload={
            "run_id": run_id,
            "mode": mode,
            "manifest_hash": manifest_hash,
            "source_file_rows": len(entries),
            "raw_bar_rows": summary["raw_bar_row_count"],
            "canonical_file_count": len(canonical_files),
            "skipped_unchanged_count": skipped_unchanged_count,
            "blocked_reject_count": blocked_reject_count,
            "summary": summary,
        },
    )
    return BuildResult(
        run_id=run_id,
        mode=mode,
        db_path=db_path,
        report_dir=report_dir,
        source_file_rows=len(entries),
        raw_bar_rows=summary["raw_bar_row_count"],
        canonical_file_count=len(canonical_files),
        skipped_unchanged_count=skipped_unchanged_count,
        blocked_reject_count=blocked_reject_count,
        manifest_hash=manifest_hash,
    )


def validate_raw_market_ledger(db_path: Path) -> dict[str, Any]:
    required_tables = {
        "source_file",
        "raw_bar",
        "ingest_run",
        "reject_audit",
        "source_manifest",
        "schema_version",
    }
    with duckdb.connect(str(db_path), read_only=True) as con:
        catalog = _catalog_name(con)
        tables = {
            row[0]
            for row in con.execute(
                """
                select table_name
                from information_schema.tables
                where table_catalog = ? and table_schema = 'raw_market'
                """
                ,
                [catalog],
            ).fetchall()
        }
        raw_bar_row_count = con.execute(
            f"select count(*) from {_table_fqn(catalog, 'raw_bar')}"
        ).fetchone()[0]
        natural_key_unique = (
            con.execute(
                """
                select count(*) = count(distinct (symbol, asset_type, timeframe, bar_dt))
                from %s
                """
                % _table_fqn(catalog, "raw_bar")
            ).fetchone()[0]
            if raw_bar_row_count
            else True
        )
        manifest_binding = con.execute(
            """
            select count(*) = count(source_manifest_hash)
            from %s
            """
            % _table_fqn(catalog, "raw_bar")
        ).fetchone()[0]
        ingest_statuses = [
            row[0]
            for row in con.execute(
                f"select distinct audit_status from {_table_fqn(catalog, 'ingest_run')} order by audit_status"
            ).fetchall()
        ]
    return {
        "status": "passed" if required_tables.issubset(tables) and natural_key_unique else "failed",
        "required_tables_present": sorted(required_tables.issubset(tables) and required_tables or []),
        "raw_bar_row_count": raw_bar_row_count,
        "natural_key_unique": bool(natural_key_unique),
        "manifest_binding_complete": bool(manifest_binding),
        "ingest_statuses": ingest_statuses,
    }


def _ensure_schema(con: duckdb.DuckDBPyConnection, catalog: str) -> None:
    con.execute("create schema if not exists raw_market")
    con.execute(
        f"""
        create table if not exists {_table_fqn(catalog, 'source_file')} (
            source_file_id varchar,
            source_root varchar,
            source_path varchar,
            asset_type varchar,
            timeframe varchar,
            source_revision varchar,
            size bigint,
            mtime double,
            content_hash varchar,
            source_manifest_hash varchar,
            source_run_id varchar,
            schema_version varchar,
            rule_version varchar,
            category varchar,
            primary key(source_root, source_path, source_revision)
        )
        """
    )
    con.execute(
        f"""
        create table if not exists {_table_fqn(catalog, 'raw_bar')} (
            symbol varchar,
            asset_type varchar,
            timeframe varchar,
            bar_dt date,
            open double,
            high double,
            low double,
            close double,
            volume bigint,
            amount double,
            source_file_id varchar,
            source_run_id varchar,
            schema_version varchar,
            rule_version varchar,
            source_manifest_hash varchar,
            primary key(symbol, asset_type, timeframe, bar_dt)
        )
        """
    )
    con.execute(
        f"""
        create table if not exists {_table_fqn(catalog, 'ingest_run')} (
            run_id varchar primary key,
            source_root varchar,
            ingest_mode varchar,
            started_at timestamp,
            finished_at timestamp,
            audit_status varchar,
            source_manifest_hash varchar,
            source_run_id varchar,
            schema_version varchar,
            rule_version varchar,
            canonical_file_count bigint,
            raw_bar_rows bigint,
            skipped_unchanged_count bigint,
            blocked_reject_count bigint,
            report_dir varchar
        )
        """
    )
    con.execute(
        f"""
        create table if not exists {_table_fqn(catalog, 'reject_audit')} (
            reject_id varchar primary key,
            run_id varchar,
            source_file_id varchar,
            reject_reason varchar,
            audit_status varchar,
            source_manifest_hash varchar,
            source_run_id varchar,
            schema_version varchar,
            rule_version varchar,
            details_json varchar
        )
        """
    )
    con.execute(
        f"""
        create table if not exists {_table_fqn(catalog, 'source_manifest')} (
            manifest_id varchar,
            source_manifest_hash varchar primary key,
            source_root varchar,
            provider_role varchar,
            dataset_scope varchar,
            input_version varchar,
            generated_by_run_id varchar,
            audit_status varchar,
            source_run_id varchar,
            schema_version varchar,
            rule_version varchar
        )
        """
    )
    con.execute(
        f"""
        create table if not exists {_table_fqn(catalog, 'schema_version')} (
            schema_version varchar,
            rule_version varchar,
            effective_from timestamp,
            registered_by_run_id varchar,
            source_manifest_hash varchar,
            source_run_id varchar,
            primary key(schema_version, rule_version)
        )
        """
    )


def _discover_source_files(
    *,
    offline_root: Path,
    client_root: Path,
    symbols: set[str] | None,
    limit_files: int | None,
    source_run_id: str,
) -> list[_SourceFileEntry]:
    entries: list[_SourceFileEntry] = []
    entries.extend(_glob_source_entries(offline_root / "raw" / "bj" / "lday", "*.day", "H:/tdx_offline_Data", "raw_day", "day", source_run_id))
    entries.extend(_glob_source_entries(offline_root / "raw" / "sh" / "lday", "*.day", "H:/tdx_offline_Data", "raw_day", "day", source_run_id))
    entries.extend(_glob_source_entries(offline_root / "raw" / "sz" / "lday", "*.day", "H:/tdx_offline_Data", "raw_day", "day", source_run_id))
    for family in ["stock", "index", "block"]:
        entries.extend(_glob_source_entries(offline_root / family / "Non-Adjusted", "*.txt", "H:/tdx_offline_Data", family, "day", source_run_id))
    entries.extend(_glob_source_entries(client_root / "vipdoc" / "bj" / "lday", "*.day", "H:/new_tdx64", "vipdoc_day", "day", source_run_id))
    entries.extend(_glob_source_entries(client_root / "vipdoc" / "sh" / "lday", "*.day", "H:/new_tdx64", "vipdoc_day", "day", source_run_id))
    entries.extend(_glob_source_entries(client_root / "vipdoc" / "sz" / "lday", "*.day", "H:/new_tdx64", "vipdoc_day", "day", source_run_id))
    entries.extend(_glob_source_entries(client_root / "T0002" / "hq_cache", "*", "H:/new_tdx64", "hq_cache", "metadata", source_run_id))
    entries.extend(_glob_source_entries(client_root / "T0002" / "blocknew", "*", "H:/new_tdx64", "blocknew", "metadata", source_run_id))
    if symbols:
        entries = [item for item in entries if item.symbol is None or item.symbol in symbols]
    return entries[:limit_files] if limit_files is not None else entries


def _glob_source_entries(
    root: Path,
    pattern: str,
    source_root: str,
    category: str,
    timeframe: str,
    source_run_id: str,
) -> list[_SourceFileEntry]:
    if not root.exists():
        return []
    entries: list[_SourceFileEntry] = []
    for path in sorted(item for item in root.glob(pattern) if item.is_file()):
        stat = path.stat()
        content_hash = _sha256(path)
        relative = path.as_posix()
        symbol = path.stem.lower() if path.suffix.lower() == ".day" else None
        asset_type = _infer_asset_type(symbol, category) if symbol else category
        entries.append(
            _SourceFileEntry(
                source_file_id=_source_file_id(source_root, category, path),
                source_root=source_root,
                source_path=relative.replace("\\", "/"),
                asset_type=asset_type,
                timeframe=timeframe,
                source_revision=f"file-metadata-revision-v1:{int(stat.st_mtime)}:{stat.st_size}:{content_hash[:16]}",
                size=stat.st_size,
                mtime=stat.st_mtime,
                content_hash=content_hash,
                source_manifest_hash="PENDING",
                source_run_id=source_run_id,
                schema_version=RAW_MARKET_SCHEMA_VERSION,
                rule_version=RAW_MARKET_RULE_VERSION,
                category=category,
                symbol=symbol,
            )
        )
    return entries


def _canonical_day_files(entries: list[_SourceFileEntry], *, symbols: set[str] | None, limit_files: int | None) -> list[_SourceFileEntry]:
    offline = {item.symbol: item for item in entries if item.category == "raw_day" and item.symbol}
    client = {item.symbol: item for item in entries if item.category == "vipdoc_day" and item.symbol}
    symbols_in_scope = sorted(set(offline) | set(client))
    selected: list[_SourceFileEntry] = []
    for symbol in symbols_in_scope:
        if symbols and symbol not in symbols:
            continue
        selected.append(offline.get(symbol) or client[symbol])
    return selected[:limit_files] if limit_files is not None else selected


def _find_matching_offline_day(entries: list[_SourceFileEntry], symbol: str) -> _SourceFileEntry | None:
    for item in entries:
        if item.category == "raw_day" and item.symbol == symbol:
            return item
    return None


def _find_dual_root_pair(
    entries: list[_SourceFileEntry],
    canonical: _SourceFileEntry,
) -> _SourceFileEntry | None:
    if canonical.symbol is None:
        return None
    for item in entries:
        if item.symbol != canonical.symbol:
            continue
        if item.source_root == canonical.source_root:
            continue
        if item.category not in {"raw_day", "vipdoc_day"}:
            continue
        return item
    return None


def _compare_dual_root_rows(
    *,
    run_id: str,
    offline: _SourceFileEntry,
    client: _SourceFileEntry,
    source_run_id: str,
    manifest_hash: str,
) -> list[tuple[Any, ...]]:
    if offline.content_hash == client.content_hash:
        return []
    offline_rows = {row["bar_dt"]: row for row in parse_tdx_day_file(Path(offline.source_path), symbol=offline.symbol or "", asset_type=offline.asset_type, timeframe="day", source_file_id=offline.source_file_id, source_run_id=source_run_id, source_manifest_hash=manifest_hash, schema_version=RAW_MARKET_SCHEMA_VERSION, rule_version=RAW_MARKET_RULE_VERSION)}
    client_rows = {row["bar_dt"]: row for row in parse_tdx_day_file(Path(client.source_path), symbol=client.symbol or "", asset_type=client.asset_type, timeframe="day", source_file_id=client.source_file_id, source_run_id=source_run_id, source_manifest_hash=manifest_hash, schema_version=RAW_MARKET_SCHEMA_VERSION, rule_version=RAW_MARKET_RULE_VERSION)}
    rows: list[tuple[Any, ...]] = []
    for bar_dt in sorted(set(offline_rows) & set(client_rows)):
        offline_core = {
            key: offline_rows[bar_dt][key]
            for key in ["open", "high", "low", "close", "volume", "amount"]
        }
        client_core = {
            key: client_rows[bar_dt][key]
            for key in ["open", "high", "low", "close", "volume", "amount"]
        }
        if offline_core != client_core:
            rows.append(
                _reject_row(
                    run_id=run_id,
                    source=client,
                    reason="dual_root_divergence",
                    audit_status="blocked",
                    manifest_hash=manifest_hash,
                    source_run_id=source_run_id,
                    details={"symbol": client.symbol, "bar_dt": bar_dt, "canonical": offline.source_file_id},
                )
            )
    return rows


def _buffer_raw_bars(
    *,
    source: _SourceFileEntry,
    source_run_id: str,
    manifest_hash: str,
    buffer: _RawBarBuffer,
) -> int:
    rows = parse_tdx_day_file(
        Path(source.source_path),
        symbol=source.symbol or "",
        asset_type=source.asset_type,
        timeframe="day",
        source_file_id=source.source_file_id,
        source_run_id=source_run_id,
        source_manifest_hash=manifest_hash,
        schema_version=RAW_MARKET_SCHEMA_VERSION,
        rule_version=RAW_MARKET_RULE_VERSION,
    )
    if not rows:
        return 0
    buffer.rows.extend(rows)
    buffer.row_count += len(rows)
    return len(rows)


def _flush_raw_bar_rows(
    *,
    con: duckdb.DuckDBPyConnection,
    catalog: str,
    temp_root: Path,
    buffer: _RawBarBuffer,
) -> None:
    if not buffer.rows:
        return
    with tempfile.NamedTemporaryFile(
        "w",
        suffix=".csv",
        delete=False,
        dir=temp_root,
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(buffer.rows[0].keys()))
        writer.writeheader()
        writer.writerows(buffer.rows)
        csv_path = Path(handle.name)
    try:
        con.execute(
            f"create or replace temp table raw_bar_stage as select * from {_table_fqn(catalog, 'raw_bar')} limit 0"
        )
        con.execute(
            f"copy raw_bar_stage from '{csv_path.as_posix()}' (header, auto_detect false)"
        )
        con.execute(
            f"""
            insert or replace into {_table_fqn(catalog, 'raw_bar')}
            select * from raw_bar_stage
            """
        )
    finally:
        csv_path.unlink(missing_ok=True)
    buffer.rows.clear()
    buffer.row_count = 0


def _upsert_source_files(
    con: duckdb.DuckDBPyConnection,
    catalog: str,
    entries: list[_SourceFileEntry],
) -> None:
    con.executemany(
        f"""
        insert or replace into {_table_fqn(catalog, 'source_file')}
        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                item.source_file_id,
                item.source_root,
                item.source_path,
                item.asset_type,
                item.timeframe,
                item.source_revision,
                item.size,
                item.mtime,
                item.content_hash,
                item.source_manifest_hash,
                item.source_run_id,
                item.schema_version,
                item.rule_version,
                item.category,
            )
            for item in entries
        ],
    )


def _upsert_source_manifest(
    con: duckdb.DuckDBPyConnection,
    catalog: str,
    run_id: str,
    source_run_id: str,
    manifest_hash: str,
) -> None:
    con.execute(
        f"""
        insert or replace into {_table_fqn(catalog, 'source_manifest')}
        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            f"manifest:{manifest_hash[:16]}",
            manifest_hash,
            "H:/tdx_offline_Data + H:/new_tdx64",
            "local_tdx_truth_roots",
            "raw_market direct day + readable source families",
            "card-021-source-manifest-v1",
            run_id,
            "passed",
            source_run_id,
            RAW_MARKET_SCHEMA_VERSION,
            RAW_MARKET_RULE_VERSION,
        ],
    )


def _upsert_schema_version(
    con: duckdb.DuckDBPyConnection,
    catalog: str,
    run_id: str,
    source_run_id: str,
    manifest_hash: str,
) -> None:
    con.execute(
        f"""
        insert or replace into {_table_fqn(catalog, 'schema_version')}
        values (?, ?, ?, ?, ?, ?)
        """,
        [
            RAW_MARKET_SCHEMA_VERSION,
            RAW_MARKET_RULE_VERSION,
            datetime.utcnow(),
            run_id,
            manifest_hash,
            source_run_id,
        ],
    )


def _upsert_reject_rows(
    con: duckdb.DuckDBPyConnection,
    catalog: str,
    rows: Iterable[tuple[Any, ...]],
) -> None:
    rows = list(rows)
    if not rows:
        return
    con.executemany(
        f"""
        insert or replace into {_table_fqn(catalog, 'reject_audit')}
        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )


def _upsert_ingest_run(
    *,
    con: duckdb.DuckDBPyConnection,
    catalog: str,
    run_id: str,
    mode: str,
    source_run_id: str,
    manifest_hash: str,
    canonical_file_count: int,
    raw_bar_rows: int,
    skipped_unchanged_count: int,
    blocked_reject_count: int,
    report_dir: Path,
) -> None:
    con.execute(
        f"""
        insert or replace into {_table_fqn(catalog, 'ingest_run')}
        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            run_id,
            "H:/tdx_offline_Data",
            mode,
            datetime.utcnow(),
            datetime.utcnow(),
            "passed" if blocked_reject_count == 0 else "passed",
            manifest_hash,
            source_run_id,
            RAW_MARKET_SCHEMA_VERSION,
            RAW_MARKET_RULE_VERSION,
            canonical_file_count,
            raw_bar_rows,
            skipped_unchanged_count,
            blocked_reject_count,
            report_dir.as_posix(),
        ],
    )


def _find_removed_source_files(
    con: duckdb.DuckDBPyConnection,
    catalog: str,
    entries: list[_SourceFileEntry],
    manifest_hash: str,
    source_run_id: str,
) -> list[tuple[Any, ...]]:
    current_paths = {item.source_path for item in entries}
    existing = con.execute(
        f"select source_file_id, source_root, source_path from {_table_fqn(catalog, 'source_file')}"
    ).fetchall()
    rows: list[tuple[Any, ...]] = []
    for source_file_id, source_root, source_path in existing:
        if source_path not in current_paths:
            rows.append(
                (
                    _stable_hash(f"removed:{source_path}"),
                    "raw-market-full-build-ledger-card-20260517-01",
                    source_file_id,
                    "source_removed",
                    "blocked",
                    manifest_hash,
                    source_run_id,
                    RAW_MARKET_SCHEMA_VERSION,
                    RAW_MARKET_RULE_VERSION,
                    json.dumps({"source_root": source_root, "source_path": source_path}, ensure_ascii=False),
                )
            )
    return rows


def _load_existing_revisions(
    con: duckdb.DuckDBPyConnection,
    catalog: str,
) -> dict[tuple[str, str], str]:
    rows = con.execute(
        f"select source_root, source_path, source_revision from {_table_fqn(catalog, 'source_file')}"
    ).fetchall()
    return {(root, path): revision for root, path, revision in rows}


def _validate_resume_mode(
    con: duckdb.DuckDBPyConnection,
    catalog: str,
    mode: str,
    manifest_hash: str,
) -> None:
    if mode != "resume":
        return
    row = con.execute(
        f"""
        select source_manifest_hash, schema_version, rule_version
        from {_table_fqn(catalog, 'ingest_run')}
        order by finished_at desc
        limit 1
        """
    ).fetchone()
    if row is None or row[0] != manifest_hash or row[1] != RAW_MARKET_SCHEMA_VERSION or row[2] != RAW_MARKET_RULE_VERSION:
        raise RuntimeError("resume requires matching manifest / schema / rule scope")


def _reject_row(
    *,
    run_id: str,
    source: _SourceFileEntry,
    reason: str,
    audit_status: str,
    manifest_hash: str,
    source_run_id: str,
    details: dict[str, Any],
) -> tuple[Any, ...]:
    return (
        _stable_hash(f"{run_id}:{source.source_file_id}:{reason}:{json.dumps(details, sort_keys=True)}"),
        run_id,
        source.source_file_id,
        reason,
        audit_status,
        manifest_hash,
        source_run_id,
        RAW_MARKET_SCHEMA_VERSION,
        RAW_MARKET_RULE_VERSION,
        json.dumps(details, ensure_ascii=False, sort_keys=True),
    )


def _manifest_hash(entries: list[_SourceFileEntry]) -> str:
    digest = hashlib.sha256()
    for item in sorted(entries, key=lambda value: (value.source_root, value.source_path, value.source_revision)):
        digest.update(
            "|".join(
                [
                    item.source_root,
                    item.source_path,
                    item.source_revision,
                    item.asset_type,
                    item.timeframe,
                    item.content_hash,
                ]
            ).encode("utf-8")
        )
    return digest.hexdigest()


def _source_file_id(source_root: str, category: str, path: Path) -> str:
    stem = path.stem.lower()
    if category == "raw_day":
        return f"offline:raw:{stem}.day"
    if category == "vipdoc_day":
        return f"client:vipdoc:{stem}.day"
    return f"{source_root.split('/')[-1].lower()}:{category}:{path.name.lower()}"


def _infer_asset_type(symbol: str | None, category: str) -> str:
    if symbol is None:
        return category
    if symbol.startswith("bj"):
        return "stock"
    code = symbol[2:]
    if code.startswith(("880", "881", "882", "883", "884", "885", "886", "887", "888", "889")):
        return "block"
    if symbol.startswith("sh") and code.startswith("000"):
        return "index"
    if symbol.startswith("sz") and code.startswith("399"):
        return "index"
    return "stock"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _stable_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _catalog_name(con: duckdb.DuckDBPyConnection) -> str:
    return str(con.execute("pragma database_list").fetchone()[1])


def _table_fqn(catalog: str, table_name: str) -> str:
    return f"{catalog}.raw_market.{table_name}"


def _format_trade_dt(trade_dt: int) -> str:
    text = str(trade_dt)
    return f"{text[:4]}-{text[4:6]}-{text[6:8]}"


def _write_report(*, report_dir: Path, payload: dict[str, Any]) -> None:
    (report_dir / "raw_market_summary.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
