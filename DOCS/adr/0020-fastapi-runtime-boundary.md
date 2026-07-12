# ADR 0020: FastAPI Runtime Boundary

## Status

Accepted

## Context

M7 introduces the HTTP application runtime after the event ledger, lifecycle
engine, replay foundation, workspace projections, persona context, Postgres
persistence, and migration infrastructure are established.

TradeForge needs an API boundary for frontend and operational workflows, but the
HTTP layer must not become a competing owner of domain rules, lifecycle
authority, event semantics, replay behavior, or persistence semantics.

## Decision

TradeForge will use FastAPI as the HTTP application boundary.

FastAPI route handlers live in the app layer. They may parse requests, call
services, translate service results into HTTP responses, and register routers.
They must delegate domain behavior to domain and services layers.

The FastAPI runtime may expose operational metadata and health routes directly.
Workflow routes introduced in later issues must call the appropriate service
boundary rather than implementing lifecycle, replay, workspace, persistence, or
AI authority in HTTP handlers.

## Consequences

- The runtime has a local HTTP startup path.
- Endpoint-specific issues can register routers into a shared app factory.
- HTTP handlers remain orchestration adapters.
- Lifecycle API endpoints remain scoped to TF-0028.
- Replay API endpoints remain scoped to TF-0029.
- Workspace projection APIs remain scoped to TF-0030.
- Authentication/session behavior remains scoped to TF-0034.

## Invariants Preserved

- Layer Separation: HTTP code remains in the app layer.
- Decision Lifecycle: lifecycle transitions remain service/domain controlled.
- Event Sourcing: HTTP routes do not mutate canonical truth directly.
- Replay: replay endpoints must consume replay services, not live APIs or UI
  state.

## Rejected Alternatives

### Put lifecycle logic in route handlers

Rejected because the Decision Lifecycle Engine owns workflow authority.

### Let routes access Postgres directly

Rejected because persistence remains behind ports/adapters and service
boundaries.

### Build endpoint-specific apps per feature

Rejected because a shared app factory preserves a single runtime boundary and
consistent middleware/router registration.

## History

- 2026-07-12 (M-RF, TF-RF001–TF-RF010): the `routes.py` monolith was
  decomposed into per-domain router modules under `src/app/api/routes/`,
  with shared service accessors in `src/app/api/deps.py`, cross-domain
  schemas in `src/app/api/shared_schemas.py`, and markdown import parsing
  relocated to `src/services/advisory/local_import_parsing.py`. Structural
  only — the runtime boundary, route contract, and this decision are
  unchanged (OpenAPI snapshot byte-identical across the milestone).
