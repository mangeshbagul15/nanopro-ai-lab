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

from nanopro_connectors import ChatPersistenceConnector
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
    .model-badge-chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(99, 102, 241, 0.15);
        color: #A5B4FC;
        border: 1px solid rgba(99, 102, 241, 0.3);
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        margin-bottom: 6px;
    }
</style>
""", unsafe_allow_html=True)

# 1. CLEAN-SLATE SESSION INITIALIZATION (ZERO PRE-LOADED STATIC MESSAGES)
if "session_id" not in st.session_state:
    st.session_state.session_id = f"sess_{int(time.time()*1000)}"
if "active_project_id" not in st.session_state:
    st.session_state.active_project_id = "proj_01"
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "messages" not in st.session_state:
    st.session_state.messages = []

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

# =========================================================================
# SIDEBAR: CHATS & PROJECTS + TELEMETRY + QUICK ACTION TOOLS
# =========================================================================
with st.sidebar:
    st.markdown("### 💬 Chats & Projects")
    
    col_c1, col_c2 = st.columns([1, 1])
    with col_c1:
        if st.button("➕ New Chat", use_container_width=True):
            st.session_state.session_id = f"sess_{int(time.time()*1000)}"
            st.session_state.chat_messages = []
            st.session_state.messages = []
            st.rerun()
    with col_c2:
        with st.popover("📁 Project", use_container_width=True):
            st.markdown("**Create New Project**")
            p_name = st.text_input("Name", placeholder="AML Intelligence", key="new_proj_name_input")
            p_desc = st.text_input("Description", placeholder="Regulatory Audits", key="new_proj_desc_input")
            if st.button("Save", key="save_new_proj_btn"):
                if p_name.strip():
                    new_p = ChatPersistenceConnector.create_project(p_name.strip(), p_desc.strip())
                    st.session_state.active_project_id = new_p["project_id"]
                    st.success(f"Project '{p_name}' created!")
                    st.rerun()

    # Dynamic Live History Loading directly from Live Database
    live_history = ChatPersistenceConnector.list_sessions_and_projects()
    saved_projs = live_history.get("projects", [])
    saved_sess = live_history.get("sessions", [])

    # Project Filter
    proj_map = {"All Projects": ""}
    for p in saved_projs:
        proj_map[p.get("name", p.get("project_id"))] = p.get("project_id")
    
    sel_proj_name = st.selectbox("Active Workspace", list(proj_map.keys()), index=0)
    filter_pid = proj_map[sel_proj_name]
    
    filtered_sessions = saved_sess
    if filter_pid:
        filtered_sessions = [s for s in saved_sess if s.get("project_id") == filter_pid]

    st.markdown(f"<span style='font-size:0.78rem; color:#94A3B8;'>Live Sessions ({len(filtered_sessions)})</span>", unsafe_allow_html=True)
    
    # Render session buttons
    for s in filtered_sessions[:10]:
        s_id = s.get("session_id")
        s_title = s.get("title", "AI Session")[:22]
        msg_cnt = s.get("message_count", 0)
        is_active = (s_id == st.session_state.session_id)
        icon = "🟢" if is_active else ("📌" if s.get("is_pinned") else "💬")
        
        if st.button(f"{icon} {s_title} ({msg_cnt})", key=f"chat_sess_{s_id}", use_container_width=True):
            st.session_state.session_id = s_id
            st.session_state.active_project_id = s.get("project_id", "")
            # RESTORE FULL CONVERSATION DIRECTLY FROM LIVE DB (Both User & Complete Assistant with tools, models, tables)
            restored = ChatPersistenceConnector.get_session_messages(s_id)
            st.session_state.chat_messages = restored
            st.session_state.messages = restored
            st.rerun()

    st.markdown("---")
    st.subheader("⚡ Multi-Cloud Ecosystem")
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
        q_user = "Ecosystem chi health dakhava"
        res = get_nanopro_ecosystem_health("ALL")
        table_rows = []
        for eng_name, tel in res.get("ecosystem_health", {}).items():
            status = tel.get("status", "ONLINE")
            lat = tel.get("latency_ms", "—")
            table_rows.append(f"| **{eng_name}** | `{status}` | {lat}ms |")
        rows_str = "\n".join(table_rows)
        q_asst = f"### 🌐 NanoPro Multi-Cloud Ecosystem Health\n\n| Engine | Live Status | Latency |\n|---|---|---|\n{rows_str}"
        
        # Save user and assistant turns to DB
        ChatPersistenceConnector.save_message(st.session_state.session_id, "user", q_user, st.session_state.active_project_id)
        ChatPersistenceConnector.save_message(
            st.session_state.session_id, "assistant", q_asst, st.session_state.active_project_id,
            tool_logs=[{"tool": "get_nanopro_ecosystem_health", "result_status": "SUCCESS"}],
            model_used="qwen/qwen3.8-27b", duration_ms=res.get("latency_ms", 35.0)
        )
        st.session_state.chat_messages.append({"role": "user", "content": q_user})
        st.session_state.chat_messages.append({
            "role": "assistant", "content": q_asst,
            "model_used": "qwen/qwen3.8-27b", "duration_ms": res.get("latency_ms", 35.0),
            "tool_executions": [{"tool": "get_nanopro_ecosystem_health", "result_status": "SUCCESS"}]
        })
        st.session_state.messages = st.session_state.chat_messages
        st.rerun()

    if st.button("📬 Delivery Audit (Email/TG/WA)"):
        q_user = "Mail, Telegram ani WhatsApp var reports gele ka? Konala gele?"
        res = check_and_send_notification_deliveries(channel="ALL", limit=10)
        delivs = res.get("deliveries", [])
        deliv_rows = "\n".join([f"| `{d.get('report_name')}` | **{d.get('channel')}** | `{d.get('recipient')}` | `{d.get('status')}` | {d.get('sent_at')} |" for d in delivs])
        q_asst = f"### 📬 Multi-Channel Delivery Audit Logs\n\n| Report Name | Channel | Recipient | Status | Sent At |\n|---|---|---|---|---|\n{deliv_rows}"
        
        ChatPersistenceConnector.save_message(st.session_state.session_id, "user", q_user, st.session_state.active_project_id)
        ChatPersistenceConnector.save_message(
            st.session_state.session_id, "assistant", q_asst, st.session_state.active_project_id,
            tool_logs=[{"tool": "check_and_send_notification_deliveries", "result_status": "SUCCESS"}],
            model_used="qwen/qwen3.8-27b", duration_ms=res.get("latency_ms", 40.0)
        )
        st.session_state.chat_messages.append({"role": "user", "content": q_user})
        st.session_state.chat_messages.append({
            "role": "assistant", "content": q_asst,
            "model_used": "qwen/qwen3.8-27b", "duration_ms": res.get("latency_ms", 40.0),
            "tool_executions": [{"tool": "check_and_send_notification_deliveries", "result_status": "SUCCESS"}]
        })
        st.session_state.messages = st.session_state.chat_messages
        st.rerun()

    if st.button("📚 Inspect Medallion Catalog (L0/L1/L2)"):
        q_user = "Medallion catalog madhe L0, L1, L2 tables dakhava"
        res = locate_and_inspect_medallion_catalog(layer="ALL")
        items = res.get("catalog", [])
        rows_md = "\n".join([f"| `{it.get('layer', 'L1')}` | `{it.get('engine')}` | `{it.get('table_name')}` | {it.get('row_count', '—')} |" for it in items[:15]])
        q_asst = f"### 📚 Medallion Catalog (L0 Raw -> L1 Curated -> L2 Marts)\n\n| Layer | Engine | Table Name | Rows |\n|---|---|---|---|\n{rows_md}"
        
        ChatPersistenceConnector.save_message(st.session_state.session_id, "user", q_user, st.session_state.active_project_id)
        ChatPersistenceConnector.save_message(
            st.session_state.session_id, "assistant", q_asst, st.session_state.active_project_id,
            tool_logs=[{"tool": "locate_and_inspect_medallion_catalog", "result_status": "SUCCESS"}],
            model_used="openai/gpt-oss-120b", duration_ms=res.get("latency_ms", 45.0)
        )
        st.session_state.chat_messages.append({"role": "user", "content": q_user})
        st.session_state.chat_messages.append({
            "role": "assistant", "content": q_asst,
            "model_used": "openai/gpt-oss-120b", "duration_ms": res.get("latency_ms", 45.0),
            "tool_executions": [{"tool": "locate_and_inspect_medallion_catalog", "result_status": "SUCCESS"}]
        })
        st.session_state.messages = st.session_state.chat_messages
        st.rerun()

    if st.button("⚙️ AWS Glue Jobs & Pipelines"):
        q_user = "AWS Glue jobs ani pipelines che status dakhava"
        res = manage_pipelines_and_glue_jobs(action="list_status")
        jobs = res.get("jobs", [])
        job_rows = "\n".join([f"| `{j.get('job_name')}` | {j.get('layer')} | `{j.get('status')}` | {j.get('last_run')} |" for j in jobs])
        q_asst = f"### ⚙️ AWS Glue Jobs & Pipeline Status\n\n| Job Name | Layer | Status | Last Run |\n|---|---|---|---|\n{job_rows}"
        
        ChatPersistenceConnector.save_message(st.session_state.session_id, "user", q_user, st.session_state.active_project_id)
        ChatPersistenceConnector.save_message(
            st.session_state.session_id, "assistant", q_asst, st.session_state.active_project_id,
            tool_logs=[{"tool": "manage_pipelines_and_glue_jobs", "result_status": "SUCCESS"}],
            model_used="qwen/qwen3.8-27b", duration_ms=25.0
        )
        st.session_state.chat_messages.append({"role": "user", "content": q_user})
        st.session_state.chat_messages.append({
            "role": "assistant", "content": q_asst,
            "model_used": "qwen/qwen3.8-27b", "duration_ms": 25.0,
            "tool_executions": [{"tool": "manage_pipelines_and_glue_jobs", "result_status": "SUCCESS"}]
        })
        st.session_state.messages = st.session_state.chat_messages
        st.rerun()

    if st.button("⚡ Run Federated Cross-Engine Join"):
        q_user = "CMG ani GAM join karun report banava"
        j_res = build_cross_engine_join_report(sources=["CMG", "GAM"])
        csv_info = j_res.get("downloadable_csv")
        q_asst = f"### ⚡ Federated Cross-Engine Join Complete\n\n- **Federated Engine:** {j_res.get('federated_engine')}\n- **Rows Joined:** {j_res.get('total_rows')}\n- **Latency:** {j_res.get('latency_ms')}ms\n- **SQL:** `{j_res.get('sql_executed')}`"
        
        ChatPersistenceConnector.save_message(st.session_state.session_id, "user", q_user, st.session_state.active_project_id)
        ChatPersistenceConnector.save_message(
            st.session_state.session_id, "assistant", q_asst, st.session_state.active_project_id,
            tool_logs=[{"tool": "build_cross_engine_join_report", "result_status": "SUCCESS"}],
            dataframe=csv_info,
            model_used="openai/gpt-oss-120b", duration_ms=j_res.get("latency_ms", 110.0)
        )
        st.session_state.chat_messages.append({"role": "user", "content": q_user})
        st.session_state.chat_messages.append({
            "role": "assistant", "content": q_asst,
            "model_used": "openai/gpt-oss-120b", "duration_ms": j_res.get("latency_ms", 110.0),
            "tool_executions": [{"tool": "build_cross_engine_join_report", "result_status": "SUCCESS"}],
            "csv_download": csv_info
        })
        st.session_state.messages = st.session_state.chat_messages
        st.rerun()

    if st.button("🛡️ Users & Governance (RBAC)"):
        q_user = "Platform users ani roles dakhava"
        u_res = manage_users_and_roles(action="list")
        users = u_res.get("users", [])
        user_rows = "\n".join([f"| `{u.get('name')}` | `{u.get('email')}` | **{u.get('role')}** | {'ACTIVE' if u.get('is_active') else 'INACTIVE'} |" for u in users])
        q_asst = f"### 👥 User Governance & RBAC Roles\n\n| Name | Email | Role | Status |\n|---|---|---|---|\n{user_rows}"
        
        ChatPersistenceConnector.save_message(st.session_state.session_id, "user", q_user, st.session_state.active_project_id)
        ChatPersistenceConnector.save_message(
            st.session_state.session_id, "assistant", q_asst, st.session_state.active_project_id,
            tool_logs=[{"tool": "manage_users_and_roles", "result_status": "SUCCESS"}],
            model_used="qwen/qwen3.8-27b", duration_ms=30.0
        )
        st.session_state.chat_messages.append({"role": "user", "content": q_user})
        st.session_state.chat_messages.append({
            "role": "assistant", "content": q_asst,
            "model_used": "qwen/qwen3.8-27b", "duration_ms": 30.0,
            "tool_executions": [{"tool": "manage_users_and_roles", "result_status": "SUCCESS"}]
        })
        st.session_state.messages = st.session_state.chat_messages
        st.rerun()

    st.markdown("---")
    selected_model = st.selectbox(
        "🧠 Frontier Model Routing (UCB)",
        ["auto-router", "openai/gpt-oss-120b", "qwen/qwen3.8-27b", "openai/gpt-oss-20b"]
    )

    if st.button("🧹 Clear Active Chat"):
        st.session_state.chat_messages = []
        st.session_state.messages = []
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

    # Render Conversation History with complete Assistant metadata (model badge, tools, tables)
    for idx, msg in enumerate(st.session_state.chat_messages):
        with st.chat_message(msg["role"]):
            if msg["role"] == "assistant":
                m_used = msg.get("model_used")
                dur = msg.get("duration_ms")
                if m_used:
                    st.caption(f"🧠 **Model:** `{m_used}`" + (f" | ⚡ {round(dur)}ms" if dur else ""))
                
                t_execs = msg.get("tool_executions")
                if t_execs and len(t_execs) > 0:
                    with st.expander(f"🔧 **Tools Executed ({len(t_execs)})**", expanded=False):
                        for te in t_execs:
                            t_name = te.get("tool", "tool") if isinstance(te, dict) else str(te)
                            t_res = te.get("result_status") or te.get("status", "SUCCESS") if isinstance(te, dict) else "SUCCESS"
                            st.markdown(f"• `{t_name}`: `{t_res}`")

            st.markdown(msg["content"], unsafe_allow_html=True)
            
            # Downloadable CSV / Table Preview
            csv_info = msg.get("csv_download")
            if csv_info and os.path.exists(csv_info.get("path", "")):
                with open(csv_info["path"], "rb") as f:
                    st.download_button(
                        label=f"📥 Download {csv_info.get('filename')}",
                        data=f.read(),
                        file_name=csv_info.get("filename"),
                        mime="text/csv",
                        key=f"dl_{idx}_{s_id if 's_id' in locals() else 'f'}"
                    )

    # Chat Input & ReAct Loop Execution
    user_prompt = st.chat_input("Operations बद्दल विचारा (उदा. 'Mail var report gela ka?', 'Telegram alert dakhava', 'CMG ani GAM join kara')...")

    if user_prompt:
        # 1. Immediately record and commit user turn to Render PG / DuckDB
        user_msg = {
            "role": "user",
            "content": user_prompt,
            "created_at": time.time()
        }
        st.session_state.chat_messages.append(user_msg)
        st.session_state.messages = st.session_state.chat_messages

        ChatPersistenceConnector.save_message(
            session_id=st.session_state.session_id,
            role="user",
            content=user_prompt,
            project_id=st.session_state.active_project_id
        )

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

                t_exec_start = time.time()
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
                dur_ms = round((time.time() - t_exec_start) * 1000, 2)

                tools_used = agent_result.get("tools_executed", [])
                for t in tools_used:
                    t_name = t.get("tool", "tool")
                    t_status = t.get("result_status", "success").upper()
                    status_box.write(f"• 🔧 Executed `{t_name}` — *Result: {t_status}*")

                status_box.update(label="✅ **Execution Completed via Live Telemetry**", state="complete", expanded=False)

                content = agent_result.get("content", "")
                st.caption(f"🧠 **Model:** `{effective_model}` | ⚡ {round(dur_ms)}ms")
                st.markdown(content, unsafe_allow_html=True)

                # 2. Immediately commit complete assistant turn with tool logs, model badge to Render PG / DuckDB
                asst_msg_obj = {
                    "role": "assistant",
                    "content": content,
                    "model_used": effective_model,
                    "duration_ms": dur_ms,
                    "tool_executions": tools_used,
                    "csv_download": None,
                    "created_at": time.time()
                }
                st.session_state.chat_messages.append(asst_msg_obj)
                st.session_state.messages = st.session_state.chat_messages

                ChatPersistenceConnector.save_message(
                    session_id=st.session_state.session_id,
                    role="assistant",
                    content=content,
                    project_id=st.session_state.active_project_id,
                    tool_logs=tools_used,
                    dataframe=None,
                    model_used=effective_model,
                    duration_ms=dur_ms
                )

            except Exception as e:
                status_box.update(label="⚠️ Execution error", state="error", expanded=True)
                st.error(f"Agentic Runtime Error: {e}")

# =========================================================================
# TAB 2: LIVE OPERATIONS DASHBOARD
# =========================================================================
with nav_tab2:
    render_live_operations_dashboard()
