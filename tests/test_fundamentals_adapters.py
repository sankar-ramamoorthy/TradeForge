import json
from decimal import Decimal
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

import pytest
from src.domain.market.provider import ProviderUnavailableError
from src.infrastructure.market.alpha_vantage_adapter import (
    AlphaVantageFundamentalsProvider,
)
from src.infrastructure.market.fmp_adapter import FmpFundamentalsProvider


def test_fmp_adapter_normalizes_profile_statement_and_ratios() -> None:
    provider = FmpFundamentalsProvider("secret")
    with patch(
        "src.infrastructure.market.fmp_adapter._get_json",
        side_effect=[
            [
                {
                    "companyName": "Apple Inc.",
                    "sector": "Technology",
                    "industry": "Hardware",
                }
            ],
            [{"date": "2025-12-31", "revenue": 100, "netIncome": 20}],
            [{"priceToEarningsRatio": 25, "returnOnEquityRatio": 0.4}],
        ],
    ):
        bundle = provider.fetch_fundamentals("aapl")

    assert bundle.symbol == "AAPL"
    assert bundle.profile is not None
    assert bundle.profile.company_name == "Apple Inc."
    assert dict(bundle.statements[0].values)["revenue"] == 100
    assert dict(bundle.ratios.values)["price_earnings"] == 25  # type: ignore[union-attr]


def test_fmp_adapter_uses_stable_endpoint_family() -> None:
    responses: list[list[dict[str, object]]] = [
        [{"companyName": "Apple Inc.", "sector": "Technology", "industry": "Hardware"}],
        [{"date": "2025-12-31", "revenue": 100, "netIncome": 20}],
        [{"priceToEarningsRatio": 25}],
    ]
    requested_urls: list[str] = []

    class Response:
        def __init__(self, payload: list[dict[str, object]]) -> None:
            self._payload = payload

        def __enter__(self) -> "Response":
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def read(self) -> bytes:
            return json.dumps(self._payload).encode("utf-8")

    def fake_urlopen(url: str, timeout: int) -> Response:
        requested_urls.append(url)
        return Response(responses.pop(0))

    provider = FmpFundamentalsProvider("secret")
    with patch("src.infrastructure.market.fmp_adapter.urlopen", fake_urlopen):
        provider.fetch_fundamentals("aapl")

    paths = [urlparse(url).path for url in requested_urls]
    assert paths == [
        "/stable/profile",
        "/stable/income-statement",
        "/stable/ratios",
    ]
    for url in requested_urls:
        query = parse_qs(urlparse(url).query)
        assert query["symbol"] == ["AAPL"]
        assert query["apikey"] == ["secret"]


def test_fmp_adapter_raises_on_empty_response() -> None:
    provider = FmpFundamentalsProvider("secret")
    with patch(
        "src.infrastructure.market.fmp_adapter._get_json",
        side_effect=ValueError("empty response"),
    ):
        with pytest.raises(ProviderUnavailableError):
            provider.fetch_fundamentals("AAPL")


def test_alpha_vantage_adapter_normalizes_different_shape() -> None:
    provider = AlphaVantageFundamentalsProvider("secret")
    with patch(
        "src.infrastructure.market.alpha_vantage_adapter._get_json",
        side_effect=[
            {
                "Name": "Apple Inc.",
                "Sector": "Technology",
                "Industry": "Hardware",
                "PERatio": "25",
                "ReturnOnEquityTTM": "0.4",
            },
            {
                "annualReports": [
                    {
                        "fiscalDateEnding": "2025-12-31",
                        "totalRevenue": "100",
                        "netIncome": "20",
                    }
                ]
            },
        ],
    ):
        bundle = provider.fetch_fundamentals("AAPL")

    assert bundle.profile is not None
    assert bundle.profile.company_name == "Apple Inc."
    assert dict(bundle.statements[0].values)["net_income"] == 20


def test_alpha_vantage_adapter_uses_expected_functions() -> None:
    responses: list[dict[str, object]] = [
        {
            "Name": "Apple Inc.",
            "Sector": "Technology",
            "Industry": "Hardware",
            "PERatio": "25",
            "ReturnOnEquityTTM": "0.4",
        },
        {
            "annualReports": [
                {
                    "fiscalDateEnding": "2025-12-31",
                    "totalRevenue": "100",
                    "netIncome": "20",
                }
            ]
        },
    ]
    requested_urls: list[str] = []

    class Response:
        def __init__(self, payload: dict[str, object]) -> None:
            self._payload = payload

        def __enter__(self) -> "Response":
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def read(self) -> bytes:
            return json.dumps(self._payload).encode("utf-8")

    def fake_urlopen(url: str, timeout: int) -> Response:
        requested_urls.append(url)
        return Response(responses.pop(0))

    provider = AlphaVantageFundamentalsProvider("secret")
    with patch("src.infrastructure.market.alpha_vantage_adapter.urlopen", fake_urlopen):
        provider.fetch_fundamentals("aapl")

    queries = [parse_qs(urlparse(url).query) for url in requested_urls]
    assert [query["function"] for query in queries] == [
        ["OVERVIEW"],
        ["INCOME_STATEMENT"],
    ]
    for query in queries:
        assert query["symbol"] == ["AAPL"]
        assert query["apikey"] == ["secret"]


def test_alpha_vantage_adapter_returns_partial_overview_when_income_unavailable(
) -> None:
    provider = AlphaVantageFundamentalsProvider("secret")
    with patch(
        "src.infrastructure.market.alpha_vantage_adapter._get_json",
        side_effect=[
            {
                "Name": "Intel Corporation",
                "Sector": "Technology",
                "Industry": "Semiconductors",
                "PERatio": "None",
                "ReturnOnEquityTTM": "-0.0291",
                "LatestQuarter": "2026-03-31",
            },
            {"Information": "standard API call frequency is 5 calls per minute"},
        ],
    ):
        bundle = provider.fetch_fundamentals("intc")

    assert bundle.symbol == "INTC"
    assert bundle.profile is not None
    assert bundle.profile.company_name == "Intel Corporation"
    assert bundle.statements == ()
    assert bundle.ratios is not None
    ratios = dict(bundle.ratios.values)
    assert ratios["price_earnings"] is None
    assert ratios["return_on_equity"] == Decimal("-0.0291")
    assert bundle.data_as_of.isoformat() == "2026-03-31T00:00:00+00:00"


def test_alpha_vantage_adapter_raises_on_malformed_response() -> None:
    provider = AlphaVantageFundamentalsProvider("secret")
    with patch(
        "src.infrastructure.market.alpha_vantage_adapter._get_json",
        side_effect=[{}, {"annualReports": "bad"}],
    ):
        with pytest.raises(ProviderUnavailableError):
            provider.fetch_fundamentals("AAPL")


def test_alpha_vantage_adapter_reports_overview_payload_diagnostics() -> None:
    provider = AlphaVantageFundamentalsProvider("secret")
    with patch(
        "src.infrastructure.market.alpha_vantage_adapter._get_json",
        return_value={"Information": "Alpha Vantage rate limit"},
    ):
        with pytest.raises(ProviderUnavailableError) as exc_info:
            provider.fetch_fundamentals("AAPL")

    assert "OVERVIEW" in str(exc_info.value)
    assert "Name" in str(exc_info.value)
    assert "Information: Alpha Vantage rate limit" in str(exc_info.value)
