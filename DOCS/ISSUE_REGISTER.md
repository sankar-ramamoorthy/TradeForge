# TradeForge Issue Register

## Purpose

This document is the local issue register for runtime implementation.

Every code change must be tied to one issue before implementation begins.

Each issue records:

- issue ID
- milestone
- status
- branch name
- affected layer
- linked ADRs
- impacted invariants
- implementation summary
- acceptance criteria

GitHub issues may mirror these records, but this file remains the local planning source of truth.

---

## Status Values

- `Planned`: not started
- `In Progress`: actively being implemented
- `Blocked`: cannot proceed without a resolved dependency or decision
- `Done`: accepted as complete
- `Rejected`: intentionally not implemented

---

## Issue Index

| ID | Status | Milestone | Title | Branch |
| --- | --- | --- | --- | --- |
| TF-0001 | Done | M0 | Establish milestone roadmap and issue register | `docs/tf-0001-roadmap-issue-register` |
| TF-0002 | Planned | M1 | Define event envelope and canonical event domains | `feature/tf-0002-event-envelope-domains` |
| TF-0003 | Planned | M1 | Define append-only event store interface | `feature/tf-0003-event-store-interface` |
| TF-0004 | Planned | M1 | Implement in-memory event store adapter | `feature/tf-0004-in-memory-event-store` |
| TF-0005 | Planned | M2 | Define lifecycle state model | `feature/tf-0005-lifecycle-state-model` |
| TF-0006 | Planned | M2 | Implement lifecycle transition validator | `feature/tf-0006-lifecycle-transition-validator` |
| TF-0007 | Planned | M2 | Implement lifecycle orchestration service | `feature/tf-0007-lifecycle-orchestration-service` |
| TF-0008 | Planned | M3 | Implement replay projector foundation | `feature/tf-0008-replay-projector-foundation` |
| TF-0009 | Planned | M3/M4 | Implement workspace projection read model | `feature/tf-0009-workspace-projection-read-model` |
| TF-0010 | Planned | M4 | Define persona context model | `feature/tf-0010-persona-context-model` |
| TF-0011 | Planned | M5 | Define market intelligence interpretation model | `feature/tf-0011-market-intelligence-model` |
| TF-0012 | Planned | M5 | Define scenario discovery advisory model | `feature/tf-0012-scenario-discovery-model` |
| TF-0013 | Planned | M6 | Define AI advisory boundary interfaces | `feature/tf-0013-ai-advisory-boundary` |
| TF-0014 | Planned | M7 | Implement first vertical slice from Idea through Review replay | `feature/tf-0014-first-vertical-slice` |

---

## TF-0001: Establish Milestone Roadmap And Issue Register

**Status:** Done

**Milestone:** M0

**Branch:** `docs/tf-0001-roadmap-issue-register`

**Affected Layer:** docs

**Linked ADRs:**

- ADR 0001
- ADR 0002
- ADR 0003
- ADR 0004
- ADR 0005
- ADR 0006
- ADR 0007
- ADR 0008
- ADR 0009
- ADR 0010

**Impacted Invariants:**

- Event Sourcing Invariant
- Decision Lifecycle Invariant
- Workspace Invariant
- Persona Invariant
- AI Authority Invariant
- Scenario Invariant
- Event Integrity Invariant
- Replay Invariant
- Layer Separation Invariant
- Architectural Drift Invariant

**Implementation Summary:**

Create `DOCS/MILESTONE_ROADMAP.md` and `DOCS/ISSUE_REGISTER.md` so future implementation work has a local planning source of truth.

**Acceptance Criteria:**

- Milestone roadmap exists under `DOCS/`.
- Issue register exists under `DOCS/`.
- Issue register defines issue IDs, statuses, branch names, affected layers, linked ADRs, impacted invariants, and acceptance criteria.
- Roadmap links milestones to issues and ADRs.

---

## TF-0002: Define Event Envelope And Canonical Event Domains

