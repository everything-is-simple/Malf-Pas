from __future__ import annotations

import sys
import tomllib
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from malf_pas.governance.checks import (
    _check_malf_pas_scenario_atlas_registry,
    _check_pas_v1_2_strength_weakness_matrix_registry,
    run_checks,
)


class GovernanceChecksTest(unittest.TestCase):
    def test_repository_governance_checks_pass(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]

        findings = run_checks(repo_root)

        self.assertEqual(findings, [])

    def test_pas_v1_2_strength_weakness_registry_passes_specific_check(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        registry_path = repo_root / "governance" / "pas_v1_2_strength_weakness_matrix_registry.toml"

        with registry_path.open("rb") as handle:
            registry = tomllib.load(handle)

        findings = _check_pas_v1_2_strength_weakness_matrix_registry(registry_path, registry)

        self.assertEqual(findings, [])

    def test_malf_pas_scenario_atlas_registry_passes_specific_check(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        registry_path = repo_root / "governance" / "malf_pas_scenario_atlas_registry.toml"

        with registry_path.open("rb") as handle:
            registry = tomllib.load(handle)

        findings = _check_malf_pas_scenario_atlas_registry(registry_path, registry)

        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
