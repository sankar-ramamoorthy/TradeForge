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

Roadmap v2 is the active milestone direction. This register is intentionally scoped through M8 for the fast MVP v1 path. 
Explicit roadmap checkpoint completed M9 Updated*Done*.


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
| TF-0002 | Done | M1 | Create Python project scaffold with pyproject.toml and uv | `feature/tf-0002-python-project-scaffold` |
| TF-0003 | Done | M1 | Add Dockerfile using uv Python 3.12 slim base image | `feature/tf-0003-dockerfile-uv-python312` |
| TF-0004 | Done | M1 | Add docker-compose.yml for local development | `feature/tf-0004-docker-compose-local-dev` |
| TF-0005 | Done | M1 | Add pytest baseline and test command | `feature/tf-0005-pytest-baseline` |
| TF-0006 | Done | M1 | Add lint, type, and dev command conventions | `feature/tf-0006-dev-command-conventions` |
| TF-0007 | Done | M1 | Add README developer setup section | `docs/tf-0007-readme-developer-setup` |
| TF-0008 | Done | M2 | Define event envelope and canonical event domains | `feature/tf-0008-event-envelope-domains` |
| TF-0009 | Done | M2 | Define append-only event store interface | `feature/tf-0009-event-store-interface` |
| TF-0010 | Done | M2 | Implement in-memory event store adapter | `feature/tf-0010-in-memory-event-store` |
| TF-0011 | Done | M3 | Define lifecycle state model | `feature/tf-0011-lifecycle-state-model` |
| TF-0012 | Done | M3 | Implement lifecycle transition validator | `feature/tf-0012-lifecycle-transition-validator` |
| TF-0013 | Done | M3 | Implement lifecycle orchestration service | `feature/tf-0013-lifecycle-orchestration-service` |
| TF-0014 | Done | M4 | Create workspace routing model | `M4/tf-0014-workspace-routing-model` |
| TF-0015 | Done | M4 | Define workspace state contracts | `M4/tf-0015-workspace-state-contracts` |
| TF-0016 | Done | M5 | Implement replay projector foundation | `M5/tf-0016-replay-projector-foundation` |
| TF-0017 | Done | M5 | Implement projection rebuild pipeline | `M5/tf-0017-projection-rebuild-pipeline` |
| TF-0018 | Done | M5 | Implement replay timeline engine | `M5/tf-0018-replay-timeline-engine` |
| TF-0019 | Done | M5 | Implement historical reconstruction pipeline | `M5/tf-0019-historical-reconstruction-pipeline` |
| TF-0020 | Done | M6 | Define persona context model | `feature/tf-0020-persona-context-model` |
| TF-0021 | Done | M6 | Implement workspace projection read models | `feature/tf-0021-workspace-projection-read-models` |
| TF-0022 | Done | M6 | Implement operational attention queues | `feature/tf-0022-operational-attention-queues` |
| TF-0023 | Done | M6 | Implement context-aware workspace summaries | `feature/tf-0023-context-aware-workspace-summaries` |
| TF-0024 | Done | M7 | Add Postgres persistence layer | `feature/tf-0024-postgres-persistence` |
| TF-0025 | Done | M7 | Add Alembic migration infrastructure | `feature/tf-0025-alembic-migrations` |
| TF-0026 | Done | M7 | Persist canonical event ledger | `feature/tf-0026-postgres-event-ledger` |
| TF-0027 | Done | M7 | Add FastAPI application runtime | `feature/tf-0027-fastapi-runtime` |
| TF-0028 | Done | M7 | Add lifecycle API endpoints | `feature/tf-0028-lifecycle-api-endpoints` |
| TF-0029 | Done | M7 | Add replay API endpoints | `feature/tf-0029-replay-api-endpoints` |
| TF-0030 | Done | M7 | Add workspace projection APIs | `feature/tf-0030-workspace-projection-apis` |
| TF-0031 | Done | M7 | Create React frontend scaffold | `feature/tf-0031-react-frontend-scaffold` |
| TF-0032 | Done | M7 | Add workspace routing system | `feature/tf-0032-workspace-routing-system` |
| TF-0033 | Done | M7 | Add shared operational layout system | `feature/tf-0033-operational-layout-system` |
| TF-0034 | Done | M7 | Add authentication/session model | `feature/tf-0034-auth-session-model` |
| TF-0035 | Done | M8 | Implement Operating Workspace | `feature/tf-0035-operating-workspace` |
| TF-0036 | Done | M8 | Implement Opportunity Workspace | `feature/tf-0036-opportunity-workspace` |
| TF-0037 | Done | M8 | Implement Plan Review Workspace | `feature/tf-0037-plan-review-workspace` |
| TF-0038 | Done | M8 | Implement Active Position Workspace | `feature/tf-0038-active-position-workspace` |
| TF-0039 | Done | M8 | Implement Replay Workspace | `feature/tf-0039-replay-workspace` |
| TF-0040 | Done | M8 | Implement Review Workspace | `feature/tf-0040-review-workspace` |
| TF-0041 | Done | M8 | Implement first replayable lifecycle flow | `feature/tf-0041-first-operational-mvp-flow` |
| TF-0042 | Done | M9 | Define provider boundary interfaces | `feature/tf-0042-provider-boundary-interfaces` |
| TF-0043 | Done | M9 | Implement normalized market snapshot model | `feature/tf-0043-normalized-market-snapshot-model` |
| TF-0044 | Done | M9 | Add read-only yfinance provider adapter | `feature/tf-0044-yfinance-provider-adapter` |
| TF-0045 | Done | M9 | Add Massive.com market data adapter | `feature/tf-0045-massive-com-provider-adapter` |
| TF-0046 | Done | M9 | Add Alpaca market data adapter | `feature/tf-0046-alpaca-provider-adapter` |
| TF-0047 | Done | M9 | Implement market context workspace overlays | `feature/tf-0047-market-context-overlay` |
| TF-0048 | Done | M9 | Implement market regime interpretation model | `feature/tf-0048-market-regime-interpreter` |
| TF-0049 | Done | M9 | Implement contextual operational summaries | `feature/tf-0049-contextual-operational-summaries` |
| TF-0050 | Done | M9 | Implement provider provenance tracking | `feature/tf-0050-provider-provenance-tracking` |
| TF-0051 | Done | M9 | Add seeded demo market context flow | `feature/tf-0051-seeded-demo-flow` |
| TF-0052 | Done | M9 | Add replay-compatible market snapshot persistence strategy | `feature/tf-0050-provider-provenance-tracking` |
| TF-0053 | Done | M10 | Implement new trade idea workflow | `feature/tf-0053-new-trade-idea-workflow` |
| TF-0054 | Done | M10 | Implement persistent active decision context | `feature/tf-0054-persistent-active-decision-context` |
| TF-0055 | Done | M10 | Eliminate manual workspace context propagation | `feature/tf-0055-eliminate-manual-context-propagation` |
| TF-0056 | Done | M10 | Implement guided lifecycle navigation | `feature/tf-0056-guided-lifecycle-navigation` |
| TF-0057 | Done | M10 | Implement operational workflow continuity model | `feature/tf-0057-workflow-continuity-model` |
| TF-0058 | Done | M10 | Implement guided demo mode | `feature/tf-0058-guided-demo-mode` |
| TF-0059 | Done | M10 | Implement seeded replayable demo scenarios | `feature/tf-0059-seeded-replayable-demo-scenarios` |
| TF-0060 | Done | M10 | Implement one-click operational walkthrough | `feature/tf-0060-one-click-operational-walkthrough` |
| TF-0061 | Done | M10 | Implement operational onboarding flow | `feature/tf-0061-operational-onboarding-flow` |
| TF-0062 | Done | M10 | Implement cross-workspace context persistence | `feature/tf-0062-cross-workspace-context-persistence` |
| TF-0063 | Done | M10 | Stabilize workspace transition ergonomics | `feature/tf-0063-workspace-transition-ergonomics` |
| TF-0064 | Done | M10 | Implement operational attention continuity | `feature/tf-0064-operational-attention-continuity` |
| M10AIS01 | Done | M10A | Implement structured thesis domain model | `feature/tf-0064-operational-attention-continuity` |
| M10AIS02 | Done | M10A | Implement thesis authoring workspace | `feature/tf-0064-operational-attention-continuity` |
| M10AIS03 | Done | M10A | Implement thesis revision history | `feature/tf-0064-operational-attention-continuity` |
| M10AIS04 | Done | M10A | Implement scenario branch modeling | `feature/tf-0064-operational-attention-continuity` |
| M10AIS05 | Done | M10A | Implement scenario visualization projection | `feature/tf-0064-operational-attention-continuity` |
| M10AIS06 | Done | M10A | Implement structured trade plan domain model | `feature/tf-0064-operational-attention-continuity` |
| M10AIS07 | Done | M10A | Implement trade plan authoring workspace | `feature/tf-0064-operational-attention-continuity` |
| M10AIS08 | Done | M10A | Implement plan validation preview layer | `feature/tf-0064-operational-attention-continuity` |
| M10AIS09 | Done | M10A | Implement replay cognitive artifact timeline | `feature/tf-0064-operational-attention-continuity` |
| M10AIS10 | Done | M10A | Implement cognitive snapshot reconstruction | `feature/tf-0064-operational-attention-continuity` |
| M10AIS11 | Done | M10A | Implement structured review reflection model | `feature/tf-0064-operational-attention-continuity` |
| M10AIS12 | Done | M10A | Implement review reflection workspace | `feature/tf-0064-operational-attention-continuity` |
| M10AIS13 | Planned | M10A | Implement replay annotation system | — |
| M10AIS14 | Planned | M10A | Implement playbook alignment projection layer | — |
| M10AIS15 | Planned | M10A | Implement cross-workspace cognitive continuity | — |

Explicit roadmap checkpoint completed M9 Updated*Done*.
M10A started 2026-05-14. M10AIS01-12 complete (13 of 15 issues). Remaining: M10AIS13-15.
Post-MVP Roadmap v2 implementation begins with M9 market-context infrastructure and provider-boundary work. 
M9 remains constrained to read-only advisory context and must not introduce broker execution authority, autonomous AI decision systems, or non-replayable runtime behavior.


---
## TF-0001: Establish Milestone Roadmap And Issue Register

**Status:** Done

**Milestone:** M0

**Branch:** `docs/tf-0001-roadmap-issue-register`

**Affected Layer:** docs

**Linked ADRs:** ADR 0001, ADR 0002, ADR 0003, ADR 0004, ADR 0005, ADR 0006, ADR 0007, ADR 0008, ADR 0009, ADR 0010, ADR 0011

**Impacted Invariants:** Event Sourcing, Decision Lifecycle, Workspace, Persona, AI Authority, Scenario, Event Integrity, Replay, Layer Separation, Architectural Drift

**Implementation Summary:** Create the initial milestone roadmap and `DOCS/ISSUE_REGISTER.md` so future implementation work has a local planning source of truth. The initial roadmap was later superseded by `DOCS/Milestone_Roadmap_v2.md` and preserved as `DOCS/MILESTONE_ROADMAP_DEPRECATED.md`.

**Acceptance Criteria:**

- Milestone roadmap exists under `DOCS/`.
- Issue register exists under `DOCS/`.
- Issue register defines issue IDs, statuses, branch names, affected layers, linked ADRs, impacted invariants, and acceptance criteria.
- Roadmap links milestones to issues and ADRs.

---

## TF-0002: Create Python Project Scaffold With pyproject.toml And uv

**Status:** Done

**Milestone:** M1

**Branch:** `feature/tf-0002-python-project-scaffold`

**Affected Layer:** infrastructure, app

**Linked ADRs:** ADR 0011

**Impacted Invariants:** Layer Separation

**Implementation Summary:** Add the baseline Python project metadata and `uv` workflow needed before domain implementation.

**Acceptance Criteria:**

- `pyproject.toml` exists with project metadata for TradeForge.
- Python version target is 3.12.
- Runtime package discovery includes `src/`.
- `uv` can create or use the project environment.
- No domain semantics are encoded in project tooling.

**Out Of Scope:**

- Domain event model.
- Event store implementation.

---

## TF-0003: Add Dockerfile Using uv Python 3.12 Slim Base Image

**Status:** Done

**Milestone:** M1

**Branch:** `feature/tf-0003-dockerfile-uv-python312`

**Affected Layer:** infrastructure

**Linked ADRs:** ADR 0011

**Impacted Invariants:** Layer Separation

**Implementation Summary:** Add a Dockerfile using `FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim`.

**Acceptance Criteria:**

- Dockerfile uses the accepted uv Python 3.12 slim base image.
- Image installs project dependencies through `uv`.
- Container default command is suitable for local development or test execution.
- Dockerfile does not encode domain behavior.

**Out Of Scope:**

- Production deployment hardening.
- Broker or database services.

---

## TF-0004: Add docker-compose.yml For Local Development

**Status:** Done

**Milestone:** M1

**Branch:** `feature/tf-0004-docker-compose-local-dev`

**Affected Layer:** infrastructure

**Linked ADRs:** ADR 0011

**Impacted Invariants:** Layer Separation

**Implementation Summary:** Add Docker Compose local development orchestration for the runtime container.

**Acceptance Criteria:**

- `docker-compose.yml` defines a local development service for TradeForge.
- Compose builds from the local Dockerfile.
- Source is mounted or otherwise available for local iteration.
- Compose does not imply microservice architecture.

**Out Of Scope:**

- Database, broker, or market-data containers.
- Production orchestration.

---

## TF-0005: Add pytest Baseline And Test Command

**Status:** Done

**Milestone:** M1

**Branch:** `feature/tf-0005-pytest-baseline`

**Affected Layer:** infrastructure, app

**Linked ADRs:** ADR 0011

**Impacted Invariants:** Layer Separation

**Implementation Summary:** Add pytest as the baseline test runner and establish a repeatable test command.

**Acceptance Criteria:**

- `pytest` is available through the project development dependencies.
- A baseline test exists and passes.
- Test command is documented in project tooling or README.
- Test setup does not require live external services.

**Out Of Scope:**

- Domain behavior tests.
- Integration tests with external APIs.

---

## TF-0006: Add Lint, Type, And Dev Command Conventions

**Status:** Done

**Milestone:** M1

**Branch:** `feature/tf-0006-dev-command-conventions`

**Affected Layer:** infrastructure, app

**Linked ADRs:** ADR 0011

**Impacted Invariants:** Layer Separation

**Implementation Summary:** Add `ruff` and `mypy` development dependencies, minimal project configuration, and documented `uv` command conventions for testing, linting, and type checking.

**Acceptance Criteria:**

- Lint command convention is documented.
- Type-check command convention is documented.
- Test command convention is documented.
- Commands run through `uv` where practical.
- Tooling does not define domain semantics.

