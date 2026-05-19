from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime

from src.domain.market.provenance import ProvenanceStore, ProviderFetchRecord
from src.domain.market.provider import MarketDataProvider, ProviderUnavailableError
from src.domain.market.regime import MarketRegimeInterpreter
from src.domain.market.snapshot import MarketSnapshot
from src.domain.market.snapshot_persistence import MarketSnapshotPersistenceStore
from src.services.market.context import (
    MarketContextAuthority,
    MarketContextRequest,
    MarketContextResult,
    ProviderAttempt,
    SymbolFetchResult,
)


class MarketSnapshotService:
    """Services-layer orchestrator for normalized market context fetches.

    Wraps a MarketDataProvider port and an optional MarketRegimeInterpreter.
    When an interpreter is provided, fetched snapshots are annotated with an
    inferred regime classification before being returned.

    When a provenance_store is provided, each fetch outcome (success or failure)
    is automatically recorded as an advisory ProviderFetchRecord.

    fetch_context handles partial provider failures gracefully — unavailable
    symbols are recorded rather than raising, so workspace overlays can render
    partial context without crashing.

    fetch_snapshot re-raises ProviderUnavailableError for callers that
    explicitly require a single symbol's data.
    """

    def __init__(
        self,
        provider: MarketDataProvider,
        regime_interpreter: MarketRegimeInterpreter | None = None,
        provenance_store: ProvenanceStore | None = None,
        snapshot_persistence_store: MarketSnapshotPersistenceStore | None = None,
    ) -> None:
        self._provider = provider
        self._regime_interpreter = regime_interpreter
        self._provenance_store = provenance_store
        self._snapshot_persistence_store = snapshot_persistence_store

    def _annotate(self, snapshot: MarketSnapshot) -> MarketSnapshot:
        """Apply regime interpretation if an interpreter is configured."""
        if self._regime_interpreter is None:
            return snapshot
        try:
            regime = self._regime_interpreter.interpret(snapshot)
            return replace(snapshot, regime=regime)
        except Exception:
            return snapshot

    def _persist_snapshot(self, snapshot: MarketSnapshot) -> None:
        if self._snapshot_persistence_store is None:
            return
        try:
            self._snapshot_persistence_store.persist(snapshot)
        except Exception:
            pass

    def _record_success(self, snapshot: MarketSnapshot) -> None:
        if self._provenance_store is None:
            return
        record = ProviderFetchRecord.for_success(
            provider_id=snapshot.provenance.provider_id,
            provider_version=snapshot.provenance.provider_version,
            symbol=snapshot.symbol,
            fetched_at=snapshot.provenance.fetched_at,
            data_as_of=snapshot.provenance.data_as_of,
        )
        self._provenance_store.record_fetch(record)

    def _record_failure(self, symbol: str, fetched_at: datetime, reason: str) -> None:
        if self._provenance_store is None:
            return
        record = ProviderFetchRecord.for_failure(
            provider_id=self._provider.provider_id,
            provider_version=self._provider.provider_version,
            symbol=symbol,
            fetched_at=fetched_at,
            error_reason=reason,
        )
        self._provenance_store.record_fetch(record)

    def fetch_context(self, request: MarketContextRequest) -> MarketContextResult:
        """Fetch normalized advisory context for all requested symbols.

        Partial failures are captured in MarketContextResult.unavailable_symbols.
        Never raises for individual symbol failures.
        """
        fetched_at = datetime.now(UTC)
        symbol_results: list[SymbolFetchResult] = []

        for symbol in request.symbols:
            attempt_at = datetime.now(UTC)
            try:
                snapshot = self._annotate(self._provider.fetch_snapshot(symbol))
                self._record_success(snapshot)
                self._persist_snapshot(snapshot)
                symbol_results.append(
                    SymbolFetchResult.success(
                        snapshot,
                        attempts=(
                            ProviderAttempt(
                                provider_id=self._provider.provider_id,
                                attempted_at=attempt_at,
                                outcome="success",
                            ),
                        ),
                    )
                )
            except ProviderUnavailableError as exc:
                self._record_failure(symbol, attempt_at, exc.reason)
                symbol_results.append(
                    SymbolFetchResult.failure(
                        symbol,
                        exc.reason,
                        attempts=(
                            ProviderAttempt(
                                provider_id=self._provider.provider_id,
                                attempted_at=attempt_at,
                                outcome="failure",
                                failure_reason=exc.reason,
                            ),
                        ),
                    )
                )

        available = tuple(
            r.snapshot for r in symbol_results if r.snapshot is not None
        )
        unavailable = tuple(r.symbol for r in symbol_results if not r.is_available)

        return MarketContextResult(
            available=available,
            unavailable_symbols=unavailable,
            symbol_results=tuple(symbol_results),
            provider_id=self._provider.provider_id,
            fetched_at=fetched_at,
            authority=MarketContextAuthority.ADVISORY,
        )

    def fetch_snapshot(self, symbol: str) -> MarketSnapshot:
        """Fetch a normalized advisory snapshot for a single symbol.

        Propagates ProviderUnavailableError if the provider cannot fulfil
        the request — callers that need the data must handle the failure.
        """
        attempt_at = datetime.now(UTC)
        try:
            snapshot = self._annotate(self._provider.fetch_snapshot(symbol))
            self._record_success(snapshot)
            self._persist_snapshot(snapshot)
            return snapshot
        except ProviderUnavailableError as exc:
            self._record_failure(symbol, attempt_at, exc.reason)
            raise
