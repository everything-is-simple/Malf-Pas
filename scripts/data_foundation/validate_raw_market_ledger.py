from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from malf_pas.data_foundation.raw_market import validate_raw_market_ledger


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the raw_market ledger.")
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    summary = validate_raw_market_ledger(args.db)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"raw_market validation: {summary['status']}")
        for key, value in summary.items():
            if key == "status":
                continue
            print(f"- {key}: {value}")
    return 0 if summary["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
