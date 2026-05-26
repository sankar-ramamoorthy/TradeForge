"""Tests for TF-F055: admin credential management endpoints."""
from __future__ import annotations

import os
from datetime import UTC, datetime
from pathlib import Path

from fastapi.testclient import TestClient
from src.app.api.application import create_app
from src.security import CredentialStore, KeyManager
from src.security.credential import Credential, CredentialStatus


def _make_app_with_store(tmp_path: Path) -> tuple[TestClient, CredentialStore]:
    store_path = tmp_path / ".keys.enc"
    store = CredentialStore(store_path)
    app = create_app(credential_store=store)
    return TestClient(app), store


def test_list_credentials_returns_all_known_providers(tmp_path: Path) -> None:
    client, _ = _make_app_with_store(tmp_path)
    with _master_key():
        response = client.get("/admin/credentials")
    assert response.status_code == 200
    body = response.json()
    provider_ids = {c["provider_id"] for c in body["credentials"]}
    assert "yfinance" in provider_ids
    assert "polygon" in provider_ids
    assert "alpaca" in provider_ids
    assert "fmp" in provider_ids
    assert "alpha_vantage" in provider_ids
    assert "litellm" in provider_ids
    assert "llm_groq" in provider_ids
    assert "llm_nvidia_nim" in provider_ids
    assert "llm_openai" in provider_ids
    assert "llm_anthropic" in provider_ids
    assert "llm_google" in provider_ids


def test_yfinance_always_shows_configured(tmp_path: Path) -> None:
    client, _ = _make_app_with_store(tmp_path)
    with _master_key():
        response = client.get("/admin/credentials")
    body = response.json()
    yfinance = next(c for c in body["credentials"] if c["provider_id"] == "yfinance")
    assert yfinance["configured"] is True
    assert yfinance["fields"] == []


def test_unconfigured_provider_shows_not_configured(tmp_path: Path) -> None:
    client, _ = _make_app_with_store(tmp_path)
    with _master_key():
        response = client.get("/admin/credentials")
    body = response.json()
    polygon = next(c for c in body["credentials"] if c["provider_id"] == "polygon")
    assert polygon["configured"] is False
    assert polygon["status"] is None


def test_list_without_master_key_returns_unconfigured_warning(tmp_path: Path) -> None:
    client, _ = _make_app_with_store(tmp_path)
    with _no_master_key():
        response = client.get("/admin/credentials")
    # Should succeed (GET works even without master key — shows degraded state)
    assert response.status_code == 200
    body = response.json()
    assert body["master_key_configured"] is False


def test_update_credential_saves_and_masks(tmp_path: Path) -> None:
    client, store = _make_app_with_store(tmp_path)
    with _master_key():
        response = client.put(
            "/admin/credentials/polygon",
            json={"fields": {"api_key": "pk_test_abcdefgh1234"}},
        )
    assert response.status_code == 200
    body = response.json()
    assert body["configured"] is True
    assert body["provider_id"] == "polygon"
    # Secret must be masked — last 4 chars only
    api_key_field = next(f for f in body["fields"] if f["name"] == "api_key")
    assert api_key_field["masked_value"] is not None
    assert "1234" in api_key_field["masked_value"]
    assert "pk_test" not in api_key_field["masked_value"]
    assert api_key_field["display_value"] is None


def test_update_credential_rejects_unknown_provider(tmp_path: Path) -> None:
    client, _ = _make_app_with_store(tmp_path)
    with _master_key():
        response = client.put(
            "/admin/credentials/unknown_provider",
            json={"fields": {"api_key": "test"}},
        )
    assert response.status_code == 422


def test_update_credential_rejects_missing_fields(tmp_path: Path) -> None:
    client, _ = _make_app_with_store(tmp_path)
    with _master_key():
        # alpaca requires api_key AND secret_key
        response = client.put(
            "/admin/credentials/alpaca",
            json={"fields": {"api_key": "only_one_key"}},
        )
    assert response.status_code == 422


