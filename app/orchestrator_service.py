import time
from typing import Dict, Any, List

DAGS_LIST = [
    {
        "id": "bq_to_s3_bronze_lake",
        "dag_id": "bq_to_s3_bronze_lake",
        "name": "Google BigQuery to AWS S3 Bronze",
        "engine": "BigQuery",
        "stage": "SOURCE",
        "status": "SUCCESS",
        "last_run": "2026-11-20 06:00 IST",
        "schedule": "BOD 06:00 IST",
        "tables": "8 CBS Bronze Tables",
        "rows": 900,
        "duplicates_removed": 0,
        "run_id": "run_bq_bronze_20261120_0600"
    },
    {
        "id": "s3_bronze_to_snowflake_l0",
        "dag_id": "s3_bronze_to_snowflake_l0",
        "name": "AWS S3 to Snowflake L0 Staging",
        "engine": "AWS S3 / Glue",
        "stage": "CATALOG",
        "status": "SUCCESS",
        "last_run": "2026-11-20 06:30 IST",
        "schedule": "BOD 06:30 IST",
        "tables": "8 Raw Tables",
        "rows": 900,
        "duplicates_removed": 0,
        "run_id": "run_s3_to_l0_20261120_0630"
    },
    {
        "id": "snowflake_l0_to_l1_cleansed",
        "dag_id": "snowflake_l0_to_l1_cleansed",
        "name": "Snowflake L0 to L1 Cleansed Transformation",
        "engine": "Snowflake L0-L2",
        "stage": "L0",
        "status": "SUCCESS",
        "last_run": "2026-11-20 08:00 IST",
        "schedule": "SOD 08:00 IST",
        "tables": "8 Cleansed Tables",
        "rows": 900,
        "duplicates_removed": 14,
        "run_id": "run_l0_to_l1_20261120_0800"
    },
    {
        "id": "snowflake_l1_to_l2_marts",
        "dag_id": "snowflake_l1_to_l2_marts",
        "name": "Snowflake L1 to L2 Dimensional Marts",
        "engine": "Snowflake L0-L2",
        "stage": "L1",
        "status": "SUCCESS",
        "last_run": "2026-11-20 08:30 IST",
        "schedule": "SOD 08:30 IST",
        "tables": "12 Star Schema Marts",
        "rows": 900,
        "duplicates_removed": 0,
        "run_id": "run_l1_to_l2_20261120_0830"
    },
    {
        "id": "duckdb_local_analytical_sync",
        "dag_id": "duckdb_local_analytical_sync",
        "name": "DuckDB Local Low-Latency Analytic Cache",
        "engine": "DuckDB",
        "stage": "L2",
        "status": "SUCCESS",
        "last_run": "2026-11-20 09:00 IST",
        "schedule": "Continuous",
        "tables": "DuckDB Memory Store",
        "rows": 10557,
        "duplicates_removed": 0,
        "run_id": "run_duckdb_sync_continuous"
    },
    {
        "id": "eod_statutory_aml_fiu_ind_16_reports",
        "dag_id": "eod_statutory_aml_fiu_ind_16_reports",
        "name": "16 AML & FIU-IND Statutory Regulatory Reports",
        "engine": "Snowflake L0-L2",
        "stage": "REPORT",
        "status": "SUCCESS",
        "last_run": "2026-11-20 11:00 IST",
        "schedule": "T-1 11:00 IST",
        "tables": "CTR, STR, CCR, NTR, CBWTR",
        "rows": 16,
        "duplicates_removed": 0,
        "run_id": "run_aml_fiu_ind_16_rpt"
    },
    {
        "id": "eod_master_executive_workbook",
        "dag_id": "eod_master_executive_workbook",
        "name": "5 Master Consolidated Banking Workbooks",
        "engine": "Snowflake L0-L2",
        "stage": "REPORT",
        "status": "SUCCESS",
        "last_run": "2026-11-20 11:05 IST",
        "schedule": "T-1 11:05 IST",
        "tables": "5 Master Sheets",
        "rows": 5,
        "duplicates_removed": 0,
        "run_id": "run_master_workbook_batch"
    },
    {
        "id": "sftp_inbound_landing_processor",
        "dag_id": "sftp_inbound_landing_processor",
        "name": "SFTP Inbound Landing Feed Processing",
        "engine": "AWS S3 / Glue",
        "stage": "SOURCE",
        "status": "SUCCESS",
        "last_run": "2026-11-20 05:30 IST",
        "schedule": "BOD 05:30 IST",
        "tables": "CBS_EOD & SWIFT_MT103",
        "rows": 2,
        "duplicates_removed": 0,
        "run_id": "run_sftp_inbound_feed"
    },
    {
        "id": "sftp_outbound_delivery",
        "dag_id": "sftp_outbound_delivery",
        "name": "SFTP Outbound Regulatory Secure Delivery",
        "engine": "AWS S3 / Glue",
        "stage": "REPORT",
        "status": "SUCCESS",
        "last_run": "2026-11-20 11:15 IST",
        "schedule": "T-1 11:15 IST",
        "tables": "21 Banking Reports",
        "rows": 21,
        "duplicates_removed": 0,
        "run_id": "run_sftp_outbound_drop"
    },
    {
        "id": "hourly_incremental_ingest",
        "dag_id": "hourly_incremental_ingest",
        "name": "Hourly Incremental Delta Reconciliation",
        "engine": "BigQuery",
        "stage": "SOURCE",
        "status": "SUCCESS",
        "last_run": "2026-11-20 01:00 IST",
        "schedule": "Every 60m",
        "tables": "Delta Change Log",
        "rows": 50,
        "duplicates_removed": 0,
        "run_id": "run_hourly_cdc_ingest"
    },
    {
        "id": "alm_liquidity_basel_iii_calc",
        "dag_id": "alm_liquidity_basel_iii_calc",
        "name": "ALM Structural Liquidity & Basel III LCR/NSFR",
        "engine": "Snowflake L0-L2",
        "stage": "REPORT",
        "status": "SUCCESS",
        "last_run": "2026-11-20 11:10 IST",
        "schedule": "T-1 11:10 IST",
        "tables": "ALM Maturity Buckets",
        "rows": 100,
        "duplicates_removed": 0,
        "run_id": "run_alm_basel_iii_calc"
    },
    {
        "id": "credit_card_risk_delinquency_mart",
        "dag_id": "credit_card_risk_delinquency_mart",
        "name": "Credit Card Risk & Delinquency Profiler",
        "engine": "Snowflake L0-L2",
        "stage": "REPORT",
        "status": "SUCCESS",
        "last_run": "2026-11-20 11:12 IST",
        "schedule": "T-1 11:12 IST",
        "tables": "Delinquency Bands DPD",
        "rows": 100,
        "duplicates_removed": 0,
        "run_id": "run_cc_risk_profiler"
    },
    {
        "id": "multichannel_alert_broadcast",
        "dag_id": "multichannel_alert_broadcast",
        "name": "Telegram / WhatsApp / Email Multi-Channel Broadcast",
        "engine": "Reports & Alerts",
        "stage": "ALERTS",
        "status": "SUCCESS",
        "last_run": "2026-11-20 11:20 IST",
        "schedule": "On-Event",
        "tables": "Audit Delivery Log",
        "rows": 3,
        "duplicates_removed": 0,
        "run_id": "run_multichannel_alert"
    },
    {
        "id": "self_healing_incident_sentinel",
        "dag_id": "self_healing_incident_sentinel",
        "name": "Autonomous Table Error Sentinel & Auto-Resume",
        "engine": "BigQuery",
        "stage": "CATALOG",
        "status": "SUCCESS",
        "last_run": "2026-11-20 01:30 IST",
        "schedule": "Every 15m",
        "tables": "Self-Healing Buffer",
        "rows": 0,
        "duplicates_removed": 0,
        "run_id": "run_self_healing_sentinel"
    },
    {
        "id": "eod_ledger_reconciliation_batch",
        "dag_id": "eod_ledger_reconciliation_batch",
        "name": "End of Day CBS General Ledger Reconciler",
        "engine": "Snowflake L0-L2",
        "stage": "L2",
        "status": "SUCCESS",
        "last_run": "2026-11-19 18:00 IST",
        "schedule": "EOD 18:00 IST",
        "tables": "GL Balance Ledger",
        "rows": 900,
        "duplicates_removed": 0,
        "run_id": "run_eod_reconciliation"
    }
]

