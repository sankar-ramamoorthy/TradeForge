# ADR 0002: Decision Lifecycle Engine

## Status
Accepted

## Context
TradeForge is workflow-centric, not CRUD-centric or dashboard-centric. Its core operational purpose is to guide trading and investing activity through a disciplined decision lifecycle under persona and workspace context.

The canonical lifecycle is:

```text
Idea -> Thesis -> Plan -> Approval -> Execution -> Position -> Review
```

Scenarios, market intelligence, personas, workspaces, AI summaries, and UI surfaces may influence how information is interpreted or prioritized, but they do not own workflow state. Without a single lifecycle authority, the system could skip stages, convert scenarios directly into trades, treat UI actions as state mutation, or allow execution integrations to bypass reviewable decision structure.

## Decision
TradeForge will implement the Decision Lifecycle Engine as the authoritative workflow state machine for decision progression.

All decisions must move through the lifecycle in order:

```text
Idea -> Thesis -> Plan -> Approval -> Execution -> Position -> Review
```

No stage may be skipped, merged, or silently inferred. Direct `Idea -> Position`, `Scenario -> Execution`, or `Plan -> Position` transitions are invalid.

Every lifecycle transition must be explicit, deterministic, validated by the lifecycle engine, and backed by an event in the Event Ledger. Lifecycle state is derived from those events and may not be stored as hidden mutable state.

Only the Decision Lifecycle Engine may advance lifecycle state. Other subsystems may provide inputs, context, or feedback, but they cannot own or bypass lifecycle transitions:

- Personas influence interpretation, ranking, prioritization, and workflow emphasis.
- Workspaces expose derived decision environments and queues.
- Market Intelligence provides interpreted context, not decisions.
- Scenario Discovery surfaces hypotheses, opportunities, and risks, not trades.
- AI summarizes, ranks, clusters, and suggests, but remains advisory.
- Execution integrations communicate with external systems and record external facts, but do not authorize workflow progression.

Every completed lifecycle must support review through event-backed review artifacts and deterministic replay.

## Rationale
The lifecycle engine preserves disciplined decision-making by ensuring that trade activity is not treated as an isolated action. Ideas must be structured into theses, theses must become plans, plans must be approved, execution must be recorded, positions must be tracked through events, and outcomes must be reviewed.

Centralizing lifecycle authority prevents semantic drift across UI, services, scenario discovery, and execution integration. It also keeps human decision sovereignty intact: the system may surface information and enforce workflow rules, but it does not autonomously approve or execute decisions.

Event-backed transitions make lifecycle state auditable and replayable. They also allow persona-scoped workspaces and review surfaces to reconstruct what was known, what was pending, what was approved, and what happened afterward.

## Alternatives Considered
Direct idea-to-position workflows were rejected because they bypass thesis formation, planning, approval, execution traceability, and review.

Scenario-to-trade shortcuts were rejected because scenarios are hypotheses, not decisions, trade signals, or execution instructions.

UI-driven lifecycle mutation was rejected because UI surfaces are projections over workspace state and must not own canonical workflow state.

AI-autonomous approval or execution was rejected because AI is advisory only and must not bypass deterministic lifecycle controls or human decision sovereignty.

Execution-layer workflow ownership was rejected because broker integrations and external APIs represent external interaction, not internal decision authority.

Combining lifecycle stages was rejected because merged stages obscure operator intent, reduce auditability, and weaken replay and review.

## Consequences
All decision workflow features must integrate through lifecycle transition validation rather than mutating state directly.

The Event Ledger must contain the facts needed to reconstruct lifecycle state, including idea creation, thesis creation, plan creation, approval or rejection, execution events, position events, and review events.

Workspace decision queues and review surfaces remain derived projections of event-backed lifecycle state.

Scenario and AI systems must route candidate actions through the lifecycle engine instead of creating execution authority.

This design increases workflow explicitness and may require more transition events, but it is required to preserve TradeForge invariants, replayability, and disciplined execution.
