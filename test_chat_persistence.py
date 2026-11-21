import time
import json
from nanopro_connectors import ChatPersistenceConnector
from app.history_manager import history_manager

print("=== 1. Testing ChatPersistenceConnector Initialization ===")
ChatPersistenceConnector.init_tables()
print("Chat persistence tables initialized across DuckDB & Render PG.")

# Generate test session and project
test_session_id = f"sess_verify_{int(time.time()*1000)}"
test_project_id = "proj_01"

print(f"\n=== 2. Testing Turn 1: User Submission (Immediate Save & Commit) ===")
user_prompt_1 = "Check AML report delivery status on Email, Telegram and WhatsApp"
res_u1 = ChatPersistenceConnector.save_message(
    session_id=test_session_id,
    role="user",
    content=user_prompt_1,
    project_id=test_project_id
)
assert res_u1["status"] == "success", f"User save failed: {res_u1}"
assert res_u1["committed"] is True, "Explicit commit not confirmed"
print(f"User turn 1 saved & committed! Msg ID: {res_u1['message_id']}")

print(f"\n=== 3. Testing Turn 1: Assistant Response (Full-Turn Save & Commit) ===")
assistant_reply_1 = """### 📬 Multi-Channel Notification Delivery Status

AML_STR_DAILY_RUN report delivery has been verified:
- **Email:** `compliance-officer@bank.com` — DELIVERED ✅
- **Telegram:** `@nanopro_fiu_alerts_bot` — DELIVERED ✅
- **WhatsApp:** `+919822012345` — DELIVERED ✅"""

tool_logs_1 = [
    {"tool": "check_and_send_notification_deliveries", "result_status": "SUCCESS", "records_found": 3}
]
model_used_1 = "qwen/qwen3.8-27b"
dur_1 = 38.5

res_a1 = ChatPersistenceConnector.save_message(
    session_id=test_session_id,
    role="assistant",
    content=assistant_reply_1,
    project_id=test_project_id,
    tool_logs=tool_logs_1,
    dataframe={"filename": "AML_DELIVERY_AUDIT.csv", "rows": 3},
    model_used=model_used_1,
    duration_ms=dur_1,
    routing_math={"pareto_utility": 0.985, "model": model_used_1}
)
assert res_a1["status"] == "success", f"Assistant save failed: {res_a1}"
assert res_a1["committed"] is True, "Explicit commit not confirmed"
print(f"Assistant turn 1 saved & committed! Msg ID: {res_a1['message_id']}")

print(f"\n=== 4. Testing Turn 2: Continuing Multi-Turn Conversation ===")
user_prompt_2 = "Now show the underlying CMG and GAM table catalog"
res_u2 = ChatPersistenceConnector.save_message(
    session_id=test_session_id,
    role="user",
    content=user_prompt_2,
    project_id=test_project_id
)

assistant_reply_2 = """### 📚 Medallion Catalog: CMG & GAM

| Table Name | Layer | Engine | Rows |
|---|---|---|---|
| `CMG` | L1_CURATED | Render PostgreSQL | 95 |
| `GAM` | L1_CURATED | Render PostgreSQL | 95 |"""

tool_logs_2 = [
    {"tool": "locate_and_inspect_medallion_catalog", "result_status": "SUCCESS", "tables": ["CMG", "GAM"]}
]
model_used_2 = "openai/gpt-oss-120b"
dur_2 = 142.0

res_a2 = ChatPersistenceConnector.save_message(
    session_id=test_session_id,
    role="assistant",
    content=assistant_reply_2,
    project_id=test_project_id,
    tool_logs=tool_logs_2,
    model_used=model_used_2,
    duration_ms=dur_2
)
print("Turn 2 saved successfully!")

print(f"\n=== 5. Testing Live Full-Conversation Restore on Click ===")
restored_messages = ChatPersistenceConnector.get_session_messages(test_session_id)
assert len(restored_messages) == 4, f"Expected 4 messages, got {len(restored_messages)}"

print(f"Successfully restored {len(restored_messages)} messages in chronological order:")
for i, m in enumerate(restored_messages):
    safe_content = m['content'][:45].encode('ascii', 'replace').decode('ascii')
    print(f"  [{i+1}] Role: {m['role']:<9} | Model: {m.get('model_used', ''):<22} | Tools: {len(m.get('tool_executions', []))} | Content: {safe_content}...")

# Verify complete content integrity
assert restored_messages[0]["role"] == "user"
assert restored_messages[0]["content"] == user_prompt_1

assert restored_messages[1]["role"] == "assistant"
assert restored_messages[1]["model_used"] == model_used_1
assert len(restored_messages[1]["tool_executions"]) == 1
assert restored_messages[1]["tool_executions"][0]["tool"] == "check_and_send_notification_deliveries"
assert restored_messages[1]["csv_download"]["filename"] == "AML_DELIVERY_AUDIT.csv"

assert restored_messages[2]["role"] == "user"
assert restored_messages[2]["content"] == user_prompt_2

assert restored_messages[3]["role"] == "assistant"
assert restored_messages[3]["model_used"] == model_used_2
assert len(restored_messages[3]["tool_executions"]) == 1

print("\nAll restored fields (roles, full content, model badges, tool execution logs, dataframe CSV) match perfectly!")

print(f"\n=== 6. Testing Dynamic Live Sessions Listing ===")
history_view = ChatPersistenceConnector.list_sessions_and_projects()
sessions = history_view["sessions"]
matching_sess = next((s for s in sessions if s["session_id"] == test_session_id), None)
assert matching_sess is not None, "Newly created session not found in live session listing!"
assert matching_sess["message_count"] >= 4, f"Expected message count >= 4, got {matching_sess['message_count']}"
print(f"Dynamic session found in live DB! Title: '{matching_sess['title']}' | Msg Count: {matching_sess['message_count']}")

print(f"\n=== 7. Testing FastAPI / Web History Manager Roundtrip ===")
from main import app, MessageCreateRequest
from fastapi.testclient import TestClient

client = TestClient(app)
web_msg_payload = {
    "chat_id": test_session_id,
    "role": "assistant",
    "content": "FastAPI Web Assistant Response",
    "model_routed": "groq/qwen3.8-27b",
    "model_executed": "qwen/qwen3.8-27b",
    "duration_ms": 32.5,
    "routing_math": {"pareto_utility": 0.992, "shannon_entropy": 1.45},
    "tool_logs_json": [{"tool": "test_web", "status": "OK"}]
}
res_web = client.post("/api/ai/history/messages", json=web_msg_payload)
assert res_web.status_code == 200, f"Web history endpoint failed: {res_web.status_code} - {res_web.text}"
print(f"FastAPI /api/ai/history/messages accepted complex routing_math dict without 422 error! Response: {res_web.json()}")

print("\n=== ALL CHATS & PROJECTS PERSISTENCE TESTS PASSED 100%! ===")
