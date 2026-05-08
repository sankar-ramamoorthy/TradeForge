# ADR 0004: Workspace Projection Model

## Status
Accepted

## Context
TradeForge uses Persona Workspaces as persistent cognitive and operational decision environments. Workspaces structure situational awareness, opportunity review, exposure awareness, decision queues, and reflection.

Workspaces must preserve context over time without becoming independent state holders. If workspaces were treated as dashboards, tabs, pages, or stored current-state containers, they would compete with the Event Ledger and break replayability.

ADR 0001 establishes the Event Ledger as canonical truth. ADR 0002 establishes the Decision Lifecycle Engine as lifecycle authority. ADR 0003 establishes the canonical event taxonomy. The workspace model must operate within those decisions.

## Decision
TradeForge workspaces will be derived projections over event history and deterministic interpretation rules.

A Persona Workspace is a persona-scoped operational environment, not a dashboard, tab, page, or generic UI container. It may expose briefing, opportunity, exposure, decision queue, and review surfaces, but those surfaces are projections and do not own canonical state.

Workspace state must be reconstructable from:

- Event Ledger history
- Decision Lifecycle Engine state derived from events
- Market Intelligence interpretation outputs
- Scenario Discovery outputs
- Execution feedback recorded as events
- deterministic projection rules

Workspaces may preserve cognitive continuity, active context, decision queues, opportunity prioritization, exposure awareness, and review surfaces, but this preservation must be event-derived or projection-derived. No hidden workspace state may become authoritative.

Workspace events may record facts about workspace creation, opening, closing, activation, archival, or context updates. These events establish operational context; they do not make the workspace a canonical state owner.

## Rationale
Workspaces are central to TradeForge because they keep decision context coherent across time. They provide the operating environment where personas interpret market context, scenarios become visible, lifecycle transitions are surfaced, exposure is understood, and reviews occur.

Making workspaces projections preserves this cognitive role while maintaining event sourcing. It allows workspace surfaces to be rebuilt, audited, replayed, and compared historically.

This model also prevents UI structure from redefining system semantics. The workspace is the cognitive environment; the UI is only a window into that environment.

## Alternatives Considered
Dashboard workspaces were rejected because dashboards are display constructs, not operational decision environments.

UI-tab workspaces were rejected because tabs and pages describe navigation, not persistent persona-scoped cognition.

Stored workspace state as canonical truth was rejected because it would create hidden mutable state outside the Event Ledger.

Globally shared workspace state was rejected because all operational workflows must remain persona-scoped and workspace context must not leak across personas.

Direct raw API consumption by workspaces was rejected because workspaces consume interpreted and event-backed context, not volatile external state as truth.

## Consequences
Workspace surfaces must be rebuildable from event history and deterministic projection logic.

Workspace-specific views may optimize read performance, but they remain derived state and may be discarded or rebuilt.

Workspace design must preserve persona context, decision continuity, exposure awareness, and reviewability without bypassing lifecycle authority.

UI implementations must treat workspaces as cognitive environments and avoid treating them as dashboards or navigation containers.

Replay must be able to reconstruct workspace context, including briefing state, opportunity state, exposure state, decision queue state, and review state.
