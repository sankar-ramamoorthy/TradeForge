from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import NamedTuple

from src.domain.market.provider import ProviderUnavailableError
from src.domain.market.snapshot import MarketSnapshot, PriceOHLCV, ProviderProvenance

_PROVIDER_ID = "seeded-demo"
_PROVIDER_VERSION = "1.0.0"

# Reference market close — demo data represents the session ending 2026-05-12
_DEMO_CLOSE_DATE = datetime(2026, 5, 12, 20, 0, 0, tzinfo=UTC)


class _SeedEntry(NamedTuple):
    open: str
    high: str
    low: str
    close: str
    volume: int
    # Intended regime (documentation only — interpreter derives this at runtime)
    # AAPL:  BULL            close/open +2.1%  range 3.0%
    # TSLA:  HIGH_VOLATILITY range 11.3%
    # NVDA:  BULL            close/open +2.4%  range 3.4%
    # SPY:   RANGING         close/open +0.3%  range 0.9%
    # QQQ:   BEAR            close/open -2.9%  range 3.8%
    # GLD:   RANGING         close/open +0.1%  range 1.3%
    # TLT:   LOW_VOLATILITY  range 0.38%


_DEMO_SEED: dict[str, _SeedEntry] = {
    "AAPL": _SeedEntry("182.00", "186.50", "181.00", "185.80", 52_000_000),
    "TSLA": _SeedEntry("168.00", "184.00", "165.00", "177.50", 98_000_000),
    "NVDA": _SeedEntry("875.00", "900.00", "870.00", "896.00", 41_000_000),
    "SPY":  _SeedEntry("515.00", "517.80", "513.20", "516.40", 78_000_000),
    "QQQ":  _SeedEntry("446.00", "447.00", "430.00", "433.00", 45_000_000),
    "GLD":  _SeedEntry("228.00", "229.50", "226.50", "228.20", 12_000_000),
    "TLT":  _SeedEntry("92.00",  "92.20",  "91.85",  "92.10",  18_000_000),
}


class SeededMarketDataProvider:
    """Read-only demo market data provider backed by static seed data.

    Satisfies the MarketDataProvider Protocol structurally — same boundary as
    live providers per ADR-0032: demo flow must not diverge from production path.

    Returns deterministic advisory snapshots for a curated set of demo symbols.
    Raises ProviderUnavailableError for any symbol not in the seed dataset,
    consistent with live provider error behavior.

    The seeded dataset covers all five interpretable regime outcomes so demos
    can exercise the full market regime interpretation stack without live APIs.

    Useful for:
    - local development without live API keys
    - demonstration of the complete M9 market context pipeline
    - integration tests requiring deterministic provider behavior
    """

    def __init__(self, fetched_at: datetime | None = None) -> None:
        self._fetched_at = fetched_at

    @property
    def provider_id(self) -> str:
        return _PROVIDER_ID

    @property
    def provider_version(self) -> str:
        return _PROVIDER_VERSION

    @property
    def available_symbols(self) -> tuple[str, ...]:
        """Sorted tuple of symbol tickers available in the demo seed dataset."""
        return tuple(sorted(_DEMO_SEED.keys()))

    def fetch_snapshot(self, symbol: str) -> MarketSnapshot:
        """Return a deterministic advisory snapshot for a seeded demo symbol.

        Raises ProviderUnavailableError if the symbol is not in the seed dataset.
        """
        upper = symbol.upper().strip()
        entry = _DEMO_SEED.get(upper)
        if entry is None:
            available = ", ".join(sorted(_DEMO_SEED))
            raise ProviderUnavailableError(
                _PROVIDER_ID,
                symbol,
                f"'{symbol}' not in demo seed dataset; available: {available}",
            )
        fetched_at = self._fetched_at or datetime.now(UTC)
        price = PriceOHLCV(
            symbol=upper,
            open=Decimal(entry.open),
            high=Decimal(entry.high),
            low=Decimal(entry.low),
            close=Decimal(entry.close),
            volume=entry.volume,
            as_of=_DEMO_CLOSE_DATE,
        )
        provenance = ProviderProvenance(
            provider_id=_PROVIDER_ID,
            provider_version=_PROVIDER_VERSION,
            fetched_at=fetched_at,
            data_as_of=_DEMO_CLOSE_DATE,
        )
        return MarketSnapshot(price=price, provenance=provenance)

    def fetch_snapshots(self, symbols: tuple[str, ...]) -> tuple[MarketSnapshot, ...]:
        return tuple(self.fetch_snapshot(s) for s in symbols)