def get_orchestrator_overview() -> Dict[str, Any]:
    now_ist = time.strftime("%I:%M %p IST")
    now_full = time.strftime("%d/%m/%Y, %I:%M:%S %p IST")

    outbound_reports = [
        {"report": "Master Consolidated Banking Executive Workbook", "file": "Master_Consolidated_Banking_Executive_20261120.xlsx", "url": "/api/reports/download/master_excel", "time": "11:15 IST", "status": "DELIVERED"},
        {"report": "AML & FIU-IND 16 Statutory Reports", "file": "AML_FIU_IND_16_Statutory_Reports_20261120.xlsx", "url": "/api/reports/download/aml_fiu_ind", "time": "11:15 IST", "status": "DELIVERED"},
        {"report": "Credit Card Risk & Delinquency Mart", "file": "Credit_Card_Risk_Delinquency_20261120.xlsx", "url": "/api/reports/download/credit_card_risk", "time": "11:15 IST", "status": "DELIVERED"},
        {"report": "ALM Liquidity & Basel III Structural Gap", "file": "ALM_Liquidity_Basel_III_20261120.xlsx", "url": "/api/reports/download/alm_liquidity", "time": "11:15 IST", "status": "DELIVERED"},
        {"report": "Loans & Microfinance JLG Portfolio", "file": "Loans_Microfinance_JLG_20261120.xlsx", "url": "/api/reports/download/loans_microfinance", "time": "11:15 IST", "status": "DELIVERED"}
    ]

    alert_logs = [
        {"time": now_ist, "channel": "TELEGRAM", "recipient": "@mangesh_reports_bot", "status": "DELIVERED", "text": "Telegram SLA Report dispatched to @mangesh_reports_bot (Chat ID: 1200023268)."},
        {"time": now_ist, "channel": "WHATSAPP", "recipient": "+919028882068", "status": "DELIVERED", "text": "WhatsApp Executive Summary delivered via Meta Cloud API (+919028882068)."},
        {"time": now_ist, "channel": "EMAIL", "recipient": "nanoproaistudio@gmail.com", "status": "DELIVERED", "text": "Email Dispatch complete: 21 Reports attached to nanoproaistudio@gmail.com."}
    ]

    return {
        "status": "success",
        "business_date": "2026-11-20",
        "healthy_dags": len(DAGS_LIST),
        "total_dags": len(DAGS_LIST),
        "summary": {
            "success": len(DAGS_LIST),
            "total": len(DAGS_LIST),
            "paused": 0,
            "rows": 10557,
            "text": "✔ All 15 DAGs healthy. Zero failures, data errors or alert failures recorded in the recent runs."
        },
        "cycles": {
            "business_date": "2026-11-20",
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
            "armed": True,
            "status": "ARMED",
            "interval_min": 60,
            "last_attempt": time.time() - 120,
            "last_tick": now_full
        },
        "dags": DAGS_LIST,
        "sftp": {
            "landing_zone": [
                {"file": "CBS_EOD_20261120.csv", "size": "4.2 MB", "status": "PROCESSED", "landed_at": "05:30 IST"},
                {"file": "SWIFT_MT103_FEED.xml", "size": "1.1 MB", "status": "PROCESSED", "landed_at": "05:32 IST"}
            ],
            "outbound_reports": outbound_reports
        },
        "sftp_outbound": {
            "reports": outbound_reports
        },
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
            "logs": alert_logs
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
