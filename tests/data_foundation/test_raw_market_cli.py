from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class RawMarketCliTest(unittest.TestCase):
    def test_validator_script_emits_json_summary(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo_root = Path(__file__).resolve().parents[2]
            db_path = root / "raw_market.duckdb"

            seed = (
                "import duckdb\n"
                f"con=duckdb.connect(r'{db_path}')\n"
                "con.execute('create schema raw_market')\n"
                "con.execute(\"create table raw_market.raw_market.source_file (source_file_id varchar, source_root varchar, source_path varchar, asset_type varchar, timeframe varchar, source_revision varchar, size bigint, mtime double, content_hash varchar, source_manifest_hash varchar, source_run_id varchar, schema_version varchar, rule_version varchar, primary key(source_root, source_path, source_revision))\")\n"
                "con.execute(\"create table raw_market.raw_market.raw_bar (symbol varchar, asset_type varchar, timeframe varchar, bar_dt date, open double, high double, low double, close double, volume bigint, amount double, source_file_id varchar, source_run_id varchar, schema_version varchar, rule_version varchar, source_manifest_hash varchar, primary key(symbol, asset_type, timeframe, bar_dt))\")\n"
                "con.execute(\"create table raw_market.raw_market.ingest_run (run_id varchar primary key, source_root varchar, ingest_mode varchar, started_at timestamp, finished_at timestamp, audit_status varchar, source_manifest_hash varchar, source_run_id varchar, schema_version varchar, rule_version varchar)\")\n"
                "con.execute(\"create table raw_market.raw_market.reject_audit (reject_id varchar primary key, run_id varchar, source_file_id varchar, reject_reason varchar, audit_status varchar, source_manifest_hash varchar, source_run_id varchar, schema_version varchar, rule_version varchar)\")\n"
                "con.execute(\"create table raw_market.raw_market.source_manifest (manifest_id varchar, source_manifest_hash varchar primary key, source_root varchar, provider_role varchar, dataset_scope varchar, input_version varchar, generated_by_run_id varchar, audit_status varchar, source_run_id varchar, schema_version varchar, rule_version varchar)\")\n"
                "con.execute(\"create table raw_market.raw_market.schema_version (schema_version varchar, rule_version varchar, effective_from timestamp, registered_by_run_id varchar, source_manifest_hash varchar, source_run_id varchar, primary key(schema_version, rule_version))\")\n"
                "con.execute(\"insert into raw_market.raw_market.raw_bar values ('sh600000','stock','day','2026-05-16',12.34,12.5,12.0,12.45,9000,8800.5,'offline:raw:sh600000.day','source-run','raw-market-ledger-v1','raw-market-direct-day-v1','manifest')\")\n"
                "con.execute(\"insert into raw_market.raw_market.ingest_run values ('run','H:/tdx_offline_Data','full',now(),now(),'passed','manifest','source-run','raw-market-ledger-v1','raw-market-direct-day-v1')\")\n"
                "con.close()\n"
            )
            subprocess.run([sys.executable, "-c", seed], check=True)

            result = subprocess.run(
                [
                    sys.executable,
                    str(repo_root / "scripts" / "data_foundation" / "validate_raw_market_ledger.py"),
                    "--db",
                    str(db_path),
                    "--json",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "passed")
        self.assertEqual(payload["raw_bar_row_count"], 1)


if __name__ == "__main__":
    unittest.main()
