from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from malf_pas.governance.checks import run_checks


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Malf-Pas workflow hook checks.")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--hook-event", default="Unknown")
    args = parser.parse_args(argv)

    findings = run_checks(args.repo_root.resolve())
    if findings:
        print(f"Malf-Pas workflow hook blocked at {args.hook_event}.")
        for finding in findings:
            print(f"FAIL {finding.path}: {finding.message}")
        return 1

    print(f"Malf-Pas workflow hook passed at {args.hook_event}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
