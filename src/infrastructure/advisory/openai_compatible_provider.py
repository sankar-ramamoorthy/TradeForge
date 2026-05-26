from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

from openai import APIConnectionError, APIStatusError, OpenAI
from src.domain.advisory.contracts import (
    AdvisoryArtifactKind,
    AdvisoryAuthority,
    AdvisoryProvenance,
    AdvisoryProviderUnavailableError,
    AdvisoryRequest,
    AdvisoryResponse,
    AdvisoryUncertainty,
)
from src.infrastructure.advisory.litellm_request_composer import (
    LiteLLMRequestComposer,
    LLMProviderCredentialResolver,
    ResolvedLLMProviderCredential,
)
from src.security.advisory_model_selection import AdvisoryModelSelectionConfig
from src.security.litellm_credential import (
    LITELLM_PROVIDER_ID,
    LiteLLMCredentialPayload,
)

_LOG = logging.getLogger(__name__)

_PROVIDER_VERSION = "openai-compatible-v1"
_PROMPT_VERSION = "v1"

_SAFETY_FOOTER = """

---
CONSTRAINTS (mandatory):
- You are an ADVISORY system only. Your output is non-canonical and non-authoritative.
- Do NOT issue buy/sell instructions, trade recommendations, or execution orders.
- Do NOT approve, reject, or suggest lifecycle transitions.
- Do NOT claim authority over any trading or investment decision.
- Always express uncertainty explicitly.
- Always include at least one caveat about the limits of your analysis.
"""

_SYSTEM_PROMPTS: dict[AdvisoryArtifactKind, str] = {
    AdvisoryArtifactKind.REPLAY_SUMMARY: (
        "You are an advisory assistant helping a discretionary trader review a "
        "completed "
        "trade decision replay. Summarize the key events, how the thesis evolved, and "
        "what the decision process looked like. Focus on process quality and learning "
        "opportunities, not just outcome. Be specific and concise."
        + _SAFETY_FOOTER
    ),
    AdvisoryArtifactKind.INTERPRETATION_DRAFT: (
        "You are an advisory assistant helping interpret advisory observations in the "
        "context of an active trade idea. Describe what the observations may mean "
        "qualitatively — whether they appear to support, weaken, or complicate the "
        "thesis. Preserve uncertainty. Reference the specific observations you use."
        + _SAFETY_FOOTER
    ),
    AdvisoryArtifactKind.REVIEW_ASSISTANCE: (
        "You are an advisory assistant helping a discretionary trader reflect on a "
        "completed trade. Surface patterns in the decision process, identify "
        "behavioural "
        "tendencies visible in the record, and suggest areas for reflection. "
        "Focus on process quality and cognitive discipline."
        + _SAFETY_FOOTER
    ),
    AdvisoryArtifactKind.THESIS_REVIEW: (
        "You are an advisory assistant reviewing a structured trade thesis. Identify "
        "unstated assumptions, missing invalidation conditions, regime alignment gaps, "
        "and potential blind spots in the reasoning. Surface the questions the "
        "operator "
        "may not have considered. Do not validate, endorse, or rank the thesis."
        + _SAFETY_FOOTER
    ),
    AdvisoryArtifactKind.OBSERVATION_GENERATION: (
        "You are an advisory assistant generating structured advisory observations "
        "about "
        "a financial instrument. For each observation include: the observation kind "
        "(price_action / fundamentals / market_context / risk / news_research), "
        "a concise description of what you observe, your uncertainty level "
        "(low / medium / high / unknown), and at least one caveat. "
        "Generate multiple distinct observations — do not collapse into a single "
        "summary."
        + _SAFETY_FOOTER
    ),
    AdvisoryArtifactKind.CANDIDATE_SCREENING: (
        "You are an advisory assistant helping prioritize advisory candidates for "
        "operator attention. For each candidate briefly explain why it may or may not "
        "deserve immediate attention. Order by your qualitative assessment of urgency "
        "and opportunity quality. Preserve uncertainty explicitly."
        + _SAFETY_FOOTER
    ),
    AdvisoryArtifactKind.SCENARIO_RANKING: (
        "You are an advisory assistant helping evaluate trade scenarios. Compare the "
        "scenarios on qualitative factors: probability framing, risk/reward, regime "
        "alignment, and assumption quality. Do not claim predictive authority."
        + _SAFETY_FOOTER
    ),
    AdvisoryArtifactKind.RISK_HIGHLIGHT: (
        "You are an advisory assistant highlighting risk factors for a trade. Identify "
        "the most significant risks, tail risks, and assumptions that could fail. "
        "Be specific and concrete about each risk category."
        + _SAFETY_FOOTER
    ),
    AdvisoryArtifactKind.CONTEXT_SUMMARY: (
        "You are an advisory assistant summarizing market context. Provide a concise "
        "qualitative summary of the market environment, key themes, and conditions "
        "relevant to discretionary decision-making."
        + _SAFETY_FOOTER
    ),
}

