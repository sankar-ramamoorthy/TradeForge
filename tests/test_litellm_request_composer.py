from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest
from src.domain.advisory import AdvisoryProviderUnavailableError
from src.infrastructure.advisory.litellm_request_composer import (
    LiteLLMRequestComposer,
    LLMProviderCredentialResolver,
)
from src.security import Credential, CredentialStatus, CredentialStore, KeyManager


def test_resolver_decrypts_active_groq_key_for_request_composition(
    tmp_path: Path,
) -> None:
    key_manager = KeyManager(KeyManager.generate_master_key().encode("ascii"))
    store = CredentialStore(tmp_path / ".keys.enc")
    store.save(
        Credential(
            provider_id="llm_groq",
            credential_type="api_key",
            encrypted_payload=key_manager.encrypt_payload({"api_key": "groq-key"}),
            created_at=datetime(2026, 5, 26, tzinfo=UTC),
            rotated_at=None,
            last_validated_at=None,
            status=CredentialStatus.ACTIVE,
            provenance={"set_by": "test", "source": "test"},
        )
    )

    resolved = LLMProviderCredentialResolver(
        store,
        key_manager=key_manager,
    ).resolve("llm_groq")

    assert resolved.provider_id == "llm_groq"
    assert resolved.api_key == "groq-key"
    assert resolved.api_base is None


def test_resolver_treats_ollama_as_keyless_internal_provider() -> None:
    resolved = LLMProviderCredentialResolver(
        None,
        key_manager=None,
        ollama_api_base="http://ollama:11434",
    ).resolve("ollama")

    assert resolved.provider_id == "ollama"
    assert resolved.api_key is None
    assert resolved.api_base == "http://ollama:11434"
    assert resolved.requires_api_key is False


def test_resolver_reports_missing_required_key_unavailable(tmp_path: Path) -> None:
    resolver = LLMProviderCredentialResolver(
        CredentialStore(tmp_path / ".keys.enc"),
        key_manager=KeyManager(KeyManager.generate_master_key().encode("ascii")),
    )

    with pytest.raises(AdvisoryProviderUnavailableError):
        resolver.resolve("llm_groq")


def test_composer_includes_request_scoped_secret_values_only_when_present() -> None:
    resolver = LLMProviderCredentialResolver(
        None,
        key_manager=None,
        ollama_api_base="http://ollama:11434",
    )
    kwargs = LiteLLMRequestComposer().compose_chat_completion_kwargs(
        model="ollama/granite4:350m",
        messages=[{"role": "user", "content": "test"}],
        provider_credential=resolver.resolve("ollama"),
        temperature=0.3,
        max_tokens=1500,
    )

    assert kwargs["model"] == "ollama/granite4:350m"
    assert kwargs["extra_body"] == {"api_base": "http://ollama:11434"}