def test_update_credential_without_master_key_returns_503(tmp_path: Path) -> None:
    client, _ = _make_app_with_store(tmp_path)
    with _no_master_key():
        response = client.put(
            "/admin/credentials/polygon",
            json={"fields": {"api_key": "test"}},
        )
    assert response.status_code == 503


def test_update_credential_persists_to_store(tmp_path: Path) -> None:
    client, store = _make_app_with_store(tmp_path)
    with _master_key():
        client.put(
            "/admin/credentials/fmp",
            json={"fields": {"api_key": "fmp_secret_key_xyz"}},
        )
        saved = store.get("fmp")
        assert saved is not None
        assert saved.status is CredentialStatus.ACTIVE
        km = KeyManager.from_environment()
        payload = km.decrypt_payload(saved.encrypted_payload)
        assert payload["api_key"] == "fmp_secret_key_xyz"


def test_revoke_credential(tmp_path: Path) -> None:
    client, store = _make_app_with_store(tmp_path)
    with _master_key():
        client.put(
            "/admin/credentials/fmp",
            json={"fields": {"api_key": "fmp_secret_key_xyz"}},
        )
        response = client.delete("/admin/credentials/fmp")
    assert response.status_code == 200
    body = response.json()
    assert body["configured"] is False
    assert body["status"] == "revoked"
    saved = store.get("fmp")
    assert saved is not None
    assert saved.status is CredentialStatus.REVOKED


def test_revoke_unconfigured_provider_returns_404(tmp_path: Path) -> None:
    client, _ = _make_app_with_store(tmp_path)
    with _master_key():
        response = client.delete("/admin/credentials/polygon")
    assert response.status_code == 404


def test_litellm_gateway_base_url_shows_display_value(tmp_path: Path) -> None:
    client, _ = _make_app_with_store(tmp_path)
    with _master_key():
        client.put(
            "/admin/credentials/litellm",
            json={
                "fields": {
                    "base_url": "http://localhost:4000",
                    "api_key": "secret_groq_key",
                }
            },
        )
        response = client.get("/admin/credentials")
    body = response.json()
    litellm = next(c for c in body["credentials"] if c["provider_id"] == "litellm")
    base_url_field = next(f for f in litellm["fields"] if f["name"] == "base_url")
    api_key_field = next(f for f in litellm["fields"] if f["name"] == "api_key")
    # Non-secret: display_value populated
    assert base_url_field["display_value"] == "http://localhost:4000"
    assert base_url_field["masked_value"] is None
    # Secret: masked only
    assert api_key_field["masked_value"] is not None
    assert api_key_field["display_value"] is None


def test_llm_provider_secret_is_masked_and_never_displayed(tmp_path: Path) -> None:
    client, _ = _make_app_with_store(tmp_path)
    secret = "groq_secret_value_1234"
    with _master_key():
        response = client.put(
            "/admin/credentials/llm_groq",
            json={"fields": {"api_key": secret}},
        )
        list_response = client.get("/admin/credentials")

    assert response.status_code == 200
    assert secret not in response.text
    assert secret not in list_response.text
    body = list_response.json()
    credential = next(
        item for item in body["credentials"] if item["provider_id"] == "llm_groq"
    )
    field = next(item for item in credential["fields"] if item["name"] == "api_key")
    assert field["masked_value"] is not None
    assert "1234" in field["masked_value"]
    assert field["display_value"] is None


def test_update_sets_rotated_at_on_second_save(tmp_path: Path) -> None:
    client, _ = _make_app_with_store(tmp_path)
    with _master_key():
        r1 = client.put(
            "/admin/credentials/polygon",
            json={"fields": {"api_key": "first_key"}},
        )
        r2 = client.put(
            "/admin/credentials/polygon",
            json={"fields": {"api_key": "second_key"}},
        )
    assert r1.json()["rotated_at"] is None  # first save: no rotated_at
    assert r2.json()["rotated_at"] is not None  # second save: rotated_at set


