from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ProviderCapability(StrEnum):
    PRICE = "price"
    FUNDAMENTALS = "fundamentals"


@dataclass(frozen=True, slots=True)
class ProviderDescriptor:
    provider_id: str
    capabilities: tuple[ProviderCapability, ...]

    def __post_init__(self) -> None:
        if not self.provider_id.strip():
            raise ValueError("provider_id must not be empty")
        if not self.capabilities:
            raise ValueError("capabilities must not be empty")
        object.__setattr__(self, "capabilities", tuple(self.capabilities))


@dataclass(frozen=True, slots=True)
class CapabilityPreference:
    capability: ProviderCapability
    preferred_provider_id: str
    fallback_provider_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.preferred_provider_id.strip():
            raise ValueError("preferred_provider_id must not be empty")
        object.__setattr__(
            self,
            "fallback_provider_ids",
            tuple(self.fallback_provider_ids),
        )

    @property
    def resolution_order(self) -> tuple[str, ...]:
        return (self.preferred_provider_id, *self.fallback_provider_ids)


@dataclass(frozen=True, slots=True)
class CapabilityResolution:
    capability: ProviderCapability
    configured_provider_ids: tuple[str, ...]
    selected_provider_id: str | None
    preferred_provider_id: str
    fallback_provider_ids: tuple[str, ...]

    @property
    def used_fallback(self) -> bool:
        return (
            self.selected_provider_id is not None
            and self.selected_provider_id != self.preferred_provider_id
        )

    @property
    def is_available(self) -> bool:
        return self.selected_provider_id is not None

