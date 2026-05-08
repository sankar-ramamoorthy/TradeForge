# ADR 0008: Replay System Design

## Status
Accepted

## Context
Replay is foundational to TradeForge. The system must be able to reconstruct decision context, workflow state, workspace surfaces, scenario history, market conditions, execution feedback, and review artifacts.

Replay supports auditability, behavioral review, rule evaluation, learning, and historical understanding. It must answer what was known, what was visible, what alternatives existed, what decisions were pending, and why actions occurred.

If replay depended on live APIs, current projections, mutable broker state, current AI output, or hidden state, historical reconstruction would become unreliable.

## Decision
TradeForge will implement replay as deterministic reconstruction from the Event Ledger, deterministic rules, and optional historical snapshots.

Replay may reconstruct:

- persona context
- workspace context and surfaces
- market observations and interpreted historical context
- scenario generation and ranking history
- decision lifecycle state
- execution feedback and position history
- decision queues
- reviews and annotations
- rule evaluation outcomes

Replay must not depend on:

- live market APIs
- current broker state
- current AI output
- UI state
- mutable projections
- hidden service state

Historical snapshots may be used as an optimization, but they do not replace the Event Ledger as canonical truth. Snapshot use must preserve deterministic reconstruction and must not obscure the underlying event history.

## Rationale
TradeForge is designed for disciplined decision-making and long-term operator improvement. That requires reliable reconstruction of the context in which decisions were made.

Event-backed deterministic replay allows review to distinguish between facts, derived projections, inferred interpretations, advisory outputs, operator actions, and execution feedback.

Replay also enforces architectural integrity. If a state cannot be reconstructed, the system has likely introduced hidden state or an unauthorized authority boundary.

## Alternatives Considered
Current-state replay was rejected because current projections cannot explain historical context or decision progression.

Live API replay was rejected because external systems are volatile and cannot represent what was known at the time.

Broker-state replay was rejected because broker systems do not contain internal TradeForge workflow context.

AI-regenerated replay was rejected because current AI output is not historical truth and may change over time.

Screenshot or UI-state replay was rejected because UI is a projection and not canonical state.

## Consequences
All material workflows must emit enough event-backed facts to support reconstruction.

Projection and workspace implementations must be rebuildable and must not hold hidden authoritative state.

Historical market context, scenario context, lifecycle transitions, execution feedback, and review artifacts must remain distinguishable during replay.

Rule evaluation used in replay must be deterministic and auditable.

Replay capability becomes a validation test for new architecture: designs that cannot be replayed must be rejected or rewritten.
