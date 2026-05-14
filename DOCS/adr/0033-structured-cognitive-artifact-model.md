---
title: ADR-0033 — Structured Cognitive Artifact Model
status: accepted
date: 2026-05-14
milestone: M10A
deciders: [TradeForge architecture]
---

# ADR-0033 — Structured Cognitive Artifact Model

## Context

TradeForge lifecycle stages currently record workflow transitions through immutable events.
Events carry a generic `payload: dict` field but no enforced structure.

Operators cannot persist structured reasoning at each stage:
- thesis narrative, catalysts, assumptions, and invalidation conditions
- plan entry/stop/target/sizing rationale
- scenario branch conditions
- review reflections and lessons learned

Without structured cognitive artifacts:
- replay reconstructs only stage transitions, not operator reasoning
- review workspaces cannot compare original thesis against outcome
- AI advisory systems have no structured cognition context to augment

M10A introduces durable cognitive artifacts that make operator reasoning a first-class replayable product of the TradeForge system.

## Decision

Cognitive artifacts are persisted as structured event payload data inside lifecycle events.
The event ledger remains the sole canonical source of truth.
No separate artifact storage table or side-channel is introduced.

A dedicated API endpoint validates required artifact fields before creating the lifecycle event,
ensuring that event payloads carry semantically complete cognitive content.

A projection layer extracts and reconstructs structured artifact state from event history,
providing workspace-readable artifact views without duplicating canonical state.

## Artifact Types (Phase M10AIS01 scope)

### ThesisArtifact
Attached to `decision.thesis_created` event payload:
- `narrative` (str, required): the core thesis statement
- `catalysts` (list[str], required): identified thesis drivers
- `assumptions` (list[str], required): underlying assumptions
- `invalidation_conditions` (list[str], required): conditions that invalidate the thesis
- `confidence_level` (int 1–5, required): operator conviction
- `regime_alignment` (str, optional): market regime context

### Planned Future Artifacts (later M10A issues)
- `TradePlanArtifact` — entry/stop/target/sizing rationale (M10AIS06)
- `ScenarioBranchArtifact` — conditional reasoning pathways (M10AIS04)
- `ReviewReflectionArtifact` — post-decision learning (M10AIS11)

## Consequences

- Events carry richer semantic payloads validated at the API boundary
- Projections extract structured artifact state from event history — no new tables needed for MVP
- Replay timeline entries carry artifact payload content for display
- Future AI advisory systems gain structured cognition as historical context
- Behavioral intelligence systems gain replayable reasoning as input
- The authoring step before a lifecycle transition replaces the previous immediate empty transition
- Retroactive migration of existing empty thesis events is out of scope — only new transitions carry structured content

## Authority

- Structured artifacts are canonical only when stored in immutable lifecycle events
- Workspace projection artifacts are derived, non-authoritative read models
- API endpoint validates artifacts before creating events; it does not bypass lifecycle authority

## Related ADRs

- ADR-0002: Decision Lifecycle Engine — lifecycle authority remains unchanged
- ADR-0001: Event Sourcing Core Model — immutable event ledger remains canonical truth
- ADR-0034: Thesis And Plan Authoring Architecture — authoring workflow design
- ADR-0035: Replay Cognitive Reconstruction Strategy — how replay surfaces artifact content