**Out Of Scope:**

- Strict lint cleanup for future domain code.
- CI pipeline configuration.

**Completed Verification:**

- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy src tests`

---

## TF-0007: Add README Developer Setup Section

**Status:** Done

**Milestone:** M1

**Branch:** `docs/tf-0007-readme-developer-setup`

**Affected Layer:** docs

**Linked ADRs:** ADR 0011

**Impacted Invariants:** Layer Separation

**Implementation Summary:** Document developer setup for `uv`, Docker, Docker Compose, tests, linting, type checking, and local command conventions in `README.md`.

**Acceptance Criteria:**

- README includes local setup commands.
- README includes Docker Compose usage.
- README explains that Docker/uv are execution environment concerns, not domain architecture.
- README points developers back to ADRs and issue discipline before code changes.

**Out Of Scope:**

- User-facing product documentation.

**Completed Verification:**

- `docker compose config`
- `docker compose build tradeforge`
- `docker compose run --rm tradeforge`

---

## TF-0008: Define Event Envelope And Canonical Event Domains

**Status:** Done

**Milestone:** M2

**Branch:** `feature/tf-0008-event-envelope-domains`

**Affected Layer:** domain

**Linked ADRs:** ADR 0001, ADR 0003, ADR 0008

**Impacted Invariants:** Event Sourcing, Event Integrity, Replay, Layer Separation

**Implementation Summary:** Define the framework-free domain event envelope and canonical event domain identifiers for persona, workspace, market, scenario, decision, execution, review, and system events.

**Acceptance Criteria:**

- Event envelope represents immutable facts, not interpretations.
- Event type, timestamp, context, references, payload, and provenance are modeled.
- Canonical event domains align with ADR 0003.
- Domain model contains no persistence or infrastructure logic.

**Out Of Scope:**

- Event store persistence implementation.
- Runtime API entrypoints.

**Completed Verification:**

- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy src tests`

---

## TF-0009: Define Append-Only Event Store Interface

**Status:** Done

**Milestone:** M2

**Branch:** `feature/tf-0009-event-store-interface`

**Affected Layer:** domain

**Linked ADRs:** ADR 0001, ADR 0003, ADR 0008

**Impacted Invariants:** Event Sourcing, Event Integrity, Replay, Layer Separation

**Implementation Summary:** Define the event store port that supports appending immutable events and reading event history in deterministic order.

**Acceptance Criteria:**

- Interface supports append-only writes.
- Interface supports deterministic reads for replay.
- Interface does not expose mutation or deletion of historical events.
- Domain semantics are not defined by infrastructure adapters.

**Out Of Scope:**

- Database-backed event store.
- Broker integration.

**Completed Verification:**

- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy src tests`

---

## TF-0010: Implement In-Memory Event Store Adapter

**Status:** Done

**Milestone:** M2

**Branch:** `feature/tf-0010-in-memory-event-store`

**Affected Layer:** infrastructure

**Linked ADRs:** ADR 0001, ADR 0003, ADR 0008

**Impacted Invariants:** Event Sourcing, Event Integrity, Replay, Layer Separation

**Implementation Summary:** Implement an in-memory event store adapter for tests and early vertical slices.

**Acceptance Criteria:**

- Adapter appends events without mutating prior history.
- Adapter returns events in deterministic order.
- Adapter rejects or avoids historical mutation operations.
- Tests demonstrate append and replay read behavior.

**Out Of Scope:**

- Durable database persistence.
- Distributed event streaming.

**Completed Verification:**

- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy src tests`

---

## TF-0011: Define Lifecycle State Model

**Status:** Done

**Milestone:** M3

**Branch:** `feature/tf-0011-lifecycle-state-model`

**Affected Layer:** domain

**Linked ADRs:** ADR 0002, ADR 0003

**Impacted Invariants:** Decision Lifecycle, Event Integrity, Layer Separation

**Implementation Summary:** Define lifecycle stages and decision aggregate state derived from lifecycle events.

**Acceptance Criteria:**

- Lifecycle stages are exactly `Idea`, `Thesis`, `Plan`, `Approval`, `Execution`, `Position`, and `Review`.
- Domain model does not allow stage merging.
- Current lifecycle state can be derived from event history.
- Domain layer remains framework-agnostic.

**Out Of Scope:**

- Service orchestration.
- UI decision queue.

**Completed Verification:**

- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy src tests`

---

## TF-0012: Implement Lifecycle Transition Validator

**Status:** Done

**Milestone:** M3

**Branch:** `feature/tf-0012-lifecycle-transition-validator`

**Affected Layer:** domain

**Linked ADRs:** ADR 0002, ADR 0003

**Impacted Invariants:** Decision Lifecycle, Event Integrity, Replay, Layer Separation

**Implementation Summary:** Implement deterministic validation for allowed lifecycle transitions.

**Acceptance Criteria:**

- Valid lifecycle transitions are accepted in canonical order.
- Invalid shortcuts such as `Idea -> Position` are rejected.
- Validation is deterministic and replay-compatible.
- Tests cover valid and invalid transitions.

**Out Of Scope:**

- Event store persistence.
- Broker execution.

**Completed Verification:**

- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy src tests`

---

## TF-0013: Implement Lifecycle Orchestration Service

**Status:** Done

**Milestone:** M3

**Branch:** `feature/tf-0013-lifecycle-orchestration-service`

**Affected Layer:** services

**Linked ADRs:** ADR 0001, ADR 0002, ADR 0003

**Impacted Invariants:** Event Sourcing, Decision Lifecycle, Event Integrity, Layer Separation

**Implementation Summary:** Implement a service that coordinates lifecycle transition requests, invokes domain validation, and appends valid lifecycle events through the event store port.

**Acceptance Criteria:**

- Service orchestrates but does not define domain rules.
- Valid transitions append lifecycle events.
- Invalid transitions do not append events.
- Service does not directly manage infrastructure persistence details.

**Out Of Scope:**

- UI workflows.
- Live trading execution.

**Completed Verification:**

- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy src tests`

---

## TF-0014: Create Workspace Routing Model

**Status:** Done

**Milestone:** M4

**Branch:** `M4/tf-0014-workspace-routing-model`

**Affected Layer:** app, services

**Linked ADRs:** ADR 0004, ADR 0007, ADR 0009, ADR 0012

**Impacted Invariants:** Workspace, Persona, Replay, Layer Separation

**Implementation Summary:** Defined immutable workspace routing contracts and an app entrypoint helper for the ADR 0012 workspace set without treating routes as workspace truth.

**Acceptance Criteria:**

- MVP workspace routes are named and bounded.
- Routing preserves persona and selected workflow context.
- Routes do not mutate lifecycle state directly.
- Design references align with the KB `design/` draft layer.

**Out Of Scope:**

- Full React implementation.
- Dashboard-style generic routing.

**Completed Verification:**

- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy src tests`

---

## TF-0015: Define Workspace State Contracts

**Status:** Done

**Milestone:** M4

**Branch:** `M4/tf-0015-workspace-state-contracts`

**Affected Layer:** domain, services, docs

**Linked ADRs:** ADR 0004, ADR 0007, ADR 0008, ADR 0012, ADR 0013

**Impacted Invariants:** Event Sourcing, Workspace, Persona, Replay, Layer Separation

**Implementation Summary:** Defined immutable read-model contracts for the ADR 0012 workspace set: Operating, Opportunity, Plan Review, Active Position, Replay, Review, Market Context, and Playbooks / Doctrine.

**Acceptance Criteria:**

- Each ADR 0012 workspace has an explicit derived-state contract.
- Contracts distinguish canonical, derived, inferred, and advisory fields.
- Contracts identify required event inputs and replay needs.
- No workspace contract owns canonical lifecycle state.

**Out Of Scope:**

- Persistent projection storage.
- Full UI implementation.

**Completed Verification:**

- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy src tests`

---

## TF-0016: Implement Replay Projector Foundation

**Status:** Done

**Milestone:** M5

**Branch:** `M5/tf-0016-replay-projector-foundation`

**Affected Layer:** domain, services

**Linked ADRs:** ADR 0001, ADR 0003, ADR 0008, ADR 0014

**Impacted Invariants:** Event Sourcing, Replay, Event Integrity, Layer Separation

**Implementation Summary:** Implemented a pure domain replay projector and services-layer projection wrapper that derive discardable replay projection state from ordered event history through the event store port.

**Acceptance Criteria:**

- Replay consumes event history, not live APIs or UI state.
- Projector output is deterministic for the same event stream.
- Replay reconstructs lifecycle state for a basic workflow.
- Projection output remains derived and discardable.

**Out Of Scope:**

- AI-generated replay summaries.
- Historical market-data integrations.

**Completed Verification:**

- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy src tests`

---

## TF-0017: Implement Projection Rebuild Pipeline

**Status:** Done

**Milestone:** M5

**Branch:** `M5/tf-0017-projection-rebuild-pipeline`

**Affected Layer:** services

**Linked ADRs:** ADR 0001, ADR 0004, ADR 0008, ADR 0014

**Impacted Invariants:** Event Sourcing, Replay, Layer Separation

**Implementation Summary:** Implemented a services-layer projection rebuild pipeline that reads event history through the event store port, rebuilds configured projection targets in deterministic order, and returns an immutable derived rebuild report.

**Acceptance Criteria:**

- Projections can be rebuilt from event history.
- Rebuild order is deterministic.
- Rebuild output does not become canonical truth.
- Tests cover repeatable projection output.

**Out Of Scope:**

- Durable projection persistence.

**Completed Verification:**

- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy src tests`

---

## TF-0018: Implement Replay Timeline Engine

**Status:** Done

**Milestone:** M5

**Branch:** `M5/tf-0018-replay-timeline-engine`

**Affected Layer:** domain, services

**Linked ADRs:** ADR 0008, ADR 0014

**Impacted Invariants:** Replay, Event Integrity, Historical Integrity

**Implementation Summary:** Implemented a pure domain replay timeline builder and services-layer timeline wrapper that derive immutable timeline entries for lifecycle, execution, review, and system events from event history.

**Acceptance Criteria:**

- Timeline orders lifecycle, execution, review, and relevant system events deterministically.
- Timeline entries preserve event references and provenance.
- Timeline model supports replay UI without depending on UI state.

**Out Of Scope:**

- Interactive frontend timeline.

**Completed Verification:**

- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy src tests`

---

## TF-0019: Implement Historical Reconstruction Pipeline

**Status:** Done

**Milestone:** M5

**Branch:** `M5/tf-0019-historical-reconstruction-pipeline`

**Affected Layer:** services

**Linked ADRs:** ADR 0008, ADR 0014

**Impacted Invariants:** Replay, Historical Integrity, Layer Separation

**Implementation Summary:** Implemented a services-layer historical reconstruction pipeline that composes event facts, replay projection, replay timeline, source-linked notes, review artifacts, and explicit inferred-state boundaries from event history.

**Acceptance Criteria:**

- Reconstruction can answer what was known and visible at replay time.
- Reconstruction does not call live APIs.
- Reconstruction keeps facts, derived state, and inferred state distinguishable.

**Out Of Scope:**

- AI replay narration.

**Completed Verification:**

- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy src tests`

---

## TF-0020: Define Persona Context Model

**Status:** Done

**Milestone:** M6

**Branch:** `feature/tf-0020-persona-context-model`

**Affected Layer:** domain

**Linked ADRs:** ADR 0009

**Impacted Invariants:** Persona, Workspace, Replay, Layer Separation

**Implementation Summary:** Defined immutable domain persona context contracts for versioned interpretation profiles, workspace/workflow association, and bounded interpretive influence without modeling personas as users, UI preferences, lifecycle authorities, event writers, or execution authorities.

**Acceptance Criteria:**

- Persona is not modeled as a user account or UI preference.
- Persona can be associated with workspace and workflow context.
- Persona influence is interpretive only.
- Historical replay can preserve persona context.

**Out Of Scope:**

- Authentication.

**Completed Verification:**

- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy src tests`

---

## TF-0021: Implement Workspace Projection Read Models

**Status:** Done

**Milestone:** M6

**Branch:** `feature/tf-0021-workspace-projection-read-models`

**Affected Layer:** domain, services

**Linked ADRs:** ADR 0004, ADR 0007, ADR 0008, ADR 0009, ADR 0012

**Impacted Invariants:** Event Sourcing, Workspace, Persona, Replay, Layer Separation

**Implementation Summary:** Implemented immutable, persona/workspace-scoped workspace projection read models that derive ADR 0012 workspace state from ordered event history and deterministic rules. Added a projection read service and rebuild-pipeline-compatible projectors without adding canonical state, persistence, API endpoints, UI, or lifecycle authority.

**Acceptance Criteria:**

- Workspace state is derived from events and deterministic rules.
- Workspace surfaces do not mutate canonical state.
- Workspace context is persona-scoped.
- Workspace projections can be rebuilt.

**Out Of Scope:**

- React UI.
- Stored workspace state as canonical truth.

**Completed Verification:**

- `uv run pytest tests\test_workspace_projection_read_models.py`
- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy src tests`

---

## TF-0022: Implement Operational Attention Queues

**Status:** Done

**Milestone:** M6

**Branch:** `feature/tf-0022-operational-attention-queues`

**Affected Layer:** domain, services

**Linked ADRs:** ADR 0013

**Impacted Invariants:** Workflow-Centric Architecture, Workspace, Human Decision Sovereignty

**Implementation Summary:** Implemented immutable derived operational attention queues that explain required human attention from lifecycle, review, risk, opportunity, market context, and workspace projection inputs. Queue ordering is deterministic and persona-aware through existing risk framing and decision velocity context without authorizing execution or lifecycle transitions.

**Acceptance Criteria:**

- Queues are derived from lifecycle, risk, review, and workspace context.
- Queue items explain why attention is required.
- Queue items do not authorize execution by themselves.
- Queue ordering is deterministic and persona-aware where applicable.

**Out Of Scope:**

- AI prioritization.

**Completed Verification:**

- `uv run pytest tests\test_operational_attention_queues.py`
- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy src tests`

---

## TF-0023: Implement Context-Aware Workspace Summaries

**Status:** Done

**Milestone:** M6

**Branch:** `feature/tf-0023-context-aware-workspace-summaries`

**Affected Layer:** services

**Linked ADRs:** ADR 0004, ADR 0009, ADR 0012

**Impacted Invariants:** Workspace, Persona, Derived State Distinction

**Implementation Summary:** Implemented deterministic, non-AI workspace summaries derived from workspace projections and operational attention queues. Summaries preserve explicit source inputs, source event references, attention references, persona-shaped emphasis, and non-authoritative boundaries.

**Acceptance Criteria:**

