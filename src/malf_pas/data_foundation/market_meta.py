from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import duckdb

from malf_pas.core.paths import MalfPasPaths
from malf_pas.data_foundation.raw_market import validate_raw_market_ledger
from malf_pas.data_foundation.tdx_meta import TdxStaticSnapshot, load_tdx_static_snapshot

MARKET_META_SCHEMA_VERSION = "market-meta-ledger-v1"
MARKET_META_RULE_VERSION = "market-meta-tdx-direct-v1"
MARKET_META_SCHEMA_NAME = "market_meta"


@dataclass(frozen=True)
class BuildResult:
    run_id: str
    mode: str
    meta_db_path: Path
    report_dir: Path
    source_manifest_hash: str
    instrument_row_count: int
    trade_calendar_row_count: int
    tradability_row_count: int
    relation_row_count: int
    unresolved_gap_count: int


def build_market_meta(
    *,
    run_id: str,
    mode: str,
    paths: MalfPasPaths,
    raw_db_path: Path,
    day_db_path: Path,
    meta_db_path: Path,
    hq_cache_root: Path,
    blocknew_root: Path,
    report_dir: Path,
    symbols: set[str] | None = None,
    limit_symbols: int | None = None,
) -> BuildResult:
    supported_modes = {"full", "bounded", "audit-only"}
    if mode not in supported_modes:
        raise ValueError(f"unsupported mode: {mode}")

    raw_summary = validate_raw_market_ledger(raw_db_path)
    if raw_summary["status"] != "passed":
        raise RuntimeError("raw_market ledger must validate before building market_meta")

    report_dir.mkdir(parents=True, exist_ok=True)
    meta_db_path.parent.mkdir(parents=True, exist_ok=True)
    static_snapshot = load_tdx_static_snapshot(
        hq_cache_root=hq_cache_root,
        blocknew_root=blocknew_root,
    )
    day_context = _load_day_context(
        day_db_path,
        hq_cache_root=hq_cache_root,
        blocknew_root=blocknew_root,
    )
    raw_context = _load_raw_context(raw_db_path)
    selected_symbols = _resolve_symbol_scope(
        static_snapshot=static_snapshot,
        day_db_path=day_db_path,
        symbols=symbols,
        limit_symbols=limit_symbols,
    )
    snapshot = _filter_snapshot(static_snapshot, selected_symbols)
    manifest_hash = _manifest_hash(
        day_context=day_context,
        raw_context=raw_context,
        static_files=snapshot.source_files,
        symbol_scope=selected_symbols,
    )

    if mode != "audit-only":
        _materialize_market_meta(
            run_id=run_id,
            day_context=day_context,
            raw_context=raw_context,
            snapshot=snapshot,
            manifest_hash=manifest_hash,
            day_db_path=day_db_path,
            meta_db_path=meta_db_path,
        )

    summary = validate_market_meta(meta_db_path=meta_db_path)
    _write_report(
        report_dir=report_dir,
        payload={
            "run_id": run_id,
            "mode": mode,
            "source_manifest_hash": manifest_hash,
            "symbol_scope": selected_symbols,
            "summary": summary,
        },
    )
    database = summary["databases"]["market_meta"]
    return BuildResult(
        run_id=run_id,
        mode=mode,
        meta_db_path=meta_db_path,
        report_dir=report_dir,
        source_manifest_hash=manifest_hash,
        instrument_row_count=database["instrument_master_row_count"],
        trade_calendar_row_count=database["trade_calendar_row_count"],
        tradability_row_count=database["tradability_fact_row_count"],
        relation_row_count=database["industry_block_relation_row_count"],
        unresolved_gap_count=database["tradability_unresolved_gap_count"],
    )


