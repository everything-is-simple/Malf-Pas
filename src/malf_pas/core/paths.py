from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class MalfPasPaths:
    repo_root: Path
    data_root: Path
    validated_root: Path
    temp_root: Path

    @classmethod
    def from_env(cls, repo_root: Path) -> "MalfPasPaths":
        root = repo_root.resolve()
        return cls(
            repo_root=root,
            data_root=Path(os.environ.get("MALF_PAS_DATA_ROOT", "H:/Malf-Pas-data")),
            validated_root=Path(
                os.environ.get("MALF_PAS_VALIDATED_ROOT", "H:/Asteria-Validated")
            ),
            temp_root=Path(os.environ.get("MALF_PAS_TEMP_ROOT", "H:/Malf-Pas-temp")),
        )
