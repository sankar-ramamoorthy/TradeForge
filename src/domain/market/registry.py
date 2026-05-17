from __future__ import annotations

from collections.abc import Mapping

from src.domain.market.capability import (
    CapabilityPreference,
    CapabilityResolution,
    ProviderCapability,
    ProviderDescriptor,
)


class ProviderRegistry:
    """Composition-time catalog for configured providers and capabilities."""

    def __init__(
        self,
        providers: tuple[ProviderDescriptor, ...],
        preferences: tuple[CapabilityPreference, ...],
    ) -> None:
        self._providers = {provider.provider_id: provider for provider in providers}
        self._preferences = {item.capability: item for item in preferences}

    @property
    def providers(self) -> tuple[ProviderDescriptor, ...]:
        return tuple(self._providers.values())

    @property
    def preferences(self) -> Mapping[ProviderCapability, CapabilityPreference]:
        return self._preferences

    def providers_for(
        self, capability: ProviderCapability
    ) -> tuple[ProviderDescriptor, ...]:
        return tuple(
            provider
            for provider in self._providers.values()
            if capability in provider.capabilities
        )

    def resolve(self, capability: ProviderCapability) -> CapabilityResolution:
        preference = self._preferences[capability]
        configured = tuple(
            provider.provider_id for provider in self.providers_for(capability)
        )
        selected = next(
            (
                provider_id
                for provider_id in preference.resolution_order
                if provider_id in configured
            ),
            None,
        )
        return CapabilityResolution(
            capability=capability,
            configured_provider_ids=configured,
            selected_provider_id=selected,
            preferred_provider_id=preference.preferred_provider_id,
            fallback_provider_ids=preference.fallback_provider_ids,
        )

    def set_preference(
        self,
        capability: ProviderCapability,
        preferred_provider_id: str,
        fallback_provider_ids: tuple[str, ...],
    ) -> None:
        self._preferences[capability] = CapabilityPreference(
            capability,
            preferred_provider_id,
            fallback_provider_ids,
        )
