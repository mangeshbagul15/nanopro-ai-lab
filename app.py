# -*- coding: utf-8 -*-
"""
NanoPro AI LAB - Enterprise Autonomous Data Engineering, Multi-Channel Delivery & Governance Studio
Streamlit UI backed by live Medallion Lakehouse (Snowflake, BigQuery, AWS S3/Glue, Supabase, Render PG, DuckDB),
Multi-Channel Delivery Tracking (Email, Telegram, WhatsApp), Governance, RBAC, Ad IDs & Privacy Policy.
"""

import os
import sys
import json
import time
import asyncio
from pathlib import Path
import streamlit as st

# Ensure project root is in sys.path
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

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
    select_optimal_model,
    run_nanopro_react_loop,
    NANOPRO_AGENT_TOOLS
)

from nanopro_dashboard import render_live_operations_dashboard

# Page Setup
st.set_page_config(
    page_title="NanoPro AI LAB · Enterprise Operations & Delivery Studio",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark Theme CSS
st.markdown("""
<style>
    .stApp { background-color: #0B1119; color: #E2E8F0; }
    .agent-header {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(56, 189, 248, 0.10));
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        padding: 14px 20px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .status-badge {
        background: rgba(16, 185, 129, 0.2);
        color: #10B981;
        border: 1px solid #10B981;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
    }
    .engine-pill {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 4px;
        margin-bottom: 4px;
    }
    .pill-green { background: rgba(16, 185, 129, 0.15); color: #6EE7B7; border: 1px solid rgba(16, 185, 129, 0.3); }
    .pill-blue { background: rgba(56, 189, 248, 0.15); color: #7DD3FC; border: 1px solid rgba(56, 189, 248, 0.3); }
    .pill-purple { background: rgba(168, 85, 247, 0.15); color: #D8B4FE; border: 1px solid rgba(168, 85, 247, 0.3); }
</style>
""", unsafe_allow_html=True)

# 1. CLEAN-SLATE SESSION INITIALIZATION (ZERO PRE-LOADED STATIC MESSAGES)
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# Header Bar
st.markdown("""
<div class="agent-header">
    <div>
        <h3 style="margin:0; color:#F8FAFC;">🧠 NanoPro AI LAB · Enterprise Operations Studio</h3>
        <p style="margin:2px 0 0 0; color:#94A3B8; font-size:0.88rem;">
            Medallion Data Lakehouse (Snowflake L0-L2 · BigQuery · AWS Glue · Supabase · Render PG · DuckDB) · Multi-Channel Delivery (Email · Telegram · WhatsApp) · RBAC & Governance
        </p>
    </div>
    <div>
        <span class="status-badge">● ENTERPRISE MESH ONLINE</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs: AI Agent vs Live Operations Dashboard
nav_tab1, nav_tab2 = st.tabs(["🧠 Autonomous Operations Agent", "📊 Live Operations Dashboard"])

# Sidebar: Multi-Cloud Telemetry & Quick Action Tools
with st.sidebar:
    st.subheader("⚡ Multi-Cloud Ecosystem")
    eco_health = get_nanopro_ecosystem_health("ALL")

    st.markdown("""
    <div style="font-size:0.85rem; line-height:1.7;">
        <span class="engine-pill pill-green">🐘 Render PG: LIVE</span>
        <span class="engine-pill pill-blue">☁️ BigQuery: LIVE</span>
        <span class="engine-pill pill-purple">❄️ Snowflake: READY</span>
        <span class="engine-pill pill-blue">📦 AWS Glue: HEALTHY</span>
        <span class="engine-pill pill-green">⚡ Supabase: ACTIVE</span>
        <span class="engine-pill pill-purple">🦆 DuckDB: ULTRA-FAST</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🛠️ Quick Operational Tools")

    if st.button("🩺 Ecosystem Health (All 6 Engines)"):
        res = get_nanopro_ecosystem_health("ALL")
        st.session_state.chat_messages.append({"role": "user", "content": "Ecosystem chi health dakhava"})
        table_rows = []
        for eng_name, tel in res.get("ecosystem_health", {}).items():
            status = tel.get("status", "ONLINE")
            lat = tel.get("latency_ms", "—")
            table_rows.append(f"| **{eng_name}** | `{status}` | {lat}ms |")
        rows_str = "\n".join(table_rows)
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": f"### 🌐 NanoPro Multi-Cloud Ecosystem Health\n\n| Engine | Live Status | Latency |\n|---|---|---|\n{rows_str}"
        })
        st.rerun()

    if st.button("📬 Delivery Audit (Email/TG/WA)"):
        res = check_and_send_notification_deliveries(channel="ALL", limit=10)
        delivs = res.get("deliveries", [])
        st.session_state.chat_messages.append({"role": "user", "content": "Mail, Telegram ani WhatsApp var reports gele ka? Konala gele?"})
        deliv_rows = "\n".join([f"| `{d.get('report_name')}` | **{d.get('channel')}** | `{d.get('recipient')}` | `{d.get('status')}` | {d.get('sent_at')} |" for d in delivs])
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": f"### 📬 Multi-Channel Delivery Audit Logs\n\n| Report Name | Channel | Recipient | Status | Sent At |\n|---|---|---|---|---|\n{deliv_rows}"
        })
        st.rerun()

    if st.button("📚 Inspect Medallion Catalog (L0/L1/L2)"):
        res = locate_and_inspect_medallion_catalog(layer="ALL")
        items = res.get("catalog", [])
        st.session_state.chat_messages.append({"role": "user", "content": "Medallion catalog madhe L0, L1, L2 tables dakhava"})
        rows_md = "\n".join([f"| `{it.get('layer', 'L1')}` | `{it.get('engine')}` | `{it.get('table_name')}` | {it.get('row_count', '—')} |" for it in items[:15]])
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": f"### 📚 Medallion Catalog (L0 Raw -> L1 Curated -> L2 Marts)\n\n| Layer | Engine | Table Name | Rows |\n|---|---|---|---|\n{rows_md}"
        })
        st.rerun()

    if st.button("⚙️ AWS Glue Jobs & Pipelines"):
        res = manage_pipelines_and_glue_jobs(action="list_status")
        jobs = res.get("jobs", [])
        st.session_state.chat_messages.append({"role": "user", "content": "AWS Glue jobs ani pipelines che status dakhava"})
        job_rows = "\n".join([f"| `{j.get('job_name')}` | {j.get('layer')} | `{j.get('status')}` | {j.get('last_run')} |" for j in jobs])
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": f"### ⚙️ AWS Glue Jobs & Pipeline Status\n\n| Job Name | Layer | Status | Last Run |\n|---|---|---|---|\n{job_rows}"
        })
        st.rerun()

    if st.button("⚡ Run Federated Cross-Engine Join"):
        j_res = build_cross_engine_join_report(sources=["CMG", "GAM"])
        st.session_state.chat_messages.append({"role": "user", "content": "CMG ani GAM join karun report banava"})
        csv_info = j_res.get("downloadable_csv")
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": f"### ⚡ Federated Cross-Engine Join Complete\n\n- **Federated Engine:** {j_res.get('federated_engine')}\n- **Rows Joined:** {j_res.get('total_rows')}\n- **Latency:** {j_res.get('latency_ms')}ms\n- **SQL:** `{j_res.get('sql_executed')}`",
            "csv_download": csv_info
        })
        st.rerun()

    if st.button("🛡️ Users & Governance (RBAC)"):
        u_res = manage_users_and_roles(action="list")
        users = u_res.get("users", [])
        st.session_state.chat_messages.append({"role": "user", "content": "Platform users ani roles dakhava"})
        user_rows = "\n".join([f"| `{u.get('name')}` | `{u.get('email')}` | **{u.get('role')}** | {'ACTIVE' if u.get('is_active') else 'INACTIVE'} |" for u in users])
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": f"### 👥 User Governance & RBAC Roles\n\n| Name | Email | Role | Status |\n|---|---|---|---|\n{user_rows}"
        })
        st.rerun()

    st.markdown("---")
    selected_model = st.selectbox(
        "🧠 Frontier Model Routing (UCB)",
        ["auto-router", "openai/gpt-oss-120b", "qwen/qwen3.8-27b", "openai/gpt-oss-20b"]
    )

    if st.button("🧹 Clear Chat"):
        st.session_state.chat_messages = []
        st.rerun()

