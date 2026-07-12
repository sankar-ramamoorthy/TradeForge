from __future__ import annotations

from datetime import UTC, datetime

from src.domain.events import EntityReference, EventEnvelope
from src.infrastructure.event_store.in_memory import InMemoryEventStore
from src.infrastructure.market.in_memory_snapshot_store import (
    InMemoryMarketSnapshotStore,
)
from src.infrastructure.market.seeded_provider import SeededMarketDataProvider
from src.services.evidence import (
    EvidenceEligibilityService,
    EvidencePanelService,
    EvidenceRankingService,
    EvidenceRefreshService,
    WatchlistService,
)
from src.services.market.regime_interpreter import SingleBarRegimeInterpreter
from src.services.market.snapshot_query import MarketSnapshotQueryService
from src.services.market.snapshot_service import MarketSnapshotService


def _trade_idea(symbol: str = "AAPL") -> EventEnvelope:
    return EventEnvelope(
        event_type="decision.trade_idea_created",
        timestamp=datetime(2026, 7, 12, 13, 0, tzinfo=UTC),
        persona_id="operator",
        workspace_id="operating",
        entity_references=(
            EntityReference("decision", "decision-1"),
            EntityReference("ticker", symbol),
        ),
        payload={"decision_id": "decision-1", "symbol": symbol},
    )


def _services() -> tuple[
    InMemoryEventStore,
    WatchlistService,
    EvidenceEligibilityService,
    EvidenceRefreshService,
    EvidenceRankingService,
    EvidencePanelService,
]:
    event_store = InMemoryEventStore()
    snapshot_store = InMemoryMarketSnapshotStore()
    query_service = MarketSnapshotQueryService(snapshot_store)
    snapshot_service = MarketSnapshotService(
        SeededMarketDataProvider(
            fetched_at=datetime(2026, 7, 12, 13, 5, tzinfo=UTC),
        ),
        SingleBarRegimeInterpreter(),
        snapshot_persistence_store=snapshot_store,
    )
    watchlist = WatchlistService(event_store)
    eligibility = EvidenceEligibilityService(event_store, watchlist)
    refresh = EvidenceRefreshService(eligibility, snapshot_service)
    ranking = EvidenceRankingService(eligibility, query_service)
    panel = EvidencePanelService(ranking, query_service)
    return event_store, watchlist, eligibility, refresh, ranking, panel


def test_watchlist_entries_are_market_events_not_lifecycle_events() -> None:
    event_store, watchlist, *_ = _services()

    entry = watchlist.add_entry(
        symbol="tsla",
        rationale="Volatility setup needs monitoring",
        persona_id="operator",
        workspace_id="operating",
        pinned=True,
        timestamp=datetime(2026, 7, 12, 13, 0, tzinfo=UTC),
    )

    events = event_store.read_events()
    assert entry.symbol == "TSLA"
    assert [event.event_type for event in events] == ["market.watchlist_entry_added"]
    assert all(
        event.event_type not in {"decision.trade_idea_created"} for event in events
    )


def test_refresh_uses_active_decisions_and_watchlist_without_lifecycle_writes() -> None:
    event_store, watchlist, eligibility, refresh, *_ = _services()
    event_store.append(_trade_idea("AAPL"))
    watchlist.add_entry(
        symbol="TSLA",
        rationale="High volume gap risk",
        persona_id="operator",
        workspace_id="operating",
        pinned=True,
    )

    eligible = eligibility.list_eligible()
    result = refresh.refresh_once()

    assert [item.symbol for item in eligible] == ["AAPL", "TSLA"]
    assert result.eligible_symbols == ("AAPL", "TSLA")
    assert result.refreshed_symbols == ("AAPL", "TSLA")
    assert result.unavailable_symbols == ()
    assert [event.event_type for event in event_store.read_events()] == [
        "decision.trade_idea_created",
        "market.watchlist_entry_added",
    ]


def test_ranking_is_deterministic_and_exposes_reason_codes() -> None:
    event_store, watchlist, _, refresh, ranking, _ = _services()
    event_store.append(_trade_idea("AAPL"))
    watchlist.add_entry(
        symbol="TSLA",
        rationale="Volatility setup needs monitoring",
        persona_id="operator",
        workspace_id="operating",
        pinned=True,
    )
    refresh.refresh_once()

    result = ranking.rank(now=datetime(2026, 7, 12, 14, 0, tzinfo=UTC))

    assert result.is_advisory
    assert [item.symbol for item in result.items] == ["TSLA", "AAPL"]
    assert result.items[0].rank == 1
    assert {reason.code for reason in result.items[0].reasons} >= {
        "operator-pinned-priority",
        "watchlist-monitoring",
        "meaningful-price-change",
        "unusual-volume",
    }


def test_evidence_panel_returns_facts_and_chart_points_from_snapshot_archive() -> None:
    event_store, _, _, refresh, _, panel = _services()
    event_store.append(_trade_idea("AAPL"))
    refresh.refresh_once()

    result = panel.panel_for_symbol(
        "aapl",
        now=datetime(2026, 7, 12, 14, 0, tzinfo=UTC),
    )

    assert result.symbol == "AAPL"
    assert result.is_advisory
    assert result.latest_snapshot is not None
    assert [fact.key for fact in result.facts] == [
        "latest-price",
        "open-to-close-change",
        "volume",
        "market-regime",
    ]
    assert len(result.chart_points) == 1
    assert result.chart_points[0].provider_id == "seeded-demo"
