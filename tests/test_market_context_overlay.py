"""
Tests for TF-0047: market context workspace overlay API endpoint.

All tests inject a MarketSnapshotService backed by a mocked provider —
no real network calls are made.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from src.app.api.application import create_app
from src.domain.market.provider import ProviderUnavailableError
from src.domain.market.snapshot import (
    MarketSnapshot,
    PriceOHLCV,
    ProviderProvenance,
)
from src.services.market.snapshot_service import MarketSnapshotService

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_TS = datetime(2026, 5, 12, 20, 0, 0, tzinfo=UTC)


def _make_snapshot(symbol: str = "AAPL") -> MarketSnapshot:
    provenance = ProviderProvenance(
        provider_id="yfinance",
        provider_version="1.3.0",
        fetched_at=_TS,
        data_as_of=_TS,
    )
    price = PriceOHLCV(
        symbol=symbol,
        open=Decimal("185.00"),
        high=Decimal("187.50"),
        low=Decimal("184.20"),
        close=Decimal("186.40"),
        volume=52_000_000,
        as_of=_TS,
    )
    return MarketSnapshot(price=price, provenance=provenance)


def _make_provider(*failing_symbols: str) -> MagicMock:
    """Return a mocked provider that fails for the given symbols."""
    mock = MagicMock()
    mock.provider_id = "yfinance"
    mock.provider_version = "1.3.0"

    def _side_effect(symbol: str) -> MarketSnapshot:
        if symbol in failing_symbols:
            raise ProviderUnavailableError("yfinance", symbol, "unavailable")
        return _make_snapshot(symbol)

    mock.fetch_snapshot.side_effect = _side_effect
    return mock


def _make_client(*failing_symbols: str) -> TestClient:
    service = MarketSnapshotService(_make_provider(*failing_symbols))
    return TestClient(create_app(market_snapshot_service=service))


# ---------------------------------------------------------------------------
# Success: single symbol
# ---------------------------------------------------------------------------


class TestMarketContextOverlaySuccess:
    def test_returns_200_for_valid_symbol(self) -> None:
        client = _make_client()
        response = client.get("/workspaces/market-context?symbols=AAPL")
        assert response.status_code == 200

    def test_authority_is_advisory(self) -> None:
        client = _make_client()
        data = client.get("/workspaces/market-context?symbols=AAPL").json()
        assert data["authority"] == "advisory"

    def test_available_contains_snapshot(self) -> None:
        client = _make_client()
        data = client.get("/workspaces/market-context?symbols=AAPL").json()
        assert len(data["available"]) == 1
        assert data["available"][0]["symbol"] == "AAPL"

    def test_snapshot_ohlcv_present(self) -> None:
        client = _make_client()
        data = client.get("/workspaces/market-context?symbols=AAPL").json()
        snap = data["available"][0]
        assert snap["open"] == "185.00"
        assert snap["high"] == "187.50"
        assert snap["low"] == "184.20"
        assert snap["close"] == "186.40"
        assert snap["volume"] == 52_000_000

    def test_snapshot_interpretation_present(self) -> None:
        client = _make_client()
        data = client.get("/workspaces/market-context?symbols=AAPL").json()
        snap = data["available"][0]
        assert snap["interpretation_headline"]
        assert snap["interpretation_detail"]

    def test_is_complete_true_when_all_available(self) -> None:
        client = _make_client()
        data = client.get("/workspaces/market-context?symbols=AAPL").json()
        assert data["is_complete"] is True
        assert data["is_partial"] is False
        assert data["is_empty"] is False

    def test_provider_id_present(self) -> None:
        client = _make_client()
        data = client.get("/workspaces/market-context?symbols=AAPL").json()
        assert data["provider_id"] == "yfinance"

    def test_attempt_record_present(self) -> None:
        client = _make_client()
        data = client.get("/workspaces/market-context?symbols=AAPL").json()
        assert data["attempts"][0]["provider_id"] == "yfinance"
        assert data["attempts"][0]["outcome"] == "success"

    def test_symbol_is_uppercased(self) -> None:
        client = _make_client()
        data = client.get("/workspaces/market-context?symbols=aapl").json()
        assert data["available"][0]["symbol"] == "AAPL"

    def test_multi_symbol_request(self) -> None:
        client = _make_client()
        data = client.get("/workspaces/market-context?symbols=AAPL,TSLA").json()
        assert len(data["available"]) == 2
        symbols = {s["symbol"] for s in data["available"]}
        assert symbols == {"AAPL", "TSLA"}


# ---------------------------------------------------------------------------
# Partial failure
# ---------------------------------------------------------------------------


class TestMarketContextOverlayPartial:
    def test_partial_returns_200(self) -> None:
        client = _make_client("TSLA")
        response = client.get("/workspaces/market-context?symbols=AAPL,TSLA")
        assert response.status_code == 200

    def test_partial_available_contains_successful_symbol(self) -> None:
        client = _make_client("TSLA")
        data = client.get("/workspaces/market-context?symbols=AAPL,TSLA").json()
        assert len(data["available"]) == 1
        assert data["available"][0]["symbol"] == "AAPL"

    def test_partial_unavailable_symbols_recorded(self) -> None:
        client = _make_client("TSLA")
        data = client.get("/workspaces/market-context?symbols=AAPL,TSLA").json()
        assert "TSLA" in data["unavailable_symbols"]

    def test_is_partial_true(self) -> None:
        client = _make_client("TSLA")
        data = client.get("/workspaces/market-context?symbols=AAPL,TSLA").json()
        assert data["is_partial"] is True
        assert data["is_complete"] is False
        assert data["is_empty"] is False

    def test_failed_attempt_records_reason(self) -> None:
        client = _make_client("TSLA")
        data = client.get("/workspaces/market-context?symbols=AAPL,TSLA").json()
        failed = next(item for item in data["attempts"] if item["outcome"] == "failure")
        assert failed["provider_id"] == "yfinance"
        assert failed["failure_reason"] == "unavailable"


# ---------------------------------------------------------------------------
# All unavailable
# ---------------------------------------------------------------------------


class TestMarketContextOverlayEmpty:
    def test_all_unavailable_returns_200(self) -> None:
        client = _make_client("AAPL")
        response = client.get("/workspaces/market-context?symbols=AAPL")
        assert response.status_code == 200

    def test_is_empty_true_when_all_unavailable(self) -> None:
        client = _make_client("AAPL")
        data = client.get("/workspaces/market-context?symbols=AAPL").json()
        assert data["is_empty"] is True
        assert data["is_complete"] is False
        assert data["is_partial"] is False

    def test_available_is_empty_list(self) -> None:
        client = _make_client("AAPL")
        data = client.get("/workspaces/market-context?symbols=AAPL").json()
        assert data["available"] == []


# ---------------------------------------------------------------------------
# Validation failures
# ---------------------------------------------------------------------------


class TestMarketContextOverlayValidation:
    def test_whitespace_only_symbols_returns_400(self) -> None:
        client = _make_client()
        response = client.get("/workspaces/market-context?symbols=,,,")
        assert response.status_code == 400

    def test_snapshot_regime_present(self) -> None:
        client = _make_client()
        data = client.get("/workspaces/market-context?symbols=AAPL").json()
        snap = data["available"][0]
        assert "regime" in snap

    def test_snapshot_provenance_fields_present(self) -> None:
        client = _make_client()
        data = client.get("/workspaces/market-context?symbols=AAPL").json()
        snap = data["available"][0]
        assert "fetched_at" in snap
        assert "data_as_of" in snap
        assert snap["provider_id"] == "yfinance"
