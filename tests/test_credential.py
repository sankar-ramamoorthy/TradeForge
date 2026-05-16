from datetime import UTC, datetime

import pytest
from src.security import Credential, CredentialStatus


def make_credential(**overrides: object) -> Credential:
    values: dict[str, object] = {
        "provider_id": "polygon",
        "credential_type": "api_key",
        "encrypted_payload": b"encrypted",
        "created_at": datetime(2026, 5, 16, tzinfo=UTC),
        "rotated_at": None,
        "last_validated_at": None,
        "status": CredentialStatus.ACTIVE,
        "provenance": {"set_by": "operator", "source": "manual"},
    }
    values.update(overrides)
    return Credential(**values)


def test_credential_status_values_match_boundary_contract() -> None:
    assert CredentialStatus.ACTIVE == "active"
    assert CredentialStatus.REVOKED == "revoked"
    assert CredentialStatus.EXPIRED == "expired"
    assert CredentialStatus.UNKNOWN == "unknown"


def test_credential_accepts_replay_relevant_metadata() -> None:
    rotated_at = datetime(2026, 5, 17, tzinfo=UTC)
    last_validated_at = datetime(2026, 5, 18, tzinfo=UTC)

    credential = make_credential(
        rotated_at=rotated_at,
        last_validated_at=last_validated_at,
        status=CredentialStatus.UNKNOWN,
    )

    assert credential.provider_id == "polygon"
    assert credential.credential_type == "api_key"
    assert credential.rotated_at == rotated_at
    assert credential.last_validated_at == last_validated_at
    assert credential.status is CredentialStatus.UNKNOWN
    assert dict(credential.provenance) == {"set_by": "operator", "source": "manual"}


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("provider_id", "   ", "provider_id must not be empty"),
        ("credential_type", "", "credential_type must not be empty"),
        ("encrypted_payload", b"", "encrypted_payload must not be empty"),
    ],
)
def test_credential_rejects_required_empty_values(
    field: str,
    value: object,
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        make_credential(**{field: value})


def test_credential_rejects_replay_timestamps_before_creation() -> None:
    with pytest.raises(
        ValueError,
        match="rotated_at must not be earlier than created_at",
    ):
        make_credential(rotated_at=datetime(2026, 5, 15, tzinfo=UTC))

    with pytest.raises(
        ValueError,
        match="last_validated_at must not be earlier than created_at",
    ):
        make_credential(last_validated_at=datetime(2026, 5, 15, tzinfo=UTC))


def test_credential_provenance_is_immutable_after_creation() -> None:
    credential = make_credential()

    with pytest.raises(TypeError):
        credential.provenance["set_by"] = "system"
