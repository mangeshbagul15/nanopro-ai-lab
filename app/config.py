import os
from typing import Dict, Any, List

# Provider Keys & Configurations read securely from Environment
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
DEFAPI_API_KEY = os.environ.get("DEFAPI_API_KEY", "")
DEFAPI_BASE_URL = os.environ.get("DEFAPI_BASE_URL", "https://api.defapi.org/v1")
JEV_API_KEY = os.environ.get("JEV_API_KEY", "")
JEV_BASE_URL = os.environ.get("JEV_BASE_URL", "https://jevtypesafeai.com/api/v1")
CLOUDFLARE_EDGE_URL = os.environ.get("CLOUDFLARE_EDGE_URL", "https://mangesh-nanopro.mangeshbagul15.workers.dev")

TOTAL_MODELS_COUNT = 4804
TOTAL_PROVIDERS_COUNT = 25

SYSTEM_IDENTITY = {
    "name": "NanoPro AI Lab",
    "version": "2026.4.0-PROD",
    "architecture": "4,804+ Models Unified Mesh",
    "engine": "Groq LPU Sub-Second Orchestrator",
    "sla": "<300ms",
    "memory_overhead": "0 MB Render RAM Overhead"
}