def validate_market_meta(*, meta_db_path: Path) -> dict[str, Any]:
    required_tables = {
        "instrument_master",
        "trade_calendar",
        "tradability_fact",
        "industry_block_relation",
        "source_manifest",
        "schema_version",
    }
    with duckdb.connect(str(meta_db_path), read_only=True) as con:
        catalog = _catalog_name(con)
        tables = {
            row[0]
            for row in con.execute(
                """
                select table_name
                from information_schema.tables
                where table_catalog = ? and table_schema = ?
                """,
                [catalog, MARKET_META_SCHEMA_NAME],
            ).fetchall()
        }
        table_fqn = lambda name: _table_fqn(catalog, MARKET_META_SCHEMA_NAME, name)
        counts = {
            "instrument_master_row_count": con.execute(
                f"select count(*) from {table_fqn('instrument_master')}"
            ).fetchone()[0],
            "trade_calendar_row_count": con.execute(
                f"select count(*) from {table_fqn('trade_calendar')}"
            ).fetchone()[0],
            "tradability_fact_row_count": con.execute(
                f"select count(*) from {table_fqn('tradability_fact')}"
            ).fetchone()[0],
            "industry_block_relation_row_count": con.execute(
                f"select count(*) from {table_fqn('industry_block_relation')}"
            ).fetchone()[0],
            "source_manifest_row_count": con.execute(
                f"select count(*) from {table_fqn('source_manifest')}"
            ).fetchone()[0],
            "schema_version_row_count": con.execute(
                f"select count(*) from {table_fqn('schema_version')}"
            ).fetchone()[0],
        }
        uniqueness = {
            "instrument_master_natural_key_unique": _count_equals_distinct(
                con,
                f"{table_fqn('instrument_master')}",
                "(symbol, asset_type)",
            ),
            "trade_calendar_natural_key_unique": _count_equals_distinct(
                con,
                f"{table_fqn('trade_calendar')}",
                "(exchange, trade_dt)",
            ),
            "tradability_fact_natural_key_unique": _count_equals_distinct(
                con,
                f"{table_fqn('tradability_fact')}",
                "(symbol, asset_type, trade_dt)",
            ),
            "industry_block_relation_natural_key_unique": _count_equals_distinct(
                con,
                f"{table_fqn('industry_block_relation')}",
                "(symbol, asset_type, relation_type, relation_code, effective_from)",
            ),
        }
        lineage_complete = all(
            con.execute(
                f"""
                select
                    count(*) = count(source_run_id)
                    and count(*) = count(schema_version)
                    and count(*) = count(rule_version)
                    and count(*) = count(source_manifest_hash)
                from {table_fqn(table_name)}
                """
            ).fetchone()[0]
            for table_name in [
                "instrument_master",
                "trade_calendar",
                "tradability_fact",
                "industry_block_relation",
                "source_manifest",
                "schema_version",
            ]
        )
        manifest_row = con.execute(
            f"""
            select unresolved_symbol_count, unresolved_gap_count
            from {table_fqn('source_manifest')}
            """
        ).fetchone()

    payload = {
        "required_tables_present": sorted(required_tables & tables),
        **counts,
        **uniqueness,
        "lineage_complete": bool(lineage_complete),
        "tradability_direct_covered_row_count": counts["tradability_fact_row_count"],
        "tradability_unresolved_symbol_count": int(manifest_row[0]) if manifest_row else 0,
        "tradability_unresolved_gap_count": int(manifest_row[1]) if manifest_row else 0,
        "non_empty_supporting_tables": counts["source_manifest_row_count"] > 0
        and counts["schema_version_row_count"] > 0,
    }
    status = "passed" if _meta_status(required_tables, tables, payload) else "failed"
    return {"status": status, "databases": {"market_meta": payload}}


