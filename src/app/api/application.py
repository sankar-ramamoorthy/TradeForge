from __future__ import annotations

from fastapi import FastAPI
from src.app.api.routes import runtime_router

APP_TITLE = "TradeForge Runtime"
APP_VERSION = "0.1.0"


def create_app() -> FastAPI:
    app = FastAPI(
        title=APP_TITLE,
        version=APP_VERSION,
        description="HTTP boundary for the TradeForge runtime.",
    )
    app.include_router(runtime_router)
    return app


app = create_app()
