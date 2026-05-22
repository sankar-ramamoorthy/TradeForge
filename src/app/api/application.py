from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI
from src.app.api.routes import runtime_router
from src.app.session import LocalSessionProvider, SessionProvider
from src.domain.advisory import AIAdvisoryProvider
from src.domain.events import EventStore
from src.domain.market.capability import (
    CapabilityPreference,
    ProviderCapability,
    ProviderDescriptor,
)
from src.domain.market.provider import FundamentalsDataProvider, MarketDataProvider
from src.domain.market.registry import ProviderRegistry
from src.infrastructure.advisory.in_memory_artifact_store import (
    InMemoryAdvisoryArtifactStore,
)
from src.infrastructure.advisory.in_memory_interpretation_store import (
    InMemoryAdvisoryInterpretationStore,
)
from src.infrastructure.advisory.in_memory_observation_store import (
    InMemoryAdvisoryObservationStore,
)
from src.infrastructure.advisory.postgres_artifact_store import (
    PostgresAdvisoryArtifactStore,
)
from src.infrastructure.advisory.postgres_interpretation_store import (
    PostgresAdvisoryInterpretationStore,
)
from src.infrastructure.advisory.postgres_observation_store import (
    PostgresAdvisoryObservationStore,
)
from src.infrastructure.event_store.in_memory import InMemoryEventStore
from src.infrastructure.event_store.postgres import PostgresEventStore
from src.infrastructure.market.alpaca_adapter import AlpacaProvider
from src.infrastructure.market.alpha_vantage_adapter import (
    AlphaVantageFundamentalsProvider,
)
from src.infrastructure.market.fmp_adapter import FmpFundamentalsProvider
from src.infrastructure.market.in_memory_provenance_store import InMemoryProvenanceStore
from src.infrastructure.market.in_memory_snapshot_store import (
    InMemoryMarketSnapshotStore,
)
from src.infrastructure.market.polygon_adapter import PolygonProvider
from src.infrastructure.market.yfinance_adapter import YFinanceProvider
from src.security import CredentialStore, KeyManager
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
from src.services.lifecycle import LifecycleOrchestrationService
from src.services.market.contextual_summary import ContextualSummaryService
from src.services.market.fundamentals_service import FundamentalsService
from src.services.market.provenance_query import ProvenanceQueryService
from src.services.market.regime_interpreter import SingleBarRegimeInterpreter
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

APP_TITLE = "TradeForge Runtime"
APP_VERSION = "0.1.0"


def _default_event_store() -> EventStore:
    """Use PostgresEventStore when TRADEFORGE_DATABASE_URL is set, else InMemory."""
    if os.environ.get("TRADEFORGE_DATABASE_URL") or os.environ.get(
        "TRADEFORGE_POSTGRES_HOST"
    ):
        return PostgresEventStore()
    return InMemoryEventStore()


def _default_credential_store() -> CredentialStore | None:
    store_path = Path(".keys.enc")
    if store_path.exists():
        return CredentialStore(store_path)
    return None


def _default_market_provider(
    credential_store: CredentialStore | None,
) -> MarketDataProvider:
    provider_id = os.environ.get("TRADEFORGE_MARKET_PROVIDER", "yfinance").lower()

    if provider_id == "yfinance":
        return YFinanceProvider()

    if credential_store is None:
        raise RuntimeError(
            f"credential store is required for market provider '{provider_id}'"
        )

    credential = credential_store.get(provider_id)
    if credential is None:
        raise RuntimeError(
            f"credential for market provider '{provider_id}' is not configured"
        )

    payload = KeyManager.from_environment().decrypt_payload(
        credential.encrypted_payload
    )

    if provider_id == "polygon":
        return PolygonProvider(api_key=payload["api_key"])
    if provider_id == "alpaca":
        return AlpacaProvider(
            api_key=payload["api_key"],
            secret_key=payload["secret_key"],
        )

    raise RuntimeError(f"unsupported market provider '{provider_id}'")


def _default_provider_registry(
    credential_store: CredentialStore | None,
) -> ProviderRegistry:
    descriptors = [
        ProviderDescriptor("yfinance", (ProviderCapability.PRICE,)),
        ProviderDescriptor("polygon", (ProviderCapability.PRICE,)),
        ProviderDescriptor("alpaca", (ProviderCapability.PRICE,)),
    ]
    if credential_store is not None and credential_store.get("fmp") is not None:
        descriptors.append(
            ProviderDescriptor("fmp", (ProviderCapability.FUNDAMENTALS,))
        )
    if (
        credential_store is not None
        and credential_store.get("alpha_vantage") is not None
    ):
        descriptors.append(
            ProviderDescriptor("alpha_vantage", (ProviderCapability.FUNDAMENTALS,))
        )
    return ProviderRegistry(
        providers=tuple(descriptors),
        preferences=(
            CapabilityPreference(
                ProviderCapability.PRICE,
                os.environ.get("TRADEFORGE_MARKET_PROVIDER", "yfinance").lower(),
            ),
            CapabilityPreference(
                ProviderCapability.FUNDAMENTALS,
                "fmp",
                ("alpha_vantage",),
            ),
        ),
    )


