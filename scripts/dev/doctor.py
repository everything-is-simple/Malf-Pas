from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from malf_pas import __version__
from malf_pas.core.paths import MalfPasPaths


def main() -> int:
    paths = MalfPasPaths.from_env(Path(__file__).resolve().parents[2])
    payload = {
        "malf_pas_version": __version__,
        "python": sys.version.split()[0],
        "repo_root": str(paths.repo_root),
        "data_root": str(paths.data_root),
        "validated_root": str(paths.validated_root),
        "temp_root": str(paths.temp_root),
        "formal_db_mutation": "no",
        "broker_feasibility": "deferred",
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
