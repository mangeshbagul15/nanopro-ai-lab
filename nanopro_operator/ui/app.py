# -*- coding: utf-8 -*-
"""
Production Split-Screen Dashboard UI for NanoPro Operator.
Left Panel: Chat, Task Input, Live Thought-Action Reasoning, Model Selector, Vault.
Right Panel: Real-time Screen Share with Set-of-Marks, Laser Cursor, and Devin Live Web Preview.
"""

import os
import sys
import time
import asyncio
from pathlib import Path
import streamlit as st
from PIL import Image

# Ensure package root is in sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from nanopro_operator.config import (
    VISION_MODELS_CATALOG,
    DEFAULT_MODEL,
    SCREENSHOTS_DIR,
    OLLAMA_BASE_URL
)
from nanopro_operator.core.controller import GUIController
from nanopro_operator.core.vision_agent import VisionAgent
from nanopro_operator.core.self_healing_engine import SelfHealingLoop
from nanopro_operator.core.credential_vault import vault
from nanopro_operator.core.safety_guardrails import safety_guard
from nanopro_operator.devin_engine.autonomous_dev_loop import AutonomousDevLoop

# Streamlit Page Setup
st.set_page_config(
    page_title="NanoPro Operator · Autonomous CUA & Devin Engine",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom High-Tech Eye-Comfort Dark Theme CSS
st.markdown("""
<style>
    /* Dark Theme Base */
    .stApp { background-color: #0B0F19; color: #E2E8F0; }
    .css-1d391kg, .css-12oz5g7 { padding: 1rem 2rem; }
    
    /* Topbar Header Card */
    .operator-header {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.12), rgba(56, 189, 248, 0.08));
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 12px;
        padding: 12px 20px;
        margin-bottom: 18px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    /* Panel Cards */
    .cockpit-card {
        background: #111827;
        border: 1px solid #1F2937;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 14px;
    }
    
    /* Live Status Badge */
    .badge-live {
        background: rgba(16, 185, 129, 0.2);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
    }
    
    /* Reasoning Step Pill */
    .step-pill {
        background: #1E293B;
        border-left: 3px solid #38BDF8;
        padding: 8px 12px;
        border-radius: 6px;
        margin-bottom: 8px;
        font-size: 12px;
    }
    
    /* Safety Alert Box */
    .safety-alert {
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid rgba(239, 68, 68, 0.4);
        color: #F87171;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)


# Session State Initialization
if "timeline" not in st.session_state:
    st.session_state.timeline = []
if "running" not in st.session_state:
    st.session_state.running = False
if "latest_screenshot" not in st.session_state:
    st.session_state.latest_screenshot = None
if "live_server_url" not in st.session_state:
    st.session_state.live_server_url = None
if "pending_confirmation" not in st.session_state:
    st.session_state.pending_confirmation = None


# Header
st.markdown("""
<div class="operator-header">
    <div style="display:flex;align-items:center;gap:12px;">
        <span style="font-size:28px;">🧠</span>
        <div>
            <div style="font-size:18px;font-weight:800;color:#F8FAFC;">NanoPro Operator — Autonomous GUI &amp; Devin Engine</div>
            <div style="font-size:12px;color:#94A3B8;">4,804+ Frontier Models Mesh • Playwright &amp; PyAutoGUI Hybrid • Self-Healing VLM Loop</div>
        </div>
    </div>
    <div style="display:flex;gap:8px;align-items:center;">
        <span class="badge-live">● ENGINE ARMED</span>
    </div>
</div>
""", unsafe_allow_html=True)


# Split-Screen Layout (Left: Cockpit, Right: Live Stream)
col_left, col_right = st.columns([1, 1], gap="medium")


# -----------------------------------------------------------------
# LEFT PANEL: CHAT, TASK INPUT, REASONING, VAULT, GUARDRAILS
# -----------------------------------------------------------------
with col_left:
    st.markdown("### 🎛️ Autonomous Control Cockpit")

    # Mode Selector
    mode = st.radio(
        "Operating Mode",
        ["🌐 Autonomous CUA Browser Agent", "💻 Devin Full-Stack Web Development"],
        horizontal=True
    )

    # Model Selector
    model_keys = list(VISION_MODELS_CATALOG.keys())
    selected_model = st.selectbox(
        "Vision-Language Model (VLM)",
        model_keys,
        format_func=lambda k: VISION_MODELS_CATALOG[k]["name"],
        index=0
    )

    # Task Input
    default_prompt = (
        "Open banking portal, fill customer KYC form with 'Mangesh Bagul', "
        "and calculate 5-year Fixed Deposit return for ₹500,000 at 7.5% interest."
        if "Browser" in mode else
        "Build a modern Core Banking Fixed Deposit Calculator with animated interest charts and customer account application form."
    )

    task_input = st.text_area(
        "Task / Goal Prompt",
        value=default_prompt,
        height=95,
        help="Specify the objective for the autonomous GUI agent or Devin coding engine."
    )

    start_url = st.text_input(
        "Initial URL (Optional)",
        value="about:blank" if "Devin" in mode else "https://www.google.com"
    )

    # Action Buttons
    c_btn1, c_btn2 = st.columns([1, 1])
    with c_btn1:
        run_btn = st.button("🚀 Dispatch Autonomous Agent", use_container_width=True, type="primary")
    with c_btn2:
        stop_btn = st.button("⏹️ Emergency Stop", use_container_width=True)

    if stop_btn:
        st.session_state.running = False
        st.warning("Execution stopped by user.")

    # Human-in-the-Loop Safety Confirmation Banner
    if st.session_state.pending_confirmation:
        conf = st.session_state.pending_confirmation
        st.markdown(f"""
        <div class="safety-alert">
            <strong>⚠️ HUMAN CONFIRMATION REQUIRED</strong><br>
            <strong>Category:</strong> {conf.get('category')}<br>
            <strong>Reason:</strong> {conf.get('reason')}<br>
            Action requires explicit authorization before proceeding.
        </div>
        """, unsafe_allow_html=True)
        col_appr, col_rej = st.columns(2)
        with col_appr:
            if st.button("✅ Authorize Action", key="btn_auth", use_container_width=True):
                safety_guard.resolve(conf["token"], approved=True)
                st.session_state.pending_confirmation = None
                st.rerun()
        with col_rej:
            if st.button("❌ Deny & Abort", key="btn_deny", use_container_width=True):
                safety_guard.resolve(conf["token"], approved=False)
                st.session_state.pending_confirmation = None
                st.rerun()

    # Step-by-Step Thought -> Action -> Observation Timeline
    st.markdown("#### 📜 Live Reasoning Timeline (Thought ➔ Action ➔ Observation)")
    timeline_box = st.container(height=320)
    with timeline_box:
        if not st.session_state.timeline:
            st.info("Agent standing by. Enter a goal and click 'Dispatch Autonomous Agent'.")
        else:
            for item in st.session_state.timeline[-15:]:
                st.markdown(f"""
                <div class="step-pill">
                    <strong>Step {item.get('step', 1)}:</strong> {item.get('thought', '')}<br>
                    <span style="color:#10B981;">⚡ Action:</span> <code>{item.get('action', '')}</code><br>
                    <span style="color:#94A3B8;">👁️ Observation:</span> {item.get('observation', '')}
                </div>
                """, unsafe_allow_html=True)

    # Credential Vault Expander
    with st.expander("🔐 Credential & File Vault (AES-256 Encrypted)"):
        st.caption("Securely stores passwords and tokens for automated login without plain-text exposure.")
        stored_services = vault.list_services()
        st.write("Stored Services:", stored_services if stored_services else "(Vault empty)")
        v_col1, v_col2 = st.columns(2)
        with v_col1:
            v_service = st.text_input("Service Name", "bank_portal", key="v_svc")
            v_user = st.text_input("Username / Email", "mangesh@nanopro.ai", key="v_usr")
        with v_col2:
            v_pwd = st.text_input("Password", type="password", key="v_pwd")
            if st.button("Save Credential to Vault", key="v_save"):
                vault.set_secret(v_service, v_user, v_pwd)
                st.success(f"Saved credential for '{v_service}' to encrypted vault!")


# -----------------------------------------------------------------
# RIGHT PANEL: LIVE SCREEN SHARE, SET-OF-MARKS, DEV PREVIEW
# -----------------------------------------------------------------
with col_right:
    st.markdown("### 🖥️ Live Browser Stream & Devin Preview")

    preview_tabs = st.tabs(["👁️ Live Screen Share (Set-of-Marks)", "🌐 Live Web App Preview", "💻 Codebase Tree"])

    with preview_tabs[0]:
        st.caption("Real-time browser stream with Set-of-Marks grounding and laser mouse cursor.")
        screen_placeholder = st.empty()
        current_screen_path = SCREENSHOTS_DIR / "current_screen.jpg"
        if current_screen_path.exists():
            screen_placeholder.image(str(current_screen_path), use_column_width=True)
        else:
            screen_placeholder.markdown("""
            <div style="height:420px;background:#030712;border:1px dashed #374151;border-radius:10px;display:flex;align-items:center;justify-content:center;color:#6B7280;">
                🖥️ Browser stream will appear here upon dispatch
            </div>
            """, unsafe_allow_html=True)

    with preview_tabs[1]:
        st.caption("Interactive preview of the application built by Devin.")
        if st.session_state.live_server_url:
            st.markdown(f"**Target URL:** `{st.session_state.live_server_url}`")
            st.components.v1.iframe(st.session_state.live_server_url, height=500, scrolling=True)
        else:
            st.info("Run Devin mode to launch and view the interactive web application live.")

    with preview_tabs[2]:
        st.caption("Workspace project files generated by the autonomous agent.")
        from nanopro_operator.devin_engine.workspace_manager import WorkspaceManager
        ws = WorkspaceManager("devin_live_project")
        files = ws.list_files()
        if files:
            for f in files:
                st.text(f"📄 {f['path']} ({f['size']} bytes)")
        else:
            st.info("No generated files in workspace yet.")


# -----------------------------------------------------------------
# EXECUTION ORCHESTRATION HANDLER
# -----------------------------------------------------------------
if run_btn and task_input:
    st.session_state.running = True
    st.session_state.timeline = []

    controller = GUIController(mode="playwright")
    vision_agent = VisionAgent(model=selected_model)

    def event_stream_listener(event: dict):
        etype = event.get("type")
        if etype == "thought":
            st.session_state.timeline.append({
                "step": event.get("step"),
                "thought": event.get("thought"),
                "action": str(event.get("action")),
                "observation": "Executing..."
            })
        elif etype == "screen_update":
            p = event.get("screenshot_path")
            if p and os.path.exists(p):
                screen_placeholder.image(p, use_column_width=True)
        elif etype == "server_ready":
            st.session_state.live_server_url = event.get("url")
        elif etype == "human_confirmation_needed":
            st.session_state.pending_confirmation = event.get("confirmation")

    async def execute_task():
        await controller.initialize(headed=False)
        try:
            if "Devin" in mode:
                dev_loop = AutonomousDevLoop(
                    controller=controller,
                    vision_agent=vision_agent,
                    event_callback=event_stream_listener
                )
                res = await dev_loop.build_and_test_live(task_input)
                st.success(f"🎉 Devin Build Completed: {res.get('test_summary')}")
            else:
                loop = SelfHealingLoop(
                    controller=controller,
                    vision_agent=vision_agent,
                    event_callback=event_stream_listener
                )
                res = await loop.run(task=task_input, start_url=start_url if start_url != "about:blank" else None)
                st.success(f"🎉 Task Completed: {res.get('summary')}")
        finally:
            await controller.close()

    with st.spinner("🤖 Autonomous Agent Executing Task..."):
        asyncio.run(execute_task())
        st.session_state.running = False
        st.rerun()
