from __future__ import annotations

from fastapi import FastAPI
from src.app.api.routes import runtime_router
from src.domain.events import EventStore
from src.infrastructure.event_store.in_memory import InMemoryEventStore
from src.services.lifecycle import LifecycleOrchestrationService
from src.services.replay import (
    HistoricalReconstructionPipeline,
    ReplayTimelineService,
)

APP_TITLE = "TradeForge Runtime"
APP_VERSION = "0.1.0"


def create_app(
    event_store: EventStore | None = None,
    lifecycle_service: LifecycleOrchestrationService | None = None,
    replay_timeline_service: ReplayTimelineService | None = None,
    historical_reconstruction_pipeline: (
        HistoricalReconstructionPipeline | None
    ) = None,
) -> FastAPI:
    shared_event_store = event_store or InMemoryEventStore()
    app = FastAPI(
        title=APP_TITLE,
        version=APP_VERSION,
        description="HTTP boundary for the TradeForge runtime.",
    )
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
    app.include_router(runtime_router)
    return app


app = create_app()