**Status:** Planned

**Milestone:** M1

**Branch:** `feature/tf-0002-event-envelope-domains`

**Affected Layer:** domain

**Linked ADRs:**

- ADR 0001
- ADR 0003
- ADR 0008

**Impacted Invariants:**

- Event Sourcing Invariant
- Event Integrity Invariant
- Replay Invariant
- Layer Separation Invariant

**Implementation Summary:**

Define the domain-level event envelope and canonical event domain identifiers for persona, workspace, market, scenario, decision, execution, review, and system events.

**Acceptance Criteria:**

- Event envelope represents immutable facts, not interpretations.
- Event type, timestamp, context, references, payload, and provenance are modeled.
- Canonical event domains align with ADR 0003.
- Domain model contains no persistence or infrastructure logic.

**Out Of Scope:**

- Event store persistence implementation.
- Runtime API entrypoints.

---

## TF-0003: Define Append-Only Event Store Interface

**Status:** Planned

**Milestone:** M1

**Branch:** `feature/tf-0003-event-store-interface`

**Affected Layer:** domain, infrastructure

**Linked ADRs:**

- ADR 0001
- ADR 0003
- ADR 0008

**Impacted Invariants:**

- Event Sourcing Invariant
- Event Integrity Invariant
- Replay Invariant
- Layer Separation Invariant

**Implementation Summary:**

Define the event store port that supports appending immutable events and reading event history in deterministic order.

**Acceptance Criteria:**

- Interface supports append-only writes.
- Interface supports deterministic reads for replay.
- Interface does not expose mutation or deletion of historical events.
- Domain semantics are not defined by infrastructure adapters.

**Out Of Scope:**

- Database-backed event store.
- Broker integration.

---

## TF-0004: Implement In-Memory Event Store Adapter

**Status:** Planned

**Milestone:** M1

**Branch:** `feature/tf-0004-in-memory-event-store`

**Affected Layer:** infrastructure

**Linked ADRs:**

- ADR 0001
- ADR 0003
- ADR 0008

**Impacted Invariants:**

- Event Sourcing Invariant
- Event Integrity Invariant
- Replay Invariant
- Layer Separation Invariant

**Implementation Summary:**

Implement an in-memory event store adapter for tests and early vertical slices.

**Acceptance Criteria:**

- Adapter appends events without mutating prior history.
- Adapter returns events in deterministic order.
- Adapter rejects or avoids historical mutation operations.
- Tests demonstrate append and replay read behavior.

**Out Of Scope:**

- Durable database persistence.
- Distributed event streaming.

---

## TF-0005: Define Lifecycle State Model

**Status:** Planned

**Milestone:** M2

**Branch:** `feature/tf-0005-lifecycle-state-model`

**Affected Layer:** domain

**Linked ADRs:**

- ADR 0002
- ADR 0003

**Impacted Invariants:**

- Decision Lifecycle Invariant
- Event Integrity Invariant
- Layer Separation Invariant

**Implementation Summary:**

Define the lifecycle stages and decision aggregate state derived from lifecycle events.

**Acceptance Criteria:**

- Lifecycle stages are exactly `Idea`, `Thesis`, `Plan`, `Approval`, `Execution`, `Position`, and `Review`.
- Domain model does not allow stage merging.
- Current lifecycle state can be derived from event history.
- Domain layer remains framework-agnostic.

**Out Of Scope:**

- Service orchestration.
- UI decision queue.

---

## TF-0006: Implement Lifecycle Transition Validator

**Status:** Planned

**Milestone:** M2

**Branch:** `feature/tf-0006-lifecycle-transition-validator`

**Affected Layer:** domain

**Linked ADRs:**

- ADR 0002
- ADR 0003

**Impacted Invariants:**

- Decision Lifecycle Invariant
- Event Integrity Invariant
- Replay Invariant
- Layer Separation Invariant

**Implementation Summary:**

Implement deterministic validation for allowed lifecycle transitions.

