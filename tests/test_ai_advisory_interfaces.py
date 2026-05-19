from dataclasses import FrozenInstanceError
from datetime import UTC, datetime
from pathlib import Path

import pytest
from src.domain.advisory import (
    AdvisoryArtifactKind,
    AdvisoryAuthority,
    AdvisoryProvenance,
    AdvisoryRequest,
    AdvisoryResponse,
    AdvisorySourceKind,
    AdvisorySourceReference,
    AdvisoryUncertainty,
)
from src.services.advisory import AIAdvisoryService


def _source_reference() -> AdvisorySourceReference:
    return AdvisorySourceReference(
        source_kind=AdvisorySourceKind.EVENT,
        source_id="event-123",
        description="decision thesis event",
    )


def _request() -> AdvisoryRequest:
    return AdvisoryRequest(
        request_id="advisory-request-1",
        artifact_kind=AdvisoryArtifactKind.REPLAY_SUMMARY,
        operator_question="What changed in this decision sequence?",
        context_summary="Decision moved from thesis to plan with revised risk framing.",
        source_references=(_source_reference(),),
        persona_id="persona.swing",
        workspace_id="workspace.replay",
        decision_id="decision-123",
        requested_at=datetime(2026, 5, 19, 15, 0, tzinfo=UTC),
    )


def _response(request: AdvisoryRequest | None = None) -> AdvisoryResponse:
    source_request = request or _request()
    return AdvisoryResponse(
        request_id=source_request.request_id,
        artifact_kind=source_request.artifact_kind,
        content="The plan added tighter invalidation after thesis revision.",
        provenance=AdvisoryProvenance(
            provider_id="test-ai",
            provider_version="0.1",
            model_id="test-model",
            prompt_version="tf-0065-v1",
            generated_at=datetime(2026, 5, 19, 15, 1, tzinfo=UTC),
        ),
        uncertainty=AdvisoryUncertainty(
            confidence=0.74,
            caveats=("Generated from supplied context only.",),
        ),
        source_references=source_request.source_references,
    )


def test_advisory_response_is_explicitly_non_canonical() -> None:
    response = _response()

    assert response.authority is AdvisoryAuthority.ADVISORY
    assert response.provenance.provider_id == "test-ai"
    assert response.uncertainty.confidence == 0.74
    assert response.source_references[0].source_kind is AdvisorySourceKind.EVENT


def test_advisory_contracts_are_immutable() -> None:
    response = _response()

    with pytest.raises(FrozenInstanceError):
        response.content = "mutated"  # type: ignore[misc]

    with pytest.raises(TypeError):
        response.source_references[0] = _source_reference()  # type: ignore[index]


def test_advisory_request_requires_source_context() -> None:
    with pytest.raises(ValueError, match="source_references"):
        AdvisoryRequest(
            request_id="advisory-request-1",
            artifact_kind=AdvisoryArtifactKind.CONTEXT_SUMMARY,
            operator_question="What matters?",
            context_summary="Context exists.",
            source_references=(),
            persona_id="persona.swing",
            workspace_id="workspace.context",
            requested_at=datetime(2026, 5, 19, 15, 0, tzinfo=UTC),
        )


def test_uncertainty_requires_visible_caveats_and_bounded_confidence() -> None:
    with pytest.raises(ValueError, match="confidence"):
        AdvisoryUncertainty(confidence=1.4, caveats=("invalid",))

    with pytest.raises(ValueError, match="caveats"):
        AdvisoryUncertainty(confidence=0.5, caveats=())


def test_advisory_service_invokes_provider_without_mutation_authority() -> None:
    request = _request()
    provider = _RecordingAdvisoryProvider(_response(request))
    service = AIAdvisoryService(provider)

    response = service.generate(request)

    assert response.request_id == request.request_id
    assert provider.requests == (request,)
    assert not hasattr(service, "append")
    assert not hasattr(service, "transition")
    assert not hasattr(response, "approve_plan")
    assert not hasattr(response, "execute_trade")


def test_advisory_service_rejects_mismatched_provider_response() -> None:
    request = _request()
    mismatched = AdvisoryResponse(
        request_id="different-request",
        artifact_kind=request.artifact_kind,
        content="Mismatch.",
        provenance=_response(request).provenance,
        uncertainty=_response(request).uncertainty,
        source_references=request.source_references,
    )
    service = AIAdvisoryService(_RecordingAdvisoryProvider(mismatched))

    with pytest.raises(ValueError, match="request_id"):
        service.generate(request)


def test_advisory_domain_preserves_boundary_imports() -> None:
    module_text = Path("src/domain/advisory/contracts.py").read_text(encoding="utf-8")
    service_text = Path("src/services/advisory/service.py").read_text(encoding="utf-8")

    assert "src.infrastructure" not in module_text
    assert "src.app" not in module_text
    assert "src.services.lifecycle" not in module_text
    assert "EventStore" not in module_text
    assert ".append(" not in module_text

    assert "src.infrastructure" not in service_text
    assert "src.services.lifecycle" not in service_text
    assert "EventStore" not in service_text
    assert ".append(" not in service_text


class _RecordingAdvisoryProvider:
    provider_id = "test-ai"
    provider_version = "0.1"

    def __init__(self, response: AdvisoryResponse) -> None:
        self._response = response
        self.requests: tuple[AdvisoryRequest, ...] = ()

    def generate(self, request: AdvisoryRequest) -> AdvisoryResponse:
        self.requests = (*self.requests, request)
        return self._response
