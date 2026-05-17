from __future__ import annotations

import csv
import hashlib
import json
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import duckdb

from malf_pas.core.paths import MalfPasPaths
from malf_pas.data_foundation.raw_market import validate_raw_market_ledger

MARKET_BASE_SCHEMA_VERSION = "market-base-ledger-v1"
MARKET_BASE_DAY_RULE_VERSION = "market-base-day-backward-v1"
MARKET_BASE_WEEK_RULE_VERSION = "market-base-week-from-day-v1"
MARKET_BASE_MONTH_RULE_VERSION = "market-base-month-from-day-v1"
ANALYSIS_PRICE_LINE = "backward"


@dataclass(frozen=True)
class BuildResult:
    run_id: str
    mode: str
    day_db_path: Path
    week_db_path: Path
    month_db_path: Path
    report_dir: Path
    source_manifest_hash: str
    raw_source_run_id: str
    day_row_count: int
    week_row_count: int
    month_row_count: int


def build_market_base_day_week_month(
    *,
    run_id: str,
    mode: str,
    paths: MalfPasPaths,
    raw_db_path: Path,
    day_db_path: Path,
    week_db_path: Path,
    month_db_path: Path,
    report_dir: Path,
    symbols: set[str] | None = None,
    limit_symbols: int | None = None,
) -> BuildResult:
    supported_modes = {"full", "bounded", "audit-only"}
    if mode not in supported_modes:
        raise ValueError(f"unsupported mode: {mode}")

    raw_summary = validate_raw_market_ledger(raw_db_path)
    if raw_summary["status"] != "passed":
        raise RuntimeError("raw_market ledger must validate before building market_base")

    report_dir.mkdir(parents=True, exist_ok=True)
    day_db_path.parent.mkdir(parents=True, exist_ok=True)
    paths.temp_root.mkdir(parents=True, exist_ok=True)

    raw_context = _load_raw_context(raw_db_path)
    symbol_scope = _load_symbol_scope(raw_db_path, symbols=symbols, limit_symbols=limit_symbols)

    if mode != "audit-only":
        _build_day_db(
            db_path=day_db_path,
            raw_db_path=raw_db_path,
            run_id=f"{run_id}:day",
            raw_source_run_id=raw_context["raw_source_run_id"],
            source_manifest_hash=raw_context["source_manifest_hash"],
            symbol_scope=symbol_scope,
            temp_root=paths.temp_root,
        )
        _build_derived_db(
            db_path=week_db_path,
            day_db_path=day_db_path,
            schema_name="market_base_week",
            timeframe="week",
            rule_version=MARKET_BASE_WEEK_RULE_VERSION,
            run_id=f"{run_id}:week",
            day_source_run_id=f"{run_id}:day",
            source_manifest_hash=raw_context["source_manifest_hash"],
            temp_root=paths.temp_root,
        )
        _build_derived_db(
            db_path=month_db_path,
            day_db_path=day_db_path,
            schema_name="market_base_month",
            timeframe="month",
            rule_version=MARKET_BASE_MONTH_RULE_VERSION,
            run_id=f"{run_id}:month",
            day_source_run_id=f"{run_id}:day",
            source_manifest_hash=raw_context["source_manifest_hash"],
            temp_root=paths.temp_root,
        )

    summary = validate_market_base_day_week_month(
        day_db_path=day_db_path,
        week_db_path=week_db_path,
        month_db_path=month_db_path,
    )
    _write_report(
        report_dir=report_dir,
        payload={
            "run_id": run_id,
            "mode": mode,
            "source_manifest_hash": raw_context["source_manifest_hash"],
            "raw_source_run_id": raw_context["raw_source_run_id"],
            "symbol_scope": symbol_scope,
            "summary": summary,
        },
    )
    return BuildResult(
        run_id=run_id,
        mode=mode,
        day_db_path=day_db_path,
        week_db_path=week_db_path,
        month_db_path=month_db_path,
        report_dir=report_dir,
        source_manifest_hash=raw_context["source_manifest_hash"],
        raw_source_run_id=raw_context["raw_source_run_id"],
        day_row_count=summary["databases"]["market_base_day"]["base_bar_row_count"],
        week_row_count=summary["databases"]["market_base_week"]["base_bar_row_count"],
        month_row_count=summary["databases"]["market_base_month"]["base_bar_row_count"],
    )


