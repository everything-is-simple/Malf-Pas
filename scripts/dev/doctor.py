from __future__ import annotations

import json
import sys
from pathlib import Path
import tomllib

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from malf_pas import __version__
from malf_pas.core.paths import MalfPasPaths


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    paths = MalfPasPaths.from_env(repo_root)
    with (repo_root / "governance" / "repo_governance_registry.toml").open("rb") as handle:
        repo_registry = tomllib.load(handle)
    payload = {
        "malf_pas_version": __version__,
        "python": sys.version.split()[0],
        "repo_root": str(paths.repo_root),
        "data_root": str(paths.data_root),
        "backup_root": str(paths.backup_root),
        "validated_root": str(paths.validated_root),
        "report_root": str(paths.report_root),
        "temp_root": str(paths.temp_root),
        "stage": repo_registry.get("stage"),
        "formal_db_mutation": repo_registry.get("formal_db_mutation"),
        "broker_feasibility": repo_registry.get("broker_feasibility"),
        "current_route": repo_registry.get("current_route"),
        "current_allowed_next_card": repo_registry.get("current_allowed_next_card"),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