_DEFAULT_CAVEATS = (
    "This is AI-generated advisory content. It is non-canonical and non-authoritative.",
    "The analysis may be incomplete, incorrect, or based on limited context.",
    "Always apply your own judgment before taking any action.",
)

_DEFAULT_CONFIDENCE = 0.5
_MAX_TOKENS = 1500
_TEMPERATURE = 0.3


class OpenAICompatibleAdvisoryProvider:
    """Calls any OpenAI-compatible endpoint (LiteLLM, Groq, NVIDIA NIM, Ollama).

    Credentials are passed in at construction time — already decrypted by the
    composition root. This adapter never calls CredentialStore or KeyManager.
    """

    def __init__(
        self,
        credential: LiteLLMCredentialPayload,
        *,
        model_selection: AdvisoryModelSelectionConfig | None = None,
        provider_credential_resolver: LLMProviderCredentialResolver | None = None,
        request_composer: LiteLLMRequestComposer | None = None,
    ) -> None:
        self._client = OpenAI(
            base_url=credential.base_url,
            api_key=credential.api_key,
        )
        if model_selection is None:
            if credential.default_model is None:
                raise ValueError("advisory model selection is not configured")
            model_selection = AdvisoryModelSelectionConfig(
                primary_provider_id="legacy",
                primary_model=credential.default_model,
                fallback_provider_id="legacy" if credential.fallback_model else None,
                fallback_model=credential.fallback_model,
                legacy_inferred=True,
            )
        self._model_selection = model_selection
        self._provider_credential_resolver = provider_credential_resolver
        self._request_composer = request_composer or LiteLLMRequestComposer()

    @property
    def provider_id(self) -> str:
        return LITELLM_PROVIDER_ID

    @property
    def provider_version(self) -> str:
        return _PROVIDER_VERSION

    def list_models(self) -> tuple[str, ...]:
        """Return model IDs visible through the configured OpenAI-compatible gateway."""
        models = self._client.models.list()
        return tuple(
            model_id
            for model in models.data
            if isinstance((model_id := getattr(model, "id", None)), str)
            and model_id.strip()
        )

    def generate(self, request: AdvisoryRequest) -> AdvisoryResponse:
        system_prompt = _SYSTEM_PROMPTS.get(
            request.artifact_kind,
            "You are an advisory assistant." + _SAFETY_FOOTER,
        )
        user_message = f"{request.operator_question}\n\n{request.context_summary}"
        generated_at = datetime.now(UTC)

        try:
            completion = self._create_completion(
                provider_id=self._model_selection.primary_provider_id,
                model=self._model_selection.primary_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
            )
        except (
            APIConnectionError,
            APIStatusError,
            AdvisoryProviderUnavailableError,
        ) as exc:
            if (
                self._model_selection.fallback_provider_id is None
                or self._model_selection.fallback_model is None
                or self._model_selection.fallback_model
                == self._model_selection.primary_model
            ):
                _LOG.warning("advisory provider unavailable: %s", exc)
                raise AdvisoryProviderUnavailableError(
                    f"advisory provider unreachable: {exc}"
                ) from exc
            try:
                completion = self._create_completion(
                    provider_id=self._model_selection.fallback_provider_id,
                    model=self._model_selection.fallback_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message},
                    ],
                )
            except (
                APIConnectionError,
                APIStatusError,
                AdvisoryProviderUnavailableError,
            ) as fallback_exc:
                _LOG.warning("advisory provider fallback unavailable: %s", fallback_exc)
                raise AdvisoryProviderUnavailableError(
                    f"advisory provider unreachable: {fallback_exc}"
                ) from fallback_exc

        raw_content = (completion.choices[0].message.content or "").strip()
        if not raw_content:
            raise ValueError("advisory provider returned empty content")

        model_used = completion.model or self._model_selection.primary_model

        return AdvisoryResponse(
            request_id=request.request_id,
            artifact_kind=request.artifact_kind,
            content=raw_content,
            provenance=AdvisoryProvenance(
                provider_id=self.provider_id,
                provider_version=self.provider_version,
                model_id=model_used,
                generated_at=generated_at,
                prompt_version=_PROMPT_VERSION,
            ),
            uncertainty=AdvisoryUncertainty(
                confidence=_DEFAULT_CONFIDENCE,
                caveats=_DEFAULT_CAVEATS,
            ),
            source_references=request.source_references,
            authority=AdvisoryAuthority.ADVISORY,
        )

    def _create_completion(
        self,
        *,
        provider_id: str,
        model: str,
        messages: Any,
    ) -> Any:
        provider_credential = (
            self._provider_credential_resolver.resolve(provider_id)
            if self._provider_credential_resolver is not None
            else ResolvedLLMProviderCredential(
                provider_id="legacy",
                requires_api_key=False,
            )
        )
        kwargs = self._request_composer.compose_chat_completion_kwargs(
            model=model,
            messages=messages,
            provider_credential=provider_credential,
            temperature=_TEMPERATURE,
            max_tokens=_MAX_TOKENS,
        )
        return self._client.chat.completions.create(**kwargs)
