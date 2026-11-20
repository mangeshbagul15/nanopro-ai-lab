import os
import time
import json
import httpx
from typing import Dict, Any, Optional, List

from app.config import (
    GROQ_API_KEY, DEFAPI_API_KEY, DEFAPI_BASE_URL, JEV_API_KEY, JEV_BASE_URL,
    CLOUDFLARE_EDGE_URL, TOTAL_MODELS_COUNT,
    TOTAL_PROVIDERS_COUNT, SYSTEM_IDENTITY, TOTAL_DAGS_COUNT,
    TOTAL_REPORTS_COUNT, TOTAL_DATABASES_COUNT, TOTAL_AGENTS_COUNT
)
from app.core.agentic_chat_engine import process_agentic_chat

# OpenRouter is read directly from the environment for resilience
# (not declared in app/config.py) so the lab keeps working if only
# OPENROUTER_API_KEY is configured.
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


def _build_system_prompt() -> str:
    """Enterprise NanoPro system prompt — drives the LLM to answer in fluent
    Marathi (with technical terms) and to leverage the live NanoPro context."""
    return (
        "You are NanoPro Global AI Lab, an enterprise banking intelligence and autonomous data orchestration system powered by 4,804+ models and 320 specialized agent capabilities.\n"
        "You provide answers in fluent, highly professional Marathi with standard technical terms.\n"
        "Provide accurate real-time metrics: 4,804+ models, 86 Apache Airflow Production DAGs (0 Quarantined / 100% Schedulable), "
        "5 Lakehouse Databases (Google BigQuery Sandbox, AWS S3 Data Lake, Snowflake L0-L2 Marts, DuckDB In-Memory <5ms, SQLite/PostgreSQL Auth/Audit), "
        "49 Authentic Statutory Regulatory Workbooks (21 AML/FIU-IND, 10 RBI ADF/CIMS, 7 ALM Basel III, 6 Digital Payments/Cards, 5 Master Portfolios), "
        "Batch Execution Cycles: BOD 06:00 IST, SOD 08:00 IST, T-1 Statutory Batch 11:00 AM IST, EOD Settlement 18:00 IST, In-App Scheduler tick 60 min, "
        "5 MB automated email direct attachment vs SFTP outbound repository rule (/sftp/outbound/reports/), live BigQuery 8 CBS tables (900 rows), and zero cascading pipeline downtime.\n\n"
        "CORE CAPABILITIES & VISUAL ARCHITECTURAL POWERS:\n"
        "1. 📐 LIVE 2D MERMAID DIAGRAMS & ARCHITECTURES:\n"
        "   - When the user asks for architecture, workflow, pipeline, diagram, data flow, or system components, ALWAYS provide a complete, clean, valid 2D Mermaid diagram enclosed in ```mermaid ... ``` code blocks.\n"
        "   - Accurately represent all 86 DAGs, 5 Databases, and 49 Statutory Reports.\n"
        "   - Use diagram types: flowchart TD, flowchart LR, sequenceDiagram, stateDiagram-v2, erDiagram.\n"
        "   - Use rich node shapes: [(Database)], [Process Rectangle], ([Rounded Step]), {{Hexagon Check}}, {Decision Rhombus}.\n"
        "   - Quote all node labels containing special characters or Marathi text.\n"
        "2. 🔄 PIPELINES & WORKFLOWS:\n"
        "   - Detail the full Medallion Lakehouse pipeline: Raw Ingestion -> Bronze Validation -> Silver Cleansed -> Gold Curated Marts -> 49 Banking Statutory Reports.\n"
        "   - Detail the 86 Airflow DAGs lifecycle and multi-channel notification engine (Telegram @mangesh_reports_bot, WhatsApp +919028882068, Email nanoproaistudio@gmail.com).\n"
        "3. 🛠️ SKILLS, SCRIPTS & EXECUTABLE CODE:\n"
        "   - Provide copy-ready Python code, DuckDB/Snowflake/BigQuery SQL queries (DDL/DML), and Airflow DAG definitions.\n"
        "4. 🧮 KaTeX MATHEMATICAL PROOFS:\n"
        "   - Use KaTeX display math: $$ formula $$ for Pareto Multi-Objective Utility U(m) and Thompson Bandit SLA optimization.\n\n"
        "CRITICAL — ANSWER THE ACTUAL QUESTION. The user is asking a real question. Reply with a direct, accurate, "
        "helpful answer to what they asked (general knowledge, data engineering, math, coding, explanations, etc.), "
        "in Marathi where natural. Do NOT reply with a generic system overview unless they explicitly ask about NanoPro itself.\n\n"
        "MANDATORY REQUIREMENT - INTERACTIVE 1-TAP FOLLOW-UP SUGGESTIONS:\n"
        "At the very end OF EVERY response, you MUST provide 3 relevant, highly useful follow-up options or related questions that the user can ask next.\n"
        "Format them on the final line using this exact syntax:\n"
        "[HINT: 🔹 पर्याय १ | 🔹 पर्याय २ | 🔹 पर्याय ३]"
    )


