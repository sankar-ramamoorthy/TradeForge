from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from src.security.credential import Credential, CredentialStatus
from src.security.credential_store import CredentialStore
from src.security.key_manager import KeyManager

LITELLM_PROVIDER_ID = "litellm"
LITELLM_CREDENTIAL_TYPE = "base_url+api_key"


class LiteLLMCredentialNotConfiguredError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class LiteLLMCredentialPayload:
    base_url: str
    api_key: str
    default_model: str | None = None
    fallback_model: str | None = None

    def __post_init__(self) -> None:
        if not self.base_url.strip():
            raise ValueError("base_url must not be empty")
        if not self.api_key.strip():
            raise ValueError("api_key must not be empty")
        if self.default_model is not None and not self.default_model.strip():
            raise ValueError("default_model must not be blank when provided")
        if self.fallback_model is not None and not self.fallback_model.strip():
            raise ValueError("fallback_model must not be blank when provided")

    def as_payload(self) -> dict[str, str]:
        payload = {
            "api_key": self.api_key,
            "base_url": self.base_url,
        }
        if self.default_model is not None:
            payload["default_model"] = self.default_model
        if self.fallback_model is not None:
            payload["fallback_model"] = self.fallback_model
        return payload


def create_litellm_credential(
    payload: LiteLLMCredentialPayload,
    *,
    key_manager: KeyManager,
    set_by: str = "operator",
    source: str = "manual",
) -> Credential:
    return Credential(
        provider_id=LITELLM_PROVIDER_ID,
        credential_type=LITELLM_CREDENTIAL_TYPE,
        encrypted_payload=key_manager.encrypt_payload(payload.as_payload()),
        created_at=datetime.now(UTC),
        rotated_at=None,
        last_validated_at=None,
        status=CredentialStatus.ACTIVE,
        provenance={"set_by": set_by, "source": source},
    )


def get_litellm_credential(
    credential_store: CredentialStore,
    *,
    key_manager: KeyManager,
) -> LiteLLMCredentialPayload:
    credential = credential_store.get(LITELLM_PROVIDER_ID)
    if credential is None:
        raise LiteLLMCredentialNotConfiguredError(
            "litellm credential is not configured"
        )

    payload = key_manager.decrypt_payload(credential.encrypted_payload)
    missing_fields = {
        field
        for field in ("base_url", "api_key")
        if field not in payload
    }
    if missing_fields:
        raise ValueError(
            "litellm credential payload is missing required fields: "
            + ", ".join(sorted(missing_fields))
        )

    return LiteLLMCredentialPayload(
        base_url=payload["base_url"],
        api_key=payload["api_key"],
        default_model=payload.get("default_model") or None,
        fallback_model=payload.get("fallback_model") or None,
    )
