from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from types import MappingProxyType


class CredentialStatus(StrEnum):
    ACTIVE = "active"
    REVOKED = "revoked"
    EXPIRED = "expired"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class Credential:
    """Immutable credential metadata carried by the security boundary.

    The encrypted payload remains opaque to consumers outside `src.security`.
    Future issues add storage and decryption; this model only defines the
    stable domain shape and validation rules agreed in ADR-0037.
    """

    provider_id: str
    credential_type: str
    encrypted_payload: bytes
    created_at: datetime
    rotated_at: datetime | None
    last_validated_at: datetime | None
    status: CredentialStatus
    provenance: Mapping[str, str]

    def __post_init__(self) -> None:
        if not self.provider_id.strip():
            raise ValueError("provider_id must not be empty")
        if not self.credential_type.strip():
            raise ValueError("credential_type must not be empty")
        if not self.encrypted_payload:
            raise ValueError("encrypted_payload must not be empty")
        if self.rotated_at is not None and self.rotated_at < self.created_at:
            raise ValueError("rotated_at must not be earlier than created_at")
        if (
            self.last_validated_at is not None
            and self.last_validated_at < self.created_at
        ):
            raise ValueError("last_validated_at must not be earlier than created_at")

        object.__setattr__(
            self,
            "provenance",
            MappingProxyType(dict(self.provenance)),
        )
