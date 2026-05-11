# ADR 0019: Projection Persistence Architecture

## Status

Accepted

## Context

TradeForge uses projections and read models to support workspace surfaces,
attention queues, summaries, replay reconstruction, and operational API
responses.

Projections are derived from Event Ledger history and deterministic rules. They
may be persisted for performance, but persisted projection rows create a
source-of-truth risk if treated as canonical state.

M7 introduces database migration infrastructure before projection persistence is
implemented.

## Decision

Persisted projections may exist only as rebuildable infrastructure artifacts.

Projection persistence must remain subordinate to the Event Ledger. Projection
rows must be discardable and rebuildable from immutable event history. Runtime
code must not use persisted projections as lifecycle authority, event authority,
execution authority, persona authority, or AI authority.

Migration infrastructure may create projection tables in later scoped issues,
but those migrations must preserve source-event traceability and rebuild
semantics.

## Consequences

- Projection schemas must be designed for rebuildability.
- Projection persistence does not replace event replay.
- Runtime APIs may read persisted projections for performance only.
- Rebuild pipelines remain authoritative for regenerating projection content.
- TF-0025 creates migration infrastructure but no projection tables.
- Projection table implementation requires a separate issue and tests proving
  rebuild compatibility.

## Invariants Preserved

- Replay: historical reconstruction remains event-backed.
- Derived State Distinction: projections remain non-authoritative.
- Layer Separation: projection storage remains infrastructure.
- Workspace: workspace state remains derived from events and deterministic
  projection rules.

## Rejected Alternatives

### Treat persisted projections as source of truth

Rejected because it violates Event Ledger canonical truth and replayability.

### Persist projections before event ledger persistence

Rejected because durable projection rows without durable canonical event history
would invert TradeForge authority.

### Let UI or API code mutate projection rows directly

Rejected because direct projection mutation would create hidden state outside
the Event Ledger and rebuild pipeline.
