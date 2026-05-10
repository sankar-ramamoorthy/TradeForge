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

Roadmap v2 is the active milestone direction. This register is intentionally scoped through M8 for the fast MVP v1 path. Post-MVP Roadmap v2 candidates remain deferred until an explicit checkpoint.

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
| TF-0014 | Planned | M4 | Create workspace routing model | `feature/tf-0014-workspace-routing-model` |
| TF-0015 | Planned | M4 | Define workspace state contracts | `feature/tf-0015-workspace-state-contracts` |
| TF-0016 | Planned | M5 | Implement replay projector foundation | `feature/tf-0016-replay-projector-foundation` |
| TF-0017 | Planned | M5 | Implement projection rebuild pipeline | `feature/tf-0017-projection-rebuild-pipeline` |
| TF-0018 | Planned | M5 | Implement replay timeline engine | `feature/tf-0018-replay-timeline-engine` |
| TF-0019 | Planned | M5 | Implement historical reconstruction pipeline | `feature/tf-0019-historical-reconstruction-pipeline` |
| TF-0020 | Planned | M6 | Define persona context model | `feature/tf-0020-persona-context-model` |
| TF-0021 | Planned | M6 | Implement workspace projection read models | `feature/tf-0021-workspace-projection-read-models` |
| TF-0022 | Planned | M6 | Implement operational attention queues | `feature/tf-0022-operational-attention-queues` |
| TF-0023 | Planned | M6 | Implement context-aware workspace summaries | `feature/tf-0023-context-aware-workspace-summaries` |
| TF-0024 | Planned | M7 | Add Postgres persistence layer | `feature/tf-0024-postgres-persistence` |
| TF-0025 | Planned | M7 | Add Alembic migration infrastructure | `feature/tf-0025-alembic-migrations` |
| TF-0026 | Planned | M7 | Persist canonical event ledger | `feature/tf-0026-postgres-event-ledger` |
| TF-0027 | Planned | M7 | Add FastAPI application runtime | `feature/tf-0027-fastapi-runtime` |
| TF-0028 | Planned | M7 | Add lifecycle API endpoints | `feature/tf-0028-lifecycle-api-endpoints` |
| TF-0029 | Planned | M7 | Add replay API endpoints | `feature/tf-0029-replay-api-endpoints` |
| TF-0030 | Planned | M7 | Add workspace projection APIs | `feature/tf-0030-workspace-projection-apis` |
| TF-0031 | Planned | M7 | Create React frontend scaffold | `feature/tf-0031-react-frontend-scaffold` |
| TF-0032 | Planned | M7 | Add workspace routing system | `feature/tf-0032-workspace-routing-system` |
| TF-0033 | Planned | M7 | Add shared operational layout system | `feature/tf-0033-operational-layout-system` |
| TF-0034 | Planned | M7 | Add authentication/session model | `feature/tf-0034-auth-session-model` |
| TF-0035 | Planned | M8 | Implement Operating Workspace | `feature/tf-0035-operating-workspace` |
| TF-0036 | Planned | M8 | Implement Opportunity Workspace | `feature/tf-0036-opportunity-workspace` |
| TF-0037 | Planned | M8 | Implement Plan Review Workspace | `feature/tf-0037-plan-review-workspace` |
| TF-0038 | Planned | M8 | Implement Active Position Workspace | `feature/tf-0038-active-position-workspace` |
| TF-0039 | Planned | M8 | Implement Replay Workspace | `feature/tf-0039-replay-workspace` |
| TF-0040 | Planned | M8 | Implement Review Workspace | `feature/tf-0040-review-workspace` |
| TF-0041 | Planned | M8 | Implement first replayable lifecycle flow | `feature/tf-0041-first-operational-mvp-flow` |

Post-MVP Roadmap v2 candidates TF-0042 through TF-0062 remain deferred until the MVP v1 path is underway. Do not pull M9-M13 work into the fast MVP path without an explicit roadmap checkpoint.

---
## TF-0001: Establish Milestone Roadmap And Issue Register

**Status:** Done

**Milestone:** M0

**Branch:** `docs/tf-0001-roadmap-issue-register`

**Affected Layer:** docs

