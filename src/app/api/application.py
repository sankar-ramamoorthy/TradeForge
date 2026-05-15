from __future__ import annotations

import os

from fastapi import FastAPI
from src.app.api.routes import runtime_router
from src.app.session import LocalSessionProvider, SessionProvider
from src.domain.events import EventStore
from src.infrastructure.event_store.in_memory import InMemoryEventStore
from src.infrastructure.event_store.postgres import PostgresEventStore
from src.infrastructure.market.in_memory_provenance_store import InMemoryProvenanceStore
from src.infrastructure.market.in_memory_snapshot_store import (
    InMemoryMarketSnapshotStore,
)
from src.infrastructure.market.yfinance_adapter import YFinanceProvider
from src.services.lifecycle import LifecycleOrchestrationService
from src.services.market.contextual_summary import ContextualSummaryService
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
    if os.environ.get("TRADEFORGE_DATABASE_URL") or os.environ.get("TRADEFORGE_POSTGRES_HOST"):
        return PostgresEventStore()
    return InMemoryEventStore()


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
    _market_svc = (
        market_snapshot_service
        if market_snapshot_service is not None
        else MarketSnapshotService(
            YFinanceProvider(),
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
    app.include_router(runtime_router)
    return app


app = create_app()