def _materialize_market_meta(
    *,
    run_id: str,
    day_context: dict[str, Any],
    raw_context: dict[str, str],
    snapshot: TdxStaticSnapshot,
    manifest_hash: str,
    day_db_path: Path,
    meta_db_path: Path,
) -> None:
    with duckdb.connect(str(meta_db_path)) as con:
        catalog = _catalog_name(con)
        con.execute(f"attach '{day_db_path.as_posix()}' as day_source (read_only)")
        _ensure_schema(con, catalog)
        _clear_tables(con, catalog)
        con.executemany(
            f"insert into {_table_fqn(catalog, MARKET_META_SCHEMA_NAME, 'instrument_master')} values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    row["symbol"],
                    row["asset_type"],
                    row["exchange"],
                    row["name"],
                    row["list_dt"],
                    row["delist_dt"],
                    f"{run_id}:static",
                    MARKET_META_SCHEMA_VERSION,
                    MARKET_META_RULE_VERSION,
                    manifest_hash,
                )
                for row in snapshot.instruments
            ],
        )
        _insert_trade_calendar(
            con=con,
            catalog=catalog,
            day_source_run_id=day_context["day_source_run_id"],
            manifest_hash=manifest_hash,
        )
        _insert_tradability_fact(
            con=con,
            catalog=catalog,
            day_source_run_id=day_context["day_source_run_id"],
            manifest_hash=manifest_hash,
        )
        con.executemany(
            f"insert into {_table_fqn(catalog, MARKET_META_SCHEMA_NAME, 'industry_block_relation')} values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    row["symbol"],
                    row["asset_type"],
                    row["relation_type"],
                    row["relation_code"],
                    row["relation_name"],
                    day_context["snapshot_trade_dt"],
                    None,
                    f"{run_id}:static",
                    MARKET_META_SCHEMA_VERSION,
                    MARKET_META_RULE_VERSION,
                    manifest_hash,
                )
                for row in [*snapshot.industry_relations, *snapshot.block_relations]
            ],
        )
        unresolved = _measure_unresolved_gaps(con, catalog)
        con.execute(
            f"insert into {_table_fqn(catalog, MARKET_META_SCHEMA_NAME, 'source_manifest')} values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                f"market_meta:{manifest_hash[:16]}",
                manifest_hash,
                "instrument_master trade_calendar tradability_fact industry_block_relation",
                run_id,
                day_context["day_source_run_id"],
                MARKET_META_SCHEMA_VERSION,
                MARKET_META_RULE_VERSION,
                "passed",
                raw_context["raw_source_manifest_hash"],
                day_context["day_source_manifest_hash"],
                day_context["hq_cache_root"],
                _root_hash(snapshot.source_files, prefix=day_context["hq_cache_root"]),
                day_context["blocknew_root"],
                _root_hash(snapshot.source_files, prefix=day_context["blocknew_root"]),
                unresolved["unresolved_symbol_count"],
                unresolved["unresolved_gap_count"],
                json.dumps(
                    {
                        "tradability_source_boundary": "tdx_direct_only",
                        "negative_fact_policy": "no_inferred_negative_facts",
                        "adapter_status": "not_authorized_in_card_23",
                    },
                    ensure_ascii=False,
                ),
            ],
        )
        con.execute(
            f"insert into {_table_fqn(catalog, MARKET_META_SCHEMA_NAME, 'schema_version')} values (?, ?, ?, ?, ?, ?)",
            [
                MARKET_META_SCHEMA_VERSION,
                MARKET_META_RULE_VERSION,
                datetime.utcnow(),
                run_id,
                manifest_hash,
                day_context["day_source_run_id"],
            ],
        )
        con.execute("detach day_source")


def _load_day_context(
    day_db_path: Path,
    *,
    hq_cache_root: Path,
    blocknew_root: Path,
) -> dict[str, Any]:
    with duckdb.connect(str(day_db_path), read_only=True) as con:
        row = con.execute(
            """
            select any_value(source_run_id), any_value(source_manifest_hash), max(trade_dt)
            from market_base_day.market_base_day.base_bar
            where analysis_price_line = 'backward'
            """
        ).fetchone()
    if row is None or row[0] is None:
        raise RuntimeError("market_base_day base_bar is empty")
    return {
        "day_source_run_id": row[0],
        "day_source_manifest_hash": row[1],
        "snapshot_trade_dt": str(row[2]),
        "hq_cache_root": hq_cache_root.as_posix(),
        "blocknew_root": blocknew_root.as_posix(),
    }


def _load_raw_context(raw_db_path: Path) -> dict[str, str]:
    with duckdb.connect(str(raw_db_path), read_only=True) as con:
        row = con.execute(
            """
            select run_id, source_manifest_hash
            from raw_market.raw_market.ingest_run
            order by finished_at desc, run_id desc
            limit 1
            """
        ).fetchone()
    if row is None:
        raise RuntimeError("raw_market ingest_run is empty")
    return {"raw_source_run_id": row[0], "raw_source_manifest_hash": row[1]}


def _resolve_symbol_scope(
    *,
    static_snapshot: TdxStaticSnapshot,
    day_db_path: Path,
    symbols: set[str] | None,
    limit_symbols: int | None,
) -> list[str] | None:
    if symbols:
        return sorted(symbols)
    if limit_symbols is None:
        return None
    instrument_symbols = [row["symbol"] for row in static_snapshot.instruments]
    day_symbols = _load_day_symbols(day_db_path)
    ordered = [symbol for symbol in instrument_symbols if symbol in day_symbols]
    return ordered[:limit_symbols]


