from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from malf_pas.core.paths import MalfPasPaths
from malf_pas.data_foundation.market_base import build_market_base_day_week_month


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build market_base day/week/month ledgers.")
    parser.add_argument("--mode", choices=["full", "bounded", "audit-only"], required=True)
    parser.add_argument("--run-id", default="market-base-day-week-month-build-card-20260517-01")
    parser.add_argument("--raw-db", type=Path, default=Path("H:/Malf-Pas-data/raw_market.duckdb"))
    parser.add_argument("--day-db", type=Path, default=Path("H:/Malf-Pas-data/market_base_day.duckdb"))
    parser.add_argument("--week-db", type=Path, default=Path("H:/Malf-Pas-data/market_base_week.duckdb"))
    parser.add_argument("--month-db", type=Path, default=Path("H:/Malf-Pas-data/market_base_month.duckdb"))
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path("H:/Malf-Pas-reprot/data-foundation/market-base-day-week-month-build-card-20260517-01"),
    )
    parser.add_argument("--symbols", nargs="*", default=None)
    parser.add_argument("--limit-symbols", type=int, default=None)
    args = parser.parse_args(argv)

    repo_root = Path(__file__).resolve().parents[2]
    result = build_market_base_day_week_month(
        run_id=args.run_id,
        mode=args.mode,
        paths=MalfPasPaths.from_env(repo_root),
        raw_db_path=args.raw_db,
        day_db_path=args.day_db,
        week_db_path=args.week_db,
        month_db_path=args.month_db,
        report_dir=args.report_dir,
        symbols=set(args.symbols) if args.symbols else None,
        limit_symbols=args.limit_symbols,
    )
    print(json.dumps(result.__dict__, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
