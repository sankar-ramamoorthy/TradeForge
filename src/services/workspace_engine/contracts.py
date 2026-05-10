from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType

from src.services.workspace_engine.routing import (
    DEFAULT_WORKSPACE_ROUTE_DEFINITIONS,
    WorkspaceRouteId,
)


class WorkspaceStateAuthority(StrEnum):
    CANONICAL = "canonical"
    DERIVED = "derived"
    INFERRED = "inferred"
    ADVISORY = "advisory"


@dataclass(frozen=True, slots=True)
class WorkspaceStateField:
    name: str
    authority: WorkspaceStateAuthority
    description: str
    source_inputs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "source_inputs", tuple(self.source_inputs))


@dataclass(frozen=True, slots=True)
class WorkspaceLifecycleAction:
    action_id: str
    label: str
    lifecycle_boundary: str


@dataclass(frozen=True, slots=True)
class WorkspaceReplayRequirement:
    description: str
    required_inputs: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "required_inputs", tuple(self.required_inputs))


@dataclass(frozen=True, slots=True)
class WorkspaceStateContract:
    route_id: WorkspaceRouteId
    operational_question: str
    state_fields: tuple[WorkspaceStateField, ...]
    lifecycle_actions: tuple[WorkspaceLifecycleAction, ...]
    required_event_inputs: tuple[str, ...]
    replay_requirements: tuple[WorkspaceReplayRequirement, ...]
    authority_boundaries: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "state_fields", tuple(self.state_fields))
        object.__setattr__(
            self,
            "lifecycle_actions",
            tuple(self.lifecycle_actions),
        )
        object.__setattr__(
            self,
            "required_event_inputs",
            tuple(self.required_event_inputs),
        )
        object.__setattr__(
            self,
            "replay_requirements",
            tuple(self.replay_requirements),
        )
        object.__setattr__(
            self,
            "authority_boundaries",
            tuple(self.authority_boundaries),
        )


class UnknownWorkspaceStateContractError(ValueError):
    pass


