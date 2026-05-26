from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType

from src.security.credential import CredentialStatus
from src.security.credential_store import CredentialStore
from src.security.key_manager import KeyManager


@dataclass(frozen=True, slots=True)
class LLMProviderSecretSchema:
    provider_id: str
    display_name: str
    litellm_environment_variable: str


LLM_PROVIDER_SECRET_SCHEMAS: tuple[LLMProviderSecretSchema, ...] = (
    LLMProviderSecretSchema("llm_groq", "Groq", "GROQ_API_KEY"),
    LLMProviderSecretSchema("llm_nvidia_nim", "NVIDIA NIM", "NVIDIA_NIM_API_KEY"),
    LLMProviderSecretSchema("llm_openai", "OpenAI", "OPENAI_API_KEY"),
    LLMProviderSecretSchema("llm_anthropic", "Anthropic", "ANTHROPIC_API_KEY"),
    LLMProviderSecretSchema("llm_google", "Google", "GOOGLE_API_KEY"),
)

LLM_PROVIDER_SECRET_SCHEMA_BY_ID = MappingProxyType(
    {schema.provider_id: schema for schema in LLM_PROVIDER_SECRET_SCHEMAS}
)


def build_litellm_provider_environment(
    credential_store: CredentialStore | None,
    *,
    key_manager: KeyManager,
) -> dict[str, str]:
    """Build decrypted LiteLLM provider environment at composition time only."""
    if credential_store is None:
        return {}

    environment: dict[str, str] = {}
    for schema in LLM_PROVIDER_SECRET_SCHEMAS:
        credential = credential_store.get(schema.provider_id)
        if credential is None or credential.status is not CredentialStatus.ACTIVE:
            continue
        payload = key_manager.decrypt_payload(credential.encrypted_payload)
        api_key = payload.get("api_key", "").strip()
        if api_key:
            environment[schema.litellm_environment_variable] = api_key
    return environment
