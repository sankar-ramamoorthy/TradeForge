"""
Tests for TF-0052: replay-compatible market snapshot persistence strategy.

Validates:
- PersistedMarketSnapshot domain model
- InMemoryMarketSnapshotStore append/query behavior
- MarketSnapshotService integration with optional snapshot_persistence_store
- MarketSnapshotQueryService query logic
- PostgresMarketSnapshotStore interface shape and migration structure
- GET /market/snapshots API endpoint
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from src.app.api.application import create_app
from src.domain.market.provider import ProviderUnavailableError
from src.domain.market.snapshot import (
    MarketRegime,
    MarketSnapshot,
    PriceOHLCV,
    ProviderProvenance,
)
from src.domain.market.snapshot_persistence import (
    MarketSnapshotPersistenceStore,
    PersistedMarketSnapshot,
)
from src.infrastructure.market.in_memory_snapshot_store import (
    InMemoryMarketSnapshotStore,
)
from src.infrastructure.market.postgres_snapshot_store import (
    PostgresMarketSnapshotStore,
    _sqlalchemy_url,
)
from src.services.market.context import MarketContextRequest
from src.services.market.snapshot_query import (
    MarketSnapshotQueryAuthority,
    MarketSnapshotQueryService,
)
from src.services.market.snapshot_service import MarketSnapshotService

_NOW = datetime(2026, 5, 13, 9, 30, 0, tzinfo=UTC)
_CLOSE = datetime(2026, 5, 12, 16, 0, 0, tzinfo=UTC)


def _make_snapshot(
    symbol: str = "AAPL",
    regime: MarketRegime = MarketRegime.BULL,
) -> MarketSnapshot:
    return MarketSnapshot(
        price=PriceOHLCV(
            symbol=symbol,
            open=Decimal("180.00"),
            high=Decimal("185.00"),
            low=Decimal("179.00"),
            close=Decimal("183.00"),
            volume=5_000_000,
            as_of=_CLOSE,
        ),
        provenance=ProviderProvenance(
            provider_id="stub",
            provider_version="1.0.0",
            fetched_at=_NOW,
            data_as_of=_CLOSE,
        ),
        regime=regime,
    )


def _make_provider(
    symbol: str = "AAPL",
    raises: bool = False,
) -> MagicMock:
    provider = MagicMock()
    provider.provider_id = "stub"
    provider.provider_version = "1.0.0"
    if raises:
        provider.fetch_snapshot.side_effect = ProviderUnavailableError(
            "stub", symbol, "unavailable"
        )
    else:
        provider.fetch_snapshot.return_value = _make_snapshot(symbol)
    return provider


# ---------------------------------------------------------------------------
# PersistedMarketSnapshot tests
# ---------------------------------------------------------------------------


class TestPersistedMarketSnapshot:
    def test_is_advisory_always_true(self) -> None:
        record = PersistedMarketSnapshot(
            snapshot_id=1,
            snapshot=_make_snapshot(),
            persisted_at=_NOW,
        )
        assert record.is_advisory is True

    def test_symbol_delegates_to_snapshot(self) -> None:
        record = PersistedMarketSnapshot(
            snapshot_id=1,
            snapshot=_make_snapshot("TSLA"),
            persisted_at=_NOW,
        )
        assert record.symbol == "TSLA"

    def test_provider_id_delegates_to_snapshot(self) -> None:
        record = PersistedMarketSnapshot(
            snapshot_id=1,
            snapshot=_make_snapshot(),
            persisted_at=_NOW,
        )
        assert record.provider_id == "stub"

    def test_record_is_immutable(self) -> None:
        record = PersistedMarketSnapshot(
            snapshot_id=1,
            snapshot=_make_snapshot(),
            persisted_at=_NOW,
        )
        with pytest.raises((AttributeError, TypeError)):
            record.snapshot_id = 99  # type: ignore[misc]


# ---------------------------------------------------------------------------
# InMemoryMarketSnapshotStore tests
# ---------------------------------------------------------------------------


class TestInMemoryMarketSnapshotStore:
    def test_empty_store_returns_empty_tuple(self) -> None:
        store = InMemoryMarketSnapshotStore()
        assert store.get_snapshots() == ()

    def test_persisted_snapshot_returned(self) -> None:
        store = InMemoryMarketSnapshotStore()
        store.persist(_make_snapshot("AAPL"))
        records = store.get_snapshots()
        assert len(records) == 1
        assert records[0].symbol == "AAPL"

    def test_snapshot_ids_are_sequential(self) -> None:
        store = InMemoryMarketSnapshotStore()
        store.persist(_make_snapshot("AAPL"))
        store.persist(_make_snapshot("TSLA"))
        records = store.get_snapshots()
        assert records[0].snapshot_id == 1
        assert records[1].snapshot_id == 2

    def test_persisted_at_set_on_write(self) -> None:
        before = datetime.now(UTC)
        store = InMemoryMarketSnapshotStore()
        store.persist(_make_snapshot())
        after = datetime.now(UTC)
        record = store.get_snapshots()[0]
        assert before <= record.persisted_at <= after

    def test_filter_by_symbol(self) -> None:
        store = InMemoryMarketSnapshotStore()
        store.persist(_make_snapshot("AAPL"))
        store.persist(_make_snapshot("TSLA"))
        records = store.get_snapshots(symbol="TSLA")
        assert len(records) == 1
        assert records[0].symbol == "TSLA"

    def test_filter_by_provider_id(self) -> None:
        store = InMemoryMarketSnapshotStore()
        store.persist(_make_snapshot("AAPL"))
        records = store.get_snapshots(provider_id="stub")
        assert len(records) == 1
        records_other = store.get_snapshots(provider_id="other")
        assert len(records_other) == 0

    def test_filter_by_since(self) -> None:
        store = InMemoryMarketSnapshotStore()
        store.persist(_make_snapshot("AAPL"))
        future = datetime.now(UTC) + timedelta(hours=1)
        records = store.get_snapshots(since=future)
        assert len(records) == 0

    def test_filter_by_until(self) -> None:
        store = InMemoryMarketSnapshotStore()
        store.persist(_make_snapshot("AAPL"))
        past = datetime.now(UTC) - timedelta(hours=1)
        records = store.get_snapshots(until=past)
        assert len(records) == 0

    def test_ordered_by_persisted_at(self) -> None:
        store = InMemoryMarketSnapshotStore()
        store.persist(_make_snapshot("AAPL"))
        store.persist(_make_snapshot("TSLA"))
        records = store.get_snapshots()
        assert records[0].persisted_at <= records[1].persisted_at

    def test_returns_tuple(self) -> None:
        store = InMemoryMarketSnapshotStore()
        store.persist(_make_snapshot())
        assert isinstance(store.get_snapshots(), tuple)

    def test_snapshot_data_preserved(self) -> None:
        snap = _make_snapshot("NVDA")
        store = InMemoryMarketSnapshotStore()
        store.persist(snap)
        record = store.get_snapshots()[0]
        assert record.snapshot.price.close == Decimal("183.00")
        assert record.snapshot.provenance.provider_id == "stub"

    def test_satisfies_protocol(self) -> None:
        store: MarketSnapshotPersistenceStore = InMemoryMarketSnapshotStore()
        store.persist(_make_snapshot())
        records = store.get_snapshots()
        assert len(records) == 1


# ---------------------------------------------------------------------------
# MarketSnapshotService integration with persistence store
# ---------------------------------------------------------------------------


class TestMarketSnapshotServicePersistenceIntegration:
    def test_fetch_context_persists_successful_snapshots(self) -> None:
        store = InMemoryMarketSnapshotStore()
        provider = _make_provider("AAPL")
        svc = MarketSnapshotService(provider, snapshot_persistence_store=store)
        svc.fetch_context(MarketContextRequest(symbols=("AAPL",)))
        records = store.get_snapshots()
        assert len(records) == 1
        assert records[0].symbol == "AAPL"

    def test_fetch_context_does_not_persist_failures(self) -> None:
        store = InMemoryMarketSnapshotStore()
        provider = _make_provider("AAPL", raises=True)
        svc = MarketSnapshotService(provider, snapshot_persistence_store=store)
        svc.fetch_context(MarketContextRequest(symbols=("AAPL",)))
        assert store.get_snapshots() == ()

    def test_fetch_context_persists_partial_success(self) -> None:
        store = InMemoryMarketSnapshotStore()
        provider = MagicMock()
        provider.provider_id = "stub"
        provider.provider_version = "1.0.0"

        def side_effect(symbol: str) -> MarketSnapshot:
            if symbol == "AAPL":
                return _make_snapshot("AAPL")
            raise ProviderUnavailableError("stub", symbol, "unavailable")

        provider.fetch_snapshot.side_effect = side_effect
        svc = MarketSnapshotService(provider, snapshot_persistence_store=store)
        svc.fetch_context(MarketContextRequest(symbols=("AAPL", "FAKE")))
        records = store.get_snapshots()
        assert len(records) == 1
        assert records[0].symbol == "AAPL"

    def test_fetch_snapshot_persists_success(self) -> None:
        store = InMemoryMarketSnapshotStore()
        provider = _make_provider("TSLA")
        svc = MarketSnapshotService(provider, snapshot_persistence_store=store)
        svc.fetch_snapshot("TSLA")
        records = store.get_snapshots()
        assert len(records) == 1
        assert records[0].symbol == "TSLA"

    def test_fetch_snapshot_does_not_persist_on_failure(self) -> None:
        store = InMemoryMarketSnapshotStore()
        provider = _make_provider("AAPL", raises=True)
        svc = MarketSnapshotService(provider, snapshot_persistence_store=store)
        with pytest.raises(ProviderUnavailableError):
            svc.fetch_snapshot("AAPL")
        assert store.get_snapshots() == ()

    def test_no_persistence_store_leaves_behavior_unchanged(self) -> None:
        provider = _make_provider("AAPL")
        svc = MarketSnapshotService(provider)
        result = svc.fetch_context(MarketContextRequest(symbols=("AAPL",)))
        assert result.is_complete

    def test_persistence_store_failure_does_not_break_fetch(self) -> None:
        broken_store = MagicMock()
        broken_store.persist.side_effect = RuntimeError("storage unavailable")
        provider = _make_provider("AAPL")
        svc = MarketSnapshotService(provider, snapshot_persistence_store=broken_store)
        result = svc.fetch_context(MarketContextRequest(symbols=("AAPL",)))
        assert result.is_complete

    def test_regime_is_preserved_in_persistence(self) -> None:
        from src.services.market.regime_interpreter import SingleBarRegimeInterpreter

        store = InMemoryMarketSnapshotStore()
        from src.infrastructure.market.seeded_provider import SeededMarketDataProvider

        provider = SeededMarketDataProvider()
        svc = MarketSnapshotService(
            provider, SingleBarRegimeInterpreter(), snapshot_persistence_store=store
        )
        svc.fetch_snapshot("TSLA")
        record = store.get_snapshots()[0]
        assert record.snapshot.regime == MarketRegime.HIGH_VOLATILITY


# ---------------------------------------------------------------------------
# MarketSnapshotQueryService tests
# ---------------------------------------------------------------------------


class TestMarketSnapshotQueryService:
    def _store_with_snapshots(self) -> InMemoryMarketSnapshotStore:
        store = InMemoryMarketSnapshotStore()
        store.persist(_make_snapshot("AAPL"))
        store.persist(_make_snapshot("TSLA"))
        store.persist(_make_snapshot("NVDA"))
        return store

    def test_query_all_returns_all(self) -> None:
        svc = MarketSnapshotQueryService(self._store_with_snapshots())
        result = svc.query()
        assert result.total_count == 3

    def test_query_authority_is_advisory(self) -> None:
        svc = MarketSnapshotQueryService(self._store_with_snapshots())
        result = svc.query()
        assert result.authority == MarketSnapshotQueryAuthority.ADVISORY
        assert result.is_advisory

    def test_query_with_symbol_filter(self) -> None:
        svc = MarketSnapshotQueryService(self._store_with_snapshots())
        result = svc.query(symbol="AAPL")
        assert result.total_count == 1
        assert result.snapshots[0].symbol == "AAPL"

    def test_query_empty_store(self) -> None:
        svc = MarketSnapshotQueryService(InMemoryMarketSnapshotStore())
        result = svc.query()
        assert result.total_count == 0
        assert result.snapshots == ()

    def test_query_result_is_immutable(self) -> None:
        svc = MarketSnapshotQueryService(self._store_with_snapshots())
        result = svc.query()
        assert isinstance(result.snapshots, tuple)


# ---------------------------------------------------------------------------
# PostgresMarketSnapshotStore interface and migration tests
# ---------------------------------------------------------------------------


class TestPostgresMarketSnapshotStore:
    def test_satisfies_persistence_store_shape(self) -> None:
        store = PostgresMarketSnapshotStore(
            database_url="postgresql://example/test"
        )
        assert hasattr(store, "persist")
        assert hasattr(store, "get_snapshots")

    def test_does_not_expose_mutation_operations(self) -> None:
        store = PostgresMarketSnapshotStore(
            database_url="postgresql://example/test"
        )
        assert not hasattr(store, "delete")
        assert not hasattr(store, "update")
        assert not hasattr(store, "truncate")

    def test_sqlalchemy_url_converts_postgresql_prefix(self) -> None:
        assert _sqlalchemy_url("postgresql://user/db") == (
            "postgresql+psycopg://user/db"
        )

    def test_sqlalchemy_url_leaves_other_prefixes_unchanged(self) -> None:
        assert _sqlalchemy_url("sqlite:///db") == "sqlite:///db"

    def test_migration_creates_advisory_table(self) -> None:
        migration_path = (
            "migrations/versions/20260513_0003_create_market_snapshots.py"
        )
        with open(migration_path, encoding="utf-8") as f:
            text = f.read()
        assert "market_advisory_snapshots" in text
        assert "snapshot_id" in text
        assert "provider_id" in text
        assert "fetched_at" in text
        assert "data_as_of" in text
        assert "open_price" in text
        assert "close_price" in text
        assert "regime" in text
        assert "persisted_at" in text
        assert "advisory" in text.lower()

    def test_migration_creates_replay_indices(self) -> None:
        migration_path = (
            "migrations/versions/20260513_0003_create_market_snapshots.py"
        )
        with open(migration_path, encoding="utf-8") as f:
            text = f.read()
        assert "ix_market_advisory_snapshots_symbol_fetched" in text
        assert "ix_market_advisory_snapshots_provider_fetched" in text

    def test_migration_has_downgrade(self) -> None:
        migration_path = (
            "migrations/versions/20260513_0003_create_market_snapshots.py"
        )
        with open(migration_path, encoding="utf-8") as f:
            text = f.read()
        assert "def downgrade" in text
        assert "drop_table" in text

    def test_migration_chains_from_event_ledger(self) -> None:
        migration_path = (
            "migrations/versions/20260513_0003_create_market_snapshots.py"
        )
        with open(migration_path, encoding="utf-8") as f:
            text = f.read()
        assert "20260511_0002" in text


# ---------------------------------------------------------------------------
# GET /market/snapshots API endpoint tests
# ---------------------------------------------------------------------------


class TestMarketSnapshotsEndpoint:
    def _app_with_store(
        self,
    ) -> tuple[TestClient, InMemoryMarketSnapshotStore]:
        snapshot_store = InMemoryMarketSnapshotStore()
        query_svc = MarketSnapshotQueryService(snapshot_store)
        app = create_app(market_snapshot_query_service=query_svc)
        return TestClient(app), snapshot_store

    def test_empty_store_returns_empty_response(self) -> None:
        client, _ = self._app_with_store()
        resp = client.get("/market/snapshots")
        assert resp.status_code == 200
        data = resp.json()
        assert data["authority"] == "advisory"
        assert data["total_count"] == 0
        assert data["snapshots"] == []

    def test_persisted_snapshot_appears_in_response(self) -> None:
        client, store = self._app_with_store()
        store.persist(_make_snapshot("AAPL"))
        resp = client.get("/market/snapshots")
        data = resp.json()
        assert data["total_count"] == 1
        snap = data["snapshots"][0]
        assert snap["symbol"] == "AAPL"
        assert snap["is_advisory"] is True
        assert snap["close"] == "183.00"
        assert snap["regime"] == "bull"

    def test_filter_by_symbol(self) -> None:
        client, store = self._app_with_store()
        store.persist(_make_snapshot("AAPL"))
        store.persist(_make_snapshot("TSLA"))
        resp = client.get("/market/snapshots?symbol=AAPL")
        data = resp.json()
        assert data["total_count"] == 1
        assert data["snapshots"][0]["symbol"] == "AAPL"

    def test_filter_by_provider_id(self) -> None:
        client, store = self._app_with_store()
        store.persist(_make_snapshot("AAPL"))
        resp = client.get("/market/snapshots?provider_id=stub")
        data = resp.json()
        assert data["total_count"] == 1

    def test_provider_id_filter_no_match(self) -> None:
        client, store = self._app_with_store()
        store.persist(_make_snapshot("AAPL"))
        resp = client.get("/market/snapshots?provider_id=other")
        data = resp.json()
        assert data["total_count"] == 0

    def test_snapshot_contains_all_required_fields(self) -> None:
        client, store = self._app_with_store()
        store.persist(_make_snapshot("SPY"))
        resp = client.get("/market/snapshots")
        snap = resp.json()["snapshots"][0]
        required = {
            "snapshot_id", "provider_id", "provider_version", "symbol",
            "fetched_at", "data_as_of", "open", "high", "low", "close",
            "volume", "regime", "persisted_at", "is_advisory",
        }
        assert required.issubset(snap.keys())

    def test_default_app_has_market_snapshots_endpoint(self) -> None:
        default_app = create_app()
        client = TestClient(default_app)
        resp = client.get("/market/snapshots")
        assert resp.status_code == 200

    def test_fetching_via_market_service_populates_endpoint(self) -> None:
        from src.infrastructure.market.seeded_provider import SeededMarketDataProvider

        snapshot_store = InMemoryMarketSnapshotStore()
        query_svc = MarketSnapshotQueryService(snapshot_store)
        provider = SeededMarketDataProvider()
        svc = MarketSnapshotService(
            provider, snapshot_persistence_store=snapshot_store
        )
        app = create_app(
            market_snapshot_service=svc,
            market_snapshot_query_service=query_svc,
        )
        client = TestClient(app)
        client.get("/workspaces/market-context?symbols=AAPL,SPY")
        resp = client.get("/market/snapshots")
        data = resp.json()
        assert data["total_count"] == 2
        symbols = {s["symbol"] for s in data["snapshots"]}
        assert symbols == {"AAPL", "SPY"}