**Linked ADRs:** ADR 0001, ADR 0002, ADR 0003, ADR 0004, ADR 0005, ADR 0006, ADR 0007, ADR 0008, ADR 0009, ADR 0010, ADR 0011

**Impacted Invariants:** Event Sourcing, Decision Lifecycle, Workspace, Persona, AI Authority, Scenario, Event Integrity, Replay, Layer Separation, Architectural Drift

**Implementation Summary:** Create `DOCS/MILESTONE_ROADMAP.md` and `DOCS/ISSUE_REGISTER.md` so future implementation work has a local planning source of truth.

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

**Status:** Planned

**Milestone:** M4

**Branch:** `feature/tf-0014-workspace-routing-model`

**Affected Layer:** app, services

**Linked ADRs:** ADR 0004, ADR 0007, ADR 0009, ADR 0012

**Impacted Invariants:** Workspace, Persona, Replay, Layer Separation

**Implementation Summary:** Define the runtime route/entrypoint model for MVP workspaces without treating routes as workspace truth.

**Acceptance Criteria:**

- MVP workspace routes are named and bounded.
- Routing preserves persona and selected workflow context.
- Routes do not mutate lifecycle state directly.
- Design references align with the KB `design/` draft layer.

**Out Of Scope:**

- Full React implementation.
- Dashboard-style generic routing.

---

## TF-0015: Define Workspace State Contracts

**Status:** Planned

**Milestone:** M4

**Branch:** `feature/tf-0015-workspace-state-contracts`

**Affected Layer:** domain, services, docs

**Linked ADRs:** ADR 0004, ADR 0007, ADR 0008, ADR 0012, ADR 0013

**Impacted Invariants:** Event Sourcing, Workspace, Persona, Replay, Layer Separation

**Implementation Summary:** Define the read-model contracts needed by Operating, Opportunity, Plan Review, Active Position, Replay, and Review workspaces.

**Acceptance Criteria:**

- Each MVP workspace has an explicit derived-state contract.
- Contracts distinguish canonical, derived, inferred, and advisory fields.
- Contracts identify required event inputs and replay needs.
- No workspace contract owns canonical lifecycle state.

**Out Of Scope:**

- Persistent projection storage.
- Full UI implementation.

---

## TF-0016: Implement Replay Projector Foundation

**Status:** Planned

**Milestone:** M5

**Branch:** `feature/tf-0016-replay-projector-foundation`

**Affected Layer:** domain, services

**Linked ADRs:** ADR 0001, ADR 0003, ADR 0008, ADR 0014

**Impacted Invariants:** Event Sourcing, Replay, Event Integrity, Layer Separation

**Implementation Summary:** Implement deterministic replay projection from ordered event history.

**Acceptance Criteria:**

- Replay consumes event history, not live APIs or UI state.
- Projector output is deterministic for the same event stream.
- Replay reconstructs lifecycle state for a basic workflow.
- Projection output remains derived and discardable.

**Out Of Scope:**

- AI-generated replay summaries.
- Historical market-data integrations.

---

## TF-0017: Implement Projection Rebuild Pipeline

**Status:** Planned

**Milestone:** M5

**Branch:** `feature/tf-0017-projection-rebuild-pipeline`

**Affected Layer:** services

**Linked ADRs:** ADR 0001, ADR 0004, ADR 0008, ADR 0014

**Impacted Invariants:** Event Sourcing, Replay, Layer Separation

**Implementation Summary:** Provide a service flow for rebuilding derived projections from event history.

**Acceptance Criteria:**

- Projections can be rebuilt from event history.
- Rebuild order is deterministic.
- Rebuild output does not become canonical truth.
- Tests cover repeatable projection output.

**Out Of Scope:**

- Durable projection persistence.

---

## TF-0018: Implement Replay Timeline Engine

**Status:** Planned

**Milestone:** M5

**Branch:** `feature/tf-0018-replay-timeline-engine`

**Affected Layer:** domain, services

**Linked ADRs:** ADR 0008, ADR 0014

**Impacted Invariants:** Replay, Event Integrity, Historical Integrity

**Implementation Summary:** Build the derived timeline model used by replay and review surfaces.

**Acceptance Criteria:**

