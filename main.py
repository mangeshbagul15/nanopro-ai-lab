import os
import time
import json
from fastapi import FastAPI, Request, Response, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any

from app.config import SYSTEM_IDENTITY, TOTAL_MODELS_COUNT
from app.router import ai_router
from app.reports_service import get_report_bytes
from app.alerts_service import dispatch_telegram, dispatch_email, dispatch_whatsapp
from app.auth_manager import auth_manager, GOOGLE_CLIENT_ID
from app.ui import get_ai_lab_html, get_login_page_html

app = FastAPI(
    title="NanoPro AI Lab Production",
    version=SYSTEM_IDENTITY["version"],
    description="Dedicated 4,804+ Models Frontier Mesh with Sub-Second Groq LPU, Zero-Trust Gateway & Multi-Channel Alerts"
)

# -------------------------------------------------------------
# Pydantic Request Models
# -------------------------------------------------------------
class AIExecuteRequest(BaseModel):
    prompt: str
    model: Optional[str] = "auto"
    mode: Optional[str] = "balanced"

class AlertRequest(BaseModel):
    channel: str
    message: Optional[str] = "⚡ NanoPro Global AI Lab Operational Status Alert"
    subject: Optional[str] = "NanoPro Production Alert"
    recipient: Optional[str] = None

class AuthLoginRequest(BaseModel):
    username: str
    password: str

class GoogleLoginRequest(BaseModel):
    credential: str
    full_name: Optional[str] = None

class AuthOtpSendRequest(BaseModel):
    identifier: str
    channel: Optional[str] = "whatsapp"

class AuthOtpVerifyRequest(BaseModel):
    identifier: str
    otp_code: str
    channel: Optional[str] = "whatsapp"

class AuthRegisterRequest(BaseModel):
    username: str
    password: str
    full_name: str
    email: str
    phone: Optional[str] = ""

class AuthValidateRequest(BaseModel):
    session_token: Optional[str] = None

class AuthLogoutRequest(BaseModel):
    session_token: Optional[str] = None

# -------------------------------------------------------------
# Root & Login Pages (Direct into Global AI Lab once authenticated)
# -------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request, token: Optional[str] = None):
    # 1. Check session token from query, cookie, or header
    sess_token = token or request.cookies.get("nanopro_session") or ""
    if not sess_token:
        auth_hdr = request.headers.get("Authorization", "")
        if auth_hdr.startswith("Bearer "):
            sess_token = auth_hdr.replace("Bearer ", "").strip()

    valid_session = auth_manager.validate_session(sess_token)
    if valid_session.get("status") == "success" and valid_session.get("valid"):
        user = valid_session.get("user")
        resp = HTMLResponse(content=get_ai_lab_html(user=user), status_code=200)
        # If token was passed via URL parameter, persist in cookie for 30 days
        if token:
            resp.set_cookie(
                key="nanopro_session",
                value=token,
                max_age=2592000,
                httponly=False,
                samesite="lax",
                secure=False,
                path="/"
            )
        return resp

    # 2. If unauthenticated, serve the Cyber-Luxe Zero-Trust Login Gateway
    return HTMLResponse(content=get_login_page_html(), status_code=200)

@app.get("/login", response_class=HTMLResponse)
async def serve_login(request: Request):
    return HTMLResponse(content=get_login_page_html(), status_code=200)

# -------------------------------------------------------------
# Authentication Endpoints
# -------------------------------------------------------------
@app.post("/api/auth/login")
async def api_auth_login(req: AuthLoginRequest, request: Request):
    ip = request.client.host if request.client else "Unknown"
    ua = request.headers.get("user-agent", "Unknown")
    res = auth_manager.authenticate_user(req.username, req.password, ip=ip, ua=ua)
    status_code = 200 if res.get("status") == "success" else 401
    resp = JSONResponse(res, status_code=status_code)
    if res.get("status") == "success" and res.get("session_token"):
        resp.set_cookie(
            key="nanopro_session",
            value=res["session_token"],
            max_age=2592000,
            httponly=False,
            samesite="lax",
            secure=False,
            path="/"
        )
    return resp

@app.get("/api/auth/google-config")
async def api_google_config():
    return JSONResponse({
        "status": "success",
        "client_id": GOOGLE_CLIENT_ID,
        "enabled": bool(GOOGLE_CLIENT_ID)
    })

@app.post("/api/auth/google-login")
async def api_google_login(req: GoogleLoginRequest, request: Request):
    ip = request.client.host if request.client else "Unknown"
    ua = request.headers.get("user-agent", "Unknown")
    res = auth_manager.authenticate_google(req.credential, ip=ip, ua=ua)
    status_code = 200 if res.get("status") == "success" else 401
    resp = JSONResponse(res, status_code=status_code)
    if res.get("status") == "success" and res.get("session_token"):
        resp.set_cookie(
            key="nanopro_session",
            value=res["session_token"],
            max_age=2592000,
            httponly=False,
            samesite="lax",
            secure=False,
            path="/"
        )
    return resp

