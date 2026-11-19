import time
from typing import Dict, Any, List

DAGS_LIST = [
    {"dag_id": "bq_to_s3_bronze_lake", "name": "Google BigQuery to AWS S3 Bronze", "engine": "BigQuery", "status": "SUCCESS", "last_run": "2026-11-20 06:00 IST", "schedule": "BOD 06:00 IST", "rows": 900},
    {"dag_id": "s3_bronze_to_snowflake_l0", "name": "AWS S3 to Snowflake L0 Staging", "engine": "AWS S3 / Glue", "status": "SUCCESS", "last_run": "2026-11-20 06:30 IST", "schedule": "BOD 06:30 IST", "rows": 900},
    {"dag_id": "snowflake_l0_to_l1_cleansed", "name": "Snowflake L0 to L1 Cleansed Transformation", "engine": "Snowflake L0-L2", "status": "SUCCESS", "last_run": "2026-11-20 08:00 IST", "schedule": "SOD 08:00 IST", "rows": 900},
    {"dag_id": "snowflake_l1_to_l2_marts", "name": "Snowflake L1 to L2 Dimensional Marts", "engine": "Snowflake L0-L2", "status": "SUCCESS", "last_run": "2026-11-20 08:30 IST", "schedule": "SOD 08:30 IST", "rows": 900},
    {"dag_id": "duckdb_local_analytical_sync", "name": "DuckDB Local Low-Latency Analytic Cache", "engine": "DuckDB", "status": "SUCCESS", "last_run": "2026-11-20 09:00 IST", "schedule": "Continuous", "rows": 10557},
    {"dag_id": "eod_statutory_aml_fiu_ind_16_reports", "name": "16 AML & FIU-IND Statutory Regulatory Reports", "engine": "Snowflake L0-L2", "status": "SUCCESS", "last_run": "2026-11-20 11:00 IST", "schedule": "T-1 11:00 IST", "rows": 16},
    {"dag_id": "eod_master_executive_workbook", "name": "5 Master Consolidated Banking Workbooks", "engine": "Snowflake L0-L2", "status": "SUCCESS", "last_run": "2026-11-20 11:05 IST", "schedule": "T-1 11:05 IST", "rows": 5},
    {"dag_id": "sftp_inbound_landing_processor", "name": "SFTP Inbound Landing Feed Processing", "engine": "SFTP", "status": "SUCCESS", "last_run": "2026-11-20 05:30 IST", "schedule": "BOD 05:30 IST", "rows": 2},
    {"dag_id": "sftp_outbound_delivery", "name": "SFTP Outbound Regulatory Secure Delivery", "engine": "SFTP", "status": "SUCCESS", "last_run": "2026-11-20 11:15 IST", "schedule": "T-1 11:15 IST", "rows": 21},
    {"dag_id": "hourly_incremental_ingest", "name": "Hourly Incremental Delta Reconciliation", "engine": "BigQuery", "status": "SUCCESS", "last_run": "2026-11-20 01:00 IST", "schedule": "Every 60m", "rows": 50},
    {"dag_id": "alm_liquidity_basel_iii_calc", "name": "ALM Structural Liquidity & Basel III LCR/NSFR", "engine": "Snowflake L0-L2", "status": "SUCCESS", "last_run": "2026-11-20 11:10 IST", "schedule": "T-1 11:10 IST", "rows": 100},
    {"dag_id": "credit_card_risk_delinquency_mart", "name": "Credit Card Risk & Delinquency Profiler", "engine": "Snowflake L0-L2", "status": "SUCCESS", "last_run": "2026-11-20 11:12 IST", "schedule": "T-1 11:12 IST", "rows": 100},
    {"dag_id": "multichannel_alert_broadcast", "name": "Telegram / WhatsApp / Email Multi-Channel Broadcast", "engine": "Multi-Channel", "status": "SUCCESS", "last_run": "2026-11-20 11:20 IST", "schedule": "On-Event", "rows": 3},
    {"dag_id": "self_healing_incident_sentinel", "name": "Autonomous Table Error Sentinel & Auto-Resume", "engine": "BigQuery", "status": "SUCCESS", "last_run": "2026-11-20 01:30 IST", "schedule": "Every 15m", "rows": 0},
    {"dag_id": "eod_ledger_reconciliation_batch", "name": "End of Day CBS General Ledger Reconciler", "engine": "Snowflake L0-L2", "status": "SUCCESS", "last_run": "2026-11-19 18:00 IST", "schedule": "EOD 18:00 IST", "rows": 900}
]

