from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType

from src.domain.events import EntityReference, EventEnvelope, EventStore
from src.domain.lifecycle import DecisionLifecycleState, derive_lifecycle_state
from src.domain.personas import PersonaContext
from src.services.workspace_engine.contracts import (
    DEFAULT_WORKSPACE_STATE_CONTRACTS,
    WorkspaceStateAuthority,
    WorkspaceStateContract,
    WorkspaceStateContractCatalog,
)
from src.services.workspace_engine.routing import WorkspaceRouteId


class WorkspaceProjectionAuthority(StrEnum):
    DERIVED = "derived"


@dataclass(frozen=True, slots=True)
class WorkspaceProjectionContext:
    persona_id: str
    persona_version: str
    workspace_id: str
    workflow_id: str | None = None
    decision_id: str | None = None

    @classmethod
    def from_persona_context(
        cls,
        persona_context: PersonaContext,
    ) -> WorkspaceProjectionContext:
        return cls(
            persona_id=persona_context.persona_id,
            persona_version=persona_context.persona_version,
            workspace_id=persona_context.workspace_id,
            workflow_id=persona_context.workflow_id,
            decision_id=persona_context.decision_id,
        )


@dataclass(frozen=True, slots=True)
class WorkspaceSourceEventReference:
    event_type: str
    timestamp_iso: str
    entity_references: tuple[EntityReference, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "entity_references",
            tuple(self.entity_references),
        )

    @classmethod
    def from_event(
        cls,
        event: EventEnvelope,
    ) -> WorkspaceSourceEventReference:
        return cls(
            event_type=event.event_type,
            timestamp_iso=event.timestamp.isoformat(),
            entity_references=event.entity_references,
        )


@dataclass(frozen=True, slots=True)
class WorkspaceProjectionField:
    name: str
    authority: WorkspaceStateAuthority
    source_inputs: tuple[str, ...]
    source_events: tuple[WorkspaceSourceEventReference, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "source_inputs", tuple(self.source_inputs))
        object.__setattr__(self, "source_events", tuple(self.source_events))

    @property
    def source_event_count(self) -> int:
        return len(self.source_events)

    @property
    def source_event_types(self) -> tuple[str, ...]:
        return tuple(event.event_type for event in self.source_events)


@dataclass(frozen=True, slots=True)
class WorkspaceProjection:
    route_id: WorkspaceRouteId
    authority: WorkspaceProjectionAuthority
    context: WorkspaceProjectionContext
    operational_question: str
    lifecycle_state: DecisionLifecycleState | None
    source_events: tuple[WorkspaceSourceEventReference, ...]
    fields: Mapping[str, WorkspaceProjectionField]
    authority_boundaries: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "source_events", tuple(self.source_events))
        object.__setattr__(self, "fields", MappingProxyType(dict(self.fields)))
        object.__setattr__(
            self,
            "authority_boundaries",
            tuple(self.authority_boundaries),
        )

    @property
    def source_event_count(self) -> int:
        return len(self.source_events)

    @property
    def source_event_types(self) -> tuple[str, ...]:
        return tuple(event.event_type for event in self.source_events)


@dataclass(frozen=True, slots=True)
class WorkspaceProjectionSet:
    authority: WorkspaceProjectionAuthority
    context: WorkspaceProjectionContext
    projections: Mapping[WorkspaceRouteId, WorkspaceProjection]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "projections",
            MappingProxyType(dict(self.projections)),
        )


class WorkspaceProjectionProjector:
    def __init__(
        self,
        route_id: WorkspaceRouteId | str,
        persona_context: PersonaContext,
        contract_catalog: WorkspaceStateContractCatalog | None = None,
    ) -> None:
        self._route_id = WorkspaceRouteId(route_id)
        self._projection_context = WorkspaceProjectionContext.from_persona_context(
            persona_context,
        )
        self._contract_catalog = contract_catalog or WorkspaceStateContractCatalog()

    def project(self, events: tuple[EventEnvelope, ...]) -> WorkspaceProjection:
        contract = self._contract_catalog.contract_for(self._route_id)
        scoped_events = _scope_events(events, self._projection_context)
        source_events = tuple(
            event
            for event in scoped_events
            if _matches_any_input(event.event_type, contract.required_event_inputs)
        )

        return _build_projection(
            contract=contract,
            context=self._projection_context,
            scoped_events=scoped_events,
            source_events=source_events,
        )


