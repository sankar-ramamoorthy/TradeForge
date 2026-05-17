from src.domain.market.capability import (
    CapabilityPreference,
    ProviderCapability,
    ProviderDescriptor,
)
from src.domain.market.registry import ProviderRegistry


def test_registry_resolves_preferred_provider_when_configured() -> None:
    registry = ProviderRegistry(
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

    resolution = registry.resolve(ProviderCapability.FUNDAMENTALS)

    assert resolution.selected_provider_id == "fmp"
    assert resolution.used_fallback is False


def test_registry_resolves_fallback_when_preferred_is_not_configured() -> None:
    registry = ProviderRegistry(
        providers=(
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

    resolution = registry.resolve(ProviderCapability.FUNDAMENTALS)

    assert resolution.selected_provider_id == "alpha_vantage"
    assert resolution.used_fallback is True

