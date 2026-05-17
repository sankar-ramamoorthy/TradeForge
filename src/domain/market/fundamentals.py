from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from src.domain.market.snapshot import ProviderProvenance, _require_non_empty


@dataclass(frozen=True, slots=True)
class CompanyProfile:
    symbol: str
    company_name: str
    sector: str | None
    industry: str | None
    provenance: ProviderProvenance

    def __post_init__(self) -> None:
        _require_non_empty(self.symbol, "symbol")
        _require_non_empty(self.company_name, "company_name")

    @property
    def data_as_of(self) -> datetime:
        return self.provenance.data_as_of

    @property
    def is_advisory(self) -> bool:
        return True


@dataclass(frozen=True, slots=True)
class FinancialStatement:
    symbol: str
    statement_type: str
    period_end: datetime
    values: tuple[tuple[str, Decimal | None], ...]
    provenance: ProviderProvenance

    def __post_init__(self) -> None:
        _require_non_empty(self.symbol, "symbol")
        _require_non_empty(self.statement_type, "statement_type")
        object.__setattr__(self, "values", tuple(self.values))

    @property
    def data_as_of(self) -> datetime:
        return self.provenance.data_as_of

    @property
    def is_advisory(self) -> bool:
        return True


@dataclass(frozen=True, slots=True)
class FinancialRatios:
    symbol: str
    values: tuple[tuple[str, Decimal | None], ...]
    provenance: ProviderProvenance

    def __post_init__(self) -> None:
        _require_non_empty(self.symbol, "symbol")
        object.__setattr__(self, "values", tuple(self.values))

    @property
    def data_as_of(self) -> datetime:
        return self.provenance.data_as_of

    @property
    def is_advisory(self) -> bool:
        return True


@dataclass(frozen=True, slots=True)
class FundamentalsBundle:
    symbol: str
    profile: CompanyProfile | None
    statements: tuple[FinancialStatement, ...]
    ratios: FinancialRatios | None
    provenance: ProviderProvenance

    def __post_init__(self) -> None:
        _require_non_empty(self.symbol, "symbol")
        object.__setattr__(self, "statements", tuple(self.statements))

    @property
    def data_as_of(self) -> datetime:
        return self.provenance.data_as_of

    @property
    def provider_id(self) -> str:
        return self.provenance.provider_id

    @property
    def is_advisory(self) -> bool:
        return True

