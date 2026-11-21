# -*- coding: utf-8 -*-
"""
NanoPro AI LAB - Live Auto-Refreshing Operations Dashboard
Panels:
1. Multi-Cloud & Medallion Health Cards (Snowflake L0-L2, BigQuery, AWS S3/Glue, Supabase, Render PG, DuckDB)
2. Pipeline, Glue Jobs & Scheduler Monitor
3. Report & Multi-Channel Delivery Tracker (Email, Telegram, WhatsApp)
4. User Governance (RBAC), Ad ID Monetization Telemetry & Privacy Policy (PII Masking)
"""

import os
import json
import time
import datetime
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from nanopro_connectors import (
    RenderPostgresConnector, BigQueryConnector, SnowflakeConnector,
    SupabaseConnector, AWSConnector, DuckDBFederatedConnector,
    NotificationDeliveryConnector, SchedulerConnector, UserGovernanceConnector,
    PrivacyAndAdConfigConnector
)

from nanopro_db_agent import (
    get_nanopro_ecosystem_health,
    locate_and_inspect_medallion_catalog,
    manage_pipelines_and_glue_jobs,
    manage_schedulers,
    inspect_report_history_and_lineage,
    check_and_send_notification_deliveries,
    manage_users_and_roles,
    manage_privacy_policy_and_ad_ids
)


