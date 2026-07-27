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

---

## Amendment — UI Credential Management (TF-F055)

**Date:** 2026-05-22  
**Milestone:** M13 (feedback issue)

### Additional Decisions

Two decisions are added as addenda to the original ADR. The encryption model,
master key model, no-secrets-in-code rule, and composition root principle are
unchanged.

**1. Runtime credential write access via restricted admin API**

`CredentialStore` is now accessible at runtime via a restricted `/admin/credentials`
API surface (mounted separately from the main `runtime_router`). The endpoint
enforces that:
- `TRADEFORGE_MASTER_KEY` must be set in the OS environment before any credential
  write succeeds (503 otherwise)
- GET responses return masked field values only — secrets are never returned
  (last 4 characters of secret fields, non-secret fields like `base_url` in full)
- PUT encrypts the payload via `KeyManager` before writing to `CredentialStore`
- DELETE sets `status=REVOKED` and preserves the record for audit trail
- `create_app()` remains the sole startup path; the admin surface is a runtime
  extension only

**2. In-process provider reload after credential change**

`ProviderBootstrapService` is attached to `app.state.provider_bootstrap`.
After every successful PUT or DELETE, it calls `reload()` which rebuilds
`MarketSnapshotService`, `FundamentalsService`, and `ProviderRegistry`
from the updated `CredentialStore`. The operator does not need to restart
the application to activate a new credential.

`ProviderBootstrapService.reload()` handles `MasterKeyNotConfiguredError`
gracefully (returns without rebuilding) — startup failures are not
replicated as runtime failures.

### What Does NOT Change

- `TRADEFORGE_MASTER_KEY` cannot be set or changed via the UI. It remains
  an OS environment variable set before the process starts.
- Provider adapters continue to accept plain string parameters — they remain
  unaware of encryption or credential storage.
- `create_app()` is still the sole startup bootstrap path.
- The `CredentialStore` path (`.keys.enc`) remains fixed at the project root.

---

## Amendment - Compose First-Run Master Key Setup (EZ-02)

**Date:** 2026-07-27
**Milestone:** M-EZ

### Additional Decision

TradeForge may generate `TRADEFORGE_MASTER_KEY` through the restricted admin UI
only during first-run setup, defined as the state where no process master key
and no `.keys.enc` credential store exist.

The generated key is:

- returned to the browser once
- written to the ignored local `.tradeforge/runtime.env` file mounted by Docker
  Compose
- loaded by the runtime process on startup when the OS environment does not
  already provide `TRADEFORGE_MASTER_KEY`
- applied to the current process immediately so provider credentials can be
  entered without a container restart

This is a local single-operator trust tradeoff for the Compose ease-of-use
path. The runtime env file is plaintext local configuration, not canonical
state, not committed, and not logged.

### What Does NOT Change

- Existing `.keys.enc` files cannot be re-keyed or unlocked by first-run setup.
- Provider credentials remain encrypted in `.keys.enc`.
- GET credential responses continue to return masked values only.
- Provider adapters still receive plain constructor parameters only from the
  composition root and do not know about credential storage.
- yfinance remains the default provider and requires no credentials.
