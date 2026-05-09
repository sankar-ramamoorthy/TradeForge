# TradeForge Milestone Roadmap

## Purpose

This document is the runtime implementation milestone plan for TradeForge.

It defines implementation order, issue groupings, branch naming, acceptance criteria, and ADR alignment.

The local issue source of truth is:

```text
DOCS/ISSUE_REGISTER.md
```

GitHub issues may mirror these records, but this repository roadmap and issue register remain the planning authority for runtime implementation.

---

## Status Values

- `Planned`: not started
- `In Progress`: actively being implemented
- `Blocked`: cannot proceed without a resolved dependency or decision
- `Done`: accepted as complete
- `Rejected`: intentionally not implemented

---

## Branch Naming

All implementation branches should include the local issue ID:

```text
feature/tf-0001-short-description
fix/tf-0001-short-description
docs/tf-0001-short-description
```

Branch scope must match exactly one issue unless the issue register explicitly groups the work.

---

## M0: Runtime Planning And Documentation Foundation

**Status:** Done

**Objective:** Establish local implementation planning discipline before runtime code begins.

**Implementation Focus:**

- ADR bootstrap
- milestone roadmap
- issue register
- issue discipline and branch naming

**Affected Layers:** docs

**Linked ADRs:**

- ADR 0001: Event Sourcing Core Model
- ADR 0002: Decision Lifecycle Engine
- ADR 0003: Canonical Event Taxonomy
- ADR 0004: Workspace Projection Model
- ADR 0005: Scenario Engine Architecture
- ADR 0006: AI Advisory Boundary Model
- ADR 0007: Anti-Dashboard UX Decision
- ADR 0008: Replay System Design
- ADR 0009: Persona Interpretation Model
- ADR 0010: Market Intelligence Interpretation Layer
- ADR 0011: Runtime Development Environment

**Issues:**

- TF-0001: Establish milestone roadmap and issue register

**Acceptance Criteria:**

- `DOCS/MILESTONE_ROADMAP.md` exists and defines implementation milestones.
- `DOCS/ISSUE_REGISTER.md` exists and defines concrete coding issues.
- Every issue has status, branch name, linked ADRs, affected layer, impacted invariants, and acceptance criteria.
- Future code changes can be tied to a local issue before implementation.

---

## M1: Runtime Scaffold And Developer Environment

**Status:** Done

**Objective:** Create a reproducible Python runtime foundation before domain implementation.

**Implementation Focus:**

- `pyproject.toml`
- `uv` project workflow
- Dockerfile using `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`
- `docker-compose.yml`
- pytest baseline
- lint, type, and dev command conventions
- README developer setup

**Affected Layers:** infrastructure, app, docs

**Linked ADRs:**

- ADR 0011: Runtime Development Environment

**Issues:**

- TF-0002: Create Python project scaffold with pyproject.toml and uv (**Done**)
- TF-0003: Add Dockerfile using uv Python 3.12 slim base image (**Done**)
- TF-0004: Add docker-compose.yml for local development (**Done**)
- TF-0005: Add pytest baseline and test command (**Done**)
- TF-0006: Add lint, type, and dev command conventions (**Done**)
- TF-0007: Add README developer setup section (**Done**)

**Acceptance Criteria:**

- Runtime has a repeatable Python project scaffold.
- Local tests can run through `uv`.
- Docker image uses the accepted uv Python 3.12 slim base image.
- Docker Compose provides a local development entrypoint.
- Developer commands are documented and do not define domain semantics.

---

## M2: Event Ledger And Canonical Event Model

**Status:** Done

**Objective:** Build the event-sourced foundation that all durable runtime state derives from.

**Implementation Focus:**

- event envelope
- event domain taxonomy
- append-only event store interface
- in-memory event store adapter for tests and vertical slices
- event integrity validation

**Affected Layers:** domain, infrastructure

**Linked ADRs:**

- ADR 0001: Event Sourcing Core Model
- ADR 0003: Canonical Event Taxonomy
- ADR 0008: Replay System Design

**Issues:**

- TF-0008: Define event envelope and canonical event domains (**Done**)
- TF-0009: Define append-only event store interface (**Done**)
- TF-0010: Implement in-memory event store adapter (**Done**)

**Acceptance Criteria:**

- Events are immutable fact records with type, timestamp, context, references, payload, and provenance.
- Event domains match the canonical taxonomy.
- Event store writes are append-only.
- Stored events can be read in deterministic order.
- No projection or service state is treated as canonical truth.

---

## M3: Decision Lifecycle Engine

**Status:** In Progress

**Objective:** Implement deterministic lifecycle authority for decision progression.

**Implementation Focus:**

- lifecycle state model
- allowed transition map
- transition validator
- lifecycle orchestration service
- event-backed transition emission

**Affected Layers:** domain, services

**Linked ADRs:**

- ADR 0001: Event Sourcing Core Model
- ADR 0002: Decision Lifecycle Engine
- ADR 0003: Canonical Event Taxonomy

**Issues:**

