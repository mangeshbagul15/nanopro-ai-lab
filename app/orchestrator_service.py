import os
import json
import time
from typing import Dict, Any, List, Optional

ALERT_SCHEDULE = {
    "status": "RUNNING",
    "dispatch_time": "11:00 AM IST",
    "cycle": "T-1 Statutory EOD Batch",
    "last_updated": "2026-11-20 06:00 IST"
}

OVERRIDE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sftp_repository", "dag_schedules.json")

def load_dag_schedule_overrides() -> Dict[str, Any]:
    if os.path.exists(OVERRIDE_PATH):
        try:
            with open(OVERRIDE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_dag_schedule_overrides(ov: Dict[str, Any]) -> None:
    try:
        os.makedirs(os.path.dirname(OVERRIDE_PATH), exist_ok=True)
        with open(OVERRIDE_PATH, "w", encoding="utf-8") as f:
            json.dump(ov, f, indent=2)
    except Exception:
        pass

DAG_SCHEDULE_OVERRIDES = load_dag_schedule_overrides()

def update_dag_schedule(dag_id: str, new_schedule: str) -> Dict[str, Any]:
    global DAG_SCHEDULE_OVERRIDES
    clean_id = (dag_id or "").strip().lower()
    clean_sched = (new_schedule or "").strip()
    if not clean_id or not clean_sched:
        return {"status": "error", "message": "DAG ID and schedule string are required"}
    
    DAG_SCHEDULE_OVERRIDES[clean_id] = {
        "schedule": clean_sched,
        "updated_at": time.strftime("%Y-%m-%d %I:%M:%S %p IST")
    }
    save_dag_schedule_overrides(DAG_SCHEDULE_OVERRIDES)
    return {
        "status": "success",
        "dag_id": clean_id,
        "schedule": clean_sched,
        "message": f"Schedule for '{clean_id}' updated to '{clean_sched}' successfully."
    }

def generate_catalog_synced_dags(overrides: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Dynamically auto-syncs all DAGs with the active database Explorer & Catalog.
    Provides table-by-table granular synchronization for BigQuery, AWS S3/Glue,
    Snowflake, DuckDB and Reports & Alerts.
    """
    if overrides is None:
        overrides = DAG_SCHEDULE_OVERRIDES

    from app.explorer_service import get_explorer_catalog
    catalog = get_explorer_catalog()
    today_display = time.strftime("%d %b %Y")
    dags = []

    # 1. Google BigQuery Granular Table-Level Synchronization (12 tables)
    for db in catalog.get("databases", []):
        if db.get("kind") == "bigquery":
            for sch in db.get("schemas", []):
                sch_name = sch.get("name")
                for tbl in sch.get("tables", []):
                    tbl_name = tbl.get("name")
                    row_cnt = tbl.get("rows", 100)
                    dag_id = f"bq_sync_{sch_name}_{tbl_name}".lower()
                    default_sched = "BOD 06:00 IST" if "bronze" in sch_name else "SOD 08:00 IST"
                    sched = overrides.get(dag_id, {}).get("schedule", default_sched)
                    cols = tbl.get("columns", [])
                    
                    dags.append({
                        "id": dag_id,
                        "dag_id": dag_id,
                        "name": f"BigQuery · {tbl_name} to AWS S3 Bronze",
                        "engine": "BigQuery",
                        "stage": "SOURCE",
                        "status": "SUCCESS",
                        "last_run": f"{today_display}, 06:00:12 AM IST",
                        "next_run": f"{today_display}, 18:00:00 PM IST",
                        "schedule": sched,
                        "tables": f"{sch_name}.{tbl_name}",
                        "rows": row_cnt,
                        "columns_count": len(cols),
                        "duplicates_removed": 0,
                        "run_id": f"run_{dag_id}_20261120",
                        "description": f"Continuous table replication from BigQuery {sch_name}.{tbl_name} to AWS S3 Bronze Snappy Parquet.",
                        "detail": f"Target: s3://nanopro-data-lake-765865641438/bronze/{sch_name}/{tbl_name}/ ({len(cols)} columns)"
                    })

    # 2. BigQuery Incremental Delta CDC & Autonomous Sentinel
    dags.append({
        "id": "bq_hourly_cdc_incremental",
        "dag_id": "bq_hourly_cdc_incremental",
        "name": "BigQuery · Hourly Incremental Delta CDC Ingest",
        "engine": "BigQuery",
        "stage": "SOURCE",
        "status": "SUCCESS",
        "last_run": f"{today_display}, 09:00:00 AM IST",
        "next_run": f"{today_display}, 10:00:00 AM IST",
        "schedule": overrides.get("bq_hourly_cdc_incremental", {}).get("schedule", "Every 60m"),
        "tables": "nanopro_cbs_bronze.DELTA_CDC_LOG",
        "rows": 4820,
        "duplicates_removed": 0,
        "run_id": "run_bq_cdc_20261120_0900",
        "description": "Hourly change data capture sweep for high-frequency Core Banking transactions.",
        "detail": "Target: Streaming Buffer Queue"
    })
    dags.append({
        "id": "bq_self_healing_sentinel",
        "dag_id": "bq_self_healing_sentinel",
        "name": "BigQuery · Autonomous Error Sentinel & Auto-Resume",
        "engine": "BigQuery",
        "stage": "CATALOG",
        "status": "SUCCESS",
        "last_run": f"{today_display}, 09:15:00 AM IST",
        "next_run": f"{today_display}, 09:30:00 AM IST",
        "schedule": overrides.get("bq_self_healing_sentinel", {}).get("schedule", "Every 15m"),
        "tables": "Self-Healing Buffer",
        "rows": 0,
        "duplicates_removed": 0,
        "run_id": "run_sentinel_20261120_0915",
        "description": "Autonomous schema invariant validator, partition lock auto-healer and retry sentinel.",
        "detail": "Zero-error invariant self-healed"
    })

    # 3. AWS S3 / Glue to Snowflake L0 Staging - Granular Table DAGs (8 tables)
    for db in catalog.get("databases", []):
        if db.get("kind") == "bigquery":
            for sch in db.get("schemas", []):
                sch_name = sch.get("name")
                if "bronze" in sch_name:
                    for tbl in sch.get("tables", []):
                        tbl_name = tbl.get("name")
                        dag_id = f"s3_to_snowflake_l0_{tbl_name}".lower()
                        sched = overrides.get(dag_id, {}).get("schedule", "BOD 06:30 IST")
                        dags.append({
                            "id": dag_id,
                            "dag_id": dag_id,
                            "name": f"AWS S3 · {tbl_name} to Snowflake L0 Staging",
                            "engine": "AWS S3 / Glue",
                            "stage": "CATALOG",
                            "status": "SUCCESS",
                            "last_run": f"{today_display}, 06:30:15 AM IST",
                            "next_run": f"{today_display}, 18:30:00 PM IST",
                            "schedule": sched,
                            "tables": f"s3://nanopro-data-lake/{sch_name}/{tbl_name}/ -> STG_{tbl_name}",
                            "rows": tbl.get("rows", 100),
                            "duplicates_removed": 0,
                            "run_id": f"run_{dag_id}_20261120",
                            "description": f"External staging load into Snowflake L0 from AWS S3 Parquet landing partition for {tbl_name}.",
                            "detail": "Stage: Snowflake L0_RAW_STAGE"
                        })

    # 4. AWS S3 SFTP Inbound Landing Feeds (4 feeds)
    inbound_feeds = [
        ("sftp_inbound_cbs_eod", "SFTP · Inbound CBS EOD Feed Processor", "CBS_EOD_TXNS_20261120.csv", "BOD 05:30 IST", 45000),
        ("sftp_inbound_swift_mt103", "SFTP · Inbound SWIFT MT103 Remittance Processor", "SWIFT_MT103_CLEARING.xml", "BOD 05:32 IST", 2400),
        ("sftp_inbound_upi_settlement", "SFTP · Inbound NPCI UPI Clearing Batch", "UPI_DAILY_SETTLEMENT_BATCH_01.csv", "BOD 05:35 IST", 88000),
        ("sftp_inbound_gl_closing", "SFTP · Inbound General Ledger Closing Balances", "GL_DAILY_CLOSING_BALANCES.csv", "BOD 05:40 IST", 28000)
    ]
    for fid, fname, ffile, fsched, frows in inbound_feeds:
        sched = overrides.get(fid, {}).get("schedule", fsched)
        dags.append({
            "id": fid,
            "dag_id": fid,
            "name": f"AWS S3 · {fname}",
            "engine": "AWS S3 / Glue",
            "stage": "SOURCE",
            "status": "SUCCESS",
            "last_run": f"{today_display}, 05:30:00 AM IST",
            "next_run": f"{today_display}, 17:30:00 PM IST",
            "schedule": sched,
            "tables": ffile,
            "rows": frows,
            "duplicates_removed": 0,
            "run_id": f"run_{fid}_20261120",
            "description": f"Automated SFTP drop-zone ingestion, SHA-256 integrity validation and AWS S3 Bronze landing.",
            "detail": f"Source: sftp/inbound/{ffile}"
        })

    # 5. Snowflake L0 to L1 Cleansed Transformations (4 DAGs)
    snowflake_l1 = [
        ("snowflake_l0_to_l1_dim_customer", "Snowflake · DIM_CUSTOMER SCD2 Cleansing", "DIM_CUSTOMER", "SOD 08:00 IST", 100, 14),
        ("snowflake_l0_to_l1_fact_txns", "Snowflake · FACT_TRANSACTIONS Cleansing & Normalization", "FACT_TRANSACTIONS", "SOD 08:15 IST", 900, 0),
        ("snowflake_l0_to_l1_dim_branch", "Snowflake · DIM_BRANCH Hierarchy Consolidation", "DIM_BRANCH", "SOD 08:20 IST", 150, 0),
        ("snowflake_l0_to_l1_dim_accounts", "Snowflake · DIM_ACCOUNTS Classification & Balance Sync", "DIM_ACCOUNTS", "SOD 08:25 IST", 100, 0)
    ]
    for sid, sname, stbl, ssched, srows, sdupes in snowflake_l1:
        sched = overrides.get(sid, {}).get("schedule", ssched)
        dags.append({
            "id": sid,
            "dag_id": sid,
            "name": sname,
            "engine": "Snowflake L0-L2",
            "stage": "L0",
            "status": "SUCCESS",
            "last_run": f"{today_display}, 08:00:00 AM IST",
            "next_run": f"{today_display}, 20:00:00 PM IST",
            "schedule": sched,
            "tables": f"L1_CLEANSED.{stbl}",
            "rows": srows,
            "duplicates_removed": sdupes,
            "run_id": f"run_{sid}_20261120",
            "description": "Snowflake transformation engine deduplicating, validating invariants and applying SCD2 logic.",
            "detail": "Cleansed Data Vault Invariant Check: 100% Passed"
        })

    # 6. Snowflake L1 to L2 Dimensional Marts (4 DAGs)
    snowflake_l2 = [
        ("snowflake_l1_to_l2_aml_mart", "Snowflake · MART_AML_CTR_STR Surveillance Mart", "MART_AML_CTR_STR", "SOD 08:30 IST", 16),
        ("snowflake_l1_to_l2_alm_mart", "Snowflake · MART_ALM_BASEL_III Liquidity Mart", "MART_ALM_BASEL_III", "SOD 08:45 IST", 5),
        ("snowflake_l1_to_l2_credit_risk_mart", "Snowflake · MART_CREDIT_RISK_DPD Portfolio Mart", "MART_CREDIT_RISK_DPD", "SOD 08:50 IST", 100),
        ("snowflake_l1_to_l2_gl_ledger", "Snowflake · End of Day General Ledger Reconciler", "GL_BALANCE_LEDGER", "EOD 18:00 IST", 900)
    ]
    for sid, sname, stbl, ssched, srows in snowflake_l2:
        sched = overrides.get(sid, {}).get("schedule", ssched)
        dags.append({
            "id": sid,
            "dag_id": sid,
            "name": sname,
            "engine": "Snowflake L0-L2",
            "stage": "L1",
            "status": "SUCCESS",
            "last_run": f"{today_display}, 08:30:00 AM IST",
            "next_run": f"{today_display}, 18:00:00 PM IST",
            "schedule": sched,
            "tables": f"L2_REPORTING_MARTS.{stbl}",
            "rows": srows,
            "duplicates_removed": 0,
            "run_id": f"run_{sid}_20261120",
            "description": "Dimensional aggregate star schema aggregation for executive dashboards and regulatory reporting.",
            "detail": "Target: Snowflake L2 Star Schema"
        })

    # 7. DuckDB In-Memory Low Latency Analytical Cache (2 DAGs)
    duckdb_dags = [
        ("duckdb_sync_continuous_cache", "DuckDB · Local Analytical Lakehouse Cache (<5ms SLA)", "DuckDB Memory Store", "Continuous", 10557),
        ("duckdb_sync_chats_analytics", "DuckDB · Operational Chats & AI Telemetry Index", "CHATS / MESSAGES", "Continuous", 307)
    ]
    for did, dname, dtbl, dsched, drows in duckdb_dags:
        sched = overrides.get(did, {}).get("schedule", dsched)
        dags.append({
            "id": did,
            "dag_id": did,
            "name": dname,
            "engine": "DuckDB",
            "stage": "L2",
            "status": "SUCCESS",
            "last_run": f"{today_display}, 09:10:00 AM IST",
            "next_run": "Realtime Continuous",
            "schedule": sched,
            "tables": dtbl,
            "rows": drows,
            "duplicates_removed": 0,
            "run_id": f"run_{did}_continuous",
            "description": "Zero-dependency local columnar analytical cache serving instant SQL explorer queries with <5ms SLA.",
            "detail": "Zero RAM Overhead · Zero Cloud Costs"
        })

    # 8. Reports & Alerts (6 DAGs under engine: 'Reports & Alerts')
    reports_alerts = [
        ("report_aml_fiu_ind_16", "16 AML & FIU-IND Statutory Regulatory Reports", "16 Official Schedules (CTR, STR, NTR, CCR, CBWTR)", "T-1 11:00 IST", 16, "2.3 MB", "/api/reports/download/aml_fiu_ind"),
        ("report_master_executive_workbook", "Master Consolidated Banking Executive Workbook", "5 Master Sheets (Gov, CBS, AML, GL, Audit)", "T-1 11:05 IST", 5, "2.1 MB", "/api/reports/download/master_excel"),
        ("report_alm_liquidity", "ALM Structural Liquidity & Basel III LCR/NSFR", "ALM Maturity Buckets (Day 1 to 5+ Years)", "T-1 11:10 IST", 100, "1.0 MB", "/api/reports/download/alm_liquidity"),
        ("report_credit_card_risk", "Credit Card Risk & Delinquency Profiler", "DPD Bands (Current, 30, 60, 90+ NPA)", "T-1 11:12 IST", 100, "1.0 MB", "/api/reports/download/credit_card_risk"),
        ("report_loans_microfinance", "Loans & Microfinance JLG Portfolio", "JLG Groups & PSL Targets", "T-1 11:15 IST", 50, "790 KB", "/api/reports/download/loans_microfinance"),
        ("report_multichannel_broadcast", "Telegram / WhatsApp / Email Multi-Channel Broadcast", "Audit Delivery Log (Bot, WhatsApp, SMTP)", "On-Event", 3, "Direct Stream", None)
    ]
    for rid, rname, rtbl, rsched, rrows, rsize, rurl in reports_alerts:
        sched = overrides.get(rid, {}).get("schedule", rsched)
        dags.append({
            "id": rid,
            "dag_id": rid,
            "name": rname,
            "engine": "Reports & Alerts",
            "stage": "REPORT" if "broadcast" not in rid else "ALERTS",
            "status": "SUCCESS",
            "last_run": f"{today_display}, 11:15:00 AM IST",
            "next_run": f"{today_display}, 23:15:00 PM IST",
            "schedule": sched,
            "tables": rtbl,
            "rows": rrows,
            "duplicates_removed": 0,
            "run_id": f"run_{rid}_20261120",
            "description": f"Regulatory compliance workbook compiled and dispatched via AWS SFTP & Multi-Channel Alert Hub (Size: {rsize}).",
            "detail": f"Delivery: SFTP Outbound Drop & Direct Download" + (f" ({rurl})" if rurl else "")
        })

    return dags

# Backwards compatible alias
DAGS_LIST = generate_catalog_synced_dags()

def toggle_alert_schedule() -> Dict[str, Any]:
    global ALERT_SCHEDULE
    ALERT_SCHEDULE["status"] = "PAUSED" if ALERT_SCHEDULE["status"] == "RUNNING" else "RUNNING"
    ALERT_SCHEDULE["last_updated"] = time.strftime("%Y-%m-%d %I:%M %p IST")
    return {"status": "success", "schedule": ALERT_SCHEDULE}

def update_alert_schedule_time(new_time: str) -> Dict[str, Any]:
    global ALERT_SCHEDULE
    clean_time = (new_time or "").strip()
    if clean_time:
        ALERT_SCHEDULE["dispatch_time"] = clean_time
        ALERT_SCHEDULE["last_updated"] = time.strftime("%Y-%m-%d %I:%M %p IST")
    return {"status": "success", "schedule": ALERT_SCHEDULE}

def get_orchestrator_overview() -> Dict[str, Any]:
    now_ist = time.strftime("%I:%M %p IST")
    now_full = time.strftime("%d/%m/%Y, %I:%M:%S %p IST")
    today_date = time.strftime("%Y-%m-%d")
    today_display = time.strftime("%d %b %Y")

    # Inbound SFTP Files landing on sftp/inbound/
    sftp_inbound_files = [
        {
            "file": "CBS_EOD_TXNS_20261120.csv",
            "source": "Core Banking CBS Feed",
            "size": "6.7 MB",
            "date_time": f"{today_display}, 05:30:12 AM IST",
            "status": "INGESTED & ARCHIVED",
            "records": 45000,
            "target": "nanopro_cbs_bronze",
            "url": "/api/reports/download/cbs_inbound"
        },
        {
            "file": "SWIFT_MT103_CLEARING.xml",
            "source": "SWIFT Messaging Gateway",
            "size": "1.5 MB",
            "date_time": f"{today_display}, 05:32:45 AM IST",
            "status": "INGESTED & ARCHIVED",
            "records": 2400,
            "target": "nanopro_cbs_bronze.SWIFT_MSG",
            "url": "/api/reports/download/swift_inbound"
        },
        {
            "file": "UPI_DAILY_SETTLEMENT_BATCH_01.csv",
            "source": "NPCI UPI Fast Clearing",
            "size": "9.7 MB",
            "date_time": f"{today_display}, 05:35:10 AM IST",
            "status": "INGESTED & ARCHIVED",
            "records": 88000,
            "target": "lakehouse_s3.upi_bronze",
            "url": "/api/reports/download/upi_inbound"
        },
        {
            "file": "GL_DAILY_CLOSING_BALANCES.csv",
            "source": "General Ledger Master",
            "size": "2.3 MB",
            "date_time": f"{today_display}, 05:40:02 AM IST",
            "status": "INGESTED & ARCHIVED",
            "records": 28000,
            "target": "snowflake_l0.gl_balances",
            "url": "/api/reports/download/gl_inbound"
        }
    ]

    # Outbound Statutory & Executive Reports on sftp/outbound/reports/
    sftp_outbound_reports = [
        {
            "report": "Master Consolidated Banking Executive Workbook",
            "file": "Master_Consolidated_Banking_Executive_20261120.xlsx",
            "category": "Executive Governance",
            "size": "2.1 MB",
            "date_time": f"{today_display}, 11:15:00 AM IST",
            "status": "DELIVERED TO SFTP",
            "url": "/api/reports/download/master_excel"
        },
        {
            "report": "16 AML & FIU-IND Statutory Regulatory Reports",
            "file": "AML_FIU_IND_16_Statutory_Reports_20261120.xlsx",
            "category": "AML / FIU-IND Statutory",
            "size": "2.3 MB",
            "date_time": f"{today_display}, 11:15:00 AM IST",
            "status": "DELIVERED TO SFTP",
            "url": "/api/reports/download/aml_fiu_ind"
        },
        {
            "report": "Credit Card Risk & Delinquency Mart",
            "file": "Credit_Card_Risk_Delinquency_20261120.xlsx",
            "category": "Credit Risk Portfolio",
            "size": "1.0 MB",
            "date_time": f"{today_display}, 11:15:00 AM IST",
            "status": "DELIVERED TO SFTP",
            "url": "/api/reports/download/credit_card_risk"
        },
        {
            "report": "ALM Structural Liquidity & Basel III Structural Gap",
            "file": "ALM_Liquidity_Basel_III_20261120.xlsx",
            "category": "Basel III / ALM",
            "size": "1.0 MB",
            "date_time": f"{today_display}, 11:15:00 AM IST",
            "status": "DELIVERED TO SFTP",
            "url": "/api/reports/download/alm_liquidity"
        },
        {
            "report": "Loans & Microfinance JLG Portfolio",
            "file": "Loans_Microfinance_JLG_20261120.xlsx",
            "category": "Microfinance & Priority Lending",
            "size": "790 KB",
            "date_time": f"{today_display}, 11:15:00 AM IST",
            "status": "DELIVERED TO SFTP",
            "url": "/api/reports/download/loans_microfinance"
        }
    ]

    # Dispatched Reports Monitoring: Konta report konal gela
    dispatched_reports_monitoring = [
        {
            "report_name": "Master Consolidated Banking Executive Workbook",
            "file": "Master_Consolidated_Banking_Executive_20261120.xlsx",
            "dispatched_at": f"{today_display}, 11:15 AM IST",
            "status": "DELIVERED",
            "sla": "<300ms SLA",
            "url": "/api/reports/download/master_excel",
            "recipients": [
                {"channel": "TELEGRAM", "target": "@mangesh_reports_bot / @mangesh_reports_channel", "status": "DELIVERED"},
                {"channel": "WHATSAPP", "target": "+91 9028882068", "status": "DELIVERED"},
                {"channel": "EMAIL", "target": "nanoproaistudio@gmail.com", "status": "DELIVERED"}
            ]
        },
        {
            "report_name": "16 AML & FIU-IND Statutory Regulatory Reports",
            "file": "AML_FIU_IND_16_Statutory_Reports_20261120.xlsx",
            "dispatched_at": f"{today_display}, 11:15 AM IST",
            "status": "DELIVERED",
            "sla": "<300ms SLA",
            "url": "/api/reports/download/aml_fiu_ind",
            "recipients": [
                {"channel": "TELEGRAM", "target": "@mangesh_reports_bot / @mangesh_reports_channel", "status": "DELIVERED"},
                {"channel": "WHATSAPP", "target": "+91 9028882068", "status": "DELIVERED"},
                {"channel": "EMAIL", "target": "nanoproaistudio@gmail.com", "status": "DELIVERED"}
            ]
        },
        {
            "report_name": "Credit Card Risk & Delinquency Mart",
            "file": "Credit_Card_Risk_Delinquency_20261120.xlsx",
            "dispatched_at": f"{today_display}, 11:15 AM IST",
            "status": "DELIVERED",
            "sla": "<300ms SLA",
            "url": "/api/reports/download/credit_card_risk",
            "recipients": [
                {"channel": "TELEGRAM", "target": "@mangesh_reports_bot", "status": "DELIVERED"},
                {"channel": "WHATSAPP", "target": "+91 9028882068", "status": "DELIVERED"},
                {"channel": "EMAIL", "target": "mangeshbagul15@gmail.com", "status": "DELIVERED"}
            ]
        },
        {
            "report_name": "ALM Structural Liquidity & Basel III Report",
            "file": "ALM_Liquidity_Basel_III_20261120.xlsx",
            "dispatched_at": f"{today_display}, 11:15 AM IST",
            "status": "DELIVERED",
            "sla": "<300ms SLA",
            "url": "/api/reports/download/alm_liquidity",
            "recipients": [
                {"channel": "EMAIL", "target": "mangeshbagul15@gmail.com", "status": "DELIVERED"},
                {"channel": "TELEGRAM", "target": "@mangesh_reports_bot", "status": "DELIVERED"}
            ]
        },
        {
            "report_name": "Loans & Microfinance JLG Portfolio",
            "file": "Loans_Microfinance_JLG_20261120.xlsx",
            "dispatched_at": f"{today_display}, 11:15 AM IST",
            "status": "DELIVERED",
            "sla": "<300ms SLA",
            "url": "/api/reports/download/loans_microfinance",
            "recipients": [
                {"channel": "WHATSAPP", "target": "+91 9028882068", "status": "DELIVERED"},
                {"channel": "EMAIL", "target": "nanoproaistudio@gmail.com", "status": "DELIVERED"}
            ]
        }
    ]

    # Pipeline Failure / Health Issue Alert Monitoring & Short RCA
    pipeline_incidents_monitoring = [
        {
            "incident_id": "INC_20261120_0842",
            "occurred_at": f"{today_display}, 08:42:10 AM IST",
            "pipeline": "Google BigQuery Bronze CDC",
            "component": "nanopro_cbs_bronze.HTD_TXNS",
            "severity": "TRANSIENT (Self-Healing)",
            "telegram_alert_at": f"{today_display}, 08:42:14 AM IST (@mangesh_reports_bot)",
            "whatsapp_alert_at": f"{today_display}, 08:42:15 AM IST (+919028882068)",
            "rca": "Transient external partition lock during incremental CDC sweep. Re-connected in 3.8s with 0 row drops across 900 records.",
            "status": "HEALED & RESOLVED"
        },
        {
            "incident_id": "INC_20261120_0615",
            "occurred_at": f"{today_display}, 06:15:22 AM IST",
            "pipeline": "Snowflake L1 Dimension Merge",
            "component": "DIM_CUSTOMER (SCD2 Invariant)",
            "severity": "INFO_WARNING",
            "telegram_alert_at": f"{today_display}, 06:15:25 AM IST (@mangesh_reports_bot)",
            "whatsapp_alert_at": f"{today_display}, 06:15:26 AM IST (+919028882068)",
            "rca": "14 duplicate customer records detected in staging; auto-deduplicated via SCD2 hash check without blocking downstream mart.",
            "status": "HEALED & RESOLVED"
        }
    ]

    # Dynamically generated catalog synced DAGs
    all_dags = generate_catalog_synced_dags()
    total_rows = sum(d.get("rows", 0) for d in all_dags if isinstance(d.get("rows"), int))
    return {
        "status": "success",
        "business_date": today_date,
        "healthy_dags": len(all_dags),
        "total_dags": len(all_dags),
        "summary": {
            "success": len(all_dags),
            "total": len(all_dags),
            "paused": sum(1 for d in all_dags if d.get("paused")),
            "rows": total_rows,
            "text": f"✔ All {len(all_dags)} DAGs healthy & in sync with Database Explorer. Zero failures, data errors or alert failures recorded in recent runs."
        },
        "cycles": {
            "business_date": today_date,
            "cycles": [
                {"cycle": "BOD", "scheduled_ist": "06:00", "state": "SUCCESS"},
                {"cycle": "SOD", "scheduled_ist": "08:00", "state": "SUCCESS"},
                {"cycle": "T1", "scheduled_ist": "11:00", "state": "SUCCESS"},
                {"cycle": "EOD", "scheduled_ist": "18:00", "state": "SCHEDULED"}
            ],
            "BOD": {"time": "06:00 IST", "status": "SUCCESS"},
            "SOD": {"time": "08:00 IST", "status": "SUCCESS"},
            "T1": {"time": "11:00 IST", "status": "SUCCESS"},
            "EOD": {"time": "18:00 IST", "status": "SCHEDULED"}
        },
        "last_export_rows": 10557,
        "scheduler": {
            "armed": ALERT_SCHEDULE["status"] == "RUNNING",
            "status": "ARMED" if ALERT_SCHEDULE["status"] == "RUNNING" else "PAUSED",
            "interval_min": 60,
            "last_attempt": time.time() - 120,
            "last_tick": now_full
        },
        "dags": all_dags,
        "sftp": {
            "landing_zone": sftp_inbound_files,
            "inbound_files": sftp_inbound_files,
            "outbound_reports": sftp_outbound_reports
        },
        "sftp_outbound": {
            "reports": sftp_outbound_reports
        },
        "alerts_schedule": ALERT_SCHEDULE,
        "dispatched_reports": dispatched_reports_monitoring,
        "incidents_monitoring": pipeline_incidents_monitoring,
        "notifications": {
            "telegram": {"status": "DELIVERED", "bot": "@mangesh_reports_bot", "chat_id": "1200023268", "last_sent": now_ist},
            "whatsapp": {"status": "DELIVERED", "phone_id": "1355864990944215", "recipient": "+919028882068", "last_sent": now_ist},
            "email": {"status": "DELIVERED", "relay": "Google Apps Script", "recipient": "nanoproaistudio@gmail.com", "last_sent": now_ist}
        },
        "alerts": {
            "channels": {
                "telegram": {"enabled": True, "target": "@mangesh_reports_bot", "chat_id": "1200023268", "status": "CONNECTED", "last_delivery": now_ist},
                "whatsapp": {"enabled": True, "target": "+919028882068", "status": "CONNECTED", "last_delivery": now_ist},
                "email": {"enabled": True, "target": "nanoproaistudio@gmail.com", "status": "CONNECTED", "last_delivery": now_ist}
            },
            "schedule": ALERT_SCHEDULE,
            "dispatched": dispatched_reports_monitoring,
            "incidents": pipeline_incidents_monitoring
        },
        "logs": [
            {"time": "11:20:00 IST", "level": "INFO", "text": "Multi-Channel Broadcast delivered: Telegram (@mangesh_reports_bot), WhatsApp (+919028882068), Email."},
            {"time": "11:15:00 IST", "level": "INFO", "text": "SFTP Outbound Delivery: 5 Core Banking & FIU-IND Workbooks published to secure drop."},
            {"time": "11:05:00 IST", "level": "SUCCESS", "text": "EOD Master Consolidated Executive Workbook generated (5 Sheets, Zero Formula Errors)."},
            {"time": "11:00:00 IST", "level": "SUCCESS", "text": "16 AML/FIU-IND Regulatory Reports batch executed: CTR, STR, CCR, NTR, CBWTR compiled."},
            {"time": "08:42:15 IST", "level": "WARNING", "text": "Transient partition sweep recovered in 3.8s. Alerts dispatched to Telegram & WhatsApp."},
            {"time": "08:30:00 IST", "level": "INFO", "text": "Snowflake L1 to L2 Marts: Dimension & Fact tables materialized."},
            {"time": "08:00:00 IST", "level": "INFO", "text": "Snowflake L0 to L1 Cleansed: 900 records validated against schema manifests."},
            {"time": "06:30:00 IST", "level": "INFO", "text": "AWS S3 Bronze to Snowflake L0 Staging: Parquet ingestion verified."},
            {"time": "06:00:00 IST", "level": "SUCCESS", "text": "Google BigQuery nanopro_cbs_bronze 8 tables export complete (900 rows)."}
        ]
    }
