from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version
from typing import Any

from polygon import RESTClient
from src.domain.market.provider import ProviderUnavailableError
from src.domain.market.snapshot import MarketSnapshot, PriceOHLCV, ProviderProvenance

_PROVIDER_ID = "polygon"


def _sdk_version() -> str:
    try:
        return _pkg_version("polygon-api-client")
    except PackageNotFoundError:
        return "unknown"


class PolygonProvider:
    """Read-only market data provider adapter backed by Polygon.io / Massive.com.

    Satisfies the MarketDataProvider Protocol structurally.
    All returned snapshots are advisory and non-canonical.

    SDK coupling is entirely contained here — domain and services layers
    never import polygon directly (ADR-0032).

    An API key is required at construction. The key is an infrastructure
    concern and must not propagate into domain or services layers.
    """

    def __init__(self, api_key: str) -> None:
        self._client: RESTClient = RESTClient(api_key=api_key)

    @property
    def provider_id(self) -> str:
        return _PROVIDER_ID

    @property
    def provider_version(self) -> str:
        return _sdk_version()

    def fetch_snapshot(self, symbol: str) -> MarketSnapshot:
        """Fetch the latest advisory OHLCV snapshot for a symbol via Polygon.io.

        Uses the previous-close aggregate endpoint to obtain the most recent
        daily OHLCV candle. Raises ProviderUnavailableError if Polygon returns
        no data or any exception occurs during the fetch or response parsing.
        """
        fetched_at = datetime.now(UTC)
        upper_symbol = symbol.upper()

        try:
            aggs = list(self._client.get_previous_close_agg(upper_symbol))
        except Exception as exc:
            raise ProviderUnavailableError(
                _PROVIDER_ID, upper_symbol, str(exc)
            ) from exc

        if not aggs:
            raise ProviderUnavailableError(
                _PROVIDER_ID, upper_symbol, "no data returned for symbol"
            )

        try:
            price = _parse_agg(upper_symbol, aggs[0])
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


def _parse_agg(symbol: str, agg: Any) -> PriceOHLCV:
    """Extract and normalize OHLCV data from a Polygon aggregate response object.

    Polygon timestamps are epoch milliseconds. Volume may arrive as a float
    from the API and is cast to int for the normalized contract.
    """
    as_of = datetime.fromtimestamp(float(agg.timestamp) / 1000, tz=UTC)

    return PriceOHLCV(
        symbol=symbol,
        open=Decimal(str(float(agg.open))),
        high=Decimal(str(float(agg.high))),
        low=Decimal(str(float(agg.low))),
        close=Decimal(str(float(agg.close))),
        volume=int(float(agg.volume)),
        as_of=as_of,
    )
