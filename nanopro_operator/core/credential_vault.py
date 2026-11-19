# -*- coding: utf-8 -*-
"""
AES-256 Encrypted Credential & Secrets Vault for NanoPro Operator.
Safely stores, manages, and resolves automated credentials, tokens, and secrets
without exposing plain-text passwords in agent logs or LLM context.
"""

import os
import json
import base64
import hashlib
from typing import Dict, Any, Optional, List
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from nanopro_operator.config import VAULT_FILE


class CredentialVault:
    """
    Production AES-256-GCM encrypted local vault for automated login & secrets.
    """

    def __init__(self, master_password: Optional[str] = None):
        self.master_password = master_password or os.environ.get("OPERATOR_VAULT_KEY", "NanoProMasterKey2026")
        self._key = self._derive_key(self.master_password)
        self._store: Dict[str, Dict[str, str]] = {}
        self.load()

    def _derive_key(self, passphrase: str) -> bytes:
        """Derives 256-bit key using PBKDF2 HMAC SHA-256."""
        salt = b"nanopro_operator_salt_v2"
        return hashlib.pbkdf2_hmac("sha256", passphrase.encode("utf-8"), salt, 100000, dklen=32)

    def load(self) -> None:
        """Decrypts and loads the vault from disk."""
        if not VAULT_FILE.exists():
            self._store = {}
            return

        try:
            with open(VAULT_FILE, "rb") as f:
                data = f.read()

            if len(data) < 28:
                self._store = {}
                return

            nonce = data[:12]
            ciphertext = data[12:]
            aesgcm = AESGCM(self._key)
            decrypted = aesgcm.decrypt(nonce, ciphertext, None)
            self._store = json.loads(decrypted.decode("utf-8"))
        except Exception as e:
            print(f"[CredentialVault] Warning: could not decrypt vault: {e}")
            self._store = {}

    def save(self) -> None:
        """Encrypts and persists the vault to disk."""
        try:
            raw = json.dumps(self._store).encode("utf-8")
            nonce = os.urandom(12)
            aesgcm = AESGCM(self._key)
            ciphertext = aesgcm.encrypt(nonce, raw, None)

            with open(VAULT_FILE, "wb") as f:
                f.write(nonce + ciphertext)
        except Exception as e:
            print(f"[CredentialVault] Save error: {e}")

    def set_secret(self, service: str, username: str, password: str, notes: str = "") -> None:
        """Stores a credential set under a service key."""
        self._store[service] = {
            "username": username,
            "password": password,
            "notes": notes
        }
        self.save()

    def get_secret(self, service: str) -> Optional[Dict[str, str]]:
        """Retrieves a credential set."""
        return self._store.get(service)

    def list_services(self) -> List[str]:
        """Lists stored services without revealing secrets."""
        return list(self._store.keys())

    def resolve_tokens(self, text: str) -> str:
        """
        Replaces vault macro tokens like $VAULT[github:password] with decrypted values
        just-in-time before typing into native browser fields.
        """
        import re
        pattern = r"\$VAULT\[([^:]+):([^\]]+)\]"

        def _repl(match):
            service, field = match.group(1), match.group(2)
            sec = self.get_secret(service)
            if sec and field in sec:
                return sec[field]
            return match.group(0)

        return re.sub(pattern, _repl, text)


vault = CredentialVault()
