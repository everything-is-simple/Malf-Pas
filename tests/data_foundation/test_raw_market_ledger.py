from __future__ import annotations

import json
import struct
import tempfile
import unittest
from pathlib import Path

import duckdb

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from malf_pas.core.paths import MalfPasPaths
from malf_pas.data_foundation.raw_market import (
    RAW_MARKET_RULE_VERSION,
    RAW_MARKET_SCHEMA_VERSION,
    build_raw_market_ledger,
    parse_tdx_day_file,
    validate_raw_market_ledger,
)


def _write_day_file(path: Path, rows: list[tuple[int, int, int, int, int, float, int]]) -> None:
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


class RawMarketLedgerTest(unittest.TestCase):
    def test_parse_tdx_day_file_reads_expected_bar_values(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            day_path = Path(temp_dir) / "sh600000.day"
            _write_day_file(
                day_path,
                [
                    (20260515, 1234, 1250, 1200, 1245, 8800.5, 9000),
                    (20260516, 1245, 1260, 1230, 1255, 9900.0, 9500),
                ],
            )

            rows = parse_tdx_day_file(
                day_path,
                symbol="sh600000",
                asset_type="stock",
                timeframe="day",
                source_file_id="offline:sh600000.day",
                source_run_id="test-source-run",
                source_manifest_hash="manifest-hash",
                schema_version=RAW_MARKET_SCHEMA_VERSION,
                rule_version=RAW_MARKET_RULE_VERSION,
            )

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["bar_dt"], "2026-05-15")
        self.assertEqual(rows[0]["open"], 12.34)
        self.assertEqual(rows[0]["high"], 12.5)
        self.assertEqual(rows[0]["low"], 12.0)
        self.assertEqual(rows[0]["close"], 12.45)
        self.assertEqual(rows[0]["amount"], 8800.5)
        self.assertEqual(rows[0]["volume"], 9000)
        self.assertEqual(rows[1]["bar_dt"], "2026-05-16")

    def test_full_build_prefers_offline_root_and_audits_rerun(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo_root = root / "repo"
            repo_root.mkdir()
            data_root = root / "data"
            report_root = root / "report"
            temp_root = root / "temp"
            offline_root = root / "tdx_offline_Data"
            client_root = root / "new_tdx64"
            asteria_root = root / "Asteria-data"
            asteria_root.mkdir()

            self._seed_auxiliary_source_families(offline_root, client_root)
            _write_day_file(
                offline_root / "raw" / "sh" / "lday" / "sh600000.day",
                [
                    (20260515, 1234, 1250, 1200, 1245, 8800.5, 9000),
                    (20260516, 1245, 1260, 1230, 1255, 9900.0, 9500),
                ],
            )
            _write_day_file(
                client_root / "vipdoc" / "sh" / "lday" / "sh600000.day",
                [
                    (20260515, 1234, 1250, 1200, 1245, 8800.5, 9000),
                    (20260516, 1245, 1262, 1230, 1255, 9900.0, 9500),
                ],
            )
            _write_day_file(
                client_root / "vipdoc" / "sz" / "lday" / "sz300001.day",
                [
                    (20260516, 2234, 2260, 2200, 2255, 12000.0, 1200),
                ],
            )

            paths = MalfPasPaths(
                repo_root=repo_root,
                data_root=data_root,
                backup_root=root / "backup",
                validated_root=root / "validated",
                report_root=report_root,
                temp_root=temp_root,
            )
            db_path = data_root / "raw_market.duckdb"

            first = build_raw_market_ledger(
                run_id="raw-market-full-build-ledger-card-20260517-01",
                mode="full",
                paths=paths,
                offline_root=offline_root,
                client_root=client_root,
                asteria_data_root=asteria_root,
                db_path=db_path,
                report_dir=report_root / "run-1",
            )
            second = build_raw_market_ledger(
                run_id="raw-market-full-build-ledger-card-20260517-01",
                mode="daily_incremental",
                paths=paths,
                offline_root=offline_root,
                client_root=client_root,
                asteria_data_root=asteria_root,
                db_path=db_path,
                report_dir=report_root / "run-2",
            )

            summary = validate_raw_market_ledger(db_path)

            with duckdb.connect(str(db_path), read_only=True) as con:
                canonical = con.execute(
                    """
                    select symbol, asset_type, timeframe, bar_dt, source_file_id
                    from raw_market.raw_market.raw_bar
                    order by symbol, bar_dt
                    """
                ).fetchall()
                canonical = [
                    (symbol, asset_type, timeframe, str(bar_dt), source_file_id)
                    for symbol, asset_type, timeframe, bar_dt, source_file_id in canonical
                ]
                reject_reasons = con.execute(
                    """
                    select reject_reason, audit_status, count(*)
                    from raw_market.raw_market.reject_audit
                    group by 1, 2
                    order by 1, 2
                    """
                ).fetchall()
                source_files = con.execute(
                    "select count(*) from raw_market.raw_market.source_file"
                ).fetchone()[0]
                ingest_modes = con.execute(
                    "select distinct ingest_mode from raw_market.raw_market.ingest_run order by ingest_mode"
                ).fetchall()

        self.assertEqual(first.raw_bar_rows, 3)
        self.assertEqual(second.raw_bar_rows, 3)
        self.assertEqual(
            canonical,
            [
                ("sh600000", "stock", "day", "2026-05-15", "offline:raw:sh600000.day"),
                ("sh600000", "stock", "day", "2026-05-16", "offline:raw:sh600000.day"),
                ("sz300001", "stock", "day", "2026-05-16", "client:vipdoc:sz300001.day"),
            ],
        )
        self.assertGreaterEqual(source_files, 8)
        self.assertIn(("dual_root_divergence", "blocked", 1), reject_reasons)
        self.assertIn(("skipped_unchanged", "passed", 2), reject_reasons)
        self.assertEqual(ingest_modes, [("daily_incremental",)])
        self.assertEqual(summary["status"], "passed")
        self.assertEqual(summary["raw_bar_row_count"], 3)
        self.assertTrue(summary["natural_key_unique"])

    def test_resume_rejects_manifest_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo_root = root / "repo"
            repo_root.mkdir()
            data_root = root / "data"
            report_root = root / "report"
            temp_root = root / "temp"
            offline_root = root / "tdx_offline_Data"
            client_root = root / "new_tdx64"
            asteria_root = root / "Asteria-data"
            asteria_root.mkdir()

            self._seed_auxiliary_source_families(offline_root, client_root)
            target_file = offline_root / "raw" / "sh" / "lday" / "sh600000.day"
            _write_day_file(
                target_file,
                [(20260515, 1234, 1250, 1200, 1245, 8800.5, 9000)],
            )

            paths = MalfPasPaths(
                repo_root=repo_root,
                data_root=data_root,
                backup_root=root / "backup",
                validated_root=root / "validated",
                report_root=report_root,
                temp_root=temp_root,
            )
            db_path = data_root / "raw_market.duckdb"

            build_raw_market_ledger(
                run_id="raw-market-full-build-ledger-card-20260517-01",
                mode="full",
                paths=paths,
                offline_root=offline_root,
                client_root=client_root,
                asteria_data_root=asteria_root,
                db_path=db_path,
                report_dir=report_root / "run-1",
            )
            _write_day_file(
                target_file,
                [(20260515, 1234, 1266, 1200, 1245, 8800.5, 9000)],
            )

            with self.assertRaisesRegex(RuntimeError, "resume requires matching manifest"):
                build_raw_market_ledger(
                    run_id="raw-market-full-build-ledger-card-20260517-01",
                    mode="resume",
                    paths=paths,
                    offline_root=offline_root,
                    client_root=client_root,
                    asteria_data_root=asteria_root,
                    db_path=db_path,
                    report_dir=report_root / "run-2",
                )

    def _seed_auxiliary_source_families(self, offline_root: Path, client_root: Path) -> None:
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
        (client_root / "T0002" / "hq_cache" / "base.dbf").write_bytes(b"dbf")
        (client_root / "T0002" / "blocknew").mkdir(parents=True, exist_ok=True)
        (client_root / "T0002" / "blocknew" / "block.blk").write_bytes(b"blk")


if __name__ == "__main__":
    unittest.main()
