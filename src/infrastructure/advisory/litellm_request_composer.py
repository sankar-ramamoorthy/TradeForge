from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from src.domain.advisory.contracts import AdvisoryProviderUnavailableError
from src.security.credential import CredentialStatus
from src.security.credential_store import CredentialStore
from src.security.key_manager import KeyManager
from src.security.llm_provider_secrets import LLM_PROVIDER_SECRET_SCHEMA_BY_ID


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
    ) -> None:
        self._credential_store = credential_store
        self._key_manager = key_manager
        self._ollama_api_base = (
            ollama_api_base
            or os.environ.get("OLLAMA_API_BASE")
            or "http://host.docker.internal:11434"
        )

    def resolve(self, provider_id: str) -> ResolvedLLMProviderCredential:
        if provider_id == "ollama":
            return ResolvedLLMProviderCredential(
                provider_id=provider_id,
                api_base=self._ollama_api_base,
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
