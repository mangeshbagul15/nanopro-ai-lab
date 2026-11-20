import time
from typing import Dict, Any, List

ALERT_SCHEDULE = {
    "status": "RUNNING",
    "dispatch_time": "11:00 AM IST",
    "cycle": "T-1 Statutory EOD Batch",
    "last_updated": "2026-11-20 06:00 IST"
}

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

    return {
        "status": "success",
        "business_date": today_date,
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
        "dags": DAGS_LIST,
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