@app.post("/api/auth/google-callback")
async def api_google_callback(request: Request, credential: Optional[str] = Form(None)):
    ip = request.client.host if request.client else "Unknown"
    ua = request.headers.get("user-agent", "Unknown")
    if not credential:
        return RedirectResponse("/login?error=missing_credential", status_code=303)
    res = auth_manager.authenticate_google(credential, ip=ip, ua=ua)
    if res.get("status") == "success" and res.get("session_token"):
        resp = RedirectResponse(f"/?token={res['session_token']}", status_code=303)
        resp.set_cookie(
            key="nanopro_session",
            value=res["session_token"],
            max_age=2592000,
            httponly=False,
            samesite="lax",
            secure=False,
            path="/"
        )
        return resp
    return RedirectResponse("/login?error=google_failed", status_code=303)

@app.post("/api/auth/otp/send")
async def api_otp_send(req: AuthOtpSendRequest, request: Request):
    ip = request.client.host if request.client else "Unknown"
    res = auth_manager.generate_and_send_otp(req.identifier, channel=req.channel or "whatsapp", ip=ip)
    status_code = 200 if res.get("status") == "success" else 400
    return JSONResponse(res, status_code=status_code)

@app.post("/api/auth/otp/verify")
async def api_otp_verify(req: AuthOtpVerifyRequest, request: Request):
    ip = request.client.host if request.client else "Unknown"
    ua = request.headers.get("user-agent", "Unknown")
    res = auth_manager.verify_otp_and_login(req.identifier, req.otp_code, channel=req.channel or "whatsapp", ip=ip, ua=ua)
    status_code = 200 if res.get("status") == "success" else 401
    resp = JSONResponse(res, status_code=status_code)
    if res.get("status") == "success" and res.get("session_token"):
        resp.set_cookie(
            key="nanopro_session",
            value=res["session_token"],
            max_age=2592000,
            httponly=False,
            samesite="lax",
            secure=False,
            path="/"
        )
    return resp

@app.post("/api/auth/register")
async def api_auth_register(req: AuthRegisterRequest, request: Request):
    ip = request.client.host if request.client else "Unknown"
    ua = request.headers.get("user-agent", "Unknown")
    res = auth_manager.register_user(req.username, req.password, req.full_name, req.email, req.phone or "", ip=ip, ua=ua)
    status_code = 200 if res.get("status") == "success" else 400
    return JSONResponse(res, status_code=status_code)

@app.post("/api/auth/validate")
async def api_auth_validate_post(req: AuthValidateRequest, request: Request):
    token = req.session_token or request.cookies.get("nanopro_session") or ""
    res = auth_manager.validate_session(token)
    return JSONResponse(res)

@app.get("/api/auth/validate")
async def api_auth_validate_get(token: str = "", session_token: str = "", request: Request = None):
    t = (token or session_token or (request.cookies.get("nanopro_session") if request else "") or "").strip()
    res = auth_manager.validate_session(t)
    return JSONResponse(res)

@app.post("/api/auth/logout")
async def api_auth_logout(req: Optional[AuthLogoutRequest] = None, request: Request = None):
    token = (req.session_token if req else None) or (request.cookies.get("nanopro_session") if request else "") or ""
    res = auth_manager.logout_user(token)
    resp = JSONResponse(res)
    resp.delete_cookie(key="nanopro_session", path="/")
    return resp

# -------------------------------------------------------------
# System & AI Execution Endpoints
# -------------------------------------------------------------
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "system": SYSTEM_IDENTITY["name"],
        "version": SYSTEM_IDENTITY["version"],
        "total_models": TOTAL_MODELS_COUNT,
        "sla": SYSTEM_IDENTITY["sla"],
        "memory_overhead": SYSTEM_IDENTITY["memory_overhead"]
    }

@app.post("/api/ai/execute")
async def execute_ai(req: AIExecuteRequest):
    result = await ai_router.execute(prompt=req.prompt, model_id=req.model, mode=req.mode)
    return JSONResponse(result)

@app.post("/api/alerts/dispatch")
async def send_alert(req: AlertRequest):
    ch = req.channel.lower()
    if ch == "telegram":
        res = await dispatch_telegram(req.message or "⚡ NanoPro Production Global AI Lab status check.")
    elif ch == "email":
        res = await dispatch_email(
            subject=req.subject or "NanoPro Alert",
            body=req.message or "NanoPro Production Alert",
            to=req.recipient
        )
    elif ch == "whatsapp":
        res = await dispatch_whatsapp(text=req.message or "⚡ NanoPro WhatsApp broadcast active.")
    else:
        return JSONResponse({"status": "error", "message": f"Unsupported channel: {req.channel}"}, status_code=400)
    return JSONResponse({"status": "success", "channel": ch, "result": res})

@app.get("/api/reports/download/{report_type}")
async def download_report(report_type: str):
    content, media_type, filename = get_report_bytes(report_type)
    return Response(
        content=content,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