def test_validate_credential_sets_last_validated_at(tmp_path: Path) -> None:
    client, store = _make_app_with_store(tmp_path)
    with _master_key():
        client.put(
            "/admin/credentials/polygon",
            json={"fields": {"api_key": "pk_test_validation_key"}},
        )
        response = client.post("/admin/credentials/polygon/validate")
        saved = store.get("polygon")

    assert response.status_code == 200
    body = response.json()
    assert body["configured"] is True
    assert body["status"] == "active"
    assert body["last_validated_at"] is not None
    assert saved is not None
    assert saved.status is CredentialStatus.ACTIVE
    assert saved.last_validated_at is not None
    assert "pk_test_validation_key" not in response.text


def test_validate_missing_credential_returns_404(tmp_path: Path) -> None:
    client, _ = _make_app_with_store(tmp_path)
    with _master_key():
        response = client.post("/admin/credentials/polygon/validate")

    assert response.status_code == 404


def test_validate_revoked_credential_returns_409(tmp_path: Path) -> None:
    client, _ = _make_app_with_store(tmp_path)
    with _master_key():
        client.put(
            "/admin/credentials/polygon",
            json={"fields": {"api_key": "pk_test_validation_key"}},
        )
        client.delete("/admin/credentials/polygon")
        response = client.post("/admin/credentials/polygon/validate")

    assert response.status_code == 409


def test_validate_unreadable_payload_marks_credential_invalid(tmp_path: Path) -> None:
    client, store = _make_app_with_store(tmp_path)
    original_key = KeyManager.generate_master_key()
    runtime_key = KeyManager.generate_master_key()
    store.save(
        Credential(
            provider_id="polygon",
            credential_type="api_key",
            encrypted_payload=KeyManager(original_key.encode("ascii")).encrypt_payload(
                {"api_key": "pk_test_unreadable"}
            ),
            created_at=datetime.now(UTC),
            rotated_at=None,
            last_validated_at=None,
            status=CredentialStatus.ACTIVE,
            provenance={"set_by": "test", "source": "test"},
        )
    )

    original_env = os.environ.get("TRADEFORGE_MASTER_KEY")
    os.environ["TRADEFORGE_MASTER_KEY"] = runtime_key
    try:
        response = client.post("/admin/credentials/polygon/validate")
        saved = store.get("polygon")
    finally:
        if original_env is not None:
            os.environ["TRADEFORGE_MASTER_KEY"] = original_env
        else:
            os.environ.pop("TRADEFORGE_MASTER_KEY", None)

    assert response.status_code == 200
    assert response.json()["status"] == "invalid"
    assert saved is not None
    assert saved.status is CredentialStatus.INVALID


class _no_master_key:
    """Context manager that temporarily removes TRADEFORGE_MASTER_KEY for testing."""

    _original_key: str | None

    def __enter__(self) -> _no_master_key:
        self._original_key = os.environ.pop("TRADEFORGE_MASTER_KEY", None)
        return self

    def __exit__(self, *_: object) -> None:
        if self._original_key is not None:
            os.environ["TRADEFORGE_MASTER_KEY"] = self._original_key


class _master_key:
    """Context manager that temporarily overrides TRADEFORGE_MASTER_KEY for testing.

    Restores the original value (or removes the variable) on exit so that
    other tests are not affected by the key set here.
    """

    _generated_key: str
    _original_key: str | None

    def __enter__(self) -> _master_key:
        self._original_key = os.environ.get("TRADEFORGE_MASTER_KEY")
        self._generated_key = KeyManager.generate_master_key()
        os.environ["TRADEFORGE_MASTER_KEY"] = self._generated_key
        return self

    def __exit__(self, *_: object) -> None:
        if self._original_key is not None:
            os.environ["TRADEFORGE_MASTER_KEY"] = self._original_key
        else:
            os.environ.pop("TRADEFORGE_MASTER_KEY", None)
