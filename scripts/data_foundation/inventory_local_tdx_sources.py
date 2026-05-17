from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from malf_pas.data_foundation.source_inventory import build_source_inventory


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Read-only inventory of local TDX roots and prior Asteria Data DBs."
    )
    parser.add_argument("--tdx-offline-root", type=Path, default=Path("H:/tdx_offline_Data"))
    parser.add_argument("--tdx-client-root", type=Path, default=Path("H:/new_tdx64"))
    parser.add_argument("--asteria-data-root", type=Path, default=Path("H:/Asteria-data"))
    parser.add_argument("--json", action="store_true", help="Emit JSON to stdout.")
    args = parser.parse_args(argv)

    inventory = build_source_inventory(
        tdx_offline_root=args.tdx_offline_root,
        tdx_client_root=args.tdx_client_root,
        asteria_data_root=args.asteria_data_root,
    )
    print(json.dumps(inventory, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
