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

_PROVIDER_ID = "fmp"


class FmpFundamentalsProvider:
    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    @property
    def provider_id(self) -> str:
        return _PROVIDER_ID

    @property
    def provider_version(self) -> str:
        return "v3"

    def fetch_fundamentals(self, symbol: str) -> FundamentalsBundle:
        upper_symbol = symbol.upper()
        fetched_at = datetime.now(UTC)
        try:
            profile_data = _get_json(
                f"https://financialmodelingprep.com/api/v3/profile/{upper_symbol}",
                self._api_key,
            )
            income_data = _get_json(
                f"https://financialmodelingprep.com/api/v3/income-statement/{upper_symbol}",
                self._api_key,
            )
            ratios_data = _get_json(
                f"https://financialmodelingprep.com/api/v3/ratios/{upper_symbol}",
                self._api_key,
            )
            profile_row = profile_data[0]
            income_row = income_data[0]
            ratios_row = ratios_data[0]
        except Exception as exc:
            raise ProviderUnavailableError(
                _PROVIDER_ID, upper_symbol, str(exc)
            ) from exc

        data_as_of = _parse_date(income_row.get("date"))
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
                company_name=str(profile_row["companyName"]),
                sector=_optional_str(profile_row.get("sector")),
                industry=_optional_str(profile_row.get("industry")),
                provenance=provenance,
            ),
            statements=(
                FinancialStatement(
                    symbol=upper_symbol,
                    statement_type="income",
                    period_end=data_as_of,
                    values=(
                        ("revenue", _optional_decimal(income_row.get("revenue"))),
                        ("net_income", _optional_decimal(income_row.get("netIncome"))),
                    ),
                    provenance=provenance,
                ),
            ),
            ratios=FinancialRatios(
                symbol=upper_symbol,
                values=(
                    (
                        "price_earnings",
                        _optional_decimal(ratios_row.get("priceEarningsRatio")),
                    ),
                    (
                        "return_on_equity",
                        _optional_decimal(ratios_row.get("returnOnEquity")),
                    ),
                ),
                provenance=provenance,
            ),
            provenance=provenance,
        )


def _get_json(url: str, api_key: str) -> list[dict[str, object]]:
    with urlopen(f"{url}?{urlencode({'apikey': api_key})}", timeout=10) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, list) or not payload:
        raise ValueError("empty response")
    return payload


def _parse_date(value: object) -> datetime:
    if not isinstance(value, str):
        raise ValueError("missing statement date")
    return datetime.fromisoformat(value).replace(tzinfo=UTC)


def _optional_decimal(value: object) -> Decimal | None:
    return None if value is None else Decimal(str(value))


def _optional_str(value: object) -> str | None:
    return None if value is None else str(value)
