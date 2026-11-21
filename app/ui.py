import os
from typing import Dict, Any, Optional
from app.global_ai_lab_view import get_global_ai_lab_html as get_view_html

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
    user_name = (user.get("full_name") or user.get("username") or "Super Admin (Mangesh Bagul)") if user else "Super Admin (Mangesh Bagul)"
    user_role = (user.get("role") or "ADMIN").upper() if user else "ADMIN"

    view_content = get_view_html()

    # Bind active user identity into sidebar dock & avatar
    initials = "".join([part[0] for part in user_name.split()[:2] if part]).upper() or "MB"
    view_content = view_content.replace('>Super Admin (Mangesh Bagul)<', f'>{user_name}<')
    view_content = view_content.replace('>MB<', f'>{initials}<')
    view_content = view_content.replace('>ADMIN<', f'>{user_role}<')

    # Ensure active class is set so view displays flex
    if '<div class="workspace-view" id="view-global_ai_lab">' in view_content:
        view_content = view_content.replace(
            '<div class="workspace-view" id="view-global_ai_lab">',
            '<div class="workspace-view active" id="view-global_ai_lab" style="display:flex !important; flex-direction:column !important; width:100vw !important; height:100vh !important; flex:1 1 0% !important;">'
        )


    logout_script = """
    <script>
    async function logout() {
      try {
        await fetch('/api/auth/logout', { method: 'POST', headers: {'Content-Type': 'application/json'}, credentials: 'include' });
      } catch(e) {}
      document.cookie = 'nanopro_session=; Max-Age=0; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
      window.location.href = '/login';
    }
    // Auto-initialize Explorer, Airflow, and History
    document.addEventListener("DOMContentLoaded", () => {
      try { if (window.ailabLoadExplorer) window.ailabLoadExplorer(); } catch(e){}
      try { if (window.ailabLoadLiveModels) window.ailabLoadLiveModels(); } catch(e){}
    });
    </script>
    """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>NanoPro AI Lab — 4,804+ Models Unified Mesh (PROD)</title>
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Cdefs%3E%3ClinearGradient id='npG' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' stop-color='%2338BDF8'/%3E%3Cstop offset='50%25' stop-color='%236366F1'/%3E%3Cstop offset='100%25' stop-color='%2310B981'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='64' height='64' rx='16' fill='%230B1120'/%3E%3Cpath d='M16 46 L32 16 L48 46 L38 46 L32 30 L26 46 Z' fill='url(%23npG)'/%3E%3Ccircle cx='32' cy='22' r='4' fill='%2338BDF8'/%3E%3Ccircle cx='48' cy='46' r='3.5' fill='%2310B981'/%3E%3Ccircle cx='16' cy='46' r='3.5' fill='%236366F1'/%3E%3C/svg%3E">
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
  <style>
    html, body {{
      margin: 0; padding: 0; width: 100vw; height: 100vh;
      overflow: hidden; background: #0B1119; color: #E6EDF7;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }}
    #main-content-viewport {{
      width: 100vw; height: 100vh; display: flex; flex-direction: column; overflow: hidden;
    }}
  </style>
</head>
<body>
  <div id="main-content-viewport">
    {view_content}
  </div>
  {logout_script}
</body>
</html>"""
