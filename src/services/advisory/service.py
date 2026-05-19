from __future__ import annotations

from src.domain.advisory import (
    AdvisoryAuthority,
    AdvisoryRequest,
    AdvisoryResponse,
    AIAdvisoryProvider,
)


class AIAdvisoryService:
    """Orchestrates advisory generation without owning workflow authority."""

    def __init__(self, provider: AIAdvisoryProvider) -> None:
        self._provider = provider

    def generate(self, request: AdvisoryRequest) -> AdvisoryResponse:
        response = self._provider.generate(request)
        if response.request_id != request.request_id:
            raise ValueError("advisory response request_id does not match request")
        if response.artifact_kind is not request.artifact_kind:
            raise ValueError("advisory response artifact_kind does not match request")
        if response.authority is not AdvisoryAuthority.ADVISORY:
            raise ValueError("advisory response must remain advisory")
        return response
