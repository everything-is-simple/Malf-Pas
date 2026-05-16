from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Finding:
    path: Path
    message: str


IGNORED_PARTS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}


def _load_toml(path: Path, findings: list[Finding]) -> dict[str, Any] | None:
    if not path.exists():
        findings.append(Finding(path, "required TOML file is missing"))
        return None
    with path.open("rb") as handle:
        return tomllib.load(handle)


def _project_governance(repo_root: Path, findings: list[Finding]) -> dict[str, Any]:
    pyproject = _load_toml(repo_root / "pyproject.toml", findings)
    if pyproject is None:
        return {}
    governance = pyproject.get("tool", {}).get("malf_pas", {}).get("governance", {})
    if not governance:
        findings.append(Finding(repo_root / "pyproject.toml", "missing tool.malf_pas.governance"))
    return governance


def _check_required_paths(repo_root: Path, raw_paths: list[str], findings: list[Finding]) -> None:
    for raw_path in raw_paths:
        path = repo_root / raw_path
        if not path.exists():
            findings.append(Finding(path, "required governance path is missing"))


def _check_static_flags(repo_root: Path, governance: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    expected = {
        "stage": "governance-only",
        "formal_db_mutation": "no",
        "broker_feasibility": "deferred",
    }
    for key, value in expected.items():
        if governance.get(key) != value:
            findings.append(Finding(repo_root / "pyproject.toml", f"{key} must be {value!r}"))
    return findings


def _check_governance_roots(repo_root: Path, governance: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    required_repo_roots = {
        "H:/Malf-Pas",
        "H:/Malf-Pas-data",
        "H:/Malf-Pas-backup",
        "H:/Malf-Pas-Validated",
        "H:/Malf-Pas-reprot",
        "H:/Malf-Pas-temp",
    }
    required_reference_roots = {
        "H:/Asteria",
        "H:/Asteria-data",
        "H:/Asteria-Validated",
        "H:/Asteria-report",
        "H:/Asteria-temp",
        "G:/malf-history",
        "G:/《股市浮沉二十载》",
        "G:/《股市浮沉二十载》/2020.(Au)LanceBeggs",
    }
    repo_roots = set(governance.get("repo_roots", []))
    reference_roots = set(governance.get("reference_roots", []))

    missing_repo_roots = sorted(required_repo_roots - repo_roots)
    if missing_repo_roots:
        findings.append(
            Finding(
                repo_root / "pyproject.toml",
                f"repo_roots missing current Malf-Pas roots: {missing_repo_roots}",
            )
        )

    current_roots_in_reference = sorted(required_repo_roots & reference_roots)
    if current_roots_in_reference:
        findings.append(
            Finding(
                repo_root / "pyproject.toml",
                f"reference_roots must not contain current roots: {current_roots_in_reference}",
            )
        )

    missing_reference_roots = sorted(required_reference_roots - reference_roots)
    if missing_reference_roots:
        findings.append(
            Finding(
                repo_root / "pyproject.toml",
                f"reference_roots missing previous Asteria roots: {missing_reference_roots}",
            )
        )
    return findings


def _check_forbidden_repo_artifacts(repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    forbidden_suffixes = (".duckdb", ".duckdb.wal", ".duckdb.tmp", ".db", ".sqlite", ".sqlite3")
    for path in repo_root.rglob("*"):
        if not path.is_file() or IGNORED_PARTS.intersection(path.parts):
            continue
        if path.name.endswith(forbidden_suffixes):
            findings.append(Finding(path, "formal or scratch database artifact is inside repo"))
    for name in [".codex-tmp", "reports", "artifacts", "tmp", "temp"]:
        path = repo_root / name
        if path.exists():
            findings.append(Finding(path, "generated cache/report artifact is inside repo root"))
    return findings


def _check_no_asteria_paths_in_plugin(repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    plugin_root = repo_root / "plugins" / "malf-pas-workflow"
    for path in plugin_root.rglob("*"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if "H:/Asteria" in text or "H:\\Asteria" in text:
            findings.append(
                Finding(path, "workflow plugin must not retain hard-coded Asteria paths")
            )
    return findings


def _check_registries(repo_root: Path, governance: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    for raw_path in governance.get("required_registries", []):
        registry = _load_toml(repo_root / raw_path, findings)
        if registry is None:
            continue
        if registry.get("formal_db_mutation") not in {None, "no"}:
            findings.append(Finding(repo_root / raw_path, "formal_db_mutation must remain no"))
        if registry.get("broker_feasibility") not in {None, "deferred"}:
            findings.append(
                Finding(repo_root / raw_path, "broker_feasibility must remain deferred")
            )
        if raw_path == "governance/root_directory_registry.toml":
            findings.extend(_check_root_directory_registry(repo_root / raw_path, registry))
        if raw_path == "governance/source_authority_registry.toml":
            findings.extend(_check_source_authority_registry(repo_root / raw_path, registry))
        if raw_path == "governance/repo_governance_registry.toml":
            findings.extend(_check_repo_governance_registry(repo_root / raw_path, registry))
        if raw_path == "governance/module_gate_registry.toml":
            findings.extend(_check_module_gate_registry(repo_root / raw_path, registry))
        if raw_path == "governance/malf_v1_4_immutability_registry.toml":
            findings.extend(_check_malf_v1_4_immutability_registry(repo_root / raw_path, registry))
        if raw_path == "governance/predecessor_strength_registry.toml":
            findings.extend(_check_predecessor_strength_registry(repo_root / raw_path, registry))
        if raw_path == "governance/pas_axiomatic_state_machine_registry.toml":
            findings.extend(
                _check_pas_axiomatic_state_machine_registry(repo_root / raw_path, registry)
            )
        if raw_path == "governance/malf_v1_5_wave_behavior_snapshot_registry.toml":
            findings.extend(
                _check_malf_v1_5_wave_behavior_snapshot_registry(repo_root / raw_path, registry)
            )
        if raw_path == "governance/pas_v1_2_strength_weakness_matrix_registry.toml":
            findings.extend(
                _check_pas_v1_2_strength_weakness_matrix_registry(repo_root / raw_path, registry)
            )
        if raw_path == "governance/malf_pas_scenario_atlas_registry.toml":
            findings.extend(_check_malf_pas_scenario_atlas_registry(repo_root / raw_path, registry))
        if raw_path == "governance/malf_pas_revision_roadmap_registry.toml":
            findings.extend(
                _check_malf_pas_revision_roadmap_registry(repo_root / raw_path, registry)
            )
        if raw_path == "governance/database_topology_registry.toml":
            findings.extend(_check_database_topology_registry(repo_root / raw_path, registry))
        if raw_path == "governance/open_source_adapter_boundary_registry.toml":
            findings.extend(
                _check_open_source_adapter_boundary_registry(repo_root / raw_path, registry)
            )
        if raw_path == "governance/post_terminal_roadmap_discipline_registry.toml":
            findings.extend(
                _check_post_terminal_roadmap_discipline_registry(repo_root / raw_path, registry)
            )
    return findings


def _check_repo_governance_registry(path: Path, registry: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    expected_values = {
        "registry_version": "2026-05-16.v1",
        "stage": "governance-only",
        "formal_db_mutation": "no",
        "broker_feasibility": "deferred",
        "open_source_adapter_boundary_registry": (
            "governance/open_source_adapter_boundary_registry.toml"
        ),
        "current_allowed_next_card": "",
    }
    for key, expected in expected_values.items():
        if registry.get(key) != expected:
            findings.append(Finding(path, f"{key} must be {expected!r}"))

    required_docs = set(registry.get("required_authority_docs", []))
    if "docs/01-architecture/08-open-source-adapter-boundary-v1.md" not in required_docs:
        findings.append(
            Finding(path, "required_authority_docs must include open-source adapter boundary doc")
        )
    if "docs/00-governance/05-post-terminal-roadmap-and-module-db-discipline-v1.md" not in required_docs:
        findings.append(
            Finding(path, "required_authority_docs must include post-terminal roadmap discipline doc")
        )

    if registry.get("formal_local_truth_roots") != ["H:/tdx_offline_Data", "H:/new_tdx64"]:
        findings.append(Finding(path, "formal_local_truth_roots must be the two local TDX roots"))

    if registry.get("network_provider_formal_truth_disallowed") != [
        "TuShare",
        "baostock",
        "AKShare",
    ]:
        findings.append(
            Finding(
                path,
                "network_provider_formal_truth_disallowed must be TuShare, baostock, AKShare",
            )
        )

    if registry.get("read_only_bootstrap_reference_root") != "H:/Asteria-data":
        findings.append(Finding(path, "read_only_bootstrap_reference_root must be H:/Asteria-data"))

    if registry.get("post_data_priority_chain") != ["MALF", "PAS", "Signal"]:
        findings.append(Finding(path, "post_data_priority_chain must be MALF -> PAS -> Signal"))

    if registry.get("module_db_progression") != [
        "Data Foundation",
        "MALF v1.5",
        "PAS v1.2",
        "Signal",
    ]:
        findings.append(
            Finding(
                path,
                "module_db_progression must be Data Foundation -> MALF v1.5 -> PAS v1.2 -> Signal",
            )
        )

    hard_rules = set(registry.get("hard_rules", []))
    required_rules = {
        "post-terminal-separate-roadmap-only",
        "one-roadmap-one-module-db",
        "current-module-db-ready-before-next-roadmap",
        "post-data-core-priority-malf-pas-signal",
        "local-tdx-formal-truth-source",
        "no-network-provider-formal-truth",
        "mock-only-for-tests-and-proof",
        "asteria-data-read-only-bootstrap-reference",
        "module-dbs-are-governed-sub-ledgers",
        "advance-only-after-checks-pass",
    }
    missing_rules = sorted(required_rules - hard_rules)
    if missing_rules:
        findings.append(Finding(path, f"hard_rules missing {missing_rules}"))
    return findings


def _check_post_terminal_roadmap_discipline_registry(
    path: Path, registry: dict[str, Any]
) -> list[Finding]:
    findings: list[Finding] = []
    expected_values: dict[str, Any] = {
        "registry_version": "2026-05-16.v1",
        "stage": "governance-only",
        "formal_db_mutation": "no",
        "broker_feasibility": "deferred",
        "policy_status": "adopted-after-first-governance-roadmap-terminal",
        "authority_doc": "docs/00-governance/05-post-terminal-roadmap-and-module-db-discipline-v1.md",
        "current_repo_state": "first-governance-roadmap-terminal",
        "discipline_count": 10,
        "post_terminal_separate_roadmap_required": True,
        "one_roadmap_one_module_db": True,
        "current_module_db_ready_before_next_roadmap": True,
        "advance_only_after_checks_pass": True,
        "read_only_bootstrap_reference_root": "H:/Asteria-data",
        "historical_ledger_rule": "one logical historical ledger with governed sub-ledgers",
    }
    for key, expected in expected_values.items():
        if registry.get(key) != expected:
            findings.append(Finding(path, f"{key} must be {expected!r}"))

    if registry.get("formal_local_truth_roots") != ["H:/tdx_offline_Data", "H:/new_tdx64"]:
        findings.append(Finding(path, "formal_local_truth_roots must be the two local TDX roots"))

    if registry.get("network_provider_formal_truth_disallowed") != [
        "TuShare",
        "baostock",
        "AKShare",
    ]:
        findings.append(
            Finding(
                path,
                "network_provider_formal_truth_disallowed must be TuShare, baostock, AKShare",
            )
        )

    if registry.get("mock_allowed_scopes") != ["unit_test", "contract_test", "proof_harness"]:
        findings.append(
            Finding(
                path,
                "mock_allowed_scopes must be unit_test, contract_test, proof_harness",
            )
        )

    if registry.get("post_data_priority_chain") != ["MALF", "PAS", "Signal"]:
        findings.append(Finding(path, "post_data_priority_chain must be MALF -> PAS -> Signal"))

    if registry.get("module_db_progression") != [
        "Data Foundation",
        "MALF v1.5",
        "PAS v1.2",
        "Signal",
    ]:
        findings.append(
            Finding(
                path,
                "module_db_progression must be Data Foundation -> MALF v1.5 -> PAS v1.2 -> Signal",
            )
        )

    disciplines = registry.get("disciplines", [])
    if len(disciplines) != 10:
        findings.append(Finding(path, "disciplines must contain exactly 10 entries"))
        return findings

    expected_rule_ids = [
        "POST-TERMINAL-SEPARATE-ROADMAP-ONLY",
        "ONE-ROADMAP-ONE-MODULE-DB",
        "CURRENT-MODULE-DB-READY-BEFORE-NEXT-ROADMAP",
        "POST-DATA-CORE-PRIORITY-MALF-PAS-SIGNAL",
        "LOCAL-TDX-FORMAL-TRUTH-SOURCE",
        "NO-NETWORK-PROVIDER-FORMAL-TRUTH",
        "MOCK-ONLY-FOR-TESTS-AND-PROOF",
        "ASTERIA-DATA-READ-ONLY-BOOTSTRAP-REFERENCE",
        "MODULE-DBS-ARE-GOVERNED-SUB-LEDGERS",
        "ADVANCE-ONLY-AFTER-CHECKS-PASS",
    ]
    actual_rule_ids = [item.get("rule_id") for item in disciplines if isinstance(item, dict)]
    if actual_rule_ids != expected_rule_ids:
        findings.append(Finding(path, "disciplines.rule_id sequence must match the 10 frozen rules"))
    return findings


def _check_database_topology_registry(path: Path, registry: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    if registry.get("formal_local_truth_roots") != ["H:/tdx_offline_Data", "H:/new_tdx64"]:
        findings.append(
            Finding(path, "formal_local_truth_roots must be H:/tdx_offline_Data and H:/new_tdx64")
        )
    if registry.get("network_provider_formal_truth_disallowed") != [
        "TuShare",
        "baostock",
        "AKShare",
    ]:
        findings.append(
            Finding(
                path,
                "network_provider_formal_truth_disallowed must be TuShare, baostock, AKShare",
            )
        )
    if registry.get("next_module_db_requires_current_db_ready") is not True:
        findings.append(Finding(path, "next_module_db_requires_current_db_ready must be true"))
    if registry.get("module_db_progression") != [
        "Data Foundation",
        "MALF v1.5",
        "PAS v1.2",
        "Signal",
    ]:
        findings.append(
            Finding(
                path,
                "module_db_progression must be Data Foundation -> MALF v1.5 -> PAS v1.2 -> Signal",
            )
        )

    invariants = {
        item.get("id"): item.get("value")
        for item in registry.get("invariants", [])
        if isinstance(item, dict)
    }
    for invariant_id in [
        "ONE-ROADMAP-ONE-MODULE-DB",
        "NEXT-ROADMAP-REQUIRES-CURRENT-MODULE-DB-READY",
    ]:
        if invariants.get(invariant_id) is not True:
            findings.append(Finding(path, f"{invariant_id} invariant must be true"))
    return findings


def _check_module_gate_registry(path: Path, registry: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    expected_values = {
        "registry_version": "2026-05-16.v1",
        "stage": "governance-only",
        "active_route": "governance",
        "active_card": "open-source-adapter-boundary-card-20260516-01",
        "current_allowed_next_card": "",
        "module_contract_freeze_required_before_runtime": True,
    }
    for key, expected in expected_values.items():
        if registry.get(key) != expected:
            findings.append(Finding(path, f"{key} must be {expected!r}"))

    cards = {
        item.get("card_id"): item for item in registry.get("cards", []) if isinstance(item, dict)
    }
    terminal_card = cards.get("open-source-adapter-boundary-card")
    if terminal_card is None:
        findings.append(Finding(path, "open-source-adapter-boundary-card must be registered"))
        return findings
    if terminal_card.get("run_id") != "open-source-adapter-boundary-card-20260516-01":
        findings.append(
            Finding(path, "open-source-adapter-boundary-card run_id must be card-20260516-01")
        )
    if terminal_card.get("status") != "passed":
        findings.append(Finding(path, "open-source-adapter-boundary-card status must be passed"))
    expected_conclusion = (
        "docs/04-execution/records/governance/"
        "016-open-source-adapter-boundary-card-20260516-01.conclusion.md"
    )
    if terminal_card.get("conclusion") != expected_conclusion:
        findings.append(Finding(path, f"terminal card conclusion must be {expected_conclusion!r}"))
    return findings


def _check_malf_pas_revision_roadmap_registry(
    path: Path, registry: dict[str, Any]
) -> list[Finding]:
    findings: list[Finding] = []
    expected_values = {
        "policy_status": "frozen-by-malf-pas-revision-roadmap-card-20260516-01",
        "authority_doc": "docs/03-roadmap/00-malf-pas-governance-roadmap-v1.md",
        "run_id": "malf-pas-revision-roadmap-card-20260516-01",
        "current_malf_v1_4_anchor": (
            "H:/Malf-Pas-Validated/MALF_Three_Part_Design_Set_v1_4"
        ),
        "current_pas_v1_1_design_set": "H:/Malf-Pas-Validated/PAS__Three_Part_Design_Set_v1_1",
        "planned_malf_v1_5_design_set": (
            "H:/Malf-Pas-Validated/MALF_Three_Part_Design_Set_v1_5"
        ),
        "planned_pas_v1_2_design_set": "H:/Malf-Pas-Validated/PAS__Three_Part_Design_Set_v1_2",
        "planned_scenario_atlas": "H:/Malf-Pas-Validated/MALF_PAS_Scenario_Atlas_v1_0",
        "previous_next_card": "open-source-adapter-boundary-card",
        "next_card": "malf-v1-5-wave-behavior-snapshot-card",
    }
    for key, expected in expected_values.items():
        if registry.get(key) != expected:
            findings.append(Finding(path, f"{key} must be {expected!r}"))

    revision_principle = str(registry.get("revision_principle", ""))
    for fragment in ["extend MALF structure facts", "PAS read-only"]:
        if fragment not in revision_principle:
            findings.append(Finding(path, f"revision_principle must include {fragment!r}"))

    planned_cards = {
        item.get("card_id"): item
        for item in registry.get("planned_cards", [])
        if isinstance(item, dict)
    }
    expected_cards = {
        "malf-v1-5-wave-behavior-snapshot-card": (
            13,
            "MALF_Three_Part_Design_Set_v1_5",
            "wave_behavior_snapshot",
        ),
        "pas-v1-2-strength-weakness-matrix-card": (
            14,
            "PAS__Three_Part_Design_Set_v1_2",
            "strength_weakness_matrix",
        ),
        "malf-pas-scenario-atlas-card": (15, "MALF_PAS_Scenario_Atlas_v1_0", "diagrams"),
        "open-source-adapter-boundary-card": (16, "open-source adapter boundary", "adapters"),
    }
    for card_id, (order, deliverable_fragment, purpose_fragment) in expected_cards.items():
        card = planned_cards.get(card_id)
        if card is None:
            findings.append(Finding(path, f"{card_id} must be registered"))
            continue
        if card.get("order") != order:
            findings.append(Finding(path, f"{card_id} order must be {order}"))
        if deliverable_fragment not in str(card.get("deliverable", "")):
            findings.append(
                Finding(path, f"{card_id} deliverable must include {deliverable_fragment!r}")
            )
        if purpose_fragment not in str(card.get("purpose", "")):
            findings.append(Finding(path, f"{card_id} purpose must include {purpose_fragment!r}"))
        forbidden_scope = str(card.get("forbidden_scope", ""))
        for fragment in ["broker", "profit"]:
            if fragment not in forbidden_scope:
                findings.append(Finding(path, f"{card_id} must forbid {fragment!r}"))

    invariants = registry.get("invariants", {})
    required_invariants = {
        "malf_v1_4_remains_predecessor_authority",
        "pas_v1_1_remains_predecessor_authority",
        "malf_v1_5_must_be_new_directory",
        "pas_v1_2_must_be_new_directory",
        "pas_must_not_read_pricebar",
        "pas_must_not_rewrite_malf",
        "runtime_not_authorized",
        "formal_db_mutation_not_authorized",
        "broker_not_authorized",
        "profit_claim_not_authorized",
    }
    for key in sorted(required_invariants):
        if invariants.get(key) is not True:
            findings.append(Finding(path, f"{key} invariant must be true"))

    return findings


def _check_open_source_adapter_boundary_registry(
    path: Path, registry: dict[str, Any]
) -> list[Finding]:
    findings: list[Finding] = []
    expected_values = {
        "registry_version": "2026-05-16.v1",
        "stage": "governance-only",
        "formal_db_mutation": "no",
        "broker_feasibility": "deferred",
        "authority_doc": "docs/01-architecture/08-open-source-adapter-boundary-v1.md",
        "policy_status": "frozen-by-open-source-adapter-boundary-card-20260516-01",
        "run_id": "open-source-adapter-boundary-card-20260516-01",
        "source_authority_doc": (
            "docs/00-governance/01-source-authority-and-non-migration-rule-v1.md"
        ),
        "source_authority_registry": "governance/source_authority_registry.toml",
        "terminal_on_pass": True,
        "current_allowed_next_card_after_pass": "",
        "doc_state_after_pass": "none / terminal",
    }
    for key, expected in expected_values.items():
        if registry.get(key) != expected:
            findings.append(Finding(path, f"{key} must be {expected!r}"))

    authority_doc = path.parents[1] / str(registry.get("authority_doc", ""))
    if not authority_doc.exists():
        findings.append(Finding(authority_doc, "open-source adapter authority doc is missing"))
    else:
        authority_text = authority_doc.read_text(encoding="utf-8")
        for fragment in [
            "source_adapter",
            "research_query_or_data_processing_adapter",
            "research_proof_adapter",
            "isolated_research_reference",
            "reference_or_experimental_input_only",
            "DuckDB / Arrow / Polars",
            "vectorbt / backtesting.py",
            "Qlib",
            "baostock",
            "AKShare",
            "rejected_for_semantic_ownership",
            "none / terminal",
        ]:
            if fragment not in authority_text:
                findings.append(Finding(authority_doc, f"authority doc must mention {fragment!r}"))

    expected_roles = [
        "source_adapter",
        "research_query_or_data_processing_adapter",
        "research_proof_adapter",
        "isolated_research_reference",
        "reference_or_experimental_input_only",
    ]
    if registry.get("role_enums") != expected_roles:
        findings.append(Finding(path, "role_enums must match the five frozen adapter roles"))

    forbidden_boundaries = set(registry.get("global_forbidden_boundaries", []))
    required_forbidden = {
        "MALF semantic ownership",
        "PAS semantic ownership",
        "Signal semantic ownership",
        "Position semantic ownership",
        "Trade semantic ownership",
        "System Readout semantic ownership",
        "Pipeline semantic ownership",
        "formal truth owner",
        "order owner",
        "position owner",
        "fill owner",
        "broker instruction source",
        "profit proof source",
    }
    missing_forbidden = sorted(required_forbidden - forbidden_boundaries)
    if missing_forbidden:
        findings.append(
            Finding(path, f"global_forbidden_boundaries missing {missing_forbidden}")
        )

    projects = {
        item.get("key"): item for item in registry.get("projects", []) if isinstance(item, dict)
    }
    expected_projects = {
        "duckdb_arrow_polars": (
            "DuckDB / Arrow / Polars",
            "research_query_or_data_processing_adapter",
            "adapter_candidate",
            {"Data Foundation", "MALF", "PAS", "Signal", "Position", "Portfolio Plan",
             "Trade", "System Readout", "Pipeline"},
        ),
        "vectorbt_backtesting_py": (
            "vectorbt / backtesting.py",
            "research_proof_adapter",
            "adapter_candidate",
            {"MALF", "PAS", "Signal", "Position", "Portfolio Plan", "Trade", "System Readout"},
        ),
        "qlib": (
            "Qlib",
            "isolated_research_reference",
            "adapter_candidate",
            {"PAS", "Signal", "Position", "Portfolio Plan", "Trade", "System Readout"},
        ),
        "baostock": (
            "baostock",
            "source_adapter",
            "adapter_candidate",
            {"Data Foundation"},
        ),
        "akshare": (
            "AKShare",
            "reference_or_experimental_input_only",
            "rejected_for_semantic_ownership",
            {"Data Foundation"},
        ),
    }
    if set(projects) != set(expected_projects):
        findings.append(Finding(path, "projects must contain exactly the five frozen entries"))

    required_project_forbidden = {
        "formal truth owner",
        "order owner",
        "position owner",
        "fill owner",
        "broker instruction source",
        "profit proof source",
    }
    for key, (project_name, role, source_status, modules) in expected_projects.items():
        project = projects.get(key)
        if project is None:
            findings.append(Finding(path, f"{key} project must be registered"))
            continue
        if project.get("project") != project_name:
            findings.append(Finding(path, f"{key} project name must be {project_name!r}"))
        if project.get("allowed_role") != role:
            findings.append(Finding(path, f"{key} allowed_role must be {role!r}"))
        if project.get("source_authority_status") != source_status:
            findings.append(
                Finding(path, f"{key} source_authority_status must be {source_status!r}")
            )
        if set(project.get("applicable_modules", [])) != modules:
            findings.append(Finding(path, f"{key} applicable_modules must match frozen scope"))
        project_forbidden = set(project.get("forbidden_boundaries", []))
        missing_project_forbidden = sorted(required_project_forbidden - project_forbidden)
        if missing_project_forbidden:
            findings.append(
                Finding(path, f"{key} forbidden_boundaries missing {missing_project_forbidden}")
            )

    if projects.get("akshare", {}).get("special_policy") != "rejected_for_semantic_ownership":
        findings.append(Finding(path, "akshare special_policy must keep semantic-ownership reject"))
    return findings


def _check_malf_v1_5_wave_behavior_snapshot_registry(
    path: Path, registry: dict[str, Any]
) -> list[Finding]:
    findings: list[Finding] = []
    expected_values = {
        "policy_status": "frozen-by-malf-v1-5-wave-behavior-snapshot-card-20260516-01",
        "authority_doc": "docs/02-modules/02-malf-v1-5-wave-behavior-snapshot-v1.md",
        "current_malf_v1_4_anchor": "H:/Malf-Pas-Validated/MALF_Three_Part_Design_Set_v1_4",
        "predecessor_original_reference": "H:/Asteria-Validated/MALF_Three_Part_Design_Set_v1_4",
        "design_set": "H:/Malf-Pas-Validated/MALF_Three_Part_Design_Set_v1_5",
        "design_manifest": "H:/Malf-Pas-Validated/MALF_Three_Part_Design_Set_v1_5/MANIFEST.json",
        "next_card": "pas-v1-2-strength-weakness-matrix-card",
    }
    for key, expected in expected_values.items():
        if registry.get(key) != expected:
            findings.append(Finding(path, f"{key} must be {expected!r}"))

    expected_inputs = {
        "MALF WavePosition",
        "MALF Core trace",
        "MALF transition trace",
        "MALF Lifespan stats",
        "MALF birth descriptors",
        "MALF source lineage",
    }
    if set(registry.get("allowed_inputs", [])) != expected_inputs:
        findings.append(Finding(path, "allowed_inputs must remain MALF-output-only"))

    expected_facets = {
        "continuation_regime",
        "stagnation_regime",
        "transition_regime",
        "birth_quality_regime",
        "boundary_pressure_regime",
        "directional_continuity_regime",
    }
    if set(registry.get("behavior_facets", [])) != expected_facets:
        findings.append(Finding(path, "behavior_facets must remain the six frozen regimes"))

    expected_surfaces = {"WaveBehaviorSnapshot", "WaveBehaviorSnapshotLatest"}
    if set(registry.get("service_surfaces", [])) != expected_surfaces:
        findings.append(Finding(path, "service_surfaces must remain WaveBehaviorSnapshot pair"))

    forbidden_outputs = set(registry.get("forbidden_outputs", []))
    for expected in {"strength_score", "setup_family", "accept", "order", "profit"}:
        if expected not in forbidden_outputs:
            findings.append(Finding(path, f"forbidden_outputs must include {expected!r}"))

    principles = registry.get("principles", {})
    expected_principles = {
        "malf_v1_4_remains_anchor": True,
        "malf_v1_5_is_successor_definition": True,
        "wave_behavior_snapshot_is_structural": True,
        "pas_reads_malf_outputs_only": True,
        "pricebar_reinterpretation_for_pas": False,
        "runtime_not_authorized": True,
    }
    for key, expected in expected_principles.items():
        if principles.get(key) != expected:
            findings.append(Finding(path, f"principles.{key} must be {expected!r}"))

    return findings


def _check_pas_axiomatic_state_machine_registry(
    path: Path, registry: dict[str, Any]
) -> list[Finding]:
    findings: list[Finding] = []
    expected_values = {
        "policy_status": "frozen-by-pas-axiomatic-state-machine-card-20260515-01",
        "authority_doc": "docs/02-modules/01-pas-axiomatic-state-machine-v1.md",
        "design_set": "H:/Malf-Pas-Validated/PAS__Three_Part_Design_Set_v1_1",
        "design_manifest": "H:/Malf-Pas-Validated/PAS__Three_Part_Design_Set_v1_1/MANIFEST.json",
        "current_malf_v1_4_anchor": "H:/Malf-Pas-Validated/MALF_Three_Part_Design_Set_v1_4",
        "predecessor_malf_v1_4_reference": (
            "H:/Asteria-Validated/MALF_Three_Part_Design_Set_v1_4"
        ),
        "next_card": "open-source-adapter-boundary-card",
    }
    for key, expected in expected_values.items():
        if registry.get(key) != expected:
            findings.append(Finding(path, f"{key} must be {expected!r}"))

    principles = registry.get("principles", {})
    expected_principles = {
        "malf_owns_structure",
        "pas_owns_opportunity_interpretation",
        "signal_owns_accept_reject",
        "position_trade_own_action",
    }
    for key in sorted(expected_principles):
        if principles.get(key) is not True:
            findings.append(Finding(path, f"{key} principle must be true"))
    religion = str(principles.get("religion", ""))
    for fragment in ["identify strength / weakness", "reject weakness", "join strength"]:
        if fragment not in religion:
            findings.append(Finding(path, f"principles.religion must include {fragment!r}"))

    expected_chain = [
        "MALF WavePosition",
        "PAS-Core",
        "PAS-Lifecycle",
        "PAS-Service",
        "Signal",
    ]
    if registry.get("semantic_chain") != expected_chain:
        findings.append(
            Finding(path, "semantic_chain must remain MALF WavePosition -> PAS -> Signal")
        )

    expected_lifecycle_states = {
        "observing",
        "forming",
        "waiting",
        "triggered",
        "cancelled",
        "modified",
        "invalidated",
        "reentry_candidate",
        "submitted_to_signal",
        "accepted_by_signal",
        "rejected_by_signal",
    }
    lifecycle_states = set(registry.get("lifecycle_states", []))
    missing_states = sorted(expected_lifecycle_states - lifecycle_states)
    if missing_states:
        findings.append(Finding(path, f"lifecycle_states missing {missing_states}"))

    expected_setup_families = {"TST", "BOF", "BPB", "PB", "CPB"}
    setup_families = set(registry.get("setup_families", []))
    missing_families = sorted(expected_setup_families - setup_families)
    if missing_families:
        findings.append(Finding(path, f"setup_families missing {missing_families}"))

    expected_surfaces = {"PASCandidate", "PASCandidateLatest", "PASLifecycleTrace"}
    service_surfaces = set(registry.get("service_surfaces", []))
    missing_surfaces = sorted(expected_surfaces - service_surfaces)
    if missing_surfaces:
        findings.append(Finding(path, f"service_surfaces missing {missing_surfaces}"))

    forbidden_outputs = set(registry.get("forbidden_outputs", []))
    required_forbidden_outputs = {
        "order",
        "position",
        "fill",
        "profit",
        "broker_instruction",
    }
    missing_forbidden = sorted(required_forbidden_outputs - forbidden_outputs)
    if missing_forbidden:
        findings.append(Finding(path, f"forbidden_outputs missing {missing_forbidden}"))

    forbidden_inputs = " ".join(str(item) for item in registry.get("forbidden_inputs", []))
    for fragment in ["PriceBar", "HH/HL/LL/LH", "wave rewrite", "lifespan rank"]:
        if fragment not in forbidden_inputs:
            findings.append(Finding(path, f"forbidden_inputs must mention {fragment!r}"))

    expected_sources = {"ytc_volume_2", "ytc_volume_3", "ytc_volume_4"}
    sources = {
        item.get("key"): item for item in registry.get("sources", []) if isinstance(item, dict)
    }
    for key in sorted(expected_sources):
        source = sources.get(key)
        if source is None:
            findings.append(Finding(path, f"{key} source must be registered"))
            continue
        forbidden_role = str(source.get("forbidden_role", ""))
        if "broker" not in forbidden_role or "profit" not in forbidden_role:
            findings.append(Finding(path, f"{key} must forbid broker and profit use"))

    return findings


def _check_pas_v1_2_strength_weakness_matrix_registry(
    path: Path, registry: dict[str, Any]
) -> list[Finding]:
    findings: list[Finding] = []
    expected_values = {
        "policy_status": "frozen-by-pas-v1-2-strength-weakness-matrix-card-20260516-01",
        "authority_doc": "docs/02-modules/03-pas-v1-2-strength-weakness-matrix-v1.md",
        "design_set": "H:/Malf-Pas-Validated/PAS__Three_Part_Design_Set_v1_2",
        "design_manifest": (
            "H:/Malf-Pas-Validated/PAS__Three_Part_Design_Set_v1_2/MANIFEST.json"
        ),
        "current_malf_v1_4_anchor": "H:/Malf-Pas-Validated/MALF_Three_Part_Design_Set_v1_4",
        "current_malf_v1_5_design_set": (
            "H:/Malf-Pas-Validated/MALF_Three_Part_Design_Set_v1_5"
        ),
        "current_pas_v1_1_design_set": "H:/Malf-Pas-Validated/PAS__Three_Part_Design_Set_v1_1",
        "next_card": "malf-pas-scenario-atlas-card",
    }
    for key, expected in expected_values.items():
        if registry.get(key) != expected:
            findings.append(Finding(path, f"{key} must be {expected!r}"))

    expected_chain = [
        "MALF WavePosition",
        "MALF WaveBehaviorSnapshot",
        "PAS-Core",
        "PAS-StrengthWeaknessMatrix",
        "PAS-Lifecycle",
        "PAS-Service",
        "Signal",
    ]
    if registry.get("semantic_chain") != expected_chain:
        findings.append(
            Finding(
                path,
                "semantic_chain must remain MALF WavePosition -> WaveBehaviorSnapshot -> "
                "PAS-Core -> PAS-StrengthWeaknessMatrix -> PAS-Lifecycle -> PAS-Service "
                "-> Signal",
            )
        )

    expected_inputs = {
        "MALF WavePosition",
        "MALF Core trace",
        "MALF transition trace",
        "MALF Lifespan stats",
        "MALF birth descriptors",
        "MALF source lineage",
        "WaveBehaviorSnapshot",
        "PAS Context",
        "PAS Directional Premise",
    }
    if set(registry.get("allowed_inputs", [])) != expected_inputs:
        findings.append(Finding(path, "allowed_inputs must remain MALF + PAS-context only"))

    expected_facets = {
        "continuation_regime",
        "stagnation_regime",
        "transition_regime",
        "birth_quality_regime",
        "boundary_pressure_regime",
        "directional_continuity_regime",
    }
    if set(registry.get("behavior_facets", [])) != expected_facets:
        findings.append(Finding(path, "behavior_facets must remain the six frozen regimes"))

    expected_statuses = {"strong", "weak", "mixed", "ambiguous", "not_applicable"}
    if set(registry.get("matrix_read_statuses", [])) != expected_statuses:
        findings.append(Finding(path, "matrix_read_statuses must remain the five frozen reads"))

    expected_setup_postures = {"favored", "allowed", "deferred", "blocked"}
    if set(registry.get("setup_postures", [])) != expected_setup_postures:
        findings.append(Finding(path, "setup_postures must remain the four frozen postures"))

    expected_setup_families = {"TST", "BOF", "BPB", "PB", "CPB"}
    if set(registry.get("setup_families", [])) != expected_setup_families:
        findings.append(Finding(path, "setup_families must remain the five PAS families"))

    expected_surfaces = {
        "PASStrengthWeaknessMatrix",
        "PASStrengthWeaknessMatrixLatest",
        "PASCandidate",
        "PASCandidateLatest",
        "PASLifecycleTrace",
    }
    if set(registry.get("service_surfaces", [])) != expected_surfaces:
        findings.append(Finding(path, "service_surfaces must include matrix, candidate, and trace"))

    forbidden_outputs = set(registry.get("forbidden_outputs", []))
    required_forbidden_outputs = {
        "strength_score",
        "buy",
        "sell",
        "accept",
        "reject",
        "order",
        "position",
        "fill",
        "broker_instruction",
        "profit",
    }
    missing_forbidden = sorted(required_forbidden_outputs - forbidden_outputs)
    if missing_forbidden:
        findings.append(Finding(path, f"forbidden_outputs missing {missing_forbidden}"))

    forbidden_inputs = " ".join(str(item) for item in registry.get("forbidden_inputs", []))
    for fragment in [
        "PriceBar",
        "HH/HL/LL/LH",
        "wave rewrite",
        "WaveBehaviorSnapshot rewrite",
    ]:
        if fragment not in forbidden_inputs:
            findings.append(Finding(path, f"forbidden_inputs must mention {fragment!r}"))

    principles = registry.get("principles", {})
    expected_principles = {
        "malf_owns_structure": True,
        "malf_v1_5_remains_behavior_source": True,
        "pas_v1_1_remains_predecessor_authority": True,
        "strength_weakness_matrix_is_discrete": True,
        "pricebar_reinterpretation_for_pas": False,
        "matrix_is_not_trade_signal": True,
        "runtime_not_authorized": True,
    }
    for key, expected in expected_principles.items():
        if principles.get(key) != expected:
            findings.append(Finding(path, f"principles.{key} must be {expected!r}"))

    return findings


def _check_malf_pas_scenario_atlas_registry(
    path: Path, registry: dict[str, Any]
) -> list[Finding]:
    findings: list[Finding] = []
    expected_values = {
        "policy_status": "frozen-by-malf-pas-scenario-atlas-card-20260516-01",
        "authority_doc": "docs/02-modules/04-malf-pas-scenario-atlas-v1.md",
        "atlas_set": "H:/Malf-Pas-Validated/MALF_PAS_Scenario_Atlas_v1_0",
        "atlas_manifest": "H:/Malf-Pas-Validated/MALF_PAS_Scenario_Atlas_v1_0/MANIFEST.json",
        "current_malf_v1_4_anchor": "H:/Malf-Pas-Validated/MALF_Three_Part_Design_Set_v1_4",
        "current_malf_v1_5_design_set": "H:/Malf-Pas-Validated/MALF_Three_Part_Design_Set_v1_5",
        "current_pas_v1_1_design_set": "H:/Malf-Pas-Validated/PAS__Three_Part_Design_Set_v1_1",
        "current_pas_v1_2_design_set": "H:/Malf-Pas-Validated/PAS__Three_Part_Design_Set_v1_2",
        "next_card": "open-source-adapter-boundary-card",
        "delivery_mode": "companion_atlas",
        "visual_format": "markdown_plus_svg",
        "historical_reference_policy": "reference_only_not_proof",
    }
    for key, expected in expected_values.items():
        if registry.get(key) != expected:
            findings.append(Finding(path, f"{key} must be {expected!r}"))

    expected_scenarios = [
        "strength_continuation_case",
        "weakness_rejection_case",
        "boundary_test_case",
        "transition_unresolved_case",
        "no_actionable_premise_case",
    ]
    if registry.get("scenario_order") != expected_scenarios:
        findings.append(Finding(path, "scenario_order must remain the five frozen atlas cases"))

    expected_inputs = {
        "MALF WavePosition",
        "WaveBehaviorSnapshot",
        "PAS Context",
        "PAS Directional Premise",
        "PAS StrengthWeaknessMatrix",
    }
    if set(registry.get("allowed_inputs", [])) != expected_inputs:
        findings.append(Finding(path, "allowed_inputs must remain frozen MALF+PAS inputs only"))

    forbidden_outputs = set(registry.get("forbidden_outputs", []))
    required_forbidden_outputs = {
        "buy",
        "sell",
        "hold",
        "order",
        "position",
        "fill",
        "broker_instruction",
        "alpha_proof",
        "formal_backtest_proof",
        "profit",
    }
    missing_forbidden = sorted(required_forbidden_outputs - forbidden_outputs)
    if missing_forbidden:
        findings.append(Finding(path, f"forbidden_outputs missing {missing_forbidden}"))

    expected_principles = {
        "malf_owns_structure": True,
        "pas_owns_opportunity_interpretation": True,
        "atlas_is_companion_only": True,
        "historical_reference_is_not_proof": True,
        "runtime_not_authorized": True,
        "formal_db_mutation_not_authorized": True,
        "broker_not_authorized": True,
    }
    principles = registry.get("principles", {})
    for key, expected in expected_principles.items():
        if principles.get(key) != expected:
            findings.append(Finding(path, f"principles.{key} must be {expected!r}"))

    expected_cases = {
        "strength_continuation_case": (
            "strong",
            "ATLAS_10_Strength_Continuation_Case_v1_0.md",
            "ATLAS_10_Strength_Continuation_Case_v1_0.svg",
        ),
        "weakness_rejection_case": (
            "weak",
            "ATLAS_11_Weakness_Rejection_Case_v1_0.md",
            "ATLAS_11_Weakness_Rejection_Case_v1_0.svg",
        ),
        "boundary_test_case": (
            "mixed",
            "ATLAS_12_Boundary_Test_Case_v1_0.md",
            "ATLAS_12_Boundary_Test_Case_v1_0.svg",
        ),
        "transition_unresolved_case": (
            "ambiguous",
            "ATLAS_13_Transition_Unresolved_Case_v1_0.md",
            "ATLAS_13_Transition_Unresolved_Case_v1_0.svg",
        ),
        "no_actionable_premise_case": (
            "not_applicable",
            "ATLAS_14_No_Actionable_Premise_Case_v1_0.md",
            "ATLAS_14_No_Actionable_Premise_Case_v1_0.svg",
        ),
    }
    registered_cases = {
        item.get("case_id"): item for item in registry.get("cases", []) if isinstance(item, dict)
    }
    for case_id, (read_status, md_fragment, svg_fragment) in expected_cases.items():
        case = registered_cases.get(case_id)
        if case is None:
            findings.append(Finding(path, f"{case_id} must be registered"))
            continue
        if case.get("read_status") != read_status:
            findings.append(Finding(path, f"{case_id} read_status must be {read_status!r}"))
        if md_fragment not in str(case.get("markdown", "")):
            findings.append(Finding(path, f"{case_id} markdown must include {md_fragment!r}"))
        if svg_fragment not in str(case.get("svg", "")):
            findings.append(Finding(path, f"{case_id} svg must include {svg_fragment!r}"))

    return findings


def _check_predecessor_strength_registry(path: Path, registry: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    expected_values = {
        "policy_status": "frozen-by-predecessor-strength-map-card-20260515-01",
        "authority_doc": "docs/01-architecture/02-predecessor-strength-map-v1.md",
        "next_card": "pas-axiomatic-state-machine-card",
    }
    for key, expected in expected_values.items():
        if registry.get(key) != expected:
            findings.append(Finding(path, f"{key} must be {expected!r}"))

    expected_sources = {
        "malf_v1_4_anchor": (
            "H:/Malf-Pas-Validated/MALF_Three_Part_Design_Set_v1_4",
            "authority_anchor",
        ),
        "malf_v1_4_predecessor_original": (
            "H:/Asteria-Validated/MALF_Three_Part_Design_Set_v1_4",
            "authority_anchor",
        ),
        "malf_v1_4_predecessor_original_zip": (
            "H:/Asteria-Validated/MALF_Three_Part_Design_Set_v1_4.zip",
            "authority_anchor",
        ),
        "pas_v1_1_design_set": (
            "H:/Malf-Pas-Validated/PAS__Three_Part_Design_Set_v1_1",
            "authority_anchor",
        ),
        "malf_v1_5_design_set": (
            "H:/Malf-Pas-Validated/MALF_Three_Part_Design_Set_v1_5",
            "successor_authority_definition",
        ),
        "pas_v1_2_design_set": (
            "H:/Malf-Pas-Validated/PAS__Three_Part_Design_Set_v1_2",
            "successor_authority_definition",
        ),
        "malf_pas_scenario_atlas": (
            "H:/Malf-Pas-Validated/MALF_PAS_Scenario_Atlas_v1_0",
            "companion_authority_asset",
        ),
        "asteria_system_design_set_v1_0": (
            "H:/Asteria-Validated/Asteria_System_Design_Set_v1_0",
            "reference_input",
        ),
        "malf_system_history": (
            "H:/Asteria-Validated/MALF-system-history",
            "historical_tradeoff_reference",
        ),
        "malf_reference": ("H:/Asteria-Validated/MALF-reference", "reference_input"),
        "lance_beggs_book_root": ("G:/《股市浮沉二十载》", "brainstorming_source"),
        "ytc_lance_beggs": ("G:/《股市浮沉二十载》/2020.(Au)LanceBeggs", "concept_source"),
        "malf_history_root": ("G:/malf-history", "historical_tradeoff_reference"),
        "market_lifespan_quant": ("G:/malf-history/MarketLifespan-Quant", "reference_input"),
        "emotion_quant_gamma": ("G:/malf-history/EmotionQuant-gamma", "reference_input"),
        "astock_lifespan_alpha": ("G:/malf-history/astock_lifespan-alpha", "reference_input"),
        "lifespan_0_01": ("G:/malf-history/lifespan-0.01", "reference_input"),
    }
    sources = {
        item.get("key"): item for item in registry.get("sources", []) if isinstance(item, dict)
    }
    for key, (expected_path, expected_classification) in expected_sources.items():
        source = sources.get(key)
        if source is None:
            findings.append(Finding(path, f"{key} source must be registered"))
            continue
        if source.get("path") != expected_path:
            findings.append(Finding(path, f"{key} path must be {expected_path!r}"))
        if source.get("classification") != expected_classification:
            findings.append(
                Finding(path, f"{key} classification must be {expected_classification!r}")
            )
        for field in ["absorbable_strength", "forbidden_role", "downstream_use"]:
            if not str(source.get(field, "")).strip():
                findings.append(Finding(path, f"{key} must define {field}"))

    forbidden_fragments = {
        "legacy code migration",
        "schema transplant",
        "runner transplant",
    }
    for key in ["malf_system_history", "malf_history_root"]:
        forbidden_role = str(sources.get(key, {}).get("forbidden_role", ""))
        for fragment in forbidden_fragments:
            if fragment not in forbidden_role:
                findings.append(Finding(path, f"{key} must forbid {fragment!r}"))

    action_forbidden_keys = {
        "lance_beggs_book_root": {"broker", "order", "fill", "profit"},
        "ytc_lance_beggs": {"broker", "order", "fill", "profit"},
        "market_lifespan_quant": {"runner", "backtest proof", "semantic owner"},
        "emotion_quant_gamma": {"broker", "position"},
        "astock_lifespan_alpha": {"legacy code migration", "queue", "checkpoint"},
        "lifespan_0_01": {"schema transplant", "runner transplant"},
    }
    for key, fragments in action_forbidden_keys.items():
        forbidden_role = str(sources.get(key, {}).get("forbidden_role", ""))
        for fragment in fragments:
            if fragment not in forbidden_role:
                findings.append(Finding(path, f"{key} must forbid {fragment!r}"))

    return findings


def _check_malf_v1_4_immutability_registry(
    path: Path, registry: dict[str, Any]
) -> list[Finding]:
    findings: list[Finding] = []
    expected_values: dict[str, Any] = {
        "policy_status": "frozen-by-malf-v1-4-immutability-anchor-card-20260515-01",
        "authority_doc": "docs/01-architecture/01-malf-v1-4-anchor-position-v1.md",
        "anchor_directory": "H:/Malf-Pas-Validated/MALF_Three_Part_Design_Set_v1_4",
        "anchor_manifest": (
            "H:/Malf-Pas-Validated/MALF_Three_Part_Design_Set_v1_4/MANIFEST.json"
        ),
        "predecessor_original_directory": (
            "H:/Asteria-Validated/MALF_Three_Part_Design_Set_v1_4"
        ),
        "predecessor_original_zip": "H:/Asteria-Validated/MALF_Three_Part_Design_Set_v1_4.zip",
        "predecessor_original_manifest": (
            "H:/Asteria-Validated/MALF_Three_Part_Design_Set_v1_4/MANIFEST.json"
        ),
        "runtime_authorized": False,
        "formal_db_mutation_authorized": False,
        "downstream_redefinition_authorized": False,
        "legacy_schema_migration_authorized": False,
    }
    for key, expected in expected_values.items():
        if registry.get(key) != expected:
            findings.append(Finding(path, f"{key} must be {expected!r}"))

    required_invariants = {
        "MALF-V1-4-ANCHOR",
        "STRUCTURE-FIRST",
        "NO-PAS-REWRITE",
        "NO-SIGNAL-REWRITE",
        "NO-POSITION-TRADE-REWRITE",
        "NO-AUTHORITY-BY-ADAPTER",
        "ANCHOR-NOT-RUNTIME-AUTHORIZATION",
        "MANIFEST-IS-BOUNDARY-EVIDENCE",
    }
    invariants = {
        item.get("invariant_id"): item
        for item in registry.get("invariants", [])
        if isinstance(item, dict)
    }
    for invariant_id in sorted(required_invariants):
        invariant = invariants.get(invariant_id)
        if invariant is None:
            findings.append(Finding(path, f"{invariant_id} invariant must be registered"))
            continue
        if invariant.get("required") is not True:
            findings.append(Finding(path, f"{invariant_id} invariant must be required"))

    return findings


def _check_source_authority_registry(path: Path, registry: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    if (
        registry.get("policy_status")
        != "frozen-by-source-authority-and-non-migration-rule-card-20260515-01"
    ):
        findings.append(
            Finding(
                path,
                "policy_status must be frozen by "
                "source-authority-and-non-migration-rule-card-20260515-01",
            )
        )
    expected_sources = {
        "malf_v1_4_anchor": (
            "H:/Malf-Pas-Validated/MALF_Three_Part_Design_Set_v1_4",
            "authority_anchor",
        ),
        "malf_v1_4_predecessor_original": (
            "H:/Asteria-Validated/MALF_Three_Part_Design_Set_v1_4",
            "authority_anchor",
        ),
        "malf_v1_4_predecessor_original_zip": (
            "H:/Asteria-Validated/MALF_Three_Part_Design_Set_v1_4.zip",
            "authority_anchor",
        ),
        "pas_v1_1_design_set": (
            "H:/Malf-Pas-Validated/PAS__Three_Part_Design_Set_v1_1",
            "authority_anchor",
        ),
        "malf_v1_5_design_set": (
            "H:/Malf-Pas-Validated/MALF_Three_Part_Design_Set_v1_5",
            "successor_authority_definition",
        ),
        "pas_v1_2_design_set": (
            "H:/Malf-Pas-Validated/PAS__Three_Part_Design_Set_v1_2",
            "successor_authority_definition",
        ),
        "malf_pas_scenario_atlas": (
            "H:/Malf-Pas-Validated/MALF_PAS_Scenario_Atlas_v1_0",
            "companion_authority_asset",
        ),
        "asteria_system_design_set_v1_0": (
            "H:/Asteria-Validated/Asteria_System_Design_Set_v1_0",
            "reference_input",
        ),
        "malf_system_history": (
            "H:/Asteria-Validated/MALF-system-history",
            "historical_tradeoff_reference",
        ),
        "malf_reference": ("H:/Asteria-Validated/MALF-reference", "reference_input"),
        "lance_beggs_book_root": ("G:/《股市浮沉二十载》", "brainstorming_source"),
        "ytc_lance_beggs": ("G:/《股市浮沉二十载》/2020.(Au)LanceBeggs", "concept_source"),
        "malf_history_root": ("G:/malf-history", "historical_tradeoff_reference"),
        "duckdb_arrow_polars": ("DuckDB / Arrow / Polars", "adapter_candidate"),
        "vectorbt_backtesting_py": ("vectorbt / backtesting.py", "adapter_candidate"),
        "qlib": ("Qlib", "adapter_candidate"),
        "baostock": ("baostock", "adapter_candidate"),
        "akshare": ("AKShare", "rejected_for_semantic_ownership"),
    }
    sources = {
        item.get("key"): item for item in registry.get("sources", []) if isinstance(item, dict)
    }
    for key, (expected_path, expected_classification) in expected_sources.items():
        source = sources.get(key)
        if source is None:
            findings.append(Finding(path, f"{key} source must be registered"))
            continue
        if source.get("path") != expected_path:
            findings.append(Finding(path, f"{key} path must be {expected_path!r}"))
        if source.get("classification") != expected_classification:
            findings.append(
                Finding(path, f"{key} classification must be {expected_classification!r}")
            )

    forbidden_fragments = {
        "legacy code migration",
        "schema transplant",
        "runner transplant",
    }
    malf_history = sources.get("malf_history_root", {})
    forbidden_role = str(malf_history.get("forbidden_role", ""))
    for fragment in forbidden_fragments:
        if fragment not in forbidden_role:
            findings.append(Finding(path, f"malf_history_root must forbid {fragment!r}"))

    semantic_owner_forbidden_keys = {
        "duckdb_arrow_polars",
        "vectorbt_backtesting_py",
        "qlib",
        "akshare",
    }
    for key in semantic_owner_forbidden_keys:
        source = sources.get(key, {})
        forbidden_role = str(source.get("forbidden_role", ""))
        if "semantic" not in forbidden_role and "definition owner" not in forbidden_role:
            findings.append(Finding(path, f"{key} must forbid semantic ownership"))
    return findings


def _check_root_directory_registry(path: Path, registry: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    expected_current_roots = {
        "repo_root": "H:/Malf-Pas",
        "data_root": "H:/Malf-Pas-data",
        "backup_root": "H:/Malf-Pas-backup",
        "validated_root": "H:/Malf-Pas-Validated",
        "report_root": "H:/Malf-Pas-reprot",
        "temp_root": "H:/Malf-Pas-temp",
    }
    current_roots = {
        item.get("key"): item.get("path")
        for item in registry.get("current_roots", [])
        if isinstance(item, dict)
    }
    for key, expected_path in expected_current_roots.items():
        if current_roots.get(key) != expected_path:
            findings.append(Finding(path, f"{key} must be {expected_path!r}"))

    forbidden_current_paths = {
        "H:/Asteria",
        "H:/Asteria-data",
        "H:/Asteria-Validated",
        "H:/Asteria-report",
        "H:/Asteria-temp",
    }
    for key, raw_path in current_roots.items():
        if raw_path in forbidden_current_paths:
            findings.append(Finding(path, f"{key} must not point to previous Asteria roots"))
    return findings


def run_checks(repo_root: Path) -> list[Finding]:
    root = repo_root.resolve()
    findings: list[Finding] = []
    governance = _project_governance(root, findings)
    if governance:
        findings.extend(_check_static_flags(root, governance))
        findings.extend(_check_governance_roots(root, governance))
        _check_required_paths(root, list(governance.get("required_docs", [])), findings)
        _check_required_paths(root, list(governance.get("required_plugin_files", [])), findings)
        findings.extend(_check_registries(root, governance))
    findings.extend(_check_forbidden_repo_artifacts(root))
    findings.extend(_check_no_asteria_paths_in_plugin(root))
    return findings
