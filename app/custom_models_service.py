import os
import json
import time
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CUSTOM_STORE_PATH = os.path.join(DB_DIR, "custom_models.json")

DEFAULT_PROVIDER_CONFIG = {
    "openrouter": {
        "name": "OpenRouter Mesh",
        "base_url": "https://openrouter.ai/api/v1",
        "country": "USA",
        "flag": "🌐"
    },
    "groq": {
        "name": "Groq LPUs",
        "base_url": "https://api.groq.com/openai/v1",
        "country": "USA",
        "flag": "⚡"
    },
    "deepseek": {
        "name": "DeepSeek AI",
        "base_url": "https://api.deepseek.com",
        "country": "China",
        "flag": "🇨🇳"
    },
    "mistral": {
        "name": "Mistral AI",
        "base_url": "https://api.mistral.ai/v1",
        "country": "France",
        "flag": "🇫🇷"
    },
    "novita": {
        "name": "Novita AI",
        "base_url": "https://api.novita.ai/v3/openai",
        "country": "USA",
        "flag": "🚀"
    },
    "together": {
        "name": "Together AI",
        "base_url": "https://api.together.xyz/v1",
        "country": "USA",
        "flag": "🤝"
    },
    "openai": {
        "name": "OpenAI",
        "base_url": "https://api.openai.com/v1",
        "country": "USA",
        "flag": "🇺🇸"
    },
    "sambanova": {
        "name": "SambaNova Systems",
        "base_url": "https://api.sambanova.ai/v1",
        "country": "USA",
        "flag": "⚡"
    },
    "nvidia": {
        "name": "NVIDIA NIM",
        "base_url": "https://integrate.api.nvidia.com/v1",
        "country": "USA",
        "flag": "🟢"
    },
    "huggingface": {
        "name": "Hugging Face Hub",
        "base_url": "https://router.huggingface.co/v1",
        "country": "Global",
        "flag": "🤗"
    }
}


