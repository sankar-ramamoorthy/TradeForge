"""
Tests for TF-0050: provider provenance tracking.

Validates:
- ProviderFetchRecord domain model and factory methods
- InMemoryProvenanceStore append and query behavior
- MarketSnapshotService integration with optional provenance_store
- ProvenanceQueryService query and summary logic
- GET /provenance/market-data API endpoint
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from src.app.api.application import create_app
from src.domain.market.provenance import ProvenanceStore, ProviderFetchRecord
from src.domain.market.provider import ProviderUnavailableError
from src.domain.market.snapshot import (
    MarketRegime,
    MarketSnapshot,
    PriceOHLCV,
    ProviderProvenance,
)
from src.infrastructure.market.in_memory_provenance_store import InMemoryProvenanceStore
from src.services.market.context import MarketContextRequest
from src.services.market.provenance_query import (
    ProvenanceQueryAuthority,
    ProvenanceQueryService,
)
from src.services.market.snapshot_service import MarketSnapshotService

# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

_NOW = datetime(2026, 5, 13, 9, 30, 0, tzinfo=UTC)
_CLOSE = datetime(2026, 5, 12, 16, 0, 0, tzinfo=UTC)


def _make_snapshot(symbol: str = "AAPL") -> MarketSnapshot:
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
        regime=MarketRegime.BULL,
    )


def _make_provider(
    provider_id: str = "stub",
    snapshot: MarketSnapshot | None = None,
    raises: bool = False,
) -> MagicMock:
    provider = MagicMock()
    provider.provider_id = provider_id
    provider.provider_version = "1.0.0"
    if raises:
        provider.fetch_snapshot.side_effect = ProviderUnavailableError(
            provider_id, "AAPL", "network error"
        )
    else:
        provider.fetch_snapshot.return_value = snapshot or _make_snapshot()
    return provider


# ---------------------------------------------------------------------------
# ProviderFetchRecord tests
# ---------------------------------------------------------------------------


class TestProviderFetchRecord:
    def test_for_success_creates_valid_record(self) -> None:
        record = ProviderFetchRecord.for_success(
            provider_id="yfinance",
            provider_version="0.2.37",
            symbol="AAPL",
            fetched_at=_NOW,
            data_as_of=_CLOSE,
        )
        assert record.provider_id == "yfinance"
        assert record.symbol == "AAPL"
        assert record.outcome == "success"
        assert record.data_as_of == _CLOSE
        assert record.error_reason is None
        assert record.is_success
        assert not record.is_failure
        assert record.is_advisory

    def test_for_failure_creates_valid_record(self) -> None:
        record = ProviderFetchRecord.for_failure(
            provider_id="alpaca",
            provider_version="0.43.0",
            symbol="TSLA",
            fetched_at=_NOW,
            error_reason="rate limit exceeded",
        )
        assert record.outcome == "failure"
        assert record.error_reason == "rate limit exceeded"
        assert record.data_as_of is None
        assert record.is_failure
        assert not record.is_success
        assert record.is_advisory

    def test_success_record_requires_data_as_of(self) -> None:
        with pytest.raises(ValueError, match="data_as_of"):
            ProviderFetchRecord(
                provider_id="stub",
                provider_version="1.0",
                symbol="AAPL",
                fetched_at=_NOW,
                outcome="success",
                data_as_of=None,
            )

    def test_failure_record_requires_error_reason(self) -> None:
        with pytest.raises(ValueError, match="error_reason"):
            ProviderFetchRecord(
                provider_id="stub",
                provider_version="1.0",
                symbol="AAPL",
                fetched_at=_NOW,
                outcome="failure",
                error_reason=None,
            )

    def test_empty_provider_id_rejected(self) -> None:
        with pytest.raises(ValueError, match="provider_id"):
            ProviderFetchRecord.for_success(
                provider_id="  ",
                provider_version="1.0",
                symbol="AAPL",
                fetched_at=_NOW,
                data_as_of=_CLOSE,
            )

    def test_empty_symbol_rejected(self) -> None:
        with pytest.raises(ValueError, match="symbol"):
            ProviderFetchRecord.for_success(
                provider_id="stub",
                provider_version="1.0",
                symbol="",
                fetched_at=_NOW,
                data_as_of=_CLOSE,
            )

    def test_record_is_immutable(self) -> None:
        record = ProviderFetchRecord.for_success(
            provider_id="stub",
            provider_version="1.0",
            symbol="AAPL",
            fetched_at=_NOW,
            data_as_of=_CLOSE,
        )
        with pytest.raises((AttributeError, TypeError)):
            record.provider_id = "changed"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# InMemoryProvenanceStore tests
# ---------------------------------------------------------------------------


class TestInMemoryProvenanceStore:
    def _success(
        self, symbol: str = "AAPL", fetched_at: datetime = _NOW
    ) -> ProviderFetchRecord:
        return ProviderFetchRecord.for_success(
            provider_id="stub",
            provider_version="1.0",
            symbol=symbol,
            fetched_at=fetched_at,
            data_as_of=_CLOSE,
        )

    def _failure(
        self, symbol: str = "NVDA", fetched_at: datetime = _NOW
    ) -> ProviderFetchRecord:
        return ProviderFetchRecord.for_failure(
            provider_id="stub",
            provider_version="1.0",
            symbol=symbol,
            fetched_at=fetched_at,
            error_reason="unavailable",
        )

    def test_empty_store_returns_empty_tuple(self) -> None:
        store = InMemoryProvenanceStore()
        assert store.get_records() == ()

    def test_appended_records_are_returned(self) -> None:
        store = InMemoryProvenanceStore()
        r1 = self._success("AAPL")
        r2 = self._failure("NVDA")
        store.record_fetch(r1)
        store.record_fetch(r2)
        records = store.get_records()
        assert len(records) == 2
        assert r1 in records
        assert r2 in records

    def test_records_ordered_by_fetched_at(self) -> None:
        store = InMemoryProvenanceStore()
        t1 = datetime(2026, 5, 13, 9, 0, tzinfo=UTC)
        t2 = datetime(2026, 5, 13, 9, 30, tzinfo=UTC)
        r2 = self._success("TSLA", fetched_at=t2)
        r1 = self._success("AAPL", fetched_at=t1)
        store.record_fetch(r2)
        store.record_fetch(r1)
        records = store.get_records()
        assert records[0].fetched_at == t1
        assert records[1].fetched_at == t2

    def test_filter_by_since(self) -> None:
        store = InMemoryProvenanceStore()
        t1 = datetime(2026, 5, 13, 9, 0, tzinfo=UTC)
        t2 = datetime(2026, 5, 13, 10, 0, tzinfo=UTC)
        store.record_fetch(self._success("AAPL", fetched_at=t1))
        store.record_fetch(self._success("TSLA", fetched_at=t2))
        records = store.get_records(since=datetime(2026, 5, 13, 9, 30, tzinfo=UTC))
        assert len(records) == 1
        assert records[0].symbol == "TSLA"

    def test_filter_by_until(self) -> None:
        store = InMemoryProvenanceStore()
        t1 = datetime(2026, 5, 13, 9, 0, tzinfo=UTC)
        t2 = datetime(2026, 5, 13, 10, 0, tzinfo=UTC)
        store.record_fetch(self._success("AAPL", fetched_at=t1))
        store.record_fetch(self._success("TSLA", fetched_at=t2))
        records = store.get_records(until=datetime(2026, 5, 13, 9, 30, tzinfo=UTC))
        assert len(records) == 1
        assert records[0].symbol == "AAPL"

    def test_filter_by_provider_id(self) -> None:
        store = InMemoryProvenanceStore()
        r1 = ProviderFetchRecord.for_success(
            provider_id="yfinance", provider_version="1.0",
            symbol="AAPL", fetched_at=_NOW, data_as_of=_CLOSE,
        )
        r2 = ProviderFetchRecord.for_success(
            provider_id="alpaca", provider_version="1.0",
            symbol="AAPL", fetched_at=_NOW, data_as_of=_CLOSE,
        )
        store.record_fetch(r1)
        store.record_fetch(r2)
        records = store.get_records(provider_id="yfinance")
        assert len(records) == 1
        assert records[0].provider_id == "yfinance"

    def test_filter_by_symbol(self) -> None:
        store = InMemoryProvenanceStore()
        store.record_fetch(self._success("AAPL"))
        store.record_fetch(self._success("TSLA"))
        records = store.get_records(symbol="TSLA")
        assert len(records) == 1
        assert records[0].symbol == "TSLA"

    def test_combined_filters(self) -> None:
        store = InMemoryProvenanceStore()
        t1 = datetime(2026, 5, 13, 9, 0, tzinfo=UTC)
        t2 = datetime(2026, 5, 13, 11, 0, tzinfo=UTC)
        store.record_fetch(self._success("AAPL", fetched_at=t1))
        store.record_fetch(self._success("AAPL", fetched_at=t2))
        records = store.get_records(
            since=t1,
            until=t1,
            symbol="AAPL",
        )
        assert len(records) == 1
        assert records[0].fetched_at == t1

    def test_get_records_returns_tuple(self) -> None:
        store = InMemoryProvenanceStore()
        store.record_fetch(self._success())
        result = store.get_records()
        assert isinstance(result, tuple)

    def test_satisfies_provenance_store_protocol(self) -> None:
        store: ProvenanceStore = InMemoryProvenanceStore()
        record = ProviderFetchRecord.for_success(
            provider_id="stub", provider_version="1.0",
            symbol="AAPL", fetched_at=_NOW, data_as_of=_CLOSE,
        )
        store.record_fetch(record)
        records = store.get_records()
        assert len(records) == 1


# ---------------------------------------------------------------------------
# MarketSnapshotService integration with ProvenanceStore
# ---------------------------------------------------------------------------


class TestMarketSnapshotServiceProvenanceIntegration:
    def test_fetch_context_records_success(self) -> None:
        store = InMemoryProvenanceStore()
        provider = _make_provider(snapshot=_make_snapshot("AAPL"))
        service = MarketSnapshotService(provider, provenance_store=store)
        service.fetch_context(MarketContextRequest(symbols=("AAPL",)))
        records = store.get_records()
        assert len(records) == 1
        assert records[0].outcome == "success"
        assert records[0].symbol == "AAPL"

    def test_fetch_context_records_failure(self) -> None:
        store = InMemoryProvenanceStore()
        provider = _make_provider(raises=True)
        service = MarketSnapshotService(provider, provenance_store=store)
        service.fetch_context(MarketContextRequest(symbols=("AAPL",)))
        records = store.get_records()
        assert len(records) == 1
        assert records[0].outcome == "failure"
        assert records[0].error_reason == "network error"

    def test_fetch_context_records_mixed_outcomes(self) -> None:
        store = InMemoryProvenanceStore()
        provider = MagicMock()
        provider.provider_id = "stub"
        provider.provider_version = "1.0"

        def side_effect(symbol: str) -> MarketSnapshot:
            if symbol == "AAPL":
                return _make_snapshot("AAPL")
            raise ProviderUnavailableError("stub", symbol, "not found")

        provider.fetch_snapshot.side_effect = side_effect
        service = MarketSnapshotService(provider, provenance_store=store)
        service.fetch_context(MarketContextRequest(symbols=("AAPL", "BADTICKER")))
        records = store.get_records()
        assert len(records) == 2
        outcomes = {r.symbol: r.outcome for r in records}
        assert outcomes["AAPL"] == "success"
        assert outcomes["BADTICKER"] == "failure"

    def test_fetch_snapshot_records_success(self) -> None:
        store = InMemoryProvenanceStore()
        provider = _make_provider(snapshot=_make_snapshot("TSLA"))
        service = MarketSnapshotService(provider, provenance_store=store)
        provider.fetch_snapshot.return_value = _make_snapshot("TSLA")
        service.fetch_snapshot("TSLA")
        records = store.get_records()
        assert len(records) == 1
        assert records[0].symbol == "TSLA"
        assert records[0].outcome == "success"

    def test_fetch_snapshot_records_failure_and_reraises(self) -> None:
        store = InMemoryProvenanceStore()
        provider = _make_provider(raises=True)
        service = MarketSnapshotService(provider, provenance_store=store)
        with pytest.raises(ProviderUnavailableError):
            service.fetch_snapshot("AAPL")
        records = store.get_records()
        assert len(records) == 1
        assert records[0].outcome == "failure"

    def test_no_provenance_store_leaves_behavior_unchanged(self) -> None:
        provider = _make_provider(snapshot=_make_snapshot("AAPL"))
        service = MarketSnapshotService(provider)
        result = service.fetch_context(MarketContextRequest(symbols=("AAPL",)))
        assert result.is_complete

    def test_success_record_carries_snapshot_provenance(self) -> None:
        store = InMemoryProvenanceStore()
        snap = _make_snapshot("AAPL")
        provider = _make_provider(snapshot=snap)
        service = MarketSnapshotService(provider, provenance_store=store)
        service.fetch_snapshot("AAPL")
        records = store.get_records()
        assert records[0].data_as_of == snap.provenance.data_as_of
        assert records[0].fetched_at == snap.provenance.fetched_at
        assert records[0].provider_id == snap.provenance.provider_id


# ---------------------------------------------------------------------------
# ProvenanceQueryService tests
# ---------------------------------------------------------------------------


class TestProvenanceQueryService:
    def _store_with_records(self) -> InMemoryProvenanceStore:
        store = InMemoryProvenanceStore()
        store.record_fetch(ProviderFetchRecord.for_success(
            provider_id="yfinance", provider_version="1.0",
            symbol="AAPL", fetched_at=_NOW, data_as_of=_CLOSE,
        ))
        store.record_fetch(ProviderFetchRecord.for_success(
            provider_id="alpaca", provider_version="0.43",
            symbol="TSLA", fetched_at=_NOW, data_as_of=_CLOSE,
        ))
        store.record_fetch(ProviderFetchRecord.for_failure(
            provider_id="yfinance", provider_version="1.0",
            symbol="NVDA", fetched_at=_NOW, error_reason="unavailable",
        ))
        return store

    def test_query_all_returns_all_records(self) -> None:
        service = ProvenanceQueryService(self._store_with_records())
        result = service.query()
        assert result.total_count == 3

    def test_query_success_failure_counts(self) -> None:
        service = ProvenanceQueryService(self._store_with_records())
        result = service.query()
        assert result.success_count == 2
        assert result.failure_count == 1

    def test_query_providers_seen(self) -> None:
        service = ProvenanceQueryService(self._store_with_records())
        result = service.query()
        assert set(result.providers_seen) == {"yfinance", "alpaca"}

    def test_query_symbols_seen(self) -> None:
        service = ProvenanceQueryService(self._store_with_records())
        result = service.query()
        assert set(result.symbols_seen) == {"AAPL", "TSLA", "NVDA"}

    def test_query_authority_is_advisory(self) -> None:
        service = ProvenanceQueryService(self._store_with_records())
        result = service.query()
        assert result.authority == ProvenanceQueryAuthority.ADVISORY
        assert result.is_advisory

    def test_query_with_provider_filter(self) -> None:
        service = ProvenanceQueryService(self._store_with_records())
        result = service.query(provider_id="alpaca")
        assert result.total_count == 1
        assert result.records[0].symbol == "TSLA"

    def test_query_with_symbol_filter(self) -> None:
        service = ProvenanceQueryService(self._store_with_records())
        result = service.query(symbol="AAPL")
        assert result.total_count == 1

    def test_empty_store_query(self) -> None:
        service = ProvenanceQueryService(InMemoryProvenanceStore())
        result = service.query()
        assert result.total_count == 0
        assert result.success_count == 0
        assert result.failure_count == 0
        assert result.providers_seen == ()
        assert result.symbols_seen == ()


# ---------------------------------------------------------------------------
# API endpoint tests
# ---------------------------------------------------------------------------


class TestProvenanceEndpoint:
    def _client_with_store(self) -> tuple[TestClient, InMemoryProvenanceStore]:
        store = InMemoryProvenanceStore()
        query_service = ProvenanceQueryService(store)
        app = create_app(provenance_query_service=query_service)
        return TestClient(app), store

    def test_empty_registry_returns_empty_response(self) -> None:
        client, _ = self._client_with_store()
        resp = client.get("/provenance/market-data")
        assert resp.status_code == 200
        data = resp.json()
        assert data["authority"] == "advisory"
        assert data["total_count"] == 0
        assert data["records"] == []

    def test_records_returned_after_fetch(self) -> None:
        client, store = self._client_with_store()
        store.record_fetch(ProviderFetchRecord.for_success(
            provider_id="yfinance", provider_version="1.0",
            symbol="AAPL", fetched_at=_NOW, data_as_of=_CLOSE,
        ))
        resp = client.get("/provenance/market-data")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_count"] == 1
        assert data["success_count"] == 1
        assert data["failure_count"] == 0
        assert data["records"][0]["symbol"] == "AAPL"
        assert data["records"][0]["is_advisory"] is True

    def test_failure_record_in_response(self) -> None:
        client, store = self._client_with_store()
        store.record_fetch(ProviderFetchRecord.for_failure(
            provider_id="alpaca", provider_version="0.43",
            symbol="NVDA", fetched_at=_NOW, error_reason="rate limit",
        ))
        resp = client.get("/provenance/market-data")
        data = resp.json()
        assert data["failure_count"] == 1
        assert data["records"][0]["outcome"] == "failure"
        assert data["records"][0]["error_reason"] == "rate limit"

    def test_filter_by_provider_id(self) -> None:
        client, store = self._client_with_store()
        store.record_fetch(ProviderFetchRecord.for_success(
            provider_id="yfinance", provider_version="1.0",
            symbol="AAPL", fetched_at=_NOW, data_as_of=_CLOSE,
        ))
        store.record_fetch(ProviderFetchRecord.for_success(
            provider_id="alpaca", provider_version="0.43",
            symbol="TSLA", fetched_at=_NOW, data_as_of=_CLOSE,
        ))
        resp = client.get("/provenance/market-data?provider_id=alpaca")
        data = resp.json()
        assert data["total_count"] == 1
        assert data["records"][0]["symbol"] == "TSLA"

    def test_filter_by_symbol(self) -> None:
        client, store = self._client_with_store()
        store.record_fetch(ProviderFetchRecord.for_success(
            provider_id="yfinance", provider_version="1.0",
            symbol="AAPL", fetched_at=_NOW, data_as_of=_CLOSE,
        ))
        store.record_fetch(ProviderFetchRecord.for_success(
            provider_id="yfinance", provider_version="1.0",
            symbol="TSLA", fetched_at=_NOW, data_as_of=_CLOSE,
        ))
        resp = client.get("/provenance/market-data?symbol=AAPL")
        data = resp.json()
        assert data["total_count"] == 1
        assert data["records"][0]["symbol"] == "AAPL"

    def test_providers_seen_and_symbols_seen_in_response(self) -> None:
        client, store = self._client_with_store()
        store.record_fetch(ProviderFetchRecord.for_success(
            provider_id="yfinance", provider_version="1.0",
            symbol="AAPL", fetched_at=_NOW, data_as_of=_CLOSE,
        ))
        resp = client.get("/provenance/market-data")
        data = resp.json()
        assert "yfinance" in data["providers_seen"]
        assert "AAPL" in data["symbols_seen"]

    def test_default_app_has_provenance_endpoint(self) -> None:
        from src.app.api.application import create_app as default_create_app
        default_app = default_create_app()
        client = TestClient(default_app)
        resp = client.get("/provenance/market-data")
        assert resp.status_code == 200
