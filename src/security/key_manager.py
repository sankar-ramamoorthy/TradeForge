from __future__ import annotations

import json
import os
from collections.abc import Mapping

from cryptography.fernet import Fernet, InvalidToken


class MasterKeyNotConfiguredError(RuntimeError):
    pass


class InvalidCredentialPayloadError(ValueError):
    pass


class KeyManager:
    """Encrypt and decrypt opaque credential payloads with a Fernet master key."""

    ENV_VAR_NAME = "TRADEFORGE_MASTER_KEY"

    def __init__(self, master_key: bytes) -> None:
        try:
            self._fernet = Fernet(master_key)
        except (TypeError, ValueError) as exc:
            raise ValueError("master key must be a valid Fernet key") from exc

    @classmethod
    def from_environment(cls) -> KeyManager:
        raw_key = os.environ.get(cls.ENV_VAR_NAME)
        if not raw_key:
            raise MasterKeyNotConfiguredError(
                "TRADEFORGE_MASTER_KEY is required in the OS environment"
            )
        return cls(raw_key.encode("ascii"))

    @staticmethod
    def generate_master_key() -> str:
        return Fernet.generate_key().decode("ascii")

    def encrypt_payload(self, payload: Mapping[str, str]) -> bytes:
        normalized = self._normalize_payload(payload)
        encoded = json.dumps(
            normalized,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        return self._fernet.encrypt(encoded)

    def decrypt_payload(self, encrypted_payload: bytes) -> dict[str, str]:
        try:
            decrypted = self._fernet.decrypt(encrypted_payload)
        except InvalidToken as exc:
            raise InvalidCredentialPayloadError(
                "credential payload could not be decrypted"
            ) from exc

        try:
            decoded = json.loads(decrypted.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise InvalidCredentialPayloadError(
                "credential payload is not valid JSON"
            ) from exc

        if not isinstance(decoded, dict):
            raise InvalidCredentialPayloadError(
                "credential payload must be a JSON object"
            )

        normalized: dict[str, str] = {}
        for key, value in decoded.items():
            if not isinstance(key, str) or not isinstance(value, str):
                raise InvalidCredentialPayloadError(
                    "credential payload must contain string fields only"
                )
            normalized[key] = value
        return normalized

    @staticmethod
    def _normalize_payload(payload: Mapping[str, str]) -> dict[str, str]:
        normalized: dict[str, str] = {}
        for key, value in payload.items():
            normalized_key = key.strip()
            if not normalized_key:
                raise ValueError("credential payload keys must not be empty")
            if not isinstance(value, str) or not value:
                raise ValueError("credential payload values must be non-empty strings")
            normalized[normalized_key] = value
        if not normalized:
            raise ValueError("credential payload must not be empty")
        return normalized
