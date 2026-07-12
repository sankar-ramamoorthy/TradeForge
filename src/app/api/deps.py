"""Service accessors shared by API route handlers.

Extracted verbatim from routes.py in TF-RF002 (M-RF). Each accessor reads a
configured service from ``request.app.state``. Conversion to FastAPI
``Depends()`` injection is deliberately deferred to M-RF2.
"""

from __future__ import annotations

from typing import Any

from fastapi import HTTPException, Request, status
from src.app.session import SessionProvider
from src.domain.market.registry import ProviderRegistry
from src.security.credential_store import CredentialStore
from src.services.advisory import (
    AdvisoryArtifactIngestionService,
    AdvisoryArtifactQueryService,
    AdvisoryCandidateIngestionService,
    AdvisoryCandidateQueryService,
    AdvisoryInterpretationCaptureService,
    AdvisoryInterpretationQueryService,
    AdvisoryObservationCaptureService,
    AdvisoryObservationQueryService,
    CandidateReviewQueueService,
    InterpretationDraftService,
)
from src.services.behavioral import BehavioralSignalReadService
from src.services.lifecycle import LifecycleOrchestrationService
from src.services.market.contextual_summary import ContextualSummaryService
from src.services.market.fundamentals_service import FundamentalsService
from src.services.market.provenance_query import ProvenanceQueryService
from src.services.market.snapshot_query import MarketSnapshotQueryService
from src.services.market.snapshot_service import MarketSnapshotService
from src.services.replay import (
    HistoricalReconstructionPipeline,
    ReplayTimelineService,
)
from src.services.workspace_engine import (
    OperationalAttentionQueueReadService,
    WorkspaceProjectionReadService,
)


def _event_store_from(request: Request) -> Any:
    store = getattr(request.app.state, "event_store", None)
    if store is None:
        raise RuntimeError("event store is not configured")
    return store


def _lifecycle_service_from(request: Request) -> LifecycleOrchestrationService:
    service = getattr(request.app.state, "lifecycle_service", None)
    if not isinstance(service, LifecycleOrchestrationService):
        raise RuntimeError("lifecycle service is not configured")
    return service


def _replay_timeline_service_from(request: Request) -> ReplayTimelineService:
    service = getattr(request.app.state, "replay_timeline_service", None)
    if not isinstance(service, ReplayTimelineService):
        raise RuntimeError("replay timeline service is not configured")
    return service


def _advisory_observation_capture_service_from(
    request: Request,
) -> AdvisoryObservationCaptureService:
    service = getattr(request.app.state, "advisory_observation_capture_service", None)
    if not isinstance(service, AdvisoryObservationCaptureService):
        raise RuntimeError("advisory observation capture service is not configured")
    return service


def _advisory_observation_query_service_from(
    request: Request,
) -> AdvisoryObservationQueryService:
    service = getattr(request.app.state, "advisory_observation_query_service", None)
    if not isinstance(service, AdvisoryObservationQueryService):
        raise RuntimeError("advisory observation query service is not configured")
    return service


def _advisory_candidate_ingestion_service_from(
    request: Request,
) -> AdvisoryCandidateIngestionService:
    service = getattr(request.app.state, "advisory_candidate_ingestion_service", None)
    if not isinstance(service, AdvisoryCandidateIngestionService):
        raise RuntimeError("advisory candidate ingestion service is not configured")
    return service


def _advisory_candidate_query_service_from(
    request: Request,
) -> AdvisoryCandidateQueryService:
    service = getattr(request.app.state, "advisory_candidate_query_service", None)
    if not isinstance(service, AdvisoryCandidateQueryService):
        raise RuntimeError("advisory candidate query service is not configured")
    return service


def _candidate_review_queue_service_from(
    request: Request,
) -> CandidateReviewQueueService:
    service = getattr(request.app.state, "candidate_review_queue_service", None)
    if not isinstance(service, CandidateReviewQueueService):
        raise RuntimeError("candidate review queue service is not configured")
    return service


def _behavioral_signal_read_service_from(
    request: Request,
) -> BehavioralSignalReadService:
    service = getattr(request.app.state, "behavioral_signal_read_service", None)
    if not isinstance(service, BehavioralSignalReadService):
        raise RuntimeError("behavioral signal read service is not configured")
    return service


def _advisory_artifact_ingestion_service_from(
    request: Request,
) -> AdvisoryArtifactIngestionService:
    service = getattr(request.app.state, "advisory_artifact_ingestion_service", None)
    if not isinstance(service, AdvisoryArtifactIngestionService):
        raise RuntimeError("advisory artifact ingestion service is not configured")
    return service


