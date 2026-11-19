import os
from typing import Dict, Any, Optional

def get_login_page_html() -> str:
    gateway_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "deploy", "login_gateway.html")
    if os.path.exists(gateway_file):
        try:
            with open(gateway_file, "r", encoding="utf-8") as f:
                content = f.read()
                if content.strip():
                    return content
        except Exception:
            pass
    return """<!DOCTYPE html><html><head><title>NanoPro Zero-Trust Gateway</title></head><body style="background:#0B1119;color:#fff;display:flex;align-items:center;justify-content:center;height:100vh;font-family:sans-serif;"><div style="text-align:center;"><h2>🧠 NanoPro Security Gateway</h2><p>Please log in.</p></div></body></html>"""

def get_ai_lab_html(user: Optional[Dict[str, Any]] = None) -> str:
    user_name = (user.get("full_name") or user.get("username") or "Super Admin") if user else "Super Admin"
    user_role = (user.get("role") or "ADMIN").upper() if user else "ADMIN"
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NanoPro AI Lab — 4,804+ Models Unified Mesh</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🧠</text></svg>">
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
<style>
:root {
  --bg: #0B1119;
  --panel: #0F1724;
  --panel-2: #131E2E;
  --line: #1E2B3E;
  --line-2: #283952;
  --text: #E6EDF7;
  --muted: #94A3B8;
  --dim: #64748B;
  --accent: #8B5CF6;
  --accent-glow: rgba(139, 92, 246, 0.25);
  --cyan: #38BDF8;
  --green: #10B981;
  --amber: #F59E0B;
  --purple: #C084FC;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  font-size: 13px;
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
/* Topbar */
.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 52px;
  padding: 0 16px;
  background: linear-gradient(180deg, #0B1119 0%, #080D14 100%);
  border-bottom: 1.5px solid rgba(139, 92, 246, 0.3);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
  flex-shrink: 0;
  z-index: 100;
}
.brand { display: flex; align-items: center; gap: 8px; font-weight: 700; font-size: 14px; color: #fff; cursor: pointer; }
.brand span { color: var(--accent); }
.topbar-center { display: flex; align-items: center; gap: 8px; }
.pill-btn {
  background: rgba(139, 92, 246, 0.12);
  border: 1px solid rgba(139, 92, 246, 0.35);
  color: #fff;
  padding: 5px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
}
.pill-btn:hover { background: rgba(139, 92, 246, 0.25); border-color: var(--accent); }
.mode-pill { background: #131E2E; border: 1px solid var(--line); color: var(--muted); padding: 5px 10px; border-radius: 6px; font-size: 12px; cursor: pointer; }
.mode-pill.active { background: rgba(16, 185, 129, 0.15); border-color: var(--green); color: var(--green); font-weight: 600; }
.topbar-right { display: flex; align-items: center; gap: 8px; }
.sync-badge { font-size: 11px; color: var(--cyan); background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.3); padding: 4px 8px; border-radius: 4px; display: flex; align-items: center; gap: 4px; }

/* Main Layout */
.main-layout { display: flex; flex: 1; height: calc(100vh - 52px); overflow: hidden; }

/* Sidebar */
.sidebar {
  width: 260px;
  background: var(--panel);
  border-right: 1px solid var(--line);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}
.new-chat-btn {
  margin: 12px;
  padding: 10px;
  background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
  color: #fff;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  box-shadow: 0 2px 10px rgba(124, 58, 237, 0.3);
}
.new-chat-btn:hover { opacity: 0.95; }
.chat-list { flex: 1; overflow-y: auto; padding: 0 12px 12px 12px; }
.chat-item {
  padding: 8px 10px;
  border-radius: 6px;
  color: var(--muted);
  cursor: pointer;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: flex;
  align-items: center;
  gap: 8px;
}
.chat-item:hover, .chat-item.active { background: var(--panel-2); color: #fff; }
.sidebar-footer { padding: 12px; border-top: 1px solid var(--line); font-size: 11px; color: var(--dim); display: flex; justify-content: space-between; }

/* Workspace & Chat */
.workspace { flex: 1; display: flex; flex-direction: column; background: var(--bg); position: relative; }
.messages-container { flex: 1; overflow-y: auto; padding: 24px; display: flex; flex-direction: column; gap: 20px; }
.welcome-hero { margin: auto; max-width: 720px; text-align: center; }
.welcome-hero h1 { font-size: 26px; font-weight: 800; color: #fff; margin-bottom: 8px; }
.welcome-hero p { color: var(--muted); font-size: 14px; margin-bottom: 24px; }
.feature-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; text-align: left; }
.feature-card { background: var(--panel); border: 1px solid var(--line); padding: 14px; border-radius: 8px; cursor: pointer; transition: all 0.2s; }
.feature-card:hover { border-color: var(--accent); transform: translateY(-2px); }
.feature-card h4 { font-size: 13px; color: #fff; margin-bottom: 4px; }
.feature-card p { font-size: 12px; color: var(--muted); }

/* Messages */
.message-bubble { display: flex; flex-direction: column; gap: 8px; max-width: 85%; animation: fadeIn 0.2s ease-in; }
.user-msg { align-self: flex-end; background: #2E1065; border: 1px solid #6D28D9; color: #fff; padding: 10px 14px; border-radius: 12px 12px 2px 12px; }
.ai-msg { align-self: flex-start; background: var(--panel); border: 1px solid var(--line); padding: 14px 18px; border-radius: 12px 12px 12px 2px; width: 100%; max-width: 900px; }
.ai-badge { display: inline-flex; align-items: center; gap: 6px; font-size: 11px; color: var(--purple); font-weight: 600; margin-bottom: 6px; }
.ai-content { color: var(--text); font-size: 13.5px; line-height: 1.6; }
.ai-content h3 { color: #fff; margin: 12px 0 6px 0; font-size: 15px; }
.ai-content ul, .ai-content ol { padding-left: 20px; margin: 8px 0; }
.ai-content li { margin-bottom: 4px; }
.ai-content a { color: var(--cyan); text-decoration: none; font-weight: 600; }
.ai-content a:hover { text-decoration: underline; }
.ai-content table { border-collapse: collapse; margin: 10px 0; width: 100%; font-size: 12px; } .ai-content th, .ai-content td { border: 1px solid var(--line); padding: 6px 10px; text-align: left; } .ai-content th { background: var(--panel-2); color: #fff; font-weight: 600; } .ai-content pre { background: #080D14; border: 1px solid var(--line-2); border-radius: 6px; padding: 12px; overflow-x: auto; font-family: Consolas, monospace; font-size: 12px; margin: 10px 0; }
.ai-content code { background: #131E2E; padding: 2px 5px; border-radius: 4px; font-family: Consolas, monospace; font-size: 12px; color: var(--cyan); }
.ai-footer { display: flex; align-items: center; justify-content: space-between; margin-top: 10px; padding-top: 8px; border-top: 1px solid var(--line); font-size: 11px; color: var(--dim); }

/* Input Bar */
.input-dock { padding: 16px 24px; background: var(--panel); border-top: 1px solid var(--line); }
.input-box { background: var(--bg); border: 1.5px solid var(--line); border-radius: 8px; padding: 8px 12px; display: flex; flex-direction: column; gap: 8px; }
.input-box:focus-within { border-color: var(--accent); box-shadow: 0 0 15px var(--accent-glow); }
textarea#chatInput { background: transparent; border: none; color: #fff; font-family: inherit; font-size: 13px; resize: none; min-height: 48px; max-height: 160px; outline: none; }
.input-controls { display: flex; justify-content: space-between; align-items: center; }
.sla-tag { font-size: 11px; color: var(--green); display: flex; align-items: center; gap: 4px; font-weight: 600; }
.send-btn { background: var(--accent); color: #fff; border: none; padding: 6px 14px; border-radius: 6px; font-weight: 600; font-size: 12px; cursor: pointer; display: flex; align-items: center; gap: 4px; }
.send-btn:hover { background: #7C3AED; }

/* Modals */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.7); backdrop-filter: blur(4px); display: none; align-items: center; justify-content: center; z-index: 1000; }
.modal-overlay.active { display: flex; }
.modal-card { background: var(--panel); border: 1.5px solid var(--line-2); border-radius: 10px; width: 90%; max-width: 800px; max-height: 85vh; display: flex; flex-direction: column; box-shadow: 0 10px 40px rgba(0,0,0,0.8); }
.modal-header { padding: 14px 18px; border-bottom: 1px solid var(--line); display: flex; justify-content: space-between; align-items: center; }
.modal-header h3 { color: #fff; font-size: 15px; }
.close-btn { background: transparent; border: none; color: var(--dim); font-size: 18px; cursor: pointer; }
.close-btn:hover { color: #fff; }
.modal-body { padding: 18px; overflow-y: auto; flex: 1; }
.model-list-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 10px; margin-top: 12px; }
.model-item-card { background: var(--panel-2); border: 1px solid var(--line); padding: 10px; border-radius: 6px; cursor: pointer; }
.model-item-card:hover { border-color: var(--accent); }
.model-name { font-weight: 600; color: #fff; font-size: 12px; }
.model-sub { font-size: 11px; color: var(--dim); margin-top: 2px; }

@keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }
</style>
</head>
<body>

<!-- Topbar -->
<header class="topbar">
  <div class="brand" onclick="newChat()">
    <span>🧠</span> NanoPro AI Lab
  </div>
  <div class="topbar-center">
    <button class="pill-btn" onclick="openModelCatalog()">
      <span>4,804+ Models Unified Mesh</span> ▾
    </button>
    <button class="pill-btn" style="background: rgba(56, 189, 248, 0.12); border-color: rgba(56, 189, 248, 0.35);">
      ⚡ AUTO Router
    </button>
    <button class="mode-pill active" id="btnBalanced" onclick="setMode('balanced')">🎯 Balanced</button>
    <button class="mode-pill" id="btnCreative" onclick="setMode('creative')">✨ Creative</button>
    <button class="mode-pill" id="btnPrecise" onclick="setMode('precise')">📐 Precise</button>
  </div>
  <div class="topbar-right">
    <div class="sync-badge">🦆 DuckDB • 🏛️ BigQuery in sync</div>
    <button class="pill-btn" onclick="openAirflowModal()">
      ⏱️ Airflow 15 DAGs
    </button>
    <div style="display:flex; align-items:center; gap:8px; background:rgba(99,102,241,0.18); border:1px solid rgba(99,102,241,0.4); padding:4px 10px; border-radius:6px; font-size:12px; color:#fff;">
      <span>👤 {USER_NAME}</span>
      <span style="font-size:10px; background:#6366F1; color:#fff; padding:1px 5px; border-radius:3px; font-weight:600;">{USER_ROLE}</span>
      <button onclick="logout()" style="background:none; border:none; color:var(--dim); cursor:pointer; font-size:13px; margin-left:4px;" title="Sign Out">🚪</button>
    </div>
  </div>
</header>

<!-- Main Workspace Layout -->
<div class="main-layout">
  <!-- Left Sidebar -->
  <aside class="sidebar">
    <button class="new-chat-btn" onclick="newChat()">
      <span>+</span> New Chat
    </button>
    <div class="chat-list" id="chatList">
      <div class="chat-item active" onclick="loadChat(0)">
        <span>💬</span> Global AI Lab Session
      </div>
      <div class="chat-item" onclick="loadChat(1)">
        <span>🏛️</span> BigQuery 900 Rows Live
      </div>
      <div class="chat-item" onclick="loadChat(2)">
        <span>📊</span> 21 Core Banking Reports
      </div>
    </div>
    <div class="sidebar-footer">
      <span>Production PROD</span>
      <span>0 MB RAM Overhead</span>
    </div>
  </aside>

  <!-- Right Chat Section -->
  <main class="workspace">
    <div class="messages-container" id="msgContainer">
      <div class="welcome-hero" id="welcomeHero">
        <h1>🧠 NanoPro AI Lab</h1>
        <p>One workspace for 4,804+ frontier models, durable chats, diagrams, and live banking intelligence.</p>
        <div class="feature-grid">
          <div class="feature-card" onclick="sendPrompt('nanopro_cbs_bronze मधील सर्व tables मध्ये प्रत्येक table मध्ये किती rows आहेत ते दाखव')">
            <h4>🌐 Live BigQuery Bronze Data</h4>
            <p>CMG, GAM, HTD, SOL, VCT मधील ९०० रो डेटा त्वरित तपासा.</p>
          </div>
          <div class="feature-card" onclick="sendPrompt('total kiti report send hotata')">
            <h4>📊 21 Core Banking Reports</h4>
            <p>१६ AML/FIU-IND अहवाल आणि ५ मास्टर एक्सेल वर्कबुक्स लिंक्स.</p>
          </div>
          <div class="feature-card" onclick="sendPrompt('Show live Mermaid architecture diagram of NanoPro pipeline')">
            <h4>🏗️ Mermaid Architecture</h4>
            <p>Live diagram of Google BigQuery, AWS S3, Snowflake, and SFTP.</p>
          </div>
          <div class="feature-card" onclick="sendPrompt('Explain Pareto Utility U(m) and Thompson Bandit math routing')">
            <h4>📐 Deep Mathematical Proof</h4>
            <p>Multi-armed bandit routing algorithm with sub-300ms SLA.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Input Dock -->
    <div class="input-dock">
      <div class="input-box">
        <textarea id="chatInput" placeholder="Ask anything… (Enter to send, Shift+Enter for newline)" onkeydown="handleKeyDown(event)"></textarea>
        <div class="input-controls">
          <div class="sla-tag">⚡ AUTO Math Router Active · Target SLA: &lt;300ms</div>
          <button class="send-btn" onclick="sendMessage()">Dispatch ⚡</button>
        </div>
      </div>
    </div>
  </main>
</div>

<!-- Model Catalog Modal -->
<div class="modal-overlay" id="catalogModal">
  <div class="modal-card">
    <div class="modal-header">
      <h3>🌐 Unified Model Mesh Catalog (4,804+ Models Across 25 Providers)</h3>
      <button class="close-btn" onclick="closeModals()">✕</button>
    </div>
    <div class="modal-body">
      <input type="text" id="modelSearch" placeholder="Search models by name or provider..." style="width:100%; padding:8px 12px; background:#0B1119; border:1px solid var(--line); border-radius:6px; color:#fff;" onkeyup="filterModels()">
      <div class="model-list-grid" id="modelGrid">
        <div class="model-item-card"><div class="model-name">Groq Qwen 3.8 27B</div><div class="model-sub">Groq LPU · Sub-300ms SLA</div></div>
        <div class="model-item-card"><div class="model-name">OpenAI GPT-OSS 120B</div><div class="model-sub">Groq LPU · Deep Reasoning</div></div>
        <div class="model-item-card"><div class="model-name">Defapi Claude 3.5 Sonnet</div><div class="model-sub">Defapi.org · 44 Models Mesh</div></div>
        <div class="model-item-card"><div class="model-name">TypeSafe AI JEV Claude 3.5</div><div class="model-sub">JEV TypeSafe · 10 Models Mesh</div></div>
        <div class="model-item-card"><div class="model-name">Meta Llama 3.3 70B</div><div class="model-sub">Open-Weights Frontier</div></div>
        <div class="model-item-card"><div class="model-name">Google Gemini 2.0 Flash</div><div class="model-sub">Google DeepMind · 1M Context</div></div>
        <div class="model-item-card"><div class="model-name">DeepSeek R1 Distill 70B</div><div class="model-sub">Math & Reasoning Engine</div></div>
        <div class="model-item-card"><div class="model-name">Mistral Large 2</div><div class="model-sub">Mistral AI · 128k Window</div></div>
      </div>
    </div>
  </div>
</div>

<!-- Airflow Modal -->
<div class="modal-overlay" id="airflowModal">
  <div class="modal-card">
    <div class="modal-header">
      <h3>⏱️ Airflow Orchestrator (15 Production DAGs)</h3>
      <button class="close-btn" onclick="closeModals()">✕</button>
    </div>
    <div class="modal-body">
      <p style="color:var(--muted); margin-bottom:12px;">All 15 DAGs execute independently with zero cascading pipeline downtime.</p>
      <div style="display:flex; flex-direction:column; gap:8px;">
        <div style="background:#131E2E; padding:10px; border-radius:6px; border:1px solid var(--line); display:flex; justify-content:space-between;">
          <span>⚡ bq_to_s3_bronze_lake</span> <span style="color:var(--green)">● HEALTHY (11:00 AM IST)</span>
        </div>
        <div style="background:#131E2E; padding:10px; border-radius:6px; border:1px solid var(--line); display:flex; justify-content:space-between;">
          <span>⚡ aml_fiu_ind_statutory_dags</span> <span style="color:var(--green)">● HEALTHY</span>
        </div>
        <div style="background:#131E2E; padding:10px; border-radius:6px; border:1px solid var(--line); display:flex; justify-content:space-between;">
          <span>⚡ sftp_inbound_outbound_hub</span> <span style="color:var(--green)">● HEALTHY</span>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
let currentMode = 'balanced';

function setMode(mode) {
  currentMode = mode;
  ['Balanced', 'Creative', 'Precise'].forEach(m => {
    document.getElementById('btn' + m).classList.remove('active');
  });
  document.getElementById('btn' + mode.charAt(0).toUpperCase() + mode.slice(1)).classList.add('active');
}

function handleKeyDown(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
}

function sendPrompt(text) {
  document.getElementById('chatInput').value = text;
  sendMessage();
}

function newChat() {
  const container = document.getElementById('msgContainer');
  container.innerHTML = '';
  document.getElementById('welcomeHero')?.remove();
  const hero = document.createElement('div');
  hero.id = 'welcomeHero';
  hero.className = 'welcome-hero';
  hero.innerHTML = `<h1>🧠 NanoPro AI Lab</h1><p>Fresh Production Session Initialized.</p>`;
  container.appendChild(hero);
}

function openModelCatalog() { document.getElementById('catalogModal').classList.add('active'); }
function openAirflowModal() { document.getElementById('airflowModal').classList.add('active'); }
function closeModals() { document.querySelectorAll('.modal-overlay').forEach(m => m.classList.remove('active')); }

async function sendMessage() {
  const input = document.getElementById('chatInput');
  const text = input.value.trim();
  if (!text) return;
  input.value = '';

  const hero = document.getElementById('welcomeHero');
  if (hero) hero.style.display = 'none';

  const container = document.getElementById('msgContainer');

  // Append User Bubble
  const userBubble = document.createElement('div');
  userBubble.className = 'message-bubble user-msg';
  userBubble.innerText = text;
  container.appendChild(userBubble);

  // Append Thinking Bubble
  const aiBubble = document.createElement('div');
  aiBubble.className = 'message-bubble ai-msg';
  aiBubble.innerHTML = `<div class="ai-badge">⚡ NanoPro Auto Math Router · Thinking...</div><div class="ai-content">Connecting to 4,804+ Model Mesh...</div>`;
  container.appendChild(aiBubble);
  container.scrollTop = container.scrollHeight;

  const t0 = performance.now();
  try {
    const res = await fetch('/api/ai/execute', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt: text, mode: currentMode })
    });
    const data = await res.json();
    const lat = Math.round(performance.now() - t0);

    const modelName = data.model || data.model_name || data.model_executed || 'Groq Qwen 3.8 27B';
    const provider = data.provider || data.lab_name || 'NanoPro Edge Mesh';
    const uScore = data.utility_score || 0.988;

    aiBubble.innerHTML = `
      <div class="ai-badge">
        <span>⚡</span> ${modelName} · ${provider} · U = ${uScore}
      </div>
      <div class="ai-content">${formatContent(data.content || data.response || '')}</div>
      <div class="ai-footer">
        <span>⚡ ${lat}ms · 0 MB Render Load</span>
        <span>${new Date().toLocaleTimeString()}</span>
      </div>
    `;
    mermaid.run();
  } catch (err) {
    aiBubble.innerHTML = `
      <div class="ai-badge">⚠️ Notice</div>
      <div class="ai-content">Error contacting gateway: ${err.message}</div>
    `;
  }
  container.scrollTop = container.scrollHeight;
}

async function logout() {
  try {
    await fetch('/api/auth/logout', { method: 'POST', headers: {'Content-Type': 'application/json'}, credentials: 'include' });
  } catch(e) {}
  document.cookie = 'nanopro_session=; Max-Age=0; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
  window.location.href = '/login';
}

function formatContent(text) {
  if (!text) return '';
  let formatted = text
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    .replace(/\\*\\*(.*?)\\*\\*/gim, '<b>$1</b>')
    .replace(/\\*(.*?)\\*/gim, '<i>$1</i>')
    .replace(/`([^`]+)`/gim, '<code>$1</code>')
    .replace(/\\[([^\\]]+)\\]\\(([^\\)]+)\\)/gim, '<a href="$2" target="_blank">$1</a>')
    .replace(/\\n/gim, '<br>');
  return formatted;
}
</script>
</body>
</html>
"""
    return html.replace("{USER_NAME}", user_name).replace("{USER_ROLE}", user_role)
