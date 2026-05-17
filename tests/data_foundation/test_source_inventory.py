from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from malf_pas.data_foundation.source_inventory import build_source_inventory


class SourceInventoryTest(unittest.TestCase):
    def test_inventory_keeps_asteria_data_as_readonly_reference(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            tdx_offline = root / "tdx_offline_Data"
            tdx_client = root / "new_tdx64"
            asteria_data = root / "Asteria-data"

            (tdx_offline / "stock" / "Non-Adjusted").mkdir(parents=True)
            (tdx_offline / "stock" / "Non-Adjusted" / "SH#600000.txt").write_text(
                "sample",
                encoding="utf-8",
            )
            (tdx_offline / "raw" / "sh" / "lday").mkdir(parents=True)
            (tdx_offline / "raw" / "sh" / "lday" / "sh600000.day").write_bytes(b"day")
            (tdx_client / "vipdoc" / "sh" / "lday").mkdir(parents=True)
            (tdx_client / "vipdoc" / "sh" / "lday" / "sh600000.day").write_bytes(b"day")
            asteria_data.mkdir()
            for name in [
                "raw_market.duckdb",
                "market_base_day.duckdb",
                "market_base_week.duckdb",
                "market_base_month.duckdb",
                "market_meta.duckdb",
            ]:
                (asteria_data / name).write_bytes(b"")

            inventory = build_source_inventory(
                tdx_offline_root=tdx_offline,
                tdx_client_root=tdx_client,
                asteria_data_root=asteria_data,
            )

        self.assertEqual(
            inventory["source_roles"]["current_truth_roots"],
            [str(tdx_offline), str(tdx_client)],
        )
        self.assertEqual(
            inventory["source_roles"]["previous_reference_root"],
            str(asteria_data),
        )
        self.assertEqual(
            inventory["source_roles"]["forbidden_formal_truth"],
            ["TuShare", "baostock", "AKShare"],
        )
        self.assertEqual(
            inventory["previous_asteria_data_readonly_reference"]["role"],
            "reference_baseline_only",
        )
        self.assertFalse(
            inventory["previous_asteria_data_readonly_reference"]["current_truth_owner"]
        )
        self.assertEqual(inventory["week_month_availability"]["status"], "day-derived")
        self.assertEqual(inventory["tradability_availability"]["status"], "blocked")

    def test_inventory_records_missing_previous_data_db_as_not_present(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            tdx_offline = root / "tdx_offline_Data"
            tdx_client = root / "new_tdx64"
            asteria_data = root / "Asteria-data"
            tdx_offline.mkdir()
            tdx_client.mkdir()
            asteria_data.mkdir()

            inventory = build_source_inventory(
                tdx_offline_root=tdx_offline,
                tdx_client_root=tdx_client,
                asteria_data_root=asteria_data,
            )

        dbs = inventory["previous_asteria_data_readonly_reference"]["databases"]
        self.assertEqual(dbs["raw_market.duckdb"]["status"], "missing")
        self.assertEqual(dbs["market_meta.duckdb"]["status"], "missing")


if __name__ == "__main__":
    unittest.main()