- Summaries are derived and non-authoritative.
- Summary inputs are explicit.
- Persona context can shape emphasis without mutating facts.
- Summaries remain replay-compatible.

**Out Of Scope:**

- AI-generated summaries.

**Completed Verification:**

- `uv run pytest tests\test_workspace_summaries.py`
- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy src tests`

---

## TF-0024: Add Postgres Persistence Layer

**Status:** Done

**Milestone:** M7

**Branch:** `feature/tf-0024-postgres-persistence`

**Affected Layer:** infrastructure

**Linked ADRs:** ADR 0018

**Impacted Invariants:** Event Sourcing, Replay, Layer Separation

**Implementation Summary:** Add Postgres infrastructure for durable runtime persistence.

**Acceptance Criteria:**

- Postgres is available in local development.
- Infrastructure does not redefine domain semantics.
- Persistence layer remains behind ports/adapters.

**Out Of Scope:**

- Projection persistence.
- Broker integrations.

**Completed Verification:**

- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy src tests`
- `docker compose config`
- `docker compose up -d postgres`
- `docker compose ps postgres`

---

## TF-0025: Add Alembic Migration Infrastructure

**Status:** Done

**Milestone:** M7

**Branch:** `feature/tf-0025-alembic-migrations`

**Affected Layer:** infrastructure

**Linked ADRs:** ADR 0018, ADR 0019

**Impacted Invariants:** Replay, Layer Separation

**Implementation Summary:** Add migration infrastructure for Postgres-backed runtime tables.

**Acceptance Criteria:**

- Migration command is documented.
- Initial schema migrations are deterministic.
- Migration tooling does not define domain truth.

**Out Of Scope:**

- Production deployment.

**Completed Verification:**

- `uv lock`
- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy src tests`
- `docker compose config`
- `uv run alembic upgrade head`
- `uv run alembic current`

---

## TF-0026: Persist Canonical Event Ledger

**Status:** Done

**Milestone:** M7

**Branch:** `feature/tf-0026-postgres-event-ledger`

**Affected Layer:** infrastructure

**Linked ADRs:** ADR 0001, ADR 0003, ADR 0018

**Impacted Invariants:** Event Sourcing, Event Integrity, Replay

**Implementation Summary:** Implement a Postgres event store adapter for the canonical event ledger.

**Acceptance Criteria:**

- Events are append-only.
- Reads return deterministic event ordering.
- Prior events cannot be mutated or deleted through the adapter.
- Existing event store port remains the runtime boundary.

**Out Of Scope:**

- Event streaming infrastructure.

**Completed Verification:**

- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy src tests`
- `docker compose config`
- `uv run alembic upgrade head`
- `uv run alembic current`
- Live `PostgresEventStore` append/read/mutation-guard check against local Postgres.

---

## TF-0027: Add FastAPI Application Runtime

**Status:** Done

**Milestone:** M7

**Branch:** `feature/tf-0027-fastapi-runtime`

**Affected Layer:** app

**Linked ADRs:** ADR 0020

**Impacted Invariants:** Layer Separation, Decision Lifecycle

**Implementation Summary:** Add FastAPI as the HTTP application boundary.

**Acceptance Criteria:**

- FastAPI app starts locally.
- App routes delegate to services.
- HTTP layer does not own domain rules.

**Out Of Scope:**

- Frontend implementation.

**Completed Verification:**

- `uv lock`
- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy src tests`
- `docker compose config`
- `uv run uvicorn src.app.api.application:app --host 127.0.0.1 --port 8000`

---

## TF-0028: Add Lifecycle API Endpoints

**Status:** Done

**Milestone:** M7

**Branch:** `feature/tf-0028-lifecycle-api-endpoints`

**Affected Layer:** app, services

**Linked ADRs:** ADR 0002, ADR 0020

**Impacted Invariants:** Decision Lifecycle, Human Decision Sovereignty

**Implementation Summary:** Expose lifecycle transition requests through API endpoints backed by lifecycle services.

**Acceptance Criteria:**

- Endpoints validate through lifecycle orchestration.
- Invalid transitions return explicit errors.
- Accepted transitions append events through the event store port.

**Out Of Scope:**

- Broker execution.

**Completed Verification:**

- `uv run pytest tests\test_fastapi_runtime.py tests\test_lifecycle_orchestration_service.py`
- `uv run pytest`

---

## TF-0029: Add Replay API Endpoints

**Status:** Done

**Milestone:** M7

**Branch:** `feature/tf-0029-replay-api-endpoints`

**Affected Layer:** app, services

**Linked ADRs:** ADR 0008, ADR 0014, ADR 0020

**Impacted Invariants:** Replay, Historical Integrity

**Implementation Summary:** Expose replay reconstruction and timeline read APIs.

**Acceptance Criteria:**

- Endpoints return replay-derived read models.
- Replay output is deterministic for a given event history.
- Endpoints do not call live market APIs.

**Out Of Scope:**

- AI replay narration.

**Completed Verification:**

- `uv run pytest tests\test_fastapi_runtime.py tests\test_replay_projection_service.py tests\test_replay_timeline_service.py tests\test_historical_reconstruction_pipeline.py`
- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy src tests`

---

## TF-0030: Add Workspace Projection APIs

**Status:** Done

**Milestone:** M7

**Branch:** `feature/tf-0030-workspace-projection-apis`

**Affected Layer:** app, services

**Linked ADRs:** ADR 0004, ADR 0012, ADR 0020

**Impacted Invariants:** Workspace, Derived State Distinction

**Implementation Summary:** Expose workspace projection read models through read-only FastAPI endpoints backed by `WorkspaceProjectionReadService`. The APIs require explicit persona/workspace context, return derived projection state with source event references and authority boundaries, and do not mutate lifecycle or event ledger state.

**Acceptance Criteria:**

- APIs return derived workspace state.
- APIs do not mutate canonical lifecycle state.
- Persona/workspace context is explicit.

**Out Of Scope:**

- Frontend rendering.

**Completed Verification:**

- `uv run pytest tests\test_fastapi_runtime.py tests\test_workspace_projection_read_models.py`
- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy src tests`

---

## TF-0031: Create React Frontend Scaffold

**Status:** Done

**Milestone:** M7

**Branch:** `feature/tf-0031-react-frontend-scaffold`

**Affected Layer:** frontend

**Linked ADRs:** ADR 0021

**Impacted Invariants:** Workspace, UX Is Architectural

**Implementation Summary:** Created the React/TypeScript frontend foundation for MVP workspaces under `frontend/`, including Vite configuration, typed runtime API boundary access, a minimal workspace runtime shell, frontend command documentation, and ADR 0021 for the React workspace runtime boundary.

**Acceptance Criteria:**

- Frontend project runs locally.
- TypeScript is enabled.
- Frontend consumes API boundaries rather than event store internals.

**Out Of Scope:**

- Full workspace implementation.

**Completed Verification:**

- `npm.cmd install`
- `npm.cmd run lint`
- `npm.cmd run typecheck`
- `npm.cmd run build`
- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy src tests`

---

## TF-0032: Add Workspace Routing System

**Status:** Done

**Milestone:** M7

**Branch:** `feature/tf-0032-workspace-routing-system`

**Affected Layer:** frontend

**Linked ADRs:** ADR 0012, ADR 0021

**Impacted Invariants:** Workspace, Workflow Continuity

**Implementation Summary:** Implemented typed React workspace routing for the six core MVP workspaces with browser-history navigation, context-preserving route URLs, and derived route entry surfaces that remain inside the frontend/API presentation boundary.

**Acceptance Criteria:**

- Routes exist for the six core MVP workspaces.
- Navigation preserves selected context where applicable.
- Routes do not imply workspace ownership of canonical state.

**Out Of Scope:**

- Final visual design polish.

**Completed Verification:**

- `npm.cmd run typecheck`
- `npm.cmd run lint`
- `npm.cmd run build`
- `uv run pytest tests\test_workspace_routing.py`
- `uv run pytest`

---

## TF-0033: Add Shared Operational Layout System

**Status:** Done

**Milestone:** M7

**Branch:** `feature/tf-0033-operational-layout-system`

**Affected Layer:** frontend

**Linked ADRs:** ADR 0007, ADR 0012, ADR 0021

**Impacted Invariants:** UX Is Architectural, Workspace

**Implementation Summary:** Implemented `frontend/DESIGN.md` as a frontend runtime design translation artifact and added shared React operational layout primitives for navigation, context panels, workspace briefing, runtime boundary panels, and operational surfaces.

**Acceptance Criteria:**

- Layout supports workspace continuity.
- UI avoids dashboard-first composition.
- Components distinguish action, context, and review surfaces.
- `frontend/DESIGN.md` translates frontend tokens and layout rationale without redefining KB or ADR semantics.

**Out Of Scope:**

- Full design system library.

**Completed Verification:**

- `npm.cmd run typecheck`
- `npm.cmd run lint`
- `npm.cmd run build`
- `uv run pytest tests\test_workspace_routing.py`
- `uv run pytest`

---

## TF-0034: Add Authentication/Session Model

**Status:** Done

**Milestone:** M7

**Branch:** `feature/tf-0034-auth-session-model`

**Affected Layer:** app, frontend

**Linked ADRs:** ADR 0022

**Impacted Invariants:** Persona, Workspace, Replay

**Implementation Summary:** Added ADR 0022, immutable app-layer runtime session contracts, a local session provider, a read-only `GET /session` API endpoint, and frontend session consumption that keeps user/session identity separate from active persona and workspace context.

**Acceptance Criteria:**

- User/session identity is not confused with Persona.
- Persona activation remains explicit.
- Session context supports workspace continuity.

**Out Of Scope:**

- Full multi-user authorization model.

**Completed Verification:**

- `uv run pytest tests\test_session_model.py tests\test_fastapi_runtime.py tests\test_workspace_routing.py`
- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy src tests`
- `npm.cmd run typecheck`
- `npm.cmd run lint`
- `npm.cmd run build`

---

## TF-0035: Implement Operating Workspace

**Status:** Done

**Milestone:** M8

**Branch:** `feature/tf-0035-operating-workspace`

**Affected Layer:** frontend, app, services

**Linked ADRs:** ADR 0012, ADR 0013, ADR 0021, ADR 0023

**Impacted Invariants:** Workspace, Workflow-Centric Architecture, UX Is Architectural

**Implementation Summary:** Implemented the MVP Operating Workspace as the daily operational attention surface. Added `GET /workspaces/operating/attention` backend endpoint backed by `OperationalAttentionQueueReadService` with a default MVP persona profile. Created `OperatingWorkspace` React component that fetches and renders the ordered attention queue with lifecycle stage context, priority-coded item cards, and authority boundaries. The `App.tsx` now renders `OperatingWorkspace` for the operating route; all other workspace routes retain the existing placeholder surface.

**Acceptance Criteria:**

- Displays decision queue, active positions, watch opportunities, alerts, and review obligations.
- Prioritizes decision state over market data.
- Actions route through lifecycle/API boundaries.

**Out Of Scope:**

- Market dashboard features.

**Completed Verification:**

- `uv run pytest tests/test_operating_workspace.py`
- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy src tests`
- `npm.cmd run typecheck`
- `npm.cmd run lint`
- `npm.cmd run build`

---

## TF-0036: Implement Opportunity Workspace

**Status:** Done

**Milestone:** M8

**Branch:** `feature/tf-0036-opportunity-workspace`

**Affected Layer:** frontend

**Linked ADRs:** ADR 0002, ADR 0007, ADR 0012, ADR 0021, ADR 0023

**Impacted Invariants:** Scenario, Decision Lifecycle, Workspace, UX Is Architectural

**Implementation Summary:** Implemented the Opportunity Workspace as the structured pre-decision cognition surface. Added `LifecycleTransitionRequest`/`Response` types and `postLifecycleTransition` fetch function to `api/runtime.ts`. Created `OpportunityWorkspace.tsx` displaying the projection's four field surfaces labeled by authority (canonical/derived/inferred/advisory), a "Develop Thesis" lifecycle action (Idea-stage only, routing through `POST /lifecycle/transitions`), a chart deferred placeholder, and authority boundaries. Introduced the `FieldSurface` component pattern (reusable for subsequent M8 workspaces). Added field authority surface CSS. Updated `App.tsx` to render `OpportunityWorkspace` for the opportunity route. No new backend endpoints — existing projection and lifecycle transition APIs are sufficient.

**Acceptance Criteria:**

- Shows opportunity state, thesis, setup, risks, and conditions.
- Promotion to plan cannot bypass lifecycle semantics.
- Charts support reasoning but do not dominate.

**Out Of Scope:**

- Scenario engine automation.

**Completed Verification:**

- `uv run pytest` — 183 passed
- `uv run ruff check .` — clean
- `uv run mypy src tests` — clean
- `npm.cmd run typecheck` — clean
- `npm.cmd run lint` — clean
- `npm.cmd run build` — clean

---

## TF-0037: Implement Plan Review Workspace

**Status:** Done

**Milestone:** M8

**Branch:** `feature/tf-0037-plan-review-workspace`

**Affected Layer:** frontend

**Linked ADRs:** ADR 0002, ADR 0012, ADR 0021, ADR 0023

**Impacted Invariants:** Decision Lifecycle, Human Decision Sovereignty, UX Is Architectural

**Implementation Summary:** Implemented the Plan Review Workspace as the deliberate risk authorization surface. Created `PlanReviewWorkspace.tsx` following the `FieldSurface` component pattern (OpportunityWorkspace). Workspace fetches the `plan-review` projection via the existing `GET /workspaces/{route_id}` endpoint and displays three field surfaces: `plan_references` (canonical — event-backed thesis/plan facts), `risk_review` (derived — plan payload review), and `rule_evaluation` (inferred — plan readiness interpretation). When lifecycle stage is `Plan`, an "Authorize Plan" action is available that routes through `POST /lifecycle/transitions` to the `Approval` stage. UI framing avoids BUY/SELL brokerage-ticket language — the action label and explanatory note frame authorization as deliberate risk acceptance. Updated `App.tsx` to render `PlanReviewWorkspace` for the `plan-review` route. No new backend endpoints required.

**Acceptance Criteria:**

- Displays thesis, risk model, rule validation, sizing, and final decision context.
- Approval/rejection routes through lifecycle services.
- UI avoids BUY/SELL brokerage-ticket framing.

**Out Of Scope:**

- Broker execution.

**Completed Verification:**

- `uv run pytest` — 183 passed
- `uv run ruff check .` — clean
- `uv run mypy src tests` — clean
- `npm.cmd run typecheck` — clean
- `npm.cmd run lint` — clean
- `npm.cmd run build` — clean

---

## TF-0038: Implement Active Position Workspace

**Status:** Done

**Milestone:** M8

**Branch:** `feature/tf-0038-active-position-workspace`

**Affected Layer:** frontend

