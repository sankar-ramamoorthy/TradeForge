from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from src.app.api.application import create_app
from src.infrastructure.advisory.openai_compatible_provider import (
    OpenAICompatibleAdvisoryProvider,
)
from src.security import (
    CredentialStore,
    KeyManager,
    LiteLLMCredentialPayload,
    create_litellm_credential,
)


def test_create_app_without_litellm_credential_starts_and_reports_not_configured(
    tmp_path: Path,
) -> None:
    app = create_app(credential_store=CredentialStore(tmp_path / ".keys.enc"))

    assert app.state.ai_advisory_provider is None
    response = TestClient(app).get("/advisory/health")
    assert response.status_code == 200
    assert response.json()["status"] == "not_configured"


def test_create_app_builds_default_advisory_provider_from_litellm_credential(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    master_key = KeyManager.generate_master_key()
    monkeypatch.setenv("TRADEFORGE_MASTER_KEY", master_key)
    store = CredentialStore(tmp_path / ".keys.enc")
    store.save(
        create_litellm_credential(
            LiteLLMCredentialPayload(
                base_url="http://localhost:4000",
                api_key="litellm-key",
                default_model="configured-model",
            ),
            key_manager=KeyManager(master_key.encode("ascii")),
        )
    )

    app = create_app(credential_store=store)

    assert isinstance(app.state.ai_advisory_provider, OpenAICompatibleAdvisoryProvider)
    assert app.state.ai_advisory_provider.provider_id == "litellm"


def test_create_app_with_unreadable_litellm_credential_still_starts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_key = KeyManager.generate_master_key()
    runtime_key = KeyManager.generate_master_key()
    monkeypatch.setenv("TRADEFORGE_MASTER_KEY", runtime_key)
    store = CredentialStore(tmp_path / ".keys.enc")
    store.save(
        create_litellm_credential(
            LiteLLMCredentialPayload(
                base_url="http://localhost:4000",
                api_key="litellm-key",
                default_model="configured-model",
            ),
            key_manager=KeyManager(original_key.encode("ascii")),
        )
    )

    app = create_app(credential_store=store)

    assert app.state.ai_advisory_provider is None
    response = TestClient(app).get("/advisory/health")
    assert response.status_code == 200
    assert response.json()["status"] == "not_configured"
