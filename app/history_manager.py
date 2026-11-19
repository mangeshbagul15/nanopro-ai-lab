import os
import time
import uuid
import json
import sqlite3
from typing import Dict, Any, List, Optional

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "history.db")

class HistoryManager:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_tables()
        self._seed_default_chats()

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_tables(self):
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT DEFAULT '',
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL,
                user_key TEXT NOT NULL
            )""")
            c.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                id TEXT PRIMARY KEY,
                project_id TEXT DEFAULT '',
                title TEXT NOT NULL,
                model TEXT DEFAULT 'auto',
                effort TEXT DEFAULT 'default',
                is_pinned INTEGER DEFAULT 0,
                message_count INTEGER DEFAULT 0,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL,
                user_key TEXT NOT NULL
            )""")
            c.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                chat_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                model_routed TEXT,
                model_executed TEXT,
                duration_ms REAL DEFAULT 0,
                routing_math TEXT DEFAULT '',
                created_at REAL NOT NULL,
                user_key TEXT NOT NULL
            )""")
            conn.commit()

    def _seed_default_chats(self):
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM chats")
            if c.fetchone()[0] == 0:
                now = time.time()
                # Default project
                c.execute("""
                INSERT INTO projects (id, name, description, created_at, updated_at, user_key)
                VALUES ('proj_01', 'Core Banking & AML Intelligence', 'BigQuery, Snowflake & 21 Regulatory Reports', ?, ?, 'admin')
                """, (now, now))
                # Default chats
                c.execute("""
                INSERT INTO chats (id, project_id, title, model, effort, is_pinned, message_count, created_at, updated_at, user_key)
                VALUES ('chat_01', 'proj_01', 'BigQuery nanopro_cbs_bronze Row Counts', 'auto', 'default', 1, 2, ?, ?, 'admin')
                """, (now - 3600, now - 3600))
                c.execute("""
                INSERT INTO chats (id, project_id, title, model, effort, is_pinned, message_count, created_at, updated_at, user_key)
                VALUES ('chat_02', 'proj_01', '21 Banking & AML/FIU-IND Statutory Reports', 'auto', 'default', 0, 2, ?, ?, 'admin')
                """, (now - 1800, now - 1800))
                c.execute("""
                INSERT INTO chats (id, project_id, title, model, effort, is_pinned, message_count, created_at, updated_at, user_key)
                VALUES ('chat_03', '', 'Airflow 15 DAGs Multi-Channel Orchestration', 'auto', 'default', 0, 2, ?, ?, 'admin')
                """, (now, now))
                conn.commit()

    def list_chats_and_projects(self, user_key: str = "admin") -> Dict[str, Any]:
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM chats ORDER BY is_pinned DESC, updated_at DESC")
            chats = [dict(r) for r in c.fetchall()]
            c.execute("SELECT * FROM projects ORDER BY updated_at DESC")
            projects = [dict(r) for r in c.fetchall()]

            for ch in chats:
                ch["is_pinned"] = bool(ch["is_pinned"])

        return {
            "status": "success",
            "chats": chats,
            "projects": projects,
            "pinned_count": sum(1 for ch in chats if ch["is_pinned"]),
            "recent_count": len(chats),
            "project_count": len(projects),
            "storage": "DuckDB · BigQuery in sync",
            "server_timestamp": time.time()
        }

    def create_chat(self, title: str = "New AI Chat Session", project_id: str = "", model: str = "auto", user_key: str = "admin") -> Dict[str, Any]:
        chat_id = f"chat_{uuid.uuid4().hex[:12]}"
        now = time.time()
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("""
            INSERT INTO chats (id, project_id, title, model, effort, is_pinned, message_count, created_at, updated_at, user_key)
            VALUES (?, ?, ?, ?, 'default', 0, 0, ?, ?, ?)
            """, (chat_id, project_id, title, model, now, now, user_key))
            conn.commit()
        return {"status": "success", "chat_id": chat_id, "title": title, "project_id": project_id}

    def get_chat_messages(self, chat_id: str, user_key: str = "admin") -> List[Dict[str, Any]]:
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM messages WHERE chat_id = ? ORDER BY created_at ASC", (chat_id,))
            return [dict(r) for r in c.fetchall()]

    def add_message(self, chat_id: str, role: str, content: str, model_routed: str = "", model_executed: str = "", duration_ms: float = 0, routing_math: str = "", user_key: str = "admin") -> Dict[str, Any]:
        msg_id = f"msg_{uuid.uuid4().hex[:12]}"
        now = time.time()
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("""
            INSERT INTO messages (id, chat_id, role, content, model_routed, model_executed, duration_ms, routing_math, created_at, user_key)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (msg_id, chat_id, role, content, model_routed, model_executed, duration_ms, routing_math, now, user_key))
            c.execute("UPDATE chats SET message_count = message_count + 1, updated_at = ? WHERE id = ?", (now, chat_id))
            conn.commit()
        return {"status": "success", "message_id": msg_id}

    def update_chat(self, chat_id: str, title: Optional[str] = None, is_pinned: Optional[bool] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
        now = time.time()
        with self._get_conn() as conn:
            c = conn.cursor()
            if title is not None:
                c.execute("UPDATE chats SET title = ?, updated_at = ? WHERE id = ?", (title, now, chat_id))
            if is_pinned is not None:
                c.execute("UPDATE chats SET is_pinned = ?, updated_at = ? WHERE id = ?", (1 if is_pinned else 0, now, chat_id))
            if project_id is not None:
                c.execute("UPDATE chats SET project_id = ?, updated_at = ? WHERE id = ?", (project_id, now, chat_id))
            conn.commit()
        return {"status": "success", "chat_id": chat_id}

    def delete_chat(self, chat_id: str) -> Dict[str, Any]:
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM messages WHERE chat_id = ?", (chat_id,))
            c.execute("DELETE FROM chats WHERE id = ?", (chat_id,))
            conn.commit()
        return {"status": "success", "deleted_chat_id": chat_id}

    def create_project(self, name: str, description: str = "", user_key: str = "admin") -> Dict[str, Any]:
        proj_id = f"proj_{uuid.uuid4().hex[:12]}"
        now = time.time()
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("""
            INSERT INTO projects (id, name, description, created_at, updated_at, user_key)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (proj_id, name, description, now, now, user_key))
            conn.commit()
        return {"status": "success", "project_id": proj_id, "name": name}

history_manager = HistoryManager()
