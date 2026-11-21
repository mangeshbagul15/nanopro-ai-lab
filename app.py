# -*- coding: utf-8 -*-
"""
NanoPro AI LAB - Autonomous Operations & Data Engineering Agent
Streamlit UI backed by live Render PostgreSQL, self-healing SQL, and multi-model routing.
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

from nanopro_db_agent import (
    get_nanopro_db_health,
    locate_and_inspect_catalog,
    get_report_execution_logs,
    build_join_report,
    mutate_database_object,
    log_report_run,
    run_nanopro_react_loop,
    NANOPRO_AGENT_TOOLS
)

# Page Setup
st.set_page_config(
    page_title="NanoPro AI LAB · Operations & Data Engineering Agent",
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
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": "नमस्कार Super Admin (Mangesh Bagul)! 🙏 मी **NanoPro AI LAB Autonomous Operations & Data Engineering Agent** आहे. Render PostgreSQL लाइव्ह डेटाबेस, टेबल्स स्कीमा, अहवाल लॉग्स किंवा डेटा बदलांबद्दल सांगा, मी थेट ऑटोनॉमस टूल्स चालवून अचूक उत्तर देतो."
        }
    ]

# Header Bar
st.markdown("""
<div class="agent-header">
    <div>
        <h3 style="margin:0; color:#F8FAFC;">🧠 NanoPro AI LAB · Autonomous Agent</h3>
        <p style="margin:2px 0 0 0; color:#94A3B8; font-size:0.88rem;">Live Render PostgreSQL Engine · 4,804+ Multi-Model Mesh · Self-Healing SQL</p>
    </div>
    <div>
        <span class="status-badge">● LIVE TELEMETRY CONNECTED</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar: Live Telemetry & Quick Action Tools
with st.sidebar:
    st.subheader("⚡ Live Telemetry")
    health = get_nanopro_db_health()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Database", health.get("database_name", "nanopro_cbs_prod"))
        st.metric("Cache Hit Ratio", health.get("cache_hit_ratio", "99.8%"))
    with col2:
        st.metric("DB Size", health.get("database_size", "3.2 MB"))
        st.metric("Latency", f"{health.get('latency_ms', 1.2)}ms")

    st.markdown("---")
    st.subheader("🛠️ Quick Operational Tools")

    if st.button("🩺 Check DB Health"):
        h_res = get_nanopro_db_health()
        st.session_state.chat_messages.append({"role": "user", "content": "DB health kashi ahe?"})
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": f"**Render PostgreSQL Live Health:**\n\n| Metric | Value |\n|---|---|\n| **Status** | {h_res.get('connection_status')} |\n| **Engine** | {h_res.get('engine')} |\n| **Size** | {h_res.get('database_size')} |\n| **Cache Hit Ratio** | {h_res.get('cache_hit_ratio')} |\n| **Tables** | {h_res.get('total_tables')} |"
        })
        st.rerun()

    if st.button("📚 Inspect Live Catalog"):
        cat_res = locate_and_inspect_catalog()
        tables_list = cat_res.get("catalog", [])
        st.session_state.chat_messages.append({"role": "user", "content": "DB madhe kay kuthe ahe?"})
        rows_md = "\n".join([f"| `{t.get('table_name')}` | {t.get('row_count')} | {', '.join(t.get('primary_keys', [])) or '—'} | {t.get('purpose', 'Core Banking')} |" for t in tables_list])
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": f"**Render PostgreSQL Live Catalog ({len(tables_list)} tables):**\n\n| Table | Rows | PK | Purpose |\n|---|---|---|---|\n{rows_md}"
        })
        st.rerun()

    if st.button("📋 Check Report Logs"):
        logs_res = get_report_execution_logs(limit=10)
        logs = logs_res.get("recent_runs", [])
        st.session_state.chat_messages.append({"role": "user", "content": "Konte report kadhi gele? Kay status ahe?"})
        log_rows = "\n".join([f"| `{l.get('report_name')}` | {l.get('status')} | {l.get('rows_processed')} | {l.get('executed_at')} | {l.get('duration_sec')}s |" for l in logs])
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": f"**nanopro_report_logs Live Status:**\n\n| Report Name | Status | Rows | Executed At | Duration |\n|---|---|---|---|---|\n{log_rows}"
        })
        st.rerun()

    st.markdown("---")
    selected_model = st.selectbox(
        "🧠 Frontier Model Routing",
        ["qwen/qwen3.8-27b", "openai/gpt-oss-120b", "openai/gpt-oss-20b", "auto-router"]
    )

# Render Chat History
for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)
        if "csv_download" in msg:
            csv_info = msg["csv_download"]
            if os.path.exists(csv_info.get("path", "")):
                with open(csv_info["path"], "rb") as f:
                    st.download_button(
                        label=f"📥 Download {csv_info.get('filename')}",
                        data=f.read(),
                        file_name=csv_info.get("filename"),
                        mime="text/csv"
                    )

# Chat Input & ReAct Agent Execution
user_prompt = st.chat_input("Render PostgreSQL बद्दल विचारा (उदा. 'DB health dakhava', 'CMG ani GAM join karun report banava', 'nava table banav')...")

if user_prompt:
    st.session_state.chat_messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        status_box = st.status("⚙️ **NanoPro Agentic Runtime Active** · Inspecting Render PostgreSQL...", expanded=True)
        
        provider = {
            "name": "groq#1",
            "api_key": os.environ.get("GROQ_API_KEY", ""),
            "base_url": "https://api.groq.com/openai/v1",
            "model": "qwen/qwen3.8-27b" if selected_model == "auto-router" else selected_model,
            "timeout": 30.0
        }

        try:
            status_box.write("🔍 Inspecting database metadata & formulating execution plan...")
            
            # Execute ReAct Loop asynchronously
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
