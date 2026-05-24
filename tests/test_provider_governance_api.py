from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from src.app.api.application import create_app
from src.domain.events import EventEnvelope, EventStore
from src.domain.market.capability import (
    CapabilityPreference,
    ProviderCapability,
    ProviderDescriptor,
)
from src.domain.market.registry import ProviderRegistry
from src.security import (
    CredentialStore,
    KeyManager,
    LiteLLMCredentialPayload,
    create_litellm_credential,
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
    assert gateway["underlying_provider_id"] is None
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
    assert gateway["underlying_provider_id"] == "groq"
    assert gateway["reachability"] == "not_checked"
    assert "litellm-secret" not in response.text
    alias = next(
        route
        for route in gateway["route_aliases"]
        if route["alias"] == "tf-reasoning"
    )
    assert alias["advisory_usage_domain"] == "reasoned interpretation"
    assert alias["route_target_model"] == "groq/llama-3.1-70b-versatile"
    assert alias["underlying_provider_id"] == "groq"
    assert alias["availability_status"] == "configured"


def test_ai_gateway_visibility_endpoint_reports_not_configured() -> None:
    client = TestClient(create_app())

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


class _CountingEventStore(EventStore):
    def __init__(self) -> None:
        self.append_calls = 0

    def append(self, event: EventEnvelope) -> None:
        self.append_calls += 1

    def read_events(self) -> tuple[EventEnvelope, ...]:
        return ()