class WorkspaceProjectionSetProjector:
    def __init__(
        self,
        persona_context: PersonaContext,
        contract_catalog: WorkspaceStateContractCatalog | None = None,
    ) -> None:
        self._projection_context = WorkspaceProjectionContext.from_persona_context(
            persona_context,
        )
        self._contract_catalog = contract_catalog or WorkspaceStateContractCatalog()

    def project(self, events: tuple[EventEnvelope, ...]) -> WorkspaceProjectionSet:
        scoped_events = _scope_events(events, self._projection_context)
        projections = {
            route_id: _build_projection(
                contract=contract,
                context=self._projection_context,
                scoped_events=scoped_events,
                source_events=tuple(
                    event
                    for event in scoped_events
                    if _matches_any_input(
                        event.event_type,
                        contract.required_event_inputs,
                    )
                ),
            )
            for route_id, contract in self._contract_catalog.contracts.items()
        }

        return WorkspaceProjectionSet(
            authority=WorkspaceProjectionAuthority.DERIVED,
            context=self._projection_context,
            projections=projections,
        )


class WorkspaceProjectionReadService:
    def __init__(
        self,
        event_store: EventStore,
        contract_catalog: WorkspaceStateContractCatalog | None = None,
    ) -> None:
        self._event_store = event_store
        self._contract_catalog = contract_catalog or WorkspaceStateContractCatalog()

    def projection_for(
        self,
        route_id: WorkspaceRouteId | str,
        persona_context: PersonaContext,
    ) -> WorkspaceProjection:
        projector = WorkspaceProjectionProjector(
            route_id=route_id,
            persona_context=persona_context,
            contract_catalog=self._contract_catalog,
        )
        return projector.project(self._event_store.read_events())

    def all_projections(
        self,
        persona_context: PersonaContext,
    ) -> WorkspaceProjectionSet:
        projector = WorkspaceProjectionSetProjector(
            persona_context=persona_context,
            contract_catalog=self._contract_catalog,
        )
        return projector.project(self._event_store.read_events())


def _build_projection(
    contract: WorkspaceStateContract,
    context: WorkspaceProjectionContext,
    scoped_events: tuple[EventEnvelope, ...],
    source_events: tuple[EventEnvelope, ...],
) -> WorkspaceProjection:
    fields = {
        field.name: WorkspaceProjectionField(
            name=field.name,
            authority=field.authority,
            source_inputs=field.source_inputs,
            source_events=tuple(
                WorkspaceSourceEventReference.from_event(event)
                for event in scoped_events
                if _matches_any_input(event.event_type, field.source_inputs)
            ),
        )
        for field in contract.state_fields
    }

    return WorkspaceProjection(
        route_id=contract.route_id,
        authority=WorkspaceProjectionAuthority.DERIVED,
        context=context,
        operational_question=contract.operational_question,
        lifecycle_state=derive_lifecycle_state(scoped_events),
        source_events=tuple(
            WorkspaceSourceEventReference.from_event(event) for event in source_events
        ),
        fields=fields,
        authority_boundaries=contract.authority_boundaries,
    )


def _scope_events(
    events: Iterable[EventEnvelope],
    context: WorkspaceProjectionContext,
) -> tuple[EventEnvelope, ...]:
    return tuple(event for event in events if _matches_context(event, context))


def _matches_context(
    event: EventEnvelope,
    context: WorkspaceProjectionContext,
) -> bool:
    if event.persona_id != context.persona_id:
        return False

    if event.workspace_id not in (None, context.workspace_id):
        return False

    if context.decision_id is not None and not _event_references_entity(
        event,
        entity_type="decision",
        entity_id=context.decision_id,
    ):
        return False

    if context.workflow_id is not None and not _event_matches_workflow(
        event,
        context.workflow_id,
    ):
        return False

    return True


def _event_matches_workflow(event: EventEnvelope, workflow_id: str) -> bool:
    return (
        _event_references_entity(
            event,
            entity_type="workflow",
            entity_id=workflow_id,
        )
        or event.payload.get("workflow_id") == workflow_id
        or event.provenance.get("workflow_id") == workflow_id
    )


def _event_references_entity(
    event: EventEnvelope,
    entity_type: str,
    entity_id: str,
) -> bool:
    return any(
        reference.entity_type == entity_type and reference.entity_id == entity_id
        for reference in event.entity_references
    )


def _matches_any_input(event_type: str, source_inputs: tuple[str, ...]) -> bool:
    return any(
        _matches_input(event_type, source_input) for source_input in source_inputs
    )


def _matches_input(event_type: str, source_input: str) -> bool:
    if source_input.endswith(".*"):
        return event_type.startswith(source_input[:-1])

    return event_type == source_input


DEFAULT_WORKSPACE_PROJECTION_SET_PROJECTOR = WorkspaceProjectionSetProjector
DEFAULT_WORKSPACE_PROJECTION_CONTRACTS = DEFAULT_WORKSPACE_STATE_CONTRACTS