- Timeline orders lifecycle, execution, review, and relevant system events deterministically.
- Timeline entries preserve event references and provenance.
- Timeline model supports replay UI without depending on UI state.

**Out Of Scope:**

- Interactive frontend timeline.

---

## TF-0019: Implement Historical Reconstruction Pipeline

**Status:** Planned

**Milestone:** M5

**Branch:** `feature/tf-0019-historical-reconstruction-pipeline`

**Affected Layer:** services

**Linked ADRs:** ADR 0008, ADR 0014

**Impacted Invariants:** Replay, Historical Integrity, Layer Separation

**Implementation Summary:** Compose lifecycle state, timeline, notes, rule evaluations, and review artifacts into a replayable historical reconstruction.

**Acceptance Criteria:**

- Reconstruction can answer what was known and visible at replay time.
- Reconstruction does not call live APIs.
- Reconstruction keeps facts, derived state, and inferred state distinguishable.

**Out Of Scope:**

- AI replay narration.

---

## TF-0020: Define Persona Context Model

**Status:** Planned

**Milestone:** M6

**Branch:** `feature/tf-0020-persona-context-model`

**Affected Layer:** domain

**Linked ADRs:** ADR 0009

**Impacted Invariants:** Persona, Workspace, Replay, Layer Separation

**Implementation Summary:** Define persona context as an interpretation model for workspace projection and prioritization.

**Acceptance Criteria:**

- Persona is not modeled as a user account or UI preference.
- Persona can be associated with workspace and workflow context.
- Persona influence is interpretive only.
- Historical replay can preserve persona context.

**Out Of Scope:**

- Authentication.

---

## TF-0021: Implement Workspace Projection Read Models

**Status:** Planned

**Milestone:** M6

**Branch:** `feature/tf-0021-workspace-projection-read-models`

**Affected Layer:** domain, services

**Linked ADRs:** ADR 0004, ADR 0007, ADR 0008, ADR 0009, ADR 0012

**Impacted Invariants:** Event Sourcing, Workspace, Persona, Replay, Layer Separation

**Implementation Summary:** Implement derived read models for MVP workspaces using event history and deterministic rules.

**Acceptance Criteria:**

- Workspace state is derived from events and deterministic rules.
- Workspace surfaces do not mutate canonical state.
- Workspace context is persona-scoped.
- Workspace projections can be rebuilt.

**Out Of Scope:**

- React UI.
- Stored workspace state as canonical truth.

---

## TF-0022: Implement Operational Attention Queues

**Status:** Planned

**Milestone:** M6

**Branch:** `feature/tf-0022-operational-attention-queues`

**Affected Layer:** domain, services

**Linked ADRs:** ADR 0013

**Impacted Invariants:** Workflow-Centric Architecture, Workspace, Human Decision Sovereignty

**Implementation Summary:** Implement derived queues for decisions, alerts, review obligations, and operational attention.

**Acceptance Criteria:**

- Queues are derived from lifecycle, risk, review, and workspace context.
- Queue items explain why attention is required.
- Queue items do not authorize execution by themselves.
- Queue ordering is deterministic and persona-aware where applicable.

**Out Of Scope:**

- AI prioritization.

---

## TF-0023: Implement Context-Aware Workspace Summaries

**Status:** Planned

**Milestone:** M6

**Branch:** `feature/tf-0023-context-aware-workspace-summaries`

**Affected Layer:** services

**Linked ADRs:** ADR 0004, ADR 0009, ADR 0012

**Impacted Invariants:** Workspace, Persona, Derived State Distinction

**Implementation Summary:** Generate concise derived summaries for workspace surfaces while preserving source/provenance references.

**Acceptance Criteria:**

- Summaries are derived and non-authoritative.
- Summary inputs are explicit.
- Persona context can shape emphasis without mutating facts.
- Summaries remain replay-compatible.

**Out Of Scope:**

- AI-generated summaries.

---

## TF-0024: Add Postgres Persistence Layer

**Status:** Planned

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

---

## TF-0025: Add Alembic Migration Infrastructure

**Status:** Planned

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

---

## TF-0026: Persist Canonical Event Ledger

**Status:** Planned

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

---

## TF-0027: Add FastAPI Application Runtime

**Status:** Planned

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

---

