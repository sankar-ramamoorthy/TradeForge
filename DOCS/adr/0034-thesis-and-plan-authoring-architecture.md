---
title: ADR-0034 — Thesis And Plan Authoring Architecture
status: accepted
date: 2026-05-14
milestone: M10A
deciders: [TradeForge architecture]
---

# ADR-0034 — Thesis And Plan Authoring Architecture

## Context

The existing Idea→Thesis and Thesis→Plan lifecycle transitions accept an empty payload.
Clicking "Develop Thesis" immediately fires the transition with `payload: {}`.

This means:
- TradeThesis is a canonical lifecycle stage with no structured reasoning content
- TradePlan is a canonical lifecycle stage with no execution intent
- Replay cannot reconstruct what the operator was thinking at each stage
- Review workspaces cannot compare original thesis reasoning against outcomes

The canonical entity definitions for `TradeThesis` and `TradePlan` document their intended
semantic richness, but nothing enforces or captures that richness during authoring.

## Decision

Each lifecycle stage transition that introduces a cognitive artifact requires a structured authoring workflow.

### Thesis Authoring Workflow

A `POST /lifecycle/decisions/develop-thesis` endpoint replaces the bare
`POST /lifecycle/transitions` call for the Idea→Thesis transition.

The endpoint:
1. Accepts structured thesis fields (narrative, catalysts, assumptions, invalidation_conditions, confidence_level)
2. Validates that required fields are non-empty
3. Creates the lifecycle transition with the validated artifact embedded in the event payload
4. Returns the decision_id and resulting event metadata

The frontend presents a `ThesisDevelopmentModal` form before firing the transition.
The form collects all required fields and submits to the dedicated endpoint.

### Plan Authoring Workflow (M10AIS06–07, later)

A similar `POST /lifecycle/decisions/create-plan` endpoint will gate the Thesis→Plan transition,
requiring entry/stop/target/sizing rationale fields.

### Separation Of Concern Between Lifecycle Stages

| Stage | Content | Authority |
|---|---|---|
| TradeIdea | symbol + initial_thesis seed | lifecycle.decision.trade_idea_created |
| TradeThesis | structured narrative, catalysts, assumptions, invalidation_conditions | lifecycle.decision.thesis_created |
| TradePlan | entry/stop/target/sizing rationale, execution assumptions | lifecycle.decision.plan_created |

These are distinct semantic artifacts. `initial_thesis` in the Idea stage is a seed, not a thesis.
The Thesis stage is where structured reasoning is captured and persisted.

### Backend Endpoint Convention

Dedicated lifecycle authoring endpoints follow the pattern established by
`POST /lifecycle/decisions/init` (TF-0053):
- specific semantic meaning (not generic `/transitions`)
- required domain fields validated at the API boundary
- structured payload embedded into the event
- event creation delegated to the LifecycleOrchestrationService

### Frontend Authoring Convention

Lifecycle stage transitions that gate on structured input use modal forms:
- modals open on button click before firing any transition
- form submission calls the dedicated endpoint
- on success, navigation proceeds to the appropriate next workspace
- transition errors surface in the modal without leaving the workspace

## Consequences

- Lifecycle transitions from Idea→Thesis (and later Thesis→Plan) require structured operator input
- Immediate empty transitions are replaced by authoring-gated endpoints
- Events carry semantically complete payloads validated at the API boundary
- The Plan Review workspace can display thesis content before plan creation
- Replay timeline entries carry structured artifact content for display
- Existing empty thesis events (seeded demo scenarios) are not retroactively enriched

## Related ADRs

- ADR-0002: Decision Lifecycle Engine — lifecycle stage authority unchanged
- ADR-0033: Structured Cognitive Artifact Model — artifact data model
- ADR-0035: Replay Cognitive Reconstruction Strategy — how replay surfaces artifact content