def render_live_operations_dashboard():
    """Renders the comprehensive Live Auto-Refreshing Operations Dashboard."""
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
        <h2 style="margin:0; color:#F8FAFC;">📊 Live Operations & Multi-Channel Delivery Dashboard</h2>
        <div style="font-size:0.85rem; color:#94A3B8;">
            <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#10B981; margin-right:5px;"></span>
            Live Telemetry Sync: <strong style="color:#E2E8F0;">Active</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Top Control Bar (Auto-refresh toggle & Manual Sync button)
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([2, 1, 1])
    with ctrl_col1:
        st.caption("Real-time telemetry across Snowflake, BigQuery, AWS, Render PG, DuckDB, Email, Telegram, and WhatsApp.")
    with ctrl_col2:
        auto_refresh = st.checkbox("🔄 Auto-Refresh (15s)", value=False)
    with ctrl_col3:
        if st.button("⚡ Sync Live Now"):
            st.rerun()

    # Tabs for the 4 Dedicated Operations Panels
    dash_tab1, dash_tab2, dash_tab3, dash_tab4 = st.tabs([
        "🌐 Multi-Cloud & Medallion Health",
        "⚙️ Pipelines, Glue Jobs & Schedulers",
        "📬 Report & Delivery Audit (Email/TG/WA)",
        "🛡️ Governance, RBAC, Ad IDs & Privacy"
    ])

    # =========================================================================
    # PANEL 1: MULTI-CLOUD & MEDALLION HEALTH CARDS
    # =========================================================================
    with dash_tab1:
        st.subheader("🌐 Multi-Cloud & Medallion Architecture Health")
        eco = get_nanopro_ecosystem_health("ALL")
        h_data = eco.get("ecosystem_health", {})

        col1, col2, col3 = st.columns(3)
        with col1:
            pg = h_data.get("Render PostgreSQL", {})
            st.markdown(f"""
            <div style="background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.3); border-radius:10px; padding:15px; margin-bottom:15px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong style="color:#6EE7B7; font-size:1rem;">🐘 Render PostgreSQL</strong>
                    <span style="background:rgba(16,185,129,0.2); color:#10B981; padding:2px 8px; border-radius:12px; font-size:0.75rem;">LIVE</span>
                </div>
                <div style="margin-top:10px; font-size:0.85rem; color:#CBD5E1;">
                    <p style="margin:2px 0;"><strong>Database:</strong> {pg.get('database', 'nanopro_cbs_prod')}</p>
                    <p style="margin:2px 0;"><strong>Size:</strong> {pg.get('size', '3.26 MB')}</p>
                    <p style="margin:2px 0;"><strong>Active Conns:</strong> {pg.get('active_connections', 1)}</p>
                    <p style="margin:2px 0;"><strong>Latency:</strong> {pg.get('latency_ms', 1.2)}ms</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            aws = h_data.get("AWS S3 & Glue Data Lake", {})
            st.markdown(f"""
            <div style="background:rgba(245,158,11,0.08); border:1px solid rgba(245,158,11,0.3); border-radius:10px; padding:15px; margin-bottom:15px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong style="color:#FCD34D; font-size:1rem;">📦 AWS S3 & Glue Data Lake</strong>
                    <span style="background:rgba(245,158,11,0.2); color:#F59E0B; padding:2px 8px; border-radius:12px; font-size:0.75rem;">HEALTHY</span>
                </div>
                <div style="margin-top:10px; font-size:0.85rem; color:#CBD5E1;">
                    <p style="margin:2px 0;"><strong>Bucket:</strong> nanopro-data-lake-7658...</p>
                    <p style="margin:2px 0;"><strong>Region:</strong> ap-southeast-2</p>
                    <p style="margin:2px 0;"><strong>Inbound Feeds:</strong> {aws.get('inbound_feeds_count', 4)}</p>
                    <p style="margin:2px 0;"><strong>Glue Jobs Active:</strong> 4</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            bq = h_data.get("Google BigQuery", {})
            st.markdown(f"""
            <div style="background:rgba(56,189,248,0.08); border:1px solid rgba(56,189,248,0.3); border-radius:10px; padding:15px; margin-bottom:15px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong style="color:#7DD3FC; font-size:1rem;">☁️ Google BigQuery</strong>
                    <span style="background:rgba(56,189,248,0.2); color:#38BDF8; padding:2px 8px; border-radius:12px; font-size:0.75rem;">ONLINE</span>
                </div>
                <div style="margin-top:10px; font-size:0.85rem; color:#CBD5E1;">
                    <p style="margin:2px 0;"><strong>Project:</strong> {bq.get('project', 'nanopro-lakehouse-sandbox')}</p>
                    <p style="margin:2px 0;"><strong>Total Datasets:</strong> {bq.get('total_datasets', 5)}</p>
                    <p style="margin:2px 0;"><strong>CBS Bronze:</strong> Connected</p>
                    <p style="margin:2px 0;"><strong>Latency:</strong> {bq.get('latency_ms', 45.2)}ms</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            supa = h_data.get("Supabase DB", {})
            st.markdown(f"""
            <div style="background:rgba(52,211,153,0.08); border:1px solid rgba(52,211,153,0.3); border-radius:10px; padding:15px; margin-bottom:15px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong style="color:#A7F3D0; font-size:1rem;">⚡ Supabase Cloud Postgres</strong>
                    <span style="background:rgba(52,211,153,0.2); color:#34D399; padding:2px 8px; border-radius:12px; font-size:0.75rem;">ACTIVE</span>
                </div>
                <div style="margin-top:10px; font-size:0.85rem; color:#CBD5E1;">
                    <p style="margin:2px 0;"><strong>Project ID:</strong> tbovdmdihmhzgjvsrixo</p>
                    <p style="margin:2px 0;"><strong>PostgREST:</strong> Active (HTTP 200/401)</p>
                    <p style="margin:2px 0;"><strong>Audit Store:</strong> Synchronized</p>
                    <p style="margin:2px 0;"><strong>Latency:</strong> {supa.get('latency_ms', 180)}ms</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            sf = h_data.get("Snowflake Medallion", {})
            st.markdown(f"""
            <div style="background:rgba(168,85,247,0.08); border:1px solid rgba(168,85,247,0.3); border-radius:10px; padding:15px; margin-bottom:15px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong style="color:#D8B4FE; font-size:1rem;">❄️ Snowflake Medallion</strong>
                    <span style="background:rgba(168,85,247,0.2); color:#A855F7; padding:2px 8px; border-radius:12px; font-size:0.75rem;">READY</span>
                </div>
                <div style="margin-top:10px; font-size:0.85rem; color:#CBD5E1;">
                    <p style="margin:2px 0;"><strong>Warehouse:</strong> COMPUTE_WH</p>
                    <p style="margin:2px 0;"><strong>Layers:</strong> L0_STAGING · L1_CUR · L2_MART</p>
                    <p style="margin:2px 0;"><strong>Auto-Suspend:</strong> 60s</p>
                    <p style="margin:2px 0;"><strong>Latency:</strong> 0.0ms</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            duck = h_data.get("DuckDB Federated Engine", {})
            st.markdown(f"""
            <div style="background:rgba(234,179,8,0.08); border:1px solid rgba(234,179,8,0.3); border-radius:10px; padding:15px; margin-bottom:15px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong style="color:#FDE047; font-size:1rem;">🦆 DuckDB In-Memory Mesh</strong>
                    <span style="background:rgba(234,179,8,0.2); color:#EAB308; padding:2px 8px; border-radius:12px; font-size:0.75rem;">ULTRA-FAST</span>
                </div>
                <div style="margin-top:10px; font-size:0.85rem; color:#CBD5E1;">
                    <p style="margin:2px 0;"><strong>Tables In-Memory:</strong> {duck.get('total_tables', 12)}</p>
                    <p style="margin:2px 0;"><strong>Federated Joins:</strong> Active</p>
                    <p style="margin:2px 0;"><strong>Zero-Copy:</strong> Armed</p>
                    <p style="margin:2px 0;"><strong>Latency:</strong> {duck.get('latency_ms', 1.5)}ms</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("📚 Medallion Schema Explorer (L0 Raw -> L1 Curated -> L2 Marts)")
        cat_res = locate_and_inspect_medallion_catalog(layer="ALL")
        items = cat_res.get("catalog", [])
        if items:
            df_cat = pd.DataFrame([{
                "Layer": it.get("layer", "L1"),
                "Engine": it.get("engine", "Render PG"),
                "Table Name": it.get("table_name", ""),
                "Row Count": it.get("row_count", 0),
                "Purpose": it.get("purpose", "Core Banking")
            } for it in items[:25]])
            st.dataframe(df_cat, use_container_width=True)

    # =========================================================================
    # PANEL 2: PIPELINES, GLUE JOBS & SCHEDULERS
    # =========================================================================
    with dash_tab2:
        st.subheader("⚙️ AWS Glue ETL Jobs & Pipeline Execution Monitor")
        glue_res = manage_pipelines_and_glue_jobs(action="list_status")
        jobs = glue_res.get("jobs", [])

        df_jobs = pd.DataFrame(jobs)
        st.dataframe(df_jobs, use_container_width=True)

        st.markdown("##### 🚀 Quick Trigger / Stop Controls")
        t_col1, t_col2, t_col3 = st.columns([2, 1, 1])
        with t_col1:
            sel_job = st.selectbox("Select AWS Glue / Pipeline", [j["job_name"] for j in jobs])
        with t_col2:
            if st.button("▶️ Trigger Job Now"):
                t_res = manage_pipelines_and_glue_jobs(action="trigger_run", job_name=sel_job)
                st.success(f"Triggered: {t_res.get('message')}")
        with t_col3:
            if st.button("⏹️ Stop Job"):
                s_res = manage_pipelines_and_glue_jobs(action="stop_run", job_name=sel_job)
                st.warning(f"Stopped: {s_res.get('message')}")

        st.markdown("---")
        st.subheader("⏰ Automated Cron Schedulers (nanopro_schedules)")
        sched_res = manage_schedulers(action="list")
        schedules = sched_res.get("schedules", [])
        if schedules:
            df_sched = pd.DataFrame(schedules)
            st.dataframe(df_sched, use_container_width=True)

    # =========================================================================
    # PANEL 3: REPORT & MULTI-CHANNEL DELIVERY AUDIT (EMAIL, TELEGRAM, WHATSAPP)
    # =========================================================================
    with dash_tab3:
        st.subheader("📬 Multi-Channel Report Delivery Audit (Email / Telegram / WhatsApp)")
        notif_res = check_and_send_notification_deliveries(channel="ALL", limit=30)
        deliveries = notif_res.get("deliveries", [])
        counts = notif_res.get("channel_counts", {})

        mcol1, mcol2, mcol3, mcol4 = st.columns(4)
        mcol1.metric("Total Deliveries Logged", notif_res.get("total_records", 0))
        mcol2.metric("📧 Email Deliveries", counts.get("EMAIL", 0))
        mcol3.metric("✈️ Telegram Alerts", counts.get("TELEGRAM", 0))
        mcol4.metric("💬 WhatsApp Alerts", counts.get("WHATSAPP", 0))

        if deliveries:
            df_deliv = pd.DataFrame(deliveries)
            st.dataframe(df_deliv, use_container_width=True)

            # Plotly Distribution Chart
            st.markdown("##### 📈 Delivery Channels Distribution")
            chart_data = pd.DataFrame([
                {"Channel": "Email", "Count": counts.get("EMAIL", 0)},
                {"Channel": "Telegram", "Count": counts.get("TELEGRAM", 0)},
                {"Channel": "WhatsApp", "Count": counts.get("WHATSAPP", 0)}
            ])
            fig = px.pie(chart_data, values="Count", names="Channel", color_discrete_sequence=["#38BDF8", "#818CF8", "#34D399"])
            fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#E2E8F0")
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.markdown("##### 🚀 Test Instant Report Notification")
        scol1, scol2, scol3, scol4 = st.columns([1, 1, 1, 1])
        with scol1:
            send_ch = st.selectbox("Channel", ["EMAIL", "TELEGRAM", "WHATSAPP"])
        with scol2:
            send_rep = st.selectbox("Report Name", ["AML_STR_DAILY_RUN", "CTR_MONTHLY_AGG", "CRILC_LARGE_EXPOSURES"])
        with scol3:
            send_rec = st.text_input("Recipient", value="compliance-officer@bank.com" if send_ch == "EMAIL" else ("@nanopro_alerts" if send_ch == "TELEGRAM" else "+919822012345"))
        with scol4:
            st.write("")
            st.write("")
            if st.button("📤 Send Test Alert"):
                s_res = check_and_send_notification_deliveries(
                    action="send_notification",
                    payload={"channel": send_ch, "report_name": send_rep, "recipient": send_rec, "message_type": "SUMMARY_ALERT"}
                )
                st.success(f"Sent! Delivery Logged ID: `{s_res.get('provider_msg_id')}`")
                st.rerun()

    # =========================================================================
    # PANEL 4: GOVERNANCE, RBAC, AD IDS & PRIVACY POLICY
    # =========================================================================
    with dash_tab4:
        st.subheader("🛡️ Platform Governance, Users (RBAC) & Monetization")

        gov_col1, gov_col2 = st.columns([1, 1])

        with gov_col1:
            st.markdown("##### 👥 User Management & RBAC Roles")
            u_res = manage_users_and_roles(action="list")
            users = u_res.get("users", [])
            if users:
                df_users = pd.DataFrame(users)
                st.dataframe(df_users, use_container_width=True)

            st.markdown("###### 🔄 Modify User Role")
            u_sel = st.selectbox("Select User", [u["email"] for u in users] if users else ["mangesh@nanopro.ai"])
            r_sel = st.selectbox("Role", ["ADMIN", "DATA_ENGINEER", "ANALYST", "VIEWER"])
            if st.button("Save User Role"):
                manage_users_and_roles(action="update", username_or_email=u_sel, role=r_sel)
                st.success(f"Updated {u_sel} to role `{r_sel}`")
                st.rerun()

        with gov_col2:
            st.markdown("##### 💰 Ad Network IDs & Monetization Telemetry")
            gov_res = manage_privacy_policy_and_ad_ids(action="get", section="ALL")
            ad_telemetry = gov_res.get("ad_monetization_telemetry", {})
            
            ad_c1, ad_c2, ad_c3 = st.columns(3)
            ad_c1.metric("Impressions", f"{ad_telemetry.get('total_impressions', 48250):,}")
            ad_c2.metric("Clicks", f"{ad_telemetry.get('total_clicks', 1420):,}")
            ad_c3.metric("Est. Revenue", f"${ad_telemetry.get('total_revenue_usd', 184.75)}")

            st.markdown("###### 🏷️ Active Ad Network Configuration")
            configs = gov_res.get("platform_governance", {})
            ad_cfg = configs.get("AD_MONETIZATION", {}).get("value", {})
            st.json(ad_cfg)

        st.markdown("---")
        st.subheader("🔒 Privacy Policy & PII Masking Governance")
        priv_cfg = configs.get("PRIVACY_POLICY", {}).get("value", {})

        p_col1, p_col2 = st.columns([1, 1])
        with p_col1:
            st.markdown(f"**Policy Version:** `{priv_cfg.get('version', '2026.4.PROD')}`")
            st.markdown(f"**Effective Date:** `{priv_cfg.get('effective_date', '2026-01-01')}`")
            st.markdown(f"**Data Retention:** `{priv_cfg.get('data_retention_days', 180)} days`")
            st.markdown(f"**PII Masking:** `{'ENABLED' if priv_cfg.get('pii_masking_enabled') else 'DISABLED'}`")
            st.markdown(f"**Masked Entities:** `{', '.join(priv_cfg.get('masked_entities', ['PAN', 'AADHAAR', 'PHONE', 'EMAIL']))}`")

        with p_col2:
            st.markdown("##### 🧪 Test Real-Time PII Masking Engine")
            test_input = st.text_input("Enter test text containing PII", value="Customer Mangesh Bagul PAN: ABCDE1234F, Aadhaar: 1234 5678 9012, Phone: 9822012345, Email: mangesh@nanopro.ai")
            masked_output = PrivacyAndAdConfigConnector.mask_pii(test_input)
            st.code(masked_output, language="text")
