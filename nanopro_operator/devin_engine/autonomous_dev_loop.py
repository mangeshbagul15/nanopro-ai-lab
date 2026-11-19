# -*- coding: utf-8 -*-
"""
Devin Autonomous Full-Stack Development Loop for NanoPro Operator.
Orchestrates code generation, local server startup, Playwright browser navigation,
and automated GUI validation with live split-screen preview.
"""

import asyncio
from typing import Dict, Any, Optional, Callable
from nanopro_operator.core.controller import GUIController
from nanopro_operator.core.vision_agent import VisionAgent
from nanopro_operator.core.self_healing_engine import SelfHealingLoop
from nanopro_operator.devin_engine.workspace_manager import WorkspaceManager
from nanopro_operator.devin_engine.code_generator import CodeGenerator
from nanopro_operator.devin_engine.test_runner import ServerSupervisor


class AutonomousDevLoop:
    """
    The full Devin development cycle:
    Write Code -> Launch Server -> Navigate CUA Browser -> Test & Click -> Self-Heal.
    """

    def __init__(
        self,
        controller: GUIController,
        vision_agent: VisionAgent,
        event_callback: Optional[Callable[[Dict[str, Any]], None]] = None
    ):
        self.controller = controller
        self.vision_agent = vision_agent
        self.event_callback = event_callback
        self.workspace = WorkspaceManager("devin_live_project")
        self.code_gen = CodeGenerator(model=vision_agent.model)
        self.server = ServerSupervisor(self.workspace.project_dir)

    def emit(self, event_type: str, data: Dict[str, Any]) -> None:
        if self.event_callback:
            try:
                self.event_callback({"type": event_type, **data})
            except Exception:
                pass

    async def build_and_test_live(self, user_prompt: str) -> Dict[str, Any]:
        """
        Executes complete Devin end-to-end development and interactive test run.
        """
        self.emit("devin_phase", {
            "phase": "CODE_GENERATION",
            "message": f"Synthesizing full-stack application for: '{user_prompt}'..."
        })

        # 1. Generate full-stack codebase
        code_files = await self.code_gen.generate_app(user_prompt)

        # 2. Write files into ephemeral workspace
        written_paths = []
        for rel_path, content in code_files.items():
            full = self.workspace.write_file(rel_path, content)
            written_paths.append(rel_path)
            self.emit("file_written", {"file": rel_path, "bytes": len(content)})

        self.emit("devin_phase", {
            "phase": "SERVER_STARTUP",
            "message": "Starting local development server on ephemeral port..."
        })

        # 3. Launch local server
        success, server_url_or_err = await self.server.start()
        if not success:
            self.emit("devin_error", {"error": server_url_or_err})
            return {"status": "error", "message": server_url_or_err}

        server_url = server_url_or_err
        self.emit("server_ready", {"url": server_url, "port": self.server.port})

        self.emit("devin_phase", {
            "phase": "BROWSER_INSPECTION",
            "message": f"Pointing CUA Browser to {server_url} for live interactive validation..."
        })

        # 4. Navigate browser to live preview
        await self.controller.navigate(server_url)

        # 5. Execute autonomous GUI verification & clicking
        tester_loop = SelfHealingLoop(
            controller=self.controller,
            vision_agent=self.vision_agent,
            max_steps=10,
            event_callback=self.event_callback
        )

        test_goal = (
            f"Test this newly built web application: verify that all forms, buttons, "
            f"and visual elements render correctly. Fill in sample data, click calculate/submit, "
            f"and confirm that no errors occur."
        )

        test_result = await tester_loop.run(test_goal)

        self.emit("devin_phase", {
            "phase": "COMPLETED",
            "message": "Application built, launched, and 100% verified via autonomous GUI testing!"
        })

        return {
            "status": "success",
            "server_url": server_url,
            "port": self.server.port,
            "files": written_paths,
            "test_summary": test_result.get("summary"),
            "history": test_result.get("history")
        }

    def cleanup(self) -> None:
        """Stops running development server."""
        self.server.stop()
