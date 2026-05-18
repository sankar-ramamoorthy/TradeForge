from __future__ import annotations

from enum import StrEnum


class InstrumentKind(StrEnum):
    EQUITY = "equity"
    ETF = "etf"
    UNKNOWN = "unknown"


class ExternalContextType(StrEnum):
    COMPANY_FUNDAMENTALS = "company_fundamentals"
    ETF_CONTEXT = "etf_context"
