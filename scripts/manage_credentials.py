from __future__ import annotations

import argparse
import sys
from datetime import UTC, datetime
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.security import (
    LLM_PROVIDER_SECRET_SCHEMAS,
    Credential,
    CredentialStatus,
    CredentialStore,
    KeyManager,
    LiteLLMCredentialPayload,
    create_litellm_credential,
)

PROVIDER_FIELDS: dict[str, tuple[str, str]] = {
    "polygon": ("api_key", "api_key"),
    "alpaca": ("api_key+secret", "api_key,secret_key"),
    "alpha_vantage": ("api_key", "api_key"),
    "fmp": ("api_key", "api_key"),
    "finqual": ("api_key", "api_key"),
    "litellm": ("base_url+api_key", "base_url,api_key"),
    **{
        schema.provider_id: ("api_key", "api_key")
        for schema in LLM_PROVIDER_SECRET_SCHEMAS
    },
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage local encrypted credentials.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser(
        "generate-master-key",
        help="Print a new TRADEFORGE_MASTER_KEY value.",
    )

    register = subparsers.add_parser(
        "register",
        help="Register or replace a provider credential in .keys.enc.",
    )
    register.add_argument("provider_id", choices=sorted(PROVIDER_FIELDS))
    register.add_argument("--api-key", required=True)
    register.add_argument("--secret-key")
    register.add_argument("--base-url")
    register.add_argument("--store-path", default=".keys.enc")
    register.add_argument("--set-by", default="operator")
    register.add_argument("--source", default="manual")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "generate-master-key":
        print(KeyManager.generate_master_key())
        return

    if args.command == "register":
        register_credential(
            provider_id=args.provider_id,
            api_key=args.api_key,
            secret_key=args.secret_key,
            base_url=args.base_url,
            store_path=Path(args.store_path),
            set_by=args.set_by,
            source=args.source,
        )
        return

    parser.error("unknown command")


def register_credential(
    *,
    provider_id: str,
    api_key: str,
    secret_key: str | None,
    base_url: str | None,
    store_path: Path,
    set_by: str,
    source: str,
) -> None:
    credential_type, field_spec = PROVIDER_FIELDS[provider_id]
    key_manager = KeyManager.from_environment()

    if provider_id == "litellm":
        if not base_url:
            raise ValueError("base_url is required for litellm credentials")
        credential = create_litellm_credential(
            LiteLLMCredentialPayload(
                base_url=base_url,
                api_key=api_key,
            ),
            key_manager=key_manager,
            set_by=set_by,
            source=source,
        )
        CredentialStore(store_path).save(credential)
        return

    payload = {"api_key": api_key}
    if "secret_key" in field_spec:
        if not secret_key:
            raise ValueError("secret_key is required for alpaca credentials")
        payload["secret_key"] = secret_key

    encrypted_payload = key_manager.encrypt_payload(payload)
    credential = Credential(
        provider_id=provider_id,
        credential_type=credential_type,
        encrypted_payload=encrypted_payload,
        created_at=datetime.now(UTC),
        rotated_at=None,
        last_validated_at=None,
        status=CredentialStatus.ACTIVE,
        provenance={"set_by": set_by, "source": source},
    )
    CredentialStore(store_path).save(credential)


if __name__ == "__main__":
    main()
