/**
 * NanoPro Production Global AI Lab - Dedicated Cloudflare Worker Edge Gateway
 * 
 * ENVIRONMENT: PRODUCTION (PROD)
 * Dedicated Origin: https://nanopro-ai-lab.onrender.com
 * (Completely isolated from legacy UAT at mangesh-nanopro.mangeshbagul15.workers.dev)
 */

const PROD_RENDER_ORIGIN = "https://nanopro-ai-lab.onrender.com";

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, HEAD",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With, Cookie, Set-Cookie",
  "Access-Control-Allow-Credentials": "true",
  "Access-Control-Max-Age": "86400"
};

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const origin = env?.PROD_BACKEND_URL || PROD_RENDER_ORIGIN;

    // 1. Handle CORS Preflight
    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: CORS_HEADERS
      });
    }

    // 2. Health check route directly at edge
    if (url.pathname === "/api/edge/health") {
      return new Response(JSON.stringify({
        status: "healthy",
        tier: "PROD",
        gateway: "Cloudflare Edge Sovereign Mesh",
        target_origin: origin,
        timestamp: new Date().toISOString()
      }), {
        status: 200,
        headers: {
          "Content-Type": "application/json",
          ...CORS_HEADERS
        }
      });
    }

    // 3. Construct Upstream Request
    const upstreamUrl = new URL(url.pathname + url.search, origin);
    const newHeaders = new Headers(request.headers);
    newHeaders.set("Host", new URL(origin).host);
    newHeaders.set("X-Forwarded-Host", url.host);
    newHeaders.set("X-Forwarded-Proto", url.protocol.replace(":", ""));
    newHeaders.set("X-NanoPro-Gateway", "Cloudflare-Prod-Edge");

    try {
      const upstreamResp = await fetch(upstreamUrl.toString(), {
        method: request.method,
        headers: newHeaders,
        body: ["GET", "HEAD"].includes(request.method) ? undefined : request.body,
        redirect: "manual"
      });

      // Clone response headers and attach CORS
      const respHeaders = new Headers(upstreamResp.headers);
      for (const [k, v] of Object.entries(CORS_HEADERS)) {
        if (!respHeaders.has(k)) {
          respHeaders.set(k, v);
        }
      }

      // Intercept Render free tier cold-start (HTTP 502, 503, 504 during wake-up)
      if (upstreamResp.status >= 502 && upstreamResp.status <= 504) {
        await new Promise(r => setTimeout(r, 2000));
        try {
          const retryResp = await fetch(upstreamUrl.toString(), {
            method: request.method,
            headers: newHeaders,
            body: ["GET", "HEAD"].includes(request.method) ? undefined : request.body,
            redirect: "manual"
          });
          if (retryResp.status < 500) {
            const retryHeaders = new Headers(retryResp.headers);
            for (const [k, v] of Object.entries(CORS_HEADERS)) {
              if (!retryHeaders.has(k)) retryHeaders.set(k, v);
            }
            return new Response(retryResp.body, {
              status: retryResp.status,
              statusText: retryResp.statusText,
              headers: retryHeaders
            });
          }
        } catch (_) {}

        const accept = request.headers.get("accept") || "";
        const isHtml = url.pathname === "/" || url.pathname === "/login" || accept.includes("text/html");
        if (isHtml) {
          return new Response(getColdStartHtml(url.toString()), {
            status: 200,
            headers: {
              "Content-Type": "text/html; charset=utf-8",
              ...CORS_HEADERS
            }
          });
        }

        return new Response(JSON.stringify({
          status: "waking_up",
          message: "NanoPro PROD backend is spinning up from sleep. Auto-recovering in seconds...",
          retry_after: 3
        }), {
          status: 503,
          headers: {
            "Content-Type": "application/json",
            "Retry-After": "3",
            ...CORS_HEADERS
          }
        });
      }

      return new Response(upstreamResp.body, {
        status: upstreamResp.status,
        statusText: upstreamResp.statusText,
        headers: respHeaders
      });

    } catch (err) {
      // In case Render free tier instance is spinning up (cold start ~30s)
      if (url.pathname === "/" || url.pathname === "/login") {
        return new Response(getColdStartHtml(url.toString()), {
          status: 200,
          headers: {
            "Content-Type": "text/html; charset=utf-8",
            ...CORS_HEADERS
          }
        });
      }

      return new Response(JSON.stringify({
        status: "gateway_timeout",
        message: "NanoPro PROD backend is waking up. Please retry in a few seconds.",
        error: err.message
      }), {
        status: 504,
        headers: {
          "Content-Type": "application/json",
          ...CORS_HEADERS
        }
      });
    }
  }
};

function getColdStartHtml(retryUrl) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NanoPro PROD — Initializing Sovereign Edge</title>
<style>
  body { background: #0B1119; color: #E6EDF7; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
  .card { background: #0F1724; border: 1.5px solid #1E2B3E; border-radius: 12px; padding: 32px; text-align: center; max-width: 440px; box-shadow: 0 10px 40px rgba(0,0,0,0.8); }
  .spinner { width: 42px; height: 42px; border: 3px solid #1E2B3E; border-top-color: #8B5CF6; border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 20px auto; }
  h2 { margin: 0 0 8px 0; font-size: 20px; color: #fff; }
  p { color: #94A3B8; font-size: 13px; line-height: 1.6; margin-bottom: 20px; }
  .badge { display: inline-block; background: rgba(139, 92, 246, 0.15); border: 1px solid rgba(139, 92, 246, 0.4); color: #C084FC; font-size: 11px; padding: 4px 10px; border-radius: 20px; font-weight: 600; }
  @keyframes spin { to { transform: rotate(360deg); } }
</style>
</head>
<body>
<div class="card">
  <div class="spinner"></div>
  <div class="badge">NanoPro PROD Gateway</div>
  <h2 style="margin-top: 14px;">Waking Up Sovereign Engine</h2>
  <p>Dedicated Production Environment is spinning up. Connecting to 4,804+ models unified mesh...</p>
</div>
<script>
  setTimeout(() => { window.location.reload(); }, 4000);
</script>
</body>
</html>`;
}
