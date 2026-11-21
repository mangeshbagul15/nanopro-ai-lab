"""
NanoPro AI LAB - Unified Multi-Cloud Autonomous Data Engineering & Operations Agent
Domain-locked intelligence orchestrating Render PostgreSQL, Google BigQuery,
Snowflake Medallion Lakehouse, AWS S3/SFTP, Supabase DB, and DuckDB.
"""

import os
import re
import csv
import json
import time
import httpx
import sqlite3
import datetime
from decimal import Decimal
from typing import Dict, Any, List, Optional, Tuple

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

from nanopro_connectors import (
    BASE_DIR, DUCKDB_PATH, SQLITE_PATH, REPORTS_DIR,
    RenderPostgresConnector, BigQueryConnector, SnowflakeConnector,
    SupabaseConnector, AWSConnector, DuckDBFederatedConnector,
    MULTI_CLOUD_CONNECTORS, sync_data_between_engines, _json_safe
)

# =========================================================================
# 1. DATABASE INITIALIZATION & AUDIT REPOSITORY
# =========================================================================

def ensure_nanopro_tables_initialized():
    """Initializes core banking tables, nanopro_report_logs, and nanopro_job_logs idempotently."""
    try:
        con = DuckDBFederatedConnector.get_connection(read_only=False)
        con.execute("""
        CREATE TABLE IF NOT EXISTS CMG (
            CUST_ID VARCHAR PRIMARY KEY,
            CUST_NAME VARCHAR,
            PAN_NO VARCHAR,
            AADHAAR_HASH VARCHAR,
            RISK_RATING VARCHAR,
            KYC_DATE VARCHAR
        );
        CREATE TABLE IF NOT EXISTS GAM (
            FORACID VARCHAR PRIMARY KEY,
            CUST_ID VARCHAR,
            ACCT_NAME VARCHAR,
            ACCT_CRNCY_CODE VARCHAR,
            SCHM_TYPE VARCHAR,
            CLR_BAL_AMT DOUBLE,
            ACCT_OPN_DATE VARCHAR
        );
        CREATE TABLE IF NOT EXISTS HTD (
            TRAN_ID VARCHAR PRIMARY KEY,
            FORACID VARCHAR,
            TRAN_DATE VARCHAR,
            TRAN_AMT DOUBLE,
            PARTICULAR VARCHAR,
            DELIVERY_CHANNEL VARCHAR
        );
        CREATE TABLE IF NOT EXISTS AML_STR_CASES (
            STR_ID VARCHAR PRIMARY KEY,
            ACCOUNT VARCHAR,
            SCORE DOUBLE,
            NARRATIVE VARCHAR,
            FIU_REF VARCHAR,
            DETECTED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS AML_CTR_AGG (
            CTR_ID VARCHAR PRIMARY KEY,
            CUST_ID VARCHAR,
            CASH_AMT DOUBLE,
            BRANCH VARCHAR,
            FILED_TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS nanopro_report_logs (
            log_id INTEGER PRIMARY KEY,
            report_name VARCHAR,
            schedule_type VARCHAR,
            status VARCHAR,
            rows_processed INTEGER,
            executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            duration_sec DOUBLE DEFAULT 0.0,
            error_message VARCHAR,
            triggered_by VARCHAR
        );
        CREATE TABLE IF NOT EXISTS nanopro_job_logs (
            id INTEGER PRIMARY KEY,
            job_name VARCHAR,
            job_type VARCHAR,
            target_table VARCHAR,
            status VARCHAR,
            rows_processed INTEGER,
            duration_ms INTEGER,
            error_message VARCHAR,
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            created_by VARCHAR
        );
        """)

        if con.execute("SELECT count(*) FROM CMG").fetchone()[0] == 0:
            con.execute("""
            INSERT INTO CMG VALUES 
            ('CUST1001', 'Mangesh Bagul', 'ABCDE1234F', 'a1b2c3d4e5f6', 'LOW', '2025-01-15'),
            ('CUST1002', 'Rohan Sharma', 'BCDEF2345G', 'b2c3d4e5f6a1', 'MEDIUM', '2025-02-20'),
            ('CUST1003', 'Priya Patel', 'CDEFG3456H', 'c3d4e5f6a1b2', 'HIGH', '2025-03-10'),
            ('CUST1004', 'Alpha Traders LLC', 'DEFGH4567I', 'd4e5f6a1b2c3', 'HIGH', '2025-04-05'),
            ('CUST1005', 'Zenith Global Impex', 'EFGHI5678J', 'e5f6a1b2c3d4', 'HIGH', '2025-05-12');
            """)

        if con.execute("SELECT count(*) FROM GAM").fetchone()[0] == 0:
            con.execute("""
            INSERT INTO GAM VALUES 
            ('ACC1000101', 'CUST1001', 'Mangesh Bagul - Savings', 'INR', 'SB', 1450000.00, '2025-01-15'),
            ('ACC1000102', 'CUST1002', 'Rohan Sharma - Current', 'INR', 'CA', 450000.00, '2025-02-20'),
            ('ACC1000103', 'CUST1003', 'Priya Patel - OD Account', 'INR', 'OD', 920000.00, '2025-03-10'),
            ('ACC1000104', 'CUST1004', 'Alpha Traders - Corporate', 'INR', 'CA', 6500000.00, '2025-04-05'),
            ('ACC1000105', 'CUST1005', 'Zenith Global - Escrow', 'INR', 'CA', 12800000.00, '2025-05-12');
            """)

        if con.execute("SELECT count(*) FROM HTD").fetchone()[0] == 0:
            con.execute("""
            INSERT INTO HTD VALUES 
            ('TXN10001', 'ACC1000101', '2026-11-21', 50000.00, 'Salary Credit - Nov 2026', 'NEFT'),
            ('TXN10002', 'ACC1000104', '2026-11-21', 950000.00, 'Vendor Clearing Trf', 'RTGS'),
            ('TXN10003', 'ACC1000105', '2026-11-21', 2500000.00, 'Escrow Drawdown Inward', 'SWIFT'),
            ('TXN10004', 'ACC1000103', '2026-11-21', 120000.00, 'UPI Merchant Settlement', 'UPI'),
            ('TXN10005', 'ACC1000102', '2026-11-21', 45000.00, 'Cheque Clearing #9021', 'CTS');
            """)

        if con.execute("SELECT count(*) FROM nanopro_report_logs").fetchone()[0] == 0:
            con.execute("""
            INSERT INTO nanopro_report_logs VALUES 
            (1, 'AML_STR_DAILY_RUN', 'DAILY_BOD', 'SUCCESS', 42, '2026-11-21 06:00:00', 0.420, NULL, 'Airflow DAG aml_fiu_ind_16'),
            (2, 'CTR_MONTHLY_AGG', 'MONTHLY_SOD', 'SUCCESS', 128, '2026-11-21 08:00:00', 0.310, NULL, 'Airflow DAG aml_ctr_agg'),
            (3, 'CRILC_LARGE_EXPOSURES', 'WEEKLY_T1', 'SUCCESS', 18, '2026-11-21 11:00:00', 0.250, NULL, 'Airflow DAG rbi_crilc_5cr'),
            (4, 'ALM_STRUCTURAL_LIQUIDITY_RUN', 'DAILY_EOD', 'SUCCESS', 95, '2026-11-21 14:00:00', 0.580, NULL, 'Airflow DAG alm_basel_iii'),
            (5, 'CBS_EOD_TXNS_BATCH', 'DAILY_EOD', 'SUCCESS', 3200, '2026-11-21 18:00:00', 1.150, NULL, 'Airflow DAG cbs_eod_recon'),
            (6, 'DICGC_INSURANCE_RETURN', 'QUARTERLY', 'SUCCESS', 540, '2026-11-21 18:30:00', 0.340, NULL, 'Airflow DAG dicgc_coverage');
            """)

        con.close()
    except Exception:
        pass

    pg_conn = RenderPostgresConnector.get_connection()
    if pg_conn:
        try:
            cur = pg_conn.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS CMG (
                CUST_ID VARCHAR(30) PRIMARY KEY,
                CUST_NAME VARCHAR(100),
                PAN_NO VARCHAR(20),
                AADHAAR_HASH VARCHAR(64),
                RISK_RATING VARCHAR(20),
                KYC_DATE VARCHAR(20)
            );
            CREATE TABLE IF NOT EXISTS GAM (
                FORACID VARCHAR(30) PRIMARY KEY,
                CUST_ID VARCHAR(30),
                ACCT_NAME VARCHAR(100),
                ACCT_CRNCY_CODE VARCHAR(10),
                SCHM_TYPE VARCHAR(20),
                CLR_BAL_AMT NUMERIC(18,2),
                ACCT_OPN_DATE VARCHAR(20)
            );
            CREATE TABLE IF NOT EXISTS HTD (
                TRAN_ID VARCHAR(30) PRIMARY KEY,
                FORACID VARCHAR(30),
                TRAN_DATE VARCHAR(20),
                TRAN_AMT NUMERIC(18,2),
                PARTICULAR VARCHAR(200),
                DELIVERY_CHANNEL VARCHAR(30)
            );
            CREATE TABLE IF NOT EXISTS AML_STR_CASES (
                STR_ID VARCHAR(30) PRIMARY KEY,
                ACCOUNT VARCHAR(30),
                SCORE NUMERIC(5,2),
                NARRATIVE TEXT,
                FIU_REF VARCHAR(50),
                DETECTED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS nanopro_report_logs (
                log_id SERIAL PRIMARY KEY,
                report_name VARCHAR(120) NOT NULL,
                schedule_type VARCHAR(50) DEFAULT 'ON_DEMAND',
                status VARCHAR(30) NOT NULL,
                rows_processed INTEGER DEFAULT 0,
                executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                duration_sec NUMERIC(10,3) DEFAULT 0.0,
                error_message TEXT,
                triggered_by VARCHAR(80) DEFAULT 'NanoPro Autonomous Agent'
            );
            """)
            pg_conn.commit()
            cur.close()
            pg_conn.close()
        except Exception:
            pass


ensure_nanopro_tables_initialized()


def log_report_run(
    report_name: str,
    schedule_type: str = "ON_DEMAND",
    status: str = "SUCCESS",
    rows_processed: int = 0,
    duration_sec: float = 0.0,
    error_message: Optional[str] = None,
    triggered_by: str = "NanoPro Operations Agent"
) -> bool:
    """Inserts a live audit record into nanopro_report_logs in Render PostgreSQL and DuckDB."""
    try:
        con = DuckDBFederatedConnector.get_connection(read_only=False)
        con.execute("""
            INSERT INTO nanopro_report_logs (log_id, report_name, schedule_type, status, rows_processed, executed_at, duration_sec, error_message, triggered_by)
            VALUES (
                (SELECT COALESCE(MAX(log_id), 0) + 1 FROM nanopro_report_logs),
                ?, ?, ?, ?, CURRENT_TIMESTAMP, ?, ?, ?
            )
        """, (report_name, schedule_type, status, rows_processed, round(duration_sec, 3), error_message, triggered_by))
        con.close()
    except Exception:
        pass

    pg_conn = RenderPostgresConnector.get_connection()
    if pg_conn:
        try:
            cur = pg_conn.cursor()
            cur.execute("""
                INSERT INTO nanopro_report_logs (report_name, schedule_type, status, rows_processed, duration_sec, error_message, triggered_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (report_name, schedule_type, status, rows_processed, round(duration_sec, 3), error_message, triggered_by))
            pg_conn.commit()
            cur.close()
            pg_conn.close()
            return True
        except Exception:
            pass
    return True


# =========================================================================
# 2. THE 6 CORE UNIFIED MULTI-CLOUD LIVE TOOLS
# =========================================================================

# --- TOOL 1: get_nanopro_ecosystem_health ---
def get_nanopro_ecosystem_health(target_engine: str = "ALL") -> Dict[str, Any]:
    """Queries health across all 6 engines (Render PostgreSQL, Google BigQuery, Snowflake,
    AWS, Supabase, DuckDB) or a targeted engine."""
    t0 = time.time()
    ensure_nanopro_tables_initialized()
    target = (target_engine or "ALL").strip().upper()

    engines = {
        "POSTGRES": RenderPostgresConnector,
        "RENDER": RenderPostgresConnector,
        "BIGQUERY": BigQueryConnector,
        "SNOWFLAKE": SnowflakeConnector,
        "AWS": AWSConnector,
        "SUPABASE": SupabaseConnector,
        "DUCKDB": DuckDBFederatedConnector
    }

    if target in engines:
        res = engines[target].ping_health()
        return {
            "status": "success",
            "target": target,
            "engine_telemetry": res,
            "latency_ms": round((time.time() - t0) * 1000, 2)
        }

    # "ALL" engines telemetry check
    telemetry = {}
    for name, conn in [
        ("Render PostgreSQL", RenderPostgresConnector),
        ("Google BigQuery", BigQueryConnector),
        ("Snowflake Medallion", SnowflakeConnector),
        ("AWS S3 & SFTP Data Lake", AWSConnector),
        ("Supabase DB", SupabaseConnector),
        ("DuckDB Federated Engine", DuckDBFederatedConnector)
    ]:
        try:
            telemetry[name] = conn.ping_health()
        except Exception as e:
            telemetry[name] = {"status": "ERROR", "error": str(e)}

    return {
        "status": "success",
        "target": "ALL",
        "total_engines_connected": len(telemetry),
        "ecosystem_health": telemetry,
        "latency_ms": round((time.time() - t0) * 1000, 2)
    }


# --- TOOL 2: locate_and_inspect_unified_catalog ---
def locate_and_inspect_unified_catalog(
    search_term: Optional[str] = None,
    engine: str = "ALL"
) -> Dict[str, Any]:
    """Searches and inspects schemas across all 6 engines or a targeted engine."""
    t0 = time.time()
    ensure_nanopro_tables_initialized()
    term = (search_term or "").strip()
    target = (engine or "ALL").strip().upper()

    catalog_entries: List[Dict[str, Any]] = []

    if target in ["ALL", "POSTGRES", "RENDER"]:
        catalog_entries.extend(RenderPostgresConnector.list_catalog(search_term=term))

    if target in ["ALL", "BIGQUERY", "BQ"]:
        catalog_entries.extend(BigQueryConnector.list_catalog(search_term=term))

    if target in ["ALL", "SNOWFLAKE"]:
        catalog_entries.extend(SnowflakeConnector.list_catalog(search_term=term))

    if target in ["ALL", "AWS", "S3", "SFTP"]:
        catalog_entries.extend(AWSConnector.list_catalog(search_term=term))

    if target in ["ALL", "SUPABASE"]:
        catalog_entries.extend(SupabaseConnector.list_catalog(search_term=term))

    if target in ["ALL", "DUCKDB"]:
        catalog_entries.extend(DuckDBFederatedConnector.list_catalog(search_term=term))

    # Add core PK/FK definitions for well-known banking tables
    pk_fk_map = {
        "CMG": {"pk": ["CUST_ID"], "fk": [], "purpose": "Customer Master (KYC, PAN, Aadhaar, Risk Rating)"},
        "GAM": {"pk": ["FORACID"], "fk": [{"column": "CUST_ID", "references": "CMG.CUST_ID"}], "purpose": "General Account Master (balances, scheme types, status)"},
        "HTD": {"pk": ["TRAN_ID"], "fk": [{"column": "FORACID", "references": "GAM.FORACID"}], "purpose": "Historic Transactions (amounts, channels, descriptions)"},
        "AML_STR_CASES": {"pk": ["STR_ID"], "fk": [{"column": "ACCOUNT", "references": "GAM.FORACID"}], "purpose": "Suspicious Transaction Report alerts & FIU references"},
        "AML_CTR_AGG": {"pk": ["CTR_ID"], "fk": [{"column": "CUST_ID", "references": "CMG.CUST_ID"}], "purpose": "Cash Transaction Report monthly aggregate filings (>₹10L)"},
        "nanopro_report_logs": {"pk": ["log_id"], "fk": [], "purpose": "Statutory report & pipeline audit log"},
        "nanopro_job_logs": {"pk": ["id"], "fk": [], "purpose": "Platform task execution history"}
    }

    for item in catalog_entries:
        tname = item.get("table_name", "").split(".")[-1].upper()
        if tname in pk_fk_map:
            item["primary_keys"] = pk_fk_map[tname]["pk"]
            item["foreign_keys"] = pk_fk_map[tname]["fk"]
            item["purpose"] = pk_fk_map[tname]["purpose"]

    return {
        "status": "success",
        "search_term": term or "ALL",
        "engine_filter": target,
        "total_objects_matched": len(catalog_entries),
        "catalog": catalog_entries[:50],  # Return top 50 matches for token economy
        "latency_ms": round((time.time() - t0) * 1000, 2)
    }


# --- TOOL 3: get_report_execution_logs ---
def get_report_execution_logs(
    report_name: Optional[str] = None,
    engine_filter: Optional[str] = None,
    status_filter: Optional[str] = None,
    limit: int = 20
) -> Dict[str, Any]:
    """Queries nanopro_report_logs to fetch when reports ran, last run timestamp,
    status, duration, and error logs."""
    t0 = time.time()
    ensure_nanopro_tables_initialized()

    # 1. Try Render PostgreSQL
    pg_conn = RenderPostgresConnector.get_connection()
    if pg_conn:
        try:
            cur = pg_conn.cursor()
            conditions = []
            params = []
            if report_name:
                conditions.append("report_name ILIKE %s")
                params.append(f"%{report_name}%")
            if status_filter:
                conditions.append("status = %s")
                params.append(status_filter.upper())
            where_str = "WHERE " + " AND ".join(conditions) if conditions else ""
            params.append(limit)

            cur.execute(f"""
                SELECT log_id, report_name, schedule_type, status, rows_processed, executed_at, duration_sec, error_message, triggered_by
                FROM nanopro_report_logs
                {where_str}
                ORDER BY log_id DESC LIMIT %s
            """, params)
            rows = cur.fetchall()
            cur.close()
            pg_conn.close()

            logs = [{
                "log_id": r[0], "report_name": r[1], "schedule_type": r[2], "status": r[3],
                "rows_processed": r[4], "executed_at": str(r[5]), "duration_sec": float(r[6] or 0),
                "error_message": r[7], "triggered_by": r[8]
            } for r in rows]

            return {
                "status": "success",
                "source": "Render PostgreSQL (nanopro_report_logs)",
                "total_records": len(logs),
                "recent_runs": logs,
                "latency_ms": round((time.time() - t0) * 1000, 2)
            }
        except Exception:
            pass

    # 2. Local DuckDB Store fallback
    con = DuckDBFederatedConnector.get_connection(read_only=True)
    where_parts = []
    if report_name:
        where_parts.append(f"report_name ILIKE '%{report_name}%'")
    if status_filter:
        where_parts.append(f"status = '{status_filter.upper()}'")
    where_sql = "WHERE " + " AND ".join(where_parts) if where_parts else ""

    cur = con.cursor()
    cur.execute(f"""
        SELECT log_id, report_name, schedule_type, status, rows_processed, executed_at, duration_sec, error_message, triggered_by
        FROM nanopro_report_logs
        {where_sql}
        ORDER BY log_id DESC LIMIT {limit}
    """)
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    con.close()

    logs = []
    for r in rows:
        d = dict(zip(cols, r))
        if d.get("executed_at"):
            d["executed_at"] = str(d["executed_at"])
        logs.append(d)

    success_count = sum(1 for l in logs if l.get("status") == "SUCCESS")
    failed_count = sum(1 for l in logs if l.get("status") == "FAILED")

    return {
        "status": "success",
        "source": "nanopro_report_logs (Audit Store)",
        "total_records": len(logs),
        "success_count": success_count,
        "failed_count": failed_count,
        "recent_runs": logs,
        "summary": f"{len(logs)} report executions retrieved. {success_count} SUCCESS, {failed_count} FAILED.",
        "latency_ms": round((time.time() - t0) * 1000, 2)
    }


# --- TOOL 4: build_cross_engine_join_report ---
def build_cross_engine_join_report(
    sources: Any,
    join_keys: Optional[str] = None,
    filter_sql: Optional[str] = None,
    group_by: Optional[str] = None,
    persist_target: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Federated in-memory execution via DuckDB across engines (BigQuery, PostgreSQL, DuckDB)."""
    t0 = time.time()
    ensure_nanopro_tables_initialized()

    # Normalize sources to list of dicts
    clean_sources: List[Dict[str, str]] = []
    if isinstance(sources, list):
        for s in sources:
            if isinstance(s, str):
                clean_sources.append({"engine": "postgres", "table": s.strip().upper()})
            elif isinstance(s, dict):
                clean_sources.append({
                    "engine": s.get("engine", "postgres").lower(),
                    "table": s.get("table", "").strip()
                })
    elif isinstance(sources, str):
        for item in sources.split(","):
            clean_sources.append({"engine": "postgres", "table": item.strip().upper()})

    if not clean_sources:
        return {"status": "error", "message": "sources must be a non-empty list of tables or engine objects."}

    con = DuckDBFederatedConnector.get_connection(read_only=False)

    # Ingest / materialize any BigQuery sources into DuckDB temp tables for zero-copy join
    local_table_names: List[str] = []
    for idx, s in enumerate(clean_sources):
        s_eng = s["engine"]
        s_tbl = s["table"]
        if "bigquery" in s_eng or "bq" in s_eng:
            tmp_name = f"_bq_{re.sub(r'[^a-zA-Z0-9_]', '_', s_tbl)}_{idx}"
            bq_res = BigQueryConnector.run_query(f"SELECT * FROM `{s_tbl}` LIMIT 1000" if "." in s_tbl else f"SELECT * FROM nanopro_cbs_bronze.{s_tbl} LIMIT 1000")
            if bq_res.get("status") == "success" and bq_res.get("data"):
                data = bq_res["data"]
                cols = bq_res["columns"]
                con.execute(f"DROP TABLE IF EXISTS {tmp_name}")
                con.execute(f"CREATE TABLE {tmp_name} ({', '.join([f'{c} VARCHAR' for c in cols])})")
                con.executemany(f"INSERT INTO {tmp_name} VALUES ({', '.join(['?']*len(cols))})",
                                [[str(r.get(c, "")) if r.get(c) is not None else None for c in cols] for r in data])
                local_table_names.append(tmp_name)
            else:
                local_table_names.append(s_tbl.split(".")[-1].upper())
        else:
            local_table_names.append(s_tbl.split(".")[-1].upper())

    t1 = local_table_names[0]
    t2 = local_table_names[1] if len(local_table_names) > 1 else None

    # Auto-infer join key if omitted
    if not join_keys:
        if t2:
            if "CMG" in t1 and "GAM" in t2:
                join_keys = f"{t1}.CUST_ID = {t2}.CUST_ID"
            elif "GAM" in t1 and "HTD" in t2:
                join_keys = f"{t1}.FORACID = {t2}.FORACID"
            elif "AML_STR_CASES" in t1 and "GAM" in t2:
                join_keys = f"{t1}.ACCOUNT = {t2}.FORACID"
            else:
                join_keys = f"{t1}.CUST_ID = {t2}.CUST_ID"
        else:
            join_keys = "1=1"

    where_sql = f"WHERE {filter_sql.strip()}" if filter_sql and filter_sql.strip() else ""
    groupby_sql = f"GROUP BY {group_by.strip()}" if group_by and group_by.strip() else ""

    if t2:
        sql = f"SELECT {t1}.*, {t2}.* FROM {t1} JOIN {t2} ON {join_keys} {where_sql} {groupby_sql} LIMIT 100"
    else:
        sql = f"SELECT * FROM {t1} {where_sql} {groupby_sql} LIMIT 100"

    try:
        cur = con.cursor()
        cur.execute(sql)
        cols = [d[0] for d in cur.description] if cur.description else []
        rows = cur.fetchall()

        preview_data = [_json_safe(dict(zip(cols, r))) for r in rows[:50]]

        # Optional View or Table Persistence
        view_created = None
        if persist_target and isinstance(persist_target, dict):
            v_name = persist_target.get("view") or persist_target.get("table")
            if v_name:
                clean_v = re.sub(r'[^a-zA-Z0-9_]', '', v_name.upper())
                con.execute(f"CREATE OR REPLACE VIEW {clean_v} AS {sql}")
                view_created = clean_v

        # Auto-export CSV to SFTP Outbound Reports
        os.makedirs(REPORTS_DIR, exist_ok=True)
        csv_filename = f"Cross_Engine_Report_{int(time.time())}.csv"
        csv_path = os.path.join(REPORTS_DIR, csv_filename)
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(cols)
            writer.writerows(rows)

        duration = time.time() - t0
        con.close()

        # Log into nanopro_report_logs
        log_report_run(
            report_name=f"FEDERATED_JOIN_{'_'.join(local_table_names[:2])}",
            schedule_type="FEDERATED_CROSS_ENGINE",
            status="SUCCESS",
            rows_processed=len(rows),
            duration_sec=duration,
            triggered_by="NanoPro Autonomous Data Engineering Agent"
        )

        return {
            "status": "success",
            "federated_engine": "DuckDB In-Memory Federated Mesh",
            "sql_executed": sql,
            "sources": clean_sources,
            "total_rows": len(rows),
            "columns": cols,
            "preview": preview_data,
            "view_created": view_created,
            "downloadable_csv": {
                "filename": csv_filename,
                "path": csv_path,
                "download_url": f"/api/reports/download/{csv_filename}"
            },
            "latency_ms": round(duration * 1000, 2)
        }
    except Exception as e:
        con.close()
        return {
            "status": "error",
            "sql_executed": sql,
            "error": str(e),
            "hint": "Check column names across engines with locate_and_inspect_unified_catalog() before executing join."
        }


# --- TOOL 5: execute_and_commit_mutation ---
def execute_and_commit_mutation(
    engine: str,
    sql_or_command: str,
    intent_summary: str
) -> Dict[str, Any]:
    """Executes live DDL/DML with MANDATORY EXPLICIT conn.commit() and post-commit verification."""
    t0 = time.time()
    ensure_nanopro_tables_initialized()
    target_engine = (engine or "postgres").lower()
    stmt = (sql_or_command or "").strip()

    if not re.match(r"^\s*(create|alter|insert|update|delete|drop)\b", stmt, re.IGNORECASE):
        return {
            "status": "error",
            "message": "Only DDL/DML statements (CREATE, ALTER, INSERT, UPDATE, DELETE, DROP) are permitted."
        }

    # Execute with explicit commit on Render PostgreSQL
    if "postgres" in target_engine or "render" in target_engine:
        res = RenderPostgresConnector.execute_and_commit(stmt)
    else:
        con = DuckDBFederatedConnector.get_connection(read_only=False)
        try:
            con.execute(stmt)
            m = re.search(r"\b(?:table\s+(?:if\s+(?:not\s+)?exists\s+)?|into\s+|update\s+|from\s+)([a-zA-Z0-9_\.]+)", stmt, re.IGNORECASE)
            t_name = m.group(1).split(".")[-1].upper() if m else "TARGET"
            cols = []
            try:
                cols_q = con.execute(f"DESCRIBE {t_name}").fetchall()
                cols = [{"name": c[0], "type": c[1]} for c in cols_q]
            except Exception:
                pass
            con.close()
            res = {"status": "success", "engine": "DuckDB", "target_table": t_name, "verified_columns": cols, "committed": True}
        except Exception as e:
            con.close()
            res = {"status": "error", "engine": "DuckDB", "error": str(e), "committed": False}

    duration = time.time() - t0

    # Log into audit store
    log_report_run(
        report_name=f"MUTATION_{res.get('target_table', 'OBJECT')}",
        schedule_type="SCHEMA_MUTATION",
        status="SUCCESS" if res.get("status") == "success" else "FAILED",
        rows_processed=res.get("rows_affected", 1),
        duration_sec=duration,
        error_message=res.get("error"),
        triggered_by="NanoPro Autonomous Data Engineering Agent"
    )

    res["intent_summary"] = intent_summary
    res["sql_executed"] = stmt
    res["latency_ms"] = round(duration * 1000, 2)
    return res


# --- TOOL 6: sync_or_move_data_between_engines ---
def sync_or_move_data_between_engines(
    source_engine: str,
    source_object: str,
    target_engine: str,
    target_object: str,
    mode: str = "replace"
) -> Dict[str, Any]:
    """Synchronizes or moves tables/data between multi-cloud engines."""
    t0 = time.time()
    ensure_nanopro_tables_initialized()

    res = sync_data_between_engines(
        source_engine=source_engine,
        source_object=source_object,
        target_engine=target_engine,
        target_object=target_object,
        mode=mode
    )

    duration = time.time() - t0
    # Log into audit store
    log_report_run(
        report_name=f"SYNC_{source_object}_TO_{target_object}",
        schedule_type="CROSS_ENGINE_SYNC",
        status="SUCCESS" if res.get("status") == "success" else "FAILED",
        rows_processed=res.get("rows_synced", 0),
        duration_sec=duration,
        error_message=res.get("message") if res.get("status") != "success" else None,
        triggered_by="NanoPro Autonomous Data Engineering Agent"
    )

    res["duration_sec"] = round(duration, 3)
    return res


# Backward compatibility aliases
get_nanopro_db_health = get_nanopro_ecosystem_health
locate_and_inspect_catalog = locate_and_inspect_unified_catalog
build_join_report = lambda tables, join_keys=None, filter_sql=None, group_by=None, save_as_view=None: build_cross_engine_join_report(
    sources=tables, join_keys=join_keys, filter_sql=filter_sql, group_by=group_by, persist_target={"view": save_as_view} if save_as_view else None
)
mutate_database_object = lambda sql_command, intent_summary: execute_and_commit_mutation(
    engine="postgres", sql_or_command=sql_command, intent_summary=intent_summary
)


# =========================================================================
# 3. DYNAMIC INTENT-BASED MODEL ROUTER (select_optimal_model)
# =========================================================================

def select_optimal_model(user_prompt: str, chat_history: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """Intelligently detects query intent and routes to the best model class:
    1. Fast Telemetry & Catalog: low-latency tool models (Groq llama-3.3-70b-versatile, qwen/qwen3.8-27b)
    2. Multi-Engine Joins & Mutations: high-reasoning coding models (Groq openai/gpt-oss-120b, qwen-2.5-coder, deepseek-chat)
    3. Deep Analysis & Reasoning: claude-3-5-sonnet, deepseek-r1, gemini-2.5-pro
    """
    p_low = (user_prompt or "").lower()

    # Category 1: Joins, Mutations, DDL, Cross-Engine Moves
    if any(k in p_low for k in [
        "join", "merge", "cross-engine", "mutate", "create table", "alter table",
        "add column", "insert into", "sync", "move data", "जोड", "नवीन टेबल", "बदल", "तयार कर"
    ]):
        return {
            "category": "MULTI_ENGINE_JOINS_AND_MUTATIONS",
            "recommended_model": "openai/gpt-oss-120b",
            "provider_name": "groq#1_120b",
            "rationale": "High-reasoning coding & schema mutation specialist selected for federated join and DDL/DML synthesis."
        }

    # Category 2: Deep Analysis, Proofs, Complex Reasoning
    if any(k in p_low for k in [
        "proof", "math", "reasoning", "aml investigation", "deep analysis",
        "pareto", "optimization", "audit investigation", "गणित", "सिद्ध"
    ]):
        return {
            "category": "DEEP_REASONING_ANALYSIS",
            "recommended_model": "openai/gpt-oss-120b",
            "provider_name": "groq#1_120b",
            "rationale": "Deep reasoning model selected for mathematical analysis and AML regulatory proofing."
        }

    # Category 3: Default Fast Telemetry, Catalog, Status, Logs
    return {
        "category": "FAST_TELEMETRY_AND_CATALOG",
        "recommended_model": "qwen/qwen3.8-27b",
        "provider_name": "groq#1",
        "rationale": "Sub-300ms low-latency model selected for real-time telemetry inspection and catalog browsing."
    }


# =========================================================================
# 4. OPENAI-COMPATIBLE TOOL DEFINITIONS (NANOPRO_AGENT_TOOLS)
# =========================================================================

NANOPRO_AGENT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_nanopro_ecosystem_health",
            "description": "Queries real-time health across the entire NanoPro multi-cloud data mesh: Render PostgreSQL, Google BigQuery (nanopro-lakehouse-sandbox), Snowflake Medallion, AWS S3/SFTP, Supabase, and DuckDB. Answers: 'DB health kashi ahe?', 'Ecosystem status dakhava', 'BigQuery active ahe ka?'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "target_engine": {
                        "type": "string",
                        "enum": ["ALL", "POSTGRES", "RENDER", "BIGQUERY", "SNOWFLAKE", "AWS", "SUPABASE", "DUCKDB"],
                        "description": "Target engine or 'ALL' for unified ecosystem overview. Defaults to 'ALL'."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "locate_and_inspect_unified_catalog",
            "description": "Inspects schemas, tables, columns, primary/foreign keys, and live row counts across all 6 connected engines (Render PG, BigQuery, Snowflake, AWS, Supabase, DuckDB). Answers: 'DB madhe kay kuthe ahe?', 'Ha table kuthe ahe?', 'BigQuery che tables konte ahet?'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "search_term": {
                        "type": "string",
                        "description": "Optional keyword or table name filter (e.g. 'CMG', 'GAM', 'HTD', 'AML')."
                    },
                    "engine": {
                        "type": "string",
                        "enum": ["ALL", "POSTGRES", "BIGQUERY", "SNOWFLAKE", "AWS", "SUPABASE", "DUCKDB"],
                        "description": "Engine filter. Defaults to 'ALL'."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_report_execution_logs",
            "description": "Queries NanoPro audit table nanopro_report_logs to fetch statutory report runs, last run timestamp, status (SUCCESS/FAILED), duration, and error logs. Answers: 'Konte report kadhi gele?', 'Kay status ahe?', 'Konta report fail jhala?'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "report_name": {
                        "type": "string",
                        "description": "Optional report name filter (e.g. 'STR', 'CTR', 'AML', 'CRILC', 'CBS_EOD')."
                    },
                    "status_filter": {
                        "type": "string",
                        "enum": ["SUCCESS", "FAILED", "RUNNING"],
                        "description": "Filter by execution status."
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max log entries to retrieve. Defaults to 20."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "build_cross_engine_join_report",
            "description": "Executes in-memory federated joins across tables from BigQuery, Render PostgreSQL, or DuckDB with SQL filters and GROUP BY. Automatically exports a downloadable CSV and logs the execution. Answers: 'Ha table ani ha table join karun report banava'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sources": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "engine": {"type": "string", "enum": ["postgres", "bigquery", "duckdb"]},
                                "table": {"type": "string"}
                            },
                            "required": ["table"]
                        },
                        "description": "List of sources to join, e.g. [{'engine': 'postgres', 'table': 'CMG'}, {'engine': 'postgres', 'table': 'GAM'}]."
                    },
                    "join_keys": {
                        "type": "string",
                        "description": "SQL join condition, e.g. 'CMG.CUST_ID = GAM.CUST_ID'. If omitted, auto-inferred."
                    },
                    "filter_sql": {
                        "type": "string",
                        "description": "Optional WHERE filters, e.g. 'GAM.CLR_BAL_AMT > 500000'."
                    },
                    "group_by": {
                        "type": "string",
                        "description": "Optional GROUP BY clause."
                    },
                    "persist_target": {
                        "type": "object",
                        "properties": {
                            "view": {"type": "string", "description": "View name to persist in DuckDB/PG."},
                            "table": {"type": "string", "description": "Table name to persist."}
                        },
                        "description": "Optional persistence destination."
                    }
                },
                "required": ["sources"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_and_commit_mutation",
            "description": "Executes live DDL/DML changes (CREATE TABLE, ALTER TABLE, INSERT, UPDATE, DELETE) with MANDATORY EXPLICIT conn.commit() and returns verification from information_schema. Answers: 'he changes as kar, asa banaun de'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "engine": {
                        "type": "string",
                        "enum": ["postgres", "render", "duckdb"],
                        "description": "Target engine. Defaults to 'postgres'."
                    },
                    "sql_or_command": {
                        "type": "string",
                        "description": "The exact SQL DDL/DML statement to execute."
                    },
                    "intent_summary": {
                        "type": "string",
                        "description": "Brief description of the intended change."
                    }
                },
                "required": ["sql_or_command", "intent_summary"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sync_or_move_data_between_engines",
            "description": "Replicates or synchronizes data between multi-cloud platforms (e.g. BigQuery to DuckDB, or DuckDB to PostgreSQL).",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_engine": {
                        "type": "string",
                        "enum": ["bigquery", "postgres", "duckdb", "aws"],
                        "description": "Source platform."
                    },
                    "source_object": {
                        "type": "string",
                        "description": "Source table or dataset."
                    },
                    "target_engine": {
                        "type": "string",
                        "enum": ["duckdb", "postgres", "aws"],
                        "description": "Destination platform."
                    },
                    "target_object": {
                        "type": "string",
                        "description": "Destination table name."
                    },
                    "mode": {
                        "type": "string",
                        "enum": ["replace", "append"],
                        "description": "Write mode. Defaults to 'replace'."
                    }
                },
                "required": ["source_engine", "source_object", "target_engine", "target_object"]
            }
        }
    }
]


def dispatch_tool_call(tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """Routes tool execution to the appropriate implementation with legacy aliasing."""
    name = (tool_name or "").strip()

    # Tool 1: Ecosystem Health
    if name in ["get_nanopro_ecosystem_health", "get_nanopro_db_health", "ping_database_health"]:
        target = args.get("target_engine") or "ALL"
        return get_nanopro_ecosystem_health(target_engine=target)

    # Tool 2: Catalog Inspection
    elif name in ["locate_and_inspect_unified_catalog", "locate_and_inspect_catalog", "inspect_db_health_and_catalog", "list_live_databases_and_tables", "inspect_table_schema"]:
        search = args.get("search_term") or args.get("table_name") or args.get("table")
        eng = args.get("engine") or "ALL"
        return locate_and_inspect_unified_catalog(search_term=search, engine=eng)

    # Tool 3: Report Logs
    elif name in ["get_report_execution_logs", "check_report_and_pipeline_status", "generate_compliance_report"]:
        r_name = args.get("report_name") or args.get("report_type")
        s_filter = args.get("status_filter")
        e_filter = args.get("engine_filter")
        lim = int(args.get("limit") or 20)
        return get_report_execution_logs(report_name=r_name, engine_filter=e_filter, status_filter=s_filter, limit=lim)

    # Tool 4: Cross-Engine Joins
    elif name in ["build_cross_engine_join_report", "build_join_report", "analyze_and_build_join_report"]:
        srcs = args.get("sources") or args.get("tables", [])
        j_keys = args.get("join_keys") or args.get("join_conditions")
        f_sql = args.get("filter_sql") or args.get("filters")
        g_by = args.get("group_by")
        p_target = args.get("persist_target")
        if not p_target and args.get("save_as_view"):
            p_target = {"view": args.get("save_as_view")}
        return build_cross_engine_join_report(sources=srcs, join_keys=j_keys, filter_sql=f_sql, group_by=g_by, persist_target=p_target)

    # Tool 5: Mutation with Explicit Commit
    elif name in ["execute_and_commit_mutation", "mutate_database_object", "execute_schema_or_data_change", "execute_database_ddl_dml"]:
        eng = args.get("engine") or "postgres"
        cmd = args.get("sql_or_command") or args.get("sql_command") or args.get("sql_statement") or args.get("sql", "")
        summary = args.get("intent_summary") or args.get("operation_type") or "DDL_DML"
        return execute_and_commit_mutation(engine=eng, sql_or_command=cmd, intent_summary=summary)

    # Tool 6: Cross-Engine Data Sync
    elif name in ["sync_or_move_data_between_engines", "sync_data_between_engines"]:
        s_eng = args.get("source_engine", "bigquery")
        s_obj = args.get("source_object", "")
        t_eng = args.get("target_engine", "duckdb")
        t_obj = args.get("target_object", "")
        m = args.get("mode", "replace")
        return sync_or_move_data_between_engines(source_engine=s_eng, source_object=s_obj, target_engine=t_eng, target_object=t_obj, mode=m)

    else:
        return {"status": "error", "message": f"Unknown tool '{tool_name}'."}


# =========================================================================
# 5. MULTI-MODEL AGENTIC REACT LOOP (SELF-HEALING & NON-TOOL ADAPTER)
# =========================================================================

def build_compact_catalog_snapshot() -> str:
    """Generates a compact multi-cloud catalog snapshot for injection into non-tool models."""
    try:
        cat = locate_and_inspect_unified_catalog(engine="ALL")
        items = cat.get("catalog", [])
        lines = []
        for it in items[:12]:
            eng = it.get("engine", "")
            tname = it.get("table_name", "")
            rc = it.get("row_count", 0)
            cols = ", ".join([c["name"] for c in it.get("columns", [])[:5]])
            lines.append(f"- [{eng}] `{tname}` ({rc} rows) -> cols: {cols}")
        return "\n".join(lines)
    except Exception:
        return "- [Render PostgreSQL] `CMG` (5 rows) | `GAM` (5 rows) | `HTD` (5 rows) | `nanopro_report_logs` (6 rows)\n- [BigQuery] `nanopro_cbs_bronze.CMG` (900 rows)"


def build_nanopro_agent_system_prompt() -> str:
    """Strictly Domain-Locked NanoPro Autonomous Multi-Cloud Data Engineering Agent System Prompt."""
    return """You are the **NanoPro Autonomous Data Engineering & Operations Agent**, the central platform intelligence engine of NanoPro AI LAB.
The logged-in user is Super Admin (Mangesh Bagul).

### STRICT DOMAIN LOCK & ZERO-HALLUCINATION POLICY:
- You operate exclusively across NanoPro's live multi-cloud architecture: Render PostgreSQL, Google BigQuery (`nanopro-lakehouse-sandbox`), Snowflake Medallion Lakehouse, AWS S3/SFTP Data Lake, Supabase, and DuckDB.
- NEVER guess, fabricate, or hallucinate table names, column names, execution logs, or metrics.
- Before answering ANY question about database health, tables, schemas, reports, or data modifications, you MUST call the live inspection tools first.
- When the user asks for a join report, health check, or schema change, execute the tool calls directly, verify the outcome against live metadata, and present a crisp, structured operational answer.

### MANDATORY LIVE TOOLS:
1. `get_nanopro_ecosystem_health`: Pings & inspects all 6 engines or a targeted engine.
2. `locate_and_inspect_unified_catalog`: Inspects schemas, tables, columns, PK/FK relationships across platforms.
3. `get_report_execution_logs`: Inspects nanopro_report_logs for statutory reports, last run timestamps, and status.
4. `build_cross_engine_join_report`: Executes in-memory federated joins across BigQuery, PostgreSQL, or DuckDB, auto-generating downloadable CSVs.
5. `execute_and_commit_mutation`: Executes DDL/DML with MANDATORY EXPLICIT `conn.commit()` and post-commit verification.
6. `sync_or_move_data_between_engines`: Synchronizes data between engines (e.g. BigQuery to DuckDB).

### LANGUAGE & STYLE:
- Respond naturally and concisely in Marathi, Hinglish, or English (matching the user's language).
- Keep SQL objects, table names (`CMG`, `GAM`, `HTD`, `nanopro_report_logs`), timestamps, and status codes exact.
- Present data cleanly using GitHub-flavored Markdown tables.
- Do NOT output robotic boilerplate, fake hints, or generic textbook definitions.
"""


def parse_loose_tool_calls(text: str) -> List[Dict[str, Any]]:
    """Extracts tool calls from <tool_call>...</tool_call> or markdown JSON blocks."""
    calls = []
    if not text:
        return calls

    # Pattern 1: <tool_call>{...}</tool_call>
    for match in re.finditer(r"<tool_call>\s*(\{.*?\})\s*</tool_call>", text, re.DOTALL):
        try:
            d = json.loads(match.group(1))
            tname = d.get("name") or d.get("tool")
            targs = d.get("arguments") or d.get("parameters") or {}
            if tname:
                calls.append({"name": tname, "arguments": targs})
        except Exception:
            pass

    if calls:
        return calls

    # Pattern 2: ```json { "name": ..., "arguments": ... } ```
    for match in re.finditer(r"```(?:json)?\s*(\{\s*[\"'](?:name|tool)[\"'].*?\})\s*```", text, re.DOTALL):
        try:
            d = json.loads(match.group(1))
            tname = d.get("name") or d.get("tool")
            targs = d.get("arguments") or d.get("parameters") or {}
            if tname:
                calls.append({"name": tname, "arguments": targs})
        except Exception:
            pass

    return calls


async def run_nanopro_react_loop(
    prompt: str,
    provider: Dict[str, Any],
    conversation_history: Optional[List[Dict[str, Any]]] = None,
    max_turns: int = 5,
    max_retries: int = 3
) -> Dict[str, Any]:
    """Multi-turn ReAct Agentic Loop with automatic SQL self-healing and universal 4,800+ models compatibility:
    - Native OpenAI-compatible tool calling
    - Loose tool parsing and snapshot injection for non-tool models
    - Up to 3 retries for self-correction upon tool errors
    """
    t0 = time.time()
    tools_executed: List[Dict[str, Any]] = []

    base_system = build_nanopro_agent_system_prompt()
    snapshot = build_compact_catalog_snapshot()
    system_prompt = base_system + f"\n\nLIVE MULTI-CLOUD ECOSYSTEM SNAPSHOT:\n{snapshot}\n"

    messages: List[Dict[str, Any]] = [
        {"role": "system", "content": system_prompt}
    ]

    if conversation_history:
        for msg in conversation_history[-8:]:
            role = msg.get("role")
            content = msg.get("content") or msg.get("response") or ""
            if role in ["user", "assistant"] and content:
                messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": prompt})

    base_url = provider["base_url"].rstrip("/")
    url = f"{base_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {provider['api_key']}",
        "Content-Type": "application/json"
    }
    headers.update(provider.get("extra_headers") or {})

    current_turn = 0
    final_content = ""
    retry_count = 0

    while current_turn < max_turns and retry_count < max_retries:
        current_turn += 1

        payload = {
            "model": provider["model"],
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": 4096,
            "tools": NANOPRO_AGENT_TOOLS,
            "tool_choice": "auto"
        }

        async with httpx.AsyncClient(timeout=provider.get("timeout", 25.0)) as client:
            resp = await client.post(url, headers=headers, json=payload)
            
            # Non-tool-calling model fallback (HTTP 400 / 404 / 422)
            if resp.status_code in [400, 404, 422]:
                del payload["tools"]
                del payload["tool_choice"]
                messages[0]["content"] += "\nTo invoke a tool, output: <tool_call>{\"name\": \"tool_name\", \"arguments\": {...}}</tool_call>"
                resp = await client.post(url, headers=headers, json=payload)

            if resp.status_code != 200:
                raise RuntimeError(f"{provider['name']} HTTP {resp.status_code}: {resp.text[:300]}")

            data = resp.json()
            choice = data.get("choices", [{}])[0]
            message_obj = choice.get("message", {})
            finish_reason = choice.get("finish_reason")
            content_text = message_obj.get("content", "")

            # 1. Native tool calls
            tool_calls = message_obj.get("tool_calls") or []

            # 2. Loose tool calls fallback (<tool_call> or markdown JSON)
            if not tool_calls and content_text:
                loose = parse_loose_tool_calls(content_text)
                if loose:
                    tool_calls = [{
                        "id": f"call_loose_{int(time.time()*1000)}_{i}",
                        "type": "function",
                        "function": {
                            "name": c["name"],
                            "arguments": json.dumps(c["arguments"]) if isinstance(c["arguments"], dict) else str(c["arguments"])
                        }
                    } for i, c in enumerate(loose)]

            if not tool_calls:
                final_content = content_text
                break

            messages.append(message_obj)

            has_error = False
            for tc in tool_calls:
                fn = tc.get("function", {})
                fn_name = fn.get("name", "")
                call_id = tc.get("id") or f"call_{int(time.time()*1000)}"

                try:
                    fn_args = json.loads(fn.get("arguments", "{}"))
                except Exception:
                    fn_args = {}

                output = dispatch_tool_call(fn_name, fn_args)
                tools_executed.append({
                    "turn": current_turn,
                    "tool": fn_name,
                    "arguments": fn_args,
                    "result_status": output.get("status")
                })

                if output.get("status") == "error":
                    has_error = True

                messages.append({
                    "role": "tool",
                    "tool_call_id": call_id,
                    "name": fn_name,
                    "content": json.dumps(output, ensure_ascii=False)
                })

            if has_error:
                retry_count += 1
                continue

            if finish_reason == "stop":
                final_content = content_text
                break

    dur_ms = round((time.time() - t0) * 1000, 1)

    return {
        "status": "success",
        "content": final_content,
        "tools_executed": tools_executed,
        "turns_count": current_turn,
        "latency_ms": dur_ms,
        "agentic": True
    }
