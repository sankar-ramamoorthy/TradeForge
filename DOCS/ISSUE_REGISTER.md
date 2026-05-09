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
| TF-0012 | Planned | M3 | Implement lifecycle transition validator | `feature/tf-0012-lifecycle-transition-validator` |
| TF-0013 | Planned | M3 | Implement lifecycle orchestration service | `feature/tf-0013-lifecycle-orchestration-service` |
| TF-0014 | Planned | M4 | Implement replay projector foundation | `feature/tf-0014-replay-projector-foundation` |
| TF-0015 | Planned | M4/M5 | Implement workspace projection read model | `feature/tf-0015-workspace-projection-read-model` |
| TF-0016 | Planned | M5 | Define persona context model | `feature/tf-0016-persona-context-model` |
| TF-0017 | Planned | M6 | Define market intelligence interpretation model | `feature/tf-0017-market-intelligence-model` |
| TF-0018 | Planned | M6 | Define scenario discovery advisory model | `feature/tf-0018-scenario-discovery-model` |
| TF-0019 | Planned | M7 | Define AI advisory boundary interfaces | `feature/tf-0019-ai-advisory-boundary` |
| TF-0020 | Planned | M8 | Implement first vertical slice from Idea through Review replay | `feature/tf-0020-first-vertical-slice` |

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

**Status:** Planned

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

---

## TF-0013: Implement Lifecycle Orchestration Service

**Status:** Planned

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

---

## TF-0014: Implement Replay Projector Foundation

**Status:** Planned

**Milestone:** M4

**Branch:** `feature/tf-0014-replay-projector-foundation`

**Affected Layer:** domain, services

**Linked ADRs:** ADR 0001, ADR 0003, ADR 0008

**Impacted Invariants:** Event Sourcing, Replay, Event Integrity, Layer Separation

**Implementation Summary:** Define the replay projector abstraction and implement deterministic reconstruction from ordered event history.

**Acceptance Criteria:**

- Replay uses event history, not live APIs or UI state.
- Projector output is deterministic for the same event stream.
- Replay can reconstruct lifecycle state for a basic workflow.
- Projection state is derived and discardable.

**Out Of Scope:**

- Historical market data API integration.
- AI-generated replay summaries.

---

## TF-0015: Implement Workspace Projection Read Model

**Status:** Planned

**Milestone:** M4/M5

**Branch:** `feature/tf-0015-workspace-projection-read-model`

**Affected Layer:** domain, services

**Linked ADRs:** ADR 0004, ADR 0007, ADR 0008, ADR 0009

**Impacted Invariants:** Event Sourcing, Workspace, Persona, Replay, Layer Separation

**Implementation Summary:** Implement a derived workspace read model with briefing, opportunity, exposure, decision queue, and review surface boundaries.

**Acceptance Criteria:**

- Workspace state is derived from events and deterministic rules.
- Workspace surfaces do not mutate canonical state.
- Workspace context is persona-scoped.
- Projection can be rebuilt from event history.

**Out Of Scope:**

- Dashboard-style UI.
- Stored workspace state as canonical truth.

---

## TF-0016: Define Persona Context Model

**Status:** Planned

**Milestone:** M5

**Branch:** `feature/tf-0016-persona-context-model`

**Affected Layer:** domain

**Linked ADRs:** ADR 0004, ADR 0009

**Impacted Invariants:** Persona, Workspace, Replay, Layer Separation

**Implementation Summary:** Define persona context as an interpretation model that can influence ranking, weighting, and workflow emphasis without mutating canonical state.

**Acceptance Criteria:**

- Persona is not modeled as a user account or UI preference.
- Persona context can be associated with workspace and workflow context.
- Persona influence is interpretive only.
- Persona changes are compatible with historical replay.

**Out Of Scope:**

- Authentication and authorization.
- User profile management.

---

## TF-0017: Define Market Intelligence Interpretation Model

**Status:** Planned

**Milestone:** M6

**Branch:** `feature/tf-0017-market-intelligence-model`

**Affected Layer:** domain, services

**Linked ADRs:** ADR 0003, ADR 0009, ADR 0010

**Impacted Invariants:** Event Sourcing, Persona, Event Integrity, Layer Separation

**Implementation Summary:** Define interpreted market context structures for regimes, volatility, breadth, macro context, thematic narratives, and playbook activation conditions.

**Acceptance Criteria:**

- Market Intelligence outputs are interpreted context, not decisions.
- Market observations remain distinct from interpretations.
- Persona context may influence interpretation weighting.
- Outputs do not mutate lifecycle state.

**Out Of Scope:**

- Live market data ingestion.
- Trading signal generation.

---

## TF-0018: Define Scenario Discovery Advisory Model

**Status:** Planned

**Milestone:** M6

**Branch:** `feature/tf-0018-scenario-discovery-model`

**Affected Layer:** domain, services

**Linked ADRs:** ADR 0005, ADR 0009, ADR 0010

**Impacted Invariants:** Scenario, Decision Lifecycle, AI Authority, Layer Separation

**Implementation Summary:** Define advisory scenario models for hypotheses, rankings, invalidation, and watchlist promotion without creating decisions or execution instructions.

**Acceptance Criteria:**

- Scenarios are hypotheses, not trades or positions.
- Scenario ranking is advisory and non-authoritative.
- Scenario promotion cannot bypass lifecycle stages.
- Scenario outputs can feed workspace opportunity surfaces.

**Out Of Scope:**

- Broker execution.
- Autonomous strategy execution.

---

## TF-0019: Define AI Advisory Boundary Interfaces

**Status:** Planned

**Milestone:** M7

**Branch:** `feature/tf-0019-ai-advisory-boundary`

**Affected Layer:** domain, services

**Linked ADRs:** ADR 0006, ADR 0008, ADR 0010

**Impacted Invariants:** AI Authority, Event Sourcing, Decision Lifecycle, Replay, Layer Separation

**Implementation Summary:** Define interfaces for AI advisory outputs with provenance and uncertainty where practical, while preventing AI from owning canonical events or lifecycle transitions.

**Acceptance Criteria:**

- AI outputs are modeled as advisory artifacts.
- AI cannot directly append canonical decision or execution events.
- AI cannot approve plans, execute trades, or transition lifecycle state.
- AI outputs remain distinguishable from canonical state.

**Out Of Scope:**

- Provider-specific AI integration.
- Autonomous execution.

---

## TF-0020: Implement First Vertical Slice From Idea Through Review Replay

**Status:** Planned

**Milestone:** M8

**Branch:** `feature/tf-0020-first-vertical-slice`

**Affected Layer:** domain, services, infrastructure, app

**Linked ADRs:** ADR 0001, ADR 0002, ADR 0003, ADR 0004, ADR 0008

**Impacted Invariants:** Event Sourcing, Decision Lifecycle, Workspace, Replay, Event Integrity, Layer Separation

**Implementation Summary:** Implement the first local vertical slice that progresses a user-controlled workflow through Idea, Thesis, Plan, Approval, Execution, Position, and Review using event-backed transitions and deterministic replay.

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
