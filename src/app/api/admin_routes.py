from __future__ import annotations

import os
from datetime import UTC, datetime
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel, Field
from src.security import (
    LLM_PROVIDER_SECRET_SCHEMAS,
    CredentialStore,
    KeyManager,
)
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
    "litellm": ["base_url", "api_key"],
    **{
        schema.provider_id: ["api_key"]
        for schema in LLM_PROVIDER_SECRET_SCHEMAS
    },
}

_SECRET_FIELDS = frozenset({"api_key", "secret_key"})
_RUNTIME_ENV_FILE_ENV_VAR = "TRADEFORGE_RUNTIME_ENV_FILE"
_DEFAULT_RUNTIME_ENV_FILE = ".tradeforge/runtime.env"


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
    last_validated_at: str | None
    fields: list[CredentialFieldResponse]
    master_key_configured: bool


class CredentialListResponse(BaseModel):
    credentials: list[CredentialStatusResponse]
    master_key_configured: bool


class UpdateCredentialPayload(BaseModel):
    fields: dict[str, str] = Field(min_length=1)


class SetupStatusResponse(BaseModel):
    requires_setup: bool
    master_key_configured: bool
    credential_store_exists: bool
    runtime_env_file_path: str
    can_persist_runtime_env_file: bool


class SetupMasterKeyResponse(BaseModel):
    master_key: str
    status: SetupStatusResponse


# --------------------------------------------------------------------------- #
# Helpers                                                                       #
# --------------------------------------------------------------------------- #


def _runtime_env_file_path() -> Path:
    return Path(os.environ.get(_RUNTIME_ENV_FILE_ENV_VAR, _DEFAULT_RUNTIME_ENV_FILE))


def _credential_store_exists(request: Request) -> bool:
    store: CredentialStore | None = request.app.state.credential_store
    if store is not None and tuple(store.list_credentials()):
        return True
    return Path(".keys.enc").exists()


def _setup_status(request: Request) -> SetupStatusResponse:
    master_key_configured = bool(os.environ.get(KeyManager.ENV_VAR_NAME))
    credential_store_exists = _credential_store_exists(request)
    runtime_env_file = _runtime_env_file_path()
    return SetupStatusResponse(
        requires_setup=not master_key_configured and not credential_store_exists,
        master_key_configured=master_key_configured,
        credential_store_exists=credential_store_exists,
        runtime_env_file_path=str(runtime_env_file),
        can_persist_runtime_env_file=True,
    )


def _persist_runtime_master_key(master_key: str) -> Path:
    runtime_env_file = _runtime_env_file_path()
    runtime_env_file.parent.mkdir(parents=True, exist_ok=True)
    runtime_env_file.write_text(
        f"{KeyManager.ENV_VAR_NAME}={master_key}\n",
        encoding="utf-8",
    )
    try:
        runtime_env_file.chmod(0o600)
    except OSError:
        pass
    return runtime_env_file


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
            last_validated_at=None,
            fields=[],
            master_key_configured=key_manager is not None,
        )

    if credential is None:
        return CredentialStatusResponse(
            provider_id=provider_id,
            configured=False,
            status=None,
            rotated_at=None,
            last_validated_at=None,
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
        last_validated_at=(
            credential.last_validated_at.isoformat()
            if credential.last_validated_at is not None
            else None
        ),
        fields=fields,
        master_key_configured=key_manager is not None,
    )


# --------------------------------------------------------------------------- #
# Routes                                                                        #
# --------------------------------------------------------------------------- #


@admin_router.get("/setup/status", response_model=SetupStatusResponse)
def setup_status(request: Request) -> SetupStatusResponse:
    """Report whether first-run master key setup is currently allowed."""
    return _setup_status(request)


@admin_router.post(
    "/setup/master-key",
    response_model=SetupMasterKeyResponse,
    status_code=status.HTTP_201_CREATED,
)
def setup_master_key(request: Request) -> SetupMasterKeyResponse:
    """Generate a first-run master key and persist it to the local runtime env file.

    This route is available only before a master key or credential store exists.
    The generated key is returned once so the operator can record it.
    """
    current_status = _setup_status(request)
    if not current_status.requires_setup:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "first-run setup is available only before a master key or "
                "credential store exists"
            ),
        )

    master_key = KeyManager.generate_master_key()
    _persist_runtime_master_key(master_key)
    os.environ[KeyManager.ENV_VAR_NAME] = master_key
    store = CredentialStore(Path(".keys.enc"))
    request.app.state.credential_store = store
    request.app.state.provider_bootstrap.set_credential_store(store)

    return SetupMasterKeyResponse(
        master_key=master_key,
        status=_setup_status(request),
    )


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
    normalized_fields = {
        key: value
        for key, value in payload.fields.items()
        if not (provider_id == "litellm" and key == "fallback_model" and not value)
    }
    if not expected_fields:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"provider '{provider_id}' requires no credentials",
        )

    required_fields = [
        field
        for field in expected_fields
        if not (provider_id == "litellm" and field == "fallback_model")
    ]
    missing = [f for f in required_fields if f not in normalized_fields]
    if missing:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"missing credential fields: {missing}",
        )

    key_manager = _key_manager()
    store = _credential_store_from(request)
    existing = store.get(provider_id)
    now = datetime.now(UTC)

    credential_type = "+".join(sorted(normalized_fields.keys()))
    new_credential = Credential(
        provider_id=provider_id,
        credential_type=credential_type,
        encrypted_payload=key_manager.encrypt_payload(normalized_fields),
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


@admin_router.post(
    "/credentials/{provider_id}/validate",
    status_code=status.HTTP_200_OK,
    response_model=CredentialStatusResponse,
)
def validate_credential(
    provider_id: str,
    request: Request,
) -> CredentialStatusResponse:
    """Validate a saved credential structurally without returning secrets."""
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

    key_manager = _key_manager()
    store = _credential_store_from(request)
    existing = store.get(provider_id)
    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no credential configured for provider '{provider_id}'",
        )
    if existing.status is CredentialStatus.REVOKED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"credential for provider '{provider_id}' is revoked",
        )

    now = datetime.now(UTC)
    try:
        payload = key_manager.decrypt_payload(existing.encrypted_payload)
        required_fields = [
            field
            for field in expected_fields
            if not (provider_id == "litellm" and field == "fallback_model")
        ]
        missing_or_blank = [
            field for field in required_fields if not payload.get(field, "").strip()
        ]
        if missing_or_blank:
            raise ValueError(
                "credential payload is missing required fields: "
                + ", ".join(missing_or_blank)
            )
    except Exception:  # noqa: BLE001
        invalid = Credential(
            provider_id=existing.provider_id,
            credential_type=existing.credential_type,
            encrypted_payload=existing.encrypted_payload,
            created_at=existing.created_at,
            rotated_at=existing.rotated_at,
            last_validated_at=None,
            status=CredentialStatus.INVALID,
            provenance=existing.provenance,
        )
        store.save(invalid)
        request.app.state.provider_bootstrap.reload()
        return _build_status(provider_id, invalid, key_manager)

    validated = Credential(
        provider_id=existing.provider_id,
        credential_type=existing.credential_type,
        encrypted_payload=existing.encrypted_payload,
        created_at=existing.created_at,
        rotated_at=existing.rotated_at,
        last_validated_at=now,
        status=CredentialStatus.ACTIVE,
        provenance=existing.provenance,
    )
    store.save(validated)
    request.app.state.provider_bootstrap.reload()
    return _build_status(provider_id, validated, key_manager)
