import os
import re
import time
import uuid
import json
import secrets
import hashlib
import sqlite3
import urllib.request
import urllib.parse
from typing import Dict, Any, Optional, Tuple

from app.config import (
    TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID,
    WHATSAPP_PHONE_ID, WHATSAPP_ACCESS_TOKEN
)
from app.alerts_service import dispatch_telegram, dispatch_whatsapp

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "auth.db")

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "866606165083-aujos8q7sncrs8h66q53l2fkpv0bor44.apps.googleusercontent.com")

def _fire_async(coro):
    try:
        import asyncio
        loop = asyncio.get_running_loop()
        loop.create_task(coro)
    except RuntimeError:
        try:
            coro.close()
        except Exception:
            pass

class AuthManager:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_tables()
        self._bootstrap_admin()

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_tables(self):
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                full_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone_number TEXT,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user',
                status TEXT NOT NULL DEFAULT 'ACTIVE',
                created_at REAL NOT NULL,
                last_login_at REAL,
                last_active_at REAL
            )""")
            c.execute("""
            CREATE TABLE IF NOT EXISTS user_sessions (
                session_token TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                username TEXT NOT NULL,
                role TEXT NOT NULL,
                login_time REAL NOT NULL,
                last_activity REAL NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                is_active INTEGER DEFAULT 1
            )""")
            c.execute("""
            CREATE TABLE IF NOT EXISTS auth_otps (
                id TEXT PRIMARY KEY,
                identifier TEXT NOT NULL,
                otp_code TEXT NOT NULL,
                channel TEXT NOT NULL,
                created_at REAL NOT NULL,
                expires_at REAL NOT NULL,
                is_used INTEGER DEFAULT 0
            )""")
            conn.commit()

        # Replicate & Ground User Schema in DuckDB & Render PostgreSQL
        try:
            from nanopro_connectors import DuckDBFederatedConnector
            dcon = DuckDBFederatedConnector.get_connection(read_only=False)
            dcon.execute("""
            CREATE TABLE IF NOT EXISTS nanopro_user_accounts (
                id VARCHAR PRIMARY KEY,
                username VARCHAR NOT NULL,
                full_name VARCHAR NOT NULL,
                email VARCHAR NOT NULL,
                phone_number VARCHAR DEFAULT '',
                password_hash VARCHAR NOT NULL,
                salt VARCHAR NOT NULL,
                role VARCHAR NOT NULL DEFAULT 'user',
                status VARCHAR NOT NULL DEFAULT 'ACTIVE',
                created_at DOUBLE NOT NULL,
                last_login_at DOUBLE,
                last_active_at DOUBLE
            );
            CREATE TABLE IF NOT EXISTS nanopro_user_sessions (
                session_token VARCHAR PRIMARY KEY,
                user_id VARCHAR NOT NULL,
                username VARCHAR NOT NULL,
                role VARCHAR NOT NULL,
                login_time DOUBLE NOT NULL,
                last_activity DOUBLE NOT NULL,
                ip_address VARCHAR DEFAULT '',
                user_agent VARCHAR DEFAULT '',
                is_active BOOLEAN DEFAULT TRUE
            );
            """)
            dcon.close()
        except Exception:
            pass

        try:
            from nanopro_connectors import RenderPostgresConnector
            RenderPostgresConnector.execute_and_commit("""
            CREATE TABLE IF NOT EXISTS nanopro_user_accounts (
                id VARCHAR(64) PRIMARY KEY,
                username VARCHAR(64) NOT NULL,
                full_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone_number VARCHAR(32) DEFAULT '',
                password_hash VARCHAR(255) NOT NULL,
                salt VARCHAR(255) NOT NULL,
                role VARCHAR(32) NOT NULL DEFAULT 'user',
                status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',
                created_at DOUBLE PRECISION NOT NULL,
                last_login_at DOUBLE PRECISION,
                last_active_at DOUBLE PRECISION
            );
            CREATE TABLE IF NOT EXISTS nanopro_user_sessions (
                session_token VARCHAR(128) PRIMARY KEY,
                user_id VARCHAR(64) NOT NULL,
                username VARCHAR(64) NOT NULL,
                role VARCHAR(32) NOT NULL,
                login_time DOUBLE PRECISION NOT NULL,
                last_activity DOUBLE PRECISION NOT NULL,
                ip_address VARCHAR(64) DEFAULT '',
                user_agent VARCHAR(255) DEFAULT '',
                is_active BOOLEAN DEFAULT TRUE
            );
            """)
        except Exception:
            pass

    def _mirror_user_and_session(self, user: Dict[str, Any], session_token: str = '', ip: str = 'Unknown', ua: str = 'Unknown'):
        now = time.time()
        u_id = user.get('id') or f"user_{uuid.uuid4().hex[:12]}"
        u_name = user.get('username') or 'user'
        f_name = user.get('full_name') or u_name
        email = user.get('email') or f"{u_name}@nanopro.ai"
        phone = user.get('phone_number') or ''
        pwd_hash = user.get('password_hash') or ''
        salt = user.get('salt') or ''
        role = user.get('role') or 'user'
        status = user.get('status') or 'ACTIVE'
        c_at = float(user.get('created_at') or now)

        try:
            from nanopro_connectors import DuckDBFederatedConnector
            dcon = DuckDBFederatedConnector.get_connection(read_only=False)
            dcon.execute("""
            INSERT OR REPLACE INTO nanopro_user_accounts (id, username, full_name, email, phone_number, password_hash, salt, role, status, created_at, last_login_at, last_active_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (u_id, u_name, f_name, email, phone, pwd_hash, salt, role, status, c_at, now, now))
            if session_token:
                dcon.execute("""
                INSERT OR REPLACE INTO nanopro_user_sessions (session_token, user_id, username, role, login_time, last_activity, ip_address, user_agent, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, TRUE)
                """, (session_token, u_id, u_name, role, now, now, ip, ua))
            dcon.close()
        except Exception:
            pass

        try:
            from nanopro_connectors import RenderPostgresConnector
            safe_u = u_name.replace("'", "''")
            safe_fn = f_name.replace("'", "''")
            safe_em = email.replace("'", "''")
            RenderPostgresConnector.execute_and_commit(f"""
            INSERT INTO nanopro_user_accounts (id, username, full_name, email, phone_number, password_hash, salt, role, status, created_at, last_login_at, last_active_at)
            VALUES ('{u_id}', '{safe_u}', '{safe_fn}', '{safe_em}', '{phone}', '{pwd_hash}', '{salt}', '{role}', '{status}', {c_at}, {now}, {now})
            ON CONFLICT (id) DO UPDATE SET last_login_at = {now}, last_active_at = {now};
            """)
            if session_token:
                RenderPostgresConnector.execute_and_commit(f"""
                INSERT INTO nanopro_user_sessions (session_token, user_id, username, role, login_time, last_activity, ip_address, user_agent, is_active)
                VALUES ('{session_token}', '{u_id}', '{safe_u}', '{role}', {now}, {now}, '{ip}', '{ua}', TRUE)
                ON CONFLICT (session_token) DO UPDATE SET last_activity = {now}, is_active = TRUE;
                """)
        except Exception:
            pass

    def _hash_password(self, password: str, salt: Optional[str] = None) -> Tuple[str, str]:
        if not salt:
            salt = uuid.uuid4().hex
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
        return key.hex(), salt

    def _bootstrap_admin(self):
        try:
            admin_pwd = (os.environ.get("NANOPRO_ADMIN_PASSWORD") or "Divyam@123").strip()
            pwd_hash, salt = self._hash_password(admin_pwd)
            now = time.time()
            with self._get_conn() as conn:
                c = conn.cursor()
                c.execute("SELECT id FROM users WHERE username = 'nanopro'")
                row = c.fetchone()
                if not row:
                    c.execute("""
                    INSERT INTO users (id, username, full_name, email, phone_number, password_hash, salt, role, status, created_at, last_login_at, last_active_at)
                    VALUES (?, 'nanopro', 'Super Admin (Mangesh Bagul)', 'mangeshbagul15@gmail.com', '+919028882068', ?, ?, 'admin', 'ACTIVE', ?, ?, ?)
                    """, ("user_admin_001", pwd_hash, salt, now, now, now))
                else:
                    c.execute("UPDATE users SET password_hash=?, salt=?, status='ACTIVE', role='admin' WHERE username='nanopro'", (pwd_hash, salt))
                conn.commit()
        except Exception:
            pass

    def authenticate_user(self, username: str, password: str, ip: str = "Unknown", ua: str = "Unknown") -> Dict[str, Any]:
        ident = (username or "").strip()
        ident_lower = ident.lower()
        now = time.time()

        digits = "".join(c for c in ident if c.isdigit())
        phone_variants = [ident]
        if digits:
            phone_variants.extend([digits, f"+{digits}"])
            if len(digits) == 10:
                phone_variants.extend([f"+91{digits}", f"91{digits}"])

        with self._get_conn() as conn:
            c = conn.cursor()
            placeholders = ",".join("?" for _ in phone_variants)
            query = f"""
            SELECT * FROM users
            WHERE LOWER(username) = ? OR LOWER(email) = ? OR phone_number IN ({placeholders})
            LIMIT 1
            """
            c.execute(query, [ident_lower, ident_lower] + phone_variants)
            user = c.fetchone()

            if not user:
                return {"status": "error", "error": "Invalid username or password!"}

            calc_hash, _ = self._hash_password(password, user["salt"])
            password_matches = (calc_hash == user["password_hash"])

            if not password_matches and (user["username"] == "nanopro" or user["role"] == "admin"):
                env_pwd = (os.environ.get("NANOPRO_ADMIN_PASSWORD") or "Divyam@123").strip()
                if password == env_pwd:
                    password_matches = True

            if not password_matches:
                return {"status": "error", "error": "Invalid username or password!"}

            if user["status"] not in ("ACTIVE", "APPROVED"):
                return {"status": "error", "error": "Account is pending admin approval."}

            session_token = f"np_sess_{uuid.uuid4().hex}"
            c.execute("""
            INSERT INTO user_sessions (session_token, user_id, username, role, login_time, last_activity, ip_address, user_agent, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
            """, (session_token, user["id"], user["username"], user["role"], now, now, ip, ua))
            c.execute("UPDATE users SET last_login_at=?, last_active_at=? WHERE id=?", (now, now, user["id"]))
            conn.commit()
            try:
                self._mirror_user_and_session(dict(user), session_token, ip, ua)
            except Exception:
                pass

        time_str = time.strftime('%d-%m-%Y %I:%M:%S %p', time.localtime(now))
        import asyncio
        _fire_async(dispatch_telegram(
            f"🔐 <b>NanoPro Direct Login Alert</b>\n"
            f"👤 <b>User:</b> {user['username']} ({user['full_name']})\n"
            f"👑 <b>Role:</b> {user['role'].upper()}\n"
            f"🕒 <b>Time:</b> {time_str}\n"
            f"🌐 <b>IP:</b> {ip}"
        ))

        return {
            "status": "success",
            "session_token": session_token,
            "user": {
                "id": user["id"],
                "username": user["username"],
                "full_name": user["full_name"],
                "email": user["email"],
                "role": user["role"]
            }
        }

    def verify_google_token(self, credential: str) -> Dict[str, Any]:
        url = "https://oauth2.googleapis.com/tokeninfo?" + urllib.parse.urlencode({"id_token": credential})
        req = urllib.request.Request(url, headers={"User-Agent": "NanoProAI/1.0"})
        with urllib.request.urlopen(req, timeout=10.0) as resp:
            claims = json.loads(resp.read().decode("utf-8"))
        if str(claims.get("email_verified", "")).lower() not in ("true", "1"):
            raise ValueError("Google account email is not verified.")
        if claims.get("iss") not in ("accounts.google.com", "https://accounts.google.com"):
            raise ValueError("Invalid token issuer.")
        return claims

    def authenticate_google(self, credential: str, ip: str = "Unknown", ua: str = "Unknown") -> Dict[str, Any]:
        claims = self.verify_google_token(credential)
        email = (claims.get("email") or "").strip().lower()
        full_name = claims.get("name") or "Google User"
        now = time.time()

        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE LOWER(email) = LOWER(?)", (email,))
            user = c.fetchone()

            if user:
                user_id = user["id"]
                username = user["username"]
                role = user["role"]
                c.execute("UPDATE users SET last_login_at=?, last_active_at=? WHERE id=?", (now, now, user_id))
            else:
                user_id = f"user_{uuid.uuid4().hex[:12]}"
                username = email.split("@")[0].lower()
                role = "admin" if email in ("mangeshbagul15@gmail.com", "nanoproaistudio1@gmail.com") else "user"
                pwd_hash, salt = self._hash_password(uuid.uuid4().hex)
                c.execute("""
                INSERT INTO users (id, username, full_name, email, phone_number, password_hash, salt, role, status, created_at, last_login_at, last_active_at)
                VALUES (?, ?, ?, ?, '', ?, ?, ?, 'ACTIVE', ?, ?, ?)
                """, (user_id, username, full_name, email, pwd_hash, salt, role, now, now, now))

            session_token = f"np_sess_{uuid.uuid4().hex}"
            c.execute("""
            INSERT INTO user_sessions (session_token, user_id, username, role, login_time, last_activity, ip_address, user_agent, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
            """, (session_token, user_id, username, role, now, now, ip, ua))
            conn.commit()
            try:
                self._mirror_user_and_session({"id": user_id, "username": username, "full_name": full_name, "email": email, "role": role, "created_at": now}, session_token, ip, ua)
            except Exception:
                pass
            try:
                self._mirror_user_and_session({"id": user_id, "username": username, "full_name": full_name, "email": email, "role": role, "created_at": now}, session_token, ip, ua)
            except Exception:
                pass

        time_str = time.strftime('%d-%m-%Y %I:%M:%S %p', time.localtime(now))
        import asyncio
        _fire_async(dispatch_telegram(
            f"🌐 <b>NanoPro Google SSO Login Alert</b>\n"
            f"👤 <b>User:</b> {username} ({full_name})\n"
            f"📧 <b>Email:</b> {email}\n"
            f"👑 <b>Role:</b> {role.upper()}\n"
            f"🕒 <b>Time:</b> {time_str}\n"
            f"🌐 <b>IP:</b> {ip}"
        ))

        return {
            "status": "success",
            "session_token": session_token,
            "user": {
                "id": user_id,
                "username": username,
                "full_name": full_name,
                "email": email,
                "role": role
            }
        }

    def generate_and_send_otp(self, identifier: str, channel: str = "whatsapp", ip: str = "Unknown") -> Dict[str, Any]:
        ident = str(identifier or "").strip()
        digits = re.sub(r"[^0-9]", "", ident)
        if len(digits) == 10:
            digits = "91" + digits
        clean_phone = "+" + digits if digits else ident

        otp_code = f"{secrets.randbelow(900000) + 100000}"
        now = time.time()

        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("UPDATE auth_otps SET is_used = 1 WHERE identifier = ?", (clean_phone,))
            c.execute("""
            INSERT INTO auth_otps (id, identifier, otp_code, channel, created_at, expires_at, is_used)
            VALUES (?, ?, ?, ?, ?, ?, 0)
            """, (f"otp_{uuid.uuid4().hex[:12]}", clean_phone, otp_code, channel, now, now + 300))
            conn.commit()

        # Dispatch via WhatsApp and Telegram
        import asyncio
        msg_text = f"⚡ NanoPro Login OTP: {otp_code} (Valid for 5 minutes). Do not share."
        _fire_async(dispatch_whatsapp(text=msg_text))
        _fire_async(dispatch_telegram(
            f"📲 <b>NanoPro WhatsApp OTP Generated</b>\n"
            f"📱 <b>Target:</b> {clean_phone}\n"
            f"🔑 <b>Code:</b> <code>{otp_code}</code>\n"
            f"⏳ <b>Validity:</b> 5 minutes"
        ))

        return {
            "status": "success",
            "message": f"६-अंकी OTP {clean_phone} वर यशस्वीरीत्या पाठवला आहे.",
            "channel": channel,
            "phone": clean_phone
        }

    def verify_otp_and_login(self, identifier: str, otp_code: str, channel: str = "whatsapp", ip: str = "Unknown", ua: str = "Unknown") -> Dict[str, Any]:
        ident = str(identifier or "").strip()
        code = str(otp_code or "").strip()
        digits = re.sub(r"[^0-9]", "", ident)
        if len(digits) == 10:
            digits = "91" + digits
        clean_phone = "+" + digits if digits else ident
        now = time.time()

        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("""
            SELECT * FROM auth_otps
            WHERE identifier = ? AND otp_code = ? AND is_used = 0 AND expires_at >= ?
            ORDER BY created_at DESC LIMIT 1
            """, (clean_phone, code, now))
            row = c.fetchone()

            if not row:
                return {"status": "error", "error": "Invalid or expired OTP code!"}

            c.execute("UPDATE auth_otps SET is_used = 1 WHERE id = ?", (row["id"],))

            c.execute("SELECT * FROM users WHERE phone_number = ? OR phone_number = ?", (clean_phone, digits))
            user = c.fetchone()
            if user:
                user_id = user["id"]
                username = user["username"]
                role = user["role"]
                full_name = user["full_name"]
                email = user["email"]
                c.execute("UPDATE users SET last_login_at=?, last_active_at=? WHERE id=?", (now, now, user_id))
            else:
                user_id = f"user_{uuid.uuid4().hex[:12]}"
                username = f"wa_{digits[-6:]}"
                full_name = f"WhatsApp User ({digits[-4:]})"
                email = f"{username}@whatsapp.nanopro.ai"
                role = "admin" if "9028882068" in digits else "user"
                pwd_hash, salt = self._hash_password(uuid.uuid4().hex)
                c.execute("""
                INSERT INTO users (id, username, full_name, email, phone_number, password_hash, salt, role, status, created_at, last_login_at, last_active_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'ACTIVE', ?, ?, ?)
                """, (user_id, username, full_name, email, clean_phone, pwd_hash, salt, role, now, now, now))

            session_token = f"np_sess_{uuid.uuid4().hex}"
            c.execute("""
            INSERT INTO user_sessions (session_token, user_id, username, role, login_time, last_activity, ip_address, user_agent, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
            """, (session_token, user_id, username, role, now, now, ip, ua))
            conn.commit()

        return {
            "status": "success",
            "session_token": session_token,
            "user": {
                "id": user_id,
                "username": username,
                "full_name": full_name,
                "email": email,
                "role": role
            }
        }

    def register_user(self, username: str, password: str, full_name: str, email: str, phone: str = "", ip: str = "Unknown", ua: str = "Unknown") -> Dict[str, Any]:
        u = (username or "").strip()
        e = (email or "").strip().lower()
        fn = (full_name or u).strip()
        p = str(phone or "").strip()
        now = time.time()

        if not u or not password or not e:
            return {"status": "error", "error": "Username, password and email are required."}

        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("SELECT id FROM users WHERE LOWER(username) = ? OR LOWER(email) = ?", (u.lower(), e))
            if c.fetchone():
                return {"status": "error", "error": "User or email already exists!"}

            user_id = f"user_{uuid.uuid4().hex[:12]}"
            pwd_hash, salt = self._hash_password(password)
            role = "admin" if u == "nanopro" or e == "mangeshbagul15@gmail.com" else "user"
            c.execute("""
            INSERT INTO users (id, username, full_name, email, phone_number, password_hash, salt, role, status, created_at, last_login_at, last_active_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'ACTIVE', ?, ?, ?)
            """, (user_id, u, fn, e, p, pwd_hash, salt, role, now, now, now))
            conn.commit()
            try:
                self._mirror_user_and_session({"id": user_id, "username": u, "full_name": fn, "email": e, "phone_number": p, "password_hash": pwd_hash, "salt": salt, "role": role, "created_at": now}, "", ip, ua)
            except Exception:
                pass

        import asyncio
        _fire_async(dispatch_telegram(
            f"👤 <b>NanoPro New User Registered</b>\n"
            f"🔑 <b>Username:</b> {u}\n"
            f"📛 <b>Name:</b> {fn}\n"
            f"📧 <b>Email:</b> {e}\n"
            f"📱 <b>Phone:</b> {p or 'N/A'}\n"
            f"🌐 <b>IP:</b> {ip}"
        ))

        return {"status": "success", "message": "नोंदणी यशस्वी झाली आहे! आपण आता लॉगिन करू शकता."}

    def validate_session(self, token: str) -> Dict[str, Any]:
        if not token:
            return {"status": "error", "valid": False}
        with self._get_conn() as conn:
            c = conn.cursor()
            c.execute("""
            SELECT s.*, u.full_name, u.email
            FROM user_sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.session_token = ? AND s.is_active = 1
            LIMIT 1
            """, (token.strip(),))
            row = c.fetchone()
            if not row:
                # Fallback to persistent DuckDB / Render PostgreSQL session store
                try:
                    from nanopro_connectors import DuckDBFederatedConnector
                    dcon = DuckDBFederatedConnector.get_connection(read_only=True)
                    dcur = dcon.cursor()
                    dcur.execute("""
                    SELECT s.session_token, s.user_id, s.username, s.role, s.login_time, s.last_activity, u.full_name, u.email
                    FROM nanopro_user_sessions s
                    LEFT JOIN nanopro_user_accounts u ON s.user_id = u.id
                    WHERE s.session_token = ? AND s.is_active = TRUE
                    LIMIT 1
                    """, (token.strip(),))
                    drow = dcur.fetchone()
                    dcon.close()
                    if drow:
                        s_token, u_id, u_name, u_role, l_time, l_act, f_name, u_email = drow
                        c.execute("""
                        INSERT OR IGNORE INTO users (id, username, full_name, email, phone_number, password_hash, salt, role, status, created_at, last_login_at, last_active_at)
                        VALUES (?, ?, ?, ?, '', '', '', ?, 'ACTIVE', ?, ?, ?)
                        """, (u_id, u_name, f_name or u_name, u_email or f"{u_name}@nanopro.ai", u_role, l_time, time.time(), time.time()))
                        c.execute("""
                        INSERT OR REPLACE INTO user_sessions (session_token, user_id, username, role, login_time, last_activity, is_active)
                        VALUES (?, ?, ?, ?, ?, ?, 1)
                        """, (s_token, u_id, u_name, u_role, l_time, time.time()))
                        conn.commit()
                        return {
                            "status": "success",
                            "valid": True,
                            "user": {
                                "id": u_id,
                                "username": u_name,
                                "full_name": f_name or u_name,
                                "email": u_email or f"{u_name}@nanopro.ai",
                                "role": u_role
                            }
                        }
                except Exception:
                    pass
                return {"status": "error", "valid": False}

            c.execute("UPDATE user_sessions SET last_activity = ? WHERE session_token = ?", (time.time(), token))
            conn.commit()

            return {
                "status": "success",
                "valid": True,
                "user": {
                    "id": row["user_id"],
                    "username": row["username"],
                    "full_name": row["full_name"],
                    "email": row["email"],
                    "role": row["role"]
                }
            }

    def logout_user(self, token: str) -> Dict[str, Any]:
        if token:
            with self._get_conn() as conn:
                c = conn.cursor()
                c.execute("UPDATE user_sessions SET is_active = 0 WHERE session_token = ?", (token.strip(),))
                conn.commit()
        return {"status": "success", "message": "Successfully logged out"}

auth_manager = AuthManager()
