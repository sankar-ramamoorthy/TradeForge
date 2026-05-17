from __future__ import annotations

import json
from datetime import UTC, datetime
from decimal import Decimal
from urllib.parse import urlencode
from urllib.request import urlopen

from src.domain.market.fundamentals import (
    CompanyProfile,
    FinancialRatios,
    FinancialStatement,
    FundamentalsBundle,
)
from src.domain.market.provider import ProviderUnavailableError
from src.domain.market.snapshot import ProviderProvenance

_PROVIDER_ID = "alpha_vantage"


class AlphaVantageFundamentalsProvider:
    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    @property
    def provider_id(self) -> str:
        return _PROVIDER_ID

    @property
    def provider_version(self) -> str:
        return "v1"

    def fetch_fundamentals(self, symbol: str) -> FundamentalsBundle:
        upper_symbol = symbol.upper()
        fetched_at = datetime.now(UTC)
        try:
            overview = _get_json(
                {
                    "function": "OVERVIEW",
                    "symbol": upper_symbol,
                    "apikey": self._api_key,
                }
            )
            income = _get_json(
                {
                    "function": "INCOME_STATEMENT",
                    "symbol": upper_symbol,
                    "apikey": self._api_key,
                }
            )
            annual_reports = income["annualReports"]
            if not isinstance(annual_reports, list):
                raise ValueError("annualReports must be a list")
            income_row = annual_reports[0]
            if not isinstance(income_row, dict):
                raise ValueError("annual report row must be an object")
        except Exception as exc:
            raise ProviderUnavailableError(
                _PROVIDER_ID, upper_symbol, str(exc)
            ) from exc

        data_as_of = _parse_date(income_row.get("fiscalDateEnding"))
        provenance = ProviderProvenance(
            provider_id=_PROVIDER_ID,
            provider_version=self.provider_version,
            fetched_at=fetched_at,
            data_as_of=data_as_of,
        )
        return FundamentalsBundle(
            symbol=upper_symbol,
            profile=CompanyProfile(
                symbol=upper_symbol,
                company_name=str(overview["Name"]),
                sector=_optional_str(overview.get("Sector")),
                industry=_optional_str(overview.get("Industry")),
                provenance=provenance,
            ),
            statements=(
                FinancialStatement(
                    symbol=upper_symbol,
                    statement_type="income",
                    period_end=data_as_of,
                    values=(
                        ("revenue", _optional_decimal(income_row.get("totalRevenue"))),
                        ("net_income", _optional_decimal(income_row.get("netIncome"))),
                    ),
                    provenance=provenance,
                ),
            ),
            ratios=FinancialRatios(
                symbol=upper_symbol,
                values=(
                    ("price_earnings", _optional_decimal(overview.get("PERatio"))),
                    (
                        "return_on_equity",
                        _optional_decimal(overview.get("ReturnOnEquityTTM")),
                    ),
                ),
                provenance=provenance,
            ),
            provenance=provenance,
        )


def _get_json(params: dict[str, str]) -> dict[str, object]:
    url = f"https://www.alphavantage.co/query?{urlencode(params)}"
    with urlopen(url, timeout=10) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, dict) or not payload:
        raise ValueError("empty response")
    return payload


def _parse_date(value: object) -> datetime:
    if not isinstance(value, str):
        raise ValueError("missing statement date")
    return datetime.fromisoformat(value).replace(tzinfo=UTC)


def _optional_decimal(value: object) -> Decimal | None:
    return None if value in (None, "None") else Decimal(str(value))


def _optional_str(value: object) -> str | None:
    return None if value is None else str(value)
