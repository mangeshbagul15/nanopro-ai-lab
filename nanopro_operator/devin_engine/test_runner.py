# -*- coding: utf-8 -*-
"""
Test Runner & Ephemeral Server Supervisor for NanoPro Operator Devin Engine.
Launches, monitors, and health-checks local web development servers on ephemeral ports.
"""

import sys
import socket
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from nanopro_operator.config import DEV_SERVER_PORT_RANGE


class ServerSupervisor:
    """
    Supervises local development web servers for live split-screen preview.
    """

    def __init__(self, workspace_path: Path):
        self.workspace_path = workspace_path
        self.process: Optional[subprocess.Popen] = None
        self.port: Optional[int] = None
        self.server_url: Optional[str] = None
        self.logs: list[str] = []

    def find_free_port(self) -> int:
        """Finds an unused port in the configured range."""
        start_port, end_port = DEV_SERVER_PORT_RANGE
        for p in range(start_port, end_port + 1):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex(("127.0.0.1", p)) != 0:
                    return p
        return 8085

    async def start(self, entrypoint_cmd: Optional[str] = None) -> Tuple[bool, str]:
        """
        Launches the local web server asynchronously.
        If no command provided, defaults to Python's built-in HTTP server or uvicorn.
        """
        self.port = self.find_free_port()
        self.server_url = f"http://127.0.0.1:{self.port}"

        # Detect tech stack in workspace
        has_fastapi = (self.workspace_path / "main.py").exists()
        has_streamlit = (self.workspace_path / "streamlit_app.py").exists()

        if entrypoint_cmd:
            cmd = entrypoint_cmd.replace("{PORT}", str(self.port))
        elif has_fastapi:
            cmd = f'"{sys.executable}" -m uvicorn main:app --host 127.0.0.1 --port {self.port}'
        elif has_streamlit:
            cmd = f'"{sys.executable}" -m streamlit run streamlit_app.py --server.port {self.port} --server.headless true'
        else:
            cmd = f'"{sys.executable}" -m http.server {self.port} --bind 127.0.0.1'

        try:
            self.process = subprocess.Popen(
                cmd,
                shell=True,
                cwd=str(self.workspace_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        except Exception as e:
            return False, f"Failed to spawn server process: {e}"

        # Health check poll loop (wait up to 8s for server readiness)
        for _ in range(16):
            await asyncio.sleep(0.5)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.3)
                if s.connect_ex(("127.0.0.1", self.port)) == 0:
                    return True, self.server_url

            # Check if process terminated early with error
            if self.process.poll() is not None:
                err = self.process.stderr.read() if self.process.stderr else "Unknown error"
                return False, f"Server exited prematurely: {err}"

        return True, self.server_url

    def stop(self) -> None:
        """Terminates server process tree."""
        if self.process:
            try:
                self.process.terminate()
                self.process.kill()
            except Exception:
                pass
            self.process = None
            self.port = None
            self.server_url = None
