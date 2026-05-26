from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from src.security.credential import Credential, CredentialStatus
from src.security.credential_store import CredentialStore
from src.security.key_manager import KeyManager
from src.security.litellm_credential import get_litellm_credential

ADVISORY_MODEL_SELECTION_PROVIDER_ID = "advisory_model_selection"
ADVISORY_MODEL_SELECTION_CREDENTIAL_TYPE = "provider_model_pairs"


@dataclass(frozen=True, slots=True)
class AdvisoryModelSelectionConfig:
    primary_provider_id: str
    primary_model: str
    fallback_provider_id: str | None = None
    fallback_model: str | None = None
    legacy_inferred: bool = False

    def __post_init__(self) -> None:
        if not self.primary_provider_id.strip():
            raise ValueError("primary_provider_id must not be empty")
        if not self.primary_model.strip():
            raise ValueError("primary_model must not be empty")
        if (self.fallback_provider_id is None) != (self.fallback_model is None):
            raise ValueError(
                "fallback_provider_id and fallback_model must be provided together"
            )
        if (
            self.fallback_provider_id is not None
            and not self.fallback_provider_id.strip()
        ):
            raise ValueError("fallback_provider_id must not be blank when provided")
        if self.fallback_model is not None and not self.fallback_model.strip():
            raise ValueError("fallback_model must not be blank when provided")

    def as_payload(self) -> dict[str, str]:
        payload = {
            "primary_provider_id": self.primary_provider_id,
            "primary_model": self.primary_model,
        }
        if self.fallback_provider_id is not None and self.fallback_model is not None:
            payload["fallback_provider_id"] = self.fallback_provider_id
            payload["fallback_model"] = self.fallback_model
        return payload


def infer_legacy_provider_id(model_id: str | None) -> str | None:
    if model_id is None or "/" not in model_id:
        return None
    prefix = model_id.split("/", 1)[0].strip()
    return {
        "groq": "llm_groq",
        "nvidia_nim": "llm_nvidia_nim",
        "openai": "llm_openai",
        "anthropic": "llm_anthropic",
        "gemini": "llm_google",
        "ollama": "ollama",
    }.get(prefix)


def create_advisory_model_selection_credential(
    config: AdvisoryModelSelectionConfig,
    *,
    key_manager: KeyManager,
    existing: Credential | None = None,
) -> Credential:
    now = datetime.now(UTC)
    return Credential(
        provider_id=ADVISORY_MODEL_SELECTION_PROVIDER_ID,
        credential_type=ADVISORY_MODEL_SELECTION_CREDENTIAL_TYPE,
        encrypted_payload=key_manager.encrypt_payload(config.as_payload()),
        created_at=existing.created_at if existing is not None else now,
        rotated_at=now if existing is not None else None,
        last_validated_at=None,
        status=CredentialStatus.ACTIVE,
        provenance=(
            existing.provenance
            if existing is not None
            else {"set_by": "operator", "source": "provider-governance"}
        ),
    )


def get_advisory_model_selection_config(
    credential_store: CredentialStore,
    *,
    key_manager: KeyManager,
) -> AdvisoryModelSelectionConfig | None:
    credential = credential_store.get(ADVISORY_MODEL_SELECTION_PROVIDER_ID)
    if credential is not None and credential.status is CredentialStatus.ACTIVE:
        payload = key_manager.decrypt_payload(credential.encrypted_payload)
        return AdvisoryModelSelectionConfig(
            primary_provider_id=payload["primary_provider_id"],
            primary_model=payload["primary_model"],
            fallback_provider_id=payload.get("fallback_provider_id") or None,
            fallback_model=payload.get("fallback_model") or None,
        )

    legacy = get_litellm_credential(credential_store, key_manager=key_manager)
    if legacy.default_model is None:
        return None
    return AdvisoryModelSelectionConfig(
        primary_provider_id=infer_legacy_provider_id(legacy.default_model) or "legacy",
        primary_model=legacy.default_model,
        fallback_provider_id=(
            infer_legacy_provider_id(legacy.fallback_model) or "legacy"
            if legacy.fallback_model is not None
            else None
        ),
        fallback_model=legacy.fallback_model,
        legacy_inferred=True,
    )


def save_advisory_model_selection_config(
    credential_store: CredentialStore,
    config: AdvisoryModelSelectionConfig,
    *,
    key_manager: KeyManager,
) -> None:
    existing = credential_store.get(ADVISORY_MODEL_SELECTION_PROVIDER_ID)
    credential_store.save(
        create_advisory_model_selection_credential(
            config,
            key_manager=key_manager,
            existing=existing,
        )
    )
