"""Tests for TF-F055: admin credential management endpoints."""
from __future__ import annotations

import os
from pathlib import Path

from fastapi.testclient import TestClient
from src.app.api.application import create_app
from src.security import CredentialStore, KeyManager
from src.security.credential import CredentialStatus


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


def test_litellm_non_secret_field_shows_display_value(tmp_path: Path) -> None:
    client, _ = _make_app_with_store(tmp_path)
    with _master_key():
        client.put(
            "/admin/credentials/litellm",
            json={
                "fields": {
                    "base_url": "http://localhost:4000",
                    "api_key": "secret_groq_key",
                    "default_model": "groq/llama-3.1-70b-versatile",
                }
            },
        )
        response = client.get("/admin/credentials")
    body = response.json()
    litellm = next(c for c in body["credentials"] if c["provider_id"] == "litellm")
    base_url_field = next(f for f in litellm["fields"] if f["name"] == "base_url")
    model_field = next(f for f in litellm["fields"] if f["name"] == "default_model")
    api_key_field = next(f for f in litellm["fields"] if f["name"] == "api_key")
    # Non-secret: display_value populated
    assert base_url_field["display_value"] == "http://localhost:4000"
    assert base_url_field["masked_value"] is None
    assert model_field["display_value"] == "groq/llama-3.1-70b-versatile"
    # Secret: masked only
    assert api_key_field["masked_value"] is not None
    assert api_key_field["display_value"] is None


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
