import os
import httpx
from typing import Dict, Any, Optional

from app.config import (
    TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID,
    WHATSAPP_PHONE_ID, WHATSAPP_ACCESS_TOKEN,
    EMAIL_RELAY_URL, EMAIL_RELAY_SECRET, EMAIL_RELAY_TO
)

async def dispatch_telegram(message: str) -> Dict[str, Any]:
    token = TELEGRAM_BOT_TOKEN or os.environ.get("TELEGRAM_REPORTS_BOT_TOKEN", "")
    chat_id = TELEGRAM_CHAT_ID or os.environ.get("TELEGRAM_CHAT_ID", "1200023268")
    if not token:
        return {"status": "error", "message": "Telegram Bot Token not configured"}
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
            )
            return resp.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

async def dispatch_email(subject: str, body: str, to: Optional[str] = None) -> Dict[str, Any]:
    url = EMAIL_RELAY_URL or os.environ.get("EMAIL_RELAY_URL", "")
    secret = EMAIL_RELAY_SECRET or os.environ.get("EMAIL_RELAY_SECRET", "")
    target = to or EMAIL_RELAY_TO or os.environ.get("EMAIL_RELAY_TO", "nanoproaistudio@gmail.com")
    if not url or not secret:
        return {"status": "error", "message": "Email Relay URL or Secret not configured"}
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(
                url,
                json={"secret": secret, "to": target, "subject": subject, "body": body},
                follow_redirects=True
            )
            return resp.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

async def dispatch_whatsapp(template_name: str = "report_delivered", text: str = "") -> Dict[str, Any]:
    phone_id = WHATSAPP_PHONE_ID or os.environ.get("WHATSAPP_CLOUD_PHONE_ID", "1355864990944215")
    token = WHATSAPP_ACCESS_TOKEN or os.environ.get("WHATSAPP_CLOUD_ACCESS_TOKEN", "")
    if not token:
        return {"status": "error", "message": "WhatsApp Access Token not configured"}
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"https://graph.facebook.com/v22.0/{phone_id}/messages",
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                json={
                    "messaging_product": "whatsapp",
                    "to": "919028882068",
                    "type": "text",
                    "text": {"body": text or "⚡ NanoPro Global AI Lab: Multi-channel broadcast operational."}
                }
            )
            return resp.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}