DEFAULT_WORKSPACE_STATE_CONTRACTS: Mapping[
    WorkspaceRouteId,
    WorkspaceStateContract,
] = MappingProxyType(
    {
        WorkspaceRouteId.OPERATING: WorkspaceStateContract(
            route_id=WorkspaceRouteId.OPERATING,
            operational_question=DEFAULT_WORKSPACE_ROUTE_DEFINITIONS[
                WorkspaceRouteId.OPERATING
            ].operational_question,
            state_fields=(
                WorkspaceStateField(
                    name="active_workflow_references",
                    authority=WorkspaceStateAuthority.CANONICAL,
                    description="References to event-backed active decisions.",
                    source_inputs=("decision.*", "execution.*", "review.*"),
                ),
                WorkspaceStateField(
                    name="attention_queue",
                    authority=WorkspaceStateAuthority.DERIVED,
                    description="Ordered operational attention items.",
                    source_inputs=("decision.*", "execution.*", "review.*"),
                ),
                WorkspaceStateField(
                    name="urgency_assessment",
                    authority=WorkspaceStateAuthority.INFERRED,
                    description="Urgency interpretation from workflow context.",
                    source_inputs=("attention_queue",),
                ),
            ),
            lifecycle_actions=(
                WorkspaceLifecycleAction(
                    action_id="open-decision-context",
                    label="Open decision context",
                    lifecycle_boundary="Route to workspace; do not mutate.",
                ),
            ),
            required_event_inputs=("decision.*", "execution.*", "review.*"),
            replay_requirements=(
                WorkspaceReplayRequirement(
                    description="Rebuild attention from ordered event history.",
                    required_inputs=("decision.*", "execution.*", "review.*"),
                ),
            ),
            authority_boundaries=(
                "Attention queues are derived and do not authorize execution.",
                "Lifecycle transitions must route through lifecycle services.",
            ),
        ),
        WorkspaceRouteId.OPPORTUNITY: WorkspaceStateContract(
            route_id=WorkspaceRouteId.OPPORTUNITY,
            operational_question=DEFAULT_WORKSPACE_ROUTE_DEFINITIONS[
                WorkspaceRouteId.OPPORTUNITY
            ].operational_question,
            state_fields=(
                WorkspaceStateField(
                    name="scenario_references",
                    authority=WorkspaceStateAuthority.CANONICAL,
                    description="References to recorded scenario facts and decisions.",
                    source_inputs=("scenario.*", "decision.*"),
                ),
                WorkspaceStateField(
                    name="opportunity_candidates",
                    authority=WorkspaceStateAuthority.DERIVED,
                    description="Candidates derived from scenarios and workflow state.",
                    source_inputs=("scenario.*", "decision.*", "market.*"),
                ),
                WorkspaceStateField(
                    name="setup_quality",
                    authority=WorkspaceStateAuthority.INFERRED,
                    description="Setup assessment from deterministic rules.",
                    source_inputs=("opportunity_candidates",),
                ),
                WorkspaceStateField(
                    name="advisory_notes",
                    authority=WorkspaceStateAuthority.ADVISORY,
                    description="Optional non-authoritative opportunity notes.",
                    source_inputs=("opportunity_candidates",),
                ),
            ),
            lifecycle_actions=(
                WorkspaceLifecycleAction(
                    action_id="develop-thesis",
                    label="Develop thesis",
                    lifecycle_boundary="May request transition; does not create it.",
                ),
            ),
            required_event_inputs=("scenario.*", "decision.*", "market.*"),
            replay_requirements=(
                WorkspaceReplayRequirement(
                    description="Rebuild visible candidates from historical inputs.",
                    required_inputs=("scenario.*", "decision.*", "market.*"),
                ),
            ),
            authority_boundaries=(
                "Scenario-derived opportunity state is not a trade signal.",
                "Promotion to thesis or plan must use lifecycle authority.",
            ),
        ),
        WorkspaceRouteId.PLAN_REVIEW: WorkspaceStateContract(
            route_id=WorkspaceRouteId.PLAN_REVIEW,
            operational_question=DEFAULT_WORKSPACE_ROUTE_DEFINITIONS[
                WorkspaceRouteId.PLAN_REVIEW
            ].operational_question,
            state_fields=(
                WorkspaceStateField(
                    name="plan_references",
                    authority=WorkspaceStateAuthority.CANONICAL,
                    description="References to event-backed thesis and plan facts.",
                    source_inputs=("decision.thesis_created", "decision.plan_created"),
                ),
                WorkspaceStateField(
                    name="risk_review",
                    authority=WorkspaceStateAuthority.DERIVED,
                    description="Review context derived from plan payloads and rules.",
                    source_inputs=("decision.plan_created",),
                ),
                WorkspaceStateField(
                    name="rule_evaluation",
                    authority=WorkspaceStateAuthority.INFERRED,
                    description="Deterministic interpretation of plan readiness.",
                    source_inputs=("risk_review",),
                ),
            ),
            lifecycle_actions=(
                WorkspaceLifecycleAction(
                    action_id="approve-plan",
                    label="Approve plan",
                    lifecycle_boundary="Must call lifecycle service for Approval.",
                ),
            ),
            required_event_inputs=("decision.thesis_created", "decision.plan_created"),
            replay_requirements=(
                WorkspaceReplayRequirement(
                    description="Reconstruct plan review context before approval.",
                    required_inputs=(
                        "decision.thesis_created",
                        "decision.plan_created",
                    ),
                ),
            ),
            authority_boundaries=(
                "Plan review state cannot approve a plan by itself.",
                "Approval remains a lifecycle transition event.",
            ),
        ),
        WorkspaceRouteId.ACTIVE_POSITION: WorkspaceStateContract(
            route_id=WorkspaceRouteId.ACTIVE_POSITION,
            operational_question=DEFAULT_WORKSPACE_ROUTE_DEFINITIONS[
                WorkspaceRouteId.ACTIVE_POSITION
            ].operational_question,
            state_fields=(
                WorkspaceStateField(
                    name="position_references",
                    authority=WorkspaceStateAuthority.CANONICAL,
                    description="References to execution and active decision context.",
                    source_inputs=("execution.*", "decision.*"),
                ),
                WorkspaceStateField(
                    name="exposure_summary",
                    authority=WorkspaceStateAuthority.DERIVED,
                    description="Current exposure view derived from execution history.",
                    source_inputs=("execution.*",),
                ),
                WorkspaceStateField(
                    name="thesis_drift",
                    authority=WorkspaceStateAuthority.INFERRED,
                    description="Position state interpreted against thesis context.",
                    source_inputs=("decision.*", "execution.*", "market.*"),
                ),
            ),
            lifecycle_actions=(
                WorkspaceLifecycleAction(
                    action_id="prepare-position-review",
                    label="Prepare position review",
                    lifecycle_boundary="May prepare context; review is separate.",
                ),
            ),
            required_event_inputs=("decision.*", "execution.*", "market.*"),
            replay_requirements=(
                WorkspaceReplayRequirement(
                    description="Rebuild exposure and thesis alignment at replay time.",
                    required_inputs=("decision.*", "execution.*", "market.*"),
                ),
            ),
            authority_boundaries=(
                "PnL and exposure summaries are derived, not canonical truth.",
                "Position actions must remain workflow-aware.",
                "Active position context does not own lifecycle transitions.",
            ),
        ),
        WorkspaceRouteId.REPLAY: WorkspaceStateContract(
            route_id=WorkspaceRouteId.REPLAY,
            operational_question=DEFAULT_WORKSPACE_ROUTE_DEFINITIONS[
                WorkspaceRouteId.REPLAY
            ].operational_question,
            state_fields=(
                WorkspaceStateField(
                    name="event_timeline_references",
                    authority=WorkspaceStateAuthority.CANONICAL,
                    description="References to ordered source events used for replay.",
                    source_inputs=("persona.*", "workspace.*", "decision.*"),
                ),
                WorkspaceStateField(
                    name="reconstructed_workspace_state",
                    authority=WorkspaceStateAuthority.DERIVED,
                    description="Replay reconstruction derived from historical inputs.",
                    source_inputs=("event_timeline_references",),
                ),
                WorkspaceStateField(
                    name="historical_interpretation",
                    authority=WorkspaceStateAuthority.INFERRED,
                    description="Interpretation of what was visible and relevant then.",
                    source_inputs=("reconstructed_workspace_state",),
                ),
                WorkspaceStateField(
                    name="advisory_replay_summary",
                    authority=WorkspaceStateAuthority.ADVISORY,
                    description="Optional non-authoritative replay summary.",
                    source_inputs=("reconstructed_workspace_state",),
                ),
            ),
            lifecycle_actions=(),
            required_event_inputs=(
                "persona.*",
                "workspace.*",
                "decision.*",
                "execution.*",
                "review.*",
            ),
            replay_requirements=(
                WorkspaceReplayRequirement(
                    description="Reconstruct historical workflow without live APIs.",
                    required_inputs=(
                        "persona.*",
                        "workspace.*",
                        "decision.*",
                        "execution.*",
                        "review.*",
                    ),
                ),
            ),
            authority_boundaries=(
                "Replay reconstruction is derived and discardable.",
                "Replay does not mutate event history or lifecycle state.",
            ),
        ),
        WorkspaceRouteId.REVIEW: WorkspaceStateContract(
            route_id=WorkspaceRouteId.REVIEW,
            operational_question=DEFAULT_WORKSPACE_ROUTE_DEFINITIONS[
                WorkspaceRouteId.REVIEW
            ].operational_question,
            state_fields=(
                WorkspaceStateField(
                    name="review_references",
                    authority=WorkspaceStateAuthority.CANONICAL,
                    description="References to review and source workflow events.",
                    source_inputs=("review.*", "decision.*", "execution.*"),
                ),
                WorkspaceStateField(
                    name="decision_quality_context",
                    authority=WorkspaceStateAuthority.DERIVED,
                    description="Review context from lifecycle and outcome history.",
                    source_inputs=("decision.*", "execution.*", "review.*"),
                ),
                WorkspaceStateField(
                    name="behavioral_signal",
                    authority=WorkspaceStateAuthority.INFERRED,
                    description="Interpretive discipline or behavior pattern signal.",
                    source_inputs=("decision_quality_context",),
                ),
            ),
            lifecycle_actions=(
                WorkspaceLifecycleAction(
                    action_id="complete-review",
                    label="Complete review",
                    lifecycle_boundary="Must call lifecycle service for Review.",
                ),
            ),
            required_event_inputs=("decision.*", "execution.*", "review.*"),
            replay_requirements=(
                WorkspaceReplayRequirement(
                    description="Rebuild decision context before review.",
                    required_inputs=("decision.*", "execution.*", "review.*"),
                ),
            ),
            authority_boundaries=(
                "Review surface separates decision quality from outcome.",
                "Review completion remains event-backed.",
                "Review workspace context does not own lifecycle transitions.",
            ),
        ),
        WorkspaceRouteId.MARKET_CONTEXT: WorkspaceStateContract(
            route_id=WorkspaceRouteId.MARKET_CONTEXT,
            operational_question=DEFAULT_WORKSPACE_ROUTE_DEFINITIONS[
                WorkspaceRouteId.MARKET_CONTEXT
            ].operational_question,
            state_fields=(
                WorkspaceStateField(
                    name="market_observation_references",
                    authority=WorkspaceStateAuthority.CANONICAL,
                    description="References to recorded market observation events.",
                    source_inputs=("market.*",),
                ),
                WorkspaceStateField(
                    name="context_snapshot",
                    authority=WorkspaceStateAuthority.DERIVED,
                    description="Operational market context derived from observations.",
                    source_inputs=("market.*",),
                ),
                WorkspaceStateField(
                    name="regime_interpretation",
                    authority=WorkspaceStateAuthority.INFERRED,
                    description="Interpreted regime context for workspace emphasis.",
                    source_inputs=("context_snapshot",),
                ),
            ),
            lifecycle_actions=(),
            required_event_inputs=("market.*",),
            replay_requirements=(
                WorkspaceReplayRequirement(
                    description="Rebuild historically available market context.",
                    required_inputs=("market.*",),
                ),
            ),
            authority_boundaries=(
                "Market context is interpreted context, not decision authority.",
                "Market context does not generate lifecycle transitions.",
            ),
        ),
        WorkspaceRouteId.PLAYBOOKS_DOCTRINE: WorkspaceStateContract(
            route_id=WorkspaceRouteId.PLAYBOOKS_DOCTRINE,
            operational_question=DEFAULT_WORKSPACE_ROUTE_DEFINITIONS[
                WorkspaceRouteId.PLAYBOOKS_DOCTRINE
            ].operational_question,
            state_fields=(
                WorkspaceStateField(
                    name="doctrine_references",
                    authority=WorkspaceStateAuthority.CANONICAL,
                    description="References to stable doctrine or playbook artifacts.",
                    source_inputs=("system.*",),
                ),
                WorkspaceStateField(
                    name="relevant_playbooks",
                    authority=WorkspaceStateAuthority.DERIVED,
                    description="Playbook context selected for the active workflow.",
                    source_inputs=("system.*", "decision.*", "market.*"),
                ),
                WorkspaceStateField(
                    name="playbook_fit",
                    authority=WorkspaceStateAuthority.INFERRED,
                    description="Playbook relevance to current context.",
                    source_inputs=("relevant_playbooks",),
                ),
                WorkspaceStateField(
                    name="advisory_doctrine_notes",
                    authority=WorkspaceStateAuthority.ADVISORY,
                    description="Optional non-authoritative doctrine guidance.",
                    source_inputs=("relevant_playbooks",),
                ),
            ),
            lifecycle_actions=(),
            required_event_inputs=("system.*", "decision.*", "market.*"),
            replay_requirements=(
                WorkspaceReplayRequirement(
                    description="Preserve visible doctrine context.",
                    required_inputs=("system.*", "decision.*", "market.*"),
                ),
            ),
            authority_boundaries=(
                "Doctrine context guides interpretation but does not mutate state.",
                "Advisory doctrine notes are not canonical truth.",
                "Doctrine context does not generate lifecycle transitions.",
            ),
        ),
    }
)


class WorkspaceStateContractCatalog:
    def __init__(
        self,
        contracts: Mapping[
            WorkspaceRouteId,
            WorkspaceStateContract,
        ] = DEFAULT_WORKSPACE_STATE_CONTRACTS,
    ) -> None:
        self._contracts = MappingProxyType(dict(contracts))

    @property
    def contracts(self) -> Mapping[WorkspaceRouteId, WorkspaceStateContract]:
        return self._contracts

    def contract_for(
        self,
        route_id: WorkspaceRouteId | str,
    ) -> WorkspaceStateContract:
        normalized_route_id = self._normalize_route_id(route_id)
        contract = self._contracts.get(normalized_route_id)
        if contract is None:
            raise UnknownWorkspaceStateContractError(
                f"unknown workspace state contract: {normalized_route_id}"
            )

        return contract

    def _normalize_route_id(self, route_id: WorkspaceRouteId | str) -> WorkspaceRouteId:
        try:
            return WorkspaceRouteId(route_id)
        except ValueError as error:
            raise UnknownWorkspaceStateContractError(
                f"unknown workspace state contract: {route_id}"
            ) from error
