"""
Tests for TF-0045: Polygon.io / Massive.com provider adapter.

All tests mock polygon.RESTClient — no real network calls are made.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest
from src.domain.market.provider import ProviderUnavailableError
from src.infrastructure.market.polygon_adapter import PolygonProvider

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# 2026-05-12 20:00:00 UTC in epoch milliseconds
_CLOSE_TS_MS = int(datetime(2026, 5, 12, 20, 0, 0, tzinfo=UTC).timestamp() * 1000)
_CLOSE_DT = datetime(2026, 5, 12, 20, 0, 0, tzinfo=UTC)

_PATCH_PATH = "src.infrastructure.market.polygon_adapter.RESTClient"


def _make_agg(
    open_: float = 185.0,
    high: float = 187.5,
    low: float = 184.2,
    close: float = 186.4,
    volume: float = 52_000_000,
    timestamp_ms: int = _CLOSE_TS_MS,
) -> MagicMock:
    """Return a minimal Polygon-style aggregate MagicMock."""
    agg = MagicMock()
    agg.open = open_
    agg.high = high
    agg.low = low
    agg.close = close
    agg.volume = volume
    agg.timestamp = timestamp_ms
    return agg


def _make_provider() -> tuple[PolygonProvider, MagicMock]:
    """Return a provider instance and its underlying mock RESTClient."""
    mock_client = MagicMock()
    with patch(_PATCH_PATH) as mock_cls:
        mock_cls.return_value = mock_client
        provider = PolygonProvider(api_key="test-key")
    return provider, mock_client


# ---------------------------------------------------------------------------
# provider_id and provider_version
# ---------------------------------------------------------------------------


class TestPolygonProviderIdentity:
    def test_provider_id(self) -> None:
        provider, _ = _make_provider()
        assert provider.provider_id == "polygon"

    def test_provider_version_is_non_empty_string(self) -> None:
        provider, _ = _make_provider()
        assert isinstance(provider.provider_version, str)
        assert provider.provider_version.strip() != ""

    def test_provider_version_with_known_value(self) -> None:
        provider, _ = _make_provider()
        with patch(
            "src.infrastructure.market.polygon_adapter._sdk_version",
            return_value="1.2.3",
        ):
            assert provider.provider_version == "1.2.3"


# ---------------------------------------------------------------------------
# Successful fetch
# ---------------------------------------------------------------------------


class TestPolygonProviderFetchSuccess:
    def setup_method(self) -> None:
        self.provider, self.mock_client = _make_provider()

    def test_snapshot_symbol_uppercased(self) -> None:
        self.mock_client.get_previous_close_agg.return_value = [_make_agg()]
        snap = self.provider.fetch_snapshot("aapl")
        assert snap.symbol == "AAPL"

    def test_snapshot_ohlcv_mapped_correctly(self) -> None:
        self.mock_client.get_previous_close_agg.return_value = [
            _make_agg(
                open_=185.0, high=187.5, low=184.2, close=186.4, volume=52_000_000
            )
        ]
        snap = self.provider.fetch_snapshot("AAPL")

        assert snap.price.open == Decimal("185.0")
        assert snap.price.high == Decimal("187.5")
        assert snap.price.low == Decimal("184.2")
        assert snap.price.close == Decimal("186.4")
        assert snap.price.volume == 52_000_000

    def test_snapshot_prices_are_decimal(self) -> None:
        self.mock_client.get_previous_close_agg.return_value = [_make_agg()]
        snap = self.provider.fetch_snapshot("AAPL")

        assert isinstance(snap.price.open, Decimal)
        assert isinstance(snap.price.close, Decimal)

    def test_snapshot_as_of_matches_polygon_timestamp(self) -> None:
        self.mock_client.get_previous_close_agg.return_value = [
            _make_agg(timestamp_ms=_CLOSE_TS_MS)
        ]
        snap = self.provider.fetch_snapshot("AAPL")
        assert snap.price.as_of == _CLOSE_DT

    def test_snapshot_as_of_is_utc(self) -> None:
        self.mock_client.get_previous_close_agg.return_value = [_make_agg()]
        snap = self.provider.fetch_snapshot("AAPL")
        assert snap.price.as_of.tzinfo is not None
        assert snap.price.as_of.tzinfo == UTC

    def test_volume_float_cast_to_int(self) -> None:
        self.mock_client.get_previous_close_agg.return_value = [
            _make_agg(volume=52_000_000.0)
        ]
        snap = self.provider.fetch_snapshot("AAPL")
        assert isinstance(snap.price.volume, int)
        assert snap.price.volume == 52_000_000

    def test_provenance_provider_id(self) -> None:
        self.mock_client.get_previous_close_agg.return_value = [_make_agg()]
        snap = self.provider.fetch_snapshot("AAPL")
        assert snap.provenance.provider_id == "polygon"

    def test_provenance_fetched_at_is_recent(self) -> None:
        self.mock_client.get_previous_close_agg.return_value = [_make_agg()]
        before = datetime.now(UTC)
        snap = self.provider.fetch_snapshot("AAPL")
        after = datetime.now(UTC)
        assert before <= snap.provenance.fetched_at <= after

    def test_provenance_data_as_of_matches_candle(self) -> None:
        self.mock_client.get_previous_close_agg.return_value = [
            _make_agg(timestamp_ms=_CLOSE_TS_MS)
        ]
        snap = self.provider.fetch_snapshot("AAPL")
        assert snap.provenance.data_as_of == snap.price.as_of

    def test_snapshot_is_advisory(self) -> None:
        self.mock_client.get_previous_close_agg.return_value = [_make_agg()]
        snap = self.provider.fetch_snapshot("AAPL")
        assert snap.is_advisory is True

    def test_uses_first_agg_from_multi_result_response(self) -> None:
        ts1_ms = int(datetime(2026, 5, 11, 20, 0, 0, tzinfo=UTC).timestamp() * 1000)
        self.mock_client.get_previous_close_agg.return_value = [
            _make_agg(close=186.4, volume=52_000_000, timestamp_ms=_CLOSE_TS_MS),
            _make_agg(close=103.0, volume=1_000_000, timestamp_ms=ts1_ms),
        ]
        snap = self.provider.fetch_snapshot("AAPL")
        assert snap.price.close == Decimal("186.4")
        assert snap.price.volume == 52_000_000


# ---------------------------------------------------------------------------
# Failure modes
# ---------------------------------------------------------------------------


class TestPolygonProviderFetchFailure:
    def setup_method(self) -> None:
        self.provider, self.mock_client = _make_provider()

    def test_empty_list_raises_provider_unavailable(self) -> None:
        self.mock_client.get_previous_close_agg.return_value = []
        with pytest.raises(ProviderUnavailableError) as exc_info:
            self.provider.fetch_snapshot("AAPL")

        assert exc_info.value.provider_id == "polygon"
        assert exc_info.value.symbol == "AAPL"
        assert "no data" in exc_info.value.reason

    def test_sdk_exception_raises_provider_unavailable(self) -> None:
        self.mock_client.get_previous_close_agg.side_effect = RuntimeError(
            "connection refused"
        )
        with pytest.raises(ProviderUnavailableError) as exc_info:
            self.provider.fetch_snapshot("AAPL")

        assert exc_info.value.provider_id == "polygon"
        assert exc_info.value.symbol == "AAPL"

    def test_parse_exception_raises_provider_unavailable(self) -> None:
        bad_agg = MagicMock()
        bad_agg.open = None
        bad_agg.high = None
        bad_agg.low = None
        bad_agg.close = None
        bad_agg.volume = None
        bad_agg.timestamp = None
        self.mock_client.get_previous_close_agg.return_value = [bad_agg]
        with pytest.raises(ProviderUnavailableError) as exc_info:
            self.provider.fetch_snapshot("AAPL")

        assert exc_info.value.provider_id == "polygon"
        assert "failed to parse" in exc_info.value.reason

    def test_provider_unavailable_error_is_subclass_of_exception(self) -> None:
        assert issubclass(ProviderUnavailableError, Exception)

    def test_symbol_in_error_is_uppercased(self) -> None:
        self.mock_client.get_previous_close_agg.return_value = []
        with pytest.raises(ProviderUnavailableError) as exc_info:
            self.provider.fetch_snapshot("aapl")

        assert exc_info.value.symbol == "AAPL"


# ---------------------------------------------------------------------------
# fetch_snapshots
# ---------------------------------------------------------------------------


class TestPolygonProviderFetchSnapshots:
    def setup_method(self) -> None:
        self.provider, self.mock_client = _make_provider()

    def test_returns_tuple_of_snapshots(self) -> None:
        self.mock_client.get_previous_close_agg.return_value = [_make_agg()]
        snaps = self.provider.fetch_snapshots(("AAPL", "TSLA", "NVDA"))

        assert isinstance(snaps, tuple)
        assert len(snaps) == 3

    def test_symbol_order_preserved(self) -> None:
        self.mock_client.get_previous_close_agg.return_value = [_make_agg()]
        symbols = ("AAPL", "TSLA", "NVDA")
        snaps = self.provider.fetch_snapshots(symbols)

        assert tuple(s.symbol for s in snaps) == symbols

    def test_all_snapshots_are_advisory(self) -> None:
        self.mock_client.get_previous_close_agg.return_value = [_make_agg()]
        snaps = self.provider.fetch_snapshots(("AAPL", "TSLA"))

        assert all(s.is_advisory for s in snaps)

    def test_raises_on_unavailable_symbol(self) -> None:
        def _side_effect(symbol: str) -> list[MagicMock]:
            if symbol == "TSLA":
                return []
            return [_make_agg()]

        self.mock_client.get_previous_close_agg.side_effect = _side_effect

        with pytest.raises(ProviderUnavailableError) as exc_info:
            self.provider.fetch_snapshots(("AAPL", "TSLA"))

        assert exc_info.value.symbol == "TSLA"
