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
        if raw_path == "governance/malf_v1_4_immutability_registry.toml":
            findings.extend(_check_malf_v1_4_immutability_registry(repo_root / raw_path, registry))
        if raw_path == "governance/predecessor_strength_registry.toml":
            findings.extend(_check_predecessor_strength_registry(repo_root / raw_path, registry))
        if raw_path == "governance/pas_axiomatic_state_machine_registry.toml":
            findings.extend(_check_pas_axiomatic_state_machine_registry(repo_root / raw_path, registry))
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
        findings.append(Finding(path, "semantic_chain must remain MALF WavePosition -> PAS -> Signal"))

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