# =========================================================================
# TAB 1: AUTONOMOUS OPERATIONS AGENT (CHAT CANVAS)
# =========================================================================
with nav_tab1:
    # Clean-slate hero (Zero canned demo prompts)
    if not st.session_state.chat_messages:
        st.markdown("""
        <div style="text-align:center; padding: 40px 20px; border: 1px dashed rgba(255,255,255,0.15); border-radius: 12px; margin-bottom: 20px;">
            <h2 style="color: #F8FAFC; margin-bottom: 8px;">🧠 NanoPro AI LAB · Autonomous Operations & Delivery Agent</h2>
            <p style="color: #94A3B8; font-size: 0.95rem; max-width: 720px; margin: 0 auto 18px auto;">
                Directly connected to Snowflake (L0-L2), BigQuery Lakehouse, AWS Glue/S3, Render PG, DuckDB,
                Email, Telegram, and WhatsApp alert gateways. Ask in Marathi, Hinglish, or English to inspect deliveries,
                run joins, check schedules, or modify pipelines.
            </p>
            <div style="display:flex; justify-content:center; gap:8px; flex-wrap:wrap;">
                <span class="engine-pill pill-green">Render PG Connected</span>
                <span class="engine-pill pill-blue">BigQuery Connected</span>
                <span class="engine-pill pill-purple">Snowflake L0-L2 Ready</span>
                <span class="engine-pill pill-blue">AWS Glue / S3 Active</span>
                <span class="engine-pill pill-green">Email / Telegram / WhatsApp Armed</span>
                <span class="engine-pill pill-purple">DuckDB Columnar Live</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Render Conversation History
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"], unsafe_allow_html=True)
            if "csv_download" in msg:
                csv_info = msg["csv_download"]
                if csv_info and os.path.exists(csv_info.get("path", "")):
                    with open(csv_info["path"], "rb") as f:
                        st.download_button(
                            label=f"📥 Download {csv_info.get('filename')}",
                            data=f.read(),
                            file_name=csv_info.get("filename"),
                            mime="text/csv"
                        )

    # Chat Input & ReAct Loop Execution
    user_prompt = st.chat_input("Operations बद्दल विचारा (उदा. 'Mail var report gela ka?', 'Telegram alert dakhava', 'CMG ani GAM join kara')...")

    if user_prompt:
        st.session_state.chat_messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            status_box = st.status("⚙️ **NanoPro Enterprise Agentic Runtime Active** · Inspecting Telemetry...", expanded=True)

            # Dynamic Model Router Decision (UCB Router)
            if selected_model == "auto-router":
                route_decision = select_optimal_model(user_prompt)
                effective_model = route_decision["recommended_model"]
                prov_name = route_decision["provider_name"]
                status_box.write(f"🧠 **UCB Model Router:** Selected `{effective_model}` (Score: {route_decision.get('ucb_score', 0.98)}) — *{route_decision['rationale']}*")
            else:
                effective_model = selected_model
                prov_name = "groq#1"
                status_box.write(f"🧠 **Model:** `{effective_model}` (manual override)")

            if "openrouter" in prov_name.lower():
                api_key = os.environ.get("OPENROUTER_API_KEY", "")
                base_url = "https://openrouter.ai/api/v1"
            else:
                api_key = os.environ.get("GROQ_API_KEY", "")
                base_url = "https://api.groq.com/openai/v1"

            provider = {
                "name": prov_name,
                "api_key": api_key,
                "base_url": base_url,
                "model": effective_model,
                "timeout": 35.0
            }

            try:
                status_box.write("🔍 Retrieving schemas via Hybrid RRF & orchestrating live execution...")

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                agent_result = loop.run_until_complete(
                    run_nanopro_react_loop(
                        prompt=user_prompt,
                        provider=provider,
                        conversation_history=st.session_state.chat_messages
                    )
                )
                loop.close()

                tools_used = agent_result.get("tools_executed", [])
                for t in tools_used:
                    t_name = t.get("tool", "tool")
                    t_status = t.get("result_status", "success").upper()
                    status_box.write(f"• 🔧 Executed `{t_name}` — *Result: {t_status}*")

                status_box.update(label="✅ **Execution Completed via Live Telemetry**", state="complete", expanded=False)

                content = agent_result.get("content", "")
                st.markdown(content, unsafe_allow_html=True)

                msg_to_store = {"role": "assistant", "content": content}
                st.session_state.chat_messages.append(msg_to_store)

            except Exception as e:
                status_box.update(label="⚠️ Execution error", state="error", expanded=True)
                st.error(f"Agentic Runtime Error: {e}")

# =========================================================================
# TAB 2: LIVE OPERATIONS DASHBOARD
# =========================================================================
with nav_tab2:
    render_live_operations_dashboard()
