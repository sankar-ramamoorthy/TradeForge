from __future__ import annotations

from typing import Protocol

from src.domain.market.fundamentals import FundamentalsBundle
from src.domain.market.snapshot import MarketSnapshot


class MarketDataProvider(Protocol):
    """Read-only provider port for normalized market snapshots.

    All provider adapters (yfinance, Polygon, Alpaca) must satisfy this
    interface. Adapters may not write to the event ledger, authorize lifecycle
    transitions, or mutate canonical workflow state.

    Structural subtyping (Protocol) is used so adapters do not require
    inheritance — consistent with the EventStore port pattern.
    """

    @property
    def provider_id(self) -> str:
        """Stable provider identifier string (e.g. 'yfinance', 'alpaca').

        Must match the provider_id used in ProviderProvenance records
        produced by this adapter.
        """
        ...

    @property
    def provider_version(self) -> str:
        """Provider adapter version string (e.g. '0.2.37', 'v2')."""
        ...

    def fetch_snapshot(self, symbol: str) -> MarketSnapshot:
        """Fetch a normalized advisory market snapshot for the given symbol.

        Returns a MarketSnapshot carrying full ProviderProvenance.
        May raise ProviderUnavailableError if the source is unreachable.
        """
        ...

    def fetch_snapshots(self, symbols: tuple[str, ...]) -> tuple[MarketSnapshot, ...]:
        """Fetch normalized advisory snapshots for multiple symbols.

        Ordering of returned snapshots must correspond to the ordering of
        the symbols argument. Unreachable symbols should raise rather than
        return partial results silently.
        """
        ...


class PriceDataProvider(MarketDataProvider, Protocol):
    """Typed alias for providers that serve normalized price data."""


class FundamentalsDataProvider(Protocol):
    """Read-only provider port for normalized fundamentals data."""

    @property
    def provider_id(self) -> str: ...

    @property
    def provider_version(self) -> str: ...

    def fetch_fundamentals(self, symbol: str) -> FundamentalsBundle: ...


class ProviderUnavailableError(Exception):
    """Raised when a market data provider cannot fulfill a snapshot request.

    Callers must handle this explicitly — provider failures must not silently
    produce empty or stale advisory context without the consumer's awareness.
    """

    def __init__(self, provider_id: str, symbol: str, reason: str) -> None:
        self.provider_id = provider_id
        self.symbol = symbol
        self.reason = reason
        super().__init__(
            f"provider '{provider_id}' unavailable for '{symbol}': {reason}"
        )
