from __future__ import annotations

import hashlib
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_DBF_HEADER_STRUCT = struct.Struct("<BBBBIHH20x")
_TNF_HEADER_LENGTH = 50
_TNF_RECORD_LENGTH = 360
_TNF_NAME_SLICE = slice(31, 55)
_TNF_FILE_TO_EXCHANGE = {
    "shs.tnf": "SH",
    "szs.tnf": "SZ",
    "bjs.tnf": "BJ",
}
_BLOCKNEW_RECORD_LENGTH = 120


@dataclass(frozen=True)
class TdxStaticSnapshot:
    instruments: list[dict[str, Any]]
    industry_relations: list[dict[str, Any]]
    block_relations: list[dict[str, Any]]
    source_files: list[dict[str, str]]


def load_tdx_static_snapshot(
    *,
    hq_cache_root: Path,
    blocknew_root: Path,
) -> TdxStaticSnapshot:
    required_paths = [
        hq_cache_root / "base.dbf",
        hq_cache_root / "shs.tnf",
        hq_cache_root / "szs.tnf",
        hq_cache_root / "bjs.tnf",
        hq_cache_root / "tdxhy.cfg",
        hq_cache_root / "tdxzs.cfg",
        blocknew_root / "blocknew.cfg",
    ]
    for path in required_paths:
        if not path.exists():
            raise FileNotFoundError(path)
        if path.is_file() and path.stat().st_size == 0:
            raise ValueError(f"empty TDX static file: {path}")

    base_records = _parse_dbf_records(hq_cache_root / "base.dbf")
    name_map = _load_tnf_name_map(hq_cache_root)
    industry_name_map = _load_industry_name_map(hq_cache_root / "tdxzs.cfg")
    block_name_map = _parse_blocknew_cfg(blocknew_root / "blocknew.cfg")
    instruments = _build_instruments(base_records, name_map)
    industry_relations = _build_industry_relations(
        tdxhy_path=hq_cache_root / "tdxhy.cfg",
        industry_name_map=industry_name_map,
        instrument_map={item["symbol"]: item for item in instruments},
    )
    block_relations = _build_block_relations(
        blocknew_root=blocknew_root,
        block_name_map=block_name_map,
        instrument_map={item["symbol"]: item for item in instruments},
    )
    source_paths = [
        *required_paths,
        *sorted(
            item
            for item in blocknew_root.glob("*.blk")
            if item.is_file() and item.stem in block_name_map
        ),
    ]
    return TdxStaticSnapshot(
        instruments=instruments,
        industry_relations=industry_relations,
        block_relations=block_relations,
        source_files=[
            {"path": path.as_posix(), "sha256": _sha256(path)}
            for path in source_paths
        ],
    )


def _parse_dbf_records(path: Path) -> list[dict[str, str]]:
    raw = path.read_bytes()
    if len(raw) < 32:
        raise ValueError(f"invalid DBF header: {path}")
    _, _, _, _, num_records, header_len, record_len = _DBF_HEADER_STRUCT.unpack(raw[:32])
    fields: list[tuple[str, int]] = []
    cursor = 32
    while cursor < len(raw) and raw[cursor] != 0x0D:
        descriptor = raw[cursor : cursor + 32]
        field_name = descriptor[:11].split(b"\x00", 1)[0].decode("ascii", "ignore")
        field_len = descriptor[16]
        fields.append((field_name, field_len))
        cursor += 32
    if not fields:
        raise ValueError(f"DBF fields missing: {path}")

    rows: list[dict[str, str]] = []
    record_base = header_len
    for index in range(num_records):
        record = raw[record_base + index * record_len : record_base + (index + 1) * record_len]
        if not record or record[0] == 0x2A:
            continue
        offset = 1
        parsed: dict[str, str] = {}
        for field_name, field_len in fields:
            value = record[offset : offset + field_len]
            offset += field_len
            parsed[field_name] = value.decode("gbk", "ignore").strip().strip("\x00")
        rows.append(parsed)
    return rows


def _load_tnf_name_map(hq_cache_root: Path) -> dict[str, str]:
    names: dict[str, str] = {}
    for file_name, exchange in _TNF_FILE_TO_EXCHANGE.items():
        names.update(_parse_tnf_file(hq_cache_root / file_name, exchange))
    return names


def _parse_tnf_file(path: Path, exchange: str) -> dict[str, str]:
    data = path.read_bytes()
    if len(data) < _TNF_HEADER_LENGTH:
        raise ValueError(f"invalid TNF header: {path}")
    if len(data) == _TNF_HEADER_LENGTH:
        return {}
    names: dict[str, str] = {}
    record_count = (len(data) - _TNF_HEADER_LENGTH) // _TNF_RECORD_LENGTH
    for index in range(record_count):
        start = _TNF_HEADER_LENGTH + index * _TNF_RECORD_LENGTH
        record = data[start : start + _TNF_RECORD_LENGTH]
        code = record[:6].decode("ascii", "ignore").strip("\x00").strip()
        if len(code) != 6 or not code.isdigit():
            continue
        name = record[_TNF_NAME_SLICE].decode("gbk", "ignore").strip("\x00").strip()
        if name:
            names[_normalize_symbol(exchange, code)] = name
    return names


