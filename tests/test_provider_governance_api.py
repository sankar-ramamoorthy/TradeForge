from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from src.app.api.application import _default_provider_registry, create_app
from src.domain.advisory import (
    AdvisoryArtifactKind,
    AdvisoryAuthority,
    AdvisoryProvenance,
    AdvisoryRequest,
    AdvisoryResponse,
    AdvisoryUncertainty,
)
from src.domain.events import EventEnvelope, EventStore
from src.domain.market.capability import (
    CapabilityPreference,
    ProviderCapability,
    ProviderDescriptor,
)
from src.domain.market.registry import ProviderRegistry
from src.security import (
    Credential,
    CredentialStatus,
    CredentialStore,
    KeyManager,
    LiteLLMCredentialPayload,
    create_litellm_credential,
    get_advisory_model_selection_config,
)


def test_provider_governance_exposes_operational_boundary() -> None:
    client = TestClient(create_app())

    response = client.get("/provider-governance")

    assert response.status_code == 200
    body = response.json()
    assert body["authority"] == "operational"
    assert body["is_canonical"] is False
    assert body["lifecycle_authority"] is False
    assert body["event_ledger_writes"] is False
    assert body["diagnostics"]["event_ledger_authority"] is False


def test_provider_governance_includes_capability_routes() -> None:
    registry = ProviderRegistry(
        (
            ProviderDescriptor("fmp", (ProviderCapability.FUNDAMENTALS,)),
            ProviderDescriptor("alpha_vantage", (ProviderCapability.FUNDAMENTALS,)),
        ),
        (
            CapabilityPreference(
                ProviderCapability.FUNDAMENTALS,
                "fmp",
                ("alpha_vantage",),
            ),
            CapabilityPreference(ProviderCapability.PRICE, "yfinance"),
        ),
    )
    client = TestClient(create_app(provider_registry=registry))

    response = client.get("/provider-governance")

    assert response.status_code == 200
    routes = response.json()["routes"]
    fundamentals = next(
        route for route in routes if route["capability"] == "fundamentals"
    )
    assert fundamentals["preferred_provider_id"] == "fmp"
    assert fundamentals["fallback_provider_ids"] == ["alpha_vantage"]
    assert fundamentals["selected_provider_id"] == "fmp"
    assert fundamentals["degraded"] is False


def test_default_fundamentals_preference_uses_alpha_vantage_before_fmp(
    tmp_path: Path,
) -> None:
    store = CredentialStore(tmp_path / ".keys.enc")
    for provider_id in ("fmp", "alpha_vantage"):
        store.save(
            Credential(
                provider_id=provider_id,
                credential_type="api_key",
                encrypted_payload=b"unused",
                created_at=datetime(2026, 7, 13, tzinfo=UTC),
                rotated_at=None,
                last_validated_at=None,
                status=CredentialStatus.ACTIVE,
                provenance={"source": "test"},
            )
        )

    registry = _default_provider_registry(store)
    resolution = registry.resolve(ProviderCapability.FUNDAMENTALS)

    assert resolution.preferred_provider_id == "alpha_vantage"
    assert resolution.fallback_provider_ids == ("fmp",)
    assert resolution.selected_provider_id == "alpha_vantage"


