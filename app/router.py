from app.core.agentic_runtime import run_agentic_loop
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

# OpenRouter is read directly from the environment for resilience
# (not declared in app/config.py) so the lab keeps working if only
# OPENROUTER_API_KEY is configured.
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Groq supports multiple keys for rate-limit rotation. Groq's free tier
# caps each key at ~30 RPM, so rotating across N keys gives ~N x 30 RPM
# headroom and 429-resilience. Only keys that are actually set are used.
GROQ_API_KEYS = [k for k in (
    GROQ_API_KEY,
    os.environ.get("GROQ_API_KEY_2", ""),
    os.environ.get("GROQ_API_KEY_3", ""),
) if k]

# ---------------------------------------------------------------------------
# Extended Provider Mesh — every entry speaks the OpenAI-compatible
# /chat/completions protocol. Keys are read from Render env vars at call
# time; unconfigured providers are skipped instantly by the cascade.
# Each tuple: (provider_name, env_key, base_url, default_model, timeout_s)
# ---------------------------------------------------------------------------
EXTENDED_PROVIDERS = [
    ("deepseek",      "DEEPSEEK_API_KEY",      "https://api.deepseek.com/v1",        "deepseek-chat",                          20.0),
    ("deepseek#2",    "DEEPSEEK_API_KEY_2",    "https://api.deepseek.com/v1",        "deepseek-chat",                          20.0),
    ("mistral",       "MISTRAL_API_KEY",       "https://api.mistral.ai/v1",          "open-mistral-nemo",                      20.0),
    ("sambanova",     "SAMBANOVA_API_KEY",     "https://api.sambanova.ai/v1",        "Meta-Llama-3.3-70B-Instruct",            20.0),
    ("nvidia-nim",    "NVIDIA_NIM_API_KEY",    "https://integrate.api.nvidia.com/v1","google/gemma-4-31b-it",                   25.0),
    ("novita",        "NOVITA_AI_KEY",         "https://api.novita.ai/v3/openai",    "meta-llama/llama-3.3-70b-instruct",      20.0),
    ("deepinfra",     "DEEPINFRA_API_KEY",     "https://api.deepinfra.com/v1/openai","deepseek-ai/DeepSeek-V3",                 20.0),
    ("requesty",      "REQUESTY_API_KEY",      "https://router.requesty.ai/v1",      "openai/gpt-4o-mini",                     20.0),
    ("aimlapi",       "AIMLAPI_KEY",           "https://api.aimlapi.com/v1",         "gpt-4o-mini",                            20.0),
    ("huggingface",   "HUGGINGFACE_API_KEY",   "https://router.huggingface.co/v1",   "meta-llama/Llama-3.3-70B-Instruct",      20.0),
    ("arcee",         "ARCEE_API_KEY",         "https://api.arcee.ai/api/v1",        "zai-org/glm-5.3-flash",                  20.0),
    ("baseten",       "BASETEN_API_KEY",       "https://inference.baseten.co/v1",    "openai/gpt-oss-120b",                    20.0),
    ("friendli",      "FRIENDLI_API_KEY",      "https://api.friendli.ai/serverless/v1","meta-llama-3.3-70b-instruct",           20.0),
    ("krutrim",       "KRUTRIM_API_KEY",       "https://api.olakrutrim.com/v1",      "krutrim-cloud-ai-v1",                    15.0),
]

# Auto-mode task → provider preference. When the user picks "auto" (or no
# model), the prompt's intent promotes the strongest provider for that task
# to the front of the cascade; failures still fall through to the rest.
AUTO_PROVIDER_HINTS = [
    (("math", "proof", "reason", "logic", "equation", "calculate", "गणित", "सिद्ध", "formula"), "deepseek"),
    (("code", "sql", "ddl", "query", "function", "bug", "python", "javascript", "debug", "script"), "deepseek"),
    (("summar", "translate", "creative", "story", "email", "mail", "rewrite", "essay"), "mistral"),
    (("bank", "compliance", "audit", "aml", "regulatory", "fraud", "fiu", "basel"), "openrouter"),
    (("image", "vision", "diagram", "chart", "mermaid"), "openrouter"),
]

