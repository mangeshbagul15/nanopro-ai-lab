import os
import sys
import re
from datetime import datetime

# Enforce UTF-8 on Windows
if sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

print("=== 1. Testing System Prompt Temporal Grounding (2026) ===")
from nanopro_db_agent import build_enterprise_system_prompt
sys_prompt = build_enterprise_system_prompt()
assert "2026" in sys_prompt, "System prompt must contain the year 2026"
assert "Asia/Kolkata" in sys_prompt or "IST" in sys_prompt, "System prompt must specify IST timezone"
assert "ZERO-HALLUCINATION" in sys_prompt, "System prompt must enforce zero-hallucination mandate"
assert "2024" in sys_prompt and "NEVER" in sys_prompt, "System prompt must explicitly forbid 2024 dates"
print("PASS: System prompt is strongly grounded to current IST date (Year 2026) and strictly forbids 2024 hallucination.")

print("\n=== 2. Testing Model Router (Marathi / Hinglish, < 3000ms, Blacklist nemo) ===")
from nanopro_db_agent import select_optimal_model, UCBModelRouter

# Test Marathi queries
test_marathi_queries = [
    "konte reports nanopro madhun generate hotat",
    "DB health kashi ahe?",
    "मला AML रिपोर्ट दाखवा",
    "कोणते टेबल्स उपलब्ध आहेत?"
]

for q in test_marathi_queries:
    route = select_optimal_model(q)
    model = route["recommended_model"]
    cat = route["category"]
    sla = route.get("latency_budget_ms", 2500)
    print(f"  Prompt: '{q}' -> Model: {model} | Category: {cat} | Latency SLA: {sla}ms")
    assert cat == "MARATHI_OPERATIONAL", f"Expected MARATHI_OPERATIONAL, got {cat}"
    assert model not in UCBModelRouter.BLACKLISTED_MODELS, f"Model {model} must not be blacklisted"
    assert "nemo" not in model.lower(), f"Nemo model must not be selected: {model}"
    assert sla <= 3000, f"SLA latency budget must be <= 3000ms, got {sla}"
    assert model in ["llama-3.3-70b-versatile", "google/gemini-2.5-flash", "qwen/qwen-2.5-72b-instruct", "claude-3-5-sonnet"], f"Invalid model: {model}"

print("PASS: Marathi/Hinglish routing selects ultra-fast high-accuracy models with strict < 3000ms SLA and blacklists open-mistral-nemo.")

print("\n=== 3. Testing Supabase Auth Error Accuracy (No Fake ONLINE on 401) ===")
from nanopro_connectors import SupabaseConnector
from nanopro_db_agent import get_nanopro_ecosystem_health

supa_health = SupabaseConnector.ping_health()
print(f"  Supabase direct ping: status={supa_health.get('status')}, code={supa_health.get('http_code')}")
assert supa_health.get("http_code") == 401, "Expected Supabase HTTP 401 with publishable/invalid key"
assert "AUTH_ERROR" in supa_health.get("status"), f"Status must be AUTH_ERROR, got {supa_health.get('status')}"
assert "ONLINE" not in supa_health.get("status"), "Status must NOT be falsely masked as ONLINE on 401"

eco_health = get_nanopro_ecosystem_health("ALL")
supa_eco = eco_health["ecosystem_health"]["Supabase DB"]
print(f"  Ecosystem health Supabase: status={supa_eco.get('status')}")
assert "AUTH_ERROR" in supa_eco.get("status"), f"Ecosystem Supabase status must report AUTH_ERROR, got {supa_eco.get('status')}"
assert len(eco_health.get("alerts", [])) > 0, "Expected at least 1 alert for Supabase 401"
print(f"  Ecosystem Alerts: {eco_health.get('alerts')}")
print("PASS: Supabase HTTP 401 is accurately reported as AUTH_ERROR (401 - Check SUPABASE_KEY) and flagged in alerts.")

print("\n=== 4. Testing Report Execution Logs & Lineage (2026 Timestamps & 0-row fallback) ===")
from nanopro_db_agent import get_report_execution_logs, inspect_report_history_and_lineage

# Test normal logs retrieval
report_res = get_report_execution_logs()
assert report_res["status"] == "success", f"Expected success, got {report_res['status']}"
assert len(report_res["recent_execution_runs"]) > 0, "Expected live execution runs"
for r in report_res["recent_execution_runs"]:
    ex_at = str(r.get("executed_at", ""))
    assert "2026" in ex_at, f"Timestamp must be in 2026, got: {ex_at}"
    assert "2024" not in ex_at, f"Must never contain 2024 date: {ex_at}"
print(f"  Verified {len(report_res['recent_execution_runs'])} live execution logs with 2026 timestamps!")

# Test 0-logs condition with non-existent report
empty_res = get_report_execution_logs(report_name="NON_EXISTENT_REPORT_XYZ")
print(f"  0-logs status: {empty_res.get('status')}")
assert empty_res["status"] == "NO_EXECUTION_LOGS_YET", f"Expected NO_EXECUTION_LOGS_YET, got {empty_res['status']}"
assert "NEVER invent" in empty_res.get("instruction_for_llm", ""), "Instruction must tell LLM to never invent dates"
print("PASS: 0-logs query returns explicit NO_EXECUTION_LOGS_YET payload with strict anti-hallucination instruction.")

print("\n=== 5. Testing Response Sanitization (Strip <details> & Robotic 'काय करावे?') ===")
from nanopro_db_agent import clean_and_sanitize_response

dirty_sample = """<details style="background: rgba(16, 185, 129, 0.08);">
<summary>⚙️ Inspecting Render PostgreSQL</summary>
<div>• Tool: locate_medallion</div>
</details>

### 📊 NanoPro अहवाल तालिका (2026)

| अहवाल नाव (Report Name) | वेळापत्रक (Schedule) | स्थिती (Status) |
|---|---|---|
| AML_STR_DAILY_RUN | 06:00 BOD | SUCCESS |
| CTR_MONTHLY_AGG | 08:00 SOD | SUCCESS |
| CRILC_LARGE_EXPOSURES | 11:00 T1 | SUCCESS |

काय करावे? 1. कंटी रिपोर्टची तपासणी करा आणि मेल तपासा."""

cleaned = clean_and_sanitize_response(dirty_sample)
print("Sanitized Output:\n" + cleaned)

assert "<details" not in cleaned, "Raw <details> tag must be removed"
assert "</details>" not in cleaned, "Raw </details> tag must be removed"
assert "काय करावे?" not in cleaned, "Robotic closing boilerplate must be stripped"
assert "| अहवाल नाव (Report Name) | वेळापत्रक (Schedule) | स्थिती (Status) |" in cleaned, "Markdown table must remain intact"
assert "|---|---|---|" in cleaned, "Markdown table structure must remain intact"
print("PASS: Response sanitization cleanly removes raw HTML details tags, strips robotic closing boilerplate, and preserves table rendering.")

print("\n=== ALL 5 CRITICAL HALLUCINATION, DATE, ROUTING & UI BUGS VERIFIED FIXED 100%! ===")