**Linked ADRs:** ADR 0012, ADR 0021, ADR 0023

**Impacted Invariants:** Workspace, Replay, Historical Integrity

**Implementation Summary:** Implemented the Active Position Workspace as the decision-state supervision surface. Created `ActivePositionWorkspace.tsx` following the `FieldSurface` component pattern. Workspace fetches the `active-position` projection via the existing `GET /workspaces/{route_id}` endpoint and displays three field surfaces: `position_references` (canonical — execution and decision facts), `exposure_summary` (derived — exposure from execution history), and `thesis_drift` (inferred — position state interpreted against thesis context). Authority boundaries are displayed prominently to prevent treating exposure summaries as canonical truth. When lifecycle stage is `Position`, a "Begin Position Review" lifecycle action routes through `POST /lifecycle/transitions` to the `Review` stage — framed as opening the review workflow, not closing the position. Updated `App.tsx` to render `ActivePositionWorkspace` for the `active-position` route. No new backend endpoints required.

**Acceptance Criteria:**

- Shows position state, thesis integrity context, timeline, actions, notes, and risk.
- PnL is visible but not dominant.
- Position actions remain workflow-aware.

**Out Of Scope:**

- Live broker sync.

**Completed Verification:**

- `uv run pytest` — 183 passed
- `uv run ruff check .` — clean
- `uv run mypy src tests` — clean
- `npm.cmd run typecheck` — clean
- `npm.cmd run lint` — clean
- `npm.cmd run build` — clean

---

## TF-0039: Implement Replay Workspace

**Status:** Done

**Milestone:** M8

**Branch:** `feature/tf-0039-replay-workspace`

**Affected Layer:** frontend

**Linked ADRs:** ADR 0008, ADR 0014, ADR 0021, ADR 0023

**Impacted Invariants:** Replay, Historical Integrity, AI Advisory Boundary

**Implementation Summary:** Implemented the Replay Workspace as the cognitive reconstruction surface. Added `ReplayTimelineEntry` and `ReplayTimeline` TypeScript types plus `fetchReplayTimeline` function (`GET /replay/timeline`) to `api/runtime.ts`. Created `ReplayWorkspace.tsx` that fetches the `replay` workspace projection and the replay timeline in parallel. Displays four field surfaces: `event_timeline_references` (canonical — ordered source event references), `reconstructed_workspace_state` (derived — reconstruction from historical inputs), `historical_interpretation` (inferred — what was visible then), and `advisory_replay_summary` (advisory — optional non-authoritative context). The timeline section renders each entry with a kind badge (Lifecycle / Execution / Review / System), event type, lifecycle stage where present, sequence number, and timestamp. Authority boundaries are displayed explicitly: reconstruction is derived and discardable; replay does not mutate event history. No lifecycle action — the Replay Workspace is read-only per contract. Updated `App.tsx` to render `ReplayWorkspace` for the `replay` route. No new backend endpoints required.

**Acceptance Criteria:**

- Displays replay timeline, context, lifecycle events, rule evaluations, and notes.
- Reconstruction depends on replay services, not live APIs or UI state.
- AI narration is not required.

**Out Of Scope:**

- AI replay assistance.

**Completed Verification:**

- `uv run pytest` — 183 passed
- `uv run ruff check .` — clean
- `uv run mypy src tests` — clean
- `npm.cmd run typecheck` — clean
- `npm.cmd run lint` — clean
- `npm.cmd run build` — clean

---

## TF-0040: Implement Review Workspace

**Status:** Done

**Milestone:** M8

**Branch:** `feature/tf-0040-review-workspace`

**Affected Layer:** frontend

**Linked ADRs:** ADR 0017, ADR 0021, ADR 0023

**Impacted Invariants:** Review, Replay, Human Decision Sovereignty

**Implementation Summary:** Implemented the Review Workspace as the reflective learning surface that separates decision quality from outcome. Created `ReviewWorkspace.tsx` following the `FieldSurface` component pattern. Fetches the `review` workspace projection via `GET /workspaces/{route_id}` and displays three field surfaces: `review_references` (canonical — review and lifecycle event references), `decision_quality_context` (derived — review context from lifecycle and outcome history), and `behavioral_signal` (inferred — interpretive discipline or behavior pattern signal). Two lifecycle-aware states are handled: when at `Position` stage, a "Complete Review" action routes through `POST /lifecycle/transitions` to `Review` stage with provenance `{ actor: "human", source: "review-workspace" }`; when already at `Review` stage, a completion note is shown with a `CheckCircle` indicator confirming the review is durable in the event ledger. The action note explicitly frames review as separating process quality from PnL outcome. Authority boundaries are displayed. Updated `App.tsx` to render `ReviewWorkspace` for the `review` route. No new backend endpoints required.

**Acceptance Criteria:**

- Captures review artifact fields.
- Shows rule adherence, replay highlights, lessons, and future adjustments.
- Review completion is event-backed.

**Out Of Scope:**

- Behavioral intelligence engine.

**Completed Verification:**

- `uv run pytest` — 183 passed
- `uv run ruff check .` — clean
- `uv run mypy src tests` — clean
- `npm.cmd run typecheck` — clean
- `npm.cmd run lint` — clean
- `npm.cmd run build` — clean

---

## TF-0041: Implement First Replayable Lifecycle Flow

**Status:** Done

**Milestone:** M8

**Branch:** `feature/tf-0041-first-operational-mvp-flow`

**Affected Layer:** frontend, services, tests

**Linked ADRs:** ADR 0001, ADR 0002, ADR 0004, ADR 0008, ADR 0023

**Impacted Invariants:** Event Sourcing, Decision Lifecycle, Workspace, Replay, Review

**Implementation Summary:** Closed the three UI lifecycle gaps that prevented end-to-end traversal, and proved the full chain with an integration test suite. Gap analysis: the attention queue routes `Thesis` and `Approval` stages to the Plan Review workspace and `Execution` to Active Position, but those workspaces only acted on a subset of stages. Fixed by: (1) adding `Create Plan` (Thesis→Plan) and `Record Execution` (Approval→Execution) action gates to `PlanReviewWorkspace.tsx` via a shared `makeTransitionHandler` factory; (2) adding `Record Position Opened` (Execution→Position) gate to `ActivePositionWorkspace.tsx` using the same pattern. All six action gates are now mutually exclusive per lifecycle stage and route through `POST /lifecycle/transitions`. Created `tests/test_mvp_lifecycle_flow.py` with 7 integration tests proving: full chain acceptance, event immutability and ordering, replay timeline reconstruction of all stages, workspace projections tracking each stage, skip-stage rejection, replay read-only invariant, and empty attention queue after `Review`. No new backend endpoints or infrastructure required.

**Acceptance Criteria:**

- A user-controlled workflow progresses from Idea through Review.
- Material state changes are event-backed.
- Workspace state is derived from projections.
- Replay reconstructs workflow context.
- No autonomous AI or live broker execution is included.

**Out Of Scope:**

- M9 market/scenario intelligence.
- M10 AI advisory integration.

**Completed Verification:**

- `uv run pytest` — 190 passed
- `uv run pytest tests/test_mvp_lifecycle_flow.py -v` — 7/7 passed
- `uv run ruff check .` — clean
- `uv run mypy src tests` — clean (65 files)
- `npm.cmd run typecheck` — clean
- `npm.cmd run lint` — clean
- `npm.cmd run build` — clean

---

## TF-0042: Define Provider Boundary Interfaces

**Status:** Done

**Milestone:** M9

**Branch:** `feature/tf-0042-provider-boundary-interfaces`

**Affected Layer:** domain

**Linked ADRs:** ADR-0010, ADR-0032

**Impacted Invariants:** Event Sourcing, Event Integrity, Replay, Historical Integrity, Layer Separation, Market Intelligence Is Interpreted Context

**Implementation Summary:** Created `src/domain/market/` as the new domain market module with three files. `snapshot.py` defines immutable advisory value objects: `MarketRegime` (StrEnum), `ProviderProvenance` (fetched_at + data_as_of for replay integrity), `PriceOHLCV` (Decimal OHLCV with OHLCV invariant validation), and `MarketSnapshot` (advisory = always True). `provider.py` defines the `MarketDataProvider` Protocol port (structural subtyping, consistent with EventStore pattern) and `ProviderUnavailableError` for explicit failure handling. All provider adapters (TF-0044 to TF-0046) must implement this Protocol. Market snapshots are non-canonical advisory context and must never enter the event ledger.

**Acceptance Criteria:**

- Normalized market snapshot contract exists independent of any provider SDK.
- Provider port interface (Protocol) defined and structurally verifiable.
- Provider provenance records fetched_at and data_as_of for replay integrity.
- Market snapshots carry is_advisory=True as explicit machine-readable contract.
- All domain models are immutable frozen dataclasses.
- No coupling to any external provider library.

**Out Of Scope:**

- Actual yfinance, Polygon, or Alpaca adapters (TF-0044 to TF-0046).
- Workspace context overlays (TF-0047).
- Snapshot persistence (TF-0052).

**Completed Verification:**

- `uv run pytest tests/test_provider_boundary.py` — 28 passed
- `uv run pytest` — 218 passed
- `uv run ruff check .` — clean
- `uv run mypy src tests` — clean (69 files)

---

## TF-0043: Implement Normalized Market Snapshot Model

**Status:** Done

**Milestone:** M9

**Branch:** `feature/tf-0043-normalized-market-snapshot-model`

**Affected Layer:** services

**Linked ADRs:** ADR-0010, ADR-0032

**Impacted Invariants:** Layer Separation, Market Intelligence Is Interpreted Context, Derived State Must Remain Distinguishable

**Implementation Summary:** Created `src/services/market/` with `MarketContextRequest` (symbols + optional persona_id), `SymbolFetchResult` (discriminated union: success with snapshot OR failure with error_reason), `MarketContextResult` (available snapshots, unavailable symbols, per-symbol record, is_complete/is_partial/is_empty properties, snapshot_for lookup, always ADVISORY authority), and `MarketSnapshotService` (stateless orchestrator: fetch_context captures partial failures gracefully, fetch_snapshot propagates ProviderUnavailableError explicitly). persona_id on MarketContextRequest is an optional placeholder for future persona-shaped context weighting in M10. No infrastructure coupling. No event ledger writes.

**Acceptance Criteria:**

- Normalized result model exists independent of any provider SDK.
- Partial provider failures are captured without raising — workspace overlays can render partial context.
- Authority is always ADVISORY on all result objects.
- fetch_snapshot propagates ProviderUnavailableError explicitly.
- Service is stateless — no caching, no hidden mutable state.

**Out Of Scope:**

- Provider adapters (TF-0044 to TF-0046).
- Workspace overlays (TF-0047).
- Snapshot persistence (TF-0052).

**Completed Verification:**

- `uv run pytest tests/test_market_snapshot_service.py` — 36 passed
- `uv run pytest` — 254 passed
- `uv run ruff check .` — clean
- `uv run mypy src tests` — clean (73 files)

---

## TF-0044: Add Read-Only yfinance Provider Adapter

**Status:** Done

**Milestone:** M9

**Branch:** `feature/tf-0044-yfinance-provider-adapter`

**Affected Layer:** infrastructure

**Linked ADRs:** ADR-0032

**Impacted Invariants:** Layer Separation, Market Intelligence Is Interpreted Context, Event Integrity (no ledger writes)

**Implementation Summary:** Created `src/infrastructure/market/YFinanceProvider` satisfying the `MarketDataProvider` Protocol structurally. Added yfinance>=1.3.0 as a runtime dependency. Added `[[tool.mypy.overrides]]` for yfinance and pandas (ignore_missing_imports=true). Adapter uses `ticker.history(period="1d")`, takes the latest row, converts numpy float64 prices via `str(float())` to `Decimal`, normalizes timestamps to UTC. All SDK errors and empty-DataFrame responses are wrapped in `ProviderUnavailableError`. yfinance coupling is fully contained in this file — domain and services layers have no yfinance imports. Tests use `unittest.mock.patch` — no real network calls.

**Acceptance Criteria:**

- Adapter satisfies `MarketDataProvider` Protocol (structural, no inheritance).
- Returns `MarketSnapshot` with full `ProviderProvenance` (fetched_at + data_as_of).
- All SDK errors map to `ProviderUnavailableError`.
- No event ledger writes anywhere in the adapter.
- Tests do not make real network calls.

**Out Of Scope:**

- Polygon/Massive.com adapter (TF-0045).
- Alpaca adapter (TF-0046).
- Caching or rate-limit handling.
- Intraday or multi-day history ranges.

**Completed Verification:**

- `uv run pytest tests/test_yfinance_adapter.py` — 20 passed (all mocked)
- `uv run pytest` — 274 passed
- `uv run ruff check .` — clean
- `uv run mypy src tests` — clean (76 files)

---

## TF-0045: Add Massive.com Market Data Adapter

**Status:** Done

**Milestone:** M9

**Branch:** `feature/tf-0045-massive-com-provider-adapter`

**Affected Layer:** infrastructure

**Linked ADRs:** ADR-0032

**Impacted Invariants:** Layer Separation, Market Intelligence Is Interpreted Context, Event Integrity (no ledger writes)

**Implementation Summary:** Created `src/infrastructure/market/PolygonProvider` satisfying the `MarketDataProvider` Protocol structurally. Added `polygon-api-client>=1.0` as a runtime dependency (installed as `polygon-api-client==1.16.3`). Added `[[tool.mypy.overrides]]` for polygon modules (`ignore_missing_imports=true`). Adapter uses `client.get_previous_close_agg(symbol)` for the latest daily OHLCV aggregate. Polygon timestamps are epoch milliseconds — converted to UTC datetime via `datetime.fromtimestamp(ms / 1000, tz=UTC)`. Polygon volume arrives as float — cast to `int(float(...))`. Provider version resolved via `importlib.metadata.version("polygon-api-client")`. API key accepted as constructor parameter (`api_key: str`) — infrastructure concern only. All SDK errors and empty-list responses wrapped in `ProviderUnavailableError`. Polygon SDK coupling is fully contained in this file — domain and services layers have no polygon imports. Tests use `unittest.mock.patch` — no real network calls.

**Acceptance Criteria:**

- Adapter satisfies `MarketDataProvider` Protocol (structural, no inheritance).
- Returns `MarketSnapshot` with full `ProviderProvenance` (fetched_at + data_as_of).
- All SDK errors map to `ProviderUnavailableError`.
- No event ledger writes anywhere in the adapter.
- Tests do not make real network calls.

**Out Of Scope:**

- Alpaca adapter (TF-0046).
- Caching or rate-limit handling.
- Intraday or multi-day history ranges.
- API key management beyond constructor parameter.

**Completed Verification:**

