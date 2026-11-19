# -*- coding: utf-8 -*-
"""
Workspace Manager for NanoPro Operator Devin Engine.
Manages ephemeral project environments, file creation, editing, and tree exploration.
"""

import os
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional
from nanopro_operator.config import WORKSPACES_DIR


class WorkspaceManager:
    """
    Manages isolated project directories for autonomous full-stack development.
    """

    def __init__(self, project_name: str = "default_devin_project"):
        self.project_name = project_name
        self.project_dir: Path = WORKSPACES_DIR / project_name
        self.project_dir.mkdir(parents=True, exist_ok=True)

    def write_file(self, rel_path: str, content: str) -> str:
        """Writes or overwrites a project file."""
        target = self.project_dir / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(content)
        return str(target)

    def read_file(self, rel_path: str) -> Optional[str]:
        """Reads a project file content."""
        target = self.project_dir / rel_path
        if not target.exists():
            return None
        with open(target, "r", encoding="utf-8") as f:
            return f.read()

    def list_files(self) -> List[Dict[str, Any]]:
        """Returns recursive file tree list."""
        file_tree = []
        for root, dirs, files in os.walk(self.project_dir):
            for file in files:
                full_path = Path(root) / file
                rel_path = full_path.relative_to(self.project_dir)
                file_tree.append({
                    "path": str(rel_path).replace("\\", "/"),
                    "size": full_path.stat().st_size,
                    "extension": full_path.suffix
                })
        return file_tree

    def clean(self) -> None:
        """Cleans up workspace directory."""
        if self.project_dir.exists():
            shutil.rmtree(self.project_dir)
            self.project_dir.mkdir(parents=True, exist_ok=True)
