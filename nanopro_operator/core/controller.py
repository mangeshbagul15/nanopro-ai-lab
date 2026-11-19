# -*- coding: utf-8 -*-
"""
Dual-Engine GUI & Mouse/Keyboard Controller for NanoPro Operator.
Controls Playwright (Browser) and PyAutoGUI (Desktop OS) with human-like Bézier
mouse gliding, realistic typing cadence, and Set-of-Marks grounding.
"""

import os
import io
import math
import random
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from PIL import Image

try:
    import pyautogui
    # Fail-safe corner trigger (top-left) disabled for automation safety
    pyautogui.FAILSAFE = False
    pyautogui.PAUSE = 0.05
except ImportError:
    pyautogui = None

from nanopro_operator.config import VIEWPORT, MOUSE_SETTINGS, SCREENSHOTS_DIR
from nanopro_operator.core.som_visual_marker import som_marker
from nanopro_operator.core.dom_tree_parser import dom_parser, EXTRACT_DOM_JS
from nanopro_operator.core.credential_vault import vault
from nanopro_operator.core.safety_guardrails import safety_guard


class GUIController:
    """
    Unified GUI Controller supporting Playwright Chromium & OS Desktop PyAutoGUI.
    """

    def __init__(self, mode: str = "playwright"):
        self.mode = mode  # "playwright" or "os"
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.cursor_pos = (VIEWPORT["width"] // 2, VIEWPORT["height"] // 2)
        self.last_screenshot_bytes: Optional[bytes] = None
        self.last_elements: List[Dict[str, Any]] = []
        self.console_logs: List[str] = []

    async def initialize(self, headed: bool = False) -> None:
        """Initializes Playwright Chromium browser."""
        from playwright.async_api import async_playwright
        self.playwright = await async_playwright().start()

        args = [
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--disable-blink-features=AutomationControlled",
            "--window-size=1280,800"
        ]

        self.browser = await self.playwright.chromium.launch(
            headless=not headed,
            args=args
        )

        self.context = await self.browser.new_context(
            viewport=VIEWPORT,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            accept_downloads=True
        )

        self.page = await self.context.new_page()

        # Capture console errors for self-healing
        self.page.on("console", lambda msg: self.console_logs.append(f"[{msg.type}] {msg.text}"))
        self.page.on("pageerror", lambda err: self.console_logs.append(f"[ERROR] {err}"))

    async def navigate(self, url: str) -> None:
        """Navigates to URL and waits for network idle."""
        if not self.page:
            await self.initialize(headed=False)
        await self.page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(0.5)

    async def capture_state(self, annotate_som: bool = True) -> Dict[str, Any]:
        """
        Captures screenshot, DOM interactive elements, and Set-of-Marks visual overlay.
        """
        if not self.page:
            return {"error": "Browser not initialized"}

        # 1. Extract DOM interactive elements
        try:
            dom_data = await self.page.evaluate(EXTRACT_DOM_JS)
        except Exception:
            dom_data = {"elements": [], "title": "", "url": self.page.url, "innerTextSummary": ""}

        elements = dom_data.get("elements", [])
        self.last_elements = elements

        # 2. Capture raw screenshot
        raw_screenshot = await self.page.screenshot(type="jpeg", quality=85)
        self.last_screenshot_bytes = raw_screenshot

        # 3. Apply Set-of-Marks visual badges
        if annotate_som and elements:
            annotated_bytes, _ = som_marker.annotate(
                raw_screenshot,
                elements,
                draw_laser_cursor=self.cursor_pos
            )
            final_screenshot = annotated_bytes
        else:
            final_screenshot = raw_screenshot

        # Save latest screenshot to disk
        screenshot_path = SCREENSHOTS_DIR / "current_screen.jpg"
        with open(screenshot_path, "wb") as f:
            f.write(final_screenshot)

        return {
            "title": dom_data.get("title", ""),
            "url": dom_data.get("url", self.page.url),
            "elements": elements,
            "elements_text": dom_parser.format_elements_for_llm(elements),
            "summary_text": dom_data.get("innerTextSummary", ""),
            "screenshot_bytes": final_screenshot,
            "screenshot_path": str(screenshot_path),
            "console_logs": self.console_logs[-10:]
        }

    async def glide_mouse(self, target_x: int, target_y: int, steps: int = 15) -> None:
        """
        Simulates human-like Bézier curve mouse motion to target coordinates.
        """
        start_x, start_y = self.cursor_pos
        duration = random.uniform(
            MOUSE_SETTINGS["glide_duration_min"],
            MOUSE_SETTINGS["glide_duration_max"]
        )

        # Generate control points for natural curved motion
        ctrl_x = (start_x + target_x) / 2 + random.randint(-40, 40)
        ctrl_y = (start_y + target_y) / 2 + random.randint(-40, 40)

        step_delay = duration / steps
        for step in range(1, steps + 1):
            t = step / steps
            # Quadratic Bézier calculation
            cur_x = int((1 - t)**2 * start_x + 2 * (1 - t) * t * ctrl_x + t**2 * target_x)
            cur_y = int((1 - t)**2 * start_y + 2 * (1 - t) * t * ctrl_y + t**2 * target_y)

            if self.page:
                await self.page.mouse.move(cur_x, cur_y)
            if self.mode == "os" and pyautogui:
                pyautogui.moveTo(cur_x, cur_y)

            await asyncio.sleep(step_delay)

        self.cursor_pos = (target_x, target_y)

    async def human_type(self, text: str) -> None:
        """Types text with natural human micro-delays between keystrokes."""
        resolved = vault.resolve_tokens(text)
        for char in resolved:
            if self.page:
                await self.page.keyboard.type(char)
            elif self.mode == "os" and pyautogui:
                pyautogui.write(char)

            delay = random.uniform(
                MOUSE_SETTINGS["typing_cadence_min"],
                MOUSE_SETTINGS["typing_cadence_max"]
            )
            await asyncio.sleep(delay)

    async def execute_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a planned GUI action with safety validation and coordinates resolution.
        """
        act_type = action.get("action", "").lower()
        elem_id = action.get("element_id")
        target_x = action.get("x")
        target_y = action.get("y")
        text = action.get("text", "")
        key = action.get("key", "")

        # Safety Check
        is_high_risk, category, reason = safety_guard.assess_risk(action, self.page.url if self.page else "")
        if is_high_risk:
            confirmation = safety_guard.create_confirmation_request(action, reason, category)
            return {
                "status": "requires_human_confirmation",
                "confirmation": confirmation,
                "message": reason
            }

        # Resolve element_id to coordinates
        if elem_id is not None and self.last_elements:
            matched = next((el for el in self.last_elements if el.get("i") == elem_id), None)
            if matched:
                box = matched.get("box", {})
                target_x = box.get("cx", target_x)
                target_y = box.get("cy", target_y)

        # 1. Click
        if act_type in ["click", "press_click"]:
            if target_x is not None and target_y is not None:
                await self.glide_mouse(target_x, target_y)
                if self.page:
                    await self.page.mouse.click(target_x, target_y)
                elif self.mode == "os" and pyautogui:
                    pyautogui.click(target_x, target_y)
                await asyncio.sleep(MOUSE_SETTINGS["click_settle_delay"])
                return {"status": "success", "message": f"Clicked at ({target_x}, {target_y})"}
            elif action.get("selector") and self.page:
                await self.page.click(action["selector"])
                return {"status": "success", "message": f"Clicked selector '{action['selector']}'"}
            return {"status": "error", "message": "Click target coordinates or selector missing"}

        # 2. Type
        elif act_type == "type":
            if target_x is not None and target_y is not None:
                await self.glide_mouse(target_x, target_y)
                if self.page:
                    await self.page.mouse.click(target_x, target_y)
            await self.human_type(text)
            return {"status": "success", "message": f"Typed '{text}'"}

        # 3. Press Key
        elif act_type in ["press", "key"]:
            k = key or text or "Enter"
            if self.page:
                await self.page.keyboard.press(k)
            elif self.mode == "os" and pyautogui:
                pyautogui.press(k.lower())
            return {"status": "success", "message": f"Pressed key '{k}'"}

        # 4. Scroll
        elif act_type == "scroll":
            delta_y = action.get("delta_y", 400)
            if self.page:
                await self.page.mouse.wheel(0, delta_y)
            elif self.mode == "os" and pyautogui:
                pyautogui.scroll(-int(delta_y / 2))
            await asyncio.sleep(0.3)
            return {"status": "success", "message": f"Scrolled by {delta_y}px"}

        # 5. Wait
        elif act_type == "wait":
            duration = min(action.get("duration", 2.0), 10.0)
            await asyncio.sleep(duration)
            return {"status": "success", "message": f"Waited {duration}s"}

        # 6. File Upload
        elif act_type == "upload":
            file_path = action.get("file_path", "")
            selector = action.get("selector", "input[type='file']")
            if self.page and os.path.exists(file_path):
                await self.page.set_input_files(selector, file_path)
                return {"status": "success", "message": f"Uploaded file '{file_path}' to '{selector}'"}
            return {"status": "error", "message": f"Upload failed, file not found: {file_path}"}

        return {"status": "error", "message": f"Unsupported action type: {act_type}"}

    async def close(self) -> None:
        """Closes browser and cleans up."""
        if self.page:
            try:
                await self.page.close()
            except Exception:
                pass
        if self.browser:
            try:
                await self.browser.close()
            except Exception:
                pass
        if self.playwright:
            try:
                await self.playwright.stop()
            except Exception:
                pass