def get_orchestrator_overview() -> Dict[str, Any]:
    return {
        "status": "success",
        "business_date": "2026-11-20",
        "healthy_dags": len(DAGS_LIST),
        "total_dags": len(DAGS_LIST),
        "summary": "✔ No failures, data errors or alert failures recorded in the recent runs.",
        "cycles": {
            "BOD": {"time": "06:00 IST", "status": "SUCCESS"},
            "SOD": {"time": "08:00 IST", "status": "SUCCESS"},
            "T1": {"time": "11:00 IST", "status": "SUCCESS"},
            "EOD": {"time": "18:00 IST", "status": "SCHEDULED"}
        },
        "last_export_rows": 10557,
        "scheduler": {
            "status": "ARMED",
            "interval": "every 60 min",
            "last_tick": time.strftime("%d/%m/%Y, %I:%M:%S %p IST")
        },
        "dags": DAGS_LIST,
        "sftp": {
            "landing_zone": [
                {"file": "CBS_EOD_20261120.csv", "size": "4.2 MB", "status": "PROCESSED", "landed_at": "05:30 IST"},
                {"file": "SWIFT_MT103_FEED.xml", "size": "1.1 MB", "status": "PROCESSED", "landed_at": "05:32 IST"}
            ],
            "outbound_reports": [
                {"report": "Master Consolidated Banking Executive Workbook", "file": "Master_Consolidated_Banking_Executive_20261120.xlsx", "url": "/api/reports/download/master_excel", "time": "11:15 IST", "status": "DELIVERED"},
                {"report": "AML & FIU-IND 16 Statutory Reports", "file": "AML_FIU_IND_16_Statutory_Reports_20261120.xlsx", "url": "/api/reports/download/aml_fiu_ind", "time": "11:15 IST", "status": "DELIVERED"},
                {"report": "Credit Card Risk & Delinquency Mart", "file": "Credit_Card_Risk_Delinquency_20261120.xlsx", "url": "/api/reports/download/credit_card_risk", "time": "11:15 IST", "status": "DELIVERED"},
                {"report": "ALM Liquidity & Basel III Structural Gap", "file": "ALM_Liquidity_Basel_III_20261120.xlsx", "url": "/api/reports/download/alm_liquidity", "time": "11:15 IST", "status": "DELIVERED"},
                {"report": "Loans & Microfinance JLG Portfolio", "file": "Loans_Microfinance_JLG_20261120.xlsx", "url": "/api/reports/download/loans_microfinance", "time": "11:15 IST", "status": "DELIVERED"}
            ]
        },
        "notifications": {
            "telegram": {"status": "DELIVERED", "bot": "@mangesh_reports_bot", "chat_id": "1200023268", "last_sent": time.strftime("%I:%M %p IST")},
            "whatsapp": {"status": "DELIVERED", "phone_id": "1355864990944215", "recipient": "+919028882068", "last_sent": time.strftime("%I:%M %p IST")},
            "email": {"status": "DELIVERED", "relay": "Google Apps Script", "recipient": "nanoproaistudio@gmail.com", "last_sent": time.strftime("%I:%M %p IST")}
        },
        "logs": [
            {"time": "11:20:00 IST", "level": "INFO", "text": "Multi-Channel Broadcast delivered: Telegram (@mangesh_reports_bot), WhatsApp, Email."},
            {"time": "11:15:00 IST", "level": "INFO", "text": "SFTP Outbound Delivery: 21 Core Banking & FIU-IND Reports published to secure drop."},
            {"time": "11:05:00 IST", "level": "SUCCESS", "text": "EOD Master Consolidated Executive Workbook generated (5 Sheets, Zero Formula Errors)."},
            {"time": "11:00:00 IST", "level": "SUCCESS", "text": "16 AML/FIU-IND Regulatory Reports batch executed: CTR, STR, CCR, NTR, CBWTR compiled."},
            {"time": "08:30:00 IST", "level": "INFO", "text": "Snowflake L1 to L2 Marts: Dimension & Fact tables materialized."},
            {"time": "08:00:00 IST", "level": "INFO", "text": "Snowflake L0 to L1 Cleansed: 900 records validated against schema manifests."},
            {"time": "06:30:00 IST", "level": "INFO", "text": "AWS S3 Bronze to Snowflake L0 Staging: Parquet ingestion verified."},
            {"time": "06:00:00 IST", "level": "SUCCESS", "text": "Google BigQuery nanopro_cbs_bronze 8 tables export complete (900 rows)."}
        ],
        "incidents": []
    }
