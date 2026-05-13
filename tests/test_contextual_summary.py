"""
Tests for TF-0049: contextual operational summaries.

Tests cover ContextualSummaryService logic and the API endpoint via TestClient.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from src.app.api.application import create_app
from src.domain.market.provider import ProviderUnavailableError
from src.domain.market.snapshot import (
    MarketRegime,
    MarketSnapshot,
    PriceOHLCV,
    ProviderProvenance,
)
from src.infrastructure.event_store.in_memory import InMemoryEventStore
from src.services.market.contextual_summary import ContextualSummaryService
from src.services.market.snapshot_service import MarketSnapshotService

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_TS = datetime(2026, 5, 12, 20, 0, 0, tzinfo=UTC)

_WORKSPACE_PARAMS = {
    "persona_id": "swing-trader",
    "persona_version": "v1",
    "workspace_id": "primary",
}


def _make_snapshot(
    symbol: str = "AAPL", regime: MarketRegime = MarketRegime.BULL
) -> MarketSnapshot:
    from dataclasses import replace
    provenance = ProviderProvenance(
        provider_id="yfinance",
        provider_version="1.3.0",
        fetched_at=_TS,
        data_as_of=_TS,
    )
    price = PriceOHLCV(
        symbol=symbol,
        open=Decimal("100.00"),
        high=Decimal("103.00"),
        low=Decimal("99.50"),
        close=Decimal("103.00"),
        volume=1_000_000,
        as_of=_TS,
    )
    snap = MarketSnapshot(price=price, provenance=provenance)
    return replace(snap, regime=regime)


def _make_provider(*failing: str) -> MagicMock:
    mock = MagicMock()
    mock.provider_id = "yfinance"

    def _side(symbol: str) -> MarketSnapshot:
        if symbol in failing:
            raise ProviderUnavailableError("yfinance", symbol, "unavailable")
        return _make_snapshot(symbol)

    mock.fetch_snapshot.side_effect = _side
    return mock


def _make_client(
    *failing: str,
    include_market: bool = True,
) -> TestClient:
    event_store = InMemoryEventStore()
    market_svc = (
        MarketSnapshotService(_make_provider(*failing)) if include_market else None
    )
    svc = ContextualSummaryService(event_store, market_svc)
    return TestClient(create_app(contextual_summary_service=svc))


# ---------------------------------------------------------------------------
# Endpoint: workspace-only (no symbols)
# ---------------------------------------------------------------------------


class TestContextualSummaryNoMarket:
    def test_returns_200(self) -> None:
        client = _make_client()
        resp = client.get("/workspaces/contextual-summary", params=_WORKSPACE_PARAMS)
        assert resp.status_code == 200

    def test_authority_is_derived(self) -> None:
        client = _make_client()
        data = client.get(
            "/workspaces/contextual-summary", params=_WORKSPACE_PARAMS
        ).json()
        assert data["authority"] == "derived"

    def test_no_market_notes_when_no_symbols(self) -> None:
        client = _make_client()
        data = client.get(
            "/workspaces/contextual-summary", params=_WORKSPACE_PARAMS
        ).json()
        assert data["market_context_notes"] == []
        assert data["market_context_available"] is False

    def test_operational_headline_present(self) -> None:
        client = _make_client()
        data = client.get(
            "/workspaces/contextual-summary", params=_WORKSPACE_PARAMS
        ).json()
        assert isinstance(data["operational_headline"], str)
        assert len(data["operational_headline"]) > 0

    def test_source_inputs_includes_workspace_summaries(self) -> None:
        client = _make_client()
        data = client.get(
            "/workspaces/contextual-summary", params=_WORKSPACE_PARAMS
        ).json()
        assert "workspace_summaries" in data["source_inputs"]

    def test_authority_boundaries_present(self) -> None:
        client = _make_client()
        data = client.get(
            "/workspaces/contextual-summary", params=_WORKSPACE_PARAMS
        ).json()
        assert len(data["authority_boundaries"]) > 0


# ---------------------------------------------------------------------------
# Endpoint: with market context
# ---------------------------------------------------------------------------


class TestContextualSummaryWithMarket:
    def test_market_note_present_when_symbol_provided(self) -> None:
        client = _make_client()
        params = {**_WORKSPACE_PARAMS, "symbols": "AAPL"}
        data = client.get("/workspaces/contextual-summary", params=params).json()
        assert data["market_context_available"] is True
        assert len(data["market_context_notes"]) == 1
        assert data["market_context_notes"][0]["symbol"] == "AAPL"

    def test_market_note_contains_close_price(self) -> None:
        client = _make_client()
        params = {**_WORKSPACE_PARAMS, "symbols": "AAPL"}
        note = client.get(
            "/workspaces/contextual-summary", params=params
        ).json()["market_context_notes"][0]
        assert "close" in note
        assert isinstance(note["close"], str)

    def test_market_note_contains_regime(self) -> None:
        client = _make_client()
        params = {**_WORKSPACE_PARAMS, "symbols": "AAPL"}
        note = client.get(
            "/workspaces/contextual-summary", params=params
        ).json()["market_context_notes"][0]
        assert "regime" in note
        assert isinstance(note["regime"], str)

    def test_market_note_is_advisory(self) -> None:
        client = _make_client()
        params = {**_WORKSPACE_PARAMS, "symbols": "AAPL"}
        note = client.get(
            "/workspaces/contextual-summary", params=params
        ).json()["market_context_notes"][0]
        assert note["is_advisory"] is True

    def test_source_inputs_includes_market_context(self) -> None:
        client = _make_client()
        params = {**_WORKSPACE_PARAMS, "symbols": "AAPL"}
        data = client.get("/workspaces/contextual-summary", params=params).json()
        assert "market_context" in data["source_inputs"]

    def test_multi_symbol_request(self) -> None:
        client = _make_client()
        params = {**_WORKSPACE_PARAMS, "symbols": "AAPL,TSLA"}
        data = client.get("/workspaces/contextual-summary", params=params).json()
        assert len(data["market_context_notes"]) == 2

    def test_symbol_uppercased(self) -> None:
        client = _make_client()
        params = {**_WORKSPACE_PARAMS, "symbols": "aapl"}
        note = client.get(
            "/workspaces/contextual-summary", params=params
        ).json()["market_context_notes"][0]
        assert note["symbol"] == "AAPL"

    def test_unavailable_symbol_omitted_from_notes(self) -> None:
        client = _make_client("TSLA")
        params = {**_WORKSPACE_PARAMS, "symbols": "AAPL,TSLA"}
        data = client.get("/workspaces/contextual-summary", params=params).json()
        symbols = {n["symbol"] for n in data["market_context_notes"]}
        assert "AAPL" in symbols
        assert "TSLA" not in symbols

    def test_all_unavailable_leaves_no_market_notes(self) -> None:
        client = _make_client("AAPL")
        params = {**_WORKSPACE_PARAMS, "symbols": "AAPL"}
        data = client.get("/workspaces/contextual-summary", params=params).json()
        assert data["market_context_available"] is False
        assert data["market_context_notes"] == []

    def test_persona_id_in_response(self) -> None:
        client = _make_client()
        data = client.get(
            "/workspaces/contextual-summary", params=_WORKSPACE_PARAMS
        ).json()
        assert data["persona_id"] == "swing-trader"

    def test_workspace_id_in_response(self) -> None:
        client = _make_client()
        data = client.get(
            "/workspaces/contextual-summary", params=_WORKSPACE_PARAMS
        ).json()
        assert data["workspace_id"] == "primary"