def _default_fundamentals_providers(
    credential_store: CredentialStore | None,
) -> dict[str, FundamentalsDataProvider]:
    if credential_store is None:
        return {}
    key_manager = KeyManager.from_environment()
    providers: dict[str, FundamentalsDataProvider] = {}
    fmp = credential_store.get("fmp")
    if fmp is not None:
        payload = key_manager.decrypt_payload(fmp.encrypted_payload)
        providers["fmp"] = FmpFundamentalsProvider(api_key=payload["api_key"])
    alpha_vantage = credential_store.get("alpha_vantage")
    if alpha_vantage is not None:
        payload = key_manager.decrypt_payload(alpha_vantage.encrypted_payload)
        providers["alpha_vantage"] = AlphaVantageFundamentalsProvider(
            api_key=payload["api_key"]
        )
    return providers


def create_app(
    event_store: EventStore | None = None,
    lifecycle_service: LifecycleOrchestrationService | None = None,
    replay_timeline_service: ReplayTimelineService | None = None,
    historical_reconstruction_pipeline: (
        HistoricalReconstructionPipeline | None
    ) = None,
    workspace_projection_read_service: WorkspaceProjectionReadService | None = None,
    operational_attention_queue_read_service: (
        OperationalAttentionQueueReadService | None
    ) = None,
    session_provider: SessionProvider | None = None,
    market_snapshot_service: MarketSnapshotService | None = None,
    contextual_summary_service: ContextualSummaryService | None = None,
    provenance_query_service: ProvenanceQueryService | None = None,
    market_snapshot_query_service: MarketSnapshotQueryService | None = None,
    credential_store: CredentialStore | None = None,
    provider_registry: ProviderRegistry | None = None,
    fundamentals_service: FundamentalsService | None = None,
    advisory_observation_capture_service: (
        AdvisoryObservationCaptureService | None
    ) = None,
    advisory_observation_query_service: AdvisoryObservationQueryService | None = None,
    advisory_candidate_ingestion_service: (
        AdvisoryCandidateIngestionService | None
    ) = None,
    advisory_candidate_query_service: AdvisoryCandidateQueryService | None = None,
    candidate_review_queue_service: CandidateReviewQueueService | None = None,
    advisory_interpretation_capture_service: (
        AdvisoryInterpretationCaptureService | None
    ) = None,
    advisory_interpretation_query_service: (
        AdvisoryInterpretationQueryService | None
    ) = None,
    interpretation_draft_service: InterpretationDraftService | None = None,
    ai_advisory_provider: AIAdvisoryProvider | None = None,
    advisory_artifact_ingestion_service: (
        AdvisoryArtifactIngestionService | None
    ) = None,
    advisory_artifact_query_service: AdvisoryArtifactQueryService | None = None,
) -> FastAPI:
    shared_event_store = event_store or _default_event_store()
    app = FastAPI(
        title=APP_TITLE,
        version=APP_VERSION,
        description="HTTP boundary for the TradeForge runtime.",
    )
    app.state.event_store = shared_event_store
    app.state.lifecycle_service = (
        lifecycle_service
        if lifecycle_service is not None
        else LifecycleOrchestrationService(shared_event_store)
    )
    app.state.replay_timeline_service = (
        replay_timeline_service
        if replay_timeline_service is not None
        else ReplayTimelineService(shared_event_store)
    )
    app.state.historical_reconstruction_pipeline = (
        historical_reconstruction_pipeline
        if historical_reconstruction_pipeline is not None
        else HistoricalReconstructionPipeline(shared_event_store)
    )
    app.state.workspace_projection_read_service = (
        workspace_projection_read_service
        if workspace_projection_read_service is not None
        else WorkspaceProjectionReadService(shared_event_store)
    )
    app.state.operational_attention_queue_read_service = (
        operational_attention_queue_read_service
        if operational_attention_queue_read_service is not None
        else OperationalAttentionQueueReadService(shared_event_store)
    )
    app.state.session_provider = (
        session_provider
        if session_provider is not None
        else LocalSessionProvider()
    )
    _provenance_store = InMemoryProvenanceStore()
    _snapshot_store = InMemoryMarketSnapshotStore()
    _credential_store = (
        credential_store
        if credential_store is not None
        else _default_credential_store()
    )
    _provider_registry = (
        provider_registry
        if provider_registry is not None
        else _default_provider_registry(_credential_store)
    )
    _market_svc = (
        market_snapshot_service
        if market_snapshot_service is not None
        else MarketSnapshotService(
            _default_market_provider(_credential_store),
            SingleBarRegimeInterpreter(),
            provenance_store=_provenance_store,
            snapshot_persistence_store=_snapshot_store,
        )
    )
    app.state.market_snapshot_service = _market_svc
    app.state.contextual_summary_service = (
        contextual_summary_service
        if contextual_summary_service is not None
        else ContextualSummaryService(
            event_store=shared_event_store,
            market_snapshot_service=_market_svc,
        )
    )
    app.state.provenance_query_service = (
        provenance_query_service
        if provenance_query_service is not None
        else ProvenanceQueryService(_provenance_store)
    )
    app.state.market_snapshot_query_service = (
        market_snapshot_query_service
        if market_snapshot_query_service is not None
        else MarketSnapshotQueryService(_snapshot_store)
    )
    app.state.provider_registry = _provider_registry
    app.state.fundamentals_service = (
        fundamentals_service
        if fundamentals_service is not None
        else FundamentalsService(
            _provider_registry,
            _default_fundamentals_providers(_credential_store),
        )
    )
    advisory_observation_store = (
        PostgresAdvisoryObservationStore()
        if os.environ.get("TRADEFORGE_DATABASE_URL")
        else InMemoryAdvisoryObservationStore()
    )
    advisory_interpretation_store = (
        PostgresAdvisoryInterpretationStore()
        if os.environ.get("TRADEFORGE_DATABASE_URL")
        else InMemoryAdvisoryInterpretationStore()
    )
    advisory_artifact_store = (
        PostgresAdvisoryArtifactStore()
        if os.environ.get("TRADEFORGE_DATABASE_URL")
        else InMemoryAdvisoryArtifactStore()
    )
    app.state.advisory_observation_capture_service = (
        advisory_observation_capture_service
        if advisory_observation_capture_service is not None
        else AdvisoryObservationCaptureService(
            advisory_observation_store,
            shared_event_store,
        )
    )
    app.state.advisory_observation_query_service = (
        advisory_observation_query_service
        if advisory_observation_query_service is not None
        else AdvisoryObservationQueryService(advisory_observation_store)
    )
    app.state.advisory_candidate_ingestion_service = (
        advisory_candidate_ingestion_service
        if advisory_candidate_ingestion_service is not None
        else AdvisoryCandidateIngestionService(
            advisory_observation_store,
            shared_event_store,
        )
    )
    _candidate_query_service = (
        advisory_candidate_query_service
        if advisory_candidate_query_service is not None
        else AdvisoryCandidateQueryService(advisory_observation_store)
    )
    app.state.advisory_candidate_query_service = _candidate_query_service
    app.state.candidate_review_queue_service = (
        candidate_review_queue_service
        if candidate_review_queue_service is not None
        else CandidateReviewQueueService(_candidate_query_service)
    )
    app.state.advisory_interpretation_capture_service = (
        advisory_interpretation_capture_service
        if advisory_interpretation_capture_service is not None
        else AdvisoryInterpretationCaptureService(
            advisory_interpretation_store,
            shared_event_store,
        )
    )
    app.state.advisory_interpretation_query_service = (
        advisory_interpretation_query_service
        if advisory_interpretation_query_service is not None
        else AdvisoryInterpretationQueryService(advisory_interpretation_store)
    )
    app.state.interpretation_draft_service = (
        interpretation_draft_service
        if interpretation_draft_service is not None
        else (
            InterpretationDraftService(
                ai_advisory_provider,
                advisory_observation_store,
            )
            if ai_advisory_provider is not None
            else None
        )
    )
    app.state.advisory_artifact_ingestion_service = (
        advisory_artifact_ingestion_service
        if advisory_artifact_ingestion_service is not None
        else AdvisoryArtifactIngestionService(advisory_artifact_store)
    )
    app.state.advisory_artifact_query_service = (
        advisory_artifact_query_service
        if advisory_artifact_query_service is not None
        else AdvisoryArtifactQueryService(advisory_artifact_store)
    )
    app.include_router(runtime_router)
    return app


app = create_app()
