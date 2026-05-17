from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from malf_pas.core.paths import MalfPasPaths
from malf_pas.data_foundation.raw_market import build_raw_market_ledger


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the raw_market full-build ledger.")
    parser.add_argument("--mode", choices=["full", "bounded", "audit-only", "resume", "daily_incremental"], required=True)
    parser.add_argument("--run-id", default="raw-market-full-build-ledger-card-20260517-01")
    parser.add_argument("--db", type=Path, default=Path("H:/Malf-Pas-data/raw_market.duckdb"))
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path("H:/Malf-Pas-reprot/data-foundation/raw-market-full-build-ledger-card-20260517-01"),
    )
    parser.add_argument("--tdx-offline-root", type=Path, default=Path("H:/tdx_offline_Data"))
    parser.add_argument("--tdx-client-root", type=Path, default=Path("H:/new_tdx64"))
    parser.add_argument("--asteria-data-root", type=Path, default=Path("H:/Asteria-data"))
    parser.add_argument("--symbols", nargs="*", default=None)
    parser.add_argument("--limit-files", type=int, default=None)
    args = parser.parse_args(argv)

    repo_root = Path(__file__).resolve().parents[2]
    result = build_raw_market_ledger(
        run_id=args.run_id,
        mode=args.mode,
        paths=MalfPasPaths.from_env(repo_root),
        offline_root=args.tdx_offline_root,
        client_root=args.tdx_client_root,
        asteria_data_root=args.asteria_data_root,
        db_path=args.db,
        report_dir=args.report_dir,
        symbols=set(args.symbols) if args.symbols else None,
        limit_files=args.limit_files,
    )
    print(json.dumps(result.__dict__, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