## TF-0028: Add Lifecycle API Endpoints

**Status:** Planned

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

---

## TF-0029: Add Replay API Endpoints

**Status:** Planned

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

---

## TF-0030: Add Workspace Projection APIs

**Status:** Planned

**Milestone:** M7

**Branch:** `feature/tf-0030-workspace-projection-apis`

**Affected Layer:** app, services

**Linked ADRs:** ADR 0004, ADR 0012, ADR 0020

**Impacted Invariants:** Workspace, Derived State Distinction

**Implementation Summary:** Expose workspace projection read models through API endpoints.

**Acceptance Criteria:**

- APIs return derived workspace state.
- APIs do not mutate canonical lifecycle state.
- Persona/workspace context is explicit.

**Out Of Scope:**

- Frontend rendering.

---

## TF-0031: Create React Frontend Scaffold

**Status:** Planned

**Milestone:** M7

**Branch:** `feature/tf-0031-react-frontend-scaffold`

**Affected Layer:** frontend

**Linked ADRs:** ADR 0021

**Impacted Invariants:** Workspace, UX Is Architectural

**Implementation Summary:** Create the React/TypeScript frontend foundation for MVP workspaces.

**Acceptance Criteria:**

- Frontend project runs locally.
- TypeScript is enabled.
- Frontend consumes API boundaries rather than event store internals.

**Out Of Scope:**

- Full workspace implementation.

---

## TF-0032: Add Workspace Routing System

**Status:** Planned

**Milestone:** M7

**Branch:** `feature/tf-0032-workspace-routing-system`

**Affected Layer:** frontend

**Linked ADRs:** ADR 0012, ADR 0021

**Impacted Invariants:** Workspace, Workflow Continuity

**Implementation Summary:** Implement frontend routing for the MVP workspace set.

**Acceptance Criteria:**

- Routes exist for the six core MVP workspaces.
- Navigation preserves selected context where applicable.
- Routes do not imply workspace ownership of canonical state.

**Out Of Scope:**

- Final visual design polish.

---

## TF-0033: Add Shared Operational Layout System

**Status:** Planned

**Milestone:** M7

**Branch:** `feature/tf-0033-operational-layout-system`

**Affected Layer:** frontend

**Linked ADRs:** ADR 0007, ADR 0012, ADR 0021

**Impacted Invariants:** UX Is Architectural, Workspace

**Implementation Summary:** Implement shared layout primitives for navigation, context panels, workspace headers, and operational surfaces.

**Acceptance Criteria:**

- Layout supports workspace continuity.
- UI avoids dashboard-first composition.
- Components distinguish action, context, and review surfaces.

**Out Of Scope:**

- Full design system library.

---

## TF-0034: Add Authentication/Session Model

**Status:** Planned

**Milestone:** M7

**Branch:** `feature/tf-0034-auth-session-model`

**Affected Layer:** app, frontend

**Linked ADRs:** ADR 0022

**Impacted Invariants:** Persona, Workspace, Replay

**Implementation Summary:** Add a minimal session model that separates user identity from persona context.

**Acceptance Criteria:**

- User/session identity is not confused with Persona.
- Persona activation remains explicit.
- Session context supports workspace continuity.

**Out Of Scope:**

- Full multi-user authorization model.

---

## TF-0035: Implement Operating Workspace

**Status:** Planned

**Milestone:** M8

**Branch:** `feature/tf-0035-operating-workspace`

**Affected Layer:** frontend, app, services

**Linked ADRs:** ADR 0012, ADR 0013, ADR 0021, ADR 0023

**Impacted Invariants:** Workspace, Workflow-Centric Architecture, UX Is Architectural

**Implementation Summary:** Implement the MVP Operating Workspace as the daily operational attention surface.

**Acceptance Criteria:**

- Displays decision queue, active positions, watch opportunities, alerts, and review obligations.
- Prioritizes decision state over market data.
- Actions route through lifecycle/API boundaries.

**Out Of Scope:**

- Market dashboard features.

---

## TF-0036: Implement Opportunity Workspace

**Status:** Planned

**Milestone:** M8

**Branch:** `feature/tf-0036-opportunity-workspace`

**Affected Layer:** frontend, app, services

