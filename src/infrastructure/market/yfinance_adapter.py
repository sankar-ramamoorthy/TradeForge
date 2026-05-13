from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

import yfinance as yf
from src.domain.market.provider import ProviderUnavailableError
from src.domain.market.snapshot import MarketSnapshot, PriceOHLCV, ProviderProvenance

_PROVIDER_ID = "yfinance"


class YFinanceProvider:
    """Read-only market data provider adapter backed by yfinance.

    Satisfies the MarketDataProvider Protocol structurally.
    All returned snapshots are advisory and non-canonical.

    SDK coupling is entirely contained here — domain and services layers
    never import yfinance directly (ADR-0032).
    """

    @property
    def provider_id(self) -> str:
        return _PROVIDER_ID

    @property
    def provider_version(self) -> str:
        try:
            return str(yf.__version__)
        except AttributeError:
            return "unknown"

    def fetch_snapshot(self, symbol: str) -> MarketSnapshot:
        """Fetch the latest advisory OHLCV snapshot for a symbol via yfinance.

        Raises ProviderUnavailableError if yfinance returns no data or any
        exception occurs during the fetch or response parsing.
        """
        fetched_at = datetime.now(UTC)

        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d")
        except Exception as exc:
            raise ProviderUnavailableError(
                _PROVIDER_ID, symbol, str(exc)
            ) from exc

        if hist.empty:
            raise ProviderUnavailableError(
                _PROVIDER_ID, symbol, "no data returned for symbol"
            )

        try:
            price = _parse_latest_ohlcv(symbol, hist)
        except Exception as exc:
            raise ProviderUnavailableError(
                _PROVIDER_ID, symbol, f"failed to parse response: {exc}"
            ) from exc

        provenance = ProviderProvenance(
            provider_id=_PROVIDER_ID,
            provider_version=self.provider_version,
            fetched_at=fetched_at,
            data_as_of=price.as_of,
        )

        return MarketSnapshot(price=price, provenance=provenance)

    def fetch_snapshots(
        self, symbols: tuple[str, ...]
    ) -> tuple[MarketSnapshot, ...]:
        """Fetch advisory snapshots for multiple symbols.

        Calls fetch_snapshot per symbol. Raises ProviderUnavailableError on
        the first symbol that cannot be fetched.
        """
        return tuple(self.fetch_snapshot(s) for s in symbols)


def _parse_latest_ohlcv(symbol: str, hist: Any) -> PriceOHLCV:
    """Extract and normalize the latest OHLCV row from a yfinance DataFrame."""
    row = hist.iloc[-1]
    ts = hist.index[-1]

    as_of: datetime = ts.to_pydatetime()
    if as_of.tzinfo is None:
        as_of = as_of.replace(tzinfo=UTC)
    else:
        as_of = as_of.astimezone(UTC)

    return PriceOHLCV(
        symbol=symbol.upper(),
        open=Decimal(str(float(row["Open"]))),
        high=Decimal(str(float(row["High"]))),
        low=Decimal(str(float(row["Low"]))),
        close=Decimal(str(float(row["Close"]))),
        volume=int(row["Volume"]),
        as_of=as_of,
    )