def test_provider_governance_never_returns_credential_values(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    master_key = KeyManager.generate_master_key()
    monkeypatch.setenv("TRADEFORGE_MASTER_KEY", master_key)
    store = CredentialStore(tmp_path / ".keys.enc")
    client = TestClient(create_app(credential_store=store))
    secret = "pk_test_do_not_return_1234"

    update_response = client.put(
        "/admin/credentials/polygon",
        json={"fields": {"api_key": secret}},
    )
    assert update_response.status_code == 200

    response = client.get("/provider-governance")

    assert response.status_code == 200
    serialized = response.text
    assert secret not in serialized
    assert "1234" not in serialized
    body = response.json()
    polygon = next(
        credential
        for credential in body["credentials"]
        if credential["provider_id"] == "polygon"
    )
    assert polygon["configured"] is True
    assert polygon["status"] == "untested"
    assert polygon["exposes_secret_values"] is False


def test_provider_governance_reports_llm_provider_secret_without_value(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    master_key = KeyManager.generate_master_key()
    monkeypatch.setenv("TRADEFORGE_MASTER_KEY", master_key)
    key_manager = KeyManager(master_key.encode("ascii"))
    store = CredentialStore(tmp_path / ".keys.enc")
    store.save(
        Credential(
            provider_id="llm_groq",
            credential_type="api_key",
            encrypted_payload=key_manager.encrypt_payload(
                {"api_key": "groq-secret-value"}
            ),
            created_at=datetime(2026, 5, 25, tzinfo=UTC),
            rotated_at=None,
            last_validated_at=None,
            status=CredentialStatus.ACTIVE,
            provenance={"set_by": "operator", "source": "test"},
        )
    )
    client = TestClient(create_app(credential_store=store))

    response = client.get("/provider-governance")

    assert response.status_code == 200
    assert "groq-secret-value" not in response.text
    body = response.json()
    credential = next(
        item for item in body["credentials"] if item["provider_id"] == "llm_groq"
    )
    provider = next(
        item for item in body["providers"] if item["provider_id"] == "llm_groq"
    )
    assert credential["configured"] is True
    assert credential["exposes_secret_values"] is False
    assert provider["capabilities"] == ["llm_provider_secret"]


def test_provider_governance_reports_ollama_route_providers(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("OLLAMA_REMOTE_URL", raising=False)
    client = TestClient(create_app())

    response = client.get("/provider-governance")

    assert response.status_code == 200
    providers = {
        item["provider_id"]: item for item in response.json()["providers"]
    }
    for provider_id in ("ollama", "ollama-local", "ollama-auto", "ollama-remote"):
        assert providers[provider_id]["capabilities"] == ["llm_provider_route"]
        assert providers[provider_id]["credential_required"] is False
        assert providers[provider_id]["is_canonical"] is False
    assert providers["ollama"]["health_status"] == "available"
    assert providers["ollama-local"]["health_status"] == "available"
    assert providers["ollama-auto"]["health_status"] == "available"
    assert providers["ollama-remote"]["health_status"] == "not_configured"


def test_provider_governance_reports_ollama_remote_configured_from_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("OLLAMA_REMOTE_URL", "http://remote-ollama:11434")
    client = TestClient(create_app())

    response = client.get("/provider-governance")

    assert response.status_code == 200
    providers = {
        item["provider_id"]: item for item in response.json()["providers"]
    }
    assert providers["ollama-remote"]["credential_required"] is False
    assert providers["ollama-remote"]["registry_configured"] is True
    assert providers["ollama-remote"]["health_status"] == "available"


def test_ai_gateway_provider_secret_injection_reports_status_without_secret(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    master_key = KeyManager.generate_master_key()
    monkeypatch.setenv("TRADEFORGE_MASTER_KEY", master_key)
    key_manager = KeyManager(master_key.encode("ascii"))
    store = CredentialStore(tmp_path / ".keys.enc")
    store.save(
        Credential(
            provider_id="llm_groq",
            credential_type="api_key",
            encrypted_payload=key_manager.encrypt_payload(
                {"api_key": "groq-secret-value"}
            ),
            created_at=datetime(2026, 5, 25, tzinfo=UTC),
            rotated_at=None,
            last_validated_at=None,
            status=CredentialStatus.ACTIVE,
            provenance={"set_by": "operator", "source": "test"},
        )
    )
    client = TestClient(create_app(credential_store=store))

    response = client.get(
        "/provider-governance/ai-gateway/provider-secret-injection"
    )

    assert response.status_code == 200
    assert "groq-secret-value" not in response.text
    body = response.json()
    assert body["authority"] == "operational"
    assert body["exposes_secret_values"] is False
    assert body["runtime_decryption_boundary"] == "composition"
    assert body["event_ledger_writes"] is False
    assert body["injectable_environment_variables"] == ["GROQ_API_KEY"]
    groq = next(
        item for item in body["provider_secrets"] if item["provider_id"] == "llm_groq"
    )
    assert groq["configured"] is True
    assert groq["available_for_runtime_injection"] is True


def test_ai_gateway_provider_secret_injection_is_stateless_request_time(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    master_key = KeyManager.generate_master_key()
    monkeypatch.setenv("TRADEFORGE_MASTER_KEY", master_key)
    key_manager = KeyManager(master_key.encode("ascii"))
    store = CredentialStore(tmp_path / ".keys.enc")
    store.save(
        Credential(
            provider_id="llm_groq",
            credential_type="api_key",
            encrypted_payload=key_manager.encrypt_payload(
                {"api_key": "groq-secret-value"}
            ),
            created_at=datetime(2026, 5, 25, tzinfo=UTC),
            rotated_at=None,
            last_validated_at=None,
            status=CredentialStatus.ACTIVE,
            provenance={"set_by": "operator", "source": "test"},
        )
    )
    client = TestClient(create_app(credential_store=store))

    response = client.get(
        "/provider-governance/ai-gateway/provider-secret-injection"
    )

    assert response.status_code == 200
    body = response.json()
    assert body["injectable_environment_variables"] == ["GROQ_API_KEY"]
    groq = next(
        item for item in body["provider_secrets"] if item["provider_id"] == "llm_groq"
    )
    assert groq["configured"] is True
    assert groq["available_for_runtime_injection"] is True


def test_provider_governance_reports_litellm_gateway_aliases(
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
                api_key="litellm-secret",
                default_model="configured-model",
            ),
            key_manager=KeyManager(master_key.encode("ascii")),
        )
    )
    client = TestClient(create_app(credential_store=store))

    response = client.get("/provider-governance")

    assert response.status_code == 200
    gateway = response.json()["ai_gateway"]
    assert gateway["gateway_id"] == "litellm"
    assert gateway["configured"] is True
    assert gateway["status"] == "configured"
    assert gateway["gateway_url"] == "http://localhost:4000"
    assert gateway["default_model"] == "configured-model"
    assert gateway["underlying_provider_id"] == "legacy"
    assert gateway["reachability"] == "not_checked"
    assert "litellm-secret" not in response.text
    aliases = {route["alias"] for route in gateway["route_aliases"]}
    expected_aliases = {
        "tf-fast",
        "tf-reasoning",
        "tf-long-context",
        "tf-cheap",
        "tf-local",
    }
    assert expected_aliases <= aliases
    assert gateway["lifecycle_authority"] is False
    assert gateway["execution_authority"] is False


def test_ai_gateway_visibility_endpoint_exposes_route_target_provider(
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
                api_key="litellm-secret",
                default_model="groq/llama-3.1-70b-versatile",
            ),
            key_manager=KeyManager(master_key.encode("ascii")),
        )
    )
    client = TestClient(create_app(credential_store=store))

    response = client.get("/provider-governance/ai-gateway")

    assert response.status_code == 200
    gateway = response.json()
    assert gateway["gateway_id"] == "litellm"
    assert gateway["gateway_url"] == "http://localhost:4000"
    assert gateway["default_model"] == "groq/llama-3.1-70b-versatile"
    assert gateway["underlying_provider_id"] == "llm_groq"
    assert gateway["primary_provider_id"] == "llm_groq"
    assert gateway["reachability"] == "not_checked"
    assert "litellm-secret" not in response.text
    alias = next(
        route
        for route in gateway["route_aliases"]
        if route["alias"] == "tf-reasoning"
    )
    assert alias["advisory_usage_domain"] == "reasoned interpretation"
    assert alias["route_target_model"] == "groq/llama-3.1-70b-versatile"
    assert alias["underlying_provider_id"] == "llm_groq"
    assert alias["route_target_provider_id"] == "llm_groq"
    assert alias["availability_status"] == "configured"


def test_ai_gateway_model_selection_reports_configured_models_without_probe(
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
                api_key="litellm-secret",
                default_model="primary-model",
                fallback_model="fallback-model",
            ),
            key_manager=KeyManager(master_key.encode("ascii")),
        )
    )
    client = TestClient(
        create_app(credential_store=store, ai_advisory_provider=_FakeAdvisoryProvider())
    )

    response = client.get("/provider-governance/ai-gateway/model-selection")

    assert response.status_code == 200
    body = response.json()
    assert body["authority"] == "operational"
    assert body["is_canonical"] is False
    assert body["event_ledger_writes"] is False
    assert body["discovery_status"] == "available"
    assert body["available_models"] == ["fallback-model", "primary-model"]
    assert body["selected_primary_model"] == "primary-model"
    assert body["selected_fallback_model"] == "fallback-model"


