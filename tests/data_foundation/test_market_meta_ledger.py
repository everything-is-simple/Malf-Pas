from __future__ import annotations

import importlib
import tempfile
import unittest
from pathlib import Path

import duckdb

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from malf_pas.core.paths import MalfPasPaths
from malf_pas.data_foundation.market_base import build_market_base_day_week_month
from malf_pas.data_foundation.raw_market import build_raw_market_ledger

from tests.data_foundation.support_tdx_meta_fixtures import (
    seed_auxiliary_source_families,
    seed_market_meta_static_files,
    write_day_file,
)


def _load_market_meta_module(test_case: unittest.TestCase):
    module_path = (
        Path(__file__).resolve().parents[2] / "src" / "malf_pas" / "data_foundation" / "market_meta.py"
    )
    if not module_path.exists():
        test_case.fail(f"market_meta runtime missing: {module_path}")
    return importlib.import_module("malf_pas.data_foundation.market_meta")


class MarketMetaLedgerTest(unittest.TestCase):
    def test_full_build_creates_market_meta_ledger_with_direct_tradability_only(self) -> None:
        market_meta = _load_market_meta_module(self)

        with tempfile.TemporaryDirectory() as temp_dir:
            paths, raw_db_path, day_db_path, client_root = self._prepare_foundation(temp_dir)
            meta_db_path = paths.data_root / "market_meta.duckdb"

            first = market_meta.build_market_meta(
                run_id="market-meta-tradability-calendar-card-20260517-01",
                mode="full",
                paths=paths,
                raw_db_path=raw_db_path,
                day_db_path=day_db_path,
                meta_db_path=meta_db_path,
                hq_cache_root=client_root / "T0002" / "hq_cache",
                blocknew_root=client_root / "T0002" / "blocknew",
                report_dir=paths.report_root / "market-meta-1",
            )
            second = market_meta.build_market_meta(
                run_id="market-meta-tradability-calendar-card-20260517-01",
                mode="full",
                paths=paths,
                raw_db_path=raw_db_path,
                day_db_path=day_db_path,
                meta_db_path=meta_db_path,
                hq_cache_root=client_root / "T0002" / "hq_cache",
                blocknew_root=client_root / "T0002" / "blocknew",
                report_dir=paths.report_root / "market-meta-2",
            )
            summary = market_meta.validate_market_meta(meta_db_path=meta_db_path)

            with duckdb.connect(str(meta_db_path), read_only=True) as con:
                instruments = con.execute(
                    """
                    select symbol, exchange, name, list_dt
                    from market_meta.market_meta.instrument_master
                    order by symbol
                    """
                ).fetchall()
                calendar = con.execute(
                    """
                    select exchange, trade_dt, is_open
                    from market_meta.market_meta.trade_calendar
                    order by exchange, trade_dt
                    """
                ).fetchall()
                tradability = con.execute(
                    """
                    select symbol, trade_dt, tradability_status, blocked_reason, source_role
                    from market_meta.market_meta.tradability_fact
                    order by symbol, trade_dt
                    """
                ).fetchall()
                unresolved_symbols = con.execute(
                    """
                    select unresolved_symbol_count, unresolved_gap_count
                    from market_meta.market_meta.source_manifest
                    """
                ).fetchone()
                relations = con.execute(
                    """
                    select symbol, relation_type, relation_code, effective_from, effective_to
                    from market_meta.market_meta.industry_block_relation
                    order by symbol, relation_type, relation_code
                    """
                ).fetchall()

        self.assertEqual(first.instrument_row_count, 3)
        self.assertEqual(second.instrument_row_count, 3)
        self.assertEqual(first.tradability_row_count, 4)
        self.assertEqual(summary["status"], "passed")
        self.assertEqual(summary["databases"]["market_meta"]["instrument_master_row_count"], 3)
        self.assertEqual(summary["databases"]["market_meta"]["trade_calendar_row_count"], 4)
        self.assertEqual(summary["databases"]["market_meta"]["tradability_direct_covered_row_count"], 4)
        self.assertEqual(summary["databases"]["market_meta"]["tradability_unresolved_gap_count"], 2)
        self.assertEqual(
            [(symbol, exchange, name, str(list_dt)) for symbol, exchange, name, list_dt in instruments],
            [
                ("sh600000", "SH", "浦发银行", "1999-11-10"),
                ("sz000001", "SZ", "平安银行", "1991-04-03"),
                ("sz300750", "SZ", "宁德时代", "2018-06-11"),
            ],
        )
        self.assertEqual(
            [(exchange, str(trade_dt), is_open) for exchange, trade_dt, is_open in calendar],
            [
                ("SH", "2026-05-29", True),
                ("SH", "2026-06-02", True),
                ("SZ", "2026-05-29", True),
                ("SZ", "2026-06-02", True),
            ],
        )
        self.assertEqual(
            [
                (symbol, str(trade_dt), tradability_status, blocked_reason, source_role)
                for symbol, trade_dt, tradability_status, blocked_reason, source_role in tradability
            ],
            [
                ("sh600000", "2026-05-29", "tradable", None, "tdx_direct"),
                ("sh600000", "2026-06-02", "tradable", None, "tdx_direct"),
                ("sz000001", "2026-05-29", "tradable", None, "tdx_direct"),
                ("sz000001", "2026-06-02", "tradable", None, "tdx_direct"),
            ],
        )
        self.assertEqual(unresolved_symbols, (1, 2))
        self.assertEqual(
            {(symbol, relation_type, relation_code, str(effective_from), effective_to) for symbol, relation_type, relation_code, effective_from, effective_to in relations},
            {
                ("sh600000", "block", "YXCX", "2026-06-02", None),
                ("sh600000", "industry", "T110201", "2026-06-02", None),
                ("sz000001", "block", "YXCX", "2026-06-02", None),
                ("sz000001", "industry", "T010101", "2026-06-02", None),
                ("sz300750", "block", "11111", "2026-06-02", None),
                ("sz300750", "industry", "T020603", "2026-06-02", None),
            },
        )

    def test_missing_static_file_fails_fast(self) -> None:
        market_meta = _load_market_meta_module(self)

        with tempfile.TemporaryDirectory() as temp_dir:
            paths, raw_db_path, day_db_path, client_root = self._prepare_foundation(temp_dir)
            (client_root / "T0002" / "hq_cache" / "tdxhy.cfg").unlink()

            with self.assertRaisesRegex(FileNotFoundError, "tdxhy.cfg"):
                market_meta.build_market_meta(
                    run_id="market-meta-tradability-calendar-card-20260517-01",
                    mode="full",
                    paths=paths,
                    raw_db_path=raw_db_path,
                    day_db_path=day_db_path,
                    meta_db_path=paths.data_root / "market_meta.duckdb",
                    hq_cache_root=client_root / "T0002" / "hq_cache",
                    blocknew_root=client_root / "T0002" / "blocknew",
                    report_dir=paths.report_root / "market-meta",
                )

    def _prepare_foundation(self, temp_dir: str) -> tuple[MalfPasPaths, Path, Path, Path]:
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

        seed_auxiliary_source_families(offline_root, client_root)
        seed_market_meta_static_files(client_root)
        write_day_file(
            offline_root / "raw" / "sh" / "lday" / "sh600000.day",
            [
                (20260529, 1000, 1100, 900, 1050, 1000.0, 100),
                (20260602, 1070, 1120, 1030, 1110, 1500.0, 130),
            ],
        )
        write_day_file(
            offline_root / "raw" / "sz" / "lday" / "sz000001.day",
            [
                (20260529, 1500, 1520, 1480, 1510, 2000.0, 200),
                (20260602, 1510, 1530, 1500, 1525, 2300.0, 210),
            ],
        )
        write_day_file(
            client_root / "vipdoc" / "sh" / "lday" / "sh600000.day",
            [
                (20260529, 1000, 1100, 900, 1050, 1000.0, 100),
                (20260602, 1070, 1120, 1030, 1110, 1500.0, 130),
            ],
        )
        write_day_file(
            client_root / "vipdoc" / "sz" / "lday" / "sz000001.day",
            [
                (20260529, 1500, 1520, 1480, 1510, 2000.0, 200),
                (20260602, 1510, 1530, 1500, 1525, 2300.0, 210),
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
        return paths, raw_db_path, day_db_path, client_root


if __name__ == "__main__":
    unittest.main()
