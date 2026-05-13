from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime

from src.domain.market.provider import MarketDataProvider, ProviderUnavailableError
from src.domain.market.regime import MarketRegimeInterpreter
from src.domain.market.snapshot import MarketSnapshot
from src.services.market.context import (
    MarketContextAuthority,
    MarketContextRequest,
    MarketContextResult,
    SymbolFetchResult,
)


class MarketSnapshotService:
    """Services-layer orchestrator for normalized market context fetches.

    Wraps a MarketDataProvider port and an optional MarketRegimeInterpreter.
    When an interpreter is provided, fetched snapshots are annotated with an
    inferred regime classification before being returned.

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
    ) -> None:
        self._provider = provider
        self._regime_interpreter = regime_interpreter

    def _annotate(self, snapshot: MarketSnapshot) -> MarketSnapshot:
        """Apply regime interpretation if an interpreter is configured."""
        if self._regime_interpreter is None:
            return snapshot
        try:
            regime = self._regime_interpreter.interpret(snapshot)
            return replace(snapshot, regime=regime)
        except Exception:
            return snapshot

    def fetch_context(self, request: MarketContextRequest) -> MarketContextResult:
        """Fetch normalized advisory context for all requested symbols.

        Partial failures are captured in MarketContextResult.unavailable_symbols.
        Never raises for individual symbol failures.
        """
        fetched_at = datetime.now(UTC)
        symbol_results: list[SymbolFetchResult] = []

        for symbol in request.symbols:
            try:
                snapshot = self._annotate(self._provider.fetch_snapshot(symbol))
                symbol_results.append(SymbolFetchResult.success(snapshot))
            except ProviderUnavailableError as exc:
                symbol_results.append(SymbolFetchResult.failure(symbol, exc.reason))

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
        return self._annotate(self._provider.fetch_snapshot(symbol))
