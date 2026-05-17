from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

FORBIDDEN_FORMAL_TRUTH = ["TuShare", "baostock", "AKShare"]
PREVIOUS_DATA_DBS = [
    "raw_market.duckdb",
    "market_base_day.duckdb",
    "market_base_week.duckdb",
    "market_base_month.duckdb",
    "market_meta.duckdb",
]
EXPECTED_MARKET_TABLES = {
    "raw_market.duckdb": [
        "raw_market_bar",
        "raw_market_reject_audit",
        "raw_market_source_file",
        "raw_market_sync_run",
        "raw_schema_version",
    ],
    "market_base_day.duckdb": [
        "market_base_bar",
        "market_base_dirty_scope",
        "market_base_latest",
        "market_base_run",
        "market_base_schema_version",
    ],
    "market_base_week.duckdb": [
        "market_base_bar",
        "market_base_dirty_scope",
        "market_base_latest",
        "market_base_run",
        "market_base_schema_version",
    ],
    "market_base_month.duckdb": [
        "market_base_bar",
        "market_base_dirty_scope",
        "market_base_latest",
        "market_base_run",
        "market_base_schema_version",
    ],
    "market_meta.duckdb": [
        "industry_classification",
        "instrument_alias",
        "instrument_master",
        "meta_run",
        "meta_schema_version",
        "meta_source_manifest",
        "tradability_fact",
        "trade_calendar",
        "universe_membership",
    ],
}


def build_source_inventory(
    *,
    tdx_offline_root: Path,
    tdx_client_root: Path,
    asteria_data_root: Path,
) -> dict[str, Any]:
    tdx_offline = tdx_offline_root.resolve()
    tdx_client = tdx_client_root.resolve()
    asteria_data = asteria_data_root.resolve()
    offline_families = _inventory_tdx_offline_root(tdx_offline)
    client_families = _inventory_tdx_client_root(tdx_client)

    return {
        "source_roles": {
            "current_truth_roots": [str(tdx_offline), str(tdx_client)],
            "previous_reference_root": str(asteria_data),
            "forbidden_formal_truth": FORBIDDEN_FORMAL_TRUTH,
        },
        "fingerprint_policy": {
            "fields": [
                "path",
                "size",
                "mtime",
                "content_hash",
                "source_root",
                "source_revision",
            ],
            "content_hash": "sha256",
            "source_revision": "file-metadata-revision-v1",
        },
        "tdx_offline_data": {
            "root": str(tdx_offline),
            "exists": tdx_offline.exists(),
            "families": offline_families,
        },
        "tdx_client": {
            "root": str(tdx_client),
            "exists": tdx_client.exists(),
            "families": client_families,
        },
        "previous_asteria_data_readonly_reference": _inventory_previous_asteria_data(
            asteria_data
        ),
        "week_month_availability": _week_month_availability(tdx_client),
        "tradability_availability": _tradability_availability(tdx_client),
    }


def _inventory_tdx_offline_root(root: Path) -> dict[str, Any]:
    return {
        "stock": _adjusted_text_family(root / "stock"),
        "index": _adjusted_text_family(root / "index"),
        "block": _adjusted_text_family(root / "block"),
        "raw_day": {
            market: _file_family(root / "raw" / market / "lday", "*.day")
            for market in ["bj", "sh", "sz"]
        },
    }


def _inventory_tdx_client_root(root: Path) -> dict[str, Any]:
    return {
        "vipdoc_day": {
            market: _file_family(root / "vipdoc" / market / "lday", "*.day")
            for market in ["bj", "sh", "sz"]
        },
        "vipdoc_week": {
            market: _file_family(root / "vipdoc" / market / "lweek", "*.day")
            for market in ["bj", "sh", "sz"]
        },
        "vipdoc_month": {
            market: _file_family(root / "vipdoc" / market / "lmonth", "*.day")
            for market in ["bj", "sh", "sz"]
        },
        "hq_cache": _extension_family(root / "T0002" / "hq_cache"),
        "blocknew": _extension_family(root / "T0002" / "blocknew"),
    }


def _adjusted_text_family(root: Path) -> dict[str, Any]:
    return {
        adj: _file_family(root / adj, "*.txt")
        for adj in ["Backward-Adjusted", "Forward-Adjusted", "Non-Adjusted"]
    }


