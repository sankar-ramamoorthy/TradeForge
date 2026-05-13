from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version
from typing import Any

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from src.domain.market.provider import ProviderUnavailableError
from src.domain.market.snapshot import MarketSnapshot, PriceOHLCV, ProviderProvenance

_PROVIDER_ID = "alpaca"
_LOOKBACK_DAYS = 5


def _sdk_version() -> str:
    try:
        return _pkg_version("alpaca-py")
    except PackageNotFoundError:
        return "unknown"


class AlpacaProvider:
    """Read-only market data provider adapter backed by Alpaca Markets.

    Satisfies the MarketDataProvider Protocol structurally.
    All returned snapshots are advisory and non-canonical.

    SDK coupling is entirely contained here — domain and services layers
    never import alpaca directly (ADR-0032).

    Both an API key and a secret key are required at construction.
    These are infrastructure concerns and must not propagate into
    domain or services layers.
    """

    def __init__(self, api_key: str, secret_key: str) -> None:
        self._client: StockHistoricalDataClient = StockHistoricalDataClient(
            api_key=api_key, secret_key=secret_key
        )

    @property
    def provider_id(self) -> str:
        return _PROVIDER_ID

    @property
    def provider_version(self) -> str:
        return _sdk_version()

    def fetch_snapshot(self, symbol: str) -> MarketSnapshot:
        """Fetch the latest advisory OHLCV snapshot for a symbol via Alpaca.

        Uses the stock bars endpoint with a short lookback window to obtain
        the most recent completed daily candle. Raises ProviderUnavailableError
        if Alpaca returns no data or any exception occurs during fetch or parsing.
        """
        fetched_at = datetime.now(UTC)
        upper_symbol = symbol.upper()

        try:
            request = StockBarsRequest(
                symbol_or_symbols=upper_symbol,
                timeframe=TimeFrame.Day,
                start=datetime.now(UTC) - timedelta(days=_LOOKBACK_DAYS),
            )
            response = self._client.get_stock_bars(request)
        except Exception as exc:
            raise ProviderUnavailableError(
                _PROVIDER_ID, upper_symbol, str(exc)
            ) from exc

        try:
            bars = list(response[upper_symbol])
        except KeyError:
            bars = []

        if not bars:
            raise ProviderUnavailableError(
                _PROVIDER_ID, upper_symbol, "no data returned for symbol"
            )

        try:
            price = _parse_bar(upper_symbol, bars[-1])
        except Exception as exc:
            raise ProviderUnavailableError(
                _PROVIDER_ID, upper_symbol, f"failed to parse response: {exc}"
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


def _parse_bar(symbol: str, bar: Any) -> PriceOHLCV:
    """Extract and normalize OHLCV data from an Alpaca Bar response object.

    Alpaca Bar.timestamp is a datetime object; it may be UTC-aware or naive.
    Volume may arrive as a float and is cast to int for the normalized contract.
    """
    as_of: datetime = bar.timestamp
    if as_of.tzinfo is None:
        as_of = as_of.replace(tzinfo=UTC)
    else:
        as_of = as_of.astimezone(UTC)

    return PriceOHLCV(
        symbol=symbol,
        open=Decimal(str(float(bar.open))),
        high=Decimal(str(float(bar.high))),
        low=Decimal(str(float(bar.low))),
        close=Decimal(str(float(bar.close))),
        volume=int(float(bar.volume)),
        as_of=as_of,
    )
