from datetime import UTC, datetime
from pathlib import Path

from cryptography.fernet import Fernet
from src.security import Credential, CredentialStatus, CredentialStore, KeyManager


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