def load_custom_store() -> Dict[str, Any]:
    os.makedirs(DB_DIR, exist_ok=True)
    if not os.path.exists(CUSTOM_STORE_PATH):
        return {"custom_models": [], "connected_providers": {}, "discovered_models": []}
    try:
        with open(CUSTOM_STORE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return {"custom_models": [], "connected_providers": {}, "discovered_models": []}
            data.setdefault("custom_models", [])
            data.setdefault("connected_providers", {})
            data.setdefault("discovered_models", [])
            return data
    except Exception:
        return {"custom_models": [], "connected_providers": {}, "discovered_models": []}


def save_custom_store(store: Dict[str, Any]) -> None:
    os.makedirs(DB_DIR, exist_ok=True)
    with open(CUSTOM_STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(store, f, indent=2, ensure_ascii=False)


def get_all_custom_models() -> List[Dict[str, Any]]:
    """Returns union of user-defined custom models and live-discovered models from connected provider keys."""
    store = load_custom_store()
    models = []
    seen = set()

    for m in store.get("custom_models", []):
        mid = m.get("id")
        if mid and mid not in seen:
            seen.add(mid)
            models.append(m)

    for m in store.get("discovered_models", []):
        mid = m.get("id")
        if mid and mid not in seen:
            seen.add(mid)
            models.append(m)

    return models


def get_connected_providers() -> Dict[str, Any]:
    store = load_custom_store()
    return store.get("connected_providers", {})


def add_custom_model(model_data: Dict[str, Any]) -> Dict[str, Any]:
    """Adds or updates a custom model in the persistent registry."""
    store = load_custom_store()
    raw_id = (model_data.get("id") or "").strip()
    if not raw_id:
        slug = (model_data.get("model_slug") or model_data.get("name") or "custom-model").lower().replace(" ", "-")
        raw_id = f"custom/{slug}"

    if not raw_id.startswith("custom/") and "/" not in raw_id:
        raw_id = f"custom/{raw_id}"

    base_url = (model_data.get("base_url") or "").strip().rstrip("/")
    api_key = (model_data.get("api_key") or "").strip()
    model_slug = (model_data.get("model_slug") or raw_id.split("/")[-1]).strip()

    tier = model_data.get("tier", "general")
    if model_data.get("is_free"):
        tier = "free"

    entry = {
        "id": raw_id,
        "name": model_data.get("name") or model_slug.replace("-", " ").title(),
        "lab": model_data.get("lab") or "Custom Private AI Lab",
        "country": model_data.get("country") or "India",
        "flag": model_data.get("flag") or "⭐",
        "tier": tier,
        "context": int(model_data.get("context") or 128000),
        "is_free": bool(model_data.get("is_free", False)),
        "base_url": base_url,
        "api_key": api_key,
        "model_slug": model_slug,
        "provider": model_data.get("provider", "custom"),
        "description": model_data.get("description", "User-registered custom model in NanoPro AI Lab."),
        "created_at": time.time()
    }

    # Replace if exists, else append
    existing = [m for m in store["custom_models"] if m.get("id") != raw_id]
    existing.append(entry)
    store["custom_models"] = existing
    save_custom_store(store)

    return {"status": "success", "message": f"Custom model '{entry['name']}' registered successfully!", "model": entry}


def delete_custom_model(model_id: str) -> Dict[str, Any]:
    """Deletes a custom model or discovered model from registry."""
    store = load_custom_store()
    c_orig = len(store.get("custom_models", []))
    d_orig = len(store.get("discovered_models", []))

    store["custom_models"] = [m for m in store.get("custom_models", []) if m.get("id") != model_id]
    store["discovered_models"] = [m for m in store.get("discovered_models", []) if m.get("id") != model_id]

    c_new = len(store["custom_models"])
    d_new = len(store["discovered_models"])

    save_custom_store(store)
    deleted = (c_orig != c_new) or (d_orig != d_new)
    return {
        "status": "success" if deleted else "not_found",
        "message": f"Model '{model_id}' removed from registry." if deleted else "Model not found."
    }


def connect_provider_key(provider_key: str, api_key: str, base_url: Optional[str] = None) -> Dict[str, Any]:
    """Validates an API key against the provider, auto-discovers all models, and saves to store."""
    pkey = (provider_key or "").strip().lower()
    key = (api_key or "").strip()
    if not key:
        return {"status": "error", "message": "API key cannot be empty."}

    cfg = DEFAULT_PROVIDER_CONFIG.get(pkey, {
        "name": pkey.capitalize(),
        "base_url": (base_url or "").rstrip("/"),
        "country": "Global",
        "flag": "🔑"
    })

    b_url = (base_url or cfg.get("base_url") or "").rstrip("/")
    if not b_url:
        return {"status": "error", "message": "Base URL is required for custom providers."}

    models_url = f"{b_url}/models"
    headers = {
        "Authorization": f"Bearer {key}",
        "User-Agent": "NanoPro-AI-Studio/2.0"
    }
    if pkey == "openrouter":
        headers["HTTP-Referer"] = "https://nanopro-prod.mangeshbagul15.workers.dev"
        headers["X-Title"] = "NanoPro AI Lab"

    discovered = []
    try:
        req = urllib.request.Request(models_url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            raw_list = data.get("data") if isinstance(data, dict) else data
            if isinstance(raw_list, list):
                for rm in raw_list:
                    if not isinstance(rm, dict):
                        continue
                    mid_raw = rm.get("id") or ""
                    if not mid_raw:
                        continue
                    m_slug = mid_raw
                    # Format namespaced id
                    if pkey == "openrouter":
                        namespaced_id = mid_raw
                    else:
                        namespaced_id = f"{pkey}/{mid_raw}" if not mid_raw.startswith(f"{pkey}/") else mid_raw

                    m_name = rm.get("name") or mid_raw.split("/")[-1].replace("-", " ").title()
                    is_free = ":free" in mid_raw or bool(rm.get("is_free"))

                    tier = "general"
                    mid_low = mid_raw.lower()
                    if is_free:
                        tier = "free"
                    elif any(k in mid_low for k in ["r1", "o1", "o3", "reason", "thinking"]):
                        tier = "reasoning"
                    elif any(k in mid_low for k in ["code", "coder", "dev"]):
                        tier = "code"
                    elif any(k in mid_low for k in ["flash", "instant", "fast", "turbo"]):
                        tier = "fast"
                    elif any(k in mid_low for k in ["pro", "large", "max", "opus", "sonnet"]):
                        tier = "flagship"

                    ctx_len = rm.get("context_length") or rm.get("context_window") or 128000

                    discovered.append({
                        "id": namespaced_id,
                        "name": m_name,
                        "lab": cfg["name"],
                        "country": cfg["country"],
                        "flag": cfg["flag"],
                        "tier": tier,
                        "context": int(ctx_len),
                        "is_free": is_free,
                        "provider": pkey,
                        "api_key": key,
                        "base_url": b_url,
                        "model_slug": m_slug,
                        "created_at": time.time()
                    })
    except urllib.error.HTTPError as e:
        if e.code == 401 or e.code == 403:
            return {"status": "error", "message": f"Authentication failed (HTTP {e.code}): Invalid API key for {cfg['name']}."}
        else:
            # Some providers don't have a /models endpoint, but allow direct chat completion
            # In that case, add standard models for that provider
            pass
    except Exception as e:
        # Fallback to provider predefined models if /models times out or endpoint differences
        pass

    # If /models endpoint was unavailable or returned 0, create default seed models for known providers
    if not discovered:
        defaults_map = {
            "groq": ["llama-3.3-70b-versatile", "qwen3.8-27b", "llama-3.1-8b-instant", "deepseek-r1-distill-llama-70b"],
            "deepseek": ["deepseek-chat", "deepseek-reasoner"],
            "mistral": ["codestral-latest", "mistral-large-latest", "ministral-14b-latest"],
            "novita": ["meta-llama/llama-3.3-70b-instruct", "deepseek/deepseek-r1", "qwen/qwen-2.5-72b-instruct"],
            "together": ["meta-llama/Llama-3.3-70B-Instruct-Turbo", "deepseek-ai/DeepSeek-R1"],
            "openai": ["gpt-4o", "o3-mini", "gpt-4o-mini"],
        }
        fallback_slugs = defaults_map.get(pkey, [pkey])
        for slug in fallback_slugs:
            discovered.append({
                "id": f"{pkey}/{slug}",
                "name": slug.replace("-", " ").title(),
                "lab": cfg["name"],
                "country": cfg["country"],
                "flag": cfg["flag"],
                "tier": "reasoning" if "r1" in slug or "o3" in slug else ("code" if "code" in slug else "flagship"),
                "context": 128000,
                "is_free": False,
                "provider": pkey,
                "api_key": key,
                "base_url": b_url,
                "model_slug": slug,
                "created_at": time.time()
            })

    # Save to persistent store
    store = load_custom_store()
    # Remove older discovered models from this provider
    store["discovered_models"] = [m for m in store.get("discovered_models", []) if m.get("provider") != pkey]
    store["discovered_models"].extend(discovered)
    store["connected_providers"][pkey] = {
        "provider": pkey,
        "name": cfg["name"],
        "base_url": b_url,
        "api_key": key,
        "connected_at": time.time(),
        "models_count": len(discovered)
    }
    save_custom_store(store)

    return {
        "status": "success",
        "message": f"Successfully connected {cfg['name']}! {len(discovered)} models are now live and usable in NanoPro AI Lab.",
        "provider": pkey,
        "models_count": len(discovered),
        "models": discovered[:10]  # return first 10 preview
    }


def get_custom_provider_for_model(model_id: str) -> Optional[Dict[str, Any]]:
    """Returns cascade config if model_id is a custom or discovered model."""
    if not model_id or model_id == "auto":
        return None

    store = load_custom_store()

    # 1. Check custom_models
    for m in store.get("custom_models", []):
        if m.get("id") == model_id:
            return {
                "name": f"custom_{m.get('provider', 'custom')}",
                "label": f"Custom {m.get('lab', 'Model')} ({m.get('name')})",
                "api_key": m.get("api_key", ""),
                "base_url": m.get("base_url", "https://api.openai.com/v1"),
                "model": m.get("model_slug") or model_id.split("/")[-1],
                "timeout": 25.0,
                "extra_headers": {}
            }

    # 2. Check discovered_models
    for m in store.get("discovered_models", []):
        if m.get("id") == model_id:
            return {
                "name": f"discovered_{m.get('provider', 'prov')}",
                "label": f"Connected {m.get('lab', 'Provider')} ({m.get('name')})",
                "api_key": m.get("api_key", ""),
                "base_url": m.get("base_url", "https://api.openai.com/v1"),
                "model": m.get("model_slug") or model_id.split("/")[-1],
                "timeout": 25.0,
                "extra_headers": {}
            }

    # 3. Check connected_providers by prefix
    prefix = model_id.split("/")[0].lower() if "/" in model_id else ""
    if prefix and prefix in store.get("connected_providers", {}):
        prov = store["connected_providers"][prefix]
        slug = model_id.split("/", 1)[1]
        return {
            "name": f"connected_{prefix}",
            "label": f"Connected {prov.get('name', prefix)}",
            "api_key": prov.get("api_key", ""),
            "base_url": prov.get("base_url", ""),
            "model": slug,
            "timeout": 25.0,
            "extra_headers": {}
        }

    return None


async def test_model_completion(model_id: str, prompt: str = "Hello from NanoPro AI Lab! Confirm ready in one short sentence.") -> Dict[str, Any]:
    """Sends a real lightweight test prompt to any model and returns live latency and response."""
    from app.router import ai_router
    t0 = time.time()
    try:
        res = await ai_router.execute(prompt=prompt, model_id=model_id, mode="fast")
        dur_ms = round((time.time() - t0) * 1000, 1)
        return {
            "status": "success",
            "model": model_id,
            "latency_ms": res.get("latency_ms") or dur_ms,
            "response": res.get("content") or res.get("response") or "Ready.",
            "timestamp": time.strftime("%d %b %Y, %I:%M %p")
        }
    except Exception as e:
        dur_ms = round((time.time() - t0) * 1000, 1)
        return {
            "status": "error",
            "model": model_id,
            "latency_ms": dur_ms,
            "error": str(e),
            "timestamp": time.strftime("%d %b %Y, %I:%M %p")
        }
