import time
from typing import Dict, Any, List

def get_explorer_catalog() -> Dict[str, Any]:
    return {
        "status": "success",
        "pipeline_generated_at": time.strftime("%Y-%m-%d %H:%M:%S IST"),
        "databases": [
            {
                "id": "pipe_bigquery",
                "pipe": True,
                "name": "GOOGLE BIGQUERY · nanopro-lakehouse-sandbox",
                "kind": "bigquery",
                "icon": "☁️",
                "status": "live",
                "detail": "Source of record · 63 tables across 4 core banking datasets",
                "error": "",
                "schemas": [
                    {
                        "name": "nanopro_cbs_bronze",
                        "tables": [
                            {"name": "CMG", "type": "table", "rows": 100, "columns": ["CUST_ID", "CUST_NAME", "PAN_NO", "AADHAAR_HASH", "RISK_RATING", "KYC_DATE"]},
                            {"name": "GAM", "type": "table", "rows": 100, "columns": ["FORACID", "ACCT_NAME", "ACCT_CRNCY_CODE", "SCHM_TYPE", "CLR_BAL_AMT", "ACCT_OPN_DATE"]},
                            {"name": "HTD", "type": "table", "rows": 100, "columns": ["TRAN_ID", "FORACID", "TRAN_DATE", "TRAN_AMT", "PARTICULAR", "DELIVERY_CHANNEL"]},
                            {"name": "SOL", "type": "table", "rows": 150, "columns": ["SOL_ID", "SOL_DESC", "CITY", "STATE", "REGION_CODE", "BRANCH_CLASSIFICATION"]},
                            {"name": "SWIFT_MSG", "type": "table", "rows": 100, "columns": ["MSG_REF_NO", "SENDER_BIC", "RECEIVER_BIC", "FIELD_32A_AMT", "FIELD_50K_ORDERING", "FIELD_59_BENEFICIARY"]},
                            {"name": "TAM_LAM", "type": "table", "rows": 100, "columns": ["OPER_ID", "SANCT_LIMIT", "OUTSTANDING_AMT", "INTEREST_RATE", "OVERDUE_BUCKET", "NPA_STAGE"]},
                            {"name": "UBO", "type": "table", "rows": 100, "columns": ["ENTITY_ID", "UBO_NAME", "NATIONALITY", "PERCENT_HOLDING", "PEP_FLAG", "FATCA_STATUS"]},
                            {"name": "VCT", "type": "table", "rows": 150, "columns": ["ACCT_ID", "AVG_MONTHLY_TURNOVER", "CASH_DEPOSIT_RATIO", "VELOCITY_INDEX", "ALERT_TRIGGERED", "LAST_SCAN_TS"]}
                        ]
                    },
                    {
                        "name": "nanopro_bank_core",
                        "tables": [
                            {"name": "AML_ALERT", "type": "table", "rows": 100, "columns": ["ALERT_ID", "RULE_CODE", "ACCOUNT_NO", "SCORE", "STATUS"]},
                            {"name": "AML_CASE", "type": "table", "rows": 100, "columns": ["CASE_ID", "CASE_TYPE", "FIU_FLAG", "ANALYST", "RISK_TIER"]},
                            {"name": "ATM_SWITCH", "type": "table", "rows": 100, "columns": ["TXN_SEQ", "TERMINAL_ID", "CARD_BIN", "TXN_STATUS", "RESPONSE_CODE"]},
                            {"name": "BORROWER_ENTITY", "type": "table", "rows": 100, "columns": ["LEI_CODE", "COMPANY_NAME", "SECTOR", "CREDIT_RATING", "EXPOSURE_AMT"]}
                        ]
                    }
                ]
            },
            {
                "id": "pipe_duckdb",
                "pipe": True,
                "name": "DUCKDB IN-MEMORY · fast analytical cache",
                "kind": "duckdb",
                "icon": "🦆",
                "status": "live",
                "detail": "Local zero-latency execution & working set persistence",
                "error": "",
                "schemas": [
                    {
                        "name": "main",
                        "tables": [
                            {"name": "CHATS", "type": "table", "rows": 31, "columns": ["ID", "TITLE", "MODEL", "EFFORT", "PINNED", "MSG_COUNT"]},
                            {"name": "MESSAGES", "type": "table", "rows": 271, "columns": ["ID", "CHAT_ID", "ROLE", "CONTENT", "DURATION_MS"]},
                            {"name": "PROJECTS", "type": "table", "rows": 5, "columns": ["ID", "NAME", "DESCRIPTION", "UPDATED_AT"]}
                        ]
                    }
                ]
            },
            {
                "id": "pipe_snowflake",
                "pipe": True,
                "name": "SNOWFLAKE L0-L2 · banking lakehouse",
                "kind": "snowflake",
                "icon": "❄️",
                "status": "live",
                "detail": "Enterprise Medallion Lakehouse Architecture",
                "error": "",
                "schemas": [
                    {
                        "name": "L0_RAW_STAGE",
                        "tables": [
                            {"name": "STG_CBS_CORE", "type": "table", "rows": 900, "columns": ["RAW_PAYLOAD", "INGEST_TS"]},
                            {"name": "STG_SWIFT_FEEDS", "type": "table", "rows": 100, "columns": ["MESSAGE_TEXT", "PARSED_STATUS"]}
                        ]
                    },
                    {
                        "name": "L1_CLEANSED",
                        "tables": [
                            {"name": "DIM_CUSTOMER", "type": "table", "rows": 100, "columns": ["SK_CUST", "CUST_ID", "KYC_VERIFIED"]},
                            {"name": "FACT_TRANSACTIONS", "type": "table", "rows": 900, "columns": ["SK_TXN", "AMOUNT", "CHANNEL"]}
                        ]
                    },
                    {
                        "name": "L2_REPORTING_MARTS",
                        "tables": [
                            {"name": "MART_AML_CTR_STR", "type": "table", "rows": 16, "columns": ["REPORT_ID", "RECORD_COUNT", "FIU_STATUS"]},
                            {"name": "MART_ALM_BASEL_III", "type": "table", "rows": 5, "columns": ["GAP_BUCKET", "LCR_RATIO", "NSFR"]}
                        ]
                    }
                ]
            },
            {
                "id": "pipe_s3",
                "pipe": True,
                "name": "AWS S3 / GLUE · medallion storage",
                "kind": "s3",
                "icon": "🟧",
                "status": "live",
                "detail": "nanopro-data-lake-765865641438 (ap-southeast-2)",
                "error": "",
                "schemas": [
                    {
                        "name": "nanopro-data-lake",
                        "tables": [
                            {"name": "bronze_cbs_raw", "type": "external", "rows": 900, "columns": ["_PARTITION_DATE", "PAYLOAD"]},
                            {"name": "silver_curated_parquet", "type": "external", "rows": 900, "columns": ["CUSTOMER_ID", "TXN_DATE"]},
                            {"name": "gold_fiu_ind_workbooks", "type": "external", "rows": 21, "columns": ["REPORT_NAME", "S3_URI"]}
                        ]
                    }
                ]
            },
            {
                "id": "pipe_sftp",
                "pipe": True,
                "name": "SFTP HUB · Regulatory & FIU-IND Exchanges",
                "kind": "sftp",
                "icon": "📂",
                "status": "live",
                "detail": "Automated inbound landing zone & outbound secure drop",
                "error": "",
                "schemas": [
                    {
                        "name": "sftp_zones",
                        "tables": [
                            {"name": "INBOUND_LANDING", "type": "feed", "rows": 2, "columns": ["FILE_NAME", "FILE_SIZE", "LANDED_TS"]},
                            {"name": "OUTBOUND_DELIVERY", "type": "feed", "rows": 21, "columns": ["REPORT_NAME", "FORMAT", "DISPATCHED_TS"]}
                        ]
                    }
                ]
            }
        ]
    }