def validate_market_base_day_week_month(
    *,
    day_db_path: Path,
    week_db_path: Path,
    month_db_path: Path,
) -> dict[str, Any]:
    databases = {
        "market_base_day": _validate_single_db(day_db_path, "market_base_day", include_analysis=True),
        "market_base_week": _validate_single_db(day_db_path=week_db_path if False else week_db_path, schema_name="market_base_week"),
        "market_base_month": _validate_single_db(day_db_path=month_db_path if False else month_db_path, schema_name="market_base_month"),
    }
    status = "passed" if all(item["status"] == "passed" for item in databases.values()) else "failed"
    return {"status": status, "databases": databases}


def _validate_single_db(
    day_db_path: Path,
    schema_name: str,
    include_analysis: bool = False,
) -> dict[str, Any]:
    required_tables = {
        "base_bar",
        "latest_pointer",
        "base_run",
        "dirty_scope",
        "source_manifest",
        "schema_version",
    }
    with duckdb.connect(str(day_db_path), read_only=True) as con:
        catalog = _catalog_name(con)
        tables = {
            row[0]
            for row in con.execute(
                """
                select table_name
                from information_schema.tables
                where table_catalog = ? and table_schema = ?
                """,
                [catalog, schema_name],
            ).fetchall()
        }
        base_bar_fqn = _table_fqn(catalog, schema_name, "base_bar")
        latest_fqn = _table_fqn(catalog, schema_name, "latest_pointer")
        dirty_scope_fqn = _table_fqn(catalog, schema_name, "dirty_scope")
        source_manifest_fqn = _table_fqn(catalog, schema_name, "source_manifest")
        schema_version_fqn = _table_fqn(catalog, schema_name, "schema_version")
        base_run_fqn = _table_fqn(catalog, schema_name, "base_run")
        row_count = con.execute(f"select count(*) from {base_bar_fqn}").fetchone()[0]
        symbol_count = con.execute(f"select count(distinct symbol) from {base_bar_fqn}").fetchone()[0]
        min_bar_dt, max_bar_dt = con.execute(
            f"select min(bar_dt), max(bar_dt) from {base_bar_fqn}"
        ).fetchone()
        natural_key_unique = (
            con.execute(
                f"""
                select count(*) = count(distinct (symbol, asset_type, timeframe, bar_dt{", analysis_price_line" if include_analysis else ""}))
                from {base_bar_fqn}
                """
            ).fetchone()[0]
            if row_count
            else True
        )
        latest_pointer_unique = (
            con.execute(
                f"select count(*) = count(distinct (symbol, asset_type, timeframe)) from {latest_fqn}"
            ).fetchone()[0]
            if con.execute(f"select count(*) from {latest_fqn}").fetchone()[0]
            else True
        )
        lineage_complete = con.execute(
            f"""
            select
                count(*) = count(source_run_id)
                and count(*) = count(schema_version)
                and count(*) = count(rule_version)
                and count(*) = count(source_manifest_hash)
            from {base_bar_fqn}
            """
        ).fetchone()[0]
        required_tables_present = required_tables.issubset(tables)
        non_empty_supporting_tables = all(
            con.execute(f"select count(*) from {table_fqn}").fetchone()[0] > 0
            for table_fqn in [latest_fqn, base_run_fqn, dirty_scope_fqn, source_manifest_fqn, schema_version_fqn]
        )
    status = "passed" if all([required_tables_present, natural_key_unique, latest_pointer_unique, lineage_complete, non_empty_supporting_tables]) else "failed"
    return {
        "status": status,
        "required_tables_present": sorted(required_tables & tables) if required_tables_present else sorted(tables),
        "base_bar_row_count": row_count,
        "symbol_count": symbol_count,
        "min_bar_dt": str(min_bar_dt) if min_bar_dt is not None else None,
        "max_bar_dt": str(max_bar_dt) if max_bar_dt is not None else None,
        "natural_key_unique": bool(natural_key_unique),
        "latest_pointer_unique": bool(latest_pointer_unique),
        "lineage_complete": bool(lineage_complete),
        "non_empty_supporting_tables": bool(non_empty_supporting_tables),
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
    return {"raw_source_run_id": row[0], "source_manifest_hash": row[1]}


def _load_symbol_scope(
    raw_db_path: Path,
    *,
    symbols: set[str] | None,
    limit_symbols: int | None,
) -> list[str] | None:
    if symbols:
        scope = sorted(symbols)
    elif limit_symbols is not None:
        with duckdb.connect(str(raw_db_path), read_only=True) as con:
            scope = [
                row[0]
                for row in con.execute(
                    """
                    select distinct symbol
                    from raw_market.raw_market.raw_bar
                    order by symbol
                    limit ?
                    """,
                    [limit_symbols],
                ).fetchall()
            ]
    else:
        scope = []
    return scope or None


def _build_day_db(
    *,
    db_path: Path,
    raw_db_path: Path,
    run_id: str,
    raw_source_run_id: str,
    source_manifest_hash: str,
    symbol_scope: list[str] | None,
    temp_root: Path,
) -> None:
    with duckdb.connect(str(db_path)) as con:
        catalog = _catalog_name(con)
        con.execute(f"attach '{raw_db_path.as_posix()}' as raw_source (read_only)")
        _ensure_schema(con, catalog, "market_base_day", include_analysis=True)
        _clear_tables(con, catalog, "market_base_day")
        _prepare_symbol_scope(con, symbol_scope)
        where_clause = "where raw.timeframe = 'day'" + (" and raw.symbol in (select symbol from symbol_scope)" if symbol_scope else "")
        con.execute(
            f"""
            insert into {_table_fqn(catalog, 'market_base_day', 'base_bar')}
            select
                raw.symbol,
                raw.asset_type,
                'day',
                raw.bar_dt,
                raw.bar_dt,
                raw.open,
                raw.high,
                raw.low,
                raw.close,
                raw.volume,
                raw.amount,
                '{ANALYSIS_PRICE_LINE}',
                '{raw_source_run_id}',
                '{MARKET_BASE_SCHEMA_VERSION}',
                '{MARKET_BASE_DAY_RULE_VERSION}',
                '{source_manifest_hash}'
            from raw_source.raw_market.raw_bar raw
            {where_clause}
            """
        )
        _populate_latest_pointer(con, catalog, "market_base_day", include_analysis=True)
        _populate_dirty_scope(con, catalog, "market_base_day", run_id)
        _insert_source_manifest(con, catalog, "market_base_day", run_id, raw_source_run_id, source_manifest_hash, "market_base_day backward from raw_market")
        _insert_schema_version(con, catalog, "market_base_day", run_id, raw_source_run_id, source_manifest_hash, MARKET_BASE_DAY_RULE_VERSION)
        _insert_base_run(con, catalog, "market_base_day", run_id, raw_source_run_id, "day", source_manifest_hash, MARKET_BASE_DAY_RULE_VERSION)
        con.execute("detach raw_source")


def _build_derived_db(
    *,
    db_path: Path,
    day_db_path: Path,
    schema_name: str,
    timeframe: str,
    rule_version: str,
    run_id: str,
    day_source_run_id: str,
    source_manifest_hash: str,
    temp_root: Path,
) -> None:
    period_expr = "date_trunc('week', bar_dt)" if timeframe == "week" else "date_trunc('month', bar_dt)"
    with duckdb.connect(str(db_path)) as con:
        catalog = _catalog_name(con)
        con.execute(f"attach '{day_db_path.as_posix()}' as day_source (read_only)")
        _ensure_schema(con, catalog, schema_name, include_analysis=False)
        _clear_tables(con, catalog, schema_name)
        con.execute(
            f"""
            insert into {_table_fqn(catalog, schema_name, 'base_bar')}
            with source as (
                select symbol, asset_type, bar_dt, trade_dt, open, high, low, close, volume, amount
                from day_source.market_base_day.base_bar
                where analysis_price_line = '{ANALYSIS_PRICE_LINE}'
            ),
            ranked as (
                select
                    *,
                    {period_expr} as period_start,
                    row_number() over(partition by symbol, asset_type, {period_expr} order by bar_dt asc) as rn_first,
                    row_number() over(partition by symbol, asset_type, {period_expr} order by bar_dt desc) as rn_last
                from source
            ),
            grouped as (
                select
                    symbol,
                    asset_type,
                    period_start,
                    max(bar_dt) as latest_bar_dt,
                    max(trade_dt) as latest_trade_dt,
                    max(high) as high,
                    min(low) as low,
                    sum(volume) as volume,
                    sum(amount) as amount
                from ranked
                group by symbol, asset_type, period_start
            ),
            first_open as (
                select symbol, asset_type, period_start, open from ranked where rn_first = 1
            ),
            last_close as (
                select symbol, asset_type, period_start, close from ranked where rn_last = 1
            )
            select
                grouped.symbol,
                grouped.asset_type,
                '{timeframe}',
                grouped.latest_bar_dt,
                grouped.latest_trade_dt,
                first_open.open,
                grouped.high,
                grouped.low,
                last_close.close,
                grouped.volume,
                grouped.amount,
                'day',
                '{day_source_run_id}',
                '{MARKET_BASE_SCHEMA_VERSION}',
                '{rule_version}',
                '{source_manifest_hash}'
            from grouped
            join first_open using(symbol, asset_type, period_start)
            join last_close using(symbol, asset_type, period_start)
            """
        )
        _populate_latest_pointer(con, catalog, schema_name, include_analysis=False)
        _populate_dirty_scope(con, catalog, schema_name, run_id)
        _insert_source_manifest(con, catalog, schema_name, run_id, day_source_run_id, source_manifest_hash, f"{schema_name} day-derived")
        _insert_schema_version(con, catalog, schema_name, run_id, day_source_run_id, source_manifest_hash, rule_version)
        _insert_base_run(con, catalog, schema_name, run_id, day_source_run_id, timeframe, source_manifest_hash, rule_version)
        con.execute("detach day_source")


def _ensure_schema(
    con: duckdb.DuckDBPyConnection,
    catalog: str,
    schema_name: str,
    *,
    include_analysis: bool,
) -> None:
    con.execute(f"create schema if not exists {schema_name}")
    extra_fact = "analysis_price_line varchar," if include_analysis else "derived_from_timeframe varchar,"
    extra_key = ", analysis_price_line" if include_analysis else ""
    con.execute(
        f"""
        create table if not exists {_table_fqn(catalog, schema_name, 'base_bar')} (
            symbol varchar,
            asset_type varchar,
            timeframe varchar,
            bar_dt date,
            trade_dt date,
            open double,
            high double,
            low double,
            close double,
            volume bigint,
            amount double,
            {extra_fact}
            source_run_id varchar,
            schema_version varchar,
            rule_version varchar,
            source_manifest_hash varchar,
            primary key(symbol, asset_type, timeframe, bar_dt{extra_key})
        )
        """
    )
    for statement in [
        f"""create table if not exists {_table_fqn(catalog, schema_name, 'latest_pointer')} (
            symbol varchar, asset_type varchar, timeframe varchar, latest_bar_dt date, latest_trade_dt date,
            source_run_id varchar, schema_version varchar, rule_version varchar, source_manifest_hash varchar,
            primary key(symbol, asset_type, timeframe)
        )""",
        f"""create table if not exists {_table_fqn(catalog, schema_name, 'base_run')} (
            run_id varchar primary key, source_run_id varchar, timeframe varchar, rule_version varchar,
            schema_version varchar, source_manifest_hash varchar, audit_status varchar
        )""",
        f"""create table if not exists {_table_fqn(catalog, schema_name, 'dirty_scope')} (
            dirty_scope_id varchar primary key, symbol varchar, asset_type varchar, timeframe varchar,
            dirty_start_dt date, dirty_end_dt date, dirty_reason varchar, source_run_id varchar,
            schema_version varchar, rule_version varchar, source_manifest_hash varchar
        )""",
        f"""create table if not exists {_table_fqn(catalog, schema_name, 'source_manifest')} (
            manifest_id varchar, source_manifest_hash varchar primary key, dataset_scope varchar,
            generated_by_run_id varchar, source_run_id varchar, schema_version varchar, rule_version varchar, audit_status varchar
        )""",
        f"""create table if not exists {_table_fqn(catalog, schema_name, 'schema_version')} (
            schema_version varchar, rule_version varchar, effective_from timestamp, registered_by_run_id varchar,
            source_manifest_hash varchar, source_run_id varchar, primary key(schema_version, rule_version)
        )""",
    ]:
        con.execute(statement)


def _clear_tables(con: duckdb.DuckDBPyConnection, catalog: str, schema_name: str) -> None:
    for table_name in ["dirty_scope", "latest_pointer", "base_run", "source_manifest", "schema_version", "base_bar"]:
        con.execute(f"delete from {_table_fqn(catalog, schema_name, table_name)}")


def _prepare_symbol_scope(con: duckdb.DuckDBPyConnection, symbol_scope: list[str] | None) -> None:
    con.execute("drop table if exists symbol_scope")
    if not symbol_scope:
        return
    con.execute("create temp table symbol_scope(symbol varchar)")
    con.executemany("insert into symbol_scope values (?)", [(symbol,) for symbol in symbol_scope])


def _populate_latest_pointer(
    con: duckdb.DuckDBPyConnection,
    catalog: str,
    schema_name: str,
    *,
    include_analysis: bool,
) -> None:
    where_clause = f"where analysis_price_line = '{ANALYSIS_PRICE_LINE}'" if include_analysis else ""
    con.execute(
        f"""
        insert into {_table_fqn(catalog, schema_name, 'latest_pointer')}
        select
            symbol,
            asset_type,
            timeframe,
            max(bar_dt),
            max(trade_dt),
            any_value(source_run_id),
            any_value(schema_version),
            any_value(rule_version),
            any_value(source_manifest_hash)
        from {_table_fqn(catalog, schema_name, 'base_bar')}
        {where_clause}
        group by symbol, asset_type, timeframe
        """
    )


def _populate_dirty_scope(
    con: duckdb.DuckDBPyConnection,
    catalog: str,
    schema_name: str,
    run_id: str,
) -> None:
    rows = con.execute(
        f"""
        select symbol, asset_type, timeframe, min(bar_dt), max(bar_dt), any_value(source_run_id), any_value(schema_version), any_value(rule_version), any_value(source_manifest_hash)
        from {_table_fqn(catalog, schema_name, 'base_bar')}
        group by symbol, asset_type, timeframe
        """
    ).fetchall()
    con.executemany(
        f"insert into {_table_fqn(catalog, schema_name, 'dirty_scope')} values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        [
            (
                _stable_hash(f"{run_id}:{symbol}:{timeframe}:{dirty_start_dt}:{dirty_end_dt}"),
                symbol,
                asset_type,
                timeframe,
                dirty_start_dt,
                dirty_end_dt,
                "source_added",
                source_run_id,
                schema_version,
                rule_version,
                source_manifest_hash,
            )
            for symbol, asset_type, timeframe, dirty_start_dt, dirty_end_dt, source_run_id, schema_version, rule_version, source_manifest_hash in rows
        ],
    )


