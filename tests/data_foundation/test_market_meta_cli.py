from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from malf_pas.core.paths import MalfPasPaths
from malf_pas.data_foundation.market_base import build_market_base_day_week_month
from malf_pas.data_foundation.raw_market import build_raw_market_ledger

from tests.data_foundation.support_tdx_meta_fixtures import (
    seed_auxiliary_source_families,
    seed_market_meta_static_files,
    write_day_file,
)


class MarketMetaCliTest(unittest.TestCase):
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

            seed_auxiliary_source_families(offline_root, client_root)
            seed_market_meta_static_files(client_root)
            write_day_file(
                offline_root / "raw" / "sh" / "lday" / "sh600000.day",
                [(20260529, 1000, 1100, 900, 1050, 1000.0, 100)],
            )
            write_day_file(
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
            day_db_path = data_root / "market_base_day.duckdb"
            build_market_base_day_week_month(
                run_id="market-base-day-week-month-build-card-20260517-01",
                mode="full",
                paths=paths,
                raw_db_path=raw_db_path,
                day_db_path=day_db_path,
                week_db_path=data_root / "market_base_week.duckdb",
                month_db_path=data_root / "market_base_month.duckdb",
                report_dir=report_root / "market-base",
            )

            meta_db_path = data_root / "market_meta.duckdb"
            build_result = subprocess.run(
                [
                    sys.executable,
                    str(
                        repo_root
                        / "scripts"
                        / "data_foundation"
                        / "build_market_meta_tradability_calendar.py"
                    ),
                    "--mode",
                    "bounded",
                    "--run-id",
                    "market-meta-tradability-calendar-card-20260517-01",
                    "--raw-db",
                    str(raw_db_path),
                    "--day-db",
                    str(day_db_path),
                    "--meta-db",
                    str(meta_db_path),
                    "--hq-cache-root",
                    str(client_root / "T0002" / "hq_cache"),
                    "--blocknew-root",
                    str(client_root / "T0002" / "blocknew"),
                    "--report-dir",
                    str(report_root / "market-meta"),
                    "--limit-symbols",
                    "1",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            validate_result = subprocess.run(
                [
                    sys.executable,
                    str(
                        repo_root
                        / "scripts"
                        / "data_foundation"
                        / "validate_market_meta_tradability_calendar.py"
                    ),
                    "--meta-db",
                    str(meta_db_path),
                    "--json",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

        build_payload = json.loads(build_result.stdout)
        validate_payload = json.loads(validate_result.stdout)
        self.assertEqual(build_payload["run_id"], "market-meta-tradability-calendar-card-20260517-01")
        self.assertEqual(build_payload["mode"], "bounded")
        self.assertEqual(build_payload["instrument_row_count"], 1)
        self.assertEqual(validate_payload["status"], "passed")
        self.assertEqual(validate_payload["databases"]["market_meta"]["instrument_master_row_count"], 1)


if __name__ == "__main__":
    unittest.main()
