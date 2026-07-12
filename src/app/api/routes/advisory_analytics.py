"""Advisory interpretation analytics routes.

Moved verbatim from the routes monolith in TF-RF007 (M-RF). Shares the
/advisory prefix; include after the advisory and generation routers to
preserve the monolith's route registration order.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from fastapi import APIRouter, Query, Request
from pydantic import BaseModel
from src.app.api.deps import (
    _advisory_interpretation_query_service_from,
)
from src.domain.advisory import (
    AdvisoryConfidenceRange,
    AdvisoryInterpretationQuery,
    ContextualWeight,
    InterpretationKind,
    ThesisInfluence,
)
from src.domain.market.snapshot import MarketRegime
from src.services.advisory import (
    ConfidenceRangeDistribution,
    ConflictSummary,
    ContextualWeightDistribution,
    InfluenceTimeline,
    ProbabilisticCognitionSummary,
    RegimeContextWeightService,
    ThesisDriftSignal,
)

advisory_analytics_router = APIRouter(prefix="/advisory", tags=["advisory"])


class ContextualWeightDistributionResponse(BaseModel):
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    thesis_id: str | None
    total_count: int
    counts: dict[str, int]


class ConfidenceRangeDistributionResponse(BaseModel):
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    thesis_id: str | None
    total_count: int
    counts: dict[str, int]


class InfluenceTimelineEntryResponse(BaseModel):
    interpretation_id: str
    captured_at: datetime
    thesis_influence: ThesisInfluence
    contextual_weight: ContextualWeight
    confidence_range: AdvisoryConfidenceRange
    interpretation_kind: InterpretationKind
    tags: list[str]


class InfluenceTimelineResponse(BaseModel):
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    thesis_id: str | None
    total_count: int
    entries: list[InfluenceTimelineEntryResponse]


class ConflictSummaryResponse(BaseModel):
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    thesis_id: str | None
    total_count: int
    conflicting_count: int
    opposing_pair_detected: bool
    conflicting_interpretation_ids: list[str]


class ThesisDriftSignalResponse(BaseModel):
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    thesis_id: str | None
    drift_detected: bool
    previous_dominant: ThesisInfluence | None
    current_dominant: ThesisInfluence | None
    total_count: int


class RegimeWeightSuggestionResponse(BaseModel):
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    suggested_weight: ContextualWeight
    regime: str
    rationale: str


class ProbabilisticCognitionSummaryResponse(BaseModel):
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    thesis_id: str | None
    total_count: int
    dominant_influence: ThesisInfluence | None
    dominant_weight: ContextualWeight | None
    has_conflict: bool
    influence_counts: dict[str, int]
    weight_counts: dict[str, int]
    confidence_counts: dict[str, int]


class ReasoningTimelineEntryResponse(BaseModel):
    kind: str
    event_type: str
    timestamp: datetime
    interpretation_id: str | None
    observation_ids: list[str]
    thesis_influence: str | None
    contextual_weight: str | None
    confidence_range: str | None
    capture_origin: str | None
    authority: Literal["advisory"]
    is_canonical: Literal[False]


class ReasoningTimelineResponse(BaseModel):
    authority: Literal["advisory"]
    is_canonical: Literal[False]
    thesis_id: str | None
    decision_id: str | None
    total_count: int
    entries: list[ReasoningTimelineEntryResponse]



@advisory_analytics_router.get(
    "/weight-distribution",
    response_model=ContextualWeightDistributionResponse,
)
def get_contextual_weight_distribution(
    request: Request,
    persona_id: str = Query(min_length=1),
    workspace_id: str = Query(min_length=1),
    thesis_id: str | None = Query(default=None, min_length=1),
    decision_id: str | None = Query(default=None, min_length=1),
) -> ContextualWeightDistributionResponse:
    dist: ContextualWeightDistribution = _advisory_interpretation_query_service_from(
        request
    ).contextual_weight_distribution(
        AdvisoryInterpretationQuery(
            persona_id=persona_id,
            workspace_id=workspace_id,
            thesis_id=thesis_id,
            decision_id=decision_id,
        )
    )
    return ContextualWeightDistributionResponse(
        authority="advisory",
        is_canonical=False,
        thesis_id=dist.thesis_id,
        total_count=dist.total_count,
        counts={w.value: count for w, count in dist.counts.items()},
    )


@advisory_analytics_router.get(
    "/confidence-distribution",
    response_model=ConfidenceRangeDistributionResponse,
)
def get_confidence_range_distribution(
    request: Request,
    persona_id: str = Query(min_length=1),
    workspace_id: str = Query(min_length=1),
    thesis_id: str | None = Query(default=None, min_length=1),
    decision_id: str | None = Query(default=None, min_length=1),
) -> ConfidenceRangeDistributionResponse:
    dist: ConfidenceRangeDistribution = _advisory_interpretation_query_service_from(
        request
    ).confidence_range_distribution(
        AdvisoryInterpretationQuery(
            persona_id=persona_id,
            workspace_id=workspace_id,
            thesis_id=thesis_id,
            decision_id=decision_id,
        )
    )
    return ConfidenceRangeDistributionResponse(
        authority="advisory",
        is_canonical=False,
        thesis_id=dist.thesis_id,
        total_count=dist.total_count,
        counts={cr.value: count for cr, count in dist.counts.items()},
    )


@advisory_analytics_router.get(
    "/influence-timeline",
    response_model=InfluenceTimelineResponse,
)
def get_influence_timeline(
    request: Request,
    persona_id: str = Query(min_length=1),
    workspace_id: str = Query(min_length=1),
    thesis_id: str | None = Query(default=None, min_length=1),
    decision_id: str | None = Query(default=None, min_length=1),
) -> InfluenceTimelineResponse:
    timeline: InfluenceTimeline = _advisory_interpretation_query_service_from(
        request
    ).influence_timeline(
        AdvisoryInterpretationQuery(
            persona_id=persona_id,
            workspace_id=workspace_id,
            thesis_id=thesis_id,
            decision_id=decision_id,
        )
    )
    return InfluenceTimelineResponse(
        authority="advisory",
        is_canonical=False,
        thesis_id=timeline.thesis_id,
        total_count=timeline.total_count,
        entries=[
            InfluenceTimelineEntryResponse(
                interpretation_id=entry.interpretation_id,
                captured_at=entry.captured_at,
                thesis_influence=entry.thesis_influence,
                contextual_weight=entry.contextual_weight,
                confidence_range=entry.confidence_range,
                interpretation_kind=entry.interpretation_kind,
                tags=list(entry.tags),
            )
            for entry in timeline.entries
        ],
    )


@advisory_analytics_router.get(
    "/conflict-summary",
    response_model=ConflictSummaryResponse,
)
def get_conflict_summary(
    request: Request,
    persona_id: str = Query(min_length=1),
    workspace_id: str = Query(min_length=1),
    thesis_id: str | None = Query(default=None, min_length=1),
    decision_id: str | None = Query(default=None, min_length=1),
) -> ConflictSummaryResponse:
    summary: ConflictSummary = _advisory_interpretation_query_service_from(
        request
    ).conflict_summary(
        AdvisoryInterpretationQuery(
            persona_id=persona_id,
            workspace_id=workspace_id,
            thesis_id=thesis_id,
            decision_id=decision_id,
        )
    )
    return ConflictSummaryResponse(
        authority="advisory",
        is_canonical=False,
        thesis_id=summary.thesis_id,
        total_count=summary.total_count,
        conflicting_count=summary.conflicting_count,
        opposing_pair_detected=summary.opposing_pair_detected,
        conflicting_interpretation_ids=list(summary.conflicting_interpretation_ids),
    )


@advisory_analytics_router.get(
    "/drift-signal",
    response_model=ThesisDriftSignalResponse,
)
def get_drift_signal(
    request: Request,
    persona_id: str = Query(min_length=1),
    workspace_id: str = Query(min_length=1),
    thesis_id: str | None = Query(default=None, min_length=1),
    decision_id: str | None = Query(default=None, min_length=1),
) -> ThesisDriftSignalResponse:
    signal: ThesisDriftSignal = _advisory_interpretation_query_service_from(
        request
    ).drift_signal(
        AdvisoryInterpretationQuery(
            persona_id=persona_id,
            workspace_id=workspace_id,
            thesis_id=thesis_id,
            decision_id=decision_id,
        )
    )
    return ThesisDriftSignalResponse(
        authority="advisory",
        is_canonical=False,
        thesis_id=signal.thesis_id,
        drift_detected=signal.drift_detected,
        previous_dominant=signal.previous_dominant,
        current_dominant=signal.current_dominant,
        total_count=signal.total_count,
    )


@advisory_analytics_router.get(
    "/regime-weight-suggestion",
    response_model=RegimeWeightSuggestionResponse,
)
def get_regime_weight_suggestion(
    regime: MarketRegime = Query(...),
) -> RegimeWeightSuggestionResponse:
    """Suggest contextual weight for interpretations based on market regime.

    Advisory only — the suggestion does not auto-apply. Operator decides.
    """
    suggestion = RegimeContextWeightService().suggest_weight(regime)
    return RegimeWeightSuggestionResponse(
        authority="advisory",
        is_canonical=False,
        suggested_weight=suggestion.suggested_weight,
        regime=suggestion.regime.value,
        rationale=suggestion.rationale,
    )


@advisory_analytics_router.get(
    "/cognition-summary",
    response_model=ProbabilisticCognitionSummaryResponse,
)
def get_probabilistic_cognition_summary(
    request: Request,
    persona_id: str = Query(min_length=1),
    workspace_id: str = Query(min_length=1),
    thesis_id: str | None = Query(default=None, min_length=1),
    decision_id: str | None = Query(default=None, min_length=1),
) -> ProbabilisticCognitionSummaryResponse:
    """Advisory probabilistic cognition summary across influence, weight, and confidence.

    Combines thesis influence, contextual weight, and confidence range distributions
    into a single advisory read model. Non-canonical — derived from advisory artifacts.
    """
    summary: ProbabilisticCognitionSummary = (
        _advisory_interpretation_query_service_from(
            request
        ).probabilistic_cognition_summary(
            AdvisoryInterpretationQuery(
                persona_id=persona_id,
                workspace_id=workspace_id,
                thesis_id=thesis_id,
                decision_id=decision_id,
            )
        )
    )
    return ProbabilisticCognitionSummaryResponse(
        authority="advisory",
        is_canonical=False,
        thesis_id=summary.thesis_id,
        total_count=summary.total_count,
        dominant_influence=summary.dominant_influence,
        dominant_weight=summary.dominant_weight,
        has_conflict=summary.has_conflict,
        influence_counts={k.value: v for k, v in summary.influence_counts.items()},
        weight_counts={k.value: v for k, v in summary.weight_counts.items()},
        confidence_counts={k.value: v for k, v in summary.confidence_counts.items()},
    )


@advisory_analytics_router.get(
    "/reasoning-timeline",
    response_model=ReasoningTimelineResponse,
)
def get_reasoning_timeline(
    request: Request,
    persona_id: str = Query(min_length=1),
    workspace_id: str = Query(min_length=1),
    decision_id: str | None = Query(default=None, min_length=1),
    thesis_id: str | None = Query(default=None, min_length=1),
) -> ReasoningTimelineResponse:
    """Contextual reasoning timeline combining advisory observations and interpretations.

    Composes advisory capture facts from the event ledger with interpretation
    analytics into a single chronological advisory reasoning timeline.
    All content is advisory-only and non-canonical.
    """
    interp_query = AdvisoryInterpretationQuery(
        persona_id=persona_id,
        workspace_id=workspace_id,
        thesis_id=thesis_id,
        decision_id=decision_id,
    )
    interp_svc = _advisory_interpretation_query_service_from(request)
    timeline = interp_svc.influence_timeline(interp_query)

    entries = [
        ReasoningTimelineEntryResponse(
            kind="interpretation",
            event_type="advisory.interpretation_captured",
            timestamp=entry.captured_at,
            interpretation_id=entry.interpretation_id,
            observation_ids=[],
            thesis_influence=entry.thesis_influence.value,
            contextual_weight=entry.contextual_weight.value,
            confidence_range=entry.confidence_range.value,
            capture_origin=None,
            authority="advisory",
            is_canonical=False,
        )
        for entry in timeline.entries
    ]

    return ReasoningTimelineResponse(
        authority="advisory",
        is_canonical=False,
        thesis_id=thesis_id,
        decision_id=decision_id,
        total_count=len(entries),
        entries=entries,
    )
