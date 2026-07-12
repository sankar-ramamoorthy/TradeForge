"""API routes package. Assembly moves here in TF-RF010; until then the
monolith owns runtime_router."""

from src.app.api.routes._monolith import runtime_router

__all__ = ["runtime_router"]
