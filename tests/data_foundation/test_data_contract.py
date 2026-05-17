from __future__ import annotations

import copy
import sys
import tomllib
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from malf_pas.data_foundation.contract import (
    contract_summary,
    load_contract_registry,
    validate_contract_registry,
)


class DataContractTest(unittest.TestCase):
    def test_current_registry_freezes_six_data_databases(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        registry_path = repo_root / "governance" / "data_module_db_contract_registry.toml"

        registry = load_contract_registry(registry_path)
        findings = validate_contract_registry(registry_path, registry)
        summary = contract_summary(registry_path, registry)

        self.assertEqual(findings, [])
        self.assertEqual(summary["status"], "passed")
        self.assertEqual(summary["registry"], str(registry_path))
        self.assertEqual(summary["database_count"], 6)
        self.assertGreaterEqual(summary["table_family_count"], 20)
        self.assertTrue(summary["forbidden_semantics_passed"])
        self.assertEqual(summary["next_card"], "raw-market-full-build-ledger-card")

    def test_contract_rejects_run_id_in_bar_natural_key(self) -> None:
        registry_path, registry = self._load_mutable_registry()
        raw_market = self._database(registry, "raw_market")
        raw_bar = self._table_family(raw_market, "raw_bar")
        raw_bar["natural_key"].append("run_id")

        findings = validate_contract_registry(registry_path, registry)

        self.assertTrue(
            any(
                "run_id must not be a business fact natural key" in item.message
                for item in findings
            )
        )

    def test_contract_rejects_missing_data_control_run_ledger(self) -> None:
        registry_path, registry = self._load_mutable_registry()
        data_control = self._database(registry, "data_control")
        data_control["table_families"] = [
            item
            for item in data_control["table_families"]
            if item.get("family") != "run_ledger"
        ]

        findings = validate_contract_registry(registry_path, registry)

        self.assertTrue(
            any("data_control must include run_ledger" in item.message for item in findings)
        )

    def test_contract_rejects_mixed_data_control_table_family_role(self) -> None:
        registry_path, registry = self._load_mutable_registry()
        data_control = self._database(registry, "data_control")
        run_ledger = self._table_family(data_control, "run_ledger")
        run_ledger["table_group"] = "orchestration_and_readout"

        findings = validate_contract_registry(registry_path, registry)

        self.assertTrue(
            any(
                "data_control table families must separate orchestration" in item.message
                for item in findings
            )
        )

    def test_contract_rejects_forbidden_downstream_semantic_fields(self) -> None:
        registry_path, registry = self._load_mutable_registry()
        market_base = self._database(registry, "market_base_day")
        base_bar = self._table_family(market_base, "base_bar")
        base_bar["required_fields"].append("malf_state")

        findings = validate_contract_registry(registry_path, registry)

        self.assertTrue(
            any("forbidden downstream semantic field" in item.message for item in findings)
        )

    def _load_mutable_registry(self) -> tuple[Path, dict[str, object]]:
        repo_root = Path(__file__).resolve().parents[2]
        registry_path = repo_root / "governance" / "data_module_db_contract_registry.toml"
        with registry_path.open("rb") as handle:
            registry = tomllib.load(handle)
        return registry_path, copy.deepcopy(registry)

    def _database(self, registry: dict[str, object], logical_name: str) -> dict[str, object]:
        for item in registry["databases"]:
            if item.get("logical_name") == logical_name:
                return item
        raise AssertionError(f"database {logical_name} not found")

    def _table_family(self, database: dict[str, object], family: str) -> dict[str, object]:
        for item in database["table_families"]:
            if item.get("family") == family:
                return item
        raise AssertionError(f"table family {family} not found")


if __name__ == "__main__":
    unittest.main()
