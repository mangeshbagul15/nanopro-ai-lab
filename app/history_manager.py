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
                tool_logs_json TEXT DEFAULT '',
                dataframe_json TEXT DEFAULT '',
                created_at REAL NOT NULL,
                user_key TEXT NOT NULL
            )""")
            try:
                c.execute("ALTER TABLE messages ADD COLUMN tool_logs_json TEXT DEFAULT ''")
            except Exception:
                pass
            try:
                c.execute("ALTER TABLE messages ADD COLUMN dataframe_json TEXT DEFAULT ''")
            except Exception:
                pass
            c.execute("""
            CREATE TABLE IF NOT EXISTS attachments (
                id TEXT PRIMARY KEY,
                chat_id TEXT NOT NULL,
                name TEXT NOT NULL,
                mime_type TEXT NOT NULL,
                data TEXT NOT NULL,
                kind TEXT DEFAULT 'image',
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
        u_key = str(user_key or "admin").strip()
        is_admin = u_key.lower() in ("admin", "nanopro")

        # 1. Fetch persistent sessions from DuckDB & Render PostgreSQL
        p_sessions = []
        p_projects = []
        try:
            from nanopro_connectors import ChatPersistenceConnector
            persisted = ChatPersistenceConnector.list_sessions_and_projects(user_key=u_key)
            p_sessions = persisted.get("sessions") or []
            p_projects = persisted.get("projects") or []
        except Exception:
            pass

        # 2. Fetch local SQLite chats & projects
        sqlite_chats = []
        sqlite_projects = []
        with self._get_conn() as conn:
            c = conn.cursor()
            if is_admin:
                c.execute("SELECT * FROM chats ORDER BY is_pinned DESC, updated_at DESC LIMIT 50")
            else:
                c.execute("SELECT * FROM chats WHERE user_key = ? ORDER BY is_pinned DESC, updated_at DESC LIMIT 50", (u_key,))
            sqlite_chats = [dict(r) for r in c.fetchall()]

            if is_admin:
                c.execute("SELECT * FROM projects ORDER BY updated_at DESC LIMIT 20")
            else:
                c.execute("SELECT * FROM projects WHERE user_key = ? ORDER BY updated_at DESC LIMIT 20", (u_key,))
            sqlite_projects = [dict(r) for r in c.fetchall()]

        # 3. Deduplicate and merge chats
        merged_chats_map = {}
        for ch in sqlite_chats:
            ch_id = ch["id"]
            merged_chats_map[ch_id] = {
                "id": ch_id,
                "project_id": ch.get("project_id") or "",
                "title": ch.get("title") or "AI Session",
                "model": ch.get("model") or "auto",
                "effort": ch.get("effort") or "default",
                "is_pinned": bool(ch.get("is_pinned", False)),
                "message_count": int(ch.get("message_count", 0)),
                "created_at": ch.get("created_at") or time.time(),
                "updated_at": ch.get("updated_at") or time.time(),
                "user_key": ch.get("user_key") or u_key
            }

        for sess in p_sessions:
            s_id = sess.get("session_id")
            if not s_id:
                continue
            merged_chats_map[s_id] = {
                "id": s_id,
                "project_id": sess.get("project_id") or "",
                "title": sess.get("title") or "AI Session",
                "model": sess.get("model_used") or "auto",
                "effort": "default",
                "is_pinned": bool(sess.get("is_pinned", False)),
                "message_count": int(sess.get("message_count", 0)),
                "created_at": str(sess.get("created_at") or time.time()),
                "updated_at": str(sess.get("updated_at") or time.time()),
                "user_key": sess.get("user_key") or u_key
            }

        # Deduplicate and merge projects
        merged_projects_map = {}
        for p in sqlite_projects:
            merged_projects_map[p["id"]] = {
                "id": p["id"],
                "name": p.get("name", "Project"),
                "description": p.get("description", ""),
                "created_at": p.get("created_at") or time.time(),
                "updated_at": p.get("updated_at") or time.time(),
                "user_key": p.get("user_key") or u_key
            }
        for p in p_projects:
            p_id = p.get("project_id")
            if p_id:
                merged_projects_map[p_id] = {
                    "id": p_id,
                    "name": p.get("name", "Project"),
                    "description": p.get("description", ""),
                    "created_at": str(p.get("created_at") or time.time()),
                    "updated_at": str(p.get("updated_at") or time.time()),
                    "user_key": p.get("user_key") or u_key
                }

        all_chats = list(merged_chats_map.values())
        all_chats.sort(key=lambda x: (1 if x.get("is_pinned") else 0, str(x.get("updated_at"))), reverse=True)
        all_projects = list(merged_projects_map.values())

        return {
            "status": "success",
            "chats": all_chats,
            "projects": all_projects,
            "owner": u_key,
            "pinned_count": sum(1 for ch in all_chats if ch.get("is_pinned")),
            "recent_count": len(all_chats),
            "project_count": len(all_projects),
            "storage": "Render PostgreSQL · DuckDB · SQLite in sync",
            "server_timestamp": time.time()
        }

    def create_chat(self, title: str = "New AI Chat Session", project_id: str = "", model: str = "auto", user_key: str = "admin") -> Dict[str, Any]:
        u_key = str(user_key or "admin").strip()
        chat_id = f"chat_{int(time.time()*1000)}_{uuid.uuid4().hex[:6]}"
        now = time.time()
        
        # 1. SQLite
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("""
            INSERT INTO chats (id, project_id, title, model, effort, is_pinned, message_count, created_at, updated_at, user_key)
            VALUES (?, ?, ?, ?, 'default', 0, 0, ?, ?, ?)
            """, (chat_id, project_id, title, model, now, now, u_key))
            conn.commit()

        # 2. DuckDB & Render PostgreSQL
        try:
            from nanopro_connectors import ChatPersistenceConnector
            ChatPersistenceConnector.create_session(title=title, project_id=project_id, model=model, user_key=u_key)
        except Exception:
            pass

        chat_obj = {
            "id": chat_id,
            "project_id": project_id,
            "title": title,
            "model": model,
            "effort": "default",
            "is_pinned": False,
            "message_count": 0,
            "created_at": now,
            "updated_at": now,
            "user_key": u_key
        }
        return {"status": "success", "chat_id": chat_id, "title": title, "project_id": project_id, "chat": chat_obj}

    def get_chat_messages(self, chat_id: str, user_key: str = "admin") -> List[Dict[str, Any]]:
        u_key = str(user_key or "admin").strip()
        # 1. Authoritative messages from DuckDB & Render PostgreSQL
        p_msgs = []
        try:
            from nanopro_connectors import ChatPersistenceConnector
            p_msgs = ChatPersistenceConnector.get_session_messages(session_id=chat_id, user_key=u_key)
        except Exception:
            p_msgs = []

        # 2. Local SQLite messages
        s_msgs = []
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM messages WHERE chat_id = ? ORDER BY created_at ASC", (chat_id,))
            s_msgs = [dict(r) for r in c.fetchall()]

        # 3. Merge & Deduplicate
        seen_ids = set()
        merged = []
        for m in p_msgs:
            m_id = m.get("id")
            if m_id and m_id not in seen_ids:
                seen_ids.add(m_id)
                merged.append(m)

        for m in s_msgs:
            m_id = m.get("id")
            if m_id and m_id not in seen_ids:
                seen_ids.add(m_id)
                t_logs = m.get("tool_logs_json", "")
                if t_logs and isinstance(t_logs, str):
                    try: t_logs = json.loads(t_logs)
                    except Exception: pass
                df_json = m.get("dataframe_json", "")
                if df_json and isinstance(df_json, str):
                    try: df_json = json.loads(df_json)
                    except Exception: pass
                r_math = m.get("routing_math", "")
                if r_math and isinstance(r_math, str):
                    try: r_math = json.loads(r_math)
                    except Exception: pass
                merged.append({
                    "id": m_id,
                    "session_id": chat_id,
                    "chat_id": chat_id,
                    "role": m.get("role", "user"),
                    "content": m.get("content", ""),
                    "model_used": m.get("model_executed") or m.get("model_routed") or "",
                    "model_executed": m.get("model_executed") or "",
                    "model_routed": m.get("model_routed") or "",
                    "duration_ms": float(m.get("duration_ms") or 0.0),
                    "routing_math": r_math,
                    "tool_executions": t_logs,
                    "tool_logs_json": t_logs,
                    "csv_download": df_json,
                    "dataframe_json": df_json,
                    "created_at": str(m.get("created_at") or time.time()),
                    "user_key": m.get("user_key", u_key)
                })

        return merged

    def add_message(
        self,
        chat_id: str,
        role: str,
        content: str,
        model_routed: str = "",
        model_executed: str = "",
        duration_ms: float = 0,
        routing_math: str = "",
        tool_logs_json: str = "",
        dataframe_json: str = "",
        user_key: str = "admin"
    ) -> Dict[str, Any]:
        u_key = str(user_key or "admin").strip()
        msg_id = f"msg_{int(time.time()*1000)}_{uuid.uuid4().hex[:6]}"
        now = time.time()
        
        # 1. SQLite
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("""
            INSERT INTO messages (id, chat_id, role, content, model_routed, model_executed, duration_ms, routing_math, tool_logs_json, dataframe_json, created_at, user_key)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (msg_id, chat_id, role, content, model_routed, model_executed, duration_ms, routing_math, tool_logs_json, dataframe_json, now, u_key))
            c.execute("UPDATE chats SET message_count = message_count + 1, updated_at = ? WHERE id = ?", (now, chat_id))
            conn.commit()

        # 2. DuckDB & Render PostgreSQL
        try:
            from nanopro_connectors import ChatPersistenceConnector
            ChatPersistenceConnector.save_message(
                session_id=chat_id,
                role=role,
                content=content,
                model_used=model_executed or model_routed,
                duration_ms=duration_ms,
                routing_math=routing_math,
                tool_logs=tool_logs_json,
                dataframe=dataframe_json,
                user_key=u_key
            )
        except Exception:
            pass

        return {"status": "success", "message_id": msg_id, "chat_id": chat_id}

    def update_chat(self, chat_id: str, title: Optional[str] = None, is_pinned: Optional[bool] = None, project_id: Optional[str] = None, user_key: str = "admin") -> Dict[str, Any]:
        u_key = str(user_key or "admin").strip()
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

        try:
            from nanopro_connectors import ChatPersistenceConnector
            ChatPersistenceConnector.update_session(session_id=chat_id, title=title, is_pinned=is_pinned, project_id=project_id, user_key=u_key)
        except Exception:
            pass

        return {"status": "success", "chat_id": chat_id}

    def delete_chat(self, chat_id: str, user_key: str = "admin") -> Dict[str, Any]:
        u_key = str(user_key or "admin").strip()
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM messages WHERE chat_id = ?", (chat_id,))
            c.execute("DELETE FROM chats WHERE id = ?", (chat_id,))
            conn.commit()

        try:
            from nanopro_connectors import ChatPersistenceConnector
            ChatPersistenceConnector.delete_session(session_id=chat_id, user_key=u_key)
        except Exception:
            pass

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
        proj_obj = {
            "id": proj_id,
            "name": name,
            "description": description,
            "created_at": now,
            "updated_at": now
        }
        return {"status": "success", "project_id": proj_id, "name": name, "project": proj_obj}

    def update_project(self, project_id: str, name: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
        now = time.time()
        with self._get_conn() as conn:
            c = conn.cursor()
            if name is not None:
                c.execute("UPDATE projects SET name = ?, updated_at = ? WHERE id = ?", (name, now, project_id))
            if description is not None:
                c.execute("UPDATE projects SET description = ?, updated_at = ? WHERE id = ?", (description, now, project_id))
            conn.commit()
        return {"status": "success", "project_id": project_id}

    def delete_project(self, project_id: str) -> Dict[str, Any]:
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM projects WHERE id = ?", (project_id,))
            c.execute("UPDATE chats SET project_id = '' WHERE project_id = ?", (project_id,))
            conn.commit()
        return {"status": "success", "deleted_project_id": project_id}

    def add_attachment(self, chat_id: str, name: str, mime_type: str, data_base64: str, kind: str = "image", user_key: str = "admin") -> Dict[str, Any]:
        att_id = f"att_{uuid.uuid4().hex[:12]}"
        now = time.time()
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("""
            INSERT INTO attachments (id, chat_id, name, mime_type, data, kind, created_at, user_key)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (att_id, chat_id, name, mime_type, data_base64, kind, now, user_key))
            conn.commit()
        return {
            "id": att_id,
            "chat_id": chat_id,
            "name": name,
            "mime_type": mime_type,
            "kind": kind,
            "created_at": now
        }

    def get_attachment(self, attachment_id: str, user_key: str = "admin") -> Optional[Dict[str, Any]]:
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM attachments WHERE id = ?", (attachment_id,))
            row = c.fetchone()
            return dict(row) if row else None

history_manager = HistoryManager()