def test_ai_gateway_model_selection_updates_litellm_credential_without_event_write(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    master_key = KeyManager.generate_master_key()
    monkeypatch.setenv("TRADEFORGE_MASTER_KEY", master_key)
    event_store = _CountingEventStore()
    store = CredentialStore(tmp_path / ".keys.enc")
    store.save(
        create_litellm_credential(
            LiteLLMCredentialPayload(
                base_url="http://localhost:4000",
                api_key="litellm-secret",
                default_model="primary-model",
            ),
            key_manager=KeyManager(master_key.encode("ascii")),
        )
    )
    client = TestClient(
        create_app(
            credential_store=store,
            event_store=event_store,
            ai_advisory_provider=_FakeAdvisoryProvider(),
        )
    )

    response = client.put(
        "/provider-governance/ai-gateway/model-selection",
        json={
            "primary_provider_id": "llm_groq",
            "primary_model": "third-model",
            "fallback_provider_id": "llm_groq",
            "fallback_model": "fallback-model",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["selected_primary_model"] == "third-model"
    assert body["selected_fallback_model"] == "fallback-model"
    assert event_store.append_calls == 0
    stored = get_advisory_model_selection_config(
        store,
        key_manager=KeyManager(master_key.encode("ascii")),
    )
    assert stored is not None
    assert stored.primary_provider_id == "llm_groq"
    assert stored.primary_model == "third-model"
    assert stored.fallback_provider_id == "llm_groq"
    assert stored.fallback_model == "fallback-model"


def test_ai_gateway_model_selection_accepts_ollama_remote_provider(
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
                api_key="litellm-secret",
                default_model="primary-model",
            ),
            key_manager=KeyManager(master_key.encode("ascii")),
        )
    )
    client = TestClient(
        create_app(credential_store=store, ai_advisory_provider=_FakeAdvisoryProvider())
    )

    response = client.put(
        "/provider-governance/ai-gateway/model-selection",
        json={
            "primary_provider_id": "ollama-remote",
            "primary_model": "ollama/llama3.1:8b",
            "fallback_provider_id": "ollama-local",
            "fallback_model": "ollama/granite4:350m",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["selected_primary_provider_id"] == "ollama-remote"
    assert body["selected_primary_model"] == "ollama/llama3.1:8b"
    assert body["selected_fallback_provider_id"] == "ollama-local"
    assert body["selected_fallback_model"] == "ollama/granite4:350m"


def test_ai_gateway_model_selection_includes_ollama_model_hints(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    master_key = KeyManager.generate_master_key()
    monkeypatch.setenv("TRADEFORGE_MASTER_KEY", master_key)
    monkeypatch.setenv("OLLAMA_REMOTE_MODEL", "ollama/remote-model")
    monkeypatch.setenv("OLLAMA_LOCAL_MODEL", "ollama/local-model")
    store = CredentialStore(tmp_path / ".keys.enc")
    store.save(
        create_litellm_credential(
            LiteLLMCredentialPayload(
                base_url="http://localhost:4000",
                api_key="litellm-secret",
                default_model="primary-model",
            ),
            key_manager=KeyManager(master_key.encode("ascii")),
        )
    )
    client = TestClient(
        create_app(credential_store=store, ai_advisory_provider=_FakeAdvisoryProvider())
    )

    response = client.get("/provider-governance/ai-gateway/model-selection")

    assert response.status_code == 200
    assert response.json()["available_models"] == [
        "ollama/local-model",
        "ollama/remote-model",
        "primary-model",
    ]


def test_ai_gateway_model_selection_requires_explicit_provider_identity(
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
                api_key="litellm-secret",
                default_model="primary-model",
            ),
            key_manager=KeyManager(master_key.encode("ascii")),
        )
    )
    client = TestClient(
        create_app(credential_store=store, ai_advisory_provider=_FakeAdvisoryProvider())
    )

    response = client.put(
        "/provider-governance/ai-gateway/model-selection",
        json={"primary_model": "groq/llama-3.1-70b-versatile", "fallback_model": None},
    )

    assert response.status_code == 422


def test_ai_gateway_visibility_endpoint_reports_not_configured(
    tmp_path: Path,
) -> None:
    client = TestClient(
        create_app(credential_store=CredentialStore(tmp_path / ".keys.enc"))
    )

    response = client.get("/provider-governance/ai-gateway")

    assert response.status_code == 200
    gateway = response.json()
    assert gateway["configured"] is False
    assert gateway["status"] == "not_configured"
    assert gateway["gateway_url"] is None
    assert gateway["default_model"] is None
    assert all(
        route["availability_status"] == "not_configured"
        for route in gateway["route_aliases"]
    )


def test_provider_governance_does_not_mutate_event_store() -> None:
    event_store = _CountingEventStore()
    client = TestClient(create_app(event_store=event_store))

    response = client.get("/provider-governance")

    assert response.status_code == 200
    assert event_store.append_calls == 0


def test_ai_gateway_smoke_test_uses_advisory_provider_without_event_write() -> None:
    event_store = _CountingEventStore()
    provider = _FakeAdvisoryProvider()
    client = TestClient(
        create_app(event_store=event_store, ai_advisory_provider=provider)
    )

    response = client.post("/provider-governance/ai-gateway/smoke-test", json={})

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "available"
    assert body["authority"] == "operational"
    assert body["is_canonical"] is False
    assert body["lifecycle_authority"] is False
    assert body["execution_authority"] is False
    assert body["event_ledger_writes"] is False
    assert body["advisory_response_authority"] == "advisory"
    assert body["provider_id"] == "litellm"
    assert body["model_id"] == "tradeforge-ollama"
    assert provider.request_count == 1
    assert event_store.append_calls == 0


def test_ai_gateway_smoke_test_reports_ollama_remote_provider_identity() -> None:
    event_store = _CountingEventStore()
    provider = _FakeAdvisoryProvider(
        provider_id="ollama-remote",
        model_id="ollama/llama3.1:8b",
    )
    client = TestClient(
        create_app(event_store=event_store, ai_advisory_provider=provider)
    )

    response = client.post("/provider-governance/ai-gateway/smoke-test", json={})

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "available"
    assert body["provider_id"] == "ollama-remote"
    assert body["model_id"] == "ollama/llama3.1:8b"
    assert body["event_ledger_writes"] is False
    assert event_store.append_calls == 0


def test_ai_gateway_smoke_test_reports_not_configured_without_event_write(
    tmp_path: Path,
) -> None:
    event_store = _CountingEventStore()
    client = TestClient(
        create_app(
            event_store=event_store,
            credential_store=CredentialStore(tmp_path / ".keys.enc"),
        )
    )

    response = client.post("/provider-governance/ai-gateway/smoke-test", json={})

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "not_configured"
    assert body["provider_id"] is None
    assert body["advisory_response_authority"] is None
    assert event_store.append_calls == 0


class _CountingEventStore(EventStore):
    def __init__(self) -> None:
        self.append_calls = 0

    def append(self, event: EventEnvelope) -> None:
        self.append_calls += 1

    def read_events(self) -> tuple[EventEnvelope, ...]:
        return ()


class _FakeAdvisoryProvider:
    provider_version = "fake-test-provider"

    def __init__(
        self,
        *,
        provider_id: str = "litellm",
        model_id: str = "tradeforge-ollama",
    ) -> None:
        self.provider_id = provider_id
        self.model_id = model_id
        self.request_count = 0

    def list_models(self) -> tuple[str, ...]:
        return ("primary-model", "fallback-model", "third-model")

    def generate(self, request: AdvisoryRequest) -> AdvisoryResponse:
        self.request_count += 1
        assert request.artifact_kind is AdvisoryArtifactKind.CONTEXT_SUMMARY
        assert request.persona_id == "provider-governance"
        assert request.workspace_id == "provider-governance"
        return AdvisoryResponse(
            request_id=request.request_id,
            artifact_kind=request.artifact_kind,
            content="advisory route smoke test ok",
            provenance=AdvisoryProvenance(
                provider_id=self.provider_id,
                provider_version=self.provider_version,
                model_id=self.model_id,
                generated_at=datetime.now(UTC),
                prompt_version="test",
            ),
            uncertainty=AdvisoryUncertainty(
                confidence=0.5,
                caveats=("Operational smoke test only.",),
            ),
            source_references=request.source_references,
            authority=AdvisoryAuthority.ADVISORY,
        )
