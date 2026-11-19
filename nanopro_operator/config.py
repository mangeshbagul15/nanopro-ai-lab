# -*- coding: utf-8 -*-
"""
Configuration module for NanoPro Operator & Autonomous CUA Engine.
"""

import os
from pathlib import Path
from typing import Dict, Any, List

BASE_DIR = Path(__file__).resolve().parent
WORKSPACES_DIR = BASE_DIR / "workspaces"
VAULT_FILE = BASE_DIR / ".vault_secrets.enc"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"

WORKSPACES_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------
# LLM & Vision Providers Configuration
# -------------------------------------------------------------
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "") or os.environ.get("DEFAPI_API_KEY", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

# Local Ollama with GPU acceleration (CUDA)
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_OLLAMA_VISION_MODEL = "qwen2.5vl:latest"

# Default Model Selection
DEFAULT_MODEL = os.environ.get("OPERATOR_DEFAULT_MODEL", "google/gemini-2.5-flash")

# Model Catalog for Vision & GUI Control
VISION_MODELS_CATALOG: Dict[str, Dict[str, Any]] = {
    "google/gemini-2.5-flash": {
        "provider": "openrouter",
        "name": "Gemini 2.5 Flash (Ultra-Fast <300ms SLA, 2M Vision)",
        "context_window": 2000000,
        "vision": True,
        "speed": "ultra_fast"
    },
    "anthropic/claude-3.7-sonnet": {
        "provider": "openrouter",
        "name": "Claude 3.7 Sonnet (Hybrid Thinking & Computer-Use SOTA)",
        "context_window": 200000,
        "vision": True,
        "speed": "deep_reasoning"
    },
    "anthropic/claude-3.5-sonnet": {
        "provider": "openrouter",
        "name": "Claude 3.5 Sonnet (Native Computer-Use API)",
        "context_window": 200000,
        "vision": True,
        "speed": "fast"
    },
    "google/gemini-2.5-pro": {
        "provider": "openrouter",
        "name": "Gemini 2.5 Pro (Frontier Multimodal SOTA)",
        "context_window": 2000000,
        "vision": True,
        "speed": "high_accuracy"
    },
    "openai/gpt-4o": {
        "provider": "openrouter",
        "name": "OpenAI GPT-4o Omni Vision",
        "context_window": 128000,
        "vision": True,
        "speed": "fast"
    },
    "qwen/qwen-2.5-vl-72b-instruct": {
        "provider": "openrouter",
        "name": "Qwen 2.5 VL 72B Instruct (Open-Weight Vision Flagship)",
        "context_window": 128000,
        "vision": True,
        "speed": "balanced"
    },
    "ollama/local-gpu": {
        "provider": "ollama",
        "name": "Local Ollama GPU (Qwen2.5-VL / LLaVA / Llama 3.2-Vision)",
        "context_window": 32768,
        "vision": True,
        "speed": "local_gpu"
    }
}

# -------------------------------------------------------------
# Browser & OS Automation Settings
# -------------------------------------------------------------
VIEWPORT = {
    "width": 1280,
    "height": 800
}

# Mouse cursor glide animation settings (Human-like Bézier curve movement)
MOUSE_SETTINGS = {
    "glide_duration_min": 0.25,
    "glide_duration_max": 0.65,
    "typing_cadence_min": 0.03,
    "typing_cadence_max": 0.09,
    "click_settle_delay": 0.20
}

# Max steps per autonomous loop before triggering human checkpoint
MAX_AUTONOMOUS_STEPS = 30

# Ephemeral ports range for Devin autonomous full-stack preview
DEV_SERVER_PORT_RANGE = (8081, 8099)

# -------------------------------------------------------------
# Safety & Human-in-the-Loop Guardrails
# -------------------------------------------------------------
HIGH_RISK_KEYWORDS: List[str] = [
    "transfer", "pay", "payout", "payment", "fund", "debit", "credit_card", "cvv", "otp",
    "delete", "drop", "truncate", "purge", "destroy", "format", "wipe",
    "password", "secret", "private_key", "auth_token", "api_key"
]

CONFIRMATION_TIMEOUT_SECONDS = 180