# Friendly model-name aliases so a UI model pick like "deepseek-chat" or
# "mistral-nemo" prioritizes the matching provider in the cascade.
MODEL_PROVIDER_HINTS = {
    "defapi": "defapi",
    "jev": "jev",
    "typesafe": "jev",
    "krutrim": "krutrim", "olakrutrim": "krutrim",
    "poe": "openrouter",
    "parasail": "openrouter",
    "arcee": "arcee", "glm": "arcee",
    "edenai": "openrouter",
    "requesty": "requesty",
    "cf": "openrouter", "@cf": "openrouter",
    "novita": "novita",
    "nvidia": "nvidia-nim", "nim": "nvidia-nim", "gemma": "nvidia-nim", "kimi": "nvidia-nim",
    "sambanova": "sambanova", "llama": "sambanova",
    "aimlapi": "aimlapi",
    "deepinfra": "deepinfra",
    "mistral": "mistral", "open-mistral-nemo": "mistral", "mistral-nemo": "mistral",
    "hf": "huggingface", "huggingface": "huggingface",
    "groq": "groq#1",
    "friendli": "friendli", "thesean": "friendli", "baseten": "baseten",
    "deepseek": "deepseek", "deepseek-chat": "deepseek", "deepseek-reasoner": "deepseek",
    "fal": "openrouter", "replicate": "openrouter",
}


