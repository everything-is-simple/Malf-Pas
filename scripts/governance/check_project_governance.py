from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from malf_pas.governance.checks import run_checks


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Malf-Pas project governance checks.")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)

    repo_root = args.repo_root.resolve()
    findings = run_checks(repo_root)
    if findings:
        for finding in findings:
            print(f"FAIL {finding.path}: {finding.message}")
        return 1

    print("Malf-Pas governance checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
