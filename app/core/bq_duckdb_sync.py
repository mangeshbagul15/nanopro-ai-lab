"""Sync Google BigQuery bronze tables into the local DuckDB analytical store.

Real data path: BigQuery (service-account creds) -> data/nanopro.duckdb.
Runs on demand via chat ("duckdb sync") or the /api/duckdb/sync endpoint.
Only activates when a real BigQuery client is available; otherwise reports
the mock fallback honestly.
"""

import os
import time
from typing import Any, Dict, List, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "data", "nanopro.duckdb")
SCHEMA = "nanopro_cbs_bronze"

# Core bronze tables mirrored into DuckDB (gold cache layer).
MIRROR_TABLES = ["CMG", "GAM", "HTD", "SOL", "SWIFT_MSG", "TAM_LAM", "UBO", "VCT"]


def _duckdb_connect(read_only: bool = False):
    import duckdb
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return duckdb.connect(DB_PATH, read_only=read_only)


def _bq_client():
    from app.core.live_catalog import _bigquery_client
    client, auth = _bigquery_client()
    return client, auth


def sync_bigquery_to_duckdb(tables: Optional[List[str]] = None, limit: int = 10000) -> Dict[str, Any]:
    """Mirror BigQuery bronze tables into DuckDB. Returns per-table stats."""
    started = time.time()
    targets = tables or MIRROR_TABLES
    client, auth = _bq_client()

    # Detect mock fallback — syncing mock rows would poison the store.
    if auth == "nanopro_live_catalog_resilience":
        return {
            "status": "skipped",
            "message": "Real BigQuery credentials not configured — mock catalog cannot be synced into DuckDB.",
            "auth": auth,
        }

    con = _duckdb_connect()
    synced: List[Dict[str, Any]] = []
    errors: List[Dict[str, Any]] = []
    try:
        project = getattr(client, "project", "nanopro-lakehouse-sandbox")
        for table in targets:
            fq = f"{project}.{SCHEMA}.{table}"
            try:
                job = client.query(f"SELECT * FROM `{fq}` LIMIT {limit}")
                rows = job.result()
                cols = [f.name for f in getattr(rows, "schema", []) or []]
                if not cols:
                    errors.append({"table": table, "error": "no columns"})
                    continue
                data = [dict(r.items()) for r in rows]
                # Recreate table deterministically
                con.execute(f"DROP TABLE IF EXISTS {SCHEMA}.{table}")
                con.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")
                col_defs = ", ".join(f'"{c}" VARCHAR' for c in cols)
                con.execute(f"CREATE TABLE {SCHEMA}.{table} ({col_defs})")
                if data:
                    placeholders = ", ".join("?" for _ in cols)
                    col_list = ", ".join(f'"{c}"' for c in cols)
                    con.executemany(
                        f"INSERT INTO {SCHEMA}.{table} ({col_list}) VALUES ({placeholders})",
                        [[None if row.get(c) is None else str(row.get(c)) for c in cols] for row in data],
                    )
                synced.append({"table": table, "rows": len(data), "columns": len(cols)})
            except Exception as exc:
                errors.append({"table": table, "error": str(exc)[:200]})
    finally:
        try:
            con.close()
        except Exception:
            pass

    duration_ms = round((time.time() - started) * 1000)
    return {
        "status": "success" if synced else "error",
        "auth": auth,
        "synced": synced,
        "errors": errors,
        "total_rows": sum(s["rows"] for s in synced),
        "duration_ms": duration_ms,
        "store": "data/nanopro.duckdb",
    }


def duckdb_status() -> Dict[str, Any]:
    """Live DuckDB store stats: tables, row counts, schemas."""
    if not os.path.exists(DB_PATH):
        return {"status": "empty", "tables": 0, "path": DB_PATH}
    try:
        con = _duckdb_connect(read_only=True)
        rows = con.execute(
            "SELECT table_schema, table_name FROM information_schema.tables "
            "WHERE table_schema NOT IN ('information_schema','pg_catalog') ORDER BY 1,2"
        ).fetchall()
        stats = []
        for sch, tbl in rows:
            try:
                cnt = con.execute(f'SELECT COUNT(*) FROM "{sch}"."{tbl}"').fetchone()[0]
            except Exception:
                cnt = 0
            stats.append({"schema": sch, "table": tbl, "rows": cnt})
        con.close()
        return {"status": "success", "tables": len(stats), "schemas": sorted({s["schema"] for s in stats}),
                "items": stats, "path": DB_PATH}
    except Exception as exc:
        return {"status": "error", "error": str(exc)[:200]}
