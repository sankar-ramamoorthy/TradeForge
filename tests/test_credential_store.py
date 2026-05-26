from datetime import UTC, datetime
from pathlib import Path

import pytest
from cryptography.fernet import Fernet
from src.security import (
    LITELLM_CREDENTIAL_TYPE,
    LITELLM_PROVIDER_ID,
    Credential,
    CredentialStatus,
    CredentialStore,
    KeyManager,
    LiteLLMCredentialNotConfiguredError,
    LiteLLMCredentialPayload,
    create_litellm_credential,
    get_litellm_credential,
)


def make_credential(
    *,
    provider_id: str,
    status: CredentialStatus,
    key_manager: KeyManager,
) -> Credential:
    return Credential(
        provider_id=provider_id,
        credential_type="api_key",
        encrypted_payload=key_manager.encrypt_payload(
            {"api_key": f"{provider_id}-key"}
        ),
        created_at=datetime(2026, 5, 16, tzinfo=UTC),
        rotated_at=None,
        last_validated_at=None,
        status=status,
        provenance={"set_by": "operator", "source": "manual"},
    )


def test_credential_store_writes_and_reads_credentials(tmp_path: Path) -> None:
    key_manager = KeyManager(Fernet.generate_key())
    store = CredentialStore(tmp_path / ".keys.enc")
    credential = make_credential(
        provider_id="polygon",
        status=CredentialStatus.ACTIVE,
        key_manager=key_manager,
    )

    store.save(credential)

    loaded = store.get("polygon")
    assert loaded == credential
    assert loaded is not None
    assert key_manager.decrypt_payload(loaded.encrypted_payload) == {
        "api_key": "polygon-key"
    }


def test_credential_store_filters_by_status(tmp_path: Path) -> None:
    key_manager = KeyManager(Fernet.generate_key())
    store = CredentialStore(tmp_path / ".keys.enc")
    store.save(
        make_credential(
            provider_id="polygon",
            status=CredentialStatus.ACTIVE,
            key_manager=key_manager,
        )
    )
    store.save(
        make_credential(
            provider_id="finqual",
            status=CredentialStatus.REVOKED,
            key_manager=key_manager,
        )
    )

    assert tuple(
        credential.provider_id
        for credential in store.list_credentials(status=CredentialStatus.ACTIVE)
    ) == ("polygon",)
    assert tuple(
        credential.provider_id
        for credential in store.list_credentials(status=CredentialStatus.REVOKED)
    ) == ("finqual",)


def test_credential_store_writes_and_reads_litellm_credentials(
    tmp_path: Path,
) -> None:
    key_manager = KeyManager(Fernet.generate_key())
    store = CredentialStore(tmp_path / ".keys.enc")
    credential = create_litellm_credential(
        LiteLLMCredentialPayload(
            base_url="http://localhost:4000",
            api_key="litellm-key",
            default_model="configured-model",
        ),
        key_manager=key_manager,
    )

    store.save(credential)

    loaded = store.get(LITELLM_PROVIDER_ID)
    assert loaded is not None
    assert loaded.provider_id == LITELLM_PROVIDER_ID
    assert loaded.credential_type == LITELLM_CREDENTIAL_TYPE
    assert key_manager.decrypt_payload(loaded.encrypted_payload) == {
        "api_key": "litellm-key",
        "base_url": "http://localhost:4000",
        "default_model": "configured-model",
    }
    assert get_litellm_credential(store, key_manager=key_manager) == (
        LiteLLMCredentialPayload(
            base_url="http://localhost:4000",
            api_key="litellm-key",
            default_model="configured-model",
        )
    )


def test_credential_store_writes_and_reads_litellm_fallback_model(
    tmp_path: Path,
) -> None:
    key_manager = KeyManager(Fernet.generate_key())
    store = CredentialStore(tmp_path / ".keys.enc")
    credential = create_litellm_credential(
        LiteLLMCredentialPayload(
            base_url="http://localhost:4000",
            api_key="litellm-key",
            default_model="primary-model",
            fallback_model="fallback-model",
        ),
        key_manager=key_manager,
    )

    store.save(credential)

    assert key_manager.decrypt_payload(credential.encrypted_payload) == {
        "api_key": "litellm-key",
        "base_url": "http://localhost:4000",
        "default_model": "primary-model",
        "fallback_model": "fallback-model",
    }
    assert get_litellm_credential(store, key_manager=key_manager) == (
        LiteLLMCredentialPayload(
            base_url="http://localhost:4000",
            api_key="litellm-key",
            default_model="primary-model",
            fallback_model="fallback-model",
        )
    )


def test_litellm_credential_retrieval_fails_when_not_configured(
    tmp_path: Path,
) -> None:
    key_manager = KeyManager(Fernet.generate_key())
    store = CredentialStore(tmp_path / ".keys.enc")

    with pytest.raises(
        LiteLLMCredentialNotConfiguredError,
        match="litellm credential is not configured",
    ):
        get_litellm_credential(store, key_manager=key_manager)
