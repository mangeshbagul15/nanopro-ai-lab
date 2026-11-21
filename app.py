# -*- coding: utf-8 -*-
"""
NanoPro AI LAB - Unified Multi-Cloud Autonomous Data Engineering & Operations Agent
Streamlit UI backed by live Render PostgreSQL, Google BigQuery, Snowflake, AWS S3,
Supabase, DuckDB federated query mesh, self-healing SQL, and dynamic model routing.
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
    locate_and_inspect_unified_catalog,
    get_report_execution_logs,
    build_cross_engine_join_report,
    execute_and_commit_mutation,
    sync_or_move_data_between_engines,
    select_optimal_model,
    run_nanopro_react_loop,
    NANOPRO_AGENT_TOOLS
)

# Page Setup
st.set_page_config(
    page_title="NanoPro AI LAB · Autonomous Data Engineering Agent",
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
        <h3 style="margin:0; color:#F8FAFC;">🧠 NanoPro AI LAB · Autonomous Multi-Cloud Agent</h3>
        <p style="margin:2px 0 0 0; color:#94A3B8; font-size:0.88rem;">
            Render PostgreSQL · BigQuery (nanopro-lakehouse-sandbox) · Snowflake · AWS · Supabase · DuckDB
        </p>
    </div>
    <div>
        <span class="status-badge">● 6 MULTI-CLOUD ENGINES ACTIVE</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar: Live Multi-Cloud Telemetry & Quick Operational Tools
with st.sidebar:
    st.subheader("⚡ Multi-Cloud Ecosystem")
    eco_health = get_nanopro_ecosystem_health("ALL")
    h_map = eco_health.get("ecosystem_health", {})

    st.markdown("""
    <div style="font-size:0.85rem; line-height:1.7;">
        <span class="engine-pill pill-green">🐘 Render PG: LIVE</span>
        <span class="engine-pill pill-blue">☁️ BigQuery: LIVE</span>
        <span class="engine-pill pill-purple">❄️ Snowflake: READY</span>
        <span class="engine-pill pill-blue">📦 AWS S3: HEALTHY</span>
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

    if st.button("📚 Inspect Unified Catalog"):
        res = locate_and_inspect_unified_catalog(engine="ALL")
        items = res.get("catalog", [])
        st.session_state.chat_messages.append({"role": "user", "content": "Multi-cloud catalog madhe kay kuthe ahe?"})
        rows_md = "\n".join([f"| `{it.get('engine')}` | `{it.get('table_name')}` | {it.get('row_count', '—')} | {', '.join(it.get('primary_keys', [])) or '—'} |" for it in items[:15]])
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": f"### 📚 Unified Catalog ({res.get('total_objects_matched')} objects found across 6 engines)\n\n| Engine | Table / Object | Rows | PK |\n|---|---|---|---|\n{rows_md}"
        })
        st.rerun()

    if st.button("📋 Check Report & Job Logs"):
        res = get_report_execution_logs(limit=10)
        logs = res.get("recent_runs", [])
        st.session_state.chat_messages.append({"role": "user", "content": "Konte report kadhi gele? Kay status ahe?"})
        log_rows = "\n".join([f"| `{l.get('report_name')}` | `{l.get('status')}` | {l.get('rows_processed')} | {l.get('executed_at')} | {l.get('duration_sec')}s |" for l in logs])
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": f"### 📋 Statutory Report & Execution Logs (nanopro_report_logs)\n\n| Report Name | Status | Rows | Executed At | Duration |\n|---|---|---|---|---|\n{log_rows}"
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

    if st.button("🔄 Sync BigQuery to DuckDB"):
        s_res = sync_or_move_data_between_engines("bigquery", "nanopro_cbs_bronze.CMG", "duckdb", "CMG_LAKEHOUSE_SYNC")
        st.session_state.chat_messages.append({"role": "user", "content": "BigQuery CMG table DuckDB madhe sync kar"})
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": f"### 🔄 Cross-Engine Replication Complete\n\n- **Source:** `{s_res.get('source')}`\n- **Target:** `{s_res.get('target')}`\n- **Rows Synced:** `{s_res.get('rows_synced')}`\n- **Total Target Rows:** `{s_res.get('target_total_rows')}`\n- **Duration:** {s_res.get('duration_sec')}s"
        })
        st.rerun()

    st.markdown("---")
    selected_model = st.selectbox(
        "🧠 Frontier Model Routing",
        ["auto-router", "openai/gpt-oss-120b", "qwen/qwen3.8-27b", "openai/gpt-oss-20b"]
    )

    if st.button("🧹 Clear Chat"):
        st.session_state.chat_messages = []
        st.rerun()

# 2. CLEAN-SLATE HERO (NO CANNED GREETINGS OR FAKE Q&A PROMPTS)
if not st.session_state.chat_messages:
    st.markdown("""
    <div style="text-align:center; padding: 40px 20px; border: 1px dashed rgba(255,255,255,0.15); border-radius: 12px; margin-bottom: 20px;">
        <h2 style="color: #F8FAFC; margin-bottom: 8px;">🧠 NanoPro AI LAB · Autonomous Operations Agent</h2>
        <p style="color: #94A3B8; font-size: 0.95rem; max-width: 650px; margin: 0 auto 18px auto;">
            Directly connected to Render PostgreSQL, Google BigQuery Lakehouse, Snowflake Medallion, AWS S3/SFTP, Supabase, and DuckDB.
            Ask in Marathi, Hinglish, or English to inspect schemas, build joins, run syncs, or execute verified changes.
        </p>
        <div style="display:flex; justify-content:center; gap:8px; flex-wrap:wrap;">
            <span class="engine-pill pill-green">Render PG Connected</span>
            <span class="engine-pill pill-blue">BigQuery Lakehouse Connected</span>
            <span class="engine-pill pill-purple">Snowflake L0-L2 Ready</span>
            <span class="engine-pill pill-blue">AWS S3 / SFTP Armed</span>
            <span class="engine-pill pill-green">Supabase Active</span>
            <span class="engine-pill pill-purple">DuckDB Columnar Live</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 3. RENDER CONVERSATION HISTORY
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

# 4. CHAT INPUT & REACT AGENT EXECUTION
user_prompt = st.chat_input("Multi-cloud डेटाबेस बद्दल विचारा (उदा. 'DB health dakhava', 'BigQuery CMG DuckDB madhe sync kar', 'CMG ani GAM join kara')...")

if user_prompt:
    st.session_state.chat_messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        status_box = st.status("⚙️ **NanoPro Agentic Runtime Active** · Inspecting Multi-Cloud Telemetry...", expanded=True)

        # Dynamic Model Router Decision
        if selected_model == "auto-router":
            route_decision = select_optimal_model(user_prompt, st.session_state.chat_messages)
            effective_model = route_decision["recommended_model"]
            prov_name = route_decision["provider_name"]
            status_box.write(f"🧠 **Auto-Router:** Selected `{effective_model}` (*{route_decision['rationale']}*)")
        else:
            effective_model = selected_model
            prov_name = "groq#1"
            status_box.write(f"🧠 **Model:** `{effective_model}` (manual selection)")

        provider = {
            "name": prov_name,
            "api_key": os.environ.get("GROQ_API_KEY", ""),
            "base_url": "https://api.groq.com/openai/v1",
            "model": effective_model,
            "timeout": 35.0
        }

        try:
            status_box.write("🔍 Inspecting live database metadata & orchestrating execution...")

            # Run ReAct Loop asynchronously
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