- `uv run pytest tests/test_polygon_adapter.py` — 23 passed (all mocked)
- `uv run pytest` — 297 passed
- `uv run ruff check .` — clean
- `uv run mypy src tests` — clean (78 files)

---

## TF-0046: Add Alpaca Market Data Adapter

**Status:** Done

**Milestone:** M9

**Branch:** `feature/tf-0046-alpaca-provider-adapter`

**Affected Layer:** infrastructure

**Linked ADRs:** ADR-0032

**Impacted Invariants:** Layer Separation, Market Intelligence Is Interpreted Context, Event Integrity (no ledger writes)

**Implementation Summary:** Created `src/infrastructure/market/AlpacaProvider` satisfying the `MarketDataProvider` Protocol structurally. Added `alpaca-py>=0.30` as a runtime dependency (installed as `alpaca-py==0.43.4`). Added `[[tool.mypy.overrides]]` for alpaca modules (`ignore_missing_imports=true`). Adapter uses `StockHistoricalDataClient.get_stock_bars(StockBarsRequest(...))` with `timeframe=TimeFrame.Day` and a 5-day lookback window; takes `bars[-1]` as most recent bar. Alpaca `Bar.timestamp` is already a `datetime` object — normalized to UTC via tzinfo check. Volume arrives as float — cast to `int(float(...))`. Provider version resolved via `importlib.metadata.version("alpaca-py")`. API key and secret key accepted as constructor parameters — infrastructure concerns only. All SDK errors, missing symbol keys, and empty bar lists wrapped in `ProviderUnavailableError`. Alpaca SDK coupling is fully contained in this file — domain and services layers have no alpaca imports. Tests use `unittest.mock.patch` — no real network calls.

**Acceptance Criteria:**

- Adapter satisfies `MarketDataProvider` Protocol (structural, no inheritance).
- Returns `MarketSnapshot` with full `ProviderProvenance` (fetched_at + data_as_of).
- All SDK errors map to `ProviderUnavailableError`.
- No event ledger writes anywhere in the adapter.
- Tests do not make real network calls.

**Out Of Scope:**

- Workspace overlays (TF-0047).
- Caching or rate-limit handling.
- Intraday or multi-day history ranges.
- Alpaca broker execution (separate SDK capability, not market data).

**Completed Verification:**

- `uv run pytest tests/test_alpaca_adapter.py` — 25 passed (all mocked)
- `uv run pytest` — 322 passed
- `uv run ruff check .` — clean
- `uv run mypy src tests` — clean (80 files)

---

## TF-0047: Implement Market Context Workspace Overlays

**Status:** Done

**Milestone:** M9

**Branch:** `feature/tf-0047-market-context-overlay`

**Affected Layer:** app, services (wiring), frontend

**Linked ADRs:** ADR-0032, ADR-0020, ADR-0021

**Impacted Invariants:** Layer Separation, Market Intelligence Is Interpreted Context, Derived State Must Remain Distinguishable, AI Advisory Boundary

**Implementation Summary:** Implemented `GET /workspaces/market-context` endpoint in the workspace router (registered before `/{route_id}` to prevent dynamic-segment capture). Endpoint accepts comma-separated `symbols` query param, delegates to `MarketSnapshotService.fetch_context()`, returns `MarketContextOverlayResponse` with OHLCV data, provider provenance, and completeness flags. `create_app()` now wires `MarketSnapshotService(YFinanceProvider())` as the default `market_snapshot_service`; other providers can be injected for production. Added `MarketSnapshotOverlay` + `MarketContextOverlay` TypeScript types and `fetchMarketContext` function to `frontend/src/api/runtime.ts`. Created `MarketContextPanel` React component with symbol text input, OHLCV display, and explicit ADVISORY boundary labels. Integrated panel into `OpportunityWorkspace` and `ActivePositionWorkspace`. Partial provider failures return 200 with `is_partial=True` — workspace overlay degrades gracefully. All market snapshots carry `ProviderProvenance` (fetched_at + data_as_of) for future replay-compatible persistence (TF-0052). Decimal prices serialized as strings for precision preservation through JSON.

**Acceptance Criteria:**

- Market context is surfaced in at least two workspaces.
- All market data is explicitly labeled as ADVISORY.
- Provider provenance (provider identity, data timestamp) is visible.
- Partial provider failures do not crash the overlay.
- Market context does not mutate lifecycle state.

**Out Of Scope:**

- Market regime interpretation (TF-0048).
- Contextual operational summaries (TF-0049).
- Provider provenance tracking registry (TF-0050).
- Symbol auto-extraction from lifecycle event payloads.
- Live chart rendering.

**Completed Verification:**

- `uv run pytest tests/test_market_context_overlay.py` — 18 passed
- `uv run pytest` — 340 passed
- `uv run ruff check .` — clean
- `uv run mypy src tests` — clean (81 files)
- `npm.cmd run typecheck` — clean
- `npm.cmd run lint` — clean
- `npm.cmd run build` — clean

---

## TF-0048: Implement Market Regime Interpretation Model

**Status:** Done

**Milestone:** M9

**Branch:** `feature/tf-0048-market-regime-interpreter`

**Affected Layer:** domain, services, app, frontend

**Linked ADRs:** ADR-0010, ADR-0032

**Impacted Invariants:** Deterministic Rule Evaluation, Market Intelligence Is Interpreted Context, Derived State Must Remain Distinguishable

**Implementation Summary:** Added `MarketRegimeInterpreter` Protocol to `src/domain/market/regime.py` following the `MarketDataProvider` port pattern. Implemented `SingleBarRegimeInterpreter` in `src/services/market/regime_interpreter.py` with deterministic OHLCV-based rules (priority order: HIGH_VOLATILITY → LOW_VOLATILITY → BULL → BEAR → RANGING → UNKNOWN). `MarketSnapshotService` gained an optional `regime_interpreter` parameter; when set, both `fetch_context` and `fetch_snapshot` annotate snapshots via `dataclasses.replace(snapshot, regime=...)`. Interpreter failures are caught by `_annotate()` — snapshot is returned unchanged rather than raised. `create_app()` now defaults to `MarketSnapshotService(YFinanceProvider(), SingleBarRegimeInterpreter())`. Frontend `MarketContextPanel.SnapshotRow` displays a color-coded regime badge when regime is not UNKNOWN. Existing tests are unaffected (interpreter defaults to None → UNKNOWN regime as before).

**Acceptance Criteria:**

- Regime classifications are deterministic and auditable.
- Single-bar rules classify OHLCV into one of five regimes or UNKNOWN.
- MarketSnapshotService annotates snapshots when an interpreter is provided.
- Existing tests unaffected when no interpreter provided.
- Regime visible in workspace overlay UI.
- Regime always labeled INFERRED/Advisory.

**Out Of Scope:**

- Multi-bar historical regime (requires historical data fetching).
- AI-based regime interpretation (M10).
- Regime persistence or storage.

**Completed Verification:**

- `uv run pytest tests/test_market_regime_interpreter.py` — 19 passed
- `uv run pytest` — 359 passed
- `uv run ruff check .` — clean
- `uv run mypy src tests` — clean (84 files)
- `npm.cmd run typecheck` — clean
- `npm.cmd run build` — clean

---

## TF-0049: Implement Contextual Operational Summaries

**Status:** Done

**Milestone:** M9

**Branch:** `feature/tf-0049-contextual-operational-summaries`

**Affected Layer:** services, app, frontend

**Linked ADRs:** ADR-0010, ADR-0013, ADR-0032

**Impacted Invariants:** Market Intelligence Is Interpreted Context, Derived State Must Remain Distinguishable, Workflow-Centric Architecture

**Implementation Summary:** Created `ContextualSummaryService` in `src/services/market/contextual_summary.py` composing `WorkspaceSummaryReadService` (TF-0023) with optional `MarketSnapshotService` (TF-0047/0048). Service produces `ContextualOperationalSummary` with an operational headline from event history and advisory market context notes with regime classification. Market fetch failures are caught silently in `_fetch_market_notes()` — market unavailability never loses the workspace summary. Added `GET /workspaces/contextual-summary` endpoint (registered before `/{route_id}` to prevent dynamic capture). Endpoint accepts workspace context params + optional comma-separated `symbols`. `create_app()` extracts `_market_svc` local variable for reuse across both `market_snapshot_service` and `ContextualSummaryService` — no double instantiation. Created `ContextualBriefingPanel` React component with symbol input, operational headline, per-symbol market notes with regime badges, and authority boundaries. Panel integrated into `OperatingWorkspace`. All market context labeled advisory; workspace summary labeled derived.

**Acceptance Criteria:**

- Workspace operational state and market context are combined in one summary.
- Market failures do not prevent workspace-only summary from rendering.
- All market context is explicitly advisory.
- Summary does not authorize lifecycle transitions.
- `GET /workspaces/contextual-summary` returns structured combined response.

**Out Of Scope:**

- Provider provenance tracking registry (TF-0050).
- Contextual summaries in all workspaces (only operating workspace for now).
- Symbol auto-extraction from lifecycle event payloads.

**Completed Verification:**

- `uv run pytest tests/test_contextual_summary.py` — 17 passed
- `uv run pytest` — 376 passed
- `uv run ruff check .` — clean
- `uv run mypy src tests` — clean (86 files)
- `npm.cmd run typecheck` — clean
- `npm.cmd run build` — clean

---

## TF-0050: Implement Provider Provenance Tracking

**Status:** Done

**Milestone:** M9

**Branch:** `feature/tf-0050-provider-provenance-tracking`

**Affected Layer:** domain, infrastructure, services, app

**Linked ADRs:** ADR-0032

**Impacted Invariants:** Layer Separation, Market Intelligence Is Interpreted Context, Derived State Must Remain Distinguishable, Event Integrity (no ledger writes), Replay

**Implementation Summary:** Implemented an advisory provider provenance registry as a separate port/store distinct from the event ledger. Added `ProviderFetchRecord` (immutable domain value object with `for_success`/`for_failure` factories), `ProvenanceStore` Protocol port, and `InMemoryProvenanceStore` infrastructure adapter (session-scoped; persistent storage is TF-0052). `MarketSnapshotService` gained an optional `provenance_store` parameter that auto-records each fetch outcome (success or failure) without changing existing behavior when unset. Added `ProvenanceQueryService` for read-only advisory queries with success/failure counts and provider/symbol summary. Added `GET /provenance/market-data` endpoint with optional since/until/provider_id/symbol filters. In `create_app()`, a single `InMemoryProvenanceStore` instance is shared between `MarketSnapshotService` (writes) and `ProvenanceQueryService` (reads). All provenance records carry `is_advisory=True` and must never be written to the event ledger.

**Acceptance Criteria:**

- `ProviderFetchRecord` captures both successful and failed fetch interactions.
- `InMemoryProvenanceStore` satisfies `ProvenanceStore` Protocol structurally.
- `MarketSnapshotService` records fetch outcomes when a provenance_store is injected.
- Failure records are first-class — capturing what was attempted but unavailable.
- `ProvenanceQueryService` returns advisory query results with summary statistics.
- `GET /provenance/market-data` returns provenance records with optional filters.
- All provenance artifacts are explicitly advisory and non-canonical.
- No provenance write to the event ledger.

**Out Of Scope:**

- Persistent provenance storage (TF-0052).
- Replay Workspace UI integration for provenance (TF-0052 territory).
- Symbol auto-extraction from lifecycle events.
- Pagination for large provenance logs.

**Completed Verification:**

- `uv run pytest tests/test_provider_provenance.py` — 39 passed
- `uv run pytest` — 415 passed
- `uv run ruff check .` — clean
- `uv run mypy src tests` — clean (90 files)

---

## TF-0051: Add Seeded Demo Market Context Flow

**Status:** Done

**Milestone:** M9

**Branch:** `feature/tf-0051-seeded-demo-flow`

**Affected Layer:** infrastructure, tests

**Linked ADRs:** ADR-0032

**Impacted Invariants:** Layer Separation, Market Intelligence Is Interpreted Context, Event Integrity (no ledger writes)

**Implementation Summary:** Implemented `SeededMarketDataProvider` satisfying the `MarketDataProvider` Protocol structurally — same normalized boundary as live providers per ADR-0032. The provider holds a static `_DEMO_SEED` dataset of 7 symbols (AAPL, TSLA, NVDA, SPY, QQQ, GLD, TLT) that together cover all five interpretable regime outcomes (BULL, HIGH_VOLATILITY, RANGING, BEAR, LOW_VOLATILITY). Raises `ProviderUnavailableError` for unknown symbols consistent with live adapters. Optional `fetched_at` injection supports deterministic test timestamps. `available_symbols` property exposes the seeded symbol set. The demo flow is enabled by injecting `SeededMarketDataProvider` into `MarketSnapshotService` via the existing `create_app(market_snapshot_service=...)` parameter — no application-layer or domain-layer changes required. The test suite exercises the complete M9 stack end-to-end: provider → regime interpreter → provenance tracking → workspace overlays → contextual summary → API endpoints.

**Acceptance Criteria:**

- SeededMarketDataProvider satisfies MarketDataProvider Protocol structurally.
- Seed data produces deterministic snapshots with full ProviderProvenance.
- All five interpretable regimes are covered by the seed dataset.
- Unknown symbols raise ProviderUnavailableError consistent with live providers.
- Complete M9 API demo flow passes with seeded data and no live API calls.
- Demo flow uses same normalized boundary as production providers (ADR-0032).

**Out Of Scope:**

- Replay-compatible market snapshot persistence (TF-0052).
- Frontend demo mode toggle.
- Seeding historical multi-day data.

**Completed Verification:**

- `uv run pytest tests/test_seeded_demo_flow.py` — 33 passed
- `uv run pytest` — 448 passed
- `uv run ruff check .` — clean
- `uv run mypy src tests` — clean (92 files)

---

## TF-0052: Add Replay-Compatible Market Snapshot Persistence Strategy

**Status:** Done

**Milestone:** M9

**Branch:** `feature/tf-0050-provider-provenance-tracking`

**Affected Layer:** domain, infrastructure, services, app

**Linked ADRs:** ADR-0032

**Impacted Invariants:** Layer Separation, Market Intelligence Is Interpreted Context, Derived State Must Remain Distinguishable, Event Integrity (separate from event ledger), Replay

