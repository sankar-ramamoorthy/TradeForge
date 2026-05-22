"""Tests for OpenAICompatibleAdvisoryProvider (TF-F046)."""
from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

import pytest

from src.domain.advisory.contracts import (
    AdvisoryArtifactKind,
    AdvisoryAuthority,
    AdvisoryProviderUnavailableError,
    AdvisoryRequest,
    AdvisorySourceKind,
    AdvisorySourceReference,
)
from src.infrastructure.advisory.openai_compatible_provider import (
    OpenAICompatibleAdvisoryProvider,
)
from src.security.litellm_credential import LiteLLMCredentialPayload


def _credential() -> LiteLLMCredentialPayload:
    return LiteLLMCredentialPayload(
        base_url="http://localhost:4000",
        api_key="test-key",
        default_model="groq/llama-3.1-8b-instant",
    )


def _request(kind: AdvisoryArtifactKind = AdvisoryArtifactKind.REPLAY_SUMMARY) -> AdvisoryRequest:
    return AdvisoryRequest(
        request_id="req-001",
        artifact_kind=kind,
        operator_question="Summarise this replay.",
        context_summary="Decision was a breakout trade on NVDA.",
        source_references=(
            AdvisorySourceReference(
                source_kind=AdvisorySourceKind.REPLAY_TIMELINE_ENTRY,
                source_id="replay-001",
                description="Replay timeline entry",
            ),
        ),
        persona_id="swing-trader",
        workspace_id="replay-ws",
        requested_at=datetime.now(UTC),
    )


def _mock_completion(content: str, model: str = "groq/llama-3.1-8b-instant") -> MagicMock:
    choice = MagicMock()
    choice.message.content = content
    completion = MagicMock()
    completion.choices = [choice]
    completion.model = model
    return completion


def test_provider_id_and_version() -> None:
    provider = OpenAICompatibleAdvisoryProvider(_credential())
    assert provider.provider_id == "litellm"
    assert provider.provider_version == "openai-compatible-v1"


def test_generate_returns_advisory_response() -> None:
    provider = OpenAICompatibleAdvisoryProvider(_credential())
    mock_completion = _mock_completion("A summary of the replay.")

    with patch.object(provider._client.chat.completions, "create", return_value=mock_completion):
        response = provider.generate(_request())

    assert response.request_id == "req-001"
    assert response.artifact_kind == AdvisoryArtifactKind.REPLAY_SUMMARY
    assert response.authority is AdvisoryAuthority.ADVISORY
    assert response.content == "A summary of the replay."
    assert response.provenance.provider_id == "litellm"
    assert response.provenance.model_id == "groq/llama-3.1-8b-instant"
    assert response.provenance.prompt_version == "v1"
    assert len(response.uncertainty.caveats) >= 1
    assert 0.0 <= response.uncertainty.confidence <= 1.0
    assert len(response.source_references) == 1


def test_generate_preserves_source_references() -> None:
    provider = OpenAICompatibleAdvisoryProvider(_credential())
    request = _request()

    with patch.object(provider._client.chat.completions, "create", return_value=_mock_completion("content")):
        response = provider.generate(request)

    assert response.source_references == request.source_references


@pytest.mark.parametrize(
    "kind",
    [
        AdvisoryArtifactKind.REPLAY_SUMMARY,
        AdvisoryArtifactKind.INTERPRETATION_DRAFT,
        AdvisoryArtifactKind.REVIEW_ASSISTANCE,
        AdvisoryArtifactKind.THESIS_REVIEW,
        AdvisoryArtifactKind.OBSERVATION_GENERATION,
        AdvisoryArtifactKind.CANDIDATE_SCREENING,
    ],
)
def test_generate_all_artifact_kinds(kind: AdvisoryArtifactKind) -> None:
    provider = OpenAICompatibleAdvisoryProvider(_credential())
    request = _request(kind)

    with patch.object(provider._client.chat.completions, "create", return_value=_mock_completion("output")):
        response = provider.generate(request)

    assert response.artifact_kind is kind
    assert response.authority is AdvisoryAuthority.ADVISORY


def test_generate_raises_on_api_connection_error() -> None:
    from openai import APIConnectionError

    provider = OpenAICompatibleAdvisoryProvider(_credential())

    with patch.object(
        provider._client.chat.completions,
        "create",
        side_effect=APIConnectionError(request=MagicMock()),
    ):
        with pytest.raises(AdvisoryProviderUnavailableError):
            provider.generate(_request())


def test_generate_raises_on_empty_content() -> None:
    provider = OpenAICompatibleAdvisoryProvider(_credential())

    with patch.object(
        provider._client.chat.completions,
        "create",
        return_value=_mock_completion(""),
    ):
        with pytest.raises(ValueError, match="empty content"):
            provider.generate(_request())


def test_generate_strips_whitespace_content() -> None:
    provider = OpenAICompatibleAdvisoryProvider(_credential())

    with patch.object(
        provider._client.chat.completions,
        "create",
        return_value=_mock_completion("  trimmed content  "),
    ):
        response = provider.generate(_request())

    assert response.content == "trimmed content"