def _insert_source_manifest(
    con: duckdb.DuckDBPyConnection,
    catalog: str,
    schema_name: str,
    run_id: str,
    source_run_id: str,
    source_manifest_hash: str,
    dataset_scope: str,
) -> None:
    con.execute(
        f"insert into {_table_fqn(catalog, schema_name, 'source_manifest')} values (?, ?, ?, ?, ?, ?, ?, ?)",
        [f"{schema_name}:{source_manifest_hash[:16]}", source_manifest_hash, dataset_scope, run_id, source_run_id, MARKET_BASE_SCHEMA_VERSION, _rule_version_for_schema(schema_name), "passed"],
    )


def _insert_schema_version(
    con: duckdb.DuckDBPyConnection,
    catalog: str,
    schema_name: str,
    run_id: str,
    source_run_id: str,
    source_manifest_hash: str,
    rule_version: str,
) -> None:
    con.execute(
        f"insert into {_table_fqn(catalog, schema_name, 'schema_version')} values (?, ?, ?, ?, ?, ?)",
        [MARKET_BASE_SCHEMA_VERSION, rule_version, datetime.utcnow(), run_id, source_manifest_hash, source_run_id],
    )


def _insert_base_run(
    con: duckdb.DuckDBPyConnection,
    catalog: str,
    schema_name: str,
    run_id: str,
    source_run_id: str,
    timeframe: str,
    source_manifest_hash: str,
    rule_version: str,
) -> None:
    con.execute(
        f"insert into {_table_fqn(catalog, schema_name, 'base_run')} values (?, ?, ?, ?, ?, ?, ?)",
        [run_id, source_run_id, timeframe, rule_version, MARKET_BASE_SCHEMA_VERSION, source_manifest_hash, "passed"],
    )


def _rule_version_for_schema(schema_name: str) -> str:
    return {
        "market_base_day": MARKET_BASE_DAY_RULE_VERSION,
        "market_base_week": MARKET_BASE_WEEK_RULE_VERSION,
        "market_base_month": MARKET_BASE_MONTH_RULE_VERSION,
    }[schema_name]


def _catalog_name(con: duckdb.DuckDBPyConnection) -> str:
    return str(con.execute("pragma database_list").fetchone()[1])


def _table_fqn(catalog: str, schema_name: str, table_name: str) -> str:
    return f"{catalog}.{schema_name}.{table_name}"


def _stable_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _write_report(*, report_dir: Path, payload: dict[str, Any]) -> None:
    (report_dir / "market_base_day_week_month_summary.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
