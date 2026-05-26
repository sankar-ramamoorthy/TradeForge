from datetime import UTC, datetime
from pathlib import Path

from cryptography.fernet import Fernet
from src.security import Credential, CredentialStatus, CredentialStore, KeyManager
from src.security.llm_provider_secrets import build_litellm_provider_environment


def _secret_credential(
    provider_id: str,
    api_key: str,
    *,
    key_manager: KeyManager,
    status: CredentialStatus = CredentialStatus.ACTIVE,
) -> Credential:
    return Credential(
        provider_id=provider_id,
        credential_type="api_key",
        encrypted_payload=key_manager.encrypt_payload({"api_key": api_key}),
        created_at=datetime(2026, 5, 25, tzinfo=UTC),
        rotated_at=None,
        last_validated_at=None,
        status=status,
        provenance={"set_by": "operator", "source": "test"},
    )


def test_build_litellm_provider_environment_decrypts_active_llm_provider_keys(
    tmp_path: Path,
) -> None:
    key_manager = KeyManager(Fernet.generate_key())
    store = CredentialStore(tmp_path / ".keys.enc")
    store.save(
        _secret_credential(
            "llm_groq",
            "groq-secret",
            key_manager=key_manager,
        )
    )
    store.save(
        _secret_credential(
            "llm_openai",
            "openai-secret",
            key_manager=key_manager,
        )
    )

    environment = build_litellm_provider_environment(
        store,
        key_manager=key_manager,
    )

    assert environment == {
        "GROQ_API_KEY": "groq-secret",
        "OPENAI_API_KEY": "openai-secret",
    }


def test_build_litellm_provider_environment_skips_revoked_secrets(
    tmp_path: Path,
) -> None:
    key_manager = KeyManager(Fernet.generate_key())
    store = CredentialStore(tmp_path / ".keys.enc")
    store.save(
        _secret_credential(
            "llm_groq",
            "groq-secret",
            key_manager=key_manager,
            status=CredentialStatus.REVOKED,
        )
    )

    assert build_litellm_provider_environment(store, key_manager=key_manager) == {}
