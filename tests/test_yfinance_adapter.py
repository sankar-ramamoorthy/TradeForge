"""
Tests for TF-0044: yfinance provider adapter.

All tests mock yfinance.Ticker — no real network calls are made.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from src.domain.market.provider import ProviderUnavailableError
from src.infrastructure.market.yfinance_adapter import YFinanceProvider

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_CLOSE_TS = pd.Timestamp("2026-05-12 20:00:00", tz="UTC")


def _make_hist(
    open_: float = 185.0,
    high: float = 187.5,
    low: float = 184.2,
    close: float = 186.4,
    volume: int = 52_000_000,
    ts: pd.Timestamp = _CLOSE_TS,
) -> pd.DataFrame:
    """Return a minimal yfinance-style history DataFrame."""
    return pd.DataFrame(
        {
            "Open": [open_],
            "High": [high],
            "Low": [low],
            "Close": [close],
            "Volume": [volume],
        },
        index=pd.DatetimeIndex([ts]),
    )


def _patch_ticker(hist: pd.DataFrame, version: str = "1.3.0") -> MagicMock:
    mock_ticker = MagicMock()
    mock_ticker.history.return_value = hist
    return mock_ticker


# ---------------------------------------------------------------------------
# provider_id and provider_version
# ---------------------------------------------------------------------------


class TestYFinanceProviderIdentity:
    def test_provider_id(self) -> None:
        provider = YFinanceProvider()
        assert provider.provider_id == "yfinance"

    def test_provider_version_is_non_empty_string(self) -> None:
        provider = YFinanceProvider()
        assert isinstance(provider.provider_version, str)
        assert provider.provider_version.strip() != ""


# ---------------------------------------------------------------------------
# Successful fetch
# ---------------------------------------------------------------------------


class TestYFinanceProviderFetchSuccess:
    def setup_method(self) -> None:
        self.provider = YFinanceProvider()

    def test_snapshot_symbol_uppercased(self) -> None:
        hist = _make_hist()
        with patch(
            "src.infrastructure.market.yfinance_adapter.yf"
        ) as mock_yf:
            mock_yf.Ticker.return_value = _patch_ticker(hist)
            snap = self.provider.fetch_snapshot("aapl")
        assert snap.symbol == "AAPL"

    def test_snapshot_ohlcv_mapped_correctly(self) -> None:
        hist = _make_hist(
            open_=185.0, high=187.5, low=184.2, close=186.4, volume=52_000_000
        )
        with patch(
            "src.infrastructure.market.yfinance_adapter.yf"
        ) as mock_yf:
            mock_yf.Ticker.return_value = _patch_ticker(hist)
            snap = self.provider.fetch_snapshot("AAPL")

        assert snap.price.open == Decimal("185.0")
        assert snap.price.high == Decimal("187.5")
        assert snap.price.low == Decimal("184.2")
        assert snap.price.close == Decimal("186.4")
        assert snap.price.volume == 52_000_000

    def test_snapshot_prices_are_decimal(self) -> None:
        hist = _make_hist()
        with patch(
            "src.infrastructure.market.yfinance_adapter.yf"
        ) as mock_yf:
            mock_yf.Ticker.return_value = _patch_ticker(hist)
            snap = self.provider.fetch_snapshot("AAPL")

        assert isinstance(snap.price.open, Decimal)
        assert isinstance(snap.price.close, Decimal)

    def test_snapshot_as_of_matches_dataframe_index(self) -> None:
        ts = pd.Timestamp("2026-05-12 20:00:00", tz="UTC")
        hist = _make_hist(ts=ts)
        with patch(
            "src.infrastructure.market.yfinance_adapter.yf"
        ) as mock_yf:
            mock_yf.Ticker.return_value = _patch_ticker(hist)
            snap = self.provider.fetch_snapshot("AAPL")

        expected = datetime(2026, 5, 12, 20, 0, 0, tzinfo=UTC)
        assert snap.price.as_of == expected

    def test_snapshot_as_of_normalized_to_utc_from_naive(self) -> None:
        ts = pd.Timestamp("2026-05-12 20:00:00")  # tz-naive
        hist = _make_hist(ts=ts)
        with patch(
            "src.infrastructure.market.yfinance_adapter.yf"
        ) as mock_yf:
            mock_yf.Ticker.return_value = _patch_ticker(hist)
            snap = self.provider.fetch_snapshot("AAPL")

        assert snap.price.as_of.tzinfo is not None

    def test_provenance_provider_id(self) -> None:
        hist = _make_hist()
        with patch(
            "src.infrastructure.market.yfinance_adapter.yf"
        ) as mock_yf:
            mock_yf.Ticker.return_value = _patch_ticker(hist)
            snap = self.provider.fetch_snapshot("AAPL")

        assert snap.provenance.provider_id == "yfinance"

    def test_provenance_fetched_at_is_recent(self) -> None:
        hist = _make_hist()
        before = datetime.now(UTC)
        with patch(
            "src.infrastructure.market.yfinance_adapter.yf"
        ) as mock_yf:
            mock_yf.Ticker.return_value = _patch_ticker(hist)
            snap = self.provider.fetch_snapshot("AAPL")
        after = datetime.now(UTC)

        assert before <= snap.provenance.fetched_at <= after

    def test_provenance_data_as_of_matches_candle(self) -> None:
        ts = pd.Timestamp("2026-05-12 20:00:00", tz="UTC")
        hist = _make_hist(ts=ts)
        with patch(
            "src.infrastructure.market.yfinance_adapter.yf"
        ) as mock_yf:
            mock_yf.Ticker.return_value = _patch_ticker(hist)
            snap = self.provider.fetch_snapshot("AAPL")

        assert snap.provenance.data_as_of == snap.price.as_of

    def test_snapshot_is_advisory(self) -> None:
        hist = _make_hist()
        with patch(
            "src.infrastructure.market.yfinance_adapter.yf"
        ) as mock_yf:
            mock_yf.Ticker.return_value = _patch_ticker(hist)
            snap = self.provider.fetch_snapshot("AAPL")

        assert snap.is_advisory is True

    def test_uses_latest_row_from_multirow_dataframe(self) -> None:
        ts1 = pd.Timestamp("2026-05-11 20:00:00", tz="UTC")
        ts2 = pd.Timestamp("2026-05-12 20:00:00", tz="UTC")
        hist = pd.DataFrame(
            {
                "Open": [100.0, 185.0],
                "High": [105.0, 187.5],
                "Low": [99.0, 184.2],
                "Close": [103.0, 186.4],
                "Volume": [1_000_000, 52_000_000],
            },
            index=pd.DatetimeIndex([ts1, ts2]),
        )
        with patch(
            "src.infrastructure.market.yfinance_adapter.yf"
        ) as mock_yf:
            mock_yf.Ticker.return_value = _patch_ticker(hist)
            snap = self.provider.fetch_snapshot("AAPL")

        assert snap.price.close == Decimal("186.4")
        assert snap.price.volume == 52_000_000


# ---------------------------------------------------------------------------
# Failure modes
# ---------------------------------------------------------------------------


class TestYFinanceProviderFetchFailure:
    def setup_method(self) -> None:
        self.provider = YFinanceProvider()

    def test_empty_dataframe_raises_provider_unavailable(self) -> None:
        empty_hist = pd.DataFrame()
        with patch(
            "src.infrastructure.market.yfinance_adapter.yf"
        ) as mock_yf:
            mock_yf.Ticker.return_value = _patch_ticker(empty_hist)
            with pytest.raises(ProviderUnavailableError) as exc_info:
                self.provider.fetch_snapshot("AAPL")

        assert exc_info.value.provider_id == "yfinance"
        assert exc_info.value.symbol == "AAPL"
        assert "no data" in exc_info.value.reason

    def test_sdk_exception_raises_provider_unavailable(self) -> None:
        with patch(
            "src.infrastructure.market.yfinance_adapter.yf"
        ) as mock_yf:
            mock_yf.Ticker.side_effect = RuntimeError("connection refused")
            with pytest.raises(ProviderUnavailableError) as exc_info:
                self.provider.fetch_snapshot("AAPL")

        assert exc_info.value.provider_id == "yfinance"
        assert exc_info.value.symbol == "AAPL"

    def test_history_exception_raises_provider_unavailable(self) -> None:
        with patch(
            "src.infrastructure.market.yfinance_adapter.yf"
        ) as mock_yf:
            mock_ticker = MagicMock()
            mock_ticker.history.side_effect = ValueError("rate limited")
            mock_yf.Ticker.return_value = mock_ticker
            with pytest.raises(ProviderUnavailableError):
                self.provider.fetch_snapshot("AAPL")

    def test_provider_unavailable_error_is_subclass_of_exception(self) -> None:
        assert issubclass(ProviderUnavailableError, Exception)


# ---------------------------------------------------------------------------
# fetch_snapshots
# ---------------------------------------------------------------------------


class TestYFinanceProviderFetchSnapshots:
    def setup_method(self) -> None:
        self.provider = YFinanceProvider()

    def test_returns_tuple_of_snapshots(self) -> None:
        symbols = ("AAPL", "TSLA", "NVDA")
        hist = _make_hist()
        with patch(
            "src.infrastructure.market.yfinance_adapter.yf"
        ) as mock_yf:
            mock_yf.Ticker.return_value = _patch_ticker(hist)
            snaps = self.provider.fetch_snapshots(symbols)

        assert isinstance(snaps, tuple)
        assert len(snaps) == 3

    def test_symbol_order_preserved(self) -> None:
        symbols = ("AAPL", "TSLA", "NVDA")
        hist = _make_hist()
        with patch(
            "src.infrastructure.market.yfinance_adapter.yf"
        ) as mock_yf:
            mock_yf.Ticker.return_value = _patch_ticker(hist)
            snaps = self.provider.fetch_snapshots(symbols)

        assert tuple(s.symbol for s in snaps) == symbols

    def test_all_snapshots_are_advisory(self) -> None:
        hist = _make_hist()
        with patch(
            "src.infrastructure.market.yfinance_adapter.yf"
        ) as mock_yf:
            mock_yf.Ticker.return_value = _patch_ticker(hist)
            snaps = self.provider.fetch_snapshots(("AAPL", "TSLA"))

        assert all(s.is_advisory for s in snaps)

    def test_raises_on_unavailable_symbol(self) -> None:
        def _side_effect(symbol: str) -> MagicMock:
            mock = MagicMock()
            if symbol == "TSLA":
                mock.history.return_value = pd.DataFrame()
            else:
                mock.history.return_value = _make_hist()
            return mock

        with patch(
            "src.infrastructure.market.yfinance_adapter.yf"
        ) as mock_yf:
            mock_yf.Ticker.side_effect = _side_effect
            with pytest.raises(ProviderUnavailableError) as exc_info:
                self.provider.fetch_snapshots(("AAPL", "TSLA"))

        assert exc_info.value.symbol == "TSLA"