def _file_family(path: Path, pattern: str) -> dict[str, Any]:
    if not path.exists():
        return {"path": str(path), "exists": False, "file_count": 0, "sample": None}
    files = sorted(item for item in path.glob(pattern) if item.is_file())
    sample = _sample_file(files[0]) if files else None
    return {
        "path": str(path),
        "exists": True,
        "file_count": len(files),
        "sample": sample,
    }


def _extension_family(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"path": str(path), "exists": False, "extension_counts": {}}
    counts: dict[str, int] = {}
    for item in path.rglob("*"):
        if not item.is_file():
            continue
        suffix = item.suffix or "<no_extension>"
        counts[suffix] = counts.get(suffix, 0) + 1
    return {
        "path": str(path),
        "exists": True,
        "extension_counts": dict(sorted(counts.items())),
    }


def _sample_file(path: Path) -> dict[str, Any]:
    stat = path.stat()
    return {
        "path": str(path),
        "size": stat.st_size,
        "mtime": stat.st_mtime,
        "content_hash": _sha256(path),
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _inventory_previous_asteria_data(root: Path) -> dict[str, Any]:
    return {
        "root": str(root),
        "role": "reference_baseline_only",
        "current_truth_owner": False,
        "schema_migration_source": False,
        "runner_migration_source": False,
        "scratch_or_output_root": False,
        "databases": {name: _inspect_previous_duckdb(root / name) for name in PREVIOUS_DATA_DBS},
    }


def _inspect_previous_duckdb(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"path": str(path), "status": "missing", "size": None, "tables": {}}
    result: dict[str, Any] = {
        "path": str(path),
        "status": "present",
        "size": path.stat().st_size,
        "tables": {},
    }
    try:
        import duckdb  # type: ignore[import-not-found]

        con = duckdb.connect(str(path), read_only=True)
        try:
            rows = con.execute(
                "select table_name from information_schema.tables "
                "where table_schema='main' order by table_name"
            ).fetchall()
            for (table_name,) in rows:
                count = con.execute(f'select count(*) from "{table_name}"').fetchone()[0]
                result["tables"][table_name] = {"rows": count}
        finally:
            con.close()
    except Exception as exc:
        result["status"] = "present_unreadable"
        result["read_error"] = str(exc)
    return result


def _week_month_availability(tdx_client_root: Path) -> dict[str, Any]:
    direct_dirs = [
        tdx_client_root / "vipdoc" / market / timeframe
        for market in ["bj", "sh", "sz"]
        for timeframe in ["lweek", "lmonth"]
    ]
    direct_present = [path for path in direct_dirs if path.exists()]
    status = "direct" if len(direct_present) == len(direct_dirs) else "day-derived"
    return {
        "status": status,
        "direct_source_directories_found": [str(path) for path in direct_present],
        "direct_parent": "vipdoc day source family and tdx_offline raw day family",
        "rule_version": "data-foundation-week-month-from-day-v1",
        "reference_baseline": [
            "H:/Asteria-data/market_base_week.duckdb",
            "H:/Asteria-data/market_base_month.duckdb",
        ],
    }


def _tradability_availability(tdx_client_root: Path) -> dict[str, Any]:
    candidate_paths = [
        tdx_client_root / "T0002" / "hq_cache" / name
        for name in ["base.dbf", "tdxhy.cfg", "tdxzs.cfg", "tdxstat.cfg"]
    ]
    present = [path for path in candidate_paths if path.exists()]
    return {
        "status": "blocked",
        "tdx_candidate_paths_found": [str(path) for path in present],
        "gap_scope": [
            "ST",
            "halt",
            "delisting",
            "tradable calendar reason",
        ],
        "reference_baseline": "H:/Asteria-data/market_meta.duckdb",
    }


def registry_rows_for_previous_data(inventory: dict[str, Any]) -> list[dict[str, Any]]:
    databases = inventory["previous_asteria_data_readonly_reference"]["databases"]
    rows: list[dict[str, Any]] = []
    for name in PREVIOUS_DATA_DBS:
        db = databases[name]
        rows.append(
            {
                "name": name,
                "path": _slash_path(db["path"]),
                "status": db["status"],
                "required": True,
                "table_count": len(db.get("tables", {})),
            }
        )
    return rows


def _slash_path(raw_path: str) -> str:
    return raw_path.replace("\\", "/")
