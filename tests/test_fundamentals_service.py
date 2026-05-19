from datetime import UTC, datetime
from unittest.mock import MagicMock

from src.domain.market.capability import (
    CapabilityPreference,
    ProviderCapability,
    ProviderDescriptor,
)
from src.domain.market.fundamentals import FundamentalsBundle
from src.domain.market.provider import ProviderUnavailableError
from src.domain.market.registry import ProviderRegistry
from src.domain.market.snapshot import ProviderProvenance
from src.services.market.fundamentals_service import FundamentalsService

_TS = datetime(2026, 5, 16, 20, 0, tzinfo=UTC)


def _bundle(provider_id: str) -> FundamentalsBundle:
    provenance = ProviderProvenance(provider_id, "test", _TS, _TS)
    return FundamentalsBundle("AAPL", None, (), None, provenance)


def _registry() -> ProviderRegistry:
    return ProviderRegistry(
        providers=(
            ProviderDescriptor("fmp", (ProviderCapability.FUNDAMENTALS,)),
            ProviderDescriptor("alpha_vantage", (ProviderCapability.FUNDAMENTALS,)),
        ),
        preferences=(
            CapabilityPreference(
                ProviderCapability.FUNDAMENTALS,
                "fmp",
                ("alpha_vantage",),
            ),
        ),
    )


def test_fundamentals_service_uses_primary_provider_first() -> None:
    fmp = MagicMock()
    fmp.fetch_fundamentals.return_value = _bundle("fmp")
    alpha = MagicMock()
    service = FundamentalsService(_registry(), {"fmp": fmp, "alpha_vantage": alpha})

    result = service.fetch("AAPL")

    assert result.selected_provider_id == "fmp"
    assert result.used_fallback is False
    assert tuple(attempt.provider_id for attempt in result.attempts) == ("fmp",)
    assert tuple(attempt.outcome for attempt in result.attempts) == ("success",)
    alpha.fetch_fundamentals.assert_not_called()


def test_fundamentals_service_uses_ordered_fallback_after_failure() -> None:
    fmp = MagicMock()
    fmp.fetch_fundamentals.side_effect = ProviderUnavailableError("fmp", "AAPL", "down")
    alpha = MagicMock()
    alpha.fetch_fundamentals.return_value = _bundle("alpha_vantage")
    service = FundamentalsService(_registry(), {"fmp": fmp, "alpha_vantage": alpha})

    result = service.fetch("AAPL")

    assert result.selected_provider_id == "alpha_vantage"
    assert result.used_fallback is True
    assert result.error_reasons == ("fmp: down",)
    assert tuple(attempt.provider_id for attempt in result.attempts) == (
        "fmp",
        "alpha_vantage",
    )
    assert tuple(attempt.outcome for attempt in result.attempts) == (
        "failure",
        "success",
    )
