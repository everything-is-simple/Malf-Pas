from __future__ import annotations

import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from malf_pas.governance.checks import (
    _check_governance_roadmap_doc,
    _check_malf_pas_revision_roadmap_registry,
    _check_malf_pas_scenario_atlas_registry,
    _check_pas_v1_2_strength_weakness_matrix_registry,
    _check_post_terminal_roadmap_discipline_registry,
    _check_repo_governance_registry,
    _check_second_roadmap_doc,
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

    def test_open_source_adapter_boundary_registry_exists(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        registry_path = repo_root / "governance" / "open_source_adapter_boundary_registry.toml"

        self.assertTrue(registry_path.exists())

    def test_governance_route_is_terminal_after_card_16(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        module_gate_path = repo_root / "governance" / "module_gate_registry.toml"
        repo_registry_path = repo_root / "governance" / "repo_governance_registry.toml"

        with module_gate_path.open("rb") as handle:
            module_gate = tomllib.load(handle)
        with repo_registry_path.open("rb") as handle:
            repo_registry = tomllib.load(handle)

        self.assertEqual(module_gate.get("current_allowed_next_card"), "")
        self.assertEqual(module_gate.get("active_card"), "")
        self.assertEqual(
            module_gate.get("last_closed_card"),
            "open-source-adapter-boundary-card-20260516-01",
        )
        self.assertEqual(module_gate.get("roadmap_status"), "none / terminal")
        self.assertEqual(module_gate.get("first_day_work_status"), "closed")
        self.assertEqual(repo_registry.get("current_allowed_next_card"), "")

    def test_malf_pas_revision_registry_records_first_day_closeout(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        registry_path = repo_root / "governance" / "malf_pas_revision_roadmap_registry.toml"

        with registry_path.open("rb") as handle:
            registry = tomllib.load(handle)

        findings = _check_malf_pas_revision_roadmap_registry(registry_path, registry)
        closeout = registry.get("first_day_closeout", {})

        self.assertEqual(findings, [])
        self.assertEqual(closeout.get("status"), "closed")
        self.assertEqual(closeout.get("completed_governance_card_count"), 17)
        self.assertEqual(
            closeout.get("next_roadmap"),
            "docs/03-roadmap/01-local-tdx-data-foundation-module-db-roadmap-v1.md",
        )
        self.assertEqual(closeout.get("next_roadmap_scope"), "Data Foundation only")

    def test_roadmap_ready_requires_development_and_daily_usability_rules(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        repo_registry_path = repo_root / "governance" / "repo_governance_registry.toml"
        discipline_registry_path = (
            repo_root / "governance" / "post_terminal_roadmap_discipline_registry.toml"
        )

        with repo_registry_path.open("rb") as handle:
            repo_registry = tomllib.load(handle)
        with discipline_registry_path.open("rb") as handle:
            discipline_registry = tomllib.load(handle)

        required_hard_rules = {
            "roadmap-ready-requires-development-usable",
            "roadmap-ready-requires-daily-usable",
        }
        self.assertTrue(required_hard_rules.issubset(set(repo_registry.get("hard_rules", []))))
        self.assertEqual(discipline_registry.get("discipline_count"), 12)
        self.assertTrue(discipline_registry.get("development_usable_required_before_next_roadmap"))
        self.assertTrue(discipline_registry.get("daily_usable_required_before_next_roadmap"))
        rule_ids = [item.get("rule_id") for item in discipline_registry.get("disciplines", [])]
        self.assertEqual(
            rule_ids[3:5],
            [
                "ROADMAP-READY-REQUIRES-DEVELOPMENT-USABLE",
                "ROADMAP-READY-REQUIRES-DAILY-USABLE",
            ],
        )

    def test_repo_registry_keeps_second_roadmap_and_execution_docs_required(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        repo_registry_path = repo_root / "governance" / "repo_governance_registry.toml"

        with repo_registry_path.open("rb") as handle:
            repo_registry = tomllib.load(handle)

        required_docs = set(repo_registry.get("required_authority_docs", []))
        self.assertTrue(
            {
                "docs/00-governance/02-execution-record-protocol-v1.md",
                "docs/00-governance/03-repo-governance-environment-bootstrap-v1.md",
                "docs/03-roadmap/01-local-tdx-data-foundation-module-db-roadmap-v1.md",
                "docs/04-execution/README.md",
            }.issubset(required_docs)
        )

        findings = _check_repo_governance_registry(repo_registry_path, repo_registry)

        self.assertEqual(findings, [])

    def test_first_governance_roadmap_records_card_17_and_roadmap_2_handoff(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]

        findings = _check_governance_roadmap_doc(repo_root)

        self.assertEqual(findings, [])

    def test_second_roadmap_freezes_data_foundation_risk_boundaries(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]

        findings = _check_second_roadmap_doc(repo_root)

        self.assertEqual(findings, [])

    def test_governance_checks_fail_without_roadmap_ready_usability_rules(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        repo_registry_path = repo_root / "governance" / "repo_governance_registry.toml"
        discipline_registry_path = (
            repo_root / "governance" / "post_terminal_roadmap_discipline_registry.toml"
        )

        with repo_registry_path.open("rb") as handle:
            repo_registry = tomllib.load(handle)
        with discipline_registry_path.open("rb") as handle:
            discipline_registry = tomllib.load(handle)

        repo_without_ready_rules = {
            **repo_registry,
            "hard_rules": [
                rule
                for rule in repo_registry.get("hard_rules", [])
                if rule
                not in {
                    "roadmap-ready-requires-development-usable",
                    "roadmap-ready-requires-daily-usable",
                }
            ],
        }
        discipline_without_ready_rules = {
            **discipline_registry,
            "discipline_count": 10,
            "development_usable_required_before_next_roadmap": False,
            "daily_usable_required_before_next_roadmap": False,
            "disciplines": [
                item
                for item in discipline_registry.get("disciplines", [])
                if item.get("rule_id")
                not in {
                    "ROADMAP-READY-REQUIRES-DEVELOPMENT-USABLE",
                    "ROADMAP-READY-REQUIRES-DAILY-USABLE",
                }
            ],
        }

        repo_findings = _check_repo_governance_registry(
            repo_registry_path,
            repo_without_ready_rules,
        )
        discipline_findings = _check_post_terminal_roadmap_discipline_registry(
            discipline_registry_path,
            discipline_without_ready_rules,
        )

        self.assertTrue(
            any(
                "roadmap-ready-requires-development-usable" in item.message
                for item in repo_findings
            )
        )
        self.assertTrue(
            any(
                "development_usable_required_before_next_roadmap" in item.message
                for item in discipline_findings
            )
        )

    def test_governance_checks_fail_without_second_roadmap_required_docs(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        repo_registry_path = repo_root / "governance" / "repo_governance_registry.toml"

        with repo_registry_path.open("rb") as handle:
            repo_registry = tomllib.load(handle)

        stripped_registry = {
            **repo_registry,
            "required_authority_docs": [
                item
                for item in repo_registry.get("required_authority_docs", [])
                if item
                not in {
                    "docs/00-governance/02-execution-record-protocol-v1.md",
                    "docs/00-governance/03-repo-governance-environment-bootstrap-v1.md",
                    "docs/03-roadmap/01-local-tdx-data-foundation-module-db-roadmap-v1.md",
                    "docs/04-execution/README.md",
                }
            ],
        }

        findings = _check_repo_governance_registry(repo_registry_path, stripped_registry)

        self.assertTrue(
            any("system second Data Foundation roadmap" in item.message for item in findings)
        )
        self.assertTrue(
            any("execution record protocol doc" in item.message for item in findings)
        )

    def test_second_roadmap_check_fails_without_inventory_contract_and_validator_fragments(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        roadmap_path = repo_root / "docs" / "03-roadmap" / "01-local-tdx-data-foundation-module-db-roadmap-v1.md"

        findings = _check_second_roadmap_doc(repo_root)
        self.assertEqual(findings, [])

        roadmap_text = roadmap_path.read_text(encoding="utf-8")
        stripped_text = (
            roadmap_text.replace("week/month direct source 可用性结论", "")
            .replace("tradability 来源可用性结论", "")
            .replace("`raw_market.ingest_run` 与 `data_control.run_ledger` 的关系", "")
            .replace("Data validator 最小骨架", "")
            .replace(
                "orchestration table families 与 freshness/readout table families 分离边界",
                "",
            )
        )

        self.assertNotEqual(stripped_text, roadmap_text)

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_repo = Path(temp_dir)
            temp_roadmap = (
                temp_repo
                / "docs"
                / "03-roadmap"
                / "01-local-tdx-data-foundation-module-db-roadmap-v1.md"
            )
            temp_roadmap.parent.mkdir(parents=True, exist_ok=True)
            temp_roadmap.write_text(stripped_text, encoding="utf-8")

            simulated_findings = _check_second_roadmap_doc(temp_repo)

        self.assertTrue(
            any("week/month direct-source availability conclusion" in item.message for item in simulated_findings)
        )
        self.assertTrue(
            any("tradability source availability conclusion" in item.message for item in simulated_findings)
        )
        self.assertTrue(
            any("raw ingest audit vs data_control run-ledger relationship" in item.message for item in simulated_findings)
        )
        self.assertTrue(
            any("Data validator minimum skeleton" in item.message for item in simulated_findings)
        )
        self.assertTrue(
            any("orchestration and readout table families separated" in item.message for item in simulated_findings)
        )


if __name__ == "__main__":
    unittest.main()
