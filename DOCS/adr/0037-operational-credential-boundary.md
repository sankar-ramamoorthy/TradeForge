---
title: ADR-0037 — Operational Credential Boundary and API Key Management
status: accepted
date: 2026-05-15
milestone: M10C
deciders: [TradeForge architecture]
---

# ADR-0037 — Operational Credential Boundary and API Key Management

## Context

TradeForge connects to multiple external data providers, each requiring credentials:

| Provider | Credential Shape | Status |
|---|---|---|
| yFinance | none (free) | Active |
| Polygon.io | `api_key` | Active |
| Alpaca | `api_key` + `secret_key` | Active |
| Alpha Vantage | `api_key` | Planned |
| FinancialModelingPrep | `api_key` | Planned |
| Finqual | `api_key` | Planned |
| LLM providers (M11+) | `api_key` | Planned |

Currently, provider adapters accept API keys as constructor parameters.
`create_app()` in `src/app/api/application.py` wires providers directly.
There is no encrypted storage, no key rotation mechanism, no revocation,
and no barrier preventing keys from appearing in logs, environment dumps,
or version control.

This is acceptable for demo and development work but is architecturally
incorrect as a permanent approach. The gap was identified as TF-F004 after
the first operational walkthrough.

Additionally, TradeForge's replay invariant creates a credential-specific
requirement not found in most systems: the system must be able to reconstruct
what provider capabilities were available at any historical point. A replay
session from a future date may fail because a key expired, a provider tier
changed, or an entitlement was revoked. That failure itself is operationally
meaningful context, not just an error.

## Decision

TradeForge will implement a **Local Credential Boundary** governing all
external provider secret management.

### Master Key

`TRADEFORGE_MASTER_KEY` is set in the OS environment only.

Rules:
- Never in `.env`
- Never in Git
- Never logged
- Generated once using Fernet (AES-128-CBC with HMAC-SHA256)
- Rotatable without changing provider credentials

### Credential Domain Model

A `Credential` entity lives in `src/security/`:

```python
@dataclass(frozen=True, slots=True)
class CredentialStatus(StrEnum):
    ACTIVE = "active"
    REVOKED = "revoked"
    EXPIRED = "expired"
    UNKNOWN = "unknown"

@dataclass(frozen=True, slots=True)
class Credential:
    provider_id: str           # "polygon", "alpaca", "alpha_vantage", "fmp", "finqual", "openai"
    credential_type: str       # "api_key", "api_key+secret", "bearer_token"
    encrypted_payload: bytes   # Fernet-encrypted JSON of credential values
    created_at: datetime
    rotated_at: datetime | None
    last_validated_at: datetime | None
    status: CredentialStatus
    provenance: Mapping[str, str]  # who set it, from where
```

The `encrypted_payload` when decrypted yields a JSON object keyed by field name:
- Single-key providers: `{"api_key": "..."}`
- Dual-key providers (Alpaca): `{"api_key": "...", "secret_key": "..."}`

### Storage

Encrypted credentials are stored in `.keys.enc` at the project root.

`.keys.enc` is gitignored. It is never committed, never logged.

### Module Boundary

Security layer lives at `src/security/` — a top-level module parallel to
`src/domain/` and `src/infrastructure/`.

```
src/security/
├── __init__.py
├── credential.py        — Credential domain model + CredentialStatus
├── key_manager.py       — KeyManager: Fernet encrypt/decrypt, master key loading
└── credential_store.py  — CredentialStore: read/write .keys.enc
```

Provider adapters do NOT know about encryption or credential storage.
They continue to accept plain string constructor parameters.

`create_app()` is the only location that calls `CredentialStore` and
passes decrypted values to provider adapters. This preserves the existing
adapter boundary.

### Architectural Boundary Rule

> No provider adapter shall know how credentials are stored or decrypted.
> The composition root (`create_app()`) is the sole caller of `CredentialStore`.

### Replay Safety

The `Credential` model's `status`, `rotated_at`, and `last_validated_at`
fields are designed to support future `CredentialValidationEvent` artifacts.

When a provider is unavailable during replay, the system will eventually
surface whether that unavailability was due to a key that was expired,
revoked, or not yet provisioned at the time of reconstruction.

This does not require event-sourced credential storage in M10B.
It requires that the domain model is designed to support it when needed.

## Rationale

Burying key management as a constructor detail is technically functional
but architecturally dishonest. External provider credentials are operational
capabilities — they have lifecycle (creation, rotation, revocation), they
affect replay fidelity, and they are subject to entitlement changes that
are operationally meaningful.

A dedicated `src/security/` layer signals this intentionally. It is not
infrastructure trivia — it is a bounded security domain that governs how
the system interacts with all external capability providers.

As the provider count grows (Polygon, Alpaca, Alpha Vantage, FMP, Finqual,
and eventually LLM providers in M11), the composition root would otherwise
become an unmanaged collection of raw environment variable lookups. The
credential boundary prevents that drift.

## Alternatives Considered

**Raw `os.environ` lookups in `create_app()`:** Rejected. Scales poorly as
provider count grows. No rotation, no revocation, no status tracking.

**`.env` file with python-dotenv:** Rejected. `.env` files are committed
accidentally, appear in logs, and are not a credential boundary — they are
configuration files.

**External secrets manager (Vault, AWS Secrets Manager):** Not appropriate
for a local-first operational system. TradeForge is designed for a single
operator running locally. Operational complexity of external secrets services
is not warranted at this stage.

**Encrypted database column:** Rejected for M10B. Adds database dependency
for a concern that is pre-database. `.keys.enc` with Fernet is appropriate
for local-first operation.

## Consequences

- `TRADEFORGE_MASTER_KEY` must be set before the application starts.
- A setup guide (`HOW-TO-SETUP-KEYS.md`) must explain key generation, credential
  registration, and rotation.
- `.keys.enc` must be added to `.gitignore`.
- `create_app()` gains a `credential_store` parameter for test injection.
- All future provider adapters (Alpha Vantage, FMP, Finqual, LLM providers)
  are registered through `CredentialStore` — not through raw env var lookups.
- Provider adapter tests continue to use constructor injection with mock values —
  no change to existing test patterns.
- M10B (Postgres persistence + multi-decision navigation) precedes this milestone.
