# -*- coding: utf-8 -*-
"""
Unified CLI Entry Point for NanoPro Operator.
Run with:
    python run_operator.py --ui                     # Launches Split-Screen Web Dashboard
    python run_operator.py --task "Book tickets"    # Headed CLI autonomous agent
    python run_operator.py --devin "Build a CRM"    # Autonomous full-stack dev engine
"""

import sys
import os
import argparse
import asyncio
import subprocess
from pathlib import Path

# Add root directory to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from nanopro_operator.config import DEFAULT_MODEL
from nanopro_operator.core.controller import GUIController
from nanopro_operator.core.vision_agent import VisionAgent
from nanopro_operator.core.self_healing_engine import SelfHealingLoop
from nanopro_operator.devin_engine.autonomous_dev_loop import AutonomousDevLoop


def launch_streamlit_ui(port: int = 8501) -> None:
    """Launches the Streamlit split-screen UI."""
    app_path = Path(__file__).parent / "ui" / "app.py"
    cmd = [
        sys.executable,
        "-m", "streamlit", "run",
        str(app_path),
        "--server.port", str(port),
        "--server.headless", "false"
    ]
    print(f"\n🚀 Launching NanoPro Operator Split-Screen Dashboard on http://localhost:{port} ...")
    subprocess.run(cmd)


async def run_cli_task(task: str, url: str = "https://www.google.com", model: str = DEFAULT_MODEL, headed: bool = True) -> None:
    """Executes an autonomous GUI task directly from terminal."""
    print(f"\n🧠 [NanoPro Operator] Initializing Autonomous Agent...")
    print(f"🎯 Target Goal: {task}")
    print(f"🤖 Vision Model: {model}")
    print(f"🌐 Initial URL: {url}")
    print(f"🖥️ Mode: {'Headed (Visible Chromium Window)' if headed else 'Headless'}\n")

    controller = GUIController(mode="playwright")
    await controller.initialize(headed=headed)

    vision_agent = VisionAgent(model=model)

    def print_event(e: dict):
        etype = e.get("type")
        if etype == "thought":
            print(f"\n[Step {e.get('step')}] 🧠 Thought: {e.get('thought')}")
            print(f"               ⚡ Action:  {e.get('action')}")
        elif etype == "screen_update":
            print(f"               👁️ Screen:  {e.get('url')} ({e.get('element_count')} interactive targets)")
        elif etype == "error_detected":
            print(f"               ⚠️ Recovery: Critic detected error ({e.get('error')}) -> Triggering self-healing...")
        elif etype == "complete":
            print(f"\n🎉 [COMPLETE] {e.get('summary')}")

    loop = SelfHealingLoop(
        controller=controller,
        vision_agent=vision_agent,
        event_callback=print_event
    )

    try:
        res = await loop.run(task=task, start_url=url)
        print("\n" + "="*60)
        print(f"RESULT: {res.get('status').upper()}")
        print(f"SUMMARY: {res.get('summary')}")
        print("="*60 + "\n")
    finally:
        await controller.close()


async def run_devin_task(prompt: str, model: str = DEFAULT_MODEL) -> None:
    """Executes Devin autonomous full-stack development task from terminal."""
    print(f"\n💻 [NanoPro Devin Engine] Initializing Autonomous Full-Stack Dev Engine...")
    print(f"📝 App Specification: {prompt}")

    controller = GUIController(mode="playwright")
    await controller.initialize(headed=True)

    vision_agent = VisionAgent(model=model)

    def print_dev_event(e: dict):
        etype = e.get("type")
        if etype == "devin_phase":
            print(f"\n🔄 [Devin Phase] {e.get('phase')}: {e.get('message')}")
        elif etype == "file_written":
            print(f"   📄 Wrote: {e.get('file')} ({e.get('bytes')} bytes)")
        elif etype == "server_ready":
            print(f"   🚀 Local Server Running: {e.get('url')}")
        elif etype == "thought":
            print(f"   🧠 Verification: {e.get('thought')[:100]}...")

    dev_loop = AutonomousDevLoop(
        controller=controller,
        vision_agent=vision_agent,
        event_callback=print_dev_event
    )

    try:
        res = await dev_loop.build_and_test_live(prompt)
        print("\n" + "="*60)
        print(f"DEVIN BUILD COMPLETE!")
        print(f"Live App URL: {res.get('server_url')}")
        print(f"Files Generated: {', '.join(res.get('files', []))}")
        print("="*60 + "\n")
    finally:
        dev_loop.cleanup()
        await controller.close()


def main():
    parser = argparse.ArgumentParser(description="NanoPro Operator: Autonomous Computer-Use AI Agent & Devin Engine")
    parser.add_argument("--ui", action="store_true", help="Launch interactive split-screen Streamlit dashboard")
    parser.add_argument("--port", type=int, default=8501, help="Port for the Streamlit dashboard")
    parser.add_argument("--task", type=str, help="Autonomous GUI task goal")
    parser.add_argument("--url", type=str, default="https://www.google.com", help="Starting URL for GUI task")
    parser.add_argument("--devin", type=str, help="Autonomous Devin coding prompt")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="Vision-Language Model to route through")
    parser.add_argument("--headless", action="store_true", help="Run Playwright in headless mode")

    args = parser.parse_args()

    if args.ui or (not args.task and not args.devin):
        launch_streamlit_ui(port=args.port)
    elif args.devin:
        asyncio.run(run_devin_task(prompt=args.devin, model=args.model))
    elif args.task:
        asyncio.run(run_cli_task(task=args.task, url=args.url, model=args.model, headed=not args.headless))


if __name__ == "__main__":
    main()