**Linked ADRs:** ADR 0012, ADR 0021, ADR 0023

**Impacted Invariants:** Scenario, Decision Lifecycle, Workspace

**Implementation Summary:** Implement structured opportunity development without signal-generation semantics.

**Acceptance Criteria:**

- Shows opportunity state, thesis, setup, risks, and conditions.
- Promotion to plan cannot bypass lifecycle semantics.
- Charts support reasoning but do not dominate.

**Out Of Scope:**

- Scenario engine automation.

---

## TF-0037: Implement Plan Review Workspace

**Status:** Planned

**Milestone:** M8

**Branch:** `feature/tf-0037-plan-review-workspace`

**Affected Layer:** frontend, app, services

**Linked ADRs:** ADR 0002, ADR 0012, ADR 0021, ADR 0023

**Impacted Invariants:** Decision Lifecycle, Human Decision Sovereignty, UX Is Architectural

**Implementation Summary:** Implement intentional risk authorization workflow for trade plans.

**Acceptance Criteria:**

- Displays thesis, risk model, rule validation, sizing, and final decision context.
- Approval/rejection routes through lifecycle services.
- UI avoids BUY/SELL brokerage-ticket framing.

**Out Of Scope:**

- Broker execution.

---

## TF-0038: Implement Active Position Workspace

**Status:** Planned

**Milestone:** M8

**Branch:** `feature/tf-0038-active-position-workspace`

**Affected Layer:** frontend, app, services

**Linked ADRs:** ADR 0012, ADR 0021, ADR 0023

**Impacted Invariants:** Workspace, Replay, Historical Integrity

**Implementation Summary:** Implement live decision-state supervision for active positions.

**Acceptance Criteria:**

- Shows position state, thesis integrity context, timeline, actions, notes, and risk.
- PnL is visible but not dominant.
- Position actions remain workflow-aware.

**Out Of Scope:**

- Live broker sync.

---

## TF-0039: Implement Replay Workspace

**Status:** Planned

**Milestone:** M8

**Branch:** `feature/tf-0039-replay-workspace`

**Affected Layer:** frontend, app, services

**Linked ADRs:** ADR 0008, ADR 0014, ADR 0021, ADR 0023

**Impacted Invariants:** Replay, Historical Integrity, AI Advisory Boundary

**Implementation Summary:** Implement replay workspace for cognitive reconstruction from event-backed projections.

**Acceptance Criteria:**

- Displays replay timeline, context, lifecycle events, rule evaluations, and notes.
- Reconstruction depends on replay services, not live APIs or UI state.
- AI narration is not required.

**Out Of Scope:**

- AI replay assistance.

---

## TF-0040: Implement Review Workspace

**Status:** Planned

**Milestone:** M8

**Branch:** `feature/tf-0040-review-workspace`

**Affected Layer:** frontend, app, services

**Linked ADRs:** ADR 0017, ADR 0021, ADR 0023

**Impacted Invariants:** Review, Replay, Human Decision Sovereignty

**Implementation Summary:** Implement reflective review workspace that separates decision quality from outcome.

**Acceptance Criteria:**

- Captures review artifact fields.
- Shows rule adherence, replay highlights, lessons, and future adjustments.
- Review completion is event-backed.

**Out Of Scope:**

- Behavioral intelligence engine.

---

## TF-0041: Implement First Replayable Lifecycle Flow

**Status:** Planned

**Milestone:** M8

**Branch:** `feature/tf-0041-first-operational-mvp-flow`

**Affected Layer:** frontend, app, services, infrastructure

**Linked ADRs:** ADR 0001, ADR 0002, ADR 0004, ADR 0008, ADR 0023

**Impacted Invariants:** Event Sourcing, Decision Lifecycle, Workspace, Replay, Review

**Implementation Summary:** Implement the first usable end-to-end MVP workflow across lifecycle, API, projections, workspaces, replay, and review.

**Acceptance Criteria:**

- A user-controlled workflow progresses from Idea through Review.
- Material state changes are event-backed.
- Workspace state is derived from projections.
- Replay reconstructs workflow context.
- No autonomous AI or live broker execution is included.

**Out Of Scope:**

- M9 market/scenario intelligence.
- M10 AI advisory integration.

---


