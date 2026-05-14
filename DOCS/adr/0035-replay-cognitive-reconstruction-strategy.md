---
title: ADR-0035 — Replay Cognitive Reconstruction Strategy
status: accepted
date: 2026-05-14
milestone: M10A
deciders: [TradeForge architecture]
---

# ADR-0035 — Replay Cognitive Reconstruction Strategy

## Context

Replay currently reconstructs workflow state from lifecycle events.
The replay timeline shows event types, timestamps, personas, and generic payloads.

It does not reconstruct operator reasoning at historical timestamps:
- no thesis narrative visible at the Thesis stage
- no plan rationale visible at the Plan stage
- no scenario branches visible
- no review reflections visible

As M10A introduces structured cognitive artifacts into event payloads, replay must evolve
to surface this content alongside the workflow event timeline.

## Decision

Replay reconstruction is extended to display cognitive artifact content from event payloads.

### Principle: No New Canonical State

Cognitive artifact content in replay derives entirely from event payload data.
No separate cognitive artifact store is created for replay.
Reconstruction remains deterministic and replayable from immutable events.

### Replay Timeline Extension

The replay timeline (`GET /replay/timeline`) already returns full `payload` fields for each event.
Consuming surfaces (Replay workspace frontend) are extended to extract and display structured
artifact content from these payloads where available.

For `decision.thesis_created` events, the payload contains the structured thesis fields:
- `narrative`, `catalysts`, `assumptions`, `invalidation_conditions`, `confidence_level`

The Replay workspace renders these fields inline when present, falling back gracefully
when events carry empty or legacy payloads.

### Point-In-Time Cognitive Snapshot (M10AIS10, later)

Future reconstruction support for `CognitiveSnapshot` at a timestamp T:
- scan all lifecycle events before T
- extract the most recent thesis artifact payload
- extract the most recent plan artifact payload
- reconstruct active scenario branches
- present as a "cognition snapshot" at that moment in time

This is deferred to M10AIS10.

### Graceful Degradation

Events created before M10A carry empty or seed-only payloads.
The replay system must display these without error.
Fields are treated as optional; absence of structured content displays a neutral placeholder.

## Consequences

- Replay workspace can display thesis narrative and catalysts alongside lifecycle events
- No new API endpoints are required for Phase M10AIS01-02 replay support
- The ReplayTimeline entries already carry payload data; frontend rendering adapts
- Seeded demo scenarios created before M10A will display "no structured thesis" gracefully
- Future M10AIS09-10 (Replay Cognitive Artifact Timeline) will formalize a dedicated
  cognitive projection layer on top of the event timeline

## Related ADRs

- ADR-0001: Event Sourcing Core Model — immutable event payloads remain canonical truth
- ADR-0008: Replay System Design — replay remains deterministic and non-mutating
- ADR-0033: Structured Cognitive Artifact Model — artifact data model
- ADR-0034: Thesis And Plan Authoring Architecture — authoring workflow creates the content
