# -*- coding: utf-8 -*-
"""
Safety & Human-in-the-Loop Guardrails for NanoPro Operator.
Intercepts high-risk actions (transactions, deletions, secrets) and requests human authorization.
"""

import time
import uuid
from typing import Dict, Any, Tuple, Optional
from nanopro_operator.config import HIGH_RISK_KEYWORDS, CONFIRMATION_TIMEOUT_SECONDS


class SafetyGuardrails:
    """
    Evaluates actions against safety policies and manages pending human confirmations.
    """

    def __init__(self):
        self.pending_confirmations: Dict[str, Dict[str, Any]] = {}

    def assess_risk(self, action: Dict[str, Any], url: str = "") -> Tuple[bool, str, str]:
        """
        Assesses if an action poses high risk.
        Returns: (is_high_risk, risk_category, explanation)
        """
        action_type = action.get("action", "").lower()
        target_text = str(action.get("text", "")).lower()
        label = str(action.get("label", "")).lower()
        selector = str(action.get("selector", "")).lower()
        combined = f"{action_type} {target_text} {label} {selector} {url}".lower()

        # 1. Financial & Payment keywords
        financial_terms = ["transfer", "pay", "payment", "payout", "fund", "debit", "cvv", "otp", "checkout"]
        for term in financial_terms:
            if term in combined:
                return (
                    True,
                    "FINANCIAL_TRANSACTION",
                    f"Action involves financial payment/transfer ('{term}'). Human confirmation required."
                )

        # 2. Deletion & Destruction keywords
        destructive_terms = ["delete", "drop table", "truncate", "purge", "destroy", "wipe", "rm -rf"]
        for term in destructive_terms:
            if term in combined:
                return (
                    True,
                    "PERMANENT_DELETION",
                    f"Action involves destructive modification or deletion ('{term}'). Human confirmation required."
                )

        # 3. Credential Submission & Secret Leakage
        auth_terms = ["password", "submit credentials", "sign in with root", "private_key"]
        for term in auth_terms:
            if term in combined and action_type in ["type", "press_enter", "click"]:
                return (
                    True,
                    "SENSITIVE_CREDENTIAL",
                    f"Action involves sensitive password/credential submission ('{term}'). Human confirmation required."
                )

        return (False, "LOW_RISK", "Action passed safety inspection.")

    def create_confirmation_request(self, action: Dict[str, Any], reason: str, category: str) -> Dict[str, Any]:
        """Creates a pending human-in-the-loop checkpoint."""
        token = str(uuid.uuid4())[:8]
        req = {
            "token": token,
            "action": action,
            "category": category,
            "reason": reason,
            "status": "PENDING",
            "created_at": time.time(),
            "expires_at": time.time() + CONFIRMATION_TIMEOUT_SECONDS
        }
        self.pending_confirmations[token] = req
        return req

    def resolve(self, token: str, approved: bool) -> bool:
        """Approves or rejects a pending human confirmation."""
        req = self.pending_confirmations.get(token)
        if not req:
            return False

        if time.time() > req["expires_at"]:
            req["status"] = "EXPIRED"
            return False

        req["status"] = "APPROVED" if approved else "REJECTED"
        return approved

    def is_approved(self, token: str) -> bool:
        req = self.pending_confirmations.get(token)
        return bool(req and req.get("status") == "APPROVED")


safety_guard = SafetyGuardrails()
