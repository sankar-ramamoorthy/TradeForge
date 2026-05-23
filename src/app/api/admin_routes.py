from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel, Field
from src.security import CredentialStore, KeyManager
from src.security.credential import Credential, CredentialStatus
from src.security.key_manager import MasterKeyNotConfiguredError

admin_router = APIRouter(prefix="/admin", tags=["admin"])

# Static registry of all known providers and their credential field names.
# This mirrors PROVIDER_CREDENTIAL_SCHEMAS in the frontend.
_PROVIDER_FIELD_NAMES: dict[str, list[str]] = {
    "yfinance": [],
    "polygon": ["api_key"],
    "alpaca": ["api_key", "secret_key"],
    "fmp": ["api_key"],
    "alpha_vantage": ["api_key"],
    "litellm": ["base_url", "api_key", "default_model"],
}

_SECRET_FIELDS = frozenset({"api_key", "secret_key"})


def _mask(value: str) -> str:
    """Return the last 4 characters of a secret field, prefixed with bullets."""
    if len(value) <= 4:
        return "••••"
    return "••••" + value[-4:]


def _key_manager() -> KeyManager:
    try:
        return KeyManager.from_environment()
    except MasterKeyNotConfiguredError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "TRADEFORGE_MASTER_KEY is not configured. "
                "Set it in the OS environment before managing credentials."
            ),
        ) from exc


def _credential_store_from(request: Request) -> CredentialStore:
    """Return the live credential store, creating .keys.enc if it doesn't exist yet."""
    store: CredentialStore | None = request.app.state.credential_store
    if store is not None:
        return store
    store = CredentialStore(Path(".keys.enc"))
    request.app.state.credential_store = store
    request.app.state.provider_bootstrap.set_credential_store(store)
    return store


# --------------------------------------------------------------------------- #
# Response models                                                               #
# --------------------------------------------------------------------------- #


class CredentialFieldResponse(BaseModel):
    name: str
    masked_value: str | None
    display_value: str | None


class CredentialStatusResponse(BaseModel):
    provider_id: str
    configured: bool
    status: str | None
    rotated_at: str | None
    fields: list[CredentialFieldResponse]
    master_key_configured: bool


class CredentialListResponse(BaseModel):
    credentials: list[CredentialStatusResponse]
    master_key_configured: bool


class UpdateCredentialPayload(BaseModel):
    fields: dict[str, str] = Field(min_length=1)


# --------------------------------------------------------------------------- #
# Helpers                                                                       #
# --------------------------------------------------------------------------- #


def _build_status(
    provider_id: str,
    credential: Credential | None,
    key_manager: KeyManager | None,
) -> CredentialStatusResponse:
    field_names = _PROVIDER_FIELD_NAMES.get(provider_id, [])

    if not field_names:
        # yfinance: always available, no credential needed
        return CredentialStatusResponse(
            provider_id=provider_id,
            configured=True,
            status="active",
            rotated_at=None,
            fields=[],
            master_key_configured=key_manager is not None,
        )

    if credential is None:
        return CredentialStatusResponse(
            provider_id=provider_id,
            configured=False,
            status=None,
            rotated_at=None,
            fields=[
                CredentialFieldResponse(name=n, masked_value=None, display_value=None)
                for n in field_names
            ],
            master_key_configured=key_manager is not None,
        )

    # Decrypt to build masked display
    fields: list[CredentialFieldResponse] = []
    if key_manager is not None:
        try:
            payload = key_manager.decrypt_payload(credential.encrypted_payload)
            for name in field_names:
                value = payload.get(name, "")
                if name in _SECRET_FIELDS:
                    fields.append(
                        CredentialFieldResponse(
                            name=name,
                            masked_value=_mask(value) if value else None,
                            display_value=None,
                        )
                    )
                else:
                    fields.append(
                        CredentialFieldResponse(
                            name=name,
                            masked_value=None,
                            display_value=value or None,
                        )
                    )
        except Exception:  # noqa: BLE001
            fields = [
                CredentialFieldResponse(name=n, masked_value=None, display_value=None)
                for n in field_names
            ]
    else:
        fields = [
            CredentialFieldResponse(name=n, masked_value=None, display_value=None)
            for n in field_names
        ]

    return CredentialStatusResponse(
        provider_id=provider_id,
        configured=credential.status is CredentialStatus.ACTIVE,
        status=credential.status.value,
        rotated_at=(
            credential.rotated_at.isoformat()
            if credential.rotated_at is not None
            else None
        ),
        fields=fields,
        master_key_configured=key_manager is not None,
    )


