# -*- coding: utf-8 -*-
"""
Autonomous Self-Healing Loop & Reasoning Engine for NanoPro Operator.
Implements the continuous Thought -> Action -> Observation -> Error Reflection cycle.
Recovers gracefully from blockers, popups, form errors, and DOM changes.
"""

import asyncio
from typing import Dict, Any, List, Optional, Callable
from nanopro_operator.config import MAX_AUTONOMOUS_STEPS
from nanopro_operator.core.controller import GUIController
from nanopro_operator.core.vision_agent import VisionAgent
from nanopro_operator.core.safety_guardrails import safety_guard


class SelfHealingLoop:
    """
    Manages autonomous execution loop with multi-agent self-healing and error reflection.
    """

    def __init__(
        self,
        controller: GUIController,
        vision_agent: VisionAgent,
        max_steps: int = MAX_AUTONOMOUS_STEPS,
        event_callback: Optional[Callable[[Dict[str, Any]], None]] = None
    ):
        self.controller = controller
        self.vision_agent = vision_agent
        self.max_steps = max_steps
        self.event_callback = event_callback
        self.history: List[Dict[str, Any]] = []
        self.is_running = False
        self.consecutive_errors = 0

    def emit(self, event_type: str, data: Dict[str, Any]) -> None:
        """Emits event to UI or logging listeners."""
        payload = {"type": event_type, "timestamp": asyncio.get_event_loop().time(), **data}
        if self.event_callback:
            try:
                self.event_callback(payload)
            except Exception:
                pass

    async def run(self, task: str, start_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Executes the autonomous loop until task success or completion.
        """
        self.is_running = True
        self.history = []
        self.consecutive_errors = 0

        self.emit("start", {"task": task, "start_url": start_url})

        # 1. Initial navigation if provided
        if start_url:
            await self.controller.navigate(start_url)
            self.emit("navigate", {"url": start_url})

        step_count = 0
        final_summary = "Task terminated."

        while self.is_running and step_count < self.max_steps:
            step_count += 1
            self.emit("step_start", {"step": step_count})

            # 2. Perception: capture screen state & Set-of-Marks markers
            state = await self.controller.capture_state(annotate_som=True)
            screenshot_bytes = state.get("screenshot_bytes", b"")
            elements_text = state.get("elements_text", "")
            current_url = state.get("url", "")
            console_logs = state.get("console_logs", [])

            self.emit("screen_update", {
                "step": step_count,
                "url": current_url,
                "screenshot_path": state.get("screenshot_path"),
                "element_count": len(state.get("elements", []))
            })

            # 3. Autonomous Reasoning: Plan next action
            decision = await self.vision_agent.plan_next_action(
                task=task,
                screenshot_bytes=screenshot_bytes,
                elements_text=elements_text,
                history=self.history,
                current_url=current_url,
                console_logs=console_logs
            )

            thought = decision.get("thought", "Analyzing screen...")
            action = {
                "action": decision.get("action", "wait"),
                "element_id": decision.get("element_id"),
                "x": decision.get("x"),
                "y": decision.get("y"),
                "text": decision.get("text", ""),
                "key": decision.get("key", "")
            }
            reflection = decision.get("self_reflection", "")
            is_complete = decision.get("is_complete", False)

            self.emit("thought", {
                "step": step_count,
                "thought": thought,
                "action": action,
                "reflection": reflection
            })

            # 4. Check if goal is already accomplished
            if is_complete:
                final_summary = decision.get("final_result", thought)
                self.emit("complete", {"summary": final_summary, "steps": step_count})
                break

            # 5. Execute Action
            exec_result = await self.controller.execute_action(action)

            # Check for Human-in-the-Loop Confirmation
            if exec_result.get("status") == "requires_human_confirmation":
                self.emit("human_confirmation_needed", {
                    "step": step_count,
                    "confirmation": exec_result.get("confirmation"),
                    "message": exec_result.get("message")
                })
                # Pause and poll for approval
                token = exec_result["confirmation"]["token"]
                approved = await self._wait_for_human_approval(token)
                if not approved:
                    self.emit("action_rejected", {"step": step_count, "reason": "User rejected safety checkpoint."})
                    final_summary = "Action rejected by user safety guardrail."
                    break
                # Retry execution once approved
                exec_result = await self.controller.execute_action(action)

            # 6. Self-Healing & Reflection check
            if exec_result.get("status") == "error":
                self.consecutive_errors += 1
                error_msg = exec_result.get("message", "Unknown error")
                self.emit("error_detected", {"step": step_count, "error": error_msg})

                # Critic agent self-healing recovery strategy
                recovery_action = await self._critic_recovery_strategy(error_msg, state)
                self.emit("self_healing_attempt", {"recovery": recovery_action})
                await self.controller.execute_action(recovery_action)
                await asyncio.sleep(1.0)
            else:
                self.consecutive_errors = 0

            # 7. Record History
            self.history.append({
                "step": step_count,
                "thought": thought,
                "action": action,
                "observation": exec_result.get("message", "Executed"),
                "url": current_url,
                "reflection": reflection
            })

            await asyncio.sleep(0.5)

        self.is_running = False
        return {
            "status": "success" if is_complete else "max_steps_reached",
            "steps": step_count,
            "summary": final_summary,
            "history": self.history
        }

    async def _wait_for_human_approval(self, token: str, timeout: int = 120) -> bool:
        """Polls for safety approval from UI or API."""
        start = asyncio.get_event_loop().time()
        while asyncio.get_event_loop().time() - start < timeout:
            if safety_guard.is_approved(token):
                return True
            req = safety_guard.pending_confirmations.get(token)
            if req and req.get("status") == "REJECTED":
                return False
            await asyncio.sleep(1.0)
        return False

    async def _critic_recovery_strategy(self, error: str, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesizes an adaptive recovery action (dismiss popups, scroll, or refocus).
        """
        # If element wasn't clickable, check if an overlay or cookie dialog is active
        elements = state.get("elements", [])
        dismiss_candidates = [
            el for el in elements
            if any(w in (el.get("label", "") + el.get("role", "")).lower() for w in ["close", "dismiss", "accept", "got it", "i agree", "ok"])
        ]
        if dismiss_candidates:
            return {"action": "click", "element_id": dismiss_candidates[0]["i"]}

        # Default recovery: scroll slightly and wait for DOM stabilization
        return {"action": "scroll", "delta_y": 250}