**Implementation Summary:** Implemented the advisory market snapshot persistence architecture. `PersistedMarketSnapshot` (domain value object) wraps a `MarketSnapshot` with stable `snapshot_id` and `persisted_at`. `MarketSnapshotPersistenceStore` Protocol port defines the persistence contract. `InMemoryMarketSnapshotStore` provides session-scoped storage. `PostgresMarketSnapshotStore` provides durable Postgres storage via `market_advisory_snapshots` table (separate from `event_ledger`; Alembic migration `20260513_0003` with advisory/replay indices). `MarketSnapshotService` gained optional `snapshot_persistence_store` — on each successful fetch the snapshot is persisted silently (failures never break the fetch). `MarketSnapshotQueryService` provides read-only time/provider/symbol-filtered queries. Added `GET /market/snapshots` endpoint. In `create_app()`, a shared `InMemoryMarketSnapshotStore` is wired between the service (write) and query service (read). All persisted records carry `is_advisory=True`. Decimal prices stored as TEXT for precision preservation. The table comment and naming (`market_advisory_snapshots`) explicitly distinguish this from the canonical `event_ledger`.

**Acceptance Criteria:**

- `MarketSnapshotPersistenceStore` Protocol defines the persistence contract.
- `InMemoryMarketSnapshotStore` and `PostgresMarketSnapshotStore` satisfy Protocol structurally.
- Persistence failures never break market data fetches (silent failure tolerance).
- `market_advisory_snapshots` table is explicitly separate from `event_ledger`.
- Alembic migration creates table with replay-oriented indices (symbol+fetched_at, provider+fetched_at).
- `GET /market/snapshots` returns advisory persisted snapshots with optional filters.
- All persisted records are explicitly advisory — `is_advisory=True`.

**Out Of Scope:**

- Postgres live integration tests (require Docker Postgres connection).
- Snapshot expiry or rotation policy.
- Replay Workspace UI consumption of persisted snapshots.

**Completed Verification:**

- `uv run pytest tests/test_market_snapshot_persistence.py` — 45 passed
- `uv run pytest` — 493 passed
- `uv run ruff check .` — clean
- `uv run mypy src tests` — clean (97 files)

---

## TF-0053: Implement New Trade Idea Workflow

**Status:** Done

**Milestone:** M10

**Branch:** `feature/tf-0053-new-trade-idea-workflow`

**Affected Layer:** app, frontend

**Linked ADRs:** ADR-0002, ADR-0028

**Impacted Invariants:** Decision Lifecycle, Human Decision Sovereignty, Workflow-Centric Architecture

**Implementation Summary:** Added `POST /lifecycle/decisions/init` endpoint as a semantic initialization wrapper over the existing `LifecycleOrchestrationService`. The endpoint generates a UUID4 decision_id server-side, uppercases the symbol, constructs entity_references `[{decision, uuid}, {ticker, SYMBOL}]`, and calls the lifecycle service with `LifecycleStage.IDEA`. Returns `decision_id`, `symbol`, `event_type`, and `timestamp`. Added `NewTradeIdeaPayload` and `NewTradeIdeaResponse` Pydantic models. Frontend: created `NewTradeIdeaModal.tsx` with symbol input, optional thesis notes, loading state, and error display. Added `initNewTradeIdea()` to `api/runtime.ts`. Added `onNavigateProgrammatic` prop to `OperatingWorkspace` for post-creation routing. On success, navigates to OpportunityWorkspace with the new `decision_id`. Added "New Trade Idea" button (PlusCircle) to `OperatingWorkspace` header area. Added modal, form, and button CSS primitives to `styles.css`. `App.tsx` provides `handleNavigateProgrammatic`.

**Acceptance Criteria:**

- No curl/API call required to initiate workflow.
- New decisions initialize through operational UI flow.
- Lifecycle integrity remains event-backed.

**Out Of Scope:**

- Persistent active decision context across workspace transitions (TF-0054).
- Eliminating manual query param propagation (TF-0055).
- Multi-decision-per-session support.

**Completed Verification:**

- `uv run pytest tests/test_new_trade_idea_workflow.py` — 11 passed
- `uv run pytest` — 504 passed
- `uv run ruff check src tests` — clean
- `uv run mypy src tests` — clean (98 files)
- `npm.cmd run typecheck` — clean
- `npm.cmd run lint` — clean
- `npm.cmd run build` — clean

---

## TF-0054: Implement Persistent Active Decision Context

**Status:** Done

**Milestone:** M10

**Branch:** `feature/tf-0054-persistent-active-decision-context`

**Affected Layer:** app, frontend

**Linked ADRs:** ADR-0028, ADR-0022

**Impacted Invariants:** Workspace, Workflow-Centric Architecture, Derived State Must Remain Distinguishable

**Implementation Summary:** Fixed the root cause of the M9 demo failure and added localStorage-backed active decision persistence. Root cause: `_matches_context` in `projections.py` filters events by `decision_id` when it is non-null — the `LocalSessionProvider` and frontend `DEFAULT_WORKSPACE_CONTEXT` both used placeholder strings (`"decision.focus"`, `"workflow.current"`) that never matched any real event entity_references, silently emptying all workspace projections and attention queues. Fix: `LocalSessionProvider` now defaults `decision_id=None, selected_workflow_id=None`. Frontend `DEFAULT_WORKSPACE_CONTEXT` now uses empty strings for both. Added `frontend/src/activeDecision.ts` with localStorage persistence (`getActiveDecision`, `setActiveDecision`, `clearActiveDecision`). `App.tsx` now initializes from localStorage on mount, exposes `handleDecisionActivated`, and builds context with merge priority: URL params > (session + activeDecision) > static defaults. `NewTradeIdeaModal` writes the real decision record to localStorage and calls `onDecisionActivated` on successful creation. 9 new tests in `test_active_decision_context.py` — explicitly prove the M9 bug and verify the fix.

**Acceptance Criteria:**

- Active decision context survives navigation.
- Manual query parameter propagation is eliminated.
- Workspace continuity becomes operationally stable.

**Out Of Scope:**

- Clearing active decision when review completes (future M10 issue).
- Multi-decision session support.

**Completed Verification:**

- `uv run pytest tests/test_active_decision_context.py` — 9 passed
- `uv run pytest` — 513 passed
- `uv run ruff check src tests` — clean
- `uv run mypy src tests` — clean (99 files)
- `npm.cmd run typecheck` — clean
- `npm.cmd run lint` — clean
- `npm.cmd run build` — clean

---

## TF-0055: Eliminate Manual Workspace Context Propagation

**Status:** Done

**Milestone:** M10

**Branch:** `feature/tf-0055-eliminate-manual-context-propagation`

**Affected Layer:** frontend

**Linked ADRs:** ADR-0021

**Impacted Invariants:** Workspace, UX Is Architectural, Derived State Must Remain Distinguishable

**Implementation Summary:** Eliminated three remaining developer-centric artifacts: (1) `buildWorkspaceHref` now only encodes `decision_id` in navigation URLs — all other internal routing params (persona_id, persona_version, workspace_id, selected_workflow_id) are dropped from the URL since they are automatically resolved from session and localStorage. Navigation links are now clean paths like `/workspaces/opportunity` or `/workspaces/opportunity?decision_id=<uuid>`. (2) `ContextPanel` (raw internal ID display) replaced with `ActiveDecisionBadge` — shows the active symbol prominently with an "in workflow" tag and a clear button; shows a helpful hint when no decision is active. (3) `WorkspaceBriefing` (developer meta-commentary banner) and `ContextLink` ("Current routed context" URL artifact) removed from App.tsx. Added `handleClearDecision` which calls `clearActiveDecision()`, resets state, and navigates to Operating Workspace. No backend changes.

**Acceptance Criteria:**

- Workspaces automatically resolve active operational context.
- Manual URL parameter workflows are unnecessary.

**Out Of Scope:**

- Guided lifecycle navigation (TF-0056).
- Workspace transition continuity model (TF-0057).

**Completed Verification:**

- `uv run pytest` — 513 passed (no backend changes)
- `uv run ruff check src tests` — clean
- `uv run mypy src tests` — clean (99 files)
- `npm.cmd run typecheck` — clean
- `npm.cmd run lint` — clean
- `npm.cmd run build` — clean

---

## TF-0056: Implement Guided Lifecycle Navigation

**Status:** Done

**Milestone:** M10

**Branch:** `feature/tf-0056-guided-lifecycle-navigation`

**Affected Layer:** frontend

**Linked ADRs:** ADR-0021

**Impacted Invariants:** UX Is Architectural, Workflow-Centric Architecture

**Implementation Summary:** Created `frontend/src/workspaces/LifecycleProgress.tsx` with `LifecycleProgressStrip` (compact 7-step horizontal tracker showing done/current/future states with colored dots and connector lines) and `WorkflowGuidanceNote` (stage-specific meaning + guidance sentence in an accent-bordered info block). Both components handle null/unknown stages silently. Replaced the minimal `lifecycle-context` div in all five active workspaces (Operating, Opportunity, PlanReview, ActivePosition, Review) with these two components. Added corresponding CSS. No backend changes, no domain logic touched.

**Acceptance Criteria:**

- Users can understand operational progression without architectural knowledge.
- Workflow continuity becomes visually understandable.

**Out Of Scope:**

- Clickable stage navigation (stages are informational, not shortcuts).
- Guided demo mode infrastructure (TF-0058).

**Completed Verification:**

- `uv run pytest` — 513 passed (no backend changes)
- `npm.cmd run typecheck` — clean
- `npm.cmd run lint` — clean
- `npm.cmd run build` — clean

---

## TF-0057: Implement Operational Workflow Continuity Model

**Status:** Done

**Milestone:** M10

**Branch:** `feature/tf-0057-workflow-continuity-model`

**Affected Layer:** frontend

**Linked ADRs:** ADR-0021

**Impacted Invariants:** Workflow-Centric Architecture, UX Is Architectural

**Implementation Summary:** Implemented two continuity mechanisms. (1) Post-transition auto-navigation: after "Develop Thesis" (Idea→Thesis), the system routes to Plan Review; after "Record Execution" (Approval→Execution), routes to Active Position; after "Begin Position Review" (Position→Review), routes to Review Workspace. All other transitions reload the current workspace projection (they stay in the same workspace). Implemented via `makeTransitionHandler(stage, nextHref?)` pattern in PlanReviewWorkspace and ActivePositionWorkspace; direct `onNavigateProgrammatic` call in OpportunityWorkspace. (2) Live stage indicator in sidebar badge: all 5 workspaces call `onStageLoaded?(stage)` after projection loads; App.tsx holds `activeStage` state updated via `handleStageLoaded` (useCallback-memoized); `ActiveDecisionBadge` gains `activeStage?` prop, rendering a `.active-decision-stage` pill showing the current stage name in accent color.

**Acceptance Criteria:**

- Workspace movement preserves cognitive continuity.
- The system feels like one operational environment rather than disconnected screens.

**Out Of Scope:**

- Guided demo mode with scripted walkthroughs (TF-0058).
- Cross-workspace context memory beyond localStorage (TF-0062).

**Completed Verification:**

- `uv run pytest` — 513 passed (no backend changes)
- `uv run ruff check src tests` — clean
- `uv run mypy src tests` — clean (99 files)
- `npm.cmd run typecheck` — clean
- `npm.cmd run lint` — clean
- `npm.cmd run build` — clean

---

## TF-0058: Implement Guided Demo Mode

**Status:** Done

**Milestone:** M10

**Branch:** `feature/tf-0058-guided-demo-mode`

**Affected Layer:** frontend

**Linked ADRs:** ADR-0021

**Impacted Invariants:** Workflow-Centric Architecture, UX Is Architectural, Human Decision Sovereignty (demo does not bypass lifecycle rules — it uses the same lifecycle API surface)

**Implementation Summary:** Created `frontend/src/demo.ts` with `DEMO_SEED` (AAPL breakout scenario with realistic thesis and plan text) and `runDemoFlow` (fires 3 API calls: init → Thesis transition → Plan transition, calls `setActiveDecision` with `is_demo: true`, returns the record). Added `is_demo?: boolean` to `ActiveDecisionRecord`. In `OperatingWorkspace`, added a `DemoInvitePanel` shown when the attention queue is empty and there is no active lifecycle stage — it describes the AAPL demo scenario and offers a "Start Demo" button with loading/error states. On success, activates the seeded decision and navigates to Plan Review Workspace. The sidebar `ActiveDecisionBadge` shows a warm-amber "Demo" pill when `is_demo` is true. All demo transitions use the same lifecycle API surface as normal workflow — demo mode does not bypass any lifecycle rules.

**Acceptance Criteria:**

- A user can experience TradeForge without manual setup.
- Demo flow remains replayable and deterministic.

**Out Of Scope:**

- Multiple named demo scenarios (TF-0059).
- One-click full walkthrough with automated stage advancement (TF-0060).
- Demo scenario persistence across server restarts (event store is in-memory).

**Completed Verification:**

- `uv run pytest` — 513 passed (no backend changes)
- `uv run ruff check src tests` — clean
- `uv run mypy src tests` — clean (99 files)
- `npm.cmd run typecheck` — clean
- `npm.cmd run lint` — clean
- `npm.cmd run build` — clean

---

## TF-0059: Implement Seeded Replayable Demo Scenarios

**Status:** Done

**Milestone:** M10

**Branch:** `feature/tf-0059-seeded-replayable-demo-scenarios`

**Affected Layer:** frontend

**Linked ADRs:** ADR-0021

**Impacted Invariants:** Workflow-Centric Architecture, UX Is Architectural, Human Decision Sovereignty (demo uses same lifecycle API surface)

**Implementation Summary:** Replaced the single AAPL "Start Demo" button (TF-0058) with a 4-scenario selection grid. Each named scenario is a `DemoScenario` value object in `frontend/src/demo.ts` specifying symbol, lifecycle target depth, landing workspace, and stage-specific payloads. `runDemoFlow` was updated to accept a scenario parameter and seed the lifecycle through Plan, Approval, Position, or Review as required. Scenarios: (1) AAPL Breakout Swing Trade → Plan stage → Plan Review workspace; (2) TSLA Completed Lifecycle Review → Review stage → Replay workspace (7-event timeline); (3) NVDA Active Position Management → Position stage → Active Position workspace; (4) SPY Disciplined Exit Review → Review stage → Review workspace. Added `scenario_name?: string` to `ActiveDecisionRecord`. Added scenario card grid CSS with stage-specific badge colors. All demo transitions use the same lifecycle API surface as normal workflow — no lifecycle bypass.

**Acceptance Criteria:**

- Replay workspaces contain meaningful operational examples.
- Demo scenarios illustrate workflow philosophy.

**Out Of Scope:**

- One-click full walkthrough with automated stage advancement (TF-0060).
- Demo scenario persistence across server restarts (event store is in-memory).

**Completed Verification:**

- `uv run pytest` — 513 passed (no backend changes)
- `npm.cmd run typecheck` — clean
- `npm.cmd run lint` — clean
- `npm.cmd run build` — clean

---

## TF-0060: Implement One-Click Operational Walkthrough

**Status:** Done

**Milestone:** M10

**Branch:** `feature/tf-0060-one-click-operational-walkthrough`

