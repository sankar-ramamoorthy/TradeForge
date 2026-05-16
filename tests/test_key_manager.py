import pytest
from cryptography.fernet import Fernet
from src.security import (
    InvalidCredentialPayloadError,
    KeyManager,
    MasterKeyNotConfiguredError,
)


def test_key_manager_encrypts_and_decrypts_payloads() -> None:
    key_manager = KeyManager(Fernet.generate_key())

    encrypted = key_manager.encrypt_payload(
        {"api_key": "polygon-key", "secret_key": "alpaca-secret"}
    )

    assert encrypted != b'{"api_key":"polygon-key","secret_key":"alpaca-secret"}'
    assert key_manager.decrypt_payload(encrypted) == {
        "api_key": "polygon-key",
        "secret_key": "alpaca-secret",
    }


def test_key_manager_from_environment_requires_master_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("TRADEFORGE_MASTER_KEY", raising=False)

    with pytest.raises(
        MasterKeyNotConfiguredError,
        match="TRADEFORGE_MASTER_KEY is required",
    ):
        KeyManager.from_environment()


def test_key_manager_rejects_wrong_master_key() -> None:
    encrypted = KeyManager(Fernet.generate_key()).encrypt_payload(
        {"api_key": "polygon-key"}
    )
    wrong_key_manager = KeyManager(Fernet.generate_key())

    with pytest.raises(
        InvalidCredentialPayloadError,
        match="credential payload could not be decrypted",
    ):
        wrong_key_manager.decrypt_payload(encrypted)
