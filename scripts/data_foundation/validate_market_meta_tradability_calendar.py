from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from malf_pas.data_foundation.market_meta import validate_market_meta


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate market_meta tradability/calendar ledger.")
    parser.add_argument("--meta-db", type=Path, required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    summary = validate_market_meta(meta_db_path=args.meta_db)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        payload = summary["databases"]["market_meta"]
        print(f"market_meta validation: {summary['status']}")
        print(
            "- market_meta: "
            f"{payload['tradability_fact_row_count']} tradability rows / "
            f"unresolved gaps={payload['tradability_unresolved_gap_count']}"
        )
    return 0 if summary["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
