from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ContractFinding:
    path: Path
    message: str


REQUIRED_DATABASES = {
    "raw_market": "raw_market.duckdb",
    "market_base_day": "market_base_day.duckdb",
    "market_base_week": "market_base_week.duckdb",
    "market_base_month": "market_base_month.duckdb",
    "market_meta": "market_meta.duckdb",
    "data_control": "data_control.duckdb",
}

REQUIRED_COMMON_GOVERNANCE_KEYS = [
    "symbol",
    "asset_type",
    "timeframe",
    "bar_dt",
    "trade_dt",
    "run_id",
    "source_run_id",
    "schema_version",
    "rule_version",
    "source_manifest_hash",
    "checkpoint_key",
]

REQUIRED_TABLE_FAMILIES = {
    "raw_market": {
        "source_file",
        "raw_bar",
        "ingest_run",
        "reject_audit",
        "source_manifest",
        "schema_version",
    },
    "market_base_day": {
        "base_bar",
        "latest_pointer",
        "base_run",
        "dirty_scope",
        "source_manifest",
        "schema_version",
    },
    "market_base_week": {
        "base_bar",
        "latest_pointer",
        "base_run",
        "dirty_scope",
        "source_manifest",
        "schema_version",
    },
    "market_base_month": {
        "base_bar",
        "latest_pointer",
        "base_run",
        "dirty_scope",
        "source_manifest",
        "schema_version",
    },
    "market_meta": {
        "instrument_master",
        "trade_calendar",
        "tradability_fact",
        "industry_block_relation",
        "source_manifest",
        "schema_version",
    },
    "data_control": {
        "run_ledger",
        "dirty_queue",
        "checkpoint",
        "resume_state",
        "audit_state",
        "freshness_audit",
        "data_readout",
        "schema_version",
    },
}

BUSINESS_FACT_GROUPS = {"source_fact", "base_fact", "meta_fact"}
DATA_CONTROL_GROUPS = {"orchestration", "freshness_readout"}
FORBIDDEN_FIELD_FRAGMENTS = {
    "malf",
    "pas",
    "signal",
    "position",
    "broker",
    "order",
    "profit",
    "buy",
    "sell",
    "fill",
}


