from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from malf_pas.data_foundation.market_base import validate_market_base_day_week_month


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate market_base day/week/month ledgers.")
    parser.add_argument("--day-db", type=Path, required=True)
    parser.add_argument("--week-db", type=Path, required=True)
    parser.add_argument("--month-db", type=Path, required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    summary = validate_market_base_day_week_month(
        day_db_path=args.day_db,
        week_db_path=args.week_db,
        month_db_path=args.month_db,
    )
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"market_base validation: {summary['status']}")
        for name, payload in summary["databases"].items():
            print(f"- {name}: {payload['status']} / rows={payload['base_bar_row_count']}")
    return 0 if summary["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
