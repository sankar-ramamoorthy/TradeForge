from __future__ import annotations

from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

runtime_router = APIRouter(tags=["runtime"])


class RuntimeStatusResponse(BaseModel):
    status: Literal["ok"]
    runtime: Literal["tradeforge"]
    boundary: Literal["http"]
    owns_domain_rules: Literal[False]


@runtime_router.get("/health", response_model=RuntimeStatusResponse)
def health() -> RuntimeStatusResponse:
    return RuntimeStatusResponse(
        status="ok",
        runtime="tradeforge",
        boundary="http",
        owns_domain_rules=False,
    )
