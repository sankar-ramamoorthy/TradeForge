from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from urllib.parse import urlencode


class WorkspaceRouteId(StrEnum):
    OPERATING = "operating"
    OPPORTUNITY = "opportunity"
    CONTEXT_WORKBENCH = "context-workbench"
    PLAN_REVIEW = "plan-review"
    ACTIVE_POSITION = "active-position"
    REPLAY = "replay"
    REVIEW = "review"
    MARKET_CONTEXT = "market-context"
    PLAYBOOKS_DOCTRINE = "playbooks-doctrine"


@dataclass(frozen=True, slots=True)
class WorkspaceRouteDefinition:
    route_id: WorkspaceRouteId
    name: str
    path: str
    operational_question: str


@dataclass(frozen=True, slots=True)
class WorkspaceRouteContext:
    persona_id: str
    selected_workflow_id: str | None = None
    decision_id: str | None = None

    def __post_init__(self) -> None:
        if not self.persona_id.strip():
            raise ValueError("persona_id is required for workspace routing")


@dataclass(frozen=True, slots=True)
class WorkspaceRoute:
    definition: WorkspaceRouteDefinition
    context: WorkspaceRouteContext
    entrypoint: str

    @property
    def route_id(self) -> WorkspaceRouteId:
        return self.definition.route_id


class UnknownWorkspaceRouteError(ValueError):
    pass


DEFAULT_WORKSPACE_ROUTE_DEFINITIONS: Mapping[
    WorkspaceRouteId,
    WorkspaceRouteDefinition,
] = MappingProxyType(
    {
        WorkspaceRouteId.OPERATING: WorkspaceRouteDefinition(
            route_id=WorkspaceRouteId.OPERATING,
            name="Operating Workspace",
            path="/workspaces/operating",
            operational_question="What requires operational attention now?",
        ),
        WorkspaceRouteId.OPPORTUNITY: WorkspaceRouteDefinition(
            route_id=WorkspaceRouteId.OPPORTUNITY,
            name="Opportunity Workspace",
            path="/workspaces/opportunity",
            operational_question="What candidate decisions are developing?",
        ),
        WorkspaceRouteId.CONTEXT_WORKBENCH: WorkspaceRouteDefinition(
            route_id=WorkspaceRouteId.CONTEXT_WORKBENCH,
            name="Context Workbench",
            path="/workspaces/context-workbench",
            operational_question=(
                "What do I need to know about this instrument before deciding "
                "how to interpret it?"
            ),
        ),
        WorkspaceRouteId.PLAN_REVIEW: WorkspaceRouteDefinition(
            route_id=WorkspaceRouteId.PLAN_REVIEW,
            name="Plan Review Workspace",
            path="/workspaces/plan-review",
            operational_question="What risk is being intentionally authorized?",
        ),
        WorkspaceRouteId.ACTIVE_POSITION: WorkspaceRouteDefinition(
            route_id=WorkspaceRouteId.ACTIVE_POSITION,
            name="Active Position Workspace",
            path="/workspaces/active-position",
            operational_question="What current exposure requires supervision?",
        ),
        WorkspaceRouteId.REPLAY: WorkspaceRouteDefinition(
            route_id=WorkspaceRouteId.REPLAY,
            name="Replay Workspace",
            path="/workspaces/replay",
            operational_question="What historical context must be reconstructed?",
        ),
        WorkspaceRouteId.REVIEW: WorkspaceRouteDefinition(
            route_id=WorkspaceRouteId.REVIEW,
            name="Review Workspace",
            path="/workspaces/review",
            operational_question="What should be learned from the decision?",
        ),
        WorkspaceRouteId.MARKET_CONTEXT: WorkspaceRouteDefinition(
            route_id=WorkspaceRouteId.MARKET_CONTEXT,
            name="Market Context Workspace",
            path="/workspaces/market-context",
            operational_question="What contextual conditions shape interpretation?",
        ),
        WorkspaceRouteId.PLAYBOOKS_DOCTRINE: WorkspaceRouteDefinition(
            route_id=WorkspaceRouteId.PLAYBOOKS_DOCTRINE,
            name="Playbooks / Doctrine Workspace",
            path="/workspaces/playbooks-doctrine",
            operational_question="What operating doctrine is relevant now?",
        ),
    }
)


class WorkspaceRouter:
    def __init__(
        self,
        route_definitions: Mapping[
            WorkspaceRouteId,
            WorkspaceRouteDefinition,
        ] = DEFAULT_WORKSPACE_ROUTE_DEFINITIONS,
    ) -> None:
        self._route_definitions = MappingProxyType(dict(route_definitions))

    @property
    def route_definitions(
        self,
    ) -> Mapping[WorkspaceRouteId, WorkspaceRouteDefinition]:
        return self._route_definitions

    def route_to(
        self,
        route_id: WorkspaceRouteId | str,
        context: WorkspaceRouteContext,
    ) -> WorkspaceRoute:
        normalized_route_id = self._normalize_route_id(route_id)
        definition = self._route_definitions.get(normalized_route_id)
        if definition is None:
            raise UnknownWorkspaceRouteError(
                f"unknown workspace route: {normalized_route_id}"
            )

        return WorkspaceRoute(
            definition=definition,
            context=context,
            entrypoint=self._build_entrypoint(definition.path, context),
        )

    def _normalize_route_id(self, route_id: WorkspaceRouteId | str) -> WorkspaceRouteId:
        try:
            return WorkspaceRouteId(route_id)
        except ValueError as error:
            raise UnknownWorkspaceRouteError(
                f"unknown workspace route: {route_id}"
            ) from error

    def _build_entrypoint(
        self,
        path: str,
        context: WorkspaceRouteContext,
    ) -> str:
        query_parameters = {
            "persona_id": context.persona_id,
            "selected_workflow_id": context.selected_workflow_id,
            "decision_id": context.decision_id,
        }
        query_string = urlencode(
            {
                key: value
                for key, value in query_parameters.items()
                if value is not None
            }
        )

        if not query_string:
            return path

        return f"{path}?{query_string}"