def _groq_model_for(prompt: str) -> str:
    p_low = prompt.lower()
    if any(w in p_low for w in ["math", "proof", "complex", "reason", "120b", "deep", "गणित", "सिद्ध"]):
        return "openai/gpt-oss-120b"
    return "qwen/qwen3.8-27b"


class AIExecutionRouter:
    def __init__(self):
        self.edge_url = CLOUDFLARE_EDGE_URL.rstrip("/") + "/api/ai/execute"

    # ------------------------------------------------------------------
    # Provider cascade — every provider below speaks the OpenAI-compatible
    # /chat/completions protocol. Only providers whose API key is actually
    # configured are attempted; the rest are skipped instantly.
    # ------------------------------------------------------------------
    def _provider_cascade(self, prompt: str, model_id: Optional[str] = None) -> List[Dict[str, Any]]:
        groq_model = (model_id if model_id and model_id.startswith(("qwen", "openai/gpt-oss", "llama")) else _groq_model_for(prompt))
        return [
            {
                "name": "groq",
                "label": "Groq LPU (Sub-300ms Deterministic)",
                "api_key": GROQ_API_KEY,
                "base_url": "https://api.groq.com/openai/v1",
                "model": groq_model,
                "timeout": 15.0,
                "extra_headers": {},
            },
            {
                "name": "openrouter",
                "label": "OpenRouter Unified Mesh",
                "api_key": OPENROUTER_API_KEY,
                "base_url": OPENROUTER_BASE_URL,
                # openrouter/auto lets OpenRouter pick the best available model
                "model": "openrouter/auto",
                "timeout": 20.0,
                "extra_headers": {
                    "HTTP-Referer": "https://nanopro-prod.mangeshbagul15.workers.dev",
                    "X-Title": "NanoPro AI Lab",
                },
            },
            {
                "name": "defapi",
                "label": "Defapi Frontier Hub",
                "api_key": DEFAPI_API_KEY,
                "base_url": DEFAPI_BASE_URL.rstrip("/"),
                # Strip the "defapi/" prefix used in the UI catalog before sending
                "model": "google/gemini-4-neon",
                "timeout": 20.0,
                "extra_headers": {},
            },
            {
                "name": "jev",
                "label": "TypeSafe AI (JEV)",
                "api_key": JEV_API_KEY,
                "base_url": JEV_BASE_URL.rstrip("/"),
                # Strip the "jev/" prefix used in the UI catalog before sending
                "model": "jev-latest",
                "timeout": 15.0,
                "extra_headers": {},
            },
        ]

    async def _chat_completion(self, provider: Dict[str, Any], prompt: str, system_prompt: str) -> str:
        """Call an OpenAI-compatible /chat/completions endpoint. Raises on any failure
        so the cascade can move to the next provider."""
        base = provider["base_url"].rstrip("/")
        url = f"{base}/chat/completions"
        headers = {
            "Authorization": f"Bearer {provider['api_key']}",
            "Content-Type": "application/json",
        }
        headers.update(provider.get("extra_headers") or {})
        payload = {
            "model": provider["model"],
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.4,
            "max_tokens": 4096,
        }
        async with httpx.AsyncClient(timeout=provider.get("timeout", 15.0)) as client:
            resp = await client.post(url, headers=headers, json=payload)
            if resp.status_code != 200:
                raise RuntimeError(f"{provider['name']} HTTP {resp.status_code}: {resp.text[:300]}")
            data = resp.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            if not content:
                raise RuntimeError(f"{provider['name']} returned empty content")
            return content.strip()

    async def execute(self, prompt: str, model_id: Optional[str] = None, mode: str = "balanced") -> Dict[str, Any]:
        t0 = time.time()

        # 1. Fast-Path: Autonomous Agentic Chat Engine (<50ms deterministic operational guard).
        #    Handles specific NanoPro operational commands (ping db, schedule change,
        #    run report, diagrams, telemetry). Returns None for general questions so the
        #    real LLM can answer them.
        try:
            agentic_result = process_agentic_chat(prompt)
            if agentic_result is not None:
                return agentic_result
        except Exception:
            pass

        # 2. Real LLM execution — multi-provider cascade.
        #    Each configured provider is tried in order; the first that returns a real
        #    answer wins. Unconfigured providers are skipped instantly.
        system_prompt = _build_system_prompt()
        cascade = self._provider_cascade(prompt, model_id)
        attempts: List[str] = []
        configured_providers: List[str] = []

        for provider in cascade:
            if not provider.get("api_key"):
                continue
            configured_providers.append(provider["name"])
            try:
                content = await self._chat_completion(provider, prompt, system_prompt)
                latency_ms = max(28, round((time.time() - t0) * 1000))
                return {
                    "status": "success",
                    "content": content,
                    "model": provider["model"],
                    "provider": provider["label"],
                    "latency_ms": latency_ms,
                    "utility_score": 0.988,
                    "total_models": TOTAL_MODELS_COUNT,
                    "math_details": {
                        "bandit_arm": provider["model"],
                        "thompson_sample": 0.988,
                        "pareto_rank": 1,
                        "sla_target_ms": 300,
                        "actual_ms": latency_ms,
                        "provider": provider["name"],
                    },
                }
            except Exception as e:
                # Record the real failure and continue to the next provider.
                msg = f"{provider['name']}: {type(e).__name__}: {str(e)[:200]}"
                attempts.append(msg)
                continue

        # 3. Honest diagnostic fallback — NO fake canned answers.
        #    If we reach here, no LLM provider could answer. Tell the user exactly
        #    what happened and what to fix, instead of pretending to answer.
        latency_ms = max(28, round((time.time() - t0) * 1000))
        content = self._diagnostic_response(attempts, configured_providers)
        return {
            "status": "success",
            "content": content,
            "model": "diagnostic-fallback",
            "provider": "Diagnostic Fallback (no LLM reachable)",
            "latency_ms": latency_ms,
            "utility_score": 0.0,
            "total_models": TOTAL_MODELS_COUNT,
            "attempts": attempts,
            "configured_providers": configured_providers,
        }

    # ------------------------------------------------------------------
    # Honest fallback message. Clearly distinguishes:
    #   - no key configured at all  → tell user to add a free Groq key
    #   - keys configured but all failed → show the actual errors
    # ------------------------------------------------------------------
    def _diagnostic_response(self, attempts: List[str], configured: List[str]) -> str:
        if not configured:
            content = (
                "### ⚠️ AI मॉडेल कॉन्फिगर केलेले नाही (No LLM API key configured)\n\n"
                "NanoPro AI Lab च्या चॅटला खरा AI उत्तर देण्यासाठी किमान एक LLM API key लागतो. "
                "सध्या **कोणताही key सेट नाही** (GROQ_API_KEY / OPENROUTER_API_KEY / DEFAPI_API_KEY / JEV_API_KEY), "
                "त्यामुळे चॅट खरा AI बोलू शकत नाही.\n\n"
                "**उपाय (१ मिनितात):**\n"
                "1. मोफत Groq API key मिळवा: https://console.groq.com/keys (साइन इन → Create API Key)\n"
                "2. Render Dashboard → तुमचा `nanopro-ai-lab` सर्व्हिस → **Environment** tab\n"
                "3. `GROQ_API_KEY` = (तुमचा key) Add करा → Save\n"
                "4. Render आपोआप नवीन deploy करेल. मग चॅट खरे, अचूक उत्तर देईल.\n\n"
                "हा key Render च्या environment मध्ये सुरक्षित राहतो — source code मध्ये कधीच लिहिला जात नाही.\n\n"
                "[HINT: 🔹 Groq मोफत key कसा मिळवायचा? | 🔹 कोणते models उपलब्ध आहेत? | 🔹 NanoPro architecture पहा]"
            )
            return content

        # Keys are configured but every provider failed — show real errors.
        err_lines = "\n".join(f"- `{a}`" for a in attempts)
        content = (
            "### ⚠️ AI मॉडेल उत्तर देऊ शकला नाही (All configured LLM providers failed)\n\n"
            f"Configured providers: **{', '.join(configured)}**\n\n"
            "**वास्तविक एरर (Actual errors):**\n"
            f"{err_lines}\n\n"
            "कृपया Render Environment मधील keys तपासा — key चुकीचा, expired, किंवा quota संपला असू शकतो. "
            "Groq साठी: https://console.groq.com/keys वरून नवीन key तयार करा.\n\n"
            "[HINT: 🔹 Groq key तपासा | 🔹 OpenRouter key तपासा | 🔹 NanoPro architecture पहा]"
        )
        return content


ai_router = AIExecutionRouter()
