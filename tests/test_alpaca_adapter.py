"""
Tests for TF-0046: Alpaca market data provider adapter.

All tests mock alpaca.data.historical.StockHistoricalDataClient —
no real network calls are made.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest
from src.domain.market.provider import ProviderUnavailableError
from src.infrastructure.market.alpaca_adapter import AlpacaProvider

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_CLOSE_DT = datetime(2026, 5, 12, 20, 0, 0, tzinfo=UTC)
_PATCH_PATH = "src.infrastructure.market.alpaca_adapter.StockHistoricalDataClient"


def _make_bar(
    open_: float = 185.0,
    high: float = 187.5,
    low: float = 184.2,
    close: float = 186.4,
    volume: float = 52_000_000,
    timestamp: datetime = _CLOSE_DT,
) -> MagicMock:
    """Return a minimal Alpaca-style Bar MagicMock."""
    bar = MagicMock()
    bar.open = open_
    bar.high = high
    bar.low = low
    bar.close = close
    bar.volume = volume
    bar.timestamp = timestamp
    return bar


def _make_provider() -> tuple[AlpacaProvider, MagicMock]:
    """Return a provider instance and its underlying mock client."""
    mock_client = MagicMock()
    with patch(_PATCH_PATH) as mock_cls:
        mock_cls.return_value = mock_client
        provider = AlpacaProvider(api_key="test-key", secret_key="test-secret")
    return provider, mock_client


# ---------------------------------------------------------------------------
# provider_id and provider_version
# ---------------------------------------------------------------------------


class TestAlpacaProviderIdentity:
    def test_provider_id(self) -> None:
        provider, _ = _make_provider()
        assert provider.provider_id == "alpaca"

    def test_provider_version_is_non_empty_string(self) -> None:
        provider, _ = _make_provider()
        assert isinstance(provider.provider_version, str)
        assert provider.provider_version.strip() != ""

    def test_provider_version_with_known_value(self) -> None:
        provider, _ = _make_provider()
        with patch(
            "src.infrastructure.market.alpaca_adapter._sdk_version",
            return_value="0.35.0",
        ):
            assert provider.provider_version == "0.35.0"


# ---------------------------------------------------------------------------
# Successful fetch
# ---------------------------------------------------------------------------


class TestAlpacaProviderFetchSuccess:
    def setup_method(self) -> None:
        self.provider, self.mock_client = _make_provider()

    def test_snapshot_symbol_uppercased(self) -> None:
        self.mock_client.get_stock_bars.return_value = {"AAPL": [_make_bar()]}
        snap = self.provider.fetch_snapshot("aapl")
        assert snap.symbol == "AAPL"

    def test_snapshot_ohlcv_mapped_correctly(self) -> None:
        self.mock_client.get_stock_bars.return_value = {
            "AAPL": [
                _make_bar(
                    open_=185.0, high=187.5, low=184.2, close=186.4, volume=52_000_000
                )
            ]
        }
        snap = self.provider.fetch_snapshot("AAPL")

        assert snap.price.open == Decimal("185.0")
        assert snap.price.high == Decimal("187.5")
        assert snap.price.low == Decimal("184.2")
        assert snap.price.close == Decimal("186.4")
        assert snap.price.volume == 52_000_000

    def test_snapshot_prices_are_decimal(self) -> None:
        self.mock_client.get_stock_bars.return_value = {"AAPL": [_make_bar()]}
        snap = self.provider.fetch_snapshot("AAPL")

        assert isinstance(snap.price.open, Decimal)
        assert isinstance(snap.price.close, Decimal)

    def test_snapshot_as_of_matches_bar_timestamp(self) -> None:
        self.mock_client.get_stock_bars.return_value = {
            "AAPL": [_make_bar(timestamp=_CLOSE_DT)]
        }
        snap = self.provider.fetch_snapshot("AAPL")
        assert snap.price.as_of == _CLOSE_DT

    def test_snapshot_as_of_is_utc(self) -> None:
        self.mock_client.get_stock_bars.return_value = {"AAPL": [_make_bar()]}
        snap = self.provider.fetch_snapshot("AAPL")
        assert snap.price.as_of.tzinfo is not None
        assert snap.price.as_of.tzinfo == UTC

    def test_naive_timestamp_normalized_to_utc(self) -> None:
        naive_dt = datetime(2026, 5, 12, 20, 0, 0)  # no tzinfo
        self.mock_client.get_stock_bars.return_value = {
            "AAPL": [_make_bar(timestamp=naive_dt)]
        }
        snap = self.provider.fetch_snapshot("AAPL")
        assert snap.price.as_of.tzinfo is not None

    def test_volume_float_cast_to_int(self) -> None:
        self.mock_client.get_stock_bars.return_value = {
            "AAPL": [_make_bar(volume=52_000_000.0)]
        }
        snap = self.provider.fetch_snapshot("AAPL")
        assert isinstance(snap.price.volume, int)
        assert snap.price.volume == 52_000_000

    def test_provenance_provider_id(self) -> None:
        self.mock_client.get_stock_bars.return_value = {"AAPL": [_make_bar()]}
        snap = self.provider.fetch_snapshot("AAPL")
        assert snap.provenance.provider_id == "alpaca"

    def test_provenance_fetched_at_is_recent(self) -> None:
        self.mock_client.get_stock_bars.return_value = {"AAPL": [_make_bar()]}
        before = datetime.now(UTC)
        snap = self.provider.fetch_snapshot("AAPL")
        after = datetime.now(UTC)
        assert before <= snap.provenance.fetched_at <= after

    def test_provenance_data_as_of_matches_candle(self) -> None:
        self.mock_client.get_stock_bars.return_value = {
            "AAPL": [_make_bar(timestamp=_CLOSE_DT)]
        }
        snap = self.provider.fetch_snapshot("AAPL")
        assert snap.provenance.data_as_of == snap.price.as_of

    def test_snapshot_is_advisory(self) -> None:
        self.mock_client.get_stock_bars.return_value = {"AAPL": [_make_bar()]}
        snap = self.provider.fetch_snapshot("AAPL")
        assert snap.is_advisory is True

    def test_uses_last_bar_from_multi_bar_response(self) -> None:
        earlier_dt = datetime(2026, 5, 11, 20, 0, 0, tzinfo=UTC)
        self.mock_client.get_stock_bars.return_value = {
            "AAPL": [
                _make_bar(close=103.0, volume=1_000_000, timestamp=earlier_dt),
                _make_bar(close=186.4, volume=52_000_000, timestamp=_CLOSE_DT),
            ]
        }
        snap = self.provider.fetch_snapshot("AAPL")
        assert snap.price.close == Decimal("186.4")
        assert snap.price.volume == 52_000_000


# ---------------------------------------------------------------------------
# Failure modes
# ---------------------------------------------------------------------------


class TestAlpacaProviderFetchFailure:
    def setup_method(self) -> None:
        self.provider, self.mock_client = _make_provider()

    def test_missing_symbol_key_raises_provider_unavailable(self) -> None:
        self.mock_client.get_stock_bars.return_value = {}
        with pytest.raises(ProviderUnavailableError) as exc_info:
            self.provider.fetch_snapshot("AAPL")

        assert exc_info.value.provider_id == "alpaca"
        assert exc_info.value.symbol == "AAPL"
        assert "no data" in exc_info.value.reason

    def test_empty_bar_list_raises_provider_unavailable(self) -> None:
        self.mock_client.get_stock_bars.return_value = {"AAPL": []}
        with pytest.raises(ProviderUnavailableError) as exc_info:
            self.provider.fetch_snapshot("AAPL")

        assert exc_info.value.provider_id == "alpaca"
        assert exc_info.value.symbol == "AAPL"
        assert "no data" in exc_info.value.reason

    def test_sdk_exception_raises_provider_unavailable(self) -> None:
        self.mock_client.get_stock_bars.side_effect = RuntimeError("connection refused")
        with pytest.raises(ProviderUnavailableError) as exc_info:
            self.provider.fetch_snapshot("AAPL")

        assert exc_info.value.provider_id == "alpaca"
        assert exc_info.value.symbol == "AAPL"

    def test_parse_exception_raises_provider_unavailable(self) -> None:
        bad_bar = MagicMock()
        bad_bar.open = None
        bad_bar.high = None
        bad_bar.low = None
        bad_bar.close = None
        bad_bar.volume = None
        bad_bar.timestamp = None
        self.mock_client.get_stock_bars.return_value = {"AAPL": [bad_bar]}
        with pytest.raises(ProviderUnavailableError) as exc_info:
            self.provider.fetch_snapshot("AAPL")

        assert exc_info.value.provider_id == "alpaca"
        assert "failed to parse" in exc_info.value.reason

    def test_provider_unavailable_error_is_subclass_of_exception(self) -> None:
        assert issubclass(ProviderUnavailableError, Exception)

    def test_symbol_in_error_is_uppercased(self) -> None:
        self.mock_client.get_stock_bars.return_value = {}
        with pytest.raises(ProviderUnavailableError) as exc_info:
            self.provider.fetch_snapshot("aapl")

        assert exc_info.value.symbol == "AAPL"


# ---------------------------------------------------------------------------
# fetch_snapshots
# ---------------------------------------------------------------------------


class TestAlpacaProviderFetchSnapshots:
    def setup_method(self) -> None:
        self.provider, self.mock_client = _make_provider()

    def test_returns_tuple_of_snapshots(self) -> None:
        self.mock_client.get_stock_bars.return_value = {
            "AAPL": [_make_bar()],
            "TSLA": [_make_bar()],
            "NVDA": [_make_bar()],
        }
        snaps = self.provider.fetch_snapshots(("AAPL", "TSLA", "NVDA"))

        assert isinstance(snaps, tuple)
        assert len(snaps) == 3

    def test_symbol_order_preserved(self) -> None:
        def _side_effect(request: object) -> dict[str, list[MagicMock]]:
            return {"AAPL": [_make_bar()], "TSLA": [_make_bar()], "NVDA": [_make_bar()]}

        self.mock_client.get_stock_bars.side_effect = _side_effect
        symbols = ("AAPL", "TSLA", "NVDA")
        snaps = self.provider.fetch_snapshots(symbols)

        assert tuple(s.symbol for s in snaps) == symbols

    def test_all_snapshots_are_advisory(self) -> None:
        self.mock_client.get_stock_bars.return_value = {
            "AAPL": [_make_bar()],
            "TSLA": [_make_bar()],
        }
        snaps = self.provider.fetch_snapshots(("AAPL", "TSLA"))

        assert all(s.is_advisory for s in snaps)

    def test_raises_on_unavailable_symbol(self) -> None:
        def _side_effect(request: object) -> dict[str, list[MagicMock]]:
            return {"AAPL": [_make_bar()]}

        self.mock_client.get_stock_bars.side_effect = _side_effect

        with pytest.raises(ProviderUnavailableError) as exc_info:
            self.provider.fetch_snapshots(("AAPL", "TSLA"))

        assert exc_info.value.symbol == "TSLA"
