from __future__ import annotations

import importlib
import struct
import tempfile
import unittest
from pathlib import Path

import duckdb

import sys

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


def _load_market_base_module(test_case: unittest.TestCase):
    module_path = (
        Path(__file__).resolve().parents[2] / "src" / "malf_pas" / "data_foundation" / "market_base.py"
    )
    if not module_path.exists():
        test_case.fail(f"market_base runtime missing: {module_path}")
    return importlib.import_module("malf_pas.data_foundation.market_base")


class MarketBaseLedgerTest(unittest.TestCase):
    def test_full_build_creates_day_week_month_ledgers_with_lineage(self) -> None:
        market_base = _load_market_base_module(self)

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
                    (20260529, 1000, 1100, 900, 1050, 1000.0, 100),
                    (20260601, 1070, 1120, 1030, 1110, 1500.0, 130),
                    (20260602, 1110, 1130, 1080, 1120, 1800.0, 160),
                ],
            )
            _write_day_file(
                client_root / "vipdoc" / "sh" / "lday" / "sh600000.day",
                [
                    (20260529, 1000, 1100, 900, 1050, 1000.0, 100),
                    (20260601, 1070, 1120, 1030, 1110, 1500.0, 130),
                    (20260602, 1110, 1130, 1080, 1120, 1800.0, 160),
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
            run_id = "market-base-day-week-month-build-card-20260517-01"

            first = market_base.build_market_base_day_week_month(
                run_id=run_id,
                mode="full",
                paths=paths,
                raw_db_path=raw_db_path,
                day_db_path=day_db,
                week_db_path=week_db,
                month_db_path=month_db,
                report_dir=report_root / "market-base-1",
            )
            second = market_base.build_market_base_day_week_month(
                run_id=run_id,
                mode="full",
                paths=paths,
                raw_db_path=raw_db_path,
                day_db_path=day_db,
                week_db_path=week_db,
                month_db_path=month_db,
                report_dir=report_root / "market-base-2",
            )
            summary = market_base.validate_market_base_day_week_month(
                day_db_path=day_db,
                week_db_path=week_db,
                month_db_path=month_db,
            )

            with duckdb.connect(str(day_db), read_only=True) as con:
                day_rows = con.execute(
                    """
                    select bar_dt, trade_dt, analysis_price_line, source_run_id
                    from market_base_day.market_base_day.base_bar
                    order by bar_dt
                    """
                ).fetchall()
                day_latest = con.execute(
                    "select symbol, latest_bar_dt from market_base_day.market_base_day.latest_pointer"
                ).fetchall()
            with duckdb.connect(str(week_db), read_only=True) as con:
                week_rows = con.execute(
                    """
                    select bar_dt, open, high, low, close, volume, amount, derived_from_timeframe, source_run_id
                    from market_base_week.market_base_week.base_bar
                    order by bar_dt
                    """
                ).fetchall()
            with duckdb.connect(str(month_db), read_only=True) as con:
                month_rows = con.execute(
                    """
                    select bar_dt, open, high, low, close, volume, amount, derived_from_timeframe, source_run_id
                    from market_base_month.market_base_month.base_bar
                    order by bar_dt
                    """
                ).fetchall()

        self.assertEqual(first.day_row_count, 3)
        self.assertEqual(second.day_row_count, 3)
        self.assertEqual(first.week_row_count, 2)
        self.assertEqual(first.month_row_count, 2)
        self.assertEqual(
            [(str(bar_dt), str(trade_dt), analysis_price_line, source_run_id) for bar_dt, trade_dt, analysis_price_line, source_run_id in day_rows],
            [
                ("2026-05-29", "2026-05-29", "backward", "raw-market-full-build-ledger-card-20260517-01"),
                ("2026-06-01", "2026-06-01", "backward", "raw-market-full-build-ledger-card-20260517-01"),
                ("2026-06-02", "2026-06-02", "backward", "raw-market-full-build-ledger-card-20260517-01"),
            ],
        )
        self.assertEqual(
            [(symbol, str(latest_bar_dt)) for symbol, latest_bar_dt in day_latest],
            [("sh600000", "2026-06-02")],
        )
        self.assertEqual(
            [(str(bar_dt), open_, high, low, close, volume, amount, derived_from_timeframe, source_run_id) for bar_dt, open_, high, low, close, volume, amount, derived_from_timeframe, source_run_id in week_rows],
            [
                ("2026-05-29", 10.0, 11.0, 9.0, 10.5, 100, 1000.0, "day", f"{run_id}:day"),
                ("2026-06-02", 10.7, 11.3, 10.3, 11.2, 290, 3300.0, "day", f"{run_id}:day"),
            ],
        )
        self.assertEqual(
            [(str(bar_dt), open_, high, low, close, volume, amount, derived_from_timeframe, source_run_id) for bar_dt, open_, high, low, close, volume, amount, derived_from_timeframe, source_run_id in month_rows],
            [
                ("2026-05-29", 10.0, 11.0, 9.0, 10.5, 100, 1000.0, "day", f"{run_id}:day"),
                ("2026-06-02", 10.7, 11.3, 10.3, 11.2, 290, 3300.0, "day", f"{run_id}:day"),
            ],
        )
        self.assertEqual(summary["status"], "passed")
        self.assertEqual(summary["databases"]["market_base_day"]["base_bar_row_count"], 3)
        self.assertTrue(summary["databases"]["market_base_week"]["latest_pointer_unique"])
        self.assertTrue(summary["databases"]["market_base_month"]["natural_key_unique"])

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