def _advisory_artifact_query_service_from(
    request: Request,
) -> AdvisoryArtifactQueryService:
    service = getattr(request.app.state, "advisory_artifact_query_service", None)
    if not isinstance(service, AdvisoryArtifactQueryService):
        raise RuntimeError("advisory artifact query service is not configured")
    return service


def _advisory_interpretation_capture_service_from(
    request: Request,
) -> AdvisoryInterpretationCaptureService:
    service = getattr(
        request.app.state,
        "advisory_interpretation_capture_service",
        None,
    )
    if not isinstance(service, AdvisoryInterpretationCaptureService):
        raise RuntimeError(
            "advisory interpretation capture service is not configured"
        )
    return service


def _advisory_interpretation_query_service_from(
    request: Request,
) -> AdvisoryInterpretationQueryService:
    service = getattr(
        request.app.state,
        "advisory_interpretation_query_service",
        None,
    )
    if not isinstance(service, AdvisoryInterpretationQueryService):
        raise RuntimeError(
            "advisory interpretation query service is not configured"
        )
    return service


def _interpretation_draft_service_from(request: Request) -> InterpretationDraftService:
    service = getattr(request.app.state, "interpretation_draft_service", None)
    if not isinstance(service, InterpretationDraftService):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "message": "interpretation draft provider is not configured",
                "authority": "advisory",
                "requires_operator_acceptance": True,
            },
        )
    return service


def _historical_reconstruction_pipeline_from(
    request: Request,
) -> HistoricalReconstructionPipeline:
    pipeline = getattr(request.app.state, "historical_reconstruction_pipeline", None)
    if not isinstance(pipeline, HistoricalReconstructionPipeline):
        raise RuntimeError("historical reconstruction pipeline is not configured")
    return pipeline


def _workspace_projection_read_service_from(
    request: Request,
) -> WorkspaceProjectionReadService:
    service = getattr(request.app.state, "workspace_projection_read_service", None)
    if not isinstance(service, WorkspaceProjectionReadService):
        raise RuntimeError("workspace projection read service is not configured")
    return service


def _attention_queue_read_service_from(
    request: Request,
) -> OperationalAttentionQueueReadService:
    service = getattr(
        request.app.state,
        "operational_attention_queue_read_service",
        None,
    )
    if not isinstance(service, OperationalAttentionQueueReadService):
        raise RuntimeError(
            "operational attention queue read service is not configured"
        )
    return service


def _session_provider_from(request: Request) -> SessionProvider:
    provider = getattr(request.app.state, "session_provider", None)
    if not isinstance(provider, SessionProvider):
        raise RuntimeError("session provider is not configured")
    return provider


def _market_snapshot_service_from(request: Request) -> MarketSnapshotService:
    service = getattr(request.app.state, "market_snapshot_service", None)
    if not isinstance(service, MarketSnapshotService):
        raise RuntimeError("market snapshot service is not configured")
    return service


def _contextual_summary_service_from(request: Request) -> ContextualSummaryService:
    service = getattr(request.app.state, "contextual_summary_service", None)
    if not isinstance(service, ContextualSummaryService):
        raise RuntimeError("contextual summary service is not configured")
    return service


def _provider_registry_from(request: Request) -> ProviderRegistry:
    registry = getattr(request.app.state, "provider_registry", None)
    if not isinstance(registry, ProviderRegistry):
        raise RuntimeError("provider registry is not configured")
    return registry


def _credential_store_from_state(request: Request) -> CredentialStore | None:
    store = getattr(request.app.state, "credential_store", None)
    if isinstance(store, CredentialStore):
        return store
    return None


def _fundamentals_service_from(request: Request) -> FundamentalsService:
    service = getattr(request.app.state, "fundamentals_service", None)
    if not isinstance(service, FundamentalsService):
        raise RuntimeError("fundamentals service is not configured")
    return service


def _market_snapshot_query_service_from(
    request: Request,
) -> MarketSnapshotQueryService:
    service = getattr(request.app.state, "market_snapshot_query_service", None)
    if not isinstance(service, MarketSnapshotQueryService):
        raise RuntimeError("market snapshot query service is not configured")
    return service


def _provenance_query_service_from(request: Request) -> ProvenanceQueryService:
    service = getattr(request.app.state, "provenance_query_service", None)
    if not isinstance(service, ProvenanceQueryService):
        raise RuntimeError("provenance query service is not configured")
    return service
