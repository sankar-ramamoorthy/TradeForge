from __future__ import annotations

from datetime import UTC, datetime

from fastapi.testclient import TestClient
from src.app.api import create_app
from src.infrastructure.event_store.in_memory import InMemoryEventStore
from src.infrastructure.market.in_memory_snapshot_store import (
    InMemoryMarketSnapshotStore,
)
from src.infrastructure.market.seeded_provider import SeededMarketDataProvider
from src.services.market.regime_interpreter import SingleBarRegimeInterpreter
from src.services.market.snapshot_query import MarketSnapshotQueryService
from src.services.market.snapshot_service import MarketSnapshotService


def _client() -> TestClient:
    snapshot_store = InMemoryMarketSnapshotStore()
    snapshot_service = MarketSnapshotService(
        SeededMarketDataProvider(
            fetched_at=datetime(2026, 7, 12, 13, 5, tzinfo=UTC),
        ),
        SingleBarRegimeInterpreter(),
        snapshot_persistence_store=snapshot_store,
    )
    app = create_app(
        event_store=InMemoryEventStore(),
        market_snapshot_service=snapshot_service,
        market_snapshot_query_service=MarketSnapshotQueryService(snapshot_store),
    )
    return TestClient(app)


def test_evidence_api_watchlist_refresh_ranking_and_panel_flow() -> None:
    client = _client()

    created = client.post(
        "/evidence/watchlist",
        json={
            "symbol": "TSLA",
            "rationale": "Monitor volatility setup",
            "persona_id": "operator",
            "workspace_id": "operating",
            "pinned": True,
        },
    )
    assert created.status_code == 201
    assert created.json()["symbol"] == "TSLA"

    watchlist = client.get("/evidence/watchlist").json()
    assert watchlist["authority"] == "canonical-event-derived"
    assert watchlist["entries"][0]["pinned"] is True

    refresh = client.post("/evidence/refresh/run")
    assert refresh.status_code == 200
    refresh_body = refresh.json()
    assert refresh_body["refreshed_symbols"] == ["TSLA"]
    assert refresh_body["coverage"][0]["symbol"] == "TSLA"
    assert refresh_body["coverage"][0]["attempts"][0]["provider_id"] == "seeded-demo"
    assert refresh_body["coverage_summary"]["attempted_count"] == 1

    ranking = client.get("/evidence/ranking").json()
    assert ranking["authority"] == "advisory"
    assert ranking["coverage_summary"]["attempted_count"] == 1
    assert ranking["items"][0]["reasons"][0]["code"] == "operator-pinned-priority"
    assert ranking["items"][0]["coverage"]["provider_ids"] == ["seeded-demo"]

    panel = client.get("/evidence/symbols/tsla").json()
    assert panel["symbol"] == "TSLA"
    assert panel["coverage"]["provider_ids"] == ["seeded-demo"]
    assert panel["latest_snapshot"]["provider_id"] == "seeded-demo"
    assert panel["chart_points"]


def test_evidence_api_reports_partial_refresh_coverage() -> None:
    client = _client()
    client.post(
        "/evidence/watchlist",
        json={
            "symbol": "BADTICKER",
            "rationale": "Monitor provider failure clarity",
            "persona_id": "operator",
            "workspace_id": "operating",
        },
    )

    refresh = client.post("/evidence/refresh/run").json()

    assert refresh["refreshed_symbols"] == []
    assert refresh["unavailable_symbols"] == ["BADTICKER"]
    assert refresh["coverage_summary"]["is_partial"] is True
    assert refresh["coverage"][0]["status"] == "provider-degraded"
    assert refresh["coverage"][0]["missing_fields"] == [
        "latest-price",
        "open-to-close-change",
        "volume",
        "market-regime",
        "chart-points",
    ]
    assert refresh["coverage"][0]["attempts"][0]["failure_reason"]
