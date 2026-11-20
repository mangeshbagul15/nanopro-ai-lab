import os
from typing import Dict, Any, List

# Provider Keys & Configurations read securely from Environment
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
DEFAPI_API_KEY = os.environ.get("DEFAPI_API_KEY", "")
DEFAPI_BASE_URL = os.environ.get("DEFAPI_BASE_URL", "https://api.defapi.org/v1")
JEV_API_KEY = os.environ.get("JEV_API_KEY", "")
JEV_BASE_URL = os.environ.get("JEV_BASE_URL", "https://jevtypesafeai.com/api/v1")
CLOUDFLARE_EDGE_URL = os.environ.get("CLOUDFLARE_EDGE_URL", "https://nanopro-prod.mangeshbagul15.workers.dev")

# Alert Channel Configurations
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_REPORTS_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "1200023268")
WHATSAPP_PHONE_ID = os.environ.get("WHATSAPP_CLOUD_PHONE_ID", "1355864990944215")
WHATSAPP_ACCESS_TOKEN = os.environ.get("WHATSAPP_CLOUD_ACCESS_TOKEN", "")
EMAIL_RELAY_URL = os.environ.get("EMAIL_RELAY_URL", "")
EMAIL_RELAY_SECRET = os.environ.get("EMAIL_RELAY_SECRET", "")
EMAIL_RELAY_TO = os.environ.get("EMAIL_RELAY_TO", "nanoproaistudio@gmail.com")

TOTAL_MODELS_COUNT = 4804
TOTAL_PROVIDERS_COUNT = 25
TOTAL_DAGS_COUNT = 86
TOTAL_REPORTS_COUNT = 49
TOTAL_DATABASES_COUNT = 5
TOTAL_AGENTS_COUNT = 320

SYSTEM_IDENTITY = {
    "name": "NanoPro AI Lab",
    "version": "2026.4.0-PROD",
    "architecture": "4,804+ Models & 320 Autonomous Agents Unified Mesh",
    "engine": "Groq LPU Sub-Second Orchestrator",
    "sla": "<300ms",
    "memory_overhead": "0 MB Render RAM Overhead",
    "total_dags": 86,
    "total_reports": 49,
    "total_databases": 5
}