def _load_day_symbols(day_db_path: Path) -> set[str]:
    with duckdb.connect(str(day_db_path), read_only=True) as con:
        return {
            row[0]
            for row in con.execute(
                """
                select distinct symbol
                from market_base_day.market_base_day.base_bar
                where analysis_price_line = 'backward'
                """
            ).fetchall()
        }


def _filter_snapshot(snapshot: TdxStaticSnapshot, symbols: list[str] | None) -> TdxStaticSnapshot:
    if not symbols:
        return snapshot
    scope = set(symbols)
    return TdxStaticSnapshot(
        instruments=[row for row in snapshot.instruments if row["symbol"] in scope],
        industry_relations=[row for row in snapshot.industry_relations if row["symbol"] in scope],
        block_relations=[row for row in snapshot.block_relations if row["symbol"] in scope],
        source_files=snapshot.source_files,
    )


def _insert_trade_calendar(
    *,
    con: duckdb.DuckDBPyConnection,
    catalog: str,
    day_source_run_id: str,
    manifest_hash: str,
) -> None:
    con.execute(
        f"""
        insert into {_table_fqn(catalog, MARKET_META_SCHEMA_NAME, 'trade_calendar')}
        select
            upper(substr(symbol, 1, 2)),
            trade_dt,
            true,
            ?,
            ?,
            ?,
            ?
        from day_source.market_base_day.base_bar
        where analysis_price_line = 'backward'
        group by 1, 2
        """,
        [day_source_run_id, MARKET_META_SCHEMA_VERSION, MARKET_META_RULE_VERSION, manifest_hash],
    )


def _insert_tradability_fact(
    *,
    con: duckdb.DuckDBPyConnection,
    catalog: str,
    day_source_run_id: str,
    manifest_hash: str,
) -> None:
    con.execute(
        f"""
        insert into {_table_fqn(catalog, MARKET_META_SCHEMA_NAME, 'tradability_fact')}
        select
            base.symbol,
            base.asset_type,
            base.trade_dt,
            'tradable',
            null,
            'tdx_direct',
            ?,
            ?,
            ?,
            ?
        from day_source.market_base_day.base_bar as base
        join {_table_fqn(catalog, MARKET_META_SCHEMA_NAME, 'instrument_master')} as instrument
          on instrument.symbol = base.symbol
         and instrument.asset_type = base.asset_type
        where base.analysis_price_line = 'backward'
        """,
        [day_source_run_id, MARKET_META_SCHEMA_VERSION, MARKET_META_RULE_VERSION, manifest_hash],
    )


def _measure_unresolved_gaps(
    con: duckdb.DuckDBPyConnection,
    catalog: str,
) -> dict[str, int]:
    table_fqn = lambda name: _table_fqn(catalog, MARKET_META_SCHEMA_NAME, name)
    row = con.execute(
        f"""
        with expected as (
            select i.symbol, i.asset_type, c.trade_dt
            from {table_fqn('instrument_master')} i
            join {table_fqn('trade_calendar')} c on c.exchange = i.exchange and c.is_open
        ),
        uncovered as (
            select expected.symbol, expected.asset_type, expected.trade_dt
            from expected
            left join {table_fqn('tradability_fact')} t
              on t.symbol = expected.symbol
             and t.asset_type = expected.asset_type
             and t.trade_dt = expected.trade_dt
            where t.symbol is null
        )
        select count(distinct symbol), count(*)
        from uncovered
        """
    ).fetchone()
    return {
        "unresolved_symbol_count": int(row[0] or 0),
        "unresolved_gap_count": int(row[1] or 0),
    }