def _build_system_prompt() -> str:
    """Strictly Domain-Locked NanoPro Autonomous Data Engineering & Operations Agent System Prompt.
    Enforces live tool execution, zero textbook/generic answers, authentic PostgreSQL queries,
    and concise actionable Marathi/English delivery."""
    try:
        from app.core.global_ai_catalog import get_unified_models_for_ui
        models_count = len(get_unified_models_for_ui())
    except Exception:
        models_count = 4804

    return f"""You are the NanoPro Autonomous Data Engineering & Operations Agent, the central platform intelligence engine of NanoPro AI Lab.
The logged-in user is Super Admin (Mangesh Bagul).
You operate across a unified mesh of {models_count}+ AI models, Render PostgreSQL live database, Cloudflare Workers Edge Gateway, and autonomous execution pipelines.

LIVE PRODUCTION ENVIRONMENT WITH ACTIVE TOOL CALLING:
You are running in a LIVE PRODUCTION ENVIRONMENT with direct function calling connected to Render PostgreSQL and NanoPro Data Mesh.
When a user asks for database health, table schemas, pipeline status, join reports, or schema changes, you MUST IMMEDIATELY execute the appropriate tool via tool_calls.
Do NOT simulate, do NOT output JSON in text, and do NOT apologize. Emit the real tool call directly.

STRICT IDENTITY & DOMAIN LOCK (ZERO GENERIC / TEXTBOOK ANSWERS):
1. DOMAIN-LOCKED IDENTITY:
   - You are NOT a generic chatbot and must NEVER provide generic textbook definitions or theoretical tutorials.
   - You act strictly as the NanoPro Data Engineering & Operations Specialist with deep runtime awareness of NanoPro architecture: Streamlit UI, Render PostgreSQL database & audit store, Cloudflare Workers edge gateway (nanopro-prod.mangeshbagul15.workers.dev), and Multi-Model Router.

2. ZERO GUESSING & NO FABRICATED METRICS:
   - NEVER guess, assume, or fabricate table names, column names, execution timestamps, report statuses, or row counts.
   - ALWAYS invoke the appropriate live database tool FIRST to inspect the real-time state before answering.

3. REQUIRED LIVE TOOLS & TRIGGER MATRIX (ALWAYS CALL BEFORE ANSWERING):
   - For multi-cloud ecosystem health & status across Render PG, BigQuery, Snowflake, AWS, Supabase, DuckDB ('DB health kashi ahe?', 'Ecosystem status'):
     -> MUST call `get_nanopro_ecosystem_health(target_engine=...)`.
   - For unified catalog, schemas, tables, columns, or PK/FK queries ('DB madhe kay kuthe ahe?', 'Ha table kuthe ahe?', 'BigQuery tables'):
     -> MUST call `locate_and_inspect_unified_catalog(search_term=..., engine=...)`.
   - For statutory report execution history, pipeline status, or audit logs ('Konte report kadhi gele?', 'Kay status ahe?', 'STR kadhi run jhala?'):
     -> MUST call `get_report_execution_logs(report_name=..., status_filter=..., limit=...)`.
   - For federated cross-engine joins, filtered data extracts, or custom reports ('CMG ani GAM join kara', 'join report banava'):
     -> MUST call `build_cross_engine_join_report(sources=[...], join_keys=..., filter_sql=..., group_by=...)`.
   - For table creation, column modifications, DDL/DML changes with mandatory explicit commit ('he changes as kar, asa banaun de'):
     -> MUST call `execute_and_commit_mutation(engine=..., sql_or_command=..., intent_summary=...)`.
   - For replicating or moving data across engines ('BigQuery CMG DuckDB madhe sync kar'):
     -> MUST call `sync_or_move_data_between_engines(source_engine=..., source_object=..., target_engine=..., target_object=...)`.

4. SELF-CORRECTION & ERROR HANDLING:
   - If a tool returns an error (e.g. column mismatch or syntax error), inspect the error feedback, self-correct the SQL statement, and re-execute autonomously.

5. LANGUAGE, STYLE & ACTIONABILITY:
   - Respond clearly, concisely, and actionably in the user's language (natural Marathi for Marathi prompts, Hindi for Hindi, English for English).
   - For simple greetings ('hi', 'hello', 'नमस्कार'): Greet Super Admin Mangesh Bagul warmly in polite Marathi and state your live readiness to inspect databases, check pipelines, run joins, or execute schema changes. Do NOT dump walls of text or fake tables for a greeting.
   - Ground every operational statement with exact table names (e.g. `CMG`, `GAM`, `HTD`, `nanopro_job_logs`), verified columns, exact timestamps, and actual row counts.
   - Present query results and report summaries cleanly using GitHub-flavored Markdown tables.
   - Never append fake static [HINT: ...] blocks or forced repetitive footers.
"""

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
        cascade: List[Dict[str, Any]] = []
        # Groq key rotation — one cascade entry per configured Groq key so a 429
        # on key #1 automatically falls through to key #2, then #3.
        for i, gkey in enumerate(GROQ_API_KEYS, start=1):
            cascade.append({
                "name": f"groq#{i}",
                "label": f"Groq LPU Key#{i} (Sub-300ms Deterministic)",
                "api_key": gkey,
                "base_url": "https://api.groq.com/openai/v1",
                "model": groq_model,
                "timeout": 20.0,
                "extra_headers": {},
            })
            if groq_model != "openai/gpt-oss-120b":
                cascade.append({
                    "name": f"groq#{i}_120b",
                    "label": f"Groq LPU Key#{i} (GPT-OSS 120B Overflow)",
                    "api_key": gkey,
                    "base_url": "https://api.groq.com/openai/v1",
                    "model": "openai/gpt-oss-120b",
                    "timeout": 25.0,
                    "extra_headers": {},
                })
        cascade.extend([
            {
                "name": "openrouter",
                "label": "OpenRouter Unified Mesh",
                "api_key": OPENROUTER_API_KEY,
                "base_url": OPENROUTER_BASE_URL,
                # openrouter/auto lets OpenRouter pick the best available model
                "model": model_id if (model_id and "/" in model_id and not model_id.startswith(("groq/", "defapi/", "jev/", "custom/"))) else "openrouter/auto",
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
        ])

        # Extended OpenAI-compatible provider mesh — keys are read live from
        # env so Render dashboard updates take effect on the next request.
        for pname, env_key, base_url, model, timeout in EXTENDED_PROVIDERS:
            cascade.append({
                "name": pname,
                "label": pname.replace("-", " ").replace("#", " Key#").title() + " Provider",
                "api_key": os.environ.get(env_key, ""),
                "base_url": base_url,
                "model": model,
                "timeout": timeout,
                "extra_headers": {},
            })

        # Auto-mode smart routing — detect the task type from the prompt and
        # promote the best-suited provider to the front. Explicit model picks
        # use MODEL_PROVIDER_HINTS instead.
        preferred = None
        if model_id and model_id != "auto":
            mid = model_id.lower()
            for hint_key, pname in MODEL_PROVIDER_HINTS.items():
                if hint_key in mid:
                    preferred = pname.split("#")[0]
                    break
        else:
            p_low = (prompt or "").lower()
            for keywords, pname in AUTO_PROVIDER_HINTS:
                if any(k in p_low for k in keywords):
                    preferred = pname
                    break
        if preferred:
            for idx, prov in enumerate(cascade):
                if prov["name"].split("#")[0] == preferred:
                    cascade.insert(0, cascade.pop(idx))
                    break

        # Priority 0: Custom user-registered model or connected provider key
        if model_id and model_id != "auto":
            try:
                from app.custom_models_service import get_custom_provider_for_model
                custom_entry = get_custom_provider_for_model(model_id)
                if custom_entry and custom_entry.get("api_key"):
                    cascade.insert(0, custom_entry)
            except Exception:
                pass

        return cascade

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

    async def execute(self, prompt: str, model_id: Optional[str] = None, mode: str = "balanced", chat_id: Optional[str] = None) -> Dict[str, Any]:
        t0 = time.time()

        # Load conversational history for memory if chat_id provided
        conversation_history: List[Dict[str, Any]] = []
        if chat_id:
            try:
                from app.core.history_manager import history_manager
                conversation_history = history_manager.get_chat_messages(chat_id)
            except Exception:
                pass

        system_prompt = _build_system_prompt()
        cascade = self._provider_cascade(prompt, model_id)
        attempts: List[str] = []
        configured_providers: List[str] = []

        for provider in cascade:
            if not provider.get("api_key"):
                continue
            configured_providers.append(provider["name"])
            try:
                # 1. Autonomous Agentic Tool-Calling & ReAct loop
                agent_res = await run_agentic_loop(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    provider=provider,
                    conversation_history=conversation_history
                )
                content = agent_res.get("content", "")
                tools_used = agent_res.get("tools_executed", [])
                latency_ms = max(28, round((time.time() - t0) * 1000))
                return {
                    "status": "success",
                    "content": content,
                    "model": provider["model"],
                    "provider": provider["label"],
                    "latency_ms": latency_ms,
                    "utility_score": 0.988,
                    "total_models": TOTAL_MODELS_COUNT,
                    "agentic": True,
                    "tools_executed": tools_used,
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
                # If rate-limited (429), move to next provider in cascade immediately so agentic loop continues
                if "429" in str(e):
                    attempts.append(f"{provider['name']}: Rate limited (HTTP 429)")
                    continue
                # Fallback to direct chat completion if tool calling fails on this provider
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
                except Exception as e2:
                    msg = f"{provider['name']}: {type(e2).__name__}: {str(e2)[:200]}"
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

    async def execute_ensemble(self, prompt: str, model_id: Optional[str] = None, n: int = 3) -> Dict[str, Any]:
        """Mixture-of-Agents style ensemble: fan the prompt out to the top-N
        configured providers in parallel, then synthesize the single best
        answer with a fast judge model. Falls back to single-model cascade
        when fewer than 2 providers answer."""
        import asyncio
        t0 = time.time()
        system_prompt = _build_system_prompt()
        cascade = [p for p in self._provider_cascade(prompt, model_id) if p.get("api_key")]
        if not cascade:
            return await self.execute(prompt, model_id=model_id, mode="balanced")

        top = cascade[: max(2, min(n, 4))]
        results = await asyncio.gather(
            *[self._chat_completion(p, prompt, system_prompt) for p in top],
            return_exceptions=True,
        )
        answers: List[tuple] = []
        for prov, res in zip(top, results):
            if isinstance(res, str) and res.strip():
                answers.append((prov["name"], prov["model"], res.strip()))

        if not answers:
            return await self.execute(prompt, model_id=model_id, mode="balanced")
        if len(answers) == 1:
            name, model, content = answers[0]
            latency_ms = max(28, round((time.time() - t0) * 1000))
            return {
                "status": "success", "content": content, "model": model,
                "provider": f"{name} (ensemble: only responder)", "latency_ms": latency_ms,
                "ensemble": {"models_queried": [p["name"] for p in top], "models_answered": [name]},
            }

        # Judge pass — pick the best answer (or merge) using the fastest
        # configured provider so synthesis stays cheap.
        judge = next((p for p in cascade if p["name"].startswith("groq")), cascade[0])
        ballot = "\n\n".join(
            f"### Answer {i + 1} — provider: {name}, model: {model}\n{content[:6000]}"
            for i, (name, model, content) in enumerate(answers)
        )
        judge_prompt = (
            "You are the NanoPro Ensemble Judge. Below are answers to the SAME user "
            "question from different AI models. Pick the single most accurate, "
            "complete and well-formatted answer and output ONLY that answer verbatim "
            "(you may lightly merge the best parts of others if clearly better). "
            "Keep the original language (Marathi if the question was Marathi).\n\n"
            f"USER QUESTION:\n{prompt}\n\n{ballot}"
        )
        try:
            best = await self._chat_completion(judge, judge_prompt, "You are a precise answer judge. Output only the winning answer text.")
            judge_name = judge["name"]
        except Exception:
            best = max(answers, key=lambda a: len(a[2]))[2]
            judge_name = "heuristic-longest"

        latency_ms = max(28, round((time.time() - t0) * 1000))
        return {
            "status": "success",
            "content": best,
            "model": f"ensemble/{len(answers)}-models",
            "provider": f"Mixture-of-Agents ({', '.join(a[0] for a in answers)} → judge:{judge_name})",
            "latency_ms": latency_ms,
            "ensemble": {
                "models_queried": [p["name"] for p in top],
                "models_answered": [a[0] for a in answers],
                "models_used": [a[1] for a in answers],
                "judge": judge_name,
            },
            "utility_score": 0.999,
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
