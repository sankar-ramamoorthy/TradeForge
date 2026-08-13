from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any
from urllib.parse import urljoin
from urllib.request import urlopen

from src.domain.advisory.contracts import AdvisoryProviderUnavailableError
from src.security.credential import CredentialStatus
from src.security.credential_store import CredentialStore
from src.security.key_manager import KeyManager
from src.security.llm_provider_secrets import LLM_PROVIDER_SECRET_SCHEMA_BY_ID

OLLAMA_PROVIDER_ID = "ollama"
OLLAMA_REMOTE_PROVIDER_ID = "ollama-remote"
OLLAMA_LOCAL_PROVIDER_ID = "ollama-local"
OLLAMA_AUTO_PROVIDER_ID = "ollama-auto"
OLLAMA_PROVIDER_IDS = frozenset(
    {
        OLLAMA_PROVIDER_ID,
        OLLAMA_REMOTE_PROVIDER_ID,
        OLLAMA_LOCAL_PROVIDER_ID,
        OLLAMA_AUTO_PROVIDER_ID,
    }
)

_DEFAULT_OLLAMA_API_BASE = "http://host.docker.internal:11434"
_DEFAULT_OLLAMA_PROBE_TIMEOUT_SECONDS = 0.75


@dataclass(frozen=True, slots=True)
class ResolvedLLMProviderCredential:
    provider_id: str
    api_key: str | None = None
    api_base: str | None = None
    requires_api_key: bool = True


class LLMProviderCredentialResolver:
    def __init__(
        self,
        credential_store: CredentialStore | None,
        *,
        key_manager: KeyManager | None,
        ollama_api_base: str | None = None,
        ollama_remote_url: str | None = None,
        ollama_local_url: str | None = None,
        ollama_remote_reachable: bool | None = None,
        ollama_probe_timeout_seconds: float = _DEFAULT_OLLAMA_PROBE_TIMEOUT_SECONDS,
    ) -> None:
        self._credential_store = credential_store
        self._key_manager = key_manager
        self._ollama_api_base = _configured_value(
            ollama_api_base,
            os.environ.get("OLLAMA_API_BASE"),
            _DEFAULT_OLLAMA_API_BASE,
        )
        self._ollama_remote_url = _configured_value(
            ollama_remote_url,
            os.environ.get("OLLAMA_REMOTE_URL"),
        )
        self._ollama_local_url = _configured_value(
            ollama_local_url,
            os.environ.get("OLLAMA_LOCAL_URL"),
            self._ollama_api_base,
        )
        self._ollama_remote_reachable = ollama_remote_reachable
        self._ollama_probe_timeout_seconds = ollama_probe_timeout_seconds

    def resolve(self, provider_id: str) -> ResolvedLLMProviderCredential:
        if provider_id == OLLAMA_PROVIDER_ID:
            return ResolvedLLMProviderCredential(
                provider_id=provider_id,
                api_base=self._ollama_api_base,
                requires_api_key=False,
            )

        if provider_id == OLLAMA_REMOTE_PROVIDER_ID:
            if self._ollama_remote_url is None:
                raise AdvisoryProviderUnavailableError(
                    "LLM provider 'ollama-remote' URL is not configured"
                )
            return ResolvedLLMProviderCredential(
                provider_id=provider_id,
                api_base=self._ollama_remote_url,
                requires_api_key=False,
            )

        if provider_id == OLLAMA_LOCAL_PROVIDER_ID:
            return ResolvedLLMProviderCredential(
                provider_id=provider_id,
                api_base=self._ollama_local_url,
                requires_api_key=False,
            )

        if provider_id == OLLAMA_AUTO_PROVIDER_ID:
            if (
                self._ollama_remote_url is not None
                and self._is_ollama_remote_reachable(self._ollama_remote_url)
            ):
                return ResolvedLLMProviderCredential(
                    provider_id=OLLAMA_REMOTE_PROVIDER_ID,
                    api_base=self._ollama_remote_url,
                    requires_api_key=False,
                )
            return ResolvedLLMProviderCredential(
                provider_id=OLLAMA_LOCAL_PROVIDER_ID,
                api_base=self._ollama_local_url,
                requires_api_key=False,
            )

        if provider_id == "legacy":
            return ResolvedLLMProviderCredential(
                provider_id=provider_id,
                requires_api_key=False,
            )

        schema = LLM_PROVIDER_SECRET_SCHEMA_BY_ID.get(provider_id)
        if schema is None:
            raise AdvisoryProviderUnavailableError(
                f"LLM provider '{provider_id}' is not governed"
            )
        if self._credential_store is None or self._key_manager is None:
            raise AdvisoryProviderUnavailableError(
                f"LLM provider '{provider_id}' credential is missing"
            )
        credential = self._credential_store.get(provider_id)
        if credential is None or credential.status is not CredentialStatus.ACTIVE:
            raise AdvisoryProviderUnavailableError(
                f"LLM provider '{provider_id}' credential is unavailable"
            )
        payload = self._key_manager.decrypt_payload(credential.encrypted_payload)
        api_key = str(payload.get("api_key", "")).strip()
        if not api_key:
            raise AdvisoryProviderUnavailableError(
                f"LLM provider '{provider_id}' credential is invalid"
            )
        return ResolvedLLMProviderCredential(provider_id=provider_id, api_key=api_key)

    def _is_ollama_remote_reachable(self, api_base: str) -> bool:
        if self._ollama_remote_reachable is not None:
            return self._ollama_remote_reachable
        try:
            with urlopen(
                urljoin(api_base.rstrip("/") + "/", "api/tags"),
                timeout=self._ollama_probe_timeout_seconds,
            ):
                return True
        except Exception:
            return False


class LiteLLMRequestComposer:
    def compose_chat_completion_kwargs(
        self,
        *,
        model: str,
        messages: Any,
        provider_credential: ResolvedLLMProviderCredential,
        temperature: float,
        max_tokens: int,
    ) -> dict[str, Any]:
        kwargs: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        extra_body: dict[str, str] = {}
        if provider_credential.api_key is not None:
            extra_body["api_key"] = provider_credential.api_key
        if provider_credential.api_base is not None:
            extra_body["api_base"] = provider_credential.api_base
        if extra_body:
            kwargs["extra_body"] = extra_body
        return kwargs


def _configured_value(*values: str | None) -> str | None:
    for value in values:
        if value is not None and value.strip():
            return value.strip()
    return None


def is_ollama_provider_configured(provider_id: str) -> bool:
    if provider_id == OLLAMA_REMOTE_PROVIDER_ID:
        return _configured_value(os.environ.get("OLLAMA_REMOTE_URL")) is not None
    if provider_id in {
        OLLAMA_PROVIDER_ID,
        OLLAMA_LOCAL_PROVIDER_ID,
        OLLAMA_AUTO_PROVIDER_ID,
    }:
        return True
    return False


def configured_ollama_model_hints() -> tuple[str, ...]:
    models = (
        _configured_value(os.environ.get("OLLAMA_REMOTE_MODEL")),
        _configured_value(os.environ.get("OLLAMA_LOCAL_MODEL")),
    )
    return tuple(model for model in models if model is not None)
