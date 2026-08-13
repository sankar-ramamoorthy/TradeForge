"""Provider governance and configuration routes.

Moved verbatim from the routes monolith in TF-RF008 (M-RF). The
provider-governance endpoints historically hang directly off the runtime
router; ``governance_router`` therefore declares no prefix and no tags so
the operations keep their exact paths and their ["runtime"] tag when
included into the runtime router (path fidelity wins over router-tag
tidiness). The workspace-scoped provider-configuration pair keeps its exact
paths via ``workspace_governance_router``, which must be included into the
runtime router before the workspace router so the ``/workspaces/{route_id}``
catch-all keeps matching last.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Literal

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel, Field
from src.app.api.deps import (
    _credential_store_from_state,
    _provider_registry_from,
)
from src.domain.advisory import (
    AdvisoryArtifactKind,
    AdvisoryProviderUnavailableError,
    AdvisoryRequest,
    AdvisorySourceKind,
    AdvisorySourceReference,
)
from src.domain.market.capability import ProviderCapability
from src.infrastructure.advisory.litellm_request_composer import (
    OLLAMA_AUTO_PROVIDER_ID,
    OLLAMA_LOCAL_PROVIDER_ID,
    OLLAMA_PROVIDER_ID,
    OLLAMA_PROVIDER_IDS,
    OLLAMA_REMOTE_PROVIDER_ID,
    configured_ollama_model_hints,
    is_ollama_provider_configured,
)
from src.security.advisory_model_selection import (
    AdvisoryModelSelectionConfig,
    get_advisory_model_selection_config,
    infer_legacy_provider_id,
    save_advisory_model_selection_config,
)
from src.security.credential import Credential, CredentialStatus
from src.security.key_manager import (
    InvalidCredentialPayloadError,
    KeyManager,
    MasterKeyNotConfiguredError,
)
from src.security.litellm_credential import (
    LiteLLMCredentialNotConfiguredError,
    get_litellm_credential,
)
from src.security.llm_provider_secrets import LLM_PROVIDER_SECRET_SCHEMAS
from src.services.advisory.service import AIAdvisoryService

governance_router = APIRouter()
workspace_governance_router = APIRouter(prefix="/workspaces", tags=["workspaces"])


_KNOWN_PROVIDER_CAPABILITIES: dict[str, tuple[str, ...]] = {
    "yfinance": ("price",),
    "polygon": ("price",),
    "alpaca": ("price",),
    "fmp": ("fundamentals",),
    "alpha_vantage": ("fundamentals",),
    "litellm": ("ai_advisory",),
    OLLAMA_PROVIDER_ID: ("llm_provider_route",),
    OLLAMA_LOCAL_PROVIDER_ID: ("llm_provider_route",),
    OLLAMA_REMOTE_PROVIDER_ID: ("llm_provider_route",),
    OLLAMA_AUTO_PROVIDER_ID: ("llm_provider_route",),
    **{
        schema.provider_id: ("llm_provider_secret",)
        for schema in LLM_PROVIDER_SECRET_SCHEMAS
    },
}
_CREDENTIAL_REQUIRED_PROVIDER_IDS = frozenset(
    {
        "polygon",
        "alpaca",
        "fmp",
        "alpha_vantage",
        "litellm",
        *(schema.provider_id for schema in LLM_PROVIDER_SECRET_SCHEMAS),
    }
)
_AI_GATEWAY_ROUTE_ALIASES: tuple[tuple[str, str, str], ...] = (
    (
        "tf-fast",
        "candidate screening and lightweight advisory summaries",
        "advisory triage",
    ),
    (
        "tf-reasoning",
        "thesis review and advisory observation generation",
        "reasoned interpretation",
    ),
    (
        "tf-long-context",
        "replay summary and long-context synthesis",
        "replay synthesis",
    ),
    ("tf-cheap", "low-cost validation and classification", "lightweight checks"),
    ("tf-local", "local or offline private drafting", "private drafting"),
)
_LLM_PROVIDER_SECRET_IDS = frozenset(
    schema.provider_id for schema in LLM_PROVIDER_SECRET_SCHEMAS
)


class ProviderCapabilityResponse(BaseModel):
    provider_id: str
    capabilities: list[str]


class CapabilityResolutionResponse(BaseModel):
    capability: str
    preferred_provider_id: str
    fallback_provider_ids: list[str]
    configured_provider_ids: list[str]
    selected_provider_id: str | None
    used_fallback: bool
    is_available: bool


class ProviderConfigurationResponse(BaseModel):
    authority: Literal["advisory"]
    providers: list[ProviderCapabilityResponse]
    resolutions: list[CapabilityResolutionResponse]


class ProviderGovernanceCredentialResponse(BaseModel):
    provider_id: str
    credential_required: bool
    configured: bool
    status: Literal[
        "configured",
        "missing",
        "revoked",
        "expired",
        "invalid",
        "unknown",
        "untested",
    ]
    credential_record_status: str | None
    rotated_at: datetime | None
    last_validated_at: datetime | None
    exposes_secret_values: Literal[False]


class ProviderGovernanceProviderResponse(BaseModel):
    provider_id: str
    capabilities: list[str]
    registry_configured: bool
    credential_required: bool
    credential_status: str
    health_status: Literal[
        "available",
        "missing_credential",
        "revoked",
        "expired",
        "invalid",
        "unknown",
        "not_configured",
    ]
    authority: Literal["operational"]
    is_canonical: Literal[False]


class ProviderGovernanceRouteResponse(BaseModel):
    capability: str
    preferred_provider_id: str
    fallback_provider_ids: list[str]
    configured_provider_ids: list[str]
    selected_provider_id: str | None
    used_fallback: bool
    is_available: bool
    degraded: bool


class ProviderGovernanceDiagnosticSummaryResponse(BaseModel):
    status: Literal["ok", "degraded", "not_configured"]
    retained_history_available: Literal[False]
    event_ledger_authority: Literal[False]
    diagnostic_classes: list[str]


class ProviderGovernanceRouteAliasResponse(BaseModel):
    alias: str
    advisory_role: str
    advisory_usage_domain: str
    configured: bool
    availability_status: Literal["configured", "not_configured", "unknown"]
    route_target_model: str | None
    fallback_model: str | None
    route_target_provider_id: str | None = None
    fallback_provider_id: str | None = None
    underlying_provider_id: str | None
    reachability: Literal["not_checked", "available", "unavailable", "unknown"]


class ProviderGovernanceAIGatewayResponse(BaseModel):
    gateway_id: Literal["litellm"]
    configured: bool
    status: Literal["configured", "not_configured", "unavailable", "unknown"]
    provider_id: str | None
    gateway_url: str | None
    default_model: str | None
    fallback_model: str | None
    primary_provider_id: str | None = None
    fallback_provider_id: str | None = None
    underlying_provider_id: str | None
    reachability: Literal["not_checked", "available", "unavailable", "unknown"]
    route_aliases: list[ProviderGovernanceRouteAliasResponse]
    lifecycle_authority: Literal[False]
    execution_authority: Literal[False]
    event_ledger_authority: Literal[False]


class AdvisoryRouteSmokeTestPayload(BaseModel):
    operator_question: str = Field(
        default=(
            "Reply with one short sentence confirming the advisory route is "
            "reachable."
        ),
        min_length=1,
        max_length=500,
    )


class AdvisoryRouteSmokeTestResponse(BaseModel):
    gateway_id: Literal["litellm"]
    status: Literal["available", "unavailable", "not_configured"]
    diagnostic_message: str
    provider_id: str | None
    model_id: str | None
    generated_at: datetime | None
    content_preview: str | None
    authority: Literal["operational"]
    is_canonical: Literal[False]
    lifecycle_authority: Literal[False]
    execution_authority: Literal[False]
    event_ledger_writes: Literal[False]
    advisory_response_authority: Literal["advisory"] | None


class AdvisoryModelSelectionPayload(BaseModel):
    primary_provider_id: str = Field(min_length=1)
    primary_model: str = Field(min_length=1)
    fallback_provider_id: str | None = Field(default=None, min_length=1)
    fallback_model: str | None = Field(default=None, min_length=1)


class AdvisoryModelSelectionResponse(BaseModel):
    gateway_id: Literal["litellm"]
    configured: bool
    discovery_status: Literal["available", "unavailable", "not_configured"]
    available_models: list[str]
    selected_primary_model: str | None
    selected_fallback_model: str | None
    selected_primary_provider_id: str | None
    selected_fallback_provider_id: str | None
    gateway_url: str | None
    authority: Literal["operational"]
    is_canonical: Literal[False]
    lifecycle_authority: Literal[False]
    execution_authority: Literal[False]
    event_ledger_writes: Literal[False]


class LLMProviderSecretInjectionItemResponse(BaseModel):
    provider_id: str
    display_name: str
    litellm_environment_variable: str
    configured: bool
    available_for_runtime_injection: bool


class LLMProviderSecretInjectionResponse(BaseModel):
    gateway_id: Literal["litellm"]
    authority: Literal["operational"]
    is_canonical: Literal[False]
    exposes_secret_values: Literal[False]
    runtime_decryption_boundary: Literal["composition"]
    reload_semantics: Literal["credential_write_triggers_provider_reload"]
    injectable_environment_variables: list[str]
    provider_secrets: list[LLMProviderSecretInjectionItemResponse]
    lifecycle_authority: Literal[False]
    execution_authority: Literal[False]
    event_ledger_writes: Literal[False]


class ProviderGovernanceResponse(BaseModel):
    authority: Literal["operational"]
    is_canonical: Literal[False]
    generated_at: datetime
    lifecycle_authority: Literal[False]
    event_ledger_writes: Literal[False]
    advisory_boundary: list[str]
    providers: list[ProviderGovernanceProviderResponse]
    credentials: list[ProviderGovernanceCredentialResponse]
    routes: list[ProviderGovernanceRouteResponse]
    diagnostics: ProviderGovernanceDiagnosticSummaryResponse
    ai_gateway: ProviderGovernanceAIGatewayResponse


class ProviderPreferenceRequest(BaseModel):
    preferred_provider_id: str
    fallback_provider_ids: list[str] = []


def _credential_status_for(
    provider_id: str,
    credential: Credential | None,
) -> ProviderGovernanceCredentialResponse:
    credential_required = provider_id in _CREDENTIAL_REQUIRED_PROVIDER_IDS
    if not credential_required:
        return ProviderGovernanceCredentialResponse(
            provider_id=provider_id,
            credential_required=False,
            configured=True,
            status="configured",
            credential_record_status=None,
            rotated_at=None,
            last_validated_at=None,
            exposes_secret_values=False,
        )
    if credential is None:
        return ProviderGovernanceCredentialResponse(
            provider_id=provider_id,
            credential_required=True,
            configured=False,
            status="missing",
            credential_record_status=None,
            rotated_at=None,
            last_validated_at=None,
            exposes_secret_values=False,
        )
    configured = credential.status is CredentialStatus.ACTIVE
    status_label: Literal[
        "configured",
        "missing",
        "revoked",
        "expired",
        "invalid",
        "unknown",
        "untested",
    ]
    if credential.status is CredentialStatus.ACTIVE:
        status_label = (
            "configured" if credential.last_validated_at is not None else "untested"
        )
    elif credential.status is CredentialStatus.REVOKED:
        status_label = "revoked"
    elif credential.status is CredentialStatus.EXPIRED:
        status_label = "expired"
    elif credential.status is CredentialStatus.INVALID:
        status_label = "invalid"
    else:
        status_label = "unknown"
    return ProviderGovernanceCredentialResponse(
        provider_id=provider_id,
        credential_required=True,
        configured=configured,
        status=status_label,
        credential_record_status=credential.status.value,
        rotated_at=credential.rotated_at,
        last_validated_at=credential.last_validated_at,
        exposes_secret_values=False,
    )


def _provider_health_status(
    *,
    registry_configured: bool,
    credential: ProviderGovernanceCredentialResponse,
) -> Literal[
    "available",
    "missing_credential",
    "revoked",
    "expired",
    "invalid",
    "unknown",
    "not_configured",
]:
    if not registry_configured:
        return "not_configured"
    if not credential.credential_required:
        return "available"
    if credential.status == "missing":
        return "missing_credential"
    if credential.status == "revoked":
        return "revoked"
    if credential.status == "expired":
        return "expired"
    if credential.status == "invalid":
        return "invalid"
    if credential.status == "unknown":
        return "unknown"
    return "available"


def _infer_underlying_provider_id(model_id: str | None) -> str | None:
    return infer_legacy_provider_id(model_id)


def _provider_registry_configured(
    *,
    provider_id: str,
    registry_provider_ids: set[str],
    ai_provider: object | None,
) -> bool:
    return (
        provider_id in registry_provider_ids
        or (provider_id == "litellm" and ai_provider is not None)
        or provider_id in _LLM_PROVIDER_SECRET_IDS
        or (
            provider_id in OLLAMA_PROVIDER_IDS
            and is_ollama_provider_configured(provider_id)
        )
    )


def _litellm_gateway_metadata(
    request: Request,
) -> tuple[str | None, AdvisoryModelSelectionConfig | None]:
    credential_store = _credential_store_from_state(request)
    if credential_store is None:
        return None, None
    try:
        key_manager = KeyManager.from_environment()
        payload = get_litellm_credential(
            credential_store,
            key_manager=key_manager,
        )
        model_selection = get_advisory_model_selection_config(
            credential_store,
            key_manager=key_manager,
        )
    except (
        KeyError,
        InvalidCredentialPayloadError,
        LiteLLMCredentialNotConfiguredError,
        MasterKeyNotConfiguredError,
        ValueError,
    ):
        return None, None
    return payload.base_url, model_selection


def _build_ai_gateway_response(request: Request) -> ProviderGovernanceAIGatewayResponse:
    credential_store = _credential_store_from_state(request)
    credential = (
        _credential_status_for(
            "litellm",
            credential_store.get("litellm") if credential_store is not None else None,
        )
        if credential_store is not None
        else _credential_status_for("litellm", None)
    )
    ai_provider = getattr(request.app.state, "ai_advisory_provider", None)
    gateway_url, model_selection = _litellm_gateway_metadata(request)
    default_model = (
        model_selection.primary_model if model_selection is not None else None
    )
    fallback_model = (
        model_selection.fallback_model if model_selection is not None else None
    )
    primary_provider_id = (
        model_selection.primary_provider_id if model_selection is not None else None
    )
    fallback_provider_id = (
        model_selection.fallback_provider_id if model_selection is not None else None
    )
    underlying_provider_id = primary_provider_id
    configured = ai_provider is not None
    if configured:
        status_label: Literal[
            "configured", "not_configured", "unavailable", "unknown"
        ] = "configured"
    elif credential.status != "missing":
        status_label = "unavailable"
    else:
        status_label = "not_configured"

    alias_availability: Literal["configured", "not_configured", "unknown"] = (
        "configured" if configured else "not_configured"
    )
    return ProviderGovernanceAIGatewayResponse(
        gateway_id="litellm",
        configured=configured,
        status=status_label,
        provider_id=getattr(ai_provider, "provider_id", None)
        if ai_provider is not None
        else None,
        gateway_url=gateway_url,
        default_model=default_model,
        fallback_model=fallback_model,
        primary_provider_id=primary_provider_id,
        fallback_provider_id=fallback_provider_id,
        underlying_provider_id=underlying_provider_id,
        reachability="not_checked",
        route_aliases=[
            ProviderGovernanceRouteAliasResponse(
                alias=alias,
                advisory_role=advisory_role,
                advisory_usage_domain=advisory_usage_domain,
                configured=configured,
                availability_status=alias_availability,
                route_target_model=default_model,
                fallback_model=fallback_model,
                route_target_provider_id=primary_provider_id,
                fallback_provider_id=fallback_provider_id,
                underlying_provider_id=underlying_provider_id,
                reachability="not_checked",
            )
            for alias, advisory_role, advisory_usage_domain in _AI_GATEWAY_ROUTE_ALIASES
        ],
        lifecycle_authority=False,
        execution_authority=False,
        event_ledger_authority=False,
    )


def _discover_litellm_models(
    request: Request,
) -> tuple[list[str], Literal["available", "unavailable", "not_configured"]]:
    _, model_selection = _litellm_gateway_metadata(request)
    if model_selection is None:
        return [], "not_configured"
    selected_models = [model_selection.primary_model]
    if model_selection.fallback_model is not None:
        selected_models.append(model_selection.fallback_model)
    selected_models.extend(configured_ollama_model_hints())
    return sorted(set(selected_models)), "available"


def _build_advisory_model_selection_response(
    request: Request,
) -> AdvisoryModelSelectionResponse:
    gateway_url, model_selection = _litellm_gateway_metadata(request)
    available_models, discovery_status = _discover_litellm_models(request)
    return AdvisoryModelSelectionResponse(
        gateway_id="litellm",
        configured=model_selection is not None,
        discovery_status=discovery_status,
        available_models=available_models,
        selected_primary_model=(
            model_selection.primary_model if model_selection is not None else None
        ),
        selected_fallback_model=(
            model_selection.fallback_model if model_selection is not None else None
        ),
        selected_primary_provider_id=(
            model_selection.primary_provider_id if model_selection is not None else None
        ),
        selected_fallback_provider_id=(
            model_selection.fallback_provider_id
            if model_selection is not None
            else None
        ),
        gateway_url=gateway_url,
        authority="operational",
        is_canonical=False,
        lifecycle_authority=False,
        execution_authority=False,
        event_ledger_writes=False,
    )


def _update_advisory_model_selection(
    request: Request,
    payload: AdvisoryModelSelectionPayload,
) -> AdvisoryModelSelectionResponse:
    credential_store = _credential_store_from_state(request)
    if credential_store is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="litellm credential is not configured",
        )
    if credential_store.get("litellm") is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="litellm credential is not configured",
        )

    key_manager = KeyManager.from_environment()
    save_advisory_model_selection_config(
        credential_store,
        AdvisoryModelSelectionConfig(
            primary_provider_id=payload.primary_provider_id,
            primary_model=payload.primary_model,
            fallback_provider_id=payload.fallback_provider_id,
            fallback_model=payload.fallback_model,
        ),
        key_manager=key_manager,
    )
    request.app.state.provider_bootstrap.reload()
    return _build_advisory_model_selection_response(request)


def _build_llm_provider_secret_injection_response(
    request: Request,
) -> LLMProviderSecretInjectionResponse:
    credential_store = _credential_store_from_state(request)
    provider_secrets = []
    for schema in LLM_PROVIDER_SECRET_SCHEMAS:
        credential = (
            credential_store.get(schema.provider_id)
            if credential_store is not None
            else None
        )
        configured = (
            credential is not None and credential.status is CredentialStatus.ACTIVE
        )
        provider_secrets.append(
            LLMProviderSecretInjectionItemResponse(
                provider_id=schema.provider_id,
                display_name=schema.display_name,
                litellm_environment_variable=schema.litellm_environment_variable,
                configured=configured,
                available_for_runtime_injection=configured,
            )
        )

    return LLMProviderSecretInjectionResponse(
        gateway_id="litellm",
        authority="operational",
        is_canonical=False,
        exposes_secret_values=False,
        runtime_decryption_boundary="composition",
        reload_semantics="credential_write_triggers_provider_reload",
        injectable_environment_variables=sorted(
            item.litellm_environment_variable
            for item in provider_secrets
            if item.available_for_runtime_injection
        ),
        provider_secrets=provider_secrets,
        lifecycle_authority=False,
        execution_authority=False,
        event_ledger_writes=False,
    )


@workspace_governance_router.get(
    "/provider-configuration",
    response_model=ProviderConfigurationResponse,
)
def get_provider_configuration(request: Request) -> ProviderConfigurationResponse:
    registry = _provider_registry_from(request)
    return ProviderConfigurationResponse(
        authority="advisory",
        providers=[
            ProviderCapabilityResponse(
                provider_id=provider.provider_id,
                capabilities=[capability.value for capability in provider.capabilities],
            )
            for provider in registry.providers
        ],
        resolutions=[
            CapabilityResolutionResponse(
                capability=capability.value,
                preferred_provider_id=resolution.preferred_provider_id,
                fallback_provider_ids=list(resolution.fallback_provider_ids),
                configured_provider_ids=list(resolution.configured_provider_ids),
                selected_provider_id=resolution.selected_provider_id,
                used_fallback=resolution.used_fallback,
                is_available=resolution.is_available,
            )
            for capability in ProviderCapability
            for resolution in (registry.resolve(capability),)
        ],
    )


@governance_router.get(
    "/provider-governance",
    response_model=ProviderGovernanceResponse,
)
def get_provider_governance(request: Request) -> ProviderGovernanceResponse:
    """Return the current provider governance read model without secrets.

    This is operational state for configuring external systems. It is not
    lifecycle truth and does not write to the canonical event ledger.
    """
    registry = _provider_registry_from(request)
    credential_store = _credential_store_from_state(request)
    registry_provider_ids = {provider.provider_id for provider in registry.providers}
    provider_ids = sorted(set(_KNOWN_PROVIDER_CAPABILITIES) | registry_provider_ids)
    ai_provider = getattr(request.app.state, "ai_advisory_provider", None)

    credential_statuses = {
        provider_id: _credential_status_for(
            provider_id,
            credential_store.get(provider_id) if credential_store is not None else None,
        )
        for provider_id in provider_ids
    }

    providers = [
        ProviderGovernanceProviderResponse(
            provider_id=provider_id,
            capabilities=list(
                _KNOWN_PROVIDER_CAPABILITIES.get(
                    provider_id,
                    tuple(
                        capability.value
                        for provider in registry.providers
                        if provider.provider_id == provider_id
                        for capability in provider.capabilities
                    ),
                )
            ),
            registry_configured=_provider_registry_configured(
                provider_id=provider_id,
                registry_provider_ids=registry_provider_ids,
                ai_provider=ai_provider,
            ),
            credential_required=credential_statuses[provider_id].credential_required,
            credential_status=credential_statuses[provider_id].status,
            health_status=_provider_health_status(
                registry_configured=_provider_registry_configured(
                    provider_id=provider_id,
                    registry_provider_ids=registry_provider_ids,
                    ai_provider=ai_provider,
                ),
                credential=credential_statuses[provider_id],
            ),
            authority="operational",
            is_canonical=False,
        )
        for provider_id in provider_ids
    ]

    routes = [
        ProviderGovernanceRouteResponse(
            capability=capability.value,
            preferred_provider_id=resolution.preferred_provider_id,
            fallback_provider_ids=list(resolution.fallback_provider_ids),
            configured_provider_ids=list(resolution.configured_provider_ids),
            selected_provider_id=resolution.selected_provider_id,
            used_fallback=resolution.used_fallback,
            is_available=resolution.is_available,
            degraded=resolution.used_fallback or not resolution.is_available,
        )
        for capability in ProviderCapability
        for resolution in (registry.resolve(capability),)
    ]

    diagnostic_classes = [
        "Provider Unreachable",
        "Credential Invalid",
        "Route Unavailable",
        "Quota Exceeded",
        "Fallback Triggered",
        "Latency Spike",
        "Validation Succeeded",
        "Validation Failed",
        "Replay Nondeterminism Warning",
    ]
    diagnostics_status: Literal["ok", "degraded", "not_configured"] = (
        "degraded" if any(route.degraded for route in routes) else "ok"
    )
    if not providers:
        diagnostics_status = "not_configured"

    return ProviderGovernanceResponse(
        authority="operational",
        is_canonical=False,
        generated_at=datetime.now(UTC),
        lifecycle_authority=False,
        event_ledger_writes=False,
        advisory_boundary=[
            "Provider governance state supports operator awareness only.",
            "External provider state is not canonical lifecycle truth.",
            "AI gateway output remains advisory and requires operator acceptance.",
        ],
        providers=providers,
        credentials=list(credential_statuses.values()),
        routes=routes,
        diagnostics=ProviderGovernanceDiagnosticSummaryResponse(
            status=diagnostics_status,
            retained_history_available=False,
            event_ledger_authority=False,
            diagnostic_classes=diagnostic_classes,
        ),
        ai_gateway=_build_ai_gateway_response(request),
    )


@governance_router.get(
    "/provider-governance/ai-gateway",
    response_model=ProviderGovernanceAIGatewayResponse,
)
def get_provider_governance_ai_gateway(
    request: Request,
) -> ProviderGovernanceAIGatewayResponse:
    """Return LiteLLM gateway route visibility without exposing API keys."""
    return _build_ai_gateway_response(request)


@governance_router.get(
    "/provider-governance/ai-gateway/model-selection",
    response_model=AdvisoryModelSelectionResponse,
)
def get_provider_governance_ai_gateway_model_selection(
    request: Request,
) -> AdvisoryModelSelectionResponse:
    """Discover LiteLLM models and return the selected advisory route config."""
    return _build_advisory_model_selection_response(request)


@governance_router.put(
    "/provider-governance/ai-gateway/model-selection",
    response_model=AdvisoryModelSelectionResponse,
)
def update_provider_governance_ai_gateway_model_selection(
    payload: AdvisoryModelSelectionPayload,
    request: Request,
) -> AdvisoryModelSelectionResponse:
    """Update global advisory primary/fallback model selection.

    This changes operational advisory routing configuration only. It does not
    write canonical events or grant AI lifecycle authority.
    """
    return _update_advisory_model_selection(request, payload)


@governance_router.get(
    "/provider-governance/ai-gateway/provider-secret-injection",
    response_model=LLMProviderSecretInjectionResponse,
)
def get_provider_governance_ai_gateway_provider_secret_injection(
    request: Request,
) -> LLMProviderSecretInjectionResponse:
    """Return managed downstream LLM provider secret injection status.

    Secret values are decrypted only into the composition-boundary environment
    projection and are never returned by this endpoint.
    """
    return _build_llm_provider_secret_injection_response(request)


@governance_router.post(
    "/provider-governance/ai-gateway/smoke-test",
    response_model=AdvisoryRouteSmokeTestResponse,
)
def smoke_test_provider_governance_ai_gateway(
    payload: AdvisoryRouteSmokeTestPayload,
    request: Request,
) -> AdvisoryRouteSmokeTestResponse:
    """Run an explicit non-canonical advisory route smoke test.

    This endpoint consumes a tiny advisory generation call. It is operational
    diagnostics only and never writes canonical decision facts.
    """
    provider = getattr(request.app.state, "ai_advisory_provider", None)
    if provider is None:
        return AdvisoryRouteSmokeTestResponse(
            gateway_id="litellm",
            status="not_configured",
            diagnostic_message=(
                "Advisory route smoke test skipped because no LiteLLM credential "
                "is configured."
            ),
            provider_id=None,
            model_id=None,
            generated_at=None,
            content_preview=None,
            authority="operational",
            is_canonical=False,
            lifecycle_authority=False,
            execution_authority=False,
            event_ledger_writes=False,
            advisory_response_authority=None,
        )

    advisory_request = AdvisoryRequest(
        request_id=f"smoke-test:{uuid.uuid4()}",
        artifact_kind=AdvisoryArtifactKind.CONTEXT_SUMMARY,
        operator_question=payload.operator_question,
        context_summary=(
            "Operational AI gateway smoke test. Confirm only that the configured "
            "advisory route can respond. Do not provide trading advice."
        ),
        source_references=(
            AdvisorySourceReference(
                source_kind=AdvisorySourceKind.OPERATOR_PROMPT,
                source_id="provider-governance:ai-gateway-smoke-test",
                description="operator-triggered non-canonical route diagnostic",
            ),
        ),
        persona_id="provider-governance",
        workspace_id="provider-governance",
        requested_at=datetime.now(UTC),
    )

    try:
        response = AIAdvisoryService(provider).generate(advisory_request)
    except AdvisoryProviderUnavailableError:
        return AdvisoryRouteSmokeTestResponse(
            gateway_id="litellm",
            status="unavailable",
            diagnostic_message=(
                "Advisory route smoke test failed because the configured route "
                "could not be reached."
            ),
            provider_id=getattr(provider, "provider_id", "litellm"),
            model_id=None,
            generated_at=None,
            content_preview=None,
            authority="operational",
            is_canonical=False,
            lifecycle_authority=False,
            execution_authority=False,
            event_ledger_writes=False,
            advisory_response_authority=None,
        )
    except Exception:
        return AdvisoryRouteSmokeTestResponse(
            gateway_id="litellm",
            status="unavailable",
            diagnostic_message=(
                "Advisory route smoke test failed before a valid advisory "
                "response was produced."
            ),
            provider_id=getattr(provider, "provider_id", "litellm"),
            model_id=None,
            generated_at=None,
            content_preview=None,
            authority="operational",
            is_canonical=False,
            lifecycle_authority=False,
            execution_authority=False,
            event_ledger_writes=False,
            advisory_response_authority=None,
        )

    return AdvisoryRouteSmokeTestResponse(
        gateway_id="litellm",
        status="available",
        diagnostic_message="Advisory route responded successfully.",
        provider_id=response.provenance.provider_id,
        model_id=response.provenance.model_id,
        generated_at=response.provenance.generated_at,
        content_preview=response.content[:240],
        authority="operational",
        is_canonical=False,
        lifecycle_authority=False,
        execution_authority=False,
        event_ledger_writes=False,
        advisory_response_authority=response.authority.value,
    )


@workspace_governance_router.put(
    "/provider-configuration/{capability}",
    response_model=ProviderConfigurationResponse,
)
def update_provider_configuration(
    request: Request,
    capability: ProviderCapability,
    payload: ProviderPreferenceRequest,
) -> ProviderConfigurationResponse:
    registry = _provider_registry_from(request)
    registry.set_preference(
        capability,
        payload.preferred_provider_id,
        tuple(payload.fallback_provider_ids),
    )
    return get_provider_configuration(request)