**Affected Layer:** frontend

**Linked ADRs:** ADR-0021

**Impacted Invariants:** Workflow-Centric Architecture, UX Is Architectural, Human Decision Sovereignty (walkthrough uses same lifecycle API surface)

**Implementation Summary:** Implemented a 7-step guided walkthrough that progresses through all lifecycle stages with contextual explanation at each workspace. New `frontend/src/walkthrough.ts` defines `WalkthroughStepDef` (7 steps), `WalkthroughSession` (localStorage-persisted), `initWalkthrough()` (creates Idea-stage AAPL decision), `advanceWalkthroughStep()` (fires sequential lifecycle transitions). New `WalkthroughPanel.tsx` is a persistent `<aside>` rendered from App.tsx as the first child of the workspace main area — no individual workspace components need modification. App.tsx adds `walkthroughSession` state, `handleStartWalkthrough`, `handleWalkthroughAdvance`, `handleExitWalkthrough`. OperatingWorkspace gains `onStartWalkthrough` prop and shows "Start Guided Walkthrough →" below the demo scenario grid. Step 3 fires two transitions (Execution + Position) in one click. Last step (Replay) exits the walkthrough instead of advancing. Session persists across page refreshes. `handleClearDecision` also clears walkthrough session.

**Acceptance Criteria:**

- A complete operational walkthrough launches from a single entry point.

**Out Of Scope:**

- Guided walkthrough resume from mid-step (starts from step 0).
- Multiple walkthrough themes.

**Completed Verification:**

- `uv run pytest` — 513 passed (no backend changes)
- `npm.cmd run typecheck` — clean
- `npm.cmd run lint` — clean
- `npm.cmd run build` — clean (263.03 kB JS, 26.83 kB CSS)

---

## TF-0061: Implement Operational Onboarding Flow

**Status:** Done

**Milestone:** M10

**Branch:** `feature/tf-0061-operational-onboarding-flow`

**Affected Layer:** frontend

**Linked ADRs:** ADR-0021

**Impacted Invariants:** UX Is Architectural, Human Decision Sovereignty (philosophy communicated before operation)

**Implementation Summary:** Implemented a 5-screen philosophical onboarding modal shown on first visit via `localStorage["tradeforge.onboarding_complete"]` flag. No API calls, no lifecycle events — purely informational. Screens cover: human decision sovereignty (Compass), canonical lifecycle (GitBranch), workspaces as cognitive environments (Layout), review as first-class workflow (BookOpen), replayability (History). Navigation: Previous/Next + "Get Started →" on last screen, "Skip" top-right. New `onboarding.ts` provides localStorage helpers. `OnboardingModal.tsx` renders from App.tsx before AppShell in a React fragment — `position: fixed; inset: 0` overlay with `z-index: 1000`. App.tsx adds `onboardingDone` state and `handleOnboardingComplete()`.

**Acceptance Criteria:**

- New users understand the system philosophically before operationally.

**Out Of Scope:**

- Onboarding reset mechanism.
- Persona-specific onboarding variants.

**Completed Verification:**

- `uv run pytest` — 513 passed (no backend changes)
- `npm.cmd run typecheck` — clean
- `npm.cmd run lint` — clean
- `npm.cmd run build` — clean (266.45 kB JS, 29.13 kB CSS)

---

## TF-0062: Implement Cross-Workspace Context Persistence

**Status:** Done

**Milestone:** M10

**Branch:** `feature/tf-0062-cross-workspace-context-persistence`

**Affected Layer:** frontend

**Linked ADRs:** ADR-0021

**Impacted Invariants:** Workspace, Workflow-Centric Architecture, Derived State Must Remain Distinguishable

**Implementation Summary:** Added `frontend/src/operationalContext.ts` — a localStorage-backed store (`tradeforge.operational_context`) holding `watched_symbols: string[]` and `last_known_stage: string | null`. `MarketContextPanel` and `ContextualBriefingPanel` now pre-fill their symbol inputs with `getWatchedSymbolsString()` on mount and call `addWatchedSymbols()` after each successful fetch. App.tsx syncs the active decision symbol via `useEffect` on `activeDecision?.symbol`, initializes `activeStage` from persisted `last_known_stage` (eliminating the null-flash on navigation), and calls `syncLastKnownStage()` in `handleStageLoaded`. `clearOperationalContext()` is called in `handleClearDecision()`. No prop drilling — panels and App.tsx communicate through the store directly.

**Acceptance Criteria:**

- Workspace transitions preserve operational meaning.

**Out Of Scope:**

- Symbol removal/management UI.
- Server-side operational context persistence.

**Completed Verification:**

- `uv run pytest` — 513 passed (no backend changes)
- `npm.cmd run typecheck` — clean
- `npm.cmd run lint` — clean
- `npm.cmd run build` — clean (267.63 kB JS)

---

## TF-0063: Stabilize Workspace Transition Ergonomics

**Status:** Done

**Milestone:** M10

**Branch:** `feature/tf-0063-workspace-transition-ergonomics`

**Affected Layer:** frontend

**Linked ADRs:** ADR-0021

**Impacted Invariants:** UX Is Architectural, Workflow-Centric Architecture

**Implementation Summary:** Added a stage-aware recommended workspace indicator to the sidebar nav. New `STAGE_TO_WORKSPACE` map in `workspaceRouting.ts` defines the canonical stage→workspace relationship (Idea→opportunity, Thesis/Plan/Approval→plan-review, Execution/Position→active-position, Review→review). `getRecommendedWorkspace(stage)` returns the mapped id. `WorkspaceNavigation` gains optional `recommendedRouteId` prop — the matching link (when not the active page) receives CSS class `"recommended"` (accent border + surface) and a right-justified `"→"` indicator span with accessible aria-label. App.tsx derives `recommendedRouteId` from `activeStage` via `useMemo`. Because `activeStage` is now initialized from persisted `last_known_stage` (TF-0062), the recommendation is correct immediately after page refresh.

**Acceptance Criteria:**

- Workspace transitions feel operationally deliberate rather than technical.

**Out Of Scope:**

- Disabling or hiding non-recommended workspaces.
- Stage-specific nav tooltips.

**Completed Verification:**

- `uv run pytest` — 513 passed (no backend changes)
- `npm.cmd run typecheck` — clean
- `npm.cmd run lint` — clean
- `npm.cmd run build` — clean (268.18 kB JS, 29.35 kB CSS)

---

## TF-0064: Implement Operational Attention Continuity

**Status:** Done

**Milestone:** M10

**Branch:** `feature/tf-0064-operational-attention-continuity`

**Affected Layer:** frontend

**Linked ADRs:** ADR-0021

**Impacted Invariants:** Workflow-Centric Architecture, UX Is Architectural, Human Decision Sovereignty

**Implementation Summary:** Added `AttentionSummaryPanel` to the sidebar between `ActiveDecisionBadge` and `SessionPanel`, making the attention queue state visible on every workspace. The panel fetches `GET /workspaces/operating/attention` independently; it renders nothing when no decision is active and fails silently on API errors. Two states: items pending (count + urgency badge + top item explanation + "View full queue →" link) and queue clear ("Queue clear ✓" indicator). The explicit "clear" state is important — it tells the user nothing is pending rather than leaving them to wonder if state was lost. App.tsx passes inline-constructed `WorkspaceApiParams` from `context` and a `handleNavigateProgrammatic("/workspaces/operating")` callback. No new API endpoints; reuses `GET /workspaces/operating/attention`.

**Acceptance Criteria:**

- Important operational context is not lost during workflow progression.

**Out Of Scope:**

- Auto-polling for real-time attention queue updates.
- Per-workspace attention filtering.

**Completed Verification:**

- `uv run pytest` — 513 passed (no backend changes)
- `npm.cmd run typecheck` — clean
- `npm.cmd run lint` — clean
- `npm.cmd run build` — clean (269.92 kB JS, 30.79 kB CSS)

---

## M10AIS01: Implement Structured Thesis Domain Model

**Status:** Done

**Milestone:** M10A

**Branch:** `feature/tf-0064-operational-attention-continuity`

**Affected Layer:** domain, api, services

**Linked ADRs:** ADR-0033, ADR-0034

**Impacted Invariants:** Event Ledger Canonical Truth, Events Are Immutable, Replayability Is Foundational, Lifecycle Authority

**Implementation Summary:** Introduced `src/domain/cognition/thesis.py` with `ThesisArtifact` — a frozen dataclass with `create()` factory (validates narrative, catalysts, assumptions, invalidation_conditions, confidence_level) and `to_payload()`/`from_payload()` for event serialization. Added `POST /lifecycle/decisions/develop-thesis` endpoint that validates structured thesis fields and creates `decision.thesis_created` event with structured payload embedded. Added `GET /lifecycle/decisions/{decision_id}/thesis` endpoint that reads the event store and extracts thesis content from the event payload. Exposed `app.state.event_store` for direct event query access. Updated plan-review `WorkspaceStateContract` with `thesis_content` field sourced from `decision.thesis_created`.

**Acceptance Criteria:**

- Thesis artifacts persist independently from lifecycle markers.
- Thesis becomes replayable cognition rather than stage metadata.

**Out Of Scope:**

- Thesis revision history (M10AIS03).
- Plan artifact model (M10AIS06).

**Completed Verification:**

- `uv run pytest` — 534 passed (21 new tests: 13 unit + 8 integration)
- `npm.cmd run typecheck` — clean
- `npm.cmd run lint` — clean
- `npm.cmd run build` — clean (276.72 kB JS, 30.79 kB CSS)

---

## M10AIS02: Implement Thesis Authoring Workspace

**Status:** Done

**Milestone:** M10A

**Branch:** `feature/tf-0064-operational-attention-continuity`

**Affected Layer:** frontend

**Linked ADRs:** ADR-0034

**Impacted Invariants:** UX Is Architectural, Human Decision Sovereignty, Workflow-Centric Architecture

**Implementation Summary:** Created `ThesisDevelopmentModal.tsx` — a modal form capturing narrative (textarea), catalysts/assumptions/invalidation_conditions (dynamic list inputs), confidence_level (range slider 1-5), and regime_alignment (optional text). Client-side validation before submission. Submits to `POST /lifecycle/decisions/develop-thesis` via new `postDevelopThesis()` API function. On success navigates to `/workspaces/plan-review`. Updated `OpportunityWorkspace.tsx` to open the modal instead of firing an immediate empty lifecycle transition; `TransitionState` now uses `"open-thesis-modal"` instead of `"transitioning"`. Added `ThesisContextPanel` component in `PlanReviewWorkspace.tsx` that fetches and displays thesis content (narrative, regime, conviction, catalysts, invalidation conditions) when the decision has a structured thesis. Added `fetchThesisArtifact()` and `ThesisArtifact` type to `frontend/src/api/runtime.ts`.

**Acceptance Criteria:**

- Traders can compose durable structured thesis artifacts.
- Thesis authoring becomes operationally usable.

**Out Of Scope:**

- Thesis revision after initial creation.
- Scenario branch visualization.

**Completed Verification:**

- `uv run pytest` — 534 passed (no new tests beyond M10AIS01)
- `npm.cmd run typecheck` — clean
- `npm.cmd run lint` — clean
- `npm.cmd run build` — clean (276.72 kB JS, 30.79 kB CSS)

---

## M10AIS03: Implement Thesis Revision History

**Status:** Done

**Milestone:** M10A

**Branch:** `feature/tf-0064-operational-attention-continuity`

**Affected Layer:** domain, api, frontend

**Linked ADRs:** ADR-0033, ADR-0035

**Impacted Invariants:** Events Are Immutable, Replayability Is Foundational, Lifecycle Authority

**Implementation Summary:** Added `decision.thesis_revised` event type — not a lifecycle stage transition; appended directly to event_store. Added `POST /lifecycle/decisions/revise-thesis` endpoint (validates thesis fields, checks stage is Thesis, sets revision_number, appends revision event). Updated `GET /lifecycle/decisions/{id}/thesis` to scan both thesis_created and thesis_revised event types returning the most recent. Added `GET /lifecycle/decisions/{id}/thesis/history` returning all thesis snapshots chronologically (ThesisHistoryResponse with total_revisions + ordered snapshots including revision_number). Added top-level imports for LIFECYCLE_EVENT_STAGE_MAP and EventEnvelope. Created `ThesisRevisionModal.tsx` (pre-populated with current thesis values, same form structure as ThesisDevelopmentModal). Updated `ThesisContextPanel` with `canRevise`/`onRevise` props (shows "Revise Thesis" button at Thesis stage, shows "— Revised" badge for revised events). Updated `PlanReviewWorkspace.tsx` with showRevisionModal state and ThesisRevisionModal integration.

**Acceptance Criteria:**

- Replay can reconstruct thesis evolution chronologically.

**Out Of Scope:**

- Thesis revision after Plan stage is entered.
- Diffing between revisions.

**Completed Verification:**

- `uv run pytest` — 541 passed (7 new tests)
- `npm.cmd run typecheck` — clean
- `npm.cmd run lint` — clean
- `npm.cmd run build` — clean (282.66 kB JS, 30.79 kB CSS)

---

## M10AIS06: Implement Structured Trade Plan Domain Model

**Status:** Done

**Milestone:** M10A

**Branch:** `feature/tf-0064-operational-attention-continuity`

**Affected Layer:** domain, api

**Linked ADRs:** ADR-0033, ADR-0034

**Impacted Invariants:** Event Ledger Canonical Truth, Events Are Immutable, Replayability Is Foundational, Lifecycle Authority

**Implementation Summary:** Introduced `src/domain/cognition/plan.py` with `TradePlanArtifact` — frozen dataclass with `create()` factory validating entry_rationale, stop_rationale, target_rationale, sizing_rationale (all required, min 10 chars), execution_assumptions (list, min 1), and optional playbook_alignment. `to_payload()`/`from_payload()` for event serialization with graceful legacy degradation. Added `POST /lifecycle/decisions/create-plan` endpoint that validates plan fields and creates `decision.plan_created` lifecycle transition (Thesis→Plan) via LifecycleOrchestrationService with structured payload `{plan: {...}}`. Added `GET /lifecycle/decisions/{id}/plan` endpoint that reads decision.plan_created event payload and returns TradePlanArtifactResponse. Added `symbol` field to ThesisArtifactResponse and TradePlanArtifactResponse (populated from event payload). Updated cognition module `__init__.py` to export TradePlanArtifact. 22 new tests (563 total).

**Acceptance Criteria:**

- Trade plans become durable cognitive artifacts.

**Completed Verification:**

- `uv run pytest` — 563 passed (22 new tests: 12 unit + 10 integration)
- `npm.cmd run typecheck` — clean
- `npm.cmd run lint` — clean
- `npm.cmd run build` — clean (290.12 kB JS, 30.79 kB CSS)

