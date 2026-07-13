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
            company_name = _required_overview_name(overview)
        except Exception as exc:
            raise ProviderUnavailableError(
                _PROVIDER_ID, upper_symbol, _payload_failure("OVERVIEW", exc)
            ) from exc

        income_row: dict[str, object] | None = None
        try:
            income = _get_json(
                {
                    "function": "INCOME_STATEMENT",
                    "symbol": upper_symbol,
                    "apikey": self._api_key,
                }
            )
            income_row = _first_annual_report(income)
        except Exception:
            income_row = None

        data_as_of = (
            _parse_date(income_row.get("fiscalDateEnding"))
            if income_row is not None
            else _parse_optional_date(overview.get("LatestQuarter"), fetched_at)
        )
        provenance = ProviderProvenance(
            provider_id=_PROVIDER_ID,
            provider_version=self.provider_version,
            fetched_at=fetched_at,
            data_as_of=data_as_of,
        )
        statements: tuple[FinancialStatement, ...] = ()
        if income_row is not None:
            statements = (
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
            )

        return FundamentalsBundle(
            symbol=upper_symbol,
            profile=CompanyProfile(
                symbol=upper_symbol,
                company_name=company_name,
                sector=_optional_str(overview.get("Sector")),
                industry=_optional_str(overview.get("Industry")),
                provenance=provenance,
            ),
            statements=statements,
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


def _first_annual_report(payload: dict[str, object]) -> dict[str, object]:
    annual_reports = payload.get("annualReports")
    if not isinstance(annual_reports, list) or not annual_reports:
        raise ValueError(_malformed_payload("INCOME_STATEMENT", payload))
    income_row = annual_reports[0]
    if not isinstance(income_row, dict):
        raise ValueError("INCOME_STATEMENT annualReports row must be an object")
    return income_row


def _parse_date(value: object) -> datetime:
    if not isinstance(value, str):
        raise ValueError("missing statement date")
    return datetime.fromisoformat(value).replace(tzinfo=UTC)


def _parse_optional_date(value: object, fallback: datetime) -> datetime:
    if not isinstance(value, str) or not value.strip():
        return fallback
    try:
        return _parse_date(value)
    except ValueError:
        return fallback


def _required_overview_name(payload: dict[str, object]) -> str:
    try:
        return _required_str(payload.get("Name"), "OVERVIEW", "Name")
    except ValueError as exc:
        upstream_message = _upstream_message(payload)
        if upstream_message is not None:
            raise ValueError(f"{exc}; {upstream_message}") from exc
        raise


def _required_str(value: object, function_name: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{function_name} missing required field {field_name}")
    return value


def _optional_decimal(value: object) -> Decimal | None:
    return None if value in (None, "None", "-") else Decimal(str(value))


def _optional_str(value: object) -> str | None:
    return None if value is None else str(value)


def _payload_failure(function_name: str, exc: Exception) -> str:
    return str(exc) if function_name in str(exc) else f"{function_name}: {exc}"


def _malformed_payload(function_name: str, payload: dict[str, object]) -> str:
    upstream_message = _upstream_message(payload)
    if upstream_message is not None:
        return f"{function_name} returned {upstream_message}"
    keys = ", ".join(sorted(str(key) for key in payload.keys()))
    return f"{function_name} response missing annualReports; keys: {keys or 'none'}"


def _upstream_message(payload: dict[str, object]) -> str | None:
    for field_name in ("Error Message", "Information", "Note"):
        message = payload.get(field_name)
        if isinstance(message, str) and message.strip():
            return f"{field_name}: {message}"
    return None
