from __future__ import annotations

import json
import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from malf_pas.core.paths import MalfPasPaths
from malf_pas.data_foundation.raw_market import build_raw_market_ledger


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


class MarketBaseCliTest(unittest.TestCase):
    def test_builder_and_validator_scripts_emit_json_summary(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo_root = Path(__file__).resolve().parents[2]
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
                [(20260529, 1000, 1100, 900, 1050, 1000.0, 100)],
            )
            _write_day_file(
                client_root / "vipdoc" / "sh" / "lday" / "sh600000.day",
                [(20260529, 1000, 1100, 900, 1050, 1000.0, 100)],
            )

            paths = MalfPasPaths(
                repo_root=root / "repo",
                data_root=data_root,
                backup_root=root / "backup",
                validated_root=root / "validated",
                report_root=report_root,
                temp_root=temp_root,
            )
            paths.repo_root.mkdir()
            raw_db_path = data_root / "raw_market.duckdb"
            build_raw_market_ledger(
                run_id="raw-market-full-build-ledger-card-20260517-01",
                mode="full",
                paths=paths,
                offline_root=offline_root,
                client_root=client_root,
                asteria_data_root=asteria_root,
                db_path=raw_db_path,
                report_dir=report_root / "raw-market",
            )

            day_db = data_root / "market_base_day.duckdb"
            week_db = data_root / "market_base_week.duckdb"
            month_db = data_root / "market_base_month.duckdb"

            build_result = subprocess.run(
                [
                    sys.executable,
                    str(repo_root / "scripts" / "data_foundation" / "build_market_base_day_week_month.py"),
                    "--mode",
                    "full",
                    "--run-id",
                    "market-base-day-week-month-build-card-20260517-01",
                    "--raw-db",
                    str(raw_db_path),
                    "--day-db",
                    str(day_db),
                    "--week-db",
                    str(week_db),
                    "--month-db",
                    str(month_db),
                    "--report-dir",
                    str(report_root / "market-base"),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            validate_result = subprocess.run(
                [
                    sys.executable,
                    str(repo_root / "scripts" / "data_foundation" / "validate_market_base_day_week_month.py"),
                    "--day-db",
                    str(day_db),
                    "--week-db",
                    str(week_db),
                    "--month-db",
                    str(month_db),
                    "--json",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

        build_payload = json.loads(build_result.stdout)
        validate_payload = json.loads(validate_result.stdout)
        self.assertEqual(build_payload["run_id"], "market-base-day-week-month-build-card-20260517-01")
        self.assertEqual(build_payload["day_row_count"], 1)
        self.assertEqual(validate_payload["status"], "passed")
        self.assertEqual(validate_payload["databases"]["market_base_day"]["base_bar_row_count"], 1)

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