def _ensure_schema(con: duckdb.DuckDBPyConnection, catalog: str) -> None:
    con.execute(f"create schema if not exists {MARKET_META_SCHEMA_NAME}")
    statements = [
        f"""create table if not exists {_table_fqn(catalog, MARKET_META_SCHEMA_NAME, 'instrument_master')} (
            symbol varchar, asset_type varchar, exchange varchar, name varchar, list_dt date, delist_dt date,
            source_run_id varchar, schema_version varchar, rule_version varchar, source_manifest_hash varchar,
            primary key(symbol, asset_type)
        )""",
        f"""create table if not exists {_table_fqn(catalog, MARKET_META_SCHEMA_NAME, 'trade_calendar')} (
            exchange varchar, trade_dt date, is_open boolean, source_run_id varchar, schema_version varchar,
            rule_version varchar, source_manifest_hash varchar, primary key(exchange, trade_dt)
        )""",
        f"""create table if not exists {_table_fqn(catalog, MARKET_META_SCHEMA_NAME, 'tradability_fact')} (
            symbol varchar, asset_type varchar, trade_dt date, tradability_status varchar, blocked_reason varchar,
            source_role varchar, source_run_id varchar, schema_version varchar, rule_version varchar,
            source_manifest_hash varchar, primary key(symbol, asset_type, trade_dt)
        )""",
        f"""create table if not exists {_table_fqn(catalog, MARKET_META_SCHEMA_NAME, 'industry_block_relation')} (
            symbol varchar, asset_type varchar, relation_type varchar, relation_code varchar, relation_name varchar,
            effective_from date, effective_to date, source_run_id varchar, schema_version varchar,
            rule_version varchar, source_manifest_hash varchar,
            primary key(symbol, asset_type, relation_type, relation_code, effective_from)
        )""",
        f"""create table if not exists {_table_fqn(catalog, MARKET_META_SCHEMA_NAME, 'source_manifest')} (
            manifest_id varchar, source_manifest_hash varchar primary key, dataset_scope varchar,
            generated_by_run_id varchar, source_run_id varchar, schema_version varchar, rule_version varchar,
            audit_status varchar, raw_source_manifest_hash varchar, day_source_manifest_hash varchar,
            hq_cache_root varchar, hq_cache_hash varchar, blocknew_root varchar, blocknew_hash varchar,
            unresolved_symbol_count bigint, unresolved_gap_count bigint, details_json varchar
        )""",
        f"""create table if not exists {_table_fqn(catalog, MARKET_META_SCHEMA_NAME, 'schema_version')} (
            schema_version varchar, rule_version varchar, effective_from timestamp, registered_by_run_id varchar,
            source_manifest_hash varchar, source_run_id varchar, primary key(schema_version, rule_version)
        )""",
    ]
    for statement in statements:
        con.execute(statement)


def _clear_tables(con: duckdb.DuckDBPyConnection, catalog: str) -> None:
    for table_name in [
        "source_manifest",
        "schema_version",
        "industry_block_relation",
        "tradability_fact",
        "trade_calendar",
        "instrument_master",
    ]:
        con.execute(f"delete from {_table_fqn(catalog, MARKET_META_SCHEMA_NAME, table_name)}")


def _manifest_hash(
    *,
    day_context: dict[str, Any],
    raw_context: dict[str, str],
    static_files: list[dict[str, str]],
    symbol_scope: list[str] | None,
) -> str:
    payload = {
        "raw": raw_context,
        "day": day_context,
        "static_files": static_files,
        "symbol_scope": symbol_scope,
    }
    return hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()


def _root_hash(static_files: list[dict[str, str]], *, prefix: str) -> str:
    filtered = [item for item in static_files if item["path"].startswith(prefix)]
    return hashlib.sha256(
        json.dumps(filtered, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()


def _count_equals_distinct(
    con: duckdb.DuckDBPyConnection,
    table_name: str,
    distinct_expr: str,
) -> bool:
    row_count = con.execute(f"select count(*) from {table_name}").fetchone()[0]
    if row_count == 0:
        return True
    return bool(
        con.execute(
            f"select count(*) = count(distinct {distinct_expr}) from {table_name}"
        ).fetchone()[0]
    )


def _meta_status(required_tables: set[str], tables: set[str], payload: dict[str, Any]) -> bool:
    checks = [
        required_tables.issubset(tables),
        payload["instrument_master_natural_key_unique"],
        payload["trade_calendar_natural_key_unique"],
        payload["tradability_fact_natural_key_unique"],
        payload["industry_block_relation_natural_key_unique"],
        payload["lineage_complete"],
        payload["non_empty_supporting_tables"],
    ]
    return all(checks)


def _catalog_name(con: duckdb.DuckDBPyConnection) -> str:
    return str(con.execute("pragma database_list").fetchone()[1])


def _table_fqn(catalog: str, schema_name: str, table_name: str) -> str:
    return f"{catalog}.{schema_name}.{table_name}"


def _write_report(*, report_dir: Path, payload: dict[str, Any]) -> None:
    (report_dir / "market_meta_summary.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
