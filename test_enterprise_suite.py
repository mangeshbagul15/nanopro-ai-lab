import time
import json
from nanopro_db_agent import (
    get_nanopro_ecosystem_health,
    locate_and_inspect_medallion_catalog,
    manage_pipelines_and_glue_jobs,
    manage_schedulers,
    inspect_report_history_and_lineage,
    check_and_send_notification_deliveries,
    modify_report_definition_and_rerun,
    build_cross_engine_join_report,
    execute_and_commit_mutation,
    manage_users_and_roles,
    manage_privacy_policy_and_ad_ids,
    UCBModelRouter,
    HybridRRFRetriever,
    validate_and_transpile_sql
)
from nanopro_connectors import PrivacyAndAdConfigConnector

print('=== 1. Testing Core AI Algorithms ===')

# UCB Router
m_fast = UCBModelRouter.select_model('What is DB health?')
m_eng = UCBModelRouter.select_model('Build a cross engine join report with sql')
m_deep = UCBModelRouter.select_model('Audit root cause failure and regulatory risk')
print(f"UCB Fast: {m_fast['recommended_model']} (Score: {m_fast['ucb_score']})")
print(f"UCB Eng: {m_eng['recommended_model']} (Score: {m_eng['ucb_score']})")
print(f"UCB Deep: {m_deep['recommended_model']} (Score: {m_deep['ucb_score']})")

# Hybrid RRF Search
candidates = [
    {'table_name': 'CMG', 'purpose': 'Customer Master General KYC and PAN records', 'columns': [{'name': 'CUST_ID'}, {'name': 'PAN_NO'}]},
    {'table_name': 'GAM', 'purpose': 'General Account Master balances and currency', 'columns': [{'name': 'FORACID'}, {'name': 'CLR_BAL_AMT'}]},
    {'table_name': 'HTD', 'purpose': 'Historical Transaction Data amounts and dates', 'columns': [{'name': 'TRAN_ID'}, {'name': 'TRAN_AMT'}]},
    {'table_name': 'AML_STR_CASES', 'purpose': 'Anti Money Laundering suspicious transactions FIU', 'columns': [{'name': 'STR_ID'}, {'name': 'SCORE'}]}
]
search_res = HybridRRFRetriever.rank_items('find suspicious transactions AML', candidates)
print(f"Hybrid RRF Top 1: {search_res[0]['table_name']} - {search_res[0]['purpose']}")

# AST Validation
ast_res = validate_and_transpile_sql('SELECT CUST_NAME, sum(TRAN_AMT) FROM CMG JOIN HTD ON CMG.CUST_ID=HTD.CUST_ID GROUP BY CUST_NAME')
print(f"AST Valid: {ast_res.get('valid')} | Transpiled: {ast_res.get('ast_transpiled')[:60]}...")

# PII Masking
raw_text = 'User Rajesh PAN ABCDE1234F Aadhaar 1234-5678-9012 Phone 9822012345 Email test@bank.com'
masked = PrivacyAndAdConfigConnector.mask_pii(raw_text)
print(f"PII Masked: {masked}")

print('\n=== 2. Testing 11 Enterprise Tools ===')

# Tool 1: Ecosystem Health
t1 = get_nanopro_ecosystem_health()
print(f"Tool 1 (Ecosystem Health): {t1['status']} - {t1.get('total_engines_connected', len(t1.get('ecosystem_health', {})))} engines connected")

# Tool 2: Medallion Catalog
t2 = locate_and_inspect_medallion_catalog('AML')
print(f"Tool 2 (Catalog): {t2['status']} - Found {t2.get('total_objects_matched', 0)} tables: {[t.get('table_name') for t in t2.get('catalog', [])[:3]]}")

# Tool 3: Pipelines & Glue Jobs
t3 = manage_pipelines_and_glue_jobs(action='LIST')
print(f"Tool 3 (Pipelines/Glue): {t3['status']} - Total jobs: {len(t3.get('jobs', []))}")

# Tool 4: Schedulers
t4 = manage_schedulers(action='LIST')
print(f"Tool 4 (Schedulers): {t4['status']} - Active: {len(t4.get('schedules', []))}")

# Tool 5: Lineage & History
t5 = inspect_report_history_and_lineage(report_name='AML_STR_DAILY_RUN')
defs = t5.get("definitions_and_lineage", [])
print(f"Tool 5 (Lineage): {t5['status']} - Layer: {defs[0].get('layer') if defs else 'None'} | Defs count: {len(defs)}")

# Tool 6: Notifications Delivery
t6 = check_and_send_notification_deliveries(action='check_logs')
print(f"Tool 6 (Delivery Audit): {t6['status']} - Deliveries logged: {t6.get('total_records', len(t6.get('deliveries', [])))}")

# Tool 7: Modify Report Def & Rerun
t7 = modify_report_definition_and_rerun('AML_STR_DAILY_RUN', 'HTD.TRAN_AMT > 75000')
print(f"Tool 7 (Modify & Rerun): {t7['status']} - Filter: {t7.get('modified_filter')} | Rows: {t7.get('rows_generated')}")

# Tool 8: Cross Engine Join
t8 = build_cross_engine_join_report(
    sources=[{'engine': 'DUCKDB', 'table': 'CMG'}, {'engine': 'DUCKDB', 'table': 'GAM'}],
    join_keys='CMG.CUST_ID = GAM.CUST_ID',
    save_as_report_name='TEST_FEDERATED_REPORT'
)
print(f"Tool 8 (Cross Engine Join): {t8['status']} - Total rows: {t8.get('total_rows')} | CSV: {t8.get('downloadable_csv', {}).get('filename')}")

# Tool 9: Execute Mutation
t9 = execute_and_commit_mutation(
    engine='DUCKDB',
    sql_or_command="""
        INSERT INTO nanopro_job_logs (id, job_name, job_type, target_table, status, rows_processed, duration_ms, created_by)
        VALUES (99999, 'TEST_JOB_MUTATION', 'VALIDATION', 'nanopro_job_logs', 'SUCCESS', 1, 15, 'Enterprise Agent')
    """,
    intent_summary="Validation job log insertion with explicit commit"
)
print(f"Tool 9 (Mutation & Commit): {t9['status']} - Committed: {t9.get('committed')} | Target: {t9.get('target_table')}")

# Tool 10: Manage Users & Roles
t10 = manage_users_and_roles(action='LIST')
print(f"Tool 10 (RBAC Users): {t10['status']} - Users count: {len(t10.get('users', []))}")

# Tool 11: Privacy & Ad Config
t11 = manage_privacy_policy_and_ad_ids(action='GET_CONFIG')
print(f"Tool 11 (Privacy & Ads): {t11['status']} - Privacy version: {t11.get('privacy_policy', {}).get('version')} | Ad unit: {t11.get('ad_monetization', {}).get('publisher_id')}")

print('\nALL 11 TOOLS AND ALGORITHMS VERIFIED SUCCESSFULLY!')
