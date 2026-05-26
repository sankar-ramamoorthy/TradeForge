# ADR-0044: Behavioral Signal Derived Read Model

## Status
Accepted

## Context
M14 introduces behavioral intelligence and cognitive auditability. The first
slice, TF-C001, detects recurring sizing violations from existing lifecycle,
plan, execution, and review history.

Behavioral analysis is useful only if it preserves TradeForge authority
boundaries. Sizing concerns, discipline drift, and process quality are
interpretive unless they are explicitly recorded as review facts or derived by
deterministic rules from canonical event history. If behavioral outputs became
hidden state, lifecycle gates, or AI-authored truth, they would violate event
sourcing, replayability, and human decision sovereignty.

## Decision
TradeForge will model M14 behavioral signals as deterministic derived read
models rebuilt from immutable event history.

The first behavioral signal implementation detects sizing discipline concerns
from structured `decision.plan_created` or `decision.plan_revised` payloads and
structured `review.review_completed` payloads. The detector emits derived
signals with source event references, severity, recurrence count, and explicit
non-canonical authority metadata.

Behavioral signal reads do not append events, mutate lifecycle state, approve
plans, execute trades, or persist hidden canonical state. Future behavioral
overlays, timelines, and clustering must preserve the distinction between
canonical facts, derived deterministic signals, and advisory interpretation.

## Rationale
M14 needs an auditable foundation before higher-order clustering or AI-assisted
interpretation. A derived read model lets review surfaces expose recurring
process problems while keeping the event ledger as the only source of truth.

Source event references make each signal explainable and replay-safe. Operators
can inspect which plan and review artifacts produced a signal rather than
trusting an opaque behavioral score.

## Consequences
Behavioral signals can be recomputed from event history and tested without
database migrations or new canonical event types.

Read APIs may expose behavioral signals as operational review context, but UI
and downstream services must label them as derived and non-canonical.

If a future issue needs to record that a deterministic behavioral evaluation
occurred, it must go through a separate ADR and event-taxonomy review before
adding `review.*` event semantics.

## Related ADRs
- ADR-0001: Event Sourcing Core Model
- ADR-0002: Decision Lifecycle Engine
- ADR-0008: Replay System Design
- ADR-0033: Structured Cognitive Artifact Model
- ADR-0035: Replay Cognitive Reconstruction Strategy
