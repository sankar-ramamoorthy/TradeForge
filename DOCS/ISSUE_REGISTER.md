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

Explicit roadmap checkpoint completed M9 Updated*Done*.
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