def _build_instruments(
    base_records: list[dict[str, str]],
    name_map: dict[str, str],
) -> list[dict[str, Any]]:
    rows_by_symbol: dict[str, dict[str, Any]] = {}
    for record in base_records:
        exchange = _map_sc_to_exchange(record.get("SC", ""))
        code = str(record.get("GPDM", "")).strip().upper()
        if len(code) != 6 or not exchange:
            continue
        symbol = _normalize_symbol(exchange, code)
        rows_by_symbol[symbol] = {
            "symbol": symbol,
            "asset_type": _infer_asset_type(exchange, code),
            "exchange": exchange,
            "name": name_map.get(symbol, code),
            "list_dt": _normalize_optional_date(record.get("SSDATE", "")),
            "delist_dt": None,
        }
    return [rows_by_symbol[key] for key in sorted(rows_by_symbol)]


def _load_industry_name_map(path: Path) -> dict[str, str]:
    names: dict[str, str] = {}
    for raw_line in path.read_text(encoding="gbk", errors="ignore").splitlines():
        line = raw_line.strip()
        if not line or "|" not in line:
            continue
        parts = [item.strip() for item in line.split("|")]
        if len(parts) < 6:
            continue
        name, _block_code, _level_code, _subtype_code, _is_public, ref_code = parts[:6]
        if ref_code:
            names[ref_code] = name or ref_code
    return names


def _build_industry_relations(
    *,
    tdxhy_path: Path,
    industry_name_map: dict[str, str],
    instrument_map: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    relations: dict[tuple[str, str], dict[str, Any]] = {}
    for raw_line in tdxhy_path.read_text(encoding="gbk", errors="ignore").splitlines():
        line = raw_line.strip()
        if not line or "|" not in line:
            continue
        parts = [item.strip() for item in line.split("|")]
        if len(parts) < 3:
            continue
        exchange = _map_sc_to_exchange(parts[0])
        code = parts[1].upper()
        relation_code = parts[2]
        if len(code) != 6 or not exchange or not relation_code:
            continue
        symbol = _normalize_symbol(exchange, code)
        instrument = instrument_map.get(symbol)
        if instrument is None:
            continue
        relations[(symbol, relation_code)] = {
            "symbol": symbol,
            "asset_type": instrument["asset_type"],
            "relation_type": "industry",
            "relation_code": relation_code,
            "relation_name": industry_name_map.get(relation_code, relation_code),
        }
    return [relations[key] for key in sorted(relations)]


def _parse_blocknew_cfg(path: Path) -> dict[str, str]:
    data = path.read_bytes()
    if len(data) < _BLOCKNEW_RECORD_LENGTH:
        raise ValueError(f"empty blocknew.cfg payload: {path}")
    mapping: dict[str, str] = {}
    for index in range(0, len(data), _BLOCKNEW_RECORD_LENGTH):
        record = data[index : index + _BLOCKNEW_RECORD_LENGTH]
        if not record.strip(b"\x00"):
            continue
        name = record[:50].decode("gbk", "ignore").strip("\x00").strip()
        file_stem = record[50:100].decode("ascii", "ignore").strip("\x00").strip()
        if file_stem:
            mapping[file_stem] = name or file_stem
    return mapping


def _build_block_relations(
    *,
    blocknew_root: Path,
    block_name_map: dict[str, str],
    instrument_map: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    relations: dict[tuple[str, str], dict[str, Any]] = {}
    for file_stem, block_name in sorted(block_name_map.items()):
        blk_path = blocknew_root / f"{file_stem}.blk"
        if not blk_path.exists() or blk_path.stat().st_size == 0:
            continue
        for symbol in _parse_blk_members(blk_path):
            instrument = instrument_map.get(symbol)
            if instrument is None:
                continue
            relations[(symbol, file_stem)] = {
                "symbol": symbol,
                "asset_type": instrument["asset_type"],
                "relation_type": "block",
                "relation_code": file_stem,
                "relation_name": block_name,
            }
    return [relations[key] for key in sorted(relations)]


def _parse_blk_members(path: Path) -> list[str]:
    members: list[str] = []
    for raw_line in path.read_text(encoding="ascii", errors="ignore").splitlines():
        line = raw_line.strip()
        if len(line) != 7 or not line.isdigit():
            continue
        exchange = {"0": "SZ", "1": "SH", "2": "BJ"}.get(line[0])
        code = line[1:]
        if exchange is None:
            continue
        members.append(_normalize_symbol(exchange, code))
    return sorted(set(members))


def _map_sc_to_exchange(sc: str) -> str:
    return {"0": "SZ", "1": "SH", "2": "BJ"}.get(str(sc).strip(), "")


def _normalize_symbol(exchange: str, code: str) -> str:
    return f"{exchange.lower()}{code.lower()}"


def _normalize_optional_date(value: str) -> str | None:
    text = str(value or "").strip()
    if len(text) != 8 or not text.isdigit():
        return None
    return f"{text[0:4]}-{text[4:6]}-{text[6:8]}"


def _infer_asset_type(exchange: str, code: str) -> str:
    if exchange == "SH" and code.startswith(("000", "880", "999")):
        return "index"
    if exchange == "SZ" and code.startswith("399"):
        return "index"
    if exchange == "BJ" and code.startswith("899"):
        return "index"
    return "stock"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