# --------------------------------------------------------------------------- #
# Routes                                                                        #
# --------------------------------------------------------------------------- #


@admin_router.get("/credentials", response_model=CredentialListResponse)
def list_credentials(request: Request) -> CredentialListResponse:
    """List all known providers with configured status and masked field values.

    Secrets are never returned. Only the last 4 characters of secret fields
    are shown. Non-secret fields (e.g., LiteLLM base_url) are shown in full.
    """
    try:
        key_manager: KeyManager | None = KeyManager.from_environment()
    except MasterKeyNotConfiguredError:
        key_manager = None

    store: CredentialStore | None = request.app.state.credential_store
    credentials: list[CredentialStatusResponse] = []

    for provider_id in _PROVIDER_FIELD_NAMES:
        existing = store.get(provider_id) if store is not None else None
        credentials.append(_build_status(provider_id, existing, key_manager))

    return CredentialListResponse(
        credentials=credentials,
        master_key_configured=key_manager is not None,
    )


@admin_router.put(
    "/credentials/{provider_id}",
    response_model=CredentialStatusResponse,
    status_code=status.HTTP_200_OK,
)
def update_credential(
    provider_id: str,
    payload: UpdateCredentialPayload,
    request: Request,
) -> CredentialStatusResponse:
    """Save or update a provider credential, then reload providers in-process.

    The master key must be configured in the OS environment. Secrets are
    encrypted before storage. Providers reload automatically — no restart needed.
    """
    if provider_id not in _PROVIDER_FIELD_NAMES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"unknown provider: '{provider_id}'",
        )

    expected_fields = _PROVIDER_FIELD_NAMES[provider_id]
    if not expected_fields:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"provider '{provider_id}' requires no credentials",
        )

    missing = [f for f in expected_fields if f not in payload.fields]
    if missing:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"missing credential fields: {missing}",
        )

    key_manager = _key_manager()
    store = _credential_store_from(request)
    existing = store.get(provider_id)
    now = datetime.now(UTC)

    credential_type = "+".join(sorted(payload.fields.keys()))
    new_credential = Credential(
        provider_id=provider_id,
        credential_type=credential_type,
        encrypted_payload=key_manager.encrypt_payload(dict(payload.fields)),
        created_at=existing.created_at if existing is not None else now,
        rotated_at=now if existing is not None else None,
        last_validated_at=None,
        status=CredentialStatus.ACTIVE,
        provenance={"set_by": "operator", "source": "ui"},
    )

    store.save(new_credential)
    request.app.state.provider_bootstrap.reload()

    return _build_status(provider_id, new_credential, key_manager)


@admin_router.delete(
    "/credentials/{provider_id}",
    status_code=status.HTTP_200_OK,
    response_model=CredentialStatusResponse,
)
def revoke_credential(
    provider_id: str,
    request: Request,
) -> CredentialStatusResponse:
    """Revoke a provider credential and reload providers in-process.

    The credential record is retained for audit trail with status=revoked.
    """
    if provider_id not in _PROVIDER_FIELD_NAMES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"unknown provider: '{provider_id}'",
        )

    key_manager = _key_manager()
    store = _credential_store_from(request)
    existing = store.get(provider_id)

    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no credential configured for provider '{provider_id}'",
        )

    revoked = Credential(
        provider_id=existing.provider_id,
        credential_type=existing.credential_type,
        encrypted_payload=existing.encrypted_payload,
        created_at=existing.created_at,
        rotated_at=existing.rotated_at,
        last_validated_at=existing.last_validated_at,
        status=CredentialStatus.REVOKED,
        provenance=existing.provenance,
    )

    store.save(revoked)
    request.app.state.provider_bootstrap.reload()

    return _build_status(provider_id, revoked, key_manager)
