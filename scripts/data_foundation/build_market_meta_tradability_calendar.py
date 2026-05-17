from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from malf_pas.core.paths import MalfPasPaths
from malf_pas.data_foundation.market_meta import build_market_meta


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build market_meta tradability/calendar ledger.")
    parser.add_argument("--mode", choices=["full", "bounded", "audit-only"], required=True)
    parser.add_argument("--run-id", default="market-meta-tradability-calendar-card-20260517-01")
    parser.add_argument("--raw-db", type=Path, default=Path("H:/Malf-Pas-data/raw_market.duckdb"))
    parser.add_argument(
        "--day-db",
        type=Path,
        default=Path("H:/Malf-Pas-data/market_base_day.duckdb"),
    )
    parser.add_argument(
        "--meta-db",
        type=Path,
        default=Path("H:/Malf-Pas-data/market_meta.duckdb"),
    )
    parser.add_argument(
        "--hq-cache-root",
        type=Path,
        default=Path("H:/new_tdx64/T0002/hq_cache"),
    )
    parser.add_argument(
        "--blocknew-root",
        type=Path,
        default=Path("H:/new_tdx64/T0002/blocknew"),
    )
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path(
            "H:/Malf-Pas-reprot/data-foundation/market-meta-tradability-calendar-card-20260517-01"
        ),
    )
    parser.add_argument("--symbols", nargs="*", default=None)
    parser.add_argument("--limit-symbols", type=int, default=None)
    args = parser.parse_args(argv)

    repo_root = Path(__file__).resolve().parents[2]
    result = build_market_meta(
        run_id=args.run_id,
        mode=args.mode,
        paths=MalfPasPaths.from_env(repo_root),
        raw_db_path=args.raw_db,
        day_db_path=args.day_db,
        meta_db_path=args.meta_db,
        hq_cache_root=args.hq_cache_root,
        blocknew_root=args.blocknew_root,
        report_dir=args.report_dir,
        symbols=set(args.symbols) if args.symbols else None,
        limit_symbols=args.limit_symbols,
    )
    print(json.dumps(result.__dict__, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