def get_table_details(db_id: str, schema: str, table: str) -> Dict[str, Any]:
    return {
        "status": "success",
        "database": db_id,
        "schema": schema,
        "table": table,
        "row_count": 100 if table in ["CMG", "GAM", "HTD"] else (150 if table in ["SOL", "VCT"] else 900),
        "columns": [
            {"name": "ID", "type": "VARCHAR(64)", "nullable": False, "is_pk": True},
            {"name": "BUSINESS_DATE", "type": "DATE", "nullable": False, "is_pk": False},
            {"name": "RECORD_DATA", "type": "JSON", "nullable": True, "is_pk": False},
            {"name": "STATUS", "type": "VARCHAR(32)", "nullable": False, "is_pk": False},
            {"name": "INGEST_TIMESTAMP", "type": "TIMESTAMP", "nullable": False, "is_pk": False}
        ],
        "sample_rows": [
            {"ID": f"{table}_001", "BUSINESS_DATE": "2026-11-20", "STATUS": "ACTIVE", "INGEST_TIMESTAMP": "2026-11-20 06:00:12 IST"},
            {"ID": f"{table}_002", "BUSINESS_DATE": "2026-11-20", "STATUS": "ACTIVE", "INGEST_TIMESTAMP": "2026-11-20 06:00:15 IST"},
            {"ID": f"{table}_003", "BUSINESS_DATE": "2026-11-20", "STATUS": "ACTIVE", "INGEST_TIMESTAMP": "2026-11-20 06:00:18 IST"}
        ]
    }
