from __future__ import annotations

import struct
from pathlib import Path


def write_day_file(
    path: Path,
    rows: list[tuple[int, int, int, int, int, float, int]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = bytearray()
    for trade_dt, open_, high, low, close, amount, volume in rows:
        payload.extend(
            struct.pack(
                "<IIIIIfII",
                trade_dt,
                open_,
                high,
                low,
                close,
                amount,
                volume,
                0,
            )
        )
    path.write_bytes(bytes(payload))


def seed_auxiliary_source_families(offline_root: Path, client_root: Path) -> None:
    for family_root in [
        offline_root / "stock" / "Non-Adjusted",
        offline_root / "index" / "Non-Adjusted",
        offline_root / "block" / "Non-Adjusted",
    ]:
        family_root.mkdir(parents=True, exist_ok=True)
        (family_root / f"{family_root.parent.name}-sample.txt").write_text(
            "sample",
            encoding="utf-8",
        )
    (client_root / "T0002" / "hq_cache").mkdir(parents=True, exist_ok=True)
    (client_root / "T0002" / "blocknew").mkdir(parents=True, exist_ok=True)


def write_base_dbf(
    path: Path,
    rows: list[dict[str, str]],
    *,
    fields: list[tuple[str, str, int, int]] | None = None,
) -> None:
    selected_fields = fields or [
        ("SC", "C", 1, 0),
        ("GPDM", "C", 6, 0),
        ("SSDATE", "C", 8, 0),
        ("MODIDATE", "C", 6, 0),
    ]
    header_len = 32 + len(selected_fields) * 32 + 1
    record_len = 1 + sum(item[2] for item in selected_fields)
    payload = bytearray()
    payload.extend(
        struct.pack(
            "<BBBBIHH20x",
            0x03,
            26,
            5,
            17,
            len(rows),
            header_len,
            record_len,
        )
    )
    for name, field_type, field_len, decimals in selected_fields:
        descriptor = bytearray(32)
        descriptor[: len(name)] = name.encode("ascii")
        descriptor[11] = ord(field_type)
        descriptor[16] = field_len
        descriptor[17] = decimals
        payload.extend(descriptor)
    payload.append(0x0D)
    for row in rows:
        payload.append(0x20)
        for name, field_type, field_len, _ in selected_fields:
            raw_value = str(row.get(name, ""))
            if field_type == "C":
                encoded = raw_value.encode("gbk", "ignore")[:field_len]
                payload.extend(encoded.ljust(field_len, b" "))
            else:
                encoded = raw_value.encode("ascii", "ignore")[:field_len]
                payload.extend(encoded.rjust(field_len, b" "))
    payload.append(0x1A)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(bytes(payload))


def write_tnf(path: Path, rows: list[tuple[str, str]]) -> None:
    payload = bytearray(b"\x00" * 50)
    for code, name in rows:
        record = bytearray(b"\x00" * 360)
        record[0:6] = code.encode("ascii")
        name_bytes = name.encode("gbk", "ignore")[:24]
        record[31 : 31 + len(name_bytes)] = name_bytes
        payload.extend(record)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(bytes(payload))


def write_tdxhy_cfg(path: Path, rows: list[tuple[str, str, str, str, str, str]]) -> None:
    text = "\n".join("|".join(parts) for parts in rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="gbk")


def write_tdxzs_cfg(path: Path, rows: list[tuple[str, str, str, str, str, str]]) -> None:
    text = "\n".join("|".join(parts) for parts in rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="gbk")


def write_blocknew_cfg(path: Path, rows: list[tuple[str, str]]) -> None:
    payload = bytearray()
    for name, file_stem in rows:
        record = bytearray(b"\x00" * 120)
        name_bytes = name.encode("gbk", "ignore")[:50]
        file_bytes = file_stem.encode("ascii", "ignore")[:50]
        record[: len(name_bytes)] = name_bytes
        record[50 : 50 + len(file_bytes)] = file_bytes
        payload.extend(record)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(bytes(payload))


def write_blk(path: Path, member_codes: list[str]) -> None:
    lines = ["", *member_codes]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\r\n".join(lines), encoding="ascii")


def seed_market_meta_static_files(client_root: Path) -> None:
    hq_cache = client_root / "T0002" / "hq_cache"
    blocknew = client_root / "T0002" / "blocknew"
    write_base_dbf(
        hq_cache / "base.dbf",
        [
            {"SC": "1", "GPDM": "600000", "SSDATE": "19991110", "MODIDATE": "260517"},
            {"SC": "0", "GPDM": "000001", "SSDATE": "19910403", "MODIDATE": "260517"},
            {"SC": "0", "GPDM": "300750", "SSDATE": "20180611", "MODIDATE": "260517"},
        ],
    )
    write_tnf(hq_cache / "shs.tnf", [("600000", "浦发银行")])
    write_tnf(hq_cache / "szs.tnf", [("000001", "平安银行"), ("300750", "宁德时代")])
    write_tnf(hq_cache / "bjs.tnf", [])
    write_tdxhy_cfg(
        hq_cache / "tdxhy.cfg",
        [
            ("1", "600000", "T110201", "", "", "X530101"),
            ("0", "000001", "T010101", "", "", "X620102"),
            ("0", "300750", "T020603", "", "", "X150201"),
        ],
    )
    write_tdxzs_cfg(
        hq_cache / "tdxzs.cfg",
        [
            ("银行", "880001", "3", "1", "0", "T110201"),
            ("金融服务", "880002", "3", "1", "0", "T010101"),
            ("锂电池", "880003", "3", "1", "0", "T020603"),
        ],
    )
    write_blocknew_cfg(
        blocknew / "blocknew.cfg",
        [
            ("月线初选", "YXCX"),
            ("自选股", "11111"),
        ],
    )
    write_blk(blocknew / "YXCX.blk", ["1600000", "0000001"])
    write_blk(blocknew / "11111.blk", ["0300750"])
