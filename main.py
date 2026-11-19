import os
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any

from app.config import SYSTEM_IDENTITY, TOTAL_MODELS_COUNT
from app.router import ai_router
from app.reports_service import get_report_bytes
from app.alerts_service import dispatch_telegram, dispatch_email, dispatch_whatsapp
from app.ui import get_ai_lab_html

app = FastAPI(
    title="NanoPro AI Lab Production",
    version=SYSTEM_IDENTITY["version"],
    description="Dedicated 4,804+ Models Frontier Mesh with Sub-Second Groq LPU & Zero-Egress Architecture"
)

class AIExecuteRequest(BaseModel):
    prompt: str
    model: Optional[str] = "auto"
    mode: Optional[str] = "balanced"

class AlertRequest(BaseModel):
    channel: str # 'telegram', 'email', 'whatsapp'
    message: Optional[str] = "⚡ NanoPro Global AI Lab Operational Status Alert"
    subject: Optional[str] = "NanoPro Production Alert"
    recipient: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
async def serve_home():
    return HTMLResponse(content=get_ai_lab_html(), status_code=200)

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
