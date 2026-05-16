from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from src.app.api.application import create_app
from src.domain.market.snapshot import (
    MarketSnapshot,
    PriceOHLCV,
    ProviderProvenance,
)
from src.security import Credential, CredentialStatus, CredentialStore, KeyManager

_TS = datetime(2026, 5, 16, 20, 0, tzinfo=UTC)


def _credential_store(
    tmp_path: Path,
    provider_id: str,
    payload: dict[str, str],
) -> tuple[CredentialStore, str]:
    master_key = KeyManager.generate_master_key()
    key_manager = KeyManager(master_key.encode("ascii"))
    credential = Credential(
        provider_id=provider_id,
        credential_type="api_key+secret" if "secret_key" in payload else "api_key",
        encrypted_payload=key_manager.encrypt_payload(payload),
        created_at=_TS,
        rotated_at=None,
        last_validated_at=None,
        status=CredentialStatus.ACTIVE,
        provenance={"set_by": "operator", "source": "test"},
    )
    store = CredentialStore(tmp_path / ".keys.enc")
    store.save(credential)
    return store, master_key


def _snapshot(symbol: str, provider_id: str) -> MarketSnapshot:
    return MarketSnapshot(
        price=PriceOHLCV(
            symbol=symbol,
            open=Decimal("100"),
            high=Decimal("105"),
            low=Decimal("99"),
            close=Decimal("103"),
            volume=1_000,
            as_of=_TS,
        ),
        provenance=ProviderProvenance(
            provider_id=provider_id,
            provider_version="test",
            fetched_at=_TS,
            data_as_of=_TS,
        ),
    )


def test_create_app_uses_decrypted_polygon_credential_for_market_context(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store, master_key = _credential_store(
        tmp_path,
        "polygon",
        {"api_key": "polygon-secret"},
    )
    monkeypatch.setenv("TRADEFORGE_MASTER_KEY", master_key)
    monkeypatch.setenv("TRADEFORGE_MARKET_PROVIDER", "polygon")

    provider = MagicMock()
    provider.provider_id = "polygon"
    provider.provider_version = "test"
    provider.fetch_snapshot.side_effect = lambda symbol: _snapshot(symbol, "polygon")

    with patch(
        "src.app.api.application.PolygonProvider",
        return_value=provider,
    ) as provider_cls:
        client = TestClient(create_app(credential_store=store))
        response = client.get("/workspaces/market-context?symbols=AAPL")

    assert response.status_code == 200
    assert response.json()["provider_id"] == "polygon"
    provider_cls.assert_called_once_with(api_key="polygon-secret")


def test_create_app_uses_decrypted_alpaca_credential_for_market_context(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store, master_key = _credential_store(
        tmp_path,
        "alpaca",
        {"api_key": "alpaca-key", "secret_key": "alpaca-secret"},
    )
    monkeypatch.setenv("TRADEFORGE_MASTER_KEY", master_key)
    monkeypatch.setenv("TRADEFORGE_MARKET_PROVIDER", "alpaca")

    provider = MagicMock()
    provider.provider_id = "alpaca"
    provider.provider_version = "test"
    provider.fetch_snapshot.side_effect = lambda symbol: _snapshot(symbol, "alpaca")

    with patch(
        "src.app.api.application.AlpacaProvider",
        return_value=provider,
    ) as provider_cls:
        client = TestClient(create_app(credential_store=store))
        response = client.get("/workspaces/market-context?symbols=SPY")

    assert response.status_code == 200
    assert response.json()["provider_id"] == "alpaca"
    provider_cls.assert_called_once_with(
        api_key="alpaca-key",
        secret_key="alpaca-secret",
    )
