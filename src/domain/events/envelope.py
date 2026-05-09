from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from types import MappingProxyType
from typing import Any

from src.domain.events.taxonomy import CANONICAL_EVENT_DOMAINS, EventDomain


@dataclass(frozen=True, slots=True)
class EntityReference:
    entity_type: str
    entity_id: str


@dataclass(frozen=True, slots=True)
class EventEnvelope:
    event_type: str
    timestamp: datetime
    persona_id: str
    workspace_id: str | None = None
    entity_references: tuple[EntityReference, ...] = ()
    payload: Mapping[str, Any] = field(default_factory=dict)
    provenance: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        domain = self.event_type.split(".", maxsplit=1)[0]
        if domain not in CANONICAL_EVENT_DOMAINS:
            allowed_domains = ", ".join(sorted(CANONICAL_EVENT_DOMAINS))
            raise ValueError(
                f"event_type must use a canonical domain prefix: {allowed_domains}"
            )

        object.__setattr__(
            self,
            "entity_references",
            tuple(self.entity_references),
        )
        object.__setattr__(self, "payload", MappingProxyType(dict(self.payload)))
        object.__setattr__(
            self,
            "provenance",
            MappingProxyType(dict(self.provenance)),
        )

    @property
    def event_domain(self) -> EventDomain:
        domain = self.event_type.split(".", maxsplit=1)[0]
        return EventDomain(domain)