**Acceptance Criteria:**

- Valid lifecycle transitions are accepted in canonical order.
- Invalid shortcuts such as `Idea -> Position` are rejected.
- Validation is deterministic and replay-compatible.
- Tests cover valid and invalid transitions.

**Out Of Scope:**

- Event store persistence.
- Broker execution.

---

## TF-0007: Implement Lifecycle Orchestration Service

**Status:** Planned

**Milestone:** M2

**Branch:** `feature/tf-0007-lifecycle-orchestration-service`

**Affected Layer:** services

**Linked ADRs:**

- ADR 0001
- ADR 0002
- ADR 0003

**Impacted Invariants:**

- Event Sourcing Invariant
- Decision Lifecycle Invariant
- Event Integrity Invariant
- Layer Separation Invariant

**Implementation Summary:**

Implement a service that coordinates lifecycle transition requests, invokes domain validation, and appends valid lifecycle events through the event store port.

**Acceptance Criteria:**

- Service orchestrates but does not define domain rules.
- Valid transitions append lifecycle events.
- Invalid transitions do not append events.
- Service does not directly manage infrastructure persistence details.

**Out Of Scope:**

- UI workflows.
- Live trading execution.

---

## TF-0008: Implement Replay Projector Foundation

**Status:** Planned

**Milestone:** M3

**Branch:** `feature/tf-0008-replay-projector-foundation`

**Affected Layer:** domain, services

**Linked ADRs:**

- ADR 0001
- ADR 0003
- ADR 0008

**Impacted Invariants:**

- Event Sourcing Invariant
- Replay Invariant
- Event Integrity Invariant
- Layer Separation Invariant

**Implementation Summary:**

Define the replay projector abstraction and implement deterministic reconstruction from ordered event history.

**Acceptance Criteria:**

- Replay uses event history, not live APIs or UI state.
- Projector output is deterministic for the same event stream.
- Replay can reconstruct lifecycle state for a basic workflow.
- Projection state is derived and discardable.

**Out Of Scope:**

- Historical market data API integration.
- AI-generated replay summaries.

---

## TF-0009: Implement Workspace Projection Read Model

**Status:** Planned

**Milestone:** M3/M4

**Branch:** `feature/tf-0009-workspace-projection-read-model`

**Affected Layer:** domain, services

**Linked ADRs:**

- ADR 0004
- ADR 0007
- ADR 0008
- ADR 0009

**Impacted Invariants:**

- Event Sourcing Invariant
- Workspace Invariant
- Persona Invariant
- Replay Invariant
- Layer Separation Invariant

**Implementation Summary:**

Implement a derived workspace read model with briefing, opportunity, exposure, decision queue, and review surface boundaries.

**Acceptance Criteria:**

- Workspace state is derived from events and deterministic rules.
- Workspace surfaces do not mutate canonical state.
- Workspace context is persona-scoped.
- Projection can be rebuilt from event history.

**Out Of Scope:**

- Dashboard-style UI.
- Stored workspace state as canonical truth.

---

## TF-0010: Define Persona Context Model

**Status:** Planned

**Milestone:** M4

**Branch:** `feature/tf-0010-persona-context-model`

**Affected Layer:** domain

**Linked ADRs:**

- ADR 0004
- ADR 0009

**Impacted Invariants:**

- Persona Invariant
- Workspace Invariant
- Replay Invariant
- Layer Separation Invariant

**Implementation Summary:**

Define persona context as an interpretation model that can influence ranking, weighting, and workflow emphasis without mutating canonical state.

**Acceptance Criteria:**

- Persona is not modeled as a user account or UI preference.
- Persona context can be associated with workspace and workflow context.
- Persona influence is interpretive only.
- Persona changes are compatible with historical replay.

**Out Of Scope:**

- Authentication and authorization.
- User profile management.

---

## TF-0011: Define Market Intelligence Interpretation Model

**Status:** Planned

