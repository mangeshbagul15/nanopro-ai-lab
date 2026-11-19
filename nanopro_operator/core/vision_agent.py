# -*- coding: utf-8 -*-
"""
Multi-Modal Vision Agent for NanoPro Operator.
Coordinates multi-modal reasoning across OpenRouter, Claude, Gemini, and Local Ollama (GPU).
Generates structured GUI actions (Thought -> Action -> Self-Reflection).
"""

import json
import base64
import aiohttp
from typing import Dict, Any, List, Optional
from nanopro_operator.config import (
    OPENROUTER_API_KEY,
    GEMINI_API_KEY,
    ANTHROPIC_API_KEY,
    OLLAMA_BASE_URL,
    DEFAULT_OLLAMA_VISION_MODEL,
    DEFAULT_MODEL,
    VISION_MODELS_CATALOG
)

SYSTEM_PROMPT = """You are NanoPro Operator, an autonomous Computer-Use AI Agent and Senior Software Engineer.
You control a real browser and desktop environment to accomplish user goals.

You are given:
1. An annotated screenshot with Set-of-Marks numbered badges [0], [1], [2], ... on interactive elements.
2. A list of interactive DOM elements with their tags, labels, and center coordinates.
3. The previous execution history, observations, and any console errors.

### RULES FOR ACTION GENERATION:
1. Reason carefully in the `thought` field before acting.
2. Whenever possible, reference elements by their `element_id` (e.g., element_id: 4) instead of guessing coordinates.
3. Available Actions:
   - {"action": "click", "element_id": <int>}
   - {"action": "click", "x": <int>, "y": <int>}
   - {"action": "type", "element_id": <int>, "text": "<string>"}
   - {"action": "press", "key": "Enter|Tab|Escape|ArrowDown|BackSpace"}
   - {"action": "scroll", "delta_y": 400}
   - {"action": "wait", "duration": 2.0}
   - {"action": "upload", "selector": "input[type='file']", "file_path": "<string>"}
4. If an unexpected modal or cookie banner blocks your target, prioritize dismissing it first.
5. If the goal is completed, set `is_complete: true` and write the summary in `final_result`.

ALWAYS output valid JSON matching this schema:
{
  "thought": "Step-by-step reasoning about the current screen and goal",
  "action": "click|type|press|scroll|wait|upload",
  "element_id": 0,
  "x": 640,
  "y": 400,
  "text": "",
  "key": "",
  "self_reflection": "What to watch out for or verify on the next screen",
  "is_complete": false,
  "final_result": ""
}
"""


class VisionAgent:
    """
    Multimodal Vision Agent supporting OpenRouter, Claude, Gemini, and Local Ollama GPU.
    """

    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model

    async def plan_next_action(
        self,
        task: str,
        screenshot_bytes: bytes,
        elements_text: str,
        history: List[Dict[str, Any]],
        current_url: str = "",
        console_logs: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Sends multi-modal payload (annotated screenshot + DOM text + history)
        to the Vision LLM and returns the structured action.
        """
        img_b64 = base64.b64encode(screenshot_bytes).decode("utf-8")

        prompt_text = f"""### USER GOAL:
{task}

### CURRENT BROWSER URL:
{current_url}

### INTERACTIVE ELEMENTS ON SCREEN (Set-of-Marks):
{elements_text}

### PREVIOUS ACTIONS TAKEN:
{json.dumps(history[-6:], indent=2) if history else '(Starting initial step)'}

### RECENT BROWSER CONSOLE LOGS:
{chr(10).join(console_logs) if console_logs else '(No errors)'}

Analyze the screen state and provide your next action in JSON.
"""

        # 1. Local Ollama GPU Provider
        if self.model.startswith("ollama") or "local" in self.model:
            return await self._call_ollama(prompt_text, img_b64)

        # 2. Anthropic Direct API
        if ANTHROPIC_API_KEY and self.model.startswith("anthropic/"):
            return await self._call_anthropic(prompt_text, img_b64)

        # 3. Google Gemini Direct API
        if GEMINI_API_KEY and self.model.startswith("google/"):
            return await self._call_gemini(prompt_text, img_b64)

        # 4. OpenRouter Multi-Model Mesh (Default)
        return await self._call_openrouter(prompt_text, img_b64)

    async def _call_openrouter(self, prompt: str, img_b64: str) -> Dict[str, Any]:
        """Calls OpenRouter Multi-Model Vision endpoint."""
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://nanopro-ai-lab.onrender.com",
            "X-Title": "NanoPro Operator CUA"
        }

        payload = {
            "model": self.model if "/" in self.model else f"google/{self.model}",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}
                        }
                    ]
                }
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.1,
            "max_tokens": 1200
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, headers=headers, json=payload, timeout=30) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        content = data["choices"][0]["message"]["content"]
                        return json.loads(content)
                    else:
                        err_text = await resp.text()
                        return self._fallback_action(f"OpenRouter HTTP {resp.status}: {err_text}")
            except Exception as e:
                return self._fallback_action(f"OpenRouter connection error: {str(e)}")

    async def _call_ollama(self, prompt: str, img_b64: str) -> Dict[str, Any]:
        """Calls Local Ollama GPU Vision model (Qwen2.5-VL / LLaVA)."""
        url = f"{OLLAMA_BASE_URL}/api/generate"
        payload = {
            "model": DEFAULT_OLLAMA_VISION_MODEL,
            "prompt": f"{SYSTEM_PROMPT}\n\n{prompt}",
            "images": [img_b64],
            "format": "json",
            "stream": False,
            "options": {"temperature": 0.1}
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload, timeout=45) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return json.loads(data.get("response", "{}"))
                    else:
                        return self._fallback_action(f"Ollama HTTP {resp.status}")
            except Exception as e:
                return self._fallback_action(f"Local Ollama connection failed ({e}). Ensure Ollama is running.")

    async def _call_gemini(self, prompt: str, img_b64: str) -> Dict[str, Any]:
        """Calls Google Gemini API directly."""
        clean_model = self.model.replace("google/", "")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{clean_model}:generateContent?key={GEMINI_API_KEY}"

        payload = {
            "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": img_b64
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "response_mime_type": "application/json",
                "temperature": 0.1
            }
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload, timeout=30) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        raw = data["candidates"][0]["content"]["parts"][0]["text"]
                        return json.loads(raw)
                    return self._fallback_action(f"Gemini HTTP {resp.status}")
            except Exception as e:
                return self._fallback_action(f"Gemini error: {e}")

    async def _call_anthropic(self, prompt: str, img_b64: str) -> Dict[str, Any]:
        """Calls Anthropic Claude Computer-Use API."""
        clean_model = self.model.replace("anthropic/", "")
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        payload = {
            "model": clean_model,
            "max_tokens": 1200,
            "system": SYSTEM_PROMPT,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": img_b64
                            }
                        },
                        {"type": "text", "text": prompt}
                    ]
                }
            ]
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, headers=headers, json=payload, timeout=35) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        text = data["content"][0]["text"]
                        return json.loads(text)
                    return self._fallback_action(f"Claude HTTP {resp.status}")
            except Exception as e:
                return self._fallback_action(f"Claude error: {e}")

    def _fallback_action(self, reason: str) -> Dict[str, Any]:
        """Heuristic fallback action to prevent crash."""
        return {
            "thought": f"Encountered upstream error: {reason}. Waiting 2s before self-healing retry.",
            "action": "wait",
            "duration": 2.0,
            "self_reflection": "Check network connectivity and retry action.",
            "is_complete": False
        }