def load_contract_registry(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def validate_contract_registry(path: Path, registry: dict[str, Any]) -> list[ContractFinding]:
    findings: list[ContractFinding] = []
    _check_static_contract_values(path, registry, findings)
    _check_common_governance_keys(path, registry, findings)
    _check_database_contracts(path, registry, findings)
    return findings


def contract_summary(path: Path, registry: dict[str, Any]) -> dict[str, Any]:
    findings = validate_contract_registry(path, registry)
    return {
        "status": "passed" if not findings else "failed",
        "registry": str(path),
        "database_count": len(_databases_by_name(registry)),
        "table_family_count": _table_family_count(registry),
        "forbidden_semantics_passed": not any(
            "forbidden downstream semantic" in item.message for item in findings
        ),
        "next_card": registry.get("next_data_foundation_card"),
        "finding_count": len(findings),
        "findings": [item.message for item in findings],
    }


def _check_static_contract_values(
    path: Path, registry: dict[str, Any], findings: list[ContractFinding]
) -> None:
    expected_values: dict[str, Any] = {
        "registry_version": "2026-05-17.v1",
        "stage": "governance-only",
        "formal_db_mutation": "no",
        "broker_feasibility": "deferred",
        "authority_doc": "docs/03-roadmap/01-local-tdx-data-foundation-module-db-roadmap-v1.md",
        "run_id": "data-module-db-contract-card-20260517-01",
        "roadmap_order": 20,
        "card_status": "passed",
        "data_root": "H:/Malf-Pas-data",
        "current_card_creates_db": False,
        "current_card_writes_data_root": False,
        "formal_db_created": False,
        "downstream_runtime_authorized": False,
        "legacy_schema_migration_authorized": False,
        "week_month_availability_status": "day-derived",
        "week_month_rule_version": "data-foundation-week-month-from-day-v1",
        "tradability_availability_status": "blocked",
        "tradability_source_role": "blocked",
        "first_consumer": "MALF v1.5",
        "next_data_foundation_card": "raw-market-full-build-ledger-card",
    }
    for key, expected in expected_values.items():
        if registry.get(key) != expected:
            findings.append(ContractFinding(path, f"{key} must be {expected!r}"))


def _check_common_governance_keys(
    path: Path, registry: dict[str, Any], findings: list[ContractFinding]
) -> None:
    if registry.get("common_governance_keys") != REQUIRED_COMMON_GOVERNANCE_KEYS:
        findings.append(ContractFinding(path, "common_governance_keys must match card 20 order"))

    if "run_id" not in registry.get("audit_lineage_keys", []):
        findings.append(ContractFinding(path, "run_id must be registered as audit lineage only"))

    if "run_id" not in registry.get("business_natural_key_forbidden_fields", []):
        findings.append(
            ContractFinding(path, "run_id must be forbidden from business natural keys")
        )


def _check_database_contracts(
    path: Path, registry: dict[str, Any], findings: list[ContractFinding]
) -> None:
    databases = _databases_by_name(registry)
    missing_dbs = sorted(set(REQUIRED_DATABASES) - set(databases))
    if missing_dbs:
        findings.append(ContractFinding(path, f"missing Data database contracts: {missing_dbs}"))

    for logical_name, file_name in REQUIRED_DATABASES.items():
        database = databases.get(logical_name)
        if database is None:
            continue
        if database.get("file_name") != file_name:
            findings.append(ContractFinding(path, f"{logical_name} file_name must be {file_name}"))
        if not str(database.get("ledger_role", "")).strip():
            findings.append(ContractFinding(path, f"{logical_name} must define ledger_role"))
        _check_table_families(path, logical_name, database, findings)


def _check_table_families(
    path: Path,
    logical_name: str,
    database: dict[str, Any],
    findings: list[ContractFinding],
) -> None:
    table_families = {
        item.get("family"): item
        for item in database.get("table_families", [])
        if isinstance(item, dict)
    }
    required_families = REQUIRED_TABLE_FAMILIES[logical_name]
    missing_families = sorted(required_families - set(table_families))
    if missing_families:
        if logical_name == "data_control" and "run_ledger" in missing_families:
            findings.append(ContractFinding(path, "data_control must include run_ledger"))
        findings.append(
            ContractFinding(path, f"{logical_name} missing table families: {missing_families}")
        )

    for family_name, table in table_families.items():
        _check_table_contract(path, logical_name, str(family_name), table, findings)


def _check_table_contract(
    path: Path,
    logical_name: str,
    family_name: str,
    table: dict[str, Any],
    findings: list[ContractFinding],
) -> None:
    table_group = table.get("table_group")
    if logical_name == "data_control" and table_group not in DATA_CONTROL_GROUPS:
        findings.append(
            ContractFinding(
                path,
                "data_control table families must separate orchestration and freshness/readout",
            )
        )

    for key in [
        "table_name",
        "required_fields",
        "natural_key",
        "governance_keys",
        "lineage_fields",
    ]:
        if not table.get(key):
            findings.append(
                ContractFinding(path, f"{logical_name}.{family_name} must define {key}")
            )

    if table_group in BUSINESS_FACT_GROUPS and "run_id" in table.get("natural_key", []):
        findings.append(
            ContractFinding(
                path,
                f"{logical_name}.{family_name}: run_id must not be a business fact natural key",
            )
        )

    required_fields = [str(item).lower() for item in table.get("required_fields", [])]
    for field_name in required_fields:
        if any(fragment in field_name for fragment in FORBIDDEN_FIELD_FRAGMENTS):
            findings.append(
                ContractFinding(
                    path,
                    f"{logical_name}.{family_name}: "
                    f"forbidden downstream semantic field {field_name}",
                )
            )

    lineage_fields = set(table.get("lineage_fields", []))
    for required in ["source_run_id", "schema_version", "rule_version", "source_manifest_hash"]:
        if required not in lineage_fields:
            findings.append(
                ContractFinding(path, f"{logical_name}.{family_name} lineage missing {required}")
            )


def _databases_by_name(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        item.get("logical_name"): item
        for item in registry.get("databases", [])
        if isinstance(item, dict)
    }


def _table_family_count(registry: dict[str, Any]) -> int:
    return sum(
        len(item.get("table_families", []))
        for item in registry.get("databases", [])
        if isinstance(item, dict)
    )