**Milestone:** M5

**Branch:** `feature/tf-0011-market-intelligence-model`

**Affected Layer:** domain, services

**Linked ADRs:**

- ADR 0003
- ADR 0009
- ADR 0010

**Impacted Invariants:**

- Event Sourcing Invariant
- Persona Invariant
- Event Integrity Invariant
- Layer Separation Invariant

**Implementation Summary:**

Define interpreted market context structures for regimes, volatility, breadth, macro context, thematic narratives, and playbook activation conditions.

**Acceptance Criteria:**

- Market Intelligence outputs are interpreted context, not decisions.
- Market observations remain distinct from interpretations.
- Persona context may influence interpretation weighting.
- Outputs do not mutate lifecycle state.

**Out Of Scope:**

- Live market data ingestion.
- Trading signal generation.

---

## TF-0012: Define Scenario Discovery Advisory Model

**Status:** Planned

**Milestone:** M5

**Branch:** `feature/tf-0012-scenario-discovery-model`

**Affected Layer:** domain, services

**Linked ADRs:**

- ADR 0005
- ADR 0009
- ADR 0010

**Impacted Invariants:**

- Scenario Invariant
- Decision Lifecycle Invariant
- AI Authority Invariant
- Layer Separation Invariant

**Implementation Summary:**

Define advisory scenario models for hypotheses, rankings, invalidation, and watchlist promotion without creating decisions or execution instructions.

**Acceptance Criteria:**

- Scenarios are hypotheses, not trades or positions.
- Scenario ranking is advisory and non-authoritative.
- Scenario promotion cannot bypass lifecycle stages.
- Scenario outputs can feed workspace opportunity surfaces.

**Out Of Scope:**

- Broker execution.
- Autonomous strategy execution.

---

## TF-0013: Define AI Advisory Boundary Interfaces

**Status:** Planned

**Milestone:** M6

**Branch:** `feature/tf-0013-ai-advisory-boundary`

**Affected Layer:** domain, services

**Linked ADRs:**

- ADR 0006
- ADR 0008
- ADR 0010

**Impacted Invariants:**

- AI Authority Invariant
- Event Sourcing Invariant
- Decision Lifecycle Invariant
- Replay Invariant
- Layer Separation Invariant

**Implementation Summary:**

Define interfaces for AI advisory outputs with provenance and uncertainty where practical, while preventing AI from owning canonical events or lifecycle transitions.

**Acceptance Criteria:**

- AI outputs are modeled as advisory artifacts.
- AI cannot directly append canonical decision or execution events.
- AI cannot approve plans, execute trades, or transition lifecycle state.
- AI outputs remain distinguishable from canonical state.

**Out Of Scope:**

- Provider-specific AI integration.
- Autonomous execution.

---

## TF-0014: Implement First Vertical Slice From Idea Through Review Replay

**Status:** Planned

**Milestone:** M7

**Branch:** `feature/tf-0014-first-vertical-slice`

**Affected Layer:** domain, services, infrastructure, app

**Linked ADRs:**

- ADR 0001
- ADR 0002
- ADR 0003
- ADR 0004
- ADR 0008

**Impacted Invariants:**

- Event Sourcing Invariant
- Decision Lifecycle Invariant
- Workspace Invariant
- Replay Invariant
- Event Integrity Invariant
- Layer Separation Invariant

**Implementation Summary:**

Implement the first local vertical slice that progresses a user-controlled workflow through Idea, Thesis, Plan, Approval, Execution, Position, and Review using event-backed transitions and deterministic replay.

**Acceptance Criteria:**

- Workflow progresses through every lifecycle stage in order.
- Each material transition is event-backed.
- Invalid lifecycle shortcuts are rejected.
- Workspace projection updates are derived from events.
- Replay reconstructs workflow and review context from event history.
- No live broker integration or autonomous AI execution is included.

**Out Of Scope:**

- Live trading execution.
- Production persistence.
- Advanced UI.
