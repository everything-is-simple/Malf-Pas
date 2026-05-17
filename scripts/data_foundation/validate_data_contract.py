from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from malf_pas.data_foundation.contract import contract_summary, load_contract_registry


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the Data Foundation contract registry.")
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path("governance/data_module_db_contract_registry.toml"),
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON to stdout.")
    args = parser.parse_args(argv)

    registry = load_contract_registry(args.registry)
    summary = contract_summary(args.registry, registry)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"Data contract validation: {summary['status']}")
        for finding in summary["findings"]:
            print(f"- {finding}")
    return 0 if summary["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