---

## M10AIS07: Implement Trade Plan Authoring Workspace

**Status:** Done

**Milestone:** M10A

**Branch:** `feature/tf-0064-operational-attention-continuity`

**Affected Layer:** frontend

**Linked ADRs:** ADR-0034

**Impacted Invariants:** UX Is Architectural, Human Decision Sovereignty, Workflow-Centric Architecture

**Implementation Summary:** Created `PlanDevelopmentModal.tsx` — modal form with `RationaleField` components for entry/stop/target/sizing rationale (textarea, required) and a dynamic list for execution_assumptions. Playbook alignment input (optional). Client-side validation before submission. Submits to `POST /lifecycle/decisions/create-plan`. On success: reloads projection (stays in plan-review at Plan stage) and re-fetches plan artifact. Added `CreatePlanRequest`, `CreatePlanResponse`, `TradePlanArtifact` types and `postCreatePlan()`, `fetchPlanArtifact()` API functions to `runtime.ts`. Updated `PlanReviewWorkspace.tsx`: `handleCreatePlan` opens `PlanDevelopmentModal` instead of empty transition, added `plan` state and `showPlanModal` state, added `PlanContextPanel` showing plan content (entry/stop/target/sizing rationale, execution assumptions, playbook) below thesis panel when plan exists, fetch plan artifact in loadProjection alongside thesis.

**Acceptance Criteria:**

- Plans become operationally authorable.

**Completed Verification:**

- `uv run pytest` — 563 passed (no additional backend tests)
- `npm.cmd run typecheck` — clean
- `npm.cmd run lint` — clean
- `npm.cmd run build` — clean (290.12 kB JS, 30.79 kB CSS)

---

## M10AIS08: Implement Plan Validation Preview Layer

**Status:** Done

**Milestone:** M10A

**Branch:** `feature/tf-0064-operational-attention-continuity`

**Affected Layer:** api, frontend

**Linked ADRs:** ADR-0033, ADR-0004

**Impacted Invariants:** UX Is Architectural, Derived State Must Remain Distinguishable, Human Decision Sovereignty

**Implementation Summary:** Added `GET /lifecycle/decisions/{decision_id}/plan-readiness` endpoint returning `PlanReadinessResponse` with: `current_stage`, `next_allowed_transition`, `has_structured_thesis`, `has_structured_plan`, `can_proceed_to_approval`, and a `checks` list of `ReadinessCheckResponse`. Hard-gate checks (advisory=False): has_structured_thesis, has_structured_plan. Advisory checks: conviction_level (warn < 3), invalidation_conditions (warn < 2), execution_assumptions (warn < 2), playbook_alignment (warn when absent). `can_proceed_to_approval` is True only when stage = Plan AND all hard gates pass. Added ALLOWED_LIFECYCLE_TRANSITIONS to top-level imports. Created `PlanReadinessPanel.tsx` with `CheckRow` subcomponent rendering pass/advisory/fail icons, summary status line, and authority boundary note. Added `PlanReadiness`, `ReadinessCheck` types and `fetchPlanReadiness()` to runtime.ts. Updated `PlanReviewWorkspace.tsx`: `readiness` state, fetch in `loadProjection`, render `PlanReadinessPanel` above "Authorize Plan" button in a React fragment. 12 new backend tests (575 total).

**Acceptance Criteria:**

- Operators receive cognition-aware planning guidance.

**Out Of Scope:**

- NLP-based consistency checking between thesis and plan rationale.
- Blocking the Authorize button based on advisory failures.
- Persistent rule engine (M12 scope).

**Completed Verification:**

- `uv run pytest` — 575 passed (12 new tests)
- `npm.cmd run typecheck` — clean
- `npm.cmd run lint` — clean
- `npm.cmd run build` — clean (292.47 kB JS, 30.79 kB CSS)

---

## M10AIS09: Implement Replay Cognitive Artifact Timeline

**Status:** Done

**Milestone:** M10A

**Branch:** `feature/tf-0064-operational-attention-continuity`

**Affected Layer:** frontend

**Linked ADRs:** ADR-0035

**Impacted Invariants:** Replayability Is Foundational, Derived State Must Remain Distinguishable

**Implementation Summary:** Extended `ReplayWorkspace.tsx` with cognitive artifact rendering — no backend changes (ADR-0035 confirmed timeline already carries full payloads). Added `extractThesisPayload()` and `extractPlanPayload()` type-guarded helpers that safely read structured artifact data from event payload dicts, returning null for legacy empty-payload events. Added `ThesisPayloadPreview` inline component — shows narrative (truncated to 160 chars), conviction badge, catalyst/invalidation/assumption counts, and regime alignment for `decision.thesis_created` and `decision.thesis_revised` entries. Added `PlanPayloadPreview` inline component — shows entry rationale (truncated), playbook badge, and execution assumption count for `decision.plan_created` entries. Added `CognitiveSnapshotSummary` panel rendered above the timeline `<ol>` — derives latest thesis and plan state by scanning all entries, shows narrative excerpt, conviction, regime, and plan entry excerpt with "N versions" indicator when thesis was revised. All artifact content labeled "Derived from event payloads" to distinguish from canonical truth. Graceful degradation: entries without structured payload show no artifact section.

**Acceptance Criteria:**

- Replay reconstructs reasoning, not merely events.

**Out Of Scope:**

- Point-in-time cognitive snapshot at a user-selected timestamp (M10AIS10).
- Diff/comparison between thesis versions (M10AIS03 follow-on).

**Completed Verification:**

- `uv run pytest` — 575 passed (no backend changes)
- `npm.cmd run typecheck` — clean
- `npm.cmd run lint` — clean
- `npm.cmd run build` — clean (298.13 kB JS, 30.79 kB CSS)

---

## M10AIS11: Implement Structured Review Reflection Model

**Status:** Done

**Milestone:** M10A

**Branch:** `feature/tf-0064-operational-attention-continuity`

**Affected Layer:** domain, api

**Linked ADRs:** ADR-0033, ADR-0002

**Impacted Invariants:** Event Ledger Canonical Truth, Replayability Is Foundational, Reflection And Review Are First-Class

**Implementation Summary:** Created `src/domain/cognition/review.py` with `ReviewReflectionArtifact` — frozen dataclass with `create()` validating: `thesis_vs_outcome` (required), `decision_quality` (1-5), `execution_quality` (1-5), `discipline_observations` (required), `lessons_learned` (list, min 1), `behavioral_observations` (optional). `to_payload()`/`from_payload()` for event serialization with graceful legacy degradation. Added `POST /lifecycle/decisions/complete-review` endpoint that validates reflection fields and creates the `review.review_completed` lifecycle transition (Position→Review) via `LifecycleOrchestrationService` with structured payload `{review: {...}}`. Added `GET /lifecycle/decisions/{id}/review` that reads `review.review_completed` event payload and returns `ReviewReflectionArtifactResponse`. Updated `cognition/__init__.py` to export `ReviewReflectionArtifact`. 23 new tests (598 total).

**Acceptance Criteria:**

- Reviews become durable learning artifacts.

**Completed Verification:**

- `uv run pytest` — 598 passed (23 new tests: 13 unit + 10 integration)
- `npm.cmd run typecheck` — clean
- `npm.cmd run build` — clean (307.69 kB JS, 30.79 kB CSS)

---

## M10AIS12: Implement Review Reflection Workspace

**Status:** Done

**Milestone:** M10A

**Branch:** `feature/tf-0064-operational-attention-continuity`

**Affected Layer:** frontend

**Linked ADRs:** ADR-0034

**Impacted Invariants:** UX Is Architectural, Reflection And Review Are First-Class, Human Decision Sovereignty

**Implementation Summary:** Created `ReviewReflectionModal.tsx` — form with `thesis_vs_outcome` textarea, `QualitySlider` subcomponent for `decision_quality` and `execution_quality` (1-5, Poor–Excellent labels), `discipline_observations` textarea, `lessons_learned` dynamic list, and optional `behavioral_observations` textarea. Submits to `POST /lifecycle/decisions/complete-review`. On success: reloads projection (stays in review workspace). Rewrote `ReviewWorkspace.tsx` entirely: imports `fetchThesisArtifact`, `fetchPlanArtifact`, `fetchReviewReflection` and respective types; fetches all three alongside workspace projection on load; added `ReviewFoundationPanel` showing original thesis narrative and plan entry rationale for cognitive comparison context before writing reflection; added `ReviewReflectionPanel` displaying completed review content (thesis vs outcome, quality scores, discipline observations, lessons, behavioral observations); `handleCompleteReview` button opens `ReviewReflectionModal` via `showReviewModal` state; "Review Recorded" complete surface shown at Review stage. Added `CompleteReviewRequest`, `CompleteReviewResponse`, `ReviewReflectionArtifact` types and `postCompleteReview()`, `fetchReviewReflection()` to `runtime.ts`.

**Acceptance Criteria:**

- Review becomes operationally meaningful.

**Completed Verification:**

- `uv run pytest` — 598 passed (no additional backend tests)
- `npm.cmd run typecheck` — clean
- `npm.cmd run build` — clean (307.69 kB JS, 30.79 kB CSS)

---

## M10AIS04: Implement Scenario Branch Modeling

**Status:** Done

**Milestone:** M10A

**Branch:** `feature/tf-0064-operational-attention-continuity`

**Affected Layer:** domain, api

**Linked ADRs:** ADR-0033

**Impacted Invariants:** Events Are Immutable, Replayability Is Foundational

**Implementation Summary:** Created `src/domain/cognition/scenario.py` with `ScenarioBranchArtifact` (frozen dataclass) and `ScenarioBranchType` StrEnum (`primary`, `alternative`, `invalidation`, `regime_transition`). `create()` validates branch_type (enum check), condition (required), implication (required), and confidence (1-5). `to_payload()`/`from_payload()` for event serialization. Added `POST /lifecycle/decisions/create-scenario-branch` endpoint — validates fields, checks decision exists and is not in Review stage, appends `decision.scenario_branch_created` event directly to event store (not a lifecycle transition). Added `GET /lifecycle/decisions/{decision_id}/scenario-branches` returning all branches chronologically. Extended `ReplayTimelineBuilder._kind_for_event()` to include `COGNITION = "cognition"` kind for non-lifecycle `EventDomain.DECISION` events — ensures `decision.scenario_branch_created` and `decision.thesis_revised` appear in replay timeline. 23 new tests (621 total).

**Completed Verification:**

- `uv run pytest` — 621 passed (23 new: 13 unit + 10 integration)
- `npm.cmd run typecheck` — clean
- `npm.cmd run build` — clean (317.91 kB JS, 30.79 kB CSS)

---

## M10AIS05: Implement Scenario Visualization Projection

**Status:** Done

**Milestone:** M10A

**Branch:** `feature/tf-0064-operational-attention-continuity`

**Affected Layer:** frontend

**Linked ADRs:** ADR-0035

**Impacted Invariants:** Replayability Is Foundational, UX Is Architectural

**Implementation Summary:** Extended `ReplayWorkspace.tsx` with scenario branch rendering. Added `extractScenarioBranchPayload()` type guard, `ScenarioBranchPreview` component (branch type badge, likelihood badge, condition/implication excerpts), `BRANCH_TYPE_LABELS` and `COGNITION` kind label. Updated `TimelineEntryRow` to render `ScenarioBranchPreview` for `decision.scenario_branch_created` entries. Updated `CognitiveSnapshotSummary` to count scenario branches and show "N scenario branches defined". Created `ScenarioBranchPanel.tsx` with `BranchCard` subcomponent, ordered by type (primary → alternative → invalidation → regime_transition), "Add Scenario" button opening `ScenarioBranchModal`. Created `ScenarioBranchModal.tsx` with branch_type select, condition/implication textareas, likelihood slider, optional notes. Updated `OpportunityWorkspace.tsx` to fetch branches on load, show `ScenarioBranchPanel` below field surfaces, re-fetch after branch added. Added `ScenarioBranchType`, `ScenarioBranch`, `ScenarioBranchList`, `postCreateScenarioBranch()`, `fetchScenarioBranches()` to `runtime.ts`.

**Completed Verification:**

- `uv run pytest` — 621 passed (no new backend tests)
- `npm.cmd run typecheck` — clean
- `npm.cmd run build` — clean (317.91 kB JS, 30.79 kB CSS)

---

## M10AIS10: Implement Cognitive Snapshot Reconstruction

**Status:** Done

**Milestone:** M10A

**Branch:** `feature/tf-0064-operational-attention-continuity`

**Affected Layer:** api, frontend

**Linked ADRs:** ADR-0035

**Impacted Invariants:** Replayability Is Foundational, Derived State Must Remain Distinguishable

**Implementation Summary:** Added `GET /lifecycle/decisions/{decision_id}/cognitive-snapshot?at=<ISO-timestamp>` endpoint. The `at` parameter is optional — when omitted, returns current full state; when provided, reconstructs cognitive state strictly before that timestamp (`ts >= at` boundary excludes events at or after the snapshot moment, applied only when `at` is explicitly provided to avoid Windows clock resolution issues). Scans decision events, tracking latest lifecycle stage, latest thesis (thesis_created or thesis_revised), latest plan (plan_created), and all scenario branches visible before T. Returns `CognitiveSnapshotResponse` with decision_id, snapshot_at, event_count_at_snapshot, current_stage, thesis, plan, scenario_branches (compact nested models, not reusing the full artifact responses), and authority="derived". 8 new tests (629 total) with deterministic time boundaries using event_timestamp from previous API responses + 1 microsecond delta (not raw datetime.now() captures). Created `CognitiveSnapshotPanel.tsx` with nested `BranchSummary` subcomponent, showing lifecycle stage tag, thesis narrative excerpt with conviction badge and counts, plan entry/stop rationale excerpts, scenario branch type badges and first 2 branches. Added fetchCognitiveSnapshot() and CognitiveSnapshot type family to runtime.ts. Updated `ReplayWorkspace.tsx`: added `cognitiveSnapshot` and `selectedEntryTimestamp` states; fetchCognitiveSnapshot on load; `handleEntryClick` callback fetches snapshot at clicked entry's timestamp; `handleClearSelection` returns to current state; `TimelineEntryRow` gains `isSelected`/`onClick` props and clickable styling; `CognitiveSnapshotPanel` replaces `CognitiveSnapshotSummary` when a decision is active; hint text "Click a timeline entry to reconstruct cognitive state at that moment."

**Acceptance Criteria:**

- Historical reasoning becomes reconstructable.

**Completed Verification:**

- `uv run pytest` — 629 passed (8 new tests)
- `npm.cmd run typecheck` — clean
- `npm.cmd run build` — clean (323.38 kB JS, 30.79 kB CSS)

---


