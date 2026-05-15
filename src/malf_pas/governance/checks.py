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
            findings.append(Finding(path, "workflow plugin must not retain hard-coded Asteria paths"))
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
            findings.append(Finding(repo_root / raw_path, "broker_feasibility must remain deferred"))
        if raw_path == "governance/root_directory_registry.toml":
            findings.extend(_check_root_directory_registry(repo_root / raw_path, registry))
        if raw_path == "governance/source_authority_registry.toml":
            findings.extend(_check_source_authority_registry(repo_root / raw_path, registry))
    return findings


def _check_source_authority_registry(path: Path, registry: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    expected_sources = {
        "lance_beggs_book_root": ("G:/《股市浮沉二十载》", "brainstorming_source"),
        "ytc_lance_beggs": ("G:/《股市浮沉二十载》/2020.(Au)LanceBeggs", "concept_source"),
        "malf_history_root": ("G:/malf-history", "historical_tradeoff_reference"),
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
