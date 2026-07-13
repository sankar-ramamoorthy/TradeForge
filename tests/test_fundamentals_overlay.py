from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from src.app.api.application import create_app
from src.domain.market.capability import (
    CapabilityPreference,
    ProviderCapability,
    ProviderDescriptor,
)
from src.domain.market.fundamentals import (
    CompanyProfile,
    FinancialRatios,
    FinancialStatement,
    FundamentalsBundle,
)
from src.domain.market.registry import ProviderRegistry
from src.domain.market.snapshot import ProviderProvenance
from src.services.market.fundamentals_service import FundamentalsService

_TS = datetime(2026, 5, 16, 20, 0, tzinfo=UTC)


def test_fundamentals_overlay_returns_advisory_bundle() -> None:
    provenance = ProviderProvenance("fmp", "test", _TS, _TS)
    provider = MagicMock()
    provider.fetch_fundamentals.return_value = FundamentalsBundle(
        symbol="AAPL",
        profile=CompanyProfile(
            "AAPL", "Apple Inc.", "Technology", "Hardware", provenance
        ),
        statements=(
            FinancialStatement(
                "AAPL",
                "income",
                _TS,
                (("revenue", Decimal("100")), ("net_income", Decimal("20"))),
                provenance,
            ),
        ),
        ratios=FinancialRatios(
            "AAPL",
            (("price_earnings", Decimal("25")), ("return_on_equity", Decimal("0.4"))),
            provenance,
        ),
        provenance=provenance,
    )
    registry = ProviderRegistry(
        (ProviderDescriptor("fmp", (ProviderCapability.FUNDAMENTALS,)),),
        (CapabilityPreference(ProviderCapability.FUNDAMENTALS, "fmp"),),
    )
    client = TestClient(
        create_app(
            provider_registry=registry,
            fundamentals_service=FundamentalsService(registry, {"fmp": provider}),
        )
    )

    response = client.get("/workspaces/fundamentals-context?symbol=AAPL")

    assert response.status_code == 200
    data = response.json()
    assert data["authority"] == "advisory"
    assert data["selected_provider_id"] == "fmp"
    assert data["attempts"][0]["provider_id"] == "fmp"
    assert data["attempts"][0]["outcome"] == "success"
    assert data["company_name"] == "Apple Inc."
    assert data["revenue"] == "100"


def test_fundamentals_overlay_returns_available_partial_bundle() -> None:
    provenance = ProviderProvenance("alpha_vantage", "test", _TS, _TS)
    provider = MagicMock()
    provider.fetch_fundamentals.return_value = FundamentalsBundle(
        symbol="INTC",
        profile=CompanyProfile(
            "INTC", "Intel Corporation", "Technology", "Semiconductors", provenance
        ),
        statements=(),
        ratios=FinancialRatios(
            "INTC",
            (("price_earnings", None), ("return_on_equity", Decimal("-0.0291"))),
            provenance,
        ),
        provenance=provenance,
    )
    registry = ProviderRegistry(
        (ProviderDescriptor("alpha_vantage", (ProviderCapability.FUNDAMENTALS,)),),
        (CapabilityPreference(ProviderCapability.FUNDAMENTALS, "alpha_vantage"),),
    )
    client = TestClient(
        create_app(
            provider_registry=registry,
            fundamentals_service=FundamentalsService(
                registry, {"alpha_vantage": provider}
            ),
        )
    )

    response = client.get(
        "/workspaces/fundamentals-context?symbol=INTC&instrument_kind=equity"
    )

    assert response.status_code == 200
    data = response.json()
    assert data["coverage_status"] == "available"
    assert data["selected_provider_id"] == "alpha_vantage"
    assert data["company_name"] == "Intel Corporation"
    assert data["sector"] == "Technology"
    assert data["revenue"] is None
    assert data["net_income"] is None
    assert data["return_on_equity"] == "-0.0291"


def test_provider_configuration_exposes_capability_resolution() -> None:
    registry = ProviderRegistry(
        (
            ProviderDescriptor("fmp", (ProviderCapability.FUNDAMENTALS,)),
            ProviderDescriptor("alpha_vantage", (ProviderCapability.FUNDAMENTALS,)),
        ),
        (
            CapabilityPreference(
                ProviderCapability.FUNDAMENTALS,
                "fmp",
                ("alpha_vantage",),
            ),
            CapabilityPreference(ProviderCapability.PRICE, "yfinance"),
        ),
    )
    client = TestClient(create_app(provider_registry=registry))

    response = client.get("/workspaces/provider-configuration")

    assert response.status_code == 200
    data = response.json()
    fundamentals = next(
        item for item in data["resolutions"] if item["capability"] == "fundamentals"
    )
    assert fundamentals["preferred_provider_id"] == "fmp"
    assert fundamentals["fallback_provider_ids"] == ["alpha_vantage"]


def test_etf_request_reports_semantic_mismatch_instead_of_provider_failure() -> None:
    client = TestClient(create_app())

    response = client.get(
        "/workspaces/fundamentals-context?symbol=EWY&instrument_kind=etf"
    )

    assert response.status_code == 200
    data = response.json()
    assert data["instrument_kind"] == "etf"
    assert data["requested_context_type"] == "company_fundamentals"
    assert data["coverage_status"] == "unsupported"
    assert data["alternative_context_type"] == "etf_context"
    assert data["attempted_provider_ids"] == []
