from unittest.mock import patch

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
            [{"priceEarningsRatio": 25, "returnOnEquity": 0.4}],
        ],
    ):
        bundle = provider.fetch_fundamentals("aapl")

    assert bundle.symbol == "AAPL"
    assert bundle.profile is not None
    assert bundle.profile.company_name == "Apple Inc."
    assert dict(bundle.statements[0].values)["revenue"] == 100
    assert dict(bundle.ratios.values)["price_earnings"] == 25  # type: ignore[union-attr]


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


def test_alpha_vantage_adapter_raises_on_malformed_response() -> None:
    provider = AlphaVantageFundamentalsProvider("secret")
    with patch(
        "src.infrastructure.market.alpha_vantage_adapter._get_json",
        side_effect=[{}, {"annualReports": "bad"}],
    ):
        with pytest.raises(ProviderUnavailableError):
            provider.fetch_fundamentals("AAPL")
