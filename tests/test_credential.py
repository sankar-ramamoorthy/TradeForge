from datetime import UTC, datetime
from typing import Any, cast

import pytest
from src.security import Credential, CredentialStatus


def make_credential(
    *,
    provider_id: str = "polygon",
    credential_type: str = "api_key",
    encrypted_payload: bytes = b"encrypted",
    created_at: datetime = datetime(2026, 5, 16, tzinfo=UTC),
    rotated_at: datetime | None = None,
    last_validated_at: datetime | None = None,
    status: CredentialStatus = CredentialStatus.ACTIVE,
    provenance: dict[str, str] | None = None,
) -> Credential:
    return Credential(
        provider_id=provider_id,
        credential_type=credential_type,
        encrypted_payload=encrypted_payload,
        created_at=created_at,
        rotated_at=rotated_at,
        last_validated_at=last_validated_at,
        status=status,
        provenance=provenance or {"set_by": "operator", "source": "manual"},
    )


def test_credential_status_values_match_boundary_contract() -> None:
    assert CredentialStatus.ACTIVE.value == "active"
    assert CredentialStatus.REVOKED.value == "revoked"
    assert CredentialStatus.EXPIRED.value == "expired"
    assert CredentialStatus.UNKNOWN.value == "unknown"


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
        make_credential(**cast(dict[str, Any], {field: value}))


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
        cast(dict[str, str], credential.provenance)["set_by"] = "system"