- TF-0011: Define lifecycle state model (**Done**)
- TF-0012: Implement lifecycle transition validator
- TF-0013: Implement lifecycle orchestration service

**Acceptance Criteria:**

- Lifecycle order is enforced as `Idea -> Thesis -> Plan -> Approval -> Execution -> Position -> Review`.
- Invalid shortcuts are rejected.
- Each accepted transition emits or prepares a valid lifecycle event.
- Lifecycle state is derived from events and deterministic rules.
- Services orchestrate transitions without owning persistence semantics.

---

## M4: Replay And Projection Foundation

**Status:** Planned

**Objective:** Provide deterministic reconstruction from event history.

**Implementation Focus:**

- replay projector interfaces
- projection rebuild flow
- deterministic ordering
- historical reconstruction of lifecycle and workspace state

**Affected Layers:** domain, services

**Linked ADRs:**

- ADR 0001: Event Sourcing Core Model
- ADR 0004: Workspace Projection Model
- ADR 0008: Replay System Design

**Issues:**

- TF-0014: Implement replay projector foundation
- TF-0015: Implement workspace projection read model

**Acceptance Criteria:**

- Replay consumes event history without live APIs or current UI state.
- Projection rebuilds are deterministic.
- Workspace read models are derived and discardable.
- Replay can reconstruct decision queue and workspace surface state for a basic workflow.

---

## M5: Persona Workspace Projection Model

**Status:** Planned

**Objective:** Implement persona-scoped workspace context without turning workspaces into dashboards or state owners.

**Implementation Focus:**

- persona context model
- workspace projection inputs
- briefing, opportunity, exposure, decision queue, and review surface projection boundaries

**Affected Layers:** domain, services

**Linked ADRs:**

- ADR 0004: Workspace Projection Model
- ADR 0007: Anti-Dashboard UX Decision
- ADR 0009: Persona Interpretation Model

**Issues:**

- TF-0015: Implement workspace projection read model
- TF-0016: Define persona context model

**Acceptance Criteria:**

- Workspaces are persona-scoped projections.
- Persona context influences interpretation and prioritization only.
- Workspace surfaces do not mutate canonical state.
- Workspace state can be rebuilt from events and deterministic rules.

---

## M6: Market Intelligence And Scenario Discovery

**Status:** Planned

**Objective:** Add advisory interpretation layers that produce context and scenarios without creating decisions.

**Implementation Focus:**

- market intelligence interpretation model
- scenario candidate model
- scenario ranking and invalidation boundaries
- clear separation between context, hypothesis, and decision

**Affected Layers:** domain, services

**Linked ADRs:**

- ADR 0005: Scenario Engine Architecture
- ADR 0009: Persona Interpretation Model
- ADR 0010: Market Intelligence Interpretation Layer

**Issues:**

- TF-0017: Define market intelligence interpretation model
- TF-0018: Define scenario discovery advisory model

**Acceptance Criteria:**

- Market Intelligence produces interpreted context, not decisions.
- Scenarios are hypotheses, not trade signals or execution instructions.
- Scenario outputs cannot bypass the Decision Lifecycle Engine.
- Persona context may influence ranking without creating state authority.

---

## M7: AI Advisory Boundary Integration

**Status:** Planned

**Objective:** Define the runtime boundary that keeps AI advisory and non-authoritative.

**Implementation Focus:**

- AI advisory request and response interfaces
- provenance and uncertainty fields where practical
- routing of AI suggestions into human-controlled lifecycle flow
- prevention of AI direct ledger writes or lifecycle transitions

**Affected Layers:** domain, services

**Linked ADRs:**

- ADR 0006: AI Advisory Boundary Model
- ADR 0008: Replay System Design
- ADR 0010: Market Intelligence Interpretation Layer

**Issues:**

- TF-0019: Define AI advisory boundary interfaces

**Acceptance Criteria:**

- AI outputs are advisory artifacts only.
- AI cannot write canonical events directly.
- AI cannot approve plans, execute trades, or mutate lifecycle state.
- AI outputs remain distinguishable from canonical, derived, and inferred state.

---

## M8: First Vertical Slice

**Status:** Planned

**Objective:** Demonstrate the first end-to-end runtime flow from idea creation through replayable review without live broker execution.

**Implementation Focus:**

- local app entrypoint
- event-backed lifecycle flow
- workspace projection update
- replay reconstruction
- review artifact creation

**Affected Layers:** domain, services, infrastructure, app

**Linked ADRs:**

- ADR 0001: Event Sourcing Core Model
- ADR 0002: Decision Lifecycle Engine
- ADR 0004: Workspace Projection Model
- ADR 0008: Replay System Design

**Issues:**

- TF-0020: Implement first vertical slice from Idea through Review replay

**Acceptance Criteria:**

- A user-controlled workflow can progress through the lifecycle without skipped stages.
- Each material state change is event-backed.
- Workspace state is derived from events.
- Replay reconstructs the workflow and review context.
- No broker integration, live trading, or autonomous AI execution is included.
