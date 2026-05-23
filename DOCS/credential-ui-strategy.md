---
title: Credential UI Strategy — TF-F055
type: planning-document
status: implemented
created: 2026-05-22
updated: 2026-05-22
tags:
  - credentials
  - security
  - admin
  - ux
  - m13
related_adrs:
  - ADR-0037 (Operational Credential Boundary — amended)
---

# Credential UI Strategy — TF-F055

## Problem

Entering and rotating provider API keys requires a terminal command:

```powershell
uv run python scripts\manage_credentials.py register polygon --api-key "..."
```

This is cumbersome for routine operation. The operator should be able to enter,
view, and rotate keys from the `ProviderConfigurationPanel` in the browser.

---

## What Does NOT Change

- `TRADEFORGE_MASTER_KEY` stays in the OS environment. It cannot be set or
  changed via the UI. This is load-bearing security — the UI never sees the
  master key.
- The encryption model (Fernet AES) is unchanged.
- The `CredentialStore` (`.keys.enc`) remains the sole persistent write path.
- Provider adapters continue to receive plain strings — they are unaware of
  the credential layer.
- The CLI (`scripts/manage_credentials.py`) continues to work. UI and CLI are
  both valid paths to the same store.

---

## Architecture

### Backend

**`ProviderBootstrapService`** (`src/app/api/application.py`)

A new class attached to `app.state.provider_bootstrap`. Its `reload()` method
rebuilds `MarketSnapshotService`, `FundamentalsService`, and `ProviderRegistry`
from the current `CredentialStore` contents. Called automatically after every
credential save or revoke — no restart required.

**`/admin/credentials` router** (`src/app/api/admin_routes.py`)

Mounted separately from the main `runtime_router`. Three endpoints:

| Method | Path | Description |
|---|---|---|
| GET | `/admin/credentials` | List all known providers with configured status and masked fields. Secrets never returned — last 4 chars only. |
| PUT | `/admin/credentials/{provider_id}` | Save/update credential. Encrypts, writes, reloads. Returns masked status. 503 if master key not set. |
| DELETE | `/admin/credentials/{provider_id}` | Revoke credential (status=REVOKED, record preserved). Reloads. 404 if not configured. |

**Known providers (static registry):**
- `yfinance` — no credentials required, always active
- `polygon` — `api_key`
- `alpaca` — `api_key`, `secret_key`
- `fmp` — `api_key`
- `alpha_vantage` — `api_key`
- `litellm` — `base_url` (non-secret), `api_key`, `default_model` (non-secret)

**Masking rule:** Secret fields (api_key, secret_key) show `••••XXXX` where
XXXX is the last 4 characters of the plaintext. Non-secret fields (base_url,
default_model) show the full plaintext value for usability.

### Frontend

**`PROVIDER_CREDENTIAL_SCHEMAS`** (`frontend/src/api/runtime.ts`)

Static constant mapping each provider to its field definitions. The frontend
knows which fields are secret (rendered as `type="password"`) and which are not.
No API round-trip needed for schema — it never changes at runtime.

**New API functions** (`frontend/src/api/runtime.ts`)
- `fetchCredentials()` → `GET /admin/credentials`
- `updateCredential(provider_id, fields)` → `PUT /admin/credentials/{provider_id}`
- `revokeCredential(provider_id)` → `DELETE /admin/credentials/{provider_id}`

**`ProviderConfigurationPanel`** (`frontend/src/workspaces/ProviderConfigurationPanel.tsx`)

A new "Credentials" section is added below the existing provider preference UI.
Each provider row shows:
- A configured/not-configured status badge
- Masked field values when configured (e.g., `api_key: ••••1234`)
- An "Update" button that toggles an inline form
- A "Revoke" button (only shown when configured)
- An inline form with `type="password"` inputs for secret fields
- A success toast ("Credential saved. Providers reloaded.") on submit
- A warning if `TRADEFORGE_MASTER_KEY` is not set

No modal, no new page. The credential section expands inline within the existing
panel, which is already a side-panel control surface.

---

## Security Properties

| Property | Guaranteed |
|---|---|
| Secrets never in response body | ✓ — masked_value is last 4 chars only |
| Secrets never in application code | ✓ — KeyManager is the only decryptor |
| Secrets never in git history | ✓ — .keys.enc is gitignored |
| Master key not configurable via UI | ✓ — 503 if not in OS environment |
| Audit trail preserved on revoke | ✓ — record kept with status=revoked |
| Restart not required on credential change | ✓ — ProviderBootstrapService.reload() |

---

## Provider Reload Model

After every `PUT` or `DELETE`:

1. `CredentialStore.save()` writes to `.keys.enc`
2. `ProviderBootstrapService.reload()` is called
3. `reload()` re-reads credentials from `.keys.enc`
4. Rebuilds `MarketSnapshotService` (new market provider if needed)
5. Rebuilds `FundamentalsService` (new fundamentals providers)
6. Updates `app.state.provider_registry`
7. In-memory snapshot/provenance caches are discarded — these are advisory
   derived caches, not canonical state

The operator sees the change take effect immediately. The event store,
lifecycle engine, and all canonical advisory artifacts are unaffected.

---

## What This Enables

Once credentials are entered via the UI:

1. The operator can configure Polygon or Alpaca for price data
2. The operator can configure FMP or Alpha Vantage for fundamentals
3. The operator can configure LiteLLM for advisory AI tasks (TF-F046+)
4. All without touching a terminal after initial TRADEFORGE_MASTER_KEY setup
