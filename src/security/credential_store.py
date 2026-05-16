from __future__ import annotations

import base64
import json
from collections.abc import Iterable
from datetime import datetime
from pathlib import Path
from typing import Any

from src.security.credential import Credential, CredentialStatus


class CredentialStore:
    """JSON-backed local registry for encrypted provider credentials."""

    def __init__(self, path: Path | str = ".keys.enc") -> None:
        self._path = Path(path)

    def save(self, credential: Credential) -> None:
        credentials = {
            item.provider_id: item
            for item in self.list_credentials()
        }
        credentials[credential.provider_id] = credential
        self._write_credentials(credentials.values())

    def get(self, provider_id: str) -> Credential | None:
        for credential in self.list_credentials():
            if credential.provider_id == provider_id:
                return credential
        return None

    def list_credentials(
        self,
        *,
        status: CredentialStatus | None = None,
    ) -> tuple[Credential, ...]:
        credentials = tuple(self._read_credentials())
        if status is None:
            return credentials
        return tuple(
            credential
            for credential in credentials
            if credential.status is status
        )

    def _read_credentials(self) -> Iterable[Credential]:
        if not self._path.exists():
            return ()

        raw = json.loads(self._path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise ValueError("credential store must contain a JSON object")

        raw_credentials = raw.get("credentials", [])
        if not isinstance(raw_credentials, list):
            raise ValueError("credential store credentials must be a list")

        return tuple(self._credential_from_record(record) for record in raw_credentials)

    def _write_credentials(self, credentials: Iterable[Credential]) -> None:
        records = [
            self._credential_to_record(credential)
            for credential in sorted(credentials, key=lambda item: item.provider_id)
        ]
        payload = {"version": 1, "credentials": records}
        self._path.write_text(
            json.dumps(payload, indent=2, sort_keys=True),
            encoding="utf-8",
        )

    @staticmethod
    def _credential_to_record(credential: Credential) -> dict[str, Any]:
        return {
            "provider_id": credential.provider_id,
            "credential_type": credential.credential_type,
            "encrypted_payload": base64.b64encode(
                credential.encrypted_payload
            ).decode("ascii"),
            "created_at": credential.created_at.isoformat(),
            "rotated_at": (
                credential.rotated_at.isoformat()
                if credential.rotated_at is not None
                else None
            ),
            "last_validated_at": (
                credential.last_validated_at.isoformat()
                if credential.last_validated_at is not None
                else None
            ),
            "status": credential.status.value,
            "provenance": dict(credential.provenance),
        }

    @staticmethod
    def _credential_from_record(record: object) -> Credential:
        if not isinstance(record, dict):
            raise ValueError("credential records must be JSON objects")

        return Credential(
            provider_id=str(record["provider_id"]),
            credential_type=str(record["credential_type"]),
            encrypted_payload=base64.b64decode(str(record["encrypted_payload"])),
            created_at=datetime.fromisoformat(str(record["created_at"])),
            rotated_at=(
                datetime.fromisoformat(str(record["rotated_at"]))
                if record.get("rotated_at") is not None
                else None
            ),
            last_validated_at=(
                datetime.fromisoformat(str(record["last_validated_at"]))
                if record.get("last_validated_at") is not None
                else None
            ),
            status=CredentialStatus(str(record["status"])),
            provenance={
                str(key): str(value)
                for key, value in dict(record.get("provenance", {})).items()
            },
        )
