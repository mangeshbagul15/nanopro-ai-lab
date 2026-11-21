import os
import sys
import json
import time

sys.path.insert(0, os.path.dirname(__file__))

def run_tests():
    print("=== STARTING USER MANAGEMENT & PERSISTENCE TEST SUITE ===")

    from app.auth_manager import auth_manager
    from app.history_manager import history_manager
    from nanopro_connectors import DuckDBFederatedConnector, ChatPersistenceConnector

    # 1. Test User Registration & DB Mirroring
    test_user_a = f"testuser_{int(time.time())}"
    test_pwd = "TestPassword@123"
    test_email_a = f"{test_user_a}@nanopro.ai"

    print(f"\n[Test 1] Registering test user '{test_user_a}'...")
    reg_res = auth_manager.register_user(
        username=test_user_a,
        password=test_pwd,
        full_name="Test User A",
        email=test_email_a
    )
    assert reg_res["status"] == "success", f"Registration failed: {reg_res}"
    print("  -> User registration SUCCESS")

    # 2. Test User Login & Session Persistence
    print(f"\n[Test 2] Logging in user '{test_user_a}'...")
    login_res = auth_manager.authenticate_user(username=test_user_a, password=test_pwd)
    assert login_res["status"] == "success", f"Login failed: {login_res}"
    token_a = login_res["session_token"]
    user_id_a = login_res["user"]["id"]
    print(f"  -> Login SUCCESS, session token: {token_a[:15]}...")

    # Verify session is mirrored into DuckDB
    dcon = DuckDBFederatedConnector.get_connection(read_only=True)
    drow = dcon.execute("SELECT session_token, username FROM nanopro_user_sessions WHERE session_token = ?", (token_a,)).fetchone()
    dcon.close()
    assert drow is not None, "Session not found in DuckDB nanopro_user_sessions!"
    print(f"  -> Session confirmed in DuckDB: {drow}")

    # 3. Test Session Validation
    print("\n[Test 3] Validating session token...")
    val_res = auth_manager.validate_session(token_a)
    assert val_res["status"] == "success" and val_res["valid"], f"Validation failed: {val_res}"
    assert val_res["user"]["username"] == test_user_a, "Username mismatch in validation!"
    print(f"  -> Validated for user: {val_res['user']['username']}")

    # 4. Test Chat Creation & Full-Turn Persistence for User A
    print(f"\n[Test 4] Creating chat session for '{test_user_a}'...")
    chat_a = history_manager.create_chat(
        title="AML Transaction Audit 2026",
        project_id="proj_01",
        model="auto",
        user_key=test_user_a
    )
    chat_id_a = chat_a["chat_id"]
    print(f"  -> Created chat_id: {chat_id_a}")

    # Add User Message
    history_manager.add_message(
        chat_id=chat_id_a,
        role="user",
        content="AML alerts madhil total high risk cases kiti ahet?",
        user_key=test_user_a
    )

    # Add Assistant Message with full tools and dataframe
    sample_tools = [
        {"tool": "inspect_live_postgresql_catalog", "result_status": "SUCCESS"},
        {"tool": "query_bronze_lakehouse_aggregates", "result_status": "SUCCESS"}
    ]
    sample_df = {"columns": ["case_id", "severity", "amount"], "rows": [["C101", "HIGH", 500000]]}

    history_manager.add_message(
        chat_id=chat_id_a,
        role="assistant",
        content="2026 नुसार उच्च-जोखीम असणाऱ्या एकूण **48** केसेस आढळल्या आहेत.\n\n| Case ID | Severity | Amount |\n| --- | --- | --- |\n| C101 | HIGH | ₹5,00,000 |",
        model_routed="google/gemini-2.5-flash",
        model_executed="google/gemini-2.5-flash",
        duration_ms=420.5,
        routing_math=json.dumps({"pareto_utility": 0.985, "task_domain": "AML Analytics"}),
        tool_logs_json=json.dumps(sample_tools),
        dataframe_json=json.dumps(sample_df),
        user_key=test_user_a
    )
    print("  -> Full turn (User + Assistant) saved to database")

    # 5. Test Retrieval for User A
    print(f"\n[Test 5] Fetching messages for chat '{chat_id_a}'...")
    msgs_a = history_manager.get_chat_messages(chat_id_a, user_key=test_user_a)
    assert len(msgs_a) >= 2, f"Expected at least 2 messages, got {len(msgs_a)}"
    assert msgs_a[0]["role"] == "user", f"Turn 0 role: {msgs_a[0]['role']}"
    assert msgs_a[1]["role"] == "assistant", f"Turn 1 role: {msgs_a[1]['role']}"
    assert "48" in msgs_a[1]["content"], "Content missing expected text!"
    assert msgs_a[1].get("tool_logs_json") or msgs_a[1].get("tool_executions"), "Tool logs missing!"
    print(f"  -> Successfully retrieved {len(msgs_a)} full-turn messages with tools and tables!")

    # 6. Test User Scoping (User B cannot see User A's chat list)
    test_user_b = f"user_b_{int(time.time())}"
    print(f"\n[Test 6] Testing User Isolation for '{test_user_b}' vs '{test_user_a}'...")
    auth_manager.register_user(username=test_user_b, password=test_pwd, full_name="User B", email=f"{test_user_b}@nanopro.ai")
    
    # User B list
    chats_b = history_manager.list_chats_and_projects(user_key=test_user_b)
    user_b_chat_ids = [c["id"] for c in chats_b["chats"]]
    assert chat_id_a not in user_b_chat_ids, f"User B should NOT see User A's chat ({chat_id_a})!"
    print(f"  -> Isolation CONFIRMED: User B sees {len(user_b_chat_ids)} chats, none of User A's!")

    # User A list
    chats_a = history_manager.list_chats_and_projects(user_key=test_user_a)
    user_a_chat_ids = [c["id"] for c in chats_a["chats"]]
    assert chat_id_a in user_a_chat_ids, f"User A should see their own chat ({chat_id_a})!"
    print(f"  -> User A sees their own chat: CONFIRMED ({chat_id_a} present in {len(user_a_chat_ids)} chats)")

    # 7. Test Admin Scoping (Admin sees all chats)
    print("\n[Test 7] Testing Admin visibility...")
    chats_admin = history_manager.list_chats_and_projects(user_key="admin")
    admin_chat_ids = [c["id"] for c in chats_admin["chats"]]
    assert chat_id_a in admin_chat_ids, "Admin should see all chats!"
    print(f"  -> Admin visibility CONFIRMED: {len(admin_chat_ids)} chats visible to Super Admin")

    print("\n=== ALL TESTS PASSED: 100% PERSISTENCE, SCOPING & FULL-TURN RESTORATION VERIFIED ===")

if __name__ == "__main__":
    run_tests()
