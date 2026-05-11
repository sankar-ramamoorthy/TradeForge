# ADR 0018: Postgres Event Store Persistence

## Status

Accepted

## Context

TradeForge requires durable runtime persistence for MVP operation. The Event
Ledger remains the canonical source of truth, and all material state must remain
reconstructable from immutable events and deterministic rules.

M1-M6 established the event envelope, Event Store port, in-memory adapter,
lifecycle engine, replay foundation, workspace projections, and persona-aware
derived summaries. M7 introduces durable infrastructure without changing those
semantic boundaries.

## Decision

TradeForge will use Postgres as the durable persistence platform for the runtime
event ledger and later projection storage.

Postgres is an infrastructure concern. It does not define event semantics,
lifecycle authority, workspace meaning, persona interpretation, replay behavior,
or AI authority boundaries.

The Event Store port remains the boundary between domain/services code and
persistence adapters. Runtime code that needs event history must depend on the
port, not on Postgres-specific APIs.

## Consequences

- Local development includes a Postgres service.
- Database connection settings live in the infrastructure layer.
- Domain models remain framework-agnostic and persistence-free.
- Services continue to orchestrate through ports rather than database clients.
- Durable event ledger implementation is deferred to TF-0026.
- Migration infrastructure is deferred to TF-0025.
- Projection persistence is not introduced by this ADR.

## Invariants Preserved

- Event Sourcing: canonical state remains immutable event history.
- Replay: replay depends on event history and deterministic rules.
- Layer Separation: database concerns remain in infrastructure.
- Event Integrity: Postgres persistence must be append-only at the adapter
  boundary when the ledger adapter is implemented.

## Rejected Alternatives

### SQLite as MVP persistence

Rejected because the M7 roadmap requires operational runtime infrastructure that
can grow into API and frontend workflows without changing persistence strategy.

### Direct database access from services

Rejected because it would bypass the Event Store port and risk coupling
orchestration to infrastructure details.

### Projection-first persistence

Rejected because projections are derived and discardable. Canonical durable
persistence must prioritize event history before projection storage.
