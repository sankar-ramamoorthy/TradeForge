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

## Issue Series

| Series | Pattern | Purpose |
|---|---|---|
| Roadmap issues | `TF-####` | Planned milestone implementation work — sequential, roadmap-tied |
| Feedback issues | `TF-F###` | Field-observed bugs, enhancements, and architectural gaps discovered during testing or operation |

`TF-F###` issues are not pre-planned. They originate from operational walkthroughs, testing sessions, or runtime observations. They are assigned to a milestone only when scheduled for implementation.

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
| TF-0065 | Done | M11 | Define AI advisory interfaces | `feature/tf-0065-ai-advisory-interfaces` |
| TF-0066 | Done | M11 | Implement replay summarization assistance | `feature/m11-ai-advisory-boundary` |
| TF-0067 | Done | M11 | Implement review assistance | `feature/m11-ai-advisory-boundary` |
| TF-0068 | Done | M11 | Implement advisory provenance tracking | `feature/m11-ai-advisory-boundary` |
| TF-A001 | Done | M12 | Define AdvisoryObservation domain model | `feature/m12-advisory-observation-foundation` |
| TF-A002 | Done | M12 | Implement advisory observation event taxonomy | `feature/m12-advisory-observation-foundation` |
| TF-A003 | Done | M12 | Implement observation provenance persistence | `feature/m12-advisory-observation-foundation` |
| TF-A004 | Done | M12 | Implement uncertainty metadata support | `feature/m12-advisory-observation-foundation` |
| TF-A005 | Done | M12 | Implement replay-visible advisory observation timeline | `feature/m12-advisory-observation-foundation` |
| TF-A006 | Done | M12 | Implement evidence attachment framework | `feature/m12-advisory-observation-foundation` |
| TF-A007 | Done | M12 | Implement thesis evidence linkage | `feature/m12-advisory-observation-foundation` |
| TF-A008 | Planned | M12 | Implement contextual interpretation artifacts | `feature/m12-advisory-observation-foundation` |
| TF-A009 | Planned | M12 | Implement conflicting evidence surfacing | `feature/m12-advisory-observation-foundation` |
| TF-A010 | Planned | M12 | Implement evidence aging/staleness visibility | `feature/m12-advisory-observation-foundation` |
| TF-A011 | Planned | M12 | Implement advisory candidate ingestion pipeline | `feature/m12-advisory-observation-foundation` |
| TF-A012 | Planned | M12 | Implement candidate review queue | `feature/m12-advisory-observation-foundation` |
| TF-A013 | Planned | M12 | Implement operator candidate promotion workflow | `feature/m12-advisory-observation-foundation` |
| TF-A014 | Planned | M12 | Prevent automated lifecycle promotion into TradeIdea | `feature/m12-advisory-observation-foundation` |
| TF-A015 | Planned | M12 | Implement candidate provenance visualization | `feature/m12-advisory-observation-foundation` |
| TF-A016 | Planned | M12 | Define external research cockpit import boundary | `feature/m12-advisory-observation-foundation` |
| TF-A017 | Planned | M12 | Implement research artifact ingestion API | `feature/m12-advisory-observation-foundation` |
| TF-A018 | Planned | M12 | Implement Codex/Claude-generated advisory artifact support | `feature/m12-advisory-observation-foundation` |
| TF-A019 | Planned | M12 | Implement advisory markdown artifact persistence | `feature/m12-advisory-observation-foundation` |
| TF-A020 | Planned | M12 | Implement replay-safe advisory snapshot capture | `feature/m12-advisory-observation-foundation` |
| TF-B001 | Planned | M13 | Define interpretation artifact schema | `feature/m13-contextual-interpretation-thesis-influence` |
| TF-B002 | Planned | M13 | Implement contextual weighting framework | `feature/m13-contextual-interpretation-thesis-influence` |
| TF-B003 | Planned | M13 | Implement regime-aware weighting model | `feature/m13-contextual-interpretation-thesis-influence` |
| TF-B004 | Planned | M13 | Implement conflicting evidence analysis | `feature/m13-contextual-interpretation-thesis-influence` |
| TF-B005 | Planned | M13 | Implement confidence-range representation | `feature/m13-contextual-interpretation-thesis-influence` |
| TF-B006 | Planned | M13 | Implement thesis evidence influence tracking | `feature/m13-contextual-interpretation-thesis-influence` |
| TF-B007 | Planned | M13 | Implement supporting vs weakening evidence classification | `feature/m13-contextual-interpretation-thesis-influence` |
| TF-B008 | Planned | M13 | Implement thesis drift detection | `feature/m13-contextual-interpretation-thesis-influence` |
| TF-B009 | Planned | M13 | Implement contextual contradiction surfacing | `feature/m13-contextual-interpretation-thesis-influence` |
| TF-B010 | Planned | M13 | Implement evidence impact replay overlays | `feature/m13-contextual-interpretation-thesis-influence` |
| TF-B011 | Planned | M13 | Implement interpretation-first operational surfaces | `feature/m13-contextual-interpretation-thesis-influence` |
| TF-B012 | Planned | M13 | Implement uncertainty-preserving UX patterns | `feature/m13-contextual-interpretation-thesis-influence` |
| TF-B013 | Planned | M13 | Implement probabilistic cognition summaries | `feature/m13-contextual-interpretation-thesis-influence` |
| TF-B014 | Planned | M13 | Implement evidence narrative generation | `feature/m13-contextual-interpretation-thesis-influence` |
| TF-B015 | Planned | M13 | Implement contextual reasoning timelines | `feature/m13-contextual-interpretation-thesis-influence` |
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
| M10AIS13 | Done | M10A | Implement replay annotation system | `feature/tf-0064-operational-attention-continuity` |
| M10AIS14 | Done | M10A | Implement playbook alignment projection layer | `feature/tf-0064-operational-attention-continuity` |
| M10AIS15 | Done | M10A | Implement cross-workspace cognitive continuity | `feature/tf-0064-operational-attention-continuity` |
| TF-F001 | Done | TBD | Add iterative revision workflow for thesis, plan, and assumptions | `feature/tf-f001-iterative-revision-workflow` |
| TF-F002 | Done | TBD | Introduce conditional execution state between Approval and Execution | `feature/tf-f002-awaiting-trigger-lifecycle-state` |
| TF-F003 | Done | TBD | Expand cognition input areas from CRUD-form style to thinking-space UX | `feature/tf-f003-cognition-ux-ergonomics` |
| TF-F004 | Done | M10C | Define operational credential boundary — ADR and Credential domain model | `feature/tf-f004-credential-boundary-design` |
| TF-F005 | Done | M10C | Implement KeyManager and encrypted local credential store | `feature/tf-f005-credential-store-implementation` |
| TF-F006 | Done | M10C | Wire all provider adapters through CredentialStore at composition root | `feature/tf-f006-provider-credential-wiring` |
| TF-F007 | Done | M10C | Credential setup guide, rotation documentation, keys-out-of-Git enforcement | `feature/tf-f007-credential-setup-documentation` |
| TF-F008 | Done | M10B | Wire PostgresEventStore as default runtime persistence via TRADEFORGE_DATABASE_URL | `feature/tf-f008-postgres-default-persistence` |
| TF-F009 | Done | M10B | Implement all-decisions projection and multi-decision navigation in Operating Workspace | `feature/tf-f009-multi-decision-navigation` |
| TF-F010 | Done | M10B | Fix thesis narrative minimum-length validation gap in ThesisDevelopmentModal | `feature/tf-0064-operational-attention-continuity` |
| TF-F012 | Done | TBD | Replace centered workspace shell with workstation-oriented operational layout model | `feature/tf-f012-workstation-layout-model` |
| TF-F013 | Done | TBD | Formalize three-layer design architecture between doctrine, workspace composition, and frontend translation | `docs/tf-f013-three-layer-design-architecture` |
| TF-F014 | Done | TBD | Extend workstation zoning to remaining market-context workspaces | `feature/tf-f014-remaining-workspace-zoning` |
| TF-F015 | Done | TBD | Fix missing return path in operational attention decision spec | `fix/tf-f015-operational-attention-mypy-return` |
| TF-F016 | Done | M10D | Capture provider capability gap and define M10D architecture | `docs/tf-f016-provider-capability-gap` |
| TF-F017 | Done | M10D | Introduce provider registry and capability metadata model | `feature/tf-f017-provider-registry-capabilities` |
| TF-F018 | Done | M10D | Split external data access into typed capability contracts | `feature/tf-f018-typed-external-data-contracts` |
| TF-F019 | Done | M10D | Add fundamentals data model and normalization boundary | `feature/tf-f019-fundamentals-normalization-boundary` |
| TF-F020 | Done | M10D | Implement initial fundamentals provider adapters | `feature/tf-f020-fundamentals-provider-adapters` |
| TF-F021 | Done | M10D | Expose capability-aware provider configuration and transparency | `feature/tf-f021-provider-capability-transparency` |
| TF-F022 | Done | M10D | Extend workspace context with fundamentals overlays | `feature/tf-f022-fundamentals-workspace-overlays` |
| TF-F023 | Done | M10D | M10D verification and M11 readiness gate | `docs/tf-f023-m10d-readiness-gate` |
| TF-F024 | Done | TBD | Fix documented credential setup command import failure | `fix/tf-f024-credential-script-import-path` |
| TF-F025 | Done | TBD | Gate frontend workspace loading when runtime API is unavailable | `fix/tf-f025-runtime-unavailable-gate` |
| TF-F026 | Done | TBD | Forward master key into Docker runtime container | `fix/tf-f026-compose-master-key-forwarding` |
| TF-F027 | Done | TBD | Clarify price versus fundamentals provider controls in context rail | `fix/tf-f027-provider-capability-rail-clarity` |
| TF-F028 | Done | M10E | Add persistent instrument identity to decision workspaces | `feature/tf-f028-workspace-instrument-identity` |
| TF-F029 | Done | M10E | Replace misleading candidate terminology in operator-facing UX | `feature/tf-f029-trader-facing-opportunity-language` |
| TF-F030 | Done | M10E | Replace provenance-first Opportunity panels with cognition-first synthesis surfaces | `feature/tf-f030-opportunity-synthesis-surfaces` |
| TF-F031 | Done | M10E | Interpret unavailable-context states with operator meaning and next actions | `feature/tf-f031-context-empty-state-interpretation` |
| TF-F032 | Done | M10E | Add explicit advisory context acquisition workflow | `feature/tf-f032-context-acquisition-workflow` |
| TF-F033 | Done | M10E | Surface advisory provider attempt status and fallback outcomes | `feature/tf-f033-provider-attempt-transparency` |
| TF-F034 | Done | M10E | Distinguish equity fundamentals from ETF context | `feature/tf-f034-instrument-aware-context-types` |
| TF-F035 | Done | M10E | Translate scenario-branch UX into trader-facing conditional reasoning | `feature/tf-f035-scenario-language-translation` |
| TF-F036 | Done | M10E | Add discretionary-thinking guidance to early opportunity evaluation | `feature/tf-f036-opportunity-cognition-guidance` |
| TF-F037 | Done | M10E | Introduce context interpretation layer between provider payloads and operator cognition | `feature/tf-f037-context-interpretation-layer` |
| TF-F038 | Done | M10E | Define dedicated Context Workbench workspace concept | `feature/tf-f038-context-workbench-concept` |
| TF-F039 | Done | M10E | Require recovery-oriented missing-information states across UX | `docs/tf-f039-missing-information-guidance` |
| TF-F040 | Done | M10E | Define trader-language boundary between canonical ontology and UX copy | `docs/tf-f040-trader-language-boundary` |
| TF-F041 | Done | M10E | Connect acquired advisory context to opportunity synthesis and thesis implications | `feature/tf-f041-context-to-synthesis-bridge` |
| TF-F042 | Done | M10E | Reframe market-context presentation from raw payload first to interpretation first | `feature/tf-f042-market-context-interpretation-first` |
| TF-F043 | Done | M10D | Update FMP fundamentals adapter to use stable endpoints | `fix/tf-f043-fmp-stable-fundamentals-endpoints` |
| TF-F044 | Done | M11 | Fold machine-assisted discretionary cognition roadmap into active roadmap v2 | `docs/tf-f044-roadmap-v3-integration` |

## TF-A001: Define AdvisoryObservation Domain Model

**Status:** Done

**Classification:** architectural

**Milestone:** M12

**Branch:** `feature/m12-advisory-observation-foundation`

**Affected Layer:** domain, services, docs, knowledge-base

**Linked ADRs:** ADR-0001, ADR-0003, ADR-0006, ADR-0008, ADR-0041

**Impacted Invariants:** Human Decision Sovereignty, AI Advisory Boundary, Derived State Must Remain Distinguishable, Terminology Stability

**Problem:**
TradeForge needs a durable pre-lifecycle advisory observation model that can capture machine- or operator-supplied observations without implying lifecycle, thesis, recommendation, or execution authority.

**Implementation Summary:**
Verified the existing advisory observation domain contract in `src/domain/advisory/observation.py`. The runtime already defines `AdvisoryObservation`, `CognitiveEvidence`, `ObservationKind`, `AdvisoryCaptureOrigin`, and `AdvisoryUncertaintyBand` as pure domain contracts with validation for persona/workspace context, provenance summary, evidence, caveats, captured timestamp, and advisory-only authority. The contract remains non-canonical and does not carry recommendation authority, lifecycle transition intent, or execution authority.

**Validation:**

- `uv run pytest tests\test_advisory_observation.py`

**Acceptance Criteria:**

- `AdvisoryObservation` exists as a pure domain contract.
- `CognitiveEvidence` exists as a pure domain contract.
- Observation kind is limited to: `price_action`, `fundamentals`, `market_context`, `news_research`, `risk`, `behavioral_process`, `operator_note`.
- Capture origin is limited to: `operator_manual`, `provider_import`, `codex_generated`, `claude_generated`, `imported_research`, `replay_annotation`, `future_scanner`.
- Observations require persona, workspace, capture origin, provenance, at least one source/evidence reference, uncertainty, caveats, and captured timestamp.
- Observations cannot carry recommendation authority, lifecycle transition intent, or execution authority.

---

## TF-A002: Implement Advisory Observation Event Taxonomy

**Status:** Done

**Classification:** architectural

**Milestone:** M12

**Branch:** `feature/m12-advisory-observation-foundation`

**Affected Layer:** domain, event model, docs

**Linked ADRs:** ADR-0001, ADR-0003, ADR-0006, ADR-0008, ADR-0041

**Impacted Invariants:** Event Ledger Canonical Truth, Events Are Immutable, Replayability Is Foundational, AI Advisory Boundary

**Problem:**
M12 advisory captures need a canonical fact event that records only that an observation artifact was captured, while preserving advisory artifact content outside the canonical ledger.

**Implementation Summary:**
Verified the existing advisory event taxonomy and capture path. `EventDomain.ADVISORY` is present in `src/domain/events/taxonomy.py`, and `AdvisoryObservationCaptureService` appends `advisory.observation_captured` as a capture-fact-only event. The payload includes observation ID, artifact ID, observation kind, capture origin, optional decision/thesis references, source references, provenance summary, uncertainty band, tags, captured timestamp, and advisory/non-canonical markers while excluding observation content and authority fields.

**Validation:**

- `uv run pytest tests\test_advisory_observation.py::test_advisory_event_domain_and_capture_event_are_supported tests\test_advisory_observation.py::test_replay_timeline_includes_advisory_capture_fact_without_content tests\test_domain_events.py`

**Acceptance Criteria:**

- `advisory` is an accepted canonical event domain.
- `advisory.observation_captured` can be appended to the event store and replayed.
- Event payload includes capture fact fields only: `observation_id`, `artifact_id`, `observation_kind`, `capture_origin`, optional `decision_id`, optional `thesis_id`, source references, provenance summary, uncertainty band, tags, and captured timestamp.
- Event payload does not include generated recommendation authority, lifecycle transition intent, execution authority, or generated observation content as canonical truth.

---

## TF-A003: Implement Observation Provenance Persistence

**Status:** Done

**Classification:** enhancement

**Milestone:** M12

**Branch:** `feature/m12-advisory-observation-foundation`

**Affected Layer:** infrastructure, services, app

**Linked ADRs:** ADR-0006, ADR-0018, ADR-0041

**Impacted Invariants:** Derived State Must Remain Distinguishable, Historical Integrity, AI Advisory Boundary

**Problem:**
Advisory observation content and evidence must persist durably without becoming event-ledger truth.

**Implementation Summary:**
Verified the existing non-canonical advisory observation artifact persistence. `InMemoryAdvisoryObservationStore` provides default/test persistence, and `PostgresAdvisoryObservationStore` persists observation content, evidence, provenance summary, caveats, tags, capture origin, persona/workspace context, optional decision/thesis context, and timestamps in the separate `advisory_observations` table. The migration creates `advisory_observations` separately from `event_ledger`, and stores support retrieval by observation ID plus list filtering by persona/workspace, decision, thesis, observation kind, source kind, and capture origin.

**Validation:**

- `uv run pytest tests\test_advisory_observation.py::test_in_memory_observation_store_persists_and_filters tests\test_advisory_observation.py::test_postgres_observation_store_shape_and_migration tests\test_advisory_observation.py::test_create_read_list_api_labels_advisory_observations`

**Acceptance Criteria:**

- A non-canonical advisory artifact store persists observation text, evidence references, provenance, caveats, tags, capture origin, persona/workspace context, and optional decision/thesis context.
- Postgres storage is separate from `event_ledger`.
- In-memory storage exists for tests and default runtime behavior.
- Stored records are retrievable by observation ID and listable by persona/workspace with filters for decision, thesis, observation kind, source kind, and capture origin.

---

## TF-A004: Implement Uncertainty Metadata Support

**Status:** Done

**Classification:** enhancement

**Milestone:** M12

**Branch:** `feature/m12-advisory-observation-foundation`

**Affected Layer:** domain, services, app

**Linked ADRs:** ADR-0006, ADR-0041

**Impacted Invariants:** AI Advisory Boundary, Derived State Must Remain Distinguishable, Human Decision Sovereignty

**Problem:**
Advisory observations must preserve uncertainty in qualitative, non-authoritative form so operators do not confuse them with deterministic signals.

**Implementation Summary:**
Verified the existing qualitative uncertainty metadata model and added focused regression coverage. `AdvisoryUncertaintyBand` supports `low`, `medium`, `high`, and `unknown`; invalid values fail enum/API validation; caveats are required by the domain model and API payload; persisted/API responses expose `uncertainty_band` and `caveats` as advisory metadata alongside advisory/non-canonical labels.

**Validation:**

- `uv run pytest tests\test_advisory_observation.py`

**Acceptance Criteria:**

- `AdvisoryUncertaintyBand` supports `low`, `medium`, `high`, and `unknown`.
- Invalid uncertainty bands fail validation.
- Caveats are required and persisted.
- API responses expose uncertainty as advisory metadata, not confidence-backed authority.

---

## TF-A005: Implement Replay-Visible Advisory Observation Timeline

**Status:** Done

**Classification:** enhancement

**Milestone:** M12

**Branch:** `feature/m12-advisory-observation-foundation`

**Affected Layer:** replay, services, app

**Linked ADRs:** ADR-0001, ADR-0006, ADR-0008, ADR-0041

**Impacted Invariants:** Replayability Is Foundational, Event Ledger Canonical Truth, Derived State Must Remain Distinguishable

**Problem:**
Replay must show that an advisory observation existed at a historical point without treating non-canonical advisory content as event truth.

**Implementation Summary:**
Verified and strengthened replay-visible advisory observation timeline behavior. The replay timeline builder includes `advisory.observation_captured` events as advisory entries in deterministic chronological order, preserves artifact identifiers and advisory/non-canonical boundary metadata, and does not require advisory content, live providers, current AI output, or mutable external state for reconstruction.

**Validation:**

- `uv run pytest tests\test_replay_timeline.py tests\test_replay_timeline_service.py tests\test_advisory_observation.py::test_replay_timeline_includes_advisory_capture_fact_without_content`

**Acceptance Criteria:**

- Replay timeline includes `advisory.observation_captured` entries in chronological order.
- Replay entries identify the artifact ID and advisory/non-canonical boundary.
- Replay distinguishes canonical capture facts from advisory artifact content.
- Replay does not depend on current AI output or live provider calls.

---

## TF-A006: Implement Evidence Attachment Framework

**Status:** Done

**Classification:** enhancement

**Milestone:** M12

**Branch:** `feature/m12-advisory-observation-foundation`

**Affected Layer:** domain, services, infrastructure, app

**Linked ADRs:** ADR-0001, ADR-0006, ADR-0033, ADR-0041

**Impacted Invariants:** AI Advisory Boundary, Derived State Must Remain Distinguishable, Historical Integrity, Replayability Is Foundational

**Problem:**
Advisory observations require durable evidence references so operators can inspect why an observation exists without treating supporting material as canonical lifecycle state.

**Implementation Summary:**
Extended the advisory evidence attachment contract with required M12 source kinds and optional per-evidence metadata for source URI, artifact ID, captured timestamp, provenance summary, and caveats. Evidence metadata is persisted in the non-canonical advisory artifact store and exposed through advisory API responses. Capture events retain only source-reference facts and continue to exclude evidence summary, provenance detail, caveats, and advisory content from canonical event truth.

**Validation:**

- `uv run pytest tests\test_advisory_observation.py`

**Acceptance Criteria:**

- `CognitiveEvidence` supports typed references for provider payloads, imported research, markdown artifacts, URLs, operator notes, replay annotations, and generated advisory artifacts.
- Advisory observations require at least one evidence reference at capture time.
- Evidence attachment records preserve source kind, source URI or artifact ID, captured timestamp, provenance summary, and caveats.
- Evidence content persists in the non-canonical advisory artifact store, not in `event_ledger`.
- Evidence attachment APIs and responses label evidence as advisory and non-canonical.

---

## TF-A007: Implement Thesis Evidence Linkage

**Status:** Done

**Classification:** enhancement

**Milestone:** M12

**Branch:** `feature/m12-advisory-observation-foundation`

**Affected Layer:** domain, services, app, replay

**Linked ADRs:** ADR-0001, ADR-0002, ADR-0006, ADR-0033, ADR-0041

**Impacted Invariants:** Human Decision Sovereignty, Lifecycle Authority, AI Advisory Boundary, Derived State Must Remain Distinguishable

**Problem:**
Operators need to associate advisory observations with an existing decision or thesis for context, while preserving that the association does not revise, approve, strengthen, weaken, or transition lifecycle state.

**Implementation Summary:**
Implemented deterministic context-link validation for advisory observations. The capture service now validates optional `decision_id` and `thesis_id` against event-store history before persisting an advisory observation or appending the capture fact. Valid links remain contextual advisory metadata in API responses and replay payloads; they do not create thesis influence, thesis revision, lifecycle transition, approval, plan change, or execution authority.

**Validation:**

- `uv run pytest tests\test_advisory_observation.py tests\test_replay_timeline.py tests\test_replay_timeline_service.py`

**Acceptance Criteria:**

- Advisory observations may optionally reference an existing `decision_id` and/or `thesis_id`.
- Linkage validation rejects references that cannot be resolved by deterministic runtime state.
- Thesis evidence links are contextual metadata only and do not create lifecycle events, thesis revisions, plan changes, approvals, or execution intent.
- API responses distinguish contextual advisory links from canonical thesis content.
- Replay can show that an observation was linked to a decision or thesis at capture time without deriving thesis influence semantics.

---

## TF-A008: Implement Contextual Interpretation Artifacts

**Status:** Planned

**Classification:** architectural

**Milestone:** M12

**Branch:** `feature/m12-advisory-observation-foundation`

**Affected Layer:** domain, services, infrastructure, app

**Linked ADRs:** ADR-0006, ADR-0039, ADR-0041, ADR-0042

**Impacted Invariants:** AI Advisory Boundary, Derived State Must Remain Distinguishable, Human Decision Sovereignty, Terminology Stability

**Problem:**
Some advisory observations need lightweight contextual framing so the operator can understand what environment the observation belongs to, but M12 must not implement M13 thesis influence, weighting, scoring, or recommendation semantics.

**Acceptance Criteria:**

- M12 contextual artifacts are stored as non-canonical advisory context attached to observations.
- Contextual artifacts may include regime notes, relevant market context references, caveats, provenance, and source links.
- Contextual artifacts do not include thesis influence, contextual weight, advisory confidence range, buy/sell direction, lifecycle transition intent, or execution authority.
- The implementation explicitly labels M13 `AdvisoryInterpretation` semantics as out of scope for this issue.
- Contextual artifact content persists outside `event_ledger`; canonical events record capture facts only when required by ADR-0041.

---

## TF-A009: Implement Conflicting Evidence Surfacing

**Status:** Planned

**Classification:** enhancement

**Milestone:** M12

**Branch:** `feature/m12-advisory-observation-foundation`

**Affected Layer:** services, app, frontend

**Linked ADRs:** ADR-0006, ADR-0039, ADR-0041, ADR-0042

**Impacted Invariants:** Human Decision Sovereignty, AI Advisory Boundary, Derived State Must Remain Distinguishable, Historical Integrity

**Problem:**
Operators need visibility when advisory evidence points in different directions, but M12 must surface conflict without turning it into scoring, thesis influence, recommendation authority, or automated decision guidance.

**Acceptance Criteria:**

- Advisory observation list/read workflows can expose conflict markers derived from explicit evidence metadata or operator-provided caveats.
- Conflicting evidence surfacing preserves source references and caveats for each side of the conflict.
- Conflict labels are qualitative advisory metadata only and do not rank, score, approve, reject, or promote observations.
- M13 supporting/weakening classification and thesis influence semantics remain out of scope.
- UI/API responses label conflict information as advisory and non-canonical.

---

## TF-A010: Implement Evidence Aging/Staleness Visibility

**Status:** Planned

**Classification:** enhancement

**Milestone:** M12

**Branch:** `feature/m12-advisory-observation-foundation`

**Affected Layer:** domain, services, app, frontend

**Linked ADRs:** ADR-0006, ADR-0041

**Impacted Invariants:** Historical Integrity, Replayability Is Foundational, AI Advisory Boundary, Derived State Must Remain Distinguishable

**Problem:**
Advisory evidence changes operational relevance over time. Operators need staleness visibility without the system mutating historical evidence or hiding uncertainty.

**Acceptance Criteria:**

- Evidence records preserve original captured timestamp and optional source timestamp.
- Derived staleness metadata is computed from timestamps and deterministic configuration, not stored as canonical truth.
- Staleness views distinguish current derived freshness from historical capture facts.
- Staleness labels do not invalidate, delete, rewrite, or silently downgrade historical observations.
- API/UI responses preserve uncertainty and caveats alongside staleness information.

---

## TF-A011: Implement Advisory Candidate Ingestion Pipeline

**Status:** Planned

**Classification:** enhancement

**Milestone:** M12

**Branch:** `feature/m12-advisory-observation-foundation`

**Affected Layer:** domain, services, infrastructure, app

**Linked ADRs:** ADR-0005, ADR-0006, ADR-0032, ADR-0041

**Impacted Invariants:** Human Decision Sovereignty, Scenario Discovery Is Non-Authoritative, AI Advisory Boundary, Derived State Must Remain Distinguishable

**Problem:**
TradeForge needs a way to ingest external or machine-surfaced advisory candidates into reviewable advisory space without creating trade ideas or lifecycle state.

**Acceptance Criteria:**

- `AdvisoryCandidate` exists as a non-canonical advisory artifact or view backed by advisory artifact persistence.
- Candidate ingestion accepts provider, imported research, generated advisory, and operator-supplied origins consistent with capture origin rules.
- Ingested candidates require provenance, evidence references, uncertainty, caveats, persona, workspace, and captured timestamp.
- Candidate ingestion does not create `TradeIdea`, thesis, plan, approval, execution, or decision lifecycle events.
- Candidate ingestion can append only advisory capture facts allowed by ADR-0041.

---

## TF-A012: Implement Candidate Review Queue

**Status:** Planned

**Classification:** enhancement

**Milestone:** M12

**Branch:** `feature/m12-advisory-observation-foundation`

**Affected Layer:** services, app, frontend

**Linked ADRs:** ADR-0004, ADR-0006, ADR-0013, ADR-0041

**Impacted Invariants:** Workspaces Are Operational Environments, Human Decision Sovereignty, Derived State Must Remain Distinguishable, Scenario Discovery Is Non-Authoritative

**Problem:**
Operators need a review queue for advisory candidates so attention can be organized without converting candidates into decisions or lifecycle obligations.

**Acceptance Criteria:**

- Candidate review queue is a derived read model, not canonical state.
- Queue entries are scoped by persona and workspace.
- Queue entries preserve source candidate ID, evidence references, provenance summary, uncertainty, caveats, and captured timestamp.
- Queue actions support inspect, dismiss from view, and begin operator-controlled promotion workflow without automated lifecycle transition.
- Queue ordering is deterministic and transparent; it does not introduce hidden AI ranking authority.

---

## TF-A013: Implement Operator Candidate Promotion Workflow

**Status:** Planned

**Classification:** architectural

**Milestone:** M12

**Branch:** `feature/m12-advisory-observation-foundation`

**Affected Layer:** domain, services, app, frontend

**Linked ADRs:** ADR-0002, ADR-0006, ADR-0034, ADR-0041

**Impacted Invariants:** Human Decision Sovereignty, Lifecycle Authority, AI Advisory Boundary, Workflow-Centric Architecture

**Problem:**
Operators need an explicit workflow to use an advisory candidate as input to a new trade idea while preserving that promotion is a human-owned lifecycle action.

**Acceptance Criteria:**

- Promotion requires an explicit operator action.
- Promotion opens or invokes the existing trade idea creation workflow rather than bypassing lifecycle rules.
- Advisory candidate content may prefill draft context only when labeled advisory and editable by the operator.
- The canonical lifecycle event, if created, is a normal operator-owned decision event and not an advisory event.
- Promotion records or preserves traceability back to the source advisory candidate without granting it lifecycle authority.

---

## TF-A014: Prevent Automated Lifecycle Promotion Into TradeIdea

**Status:** Planned

**Classification:** architectural

**Milestone:** M12

**Branch:** `feature/m12-advisory-observation-foundation`

**Affected Layer:** domain, services, app, tests

**Linked ADRs:** ADR-0002, ADR-0006, ADR-0041

**Impacted Invariants:** Human Decision Sovereignty, Lifecycle Authority, AI Advisory Boundary, Events Are Immutable

**Problem:**
M12 introduces advisory observations and candidates, increasing the risk that generated artifacts could be incorrectly treated as lifecycle inputs. Runtime safeguards must prevent automated promotion into `TradeIdea`.

**Acceptance Criteria:**

- Advisory capture, candidate ingestion, provider import, and generated artifact flows cannot create `TradeIdea` lifecycle events directly.
- Service-layer validation requires explicit operator intent for any transition from advisory candidate context into trade idea creation.
- AI/provider-generated artifacts are rejected as direct lifecycle transition commands.
- Tests cover attempts to create trade ideas through advisory ingestion paths.
- Error responses explain that advisory artifacts cannot bypass the decision lifecycle.

---

## TF-A015: Implement Candidate Provenance Visualization

**Status:** Planned

**Classification:** enhancement

**Milestone:** M12

**Branch:** `feature/m12-advisory-observation-foundation`

**Affected Layer:** services, app, frontend

**Linked ADRs:** ADR-0006, ADR-0007, ADR-0012, ADR-0041

**Impacted Invariants:** Historical Integrity, AI Advisory Boundary, Derived State Must Remain Distinguishable, UX Is Architectural

**Problem:**
Operators need to inspect where advisory candidates came from and why they are visible, without mistaking provenance displays for recommendation authority.

**Acceptance Criteria:**

- Candidate detail surfaces show capture origin, provider/source references, evidence references, caveats, uncertainty, captured timestamp, and artifact IDs.
- Provenance visualization distinguishes operator, provider, imported research, generated advisory, replay annotation, and future scanner origins.
- Provenance display is read-only with respect to canonical event history.
- UI copy labels candidates and provenance as advisory and non-canonical.
- Provenance views do not include buy/sell instructions, scores, lifecycle authority, or execution affordances.

---

## TF-A016: Define External Research Cockpit Import Boundary

**Status:** Planned

**Classification:** architectural

**Milestone:** M12

**Branch:** `feature/m12-advisory-observation-foundation`

**Affected Layer:** services, infrastructure, app, docs

**Linked ADRs:** ADR-0006, ADR-0032, ADR-0041

**Impacted Invariants:** AI Advisory Boundary, Market Intelligence Is Interpreted Context, Derived State Must Remain Distinguishable, Historical Integrity

**Problem:**
External research needs a controlled import boundary so research can become advisory evidence without becoming canonical truth, lifecycle authority, or untraceable external state.

**Acceptance Criteria:**

- Import boundary defines accepted research artifact metadata, source references, provenance, caveats, uncertainty, and capture origin.
- Imported research persists outside `event_ledger`.
- Imported research can be attached to advisory observations or candidates as evidence.
- Import boundary rejects payloads that attempt to create lifecycle transitions, approvals, execution intent, or recommendations as canonical truth.
- Runtime documentation records the non-canonical boundary and replay implications for imported research.

---

## TF-A017: Implement Research Artifact Ingestion API

**Status:** Planned

**Classification:** enhancement

**Milestone:** M12

**Branch:** `feature/m12-advisory-observation-foundation`

**Affected Layer:** infrastructure, services, app

**Linked ADRs:** ADR-0006, ADR-0020, ADR-0032, ADR-0041

**Impacted Invariants:** AI Advisory Boundary, Derived State Must Remain Distinguishable, Event Ledger Canonical Truth, Historical Integrity

**Problem:**
Operators need an API path to ingest research artifacts into advisory persistence with validation, provenance, and optional observation/candidate linkage.

**Acceptance Criteria:**

- API endpoint accepts research artifacts with required source, provenance, uncertainty, caveats, persona, workspace, and captured timestamp fields.
- API endpoint persists research content in the non-canonical advisory artifact store.
- API endpoint may create or link advisory observations/candidates only through M12 advisory capture services.
- API responses expose advisory/non-canonical labels and artifact IDs.
- Invalid payloads that imply recommendation, lifecycle transition intent, execution authority, or canonical truth are rejected.

---

## TF-A018: Implement Codex/Claude-Generated Advisory Artifact Support

**Status:** Planned

**Classification:** enhancement

**Milestone:** M12

**Branch:** `feature/m12-advisory-observation-foundation`

**Affected Layer:** domain, services, infrastructure, app

**Linked ADRs:** ADR-0006, ADR-0041

**Impacted Invariants:** AI Advisory Boundary, Human Decision Sovereignty, Derived State Must Remain Distinguishable, Historical Integrity

**Problem:**
Generated advisory artifacts from Codex or Claude need explicit capture origin, provenance, uncertainty, and operator-visible caveats so they can be inspected without becoming autonomous system authority.

**Acceptance Criteria:**

- Capture origin supports `codex_generated` and `claude_generated` for advisory artifacts.
- Generated artifacts require prompt/session provenance, source inputs or references, uncertainty, caveats, persona, workspace, and captured timestamp.
- Generated artifacts persist in the non-canonical advisory artifact store.
- Generated artifacts cannot append decision, lifecycle, approval, execution, or review events directly.
- API responses clearly label generated artifacts as advisory and non-canonical.

---

## TF-A019: Implement Advisory Markdown Artifact Persistence

**Status:** Planned

**Classification:** enhancement

**Milestone:** M12

**Branch:** `feature/m12-advisory-observation-foundation`

**Affected Layer:** infrastructure, services, app

**Linked ADRs:** ADR-0006, ADR-0041

**Impacted Invariants:** AI Advisory Boundary, Historical Integrity, Derived State Must Remain Distinguishable, Replayability Is Foundational

**Problem:**
Advisory research and generated cognition often arrive as markdown. Runtime needs durable markdown artifact persistence that remains advisory and non-canonical.

**Acceptance Criteria:**

- Advisory artifact store supports markdown body content with metadata, provenance, caveats, uncertainty, and source references.
- Markdown artifacts are retrievable by artifact ID and listable through advisory filters.
- Markdown content is stored outside `event_ledger`.
- Markdown rendering or retrieval does not execute embedded scripts or treat content as trusted commands.
- Markdown artifacts can be linked as evidence to observations or candidates.

---

## TF-A020: Implement Replay-Safe Advisory Snapshot Capture

**Status:** Planned

**Classification:** enhancement

**Milestone:** M12

**Branch:** `feature/m12-advisory-observation-foundation`

**Affected Layer:** replay, services, infrastructure, app

**Linked ADRs:** ADR-0001, ADR-0006, ADR-0008, ADR-0041

**Impacted Invariants:** Replayability Is Foundational, Event Ledger Canonical Truth, Historical Integrity, Derived State Must Remain Distinguishable

**Problem:**
Replay needs to reconstruct what advisory artifacts existed at the time of capture without depending on live providers, current AI output, or mutable external research sources.

**Acceptance Criteria:**

- Advisory artifact capture stores a replay-safe snapshot of required metadata, provenance, evidence references, uncertainty, caveats, and source identifiers.
- Snapshot capture preserves enough context to inspect historical advisory state without live provider calls.
- Snapshot content remains non-canonical; canonical events record only capture facts and artifact identifiers.
- Replay APIs expose advisory snapshot references while distinguishing event truth from advisory artifact content.
- Snapshot capture does not mutate, delete, or rewrite prior advisory artifacts or event ledger records.

---

## TF-B001: Define Interpretation Artifact Schema

**Status:** Planned

**Classification:** architectural

**Milestone:** M13

**Branch:** `feature/m13-contextual-interpretation-thesis-influence`

**Affected Layer:** domain, services, docs

**Linked ADRs:** ADR-0001, ADR-0006, ADR-0008, ADR-0041, ADR-0042

**Impacted Invariants:** Human Decision Sovereignty, Event Ledger Canonical Truth, Events Are Immutable, Replayability Is Foundational, AI Advisory Boundary, Derived State Must Remain Distinguishable, Terminology Stability

**Problem:**
M13 needs a durable interpretation artifact schema so advisory observations can gain contextual meaning without becoming lifecycle truth, recommendations, thesis revisions, approvals, or execution instructions.

**Acceptance Criteria:**

- `AdvisoryInterpretation` exists as a non-canonical advisory artifact linked to at least one `AdvisoryObservation` ID.
- Schema captures interpretation ID, artifact ID, linked observation IDs, optional decision/thesis IDs, interpretation kind, thesis influence, contextual weight, confidence range, provenance, caveats, tags, and captured timestamp.
- Interpretation content and rationale persist outside `event_ledger`.
- `advisory.interpretation_captured` records capture facts only and excludes interpretation body text, rationale, recommendations, lifecycle intent, and execution authority.
- Schema validation rejects buy/sell instructions, lifecycle transition intent, plan approval language, and execution instructions as authoritative fields.

---

## TF-B002: Implement Contextual Weighting Framework

**Status:** Planned

**Classification:** enhancement

**Milestone:** M13

**Branch:** `feature/m13-contextual-interpretation-thesis-influence`

**Affected Layer:** domain, services, app

**Linked ADRs:** ADR-0006, ADR-0039, ADR-0041, ADR-0042

**Impacted Invariants:** AI Advisory Boundary, Derived State Must Remain Distinguishable, Human Decision Sovereignty, Deterministic Rule Evaluation

**Problem:**
Operators need qualitative contextual weight for interpretations, but the system must avoid hidden scoring engines, deterministic predictive scoring, and recommendation authority.

**Acceptance Criteria:**

- Fixed qualitative contextual weight enum exists for M13 interpretation metadata.
- Contextual weight is stored as advisory metadata on `AdvisoryInterpretation`, not canonical decision state.
- Contextual weight cannot create, revise, approve, reject, or execute lifecycle artifacts.
- API responses label contextual weight as advisory and non-canonical.
- Numeric scoring, opaque ranking, and automated trade recommendation behavior are explicitly out of scope.

---

## TF-B003: Implement Regime-Aware Weighting Model

**Status:** Planned

**Classification:** enhancement

**Milestone:** M13

**Branch:** `feature/m13-contextual-interpretation-thesis-influence`

**Affected Layer:** domain, services, app

**Linked ADRs:** ADR-0006, ADR-0010, ADR-0039, ADR-0042

**Impacted Invariants:** Market Intelligence Is Interpreted Context, AI Advisory Boundary, Derived State Must Remain Distinguishable, Human Decision Sovereignty

**Problem:**
Interpretations may carry different meaning under different market regimes. Runtime needs a qualitative regime-aware model without turning regime context into automated trade selection.

**Acceptance Criteria:**

- Interpretations may reference regime context or market context artifacts as advisory inputs.
- Regime-aware metadata explains how regime context affects interpretation weight in qualitative terms.
- Regime-aware weighting does not mutate market intelligence facts, lifecycle state, thesis artifacts, plans, approvals, or executions.
- Missing or stale regime context is represented explicitly rather than inferred silently.
- API responses preserve provenance and caveats for regime context references.

---

## TF-B004: Implement Conflicting Evidence Analysis

**Status:** Planned

**Classification:** enhancement

**Milestone:** M13

**Branch:** `feature/m13-contextual-interpretation-thesis-influence`

**Affected Layer:** domain, services, app

**Linked ADRs:** ADR-0006, ADR-0041, ADR-0042

**Impacted Invariants:** Human Decision Sovereignty, AI Advisory Boundary, Derived State Must Remain Distinguishable, Historical Integrity

**Problem:**
M13 must allow operators to understand evidence conflict across observations and interpretations without reducing conflict to a hidden score or automated conclusion.

**Acceptance Criteria:**

- Conflict analysis can link multiple observations and interpretations into a non-canonical conflict artifact or interpretation field set.
- Conflict output preserves source evidence, provenance, caveats, uncertainty, and linked observation IDs.
- Conflict analysis distinguishes contradictory, partially conflicting, and unresolved evidence in qualitative terms.
- Conflict analysis cannot approve, reject, promote, execute, or revise lifecycle artifacts.
- Replay can show conflict analysis capture facts without treating conflict rationale as canonical event truth.

---

## TF-B005: Implement Confidence-Range Representation

**Status:** Planned

**Classification:** enhancement

**Milestone:** M13

**Branch:** `feature/m13-contextual-interpretation-thesis-influence`

**Affected Layer:** domain, services, app

**Linked ADRs:** ADR-0006, ADR-0041, ADR-0042

**Impacted Invariants:** AI Advisory Boundary, Derived State Must Remain Distinguishable, Human Decision Sovereignty, Terminology Stability

**Problem:**
Operators need uncertainty-preserving confidence ranges for interpretations, but M13 must avoid false precision and numeric prediction.

**Acceptance Criteria:**

- Fixed qualitative advisory confidence range enum exists for `AdvisoryInterpretation`.
- Confidence range requires caveats and provenance when persisted.
- Confidence range is exposed as advisory metadata only.
- Invalid confidence range values fail validation.
- Numeric prediction, probability-as-authority, and hidden model scores are rejected or out of scope.

---

## TF-B006: Implement Thesis Evidence Influence Tracking

**Status:** Planned

**Classification:** architectural

**Milestone:** M13

**Branch:** `feature/m13-contextual-interpretation-thesis-influence`

**Affected Layer:** domain, services, app, replay

**Linked ADRs:** ADR-0002, ADR-0006, ADR-0033, ADR-0041, ADR-0042

**Impacted Invariants:** Human Decision Sovereignty, Lifecycle Authority, AI Advisory Boundary, Derived State Must Remain Distinguishable

**Problem:**
Operators need to see how interpreted advisory evidence may influence an existing thesis, while preserving that the system does not revise the thesis or own lifecycle authority.

**Acceptance Criteria:**

- Interpretations may optionally reference a thesis and store qualitative thesis influence metadata.
- Thesis influence tracking is advisory and does not mutate thesis artifact content or append thesis revision events.
- Influence metadata preserves linked observation IDs, interpretation ID, caveats, provenance, and captured timestamp.
- API responses distinguish advisory influence from canonical thesis content.
- Operator-owned thesis revision remains a separate lifecycle or artifact workflow.

---

## TF-B007: Implement Supporting Vs Weakening Evidence Classification

**Status:** Planned

**Classification:** enhancement

**Milestone:** M13

**Branch:** `feature/m13-contextual-interpretation-thesis-influence`

**Affected Layer:** domain, services, app

**Linked ADRs:** ADR-0006, ADR-0041, ADR-0042

**Impacted Invariants:** Human Decision Sovereignty, AI Advisory Boundary, Derived State Must Remain Distinguishable, Terminology Stability

**Problem:**
Interpretations need qualitative classification for whether evidence appears to support, weaken, complicate, or remain neutral toward a thesis, without becoming an automated thesis judgment.

**Acceptance Criteria:**

- Fixed qualitative thesis influence classification exists for support, weaken, neutral, mixed, and unknown cases.
- Classification requires linked observations or evidence references.
- Classification is advisory metadata and cannot revise thesis content, promote lifecycle state, approve plans, or execute trades.
- Mixed or unknown classifications preserve uncertainty and caveats.
- API/UI responses label classification as advisory and non-canonical.

---

## TF-B008: Implement Thesis Drift Detection

**Status:** Planned

**Classification:** enhancement

**Milestone:** M13

**Branch:** `feature/m13-contextual-interpretation-thesis-influence`

**Affected Layer:** services, app, frontend

**Linked ADRs:** ADR-0002, ADR-0006, ADR-0033, ADR-0042

**Impacted Invariants:** Human Decision Sovereignty, Lifecycle Authority, Reflection And Review Are First-Class, Derived State Must Remain Distinguishable

**Problem:**
Operators need visibility when accumulated interpretations suggest that thesis context may have drifted, but the system must not automatically revise or invalidate the thesis.

**Acceptance Criteria:**

- Thesis drift indicators are derived from advisory interpretations and linked thesis context.
- Drift indicators are advisory-only and cannot append thesis revision, plan revision, approval, rejection, or execution events.
- Drift output preserves supporting interpretation IDs, evidence references, caveats, and uncertainty.
- Drift detection surfaces missing or insufficient evidence explicitly.
- UI/API responses present drift as operator attention context, not deterministic lifecycle authority.

---

## TF-B009: Implement Contextual Contradiction Surfacing

**Status:** Planned

**Classification:** enhancement

**Milestone:** M13

**Branch:** `feature/m13-contextual-interpretation-thesis-influence`

**Affected Layer:** services, app, frontend

**Linked ADRs:** ADR-0006, ADR-0039, ADR-0041, ADR-0042

**Impacted Invariants:** AI Advisory Boundary, Derived State Must Remain Distinguishable, Human Decision Sovereignty, UX Is Architectural

**Problem:**
Operators need contradictions between context, observations, interpretations, and thesis assumptions surfaced clearly without the runtime hiding uncertainty or resolving ambiguity automatically.

**Acceptance Criteria:**

- Contradiction surfacing links contradictory observations, interpretations, context references, or thesis assumptions.
- Contradictions preserve source provenance, caveats, uncertainty, and timestamps.
- The system does not automatically choose a winning interpretation or generate trade recommendations.
- Contradictions can create attention context but not lifecycle transitions.
- UI/API responses distinguish contradiction visibility from canonical decision truth.

---

## TF-B010: Implement Evidence Impact Replay Overlays

**Status:** Planned

**Classification:** enhancement

**Milestone:** M13

**Branch:** `feature/m13-contextual-interpretation-thesis-influence`

**Affected Layer:** replay, services, app, frontend

**Linked ADRs:** ADR-0001, ADR-0006, ADR-0008, ADR-0041, ADR-0042

**Impacted Invariants:** Replayability Is Foundational, Event Ledger Canonical Truth, Historical Integrity, Derived State Must Remain Distinguishable

**Problem:**
Replay should show when interpretations and evidence influence artifacts existed during a historical decision timeline without treating their content as canonical event truth.

**Acceptance Criteria:**

- Replay timeline includes `advisory.interpretation_captured` entries in chronological order.
- Replay overlays can display linked observation IDs, interpretation IDs, thesis references, influence metadata, confidence range, caveats, and provenance.
- Replay distinguishes canonical capture facts from non-canonical interpretation content.
- Replay does not require live providers, current AI output, mutable research sources, or UI state.
- Replay overlays do not alter lifecycle reconstruction or historical event ordering.

---

## TF-B011: Implement Interpretation-First Operational Surfaces

**Status:** Planned

**Classification:** enhancement

**Milestone:** M13

**Branch:** `feature/m13-contextual-interpretation-thesis-influence`

**Affected Layer:** services, app, frontend

**Linked ADRs:** ADR-0004, ADR-0006, ADR-0007, ADR-0012, ADR-0042

**Impacted Invariants:** Workspaces Are Operational Environments, UX Is Architectural, AI Advisory Boundary, Derived State Must Remain Distinguishable

**Problem:**
Workspace surfaces need to present interpretations as contextual cognition rather than raw payload lists, dashboard metrics, or recommendation cards.

**Acceptance Criteria:**

- Operational surfaces can list and inspect advisory interpretations by persona, workspace, decision, thesis, observation, influence, weight, confidence range, and tag filters.
- Surfaces prioritize interpretation summaries, caveats, provenance, uncertainty, and linked evidence.
- Surfaces label interpretation content as advisory and non-canonical.
- Surfaces do not include autonomous approve, execute, buy/sell, or lifecycle-transition controls.
- UI remains workspace-contextual rather than dashboard-centric.

---

## TF-B012: Implement Uncertainty-Preserving UX Patterns

**Status:** Planned

**Classification:** enhancement

**Milestone:** M13

**Branch:** `feature/m13-contextual-interpretation-thesis-influence`

**Affected Layer:** frontend, app, docs

**Linked ADRs:** ADR-0006, ADR-0007, ADR-0012, ADR-0042

**Impacted Invariants:** UX Is Architectural, AI Advisory Boundary, Derived State Must Remain Distinguishable, Human Decision Sovereignty

**Problem:**
M13 UX must preserve uncertainty, caveats, and non-authoritative status so operators do not confuse interpretation artifacts with deterministic signals.

**Acceptance Criteria:**

- Interpretation views render confidence range, uncertainty, caveats, provenance, and advisory/non-canonical labels together.
- Unknown, mixed, stale, or conflicting interpretation states are represented explicitly.
- UX patterns avoid numeric score emphasis, buy/sell language, hidden ranking, and recommendation framing.
- Empty and missing-information states guide operator review without fabricating conclusions.
- Runtime documentation records the uncertainty-preserving UI boundary for M13.

---

## TF-B013: Implement Probabilistic Cognition Summaries

**Status:** Planned

**Classification:** enhancement

**Milestone:** M13

**Branch:** `feature/m13-contextual-interpretation-thesis-influence`

**Affected Layer:** services, app, frontend

**Linked ADRs:** ADR-0006, ADR-0041, ADR-0042

**Impacted Invariants:** AI Advisory Boundary, Human Decision Sovereignty, Derived State Must Remain Distinguishable, Reflection And Review Are First-Class

**Problem:**
Operators need summaries of probabilistic cognition across interpretations, but summaries must remain qualitative advisory context rather than predictive scoring or automated recommendations.

**Acceptance Criteria:**

- Summary service derives qualitative cognition summaries from stored interpretations and linked observations.
- Summaries preserve uncertainty, caveats, conflicts, confidence ranges, and source provenance.
- Summaries are derived, rebuildable, non-canonical read models.
- Summaries do not create events, lifecycle transitions, thesis revisions, approvals, executions, or recommendations.
- API/UI responses label summaries as advisory and derived.

---

## TF-B014: Implement Evidence Narrative Generation

**Status:** Planned

**Classification:** enhancement

**Milestone:** M13

**Branch:** `feature/m13-contextual-interpretation-thesis-influence`

**Affected Layer:** services, app

**Linked ADRs:** ADR-0006, ADR-0041, ADR-0042

**Impacted Invariants:** AI Advisory Boundary, Human Decision Sovereignty, Historical Integrity, Derived State Must Remain Distinguishable

**Problem:**
Operators need narrative explanations of evidence and interpretation context, including AI-assisted drafts, but generated narratives must require operator acceptance before persistence and must not become canonical truth.

**Acceptance Criteria:**

- AI-assisted narrative drafts use the existing `AIAdvisoryProvider` boundary.
- Draft narratives are not persisted and do not append events until explicitly accepted or edited by the operator.
- Accepted narratives persist as non-canonical advisory interpretation artifact content.
- Narrative capture appends only allowed advisory capture facts and excludes generated rationale from canonical event truth.
- Generated narratives preserve source IDs, provenance, caveats, uncertainty, and advisory/non-canonical labels.

---

## TF-B015: Implement Contextual Reasoning Timelines

**Status:** Planned

**Classification:** enhancement

**Milestone:** M13

**Branch:** `feature/m13-contextual-interpretation-thesis-influence`

**Affected Layer:** replay, services, app, frontend

**Linked ADRs:** ADR-0001, ADR-0006, ADR-0008, ADR-0041, ADR-0042

**Impacted Invariants:** Replayability Is Foundational, Historical Integrity, Event Ledger Canonical Truth, Derived State Must Remain Distinguishable

**Problem:**
Operators need a contextual reasoning timeline that reconstructs how observations, interpretations, conflicts, and thesis influence evolved around a decision without altering canonical lifecycle history.

**Acceptance Criteria:**

- Contextual reasoning timeline composes advisory observation capture facts, interpretation capture facts, linked evidence, thesis references, and replay-safe snapshots.
- Timeline ordering is deterministic and based on captured timestamps and event history.
- Timeline distinguishes canonical events, non-canonical advisory artifacts, derived summaries, and inferred interpretation metadata.
- Timeline reconstruction does not depend on live APIs, current AI output, mutable external documents, or UI state.
- Timeline does not mutate lifecycle state, thesis artifacts, plans, approvals, executions, or event history.

---

## TF-F044: Fold Machine-Assisted Discretionary Cognition Roadmap Into Active Roadmap v2

**Status:** Done

**Classification:** documentation

**Milestone:** M11

**Branch:** `docs/tf-f044-roadmap-v3-integration`

**Affected Layer:** docs, knowledge-base

**Linked ADRs:** ADR-0006, ADR-0010, ADR-0014, ADR-0038

**Impacted Invariants:** Human Decision Sovereignty, AI Advisory Boundary, Event Ledger Canonical Truth, Replayability Is Foundational, Derived State Must Remain Distinguishable, Reflection And Review Are First-Class

**Source:** Brainstorm session captured in `knowledge/raw/TradeForge Future Direction - Machine-Assisted Discretionary Cognition.md` and proposed runtime roadmap `DOCS/Milestone_Roadmap_v3.md`.

**Problem:**
`DOCS/Milestone_Roadmap_v3.md` captured a stronger future direction for TradeForge after M11: machine-assisted discretionary cognition, evidence accumulation, contextual interpretation, behavioral auditability, replayable cognition, attention allocation, simulation, adaptive advisory research, and long-horizon cognitive performance analysis. The active planning authority remains `DOCS/Milestone_Roadmap_v2.md`, so v3 must be integrated into v2 rather than becoming a competing active roadmap.

**Acceptance Criteria:**

- M11 records the roadmap evolution note that foundational AI advisory work expands into machine-assisted discretionary cognition beginning with M12.
- `DOCS/Milestone_Roadmap_v2.md` remains the active roadmap and incorporates the v3 M12-M19 future direction.
- `DOCS/Milestone_Roadmap_v3.md` is marked as a historical proposal/source artifact rather than active planning authority.
- The raw brainstorm note is promoted into a processed KB synthesis.
- The raw brainstorm note is moved under `knowledge/raw/archived/`.
- KB index documentation is updated to point at active roadmap v2 and the processed synthesis.
- No runtime code, event model, lifecycle transition, or execution authority changes are introduced.

**Resolution Summary:**
Integrated the v3 cognitive advisory evolution into active roadmap v2, preserving v2 as the single going-forward planning source. Added the M11 roadmap evolution note and recast future milestones M12-M19 around advisory observations, contextual interpretation, behavioral auditability, cognitive replay, attention allocation, simulation, adaptive advisory research, and long-horizon cognitive performance analysis. Processed the source brainstorm into KB synthesis and archived the raw note.

**Completed Verification:**

- Documentation-only review.
- Confirmed no runtime code changes were required.

---

## TF-F043: Update FMP Fundamentals Adapter To Use Stable Endpoints

**Status:** Done

**Classification:** bug

**Milestone:** M10D

**Branch:** `fix/tf-f043-fmp-stable-fundamentals-endpoints`

**Affected Layer:** infrastructure

**Linked ADRs:** ADR-0038

**Impacted Invariants:** Market Intelligence Is Interpreted Context, Derived State Must Remain Distinguishable, Architectural Simplicity

**Source:** Runtime investigation and operator feedback captured on 2026-05-19 in `knowledge/raw/brainstorm-20260519-fmp-stable-endpoints-and-quote-context.md`.

**Problem:**
The FMP fundamentals adapter still calls older `/api/v3/...` FinancialModelingPrep endpoints. Live testing with the configured local FMP key showed those routes can return `403 Forbidden`, while the newer `/stable/income-statement` path succeeds. This causes fundamentals acquisition for symbols such as NVDA to degrade to unavailable even when the credential can access the newer stable API.

**Acceptance Criteria:**

- FMP fundamentals requests use the working stable endpoint family for profile, income statement, and ratios.
- The adapter continues to normalize provider-specific payloads into the existing `FundamentalsBundle` contract.
- Provider provenance and advisory/non-canonical boundaries remain unchanged.
- Tests cover stable endpoint URL construction and stable response normalization.
- FMP stable quote observations remain captured for future evaluation and are not added to the current fundamentals contract.

**Out Of Scope:**

- Adding FMP quote fields such as market cap, `priceAvg50`, or `priceAvg200` to runtime models.
- Changing provider preference semantics or fallback order.
- Changing lifecycle, event, or workspace authority.

**Resolution Summary:**
Updated the FMP fundamentals adapter to call the stable `profile`, `income-statement`, and `ratios` endpoint family with symbol query parameters. Adjusted stable ratios normalization to use `priceToEarningsRatio` while preserving the existing optional `return_on_equity` field. Captured the FMP stable quote observation as future advisory-context input without expanding the current fundamentals contract.

**Completed Verification:**

- `uv run ruff check src\infrastructure\market\fmp_adapter.py tests\test_fundamentals_adapters.py`
- `uv run mypy src\infrastructure\market\fmp_adapter.py tests\test_fundamentals_adapters.py`
- `uv run pytest tests\test_fundamentals_adapters.py tests\test_fundamentals_service.py tests\test_fundamentals_overlay.py`
- `uv run pytest`
- `npm.cmd run typecheck`
- `npm.cmd run build`
- Live FMP stable adapter check for `NVDA` returned company name, sector, statement date, revenue, net income, and P/E from provider `fmp`.
- Restarted the local API container and confirmed `GET /workspaces/fundamentals-context?symbol=NVDA&instrument_kind=equity` returns `coverage_status: available`, selected provider `fmp`, and a successful provider attempt.

---

## TF-F042: Reframe Market-Context Presentation From Raw Payload First To Interpretation First

**Status:** Done

**Classification:** enhancement

**Milestone:** M10E

**Branch:** `feature/tf-f042-market-context-interpretation-first`

**Affected Layer:** frontend, services

**Linked ADRs:** ADR-0010, ADR-0032, ADR-0038

**Impacted Invariants:** UX Is Architectural, Derived State Must Remain Distinguishable

**Source:** Opportunity Workspace discovery session captured on 2026-05-17 in `knowledge/raw/brainstorm-20260517-opportunity-workspace-ux-and-context-acquisition.md`; screenshots `brainstorm session Screenshot 2026-05-17 135450.png` and `brainstorm session Screenshot 2026-05-17 142020.png`.

**Problem:**
The current Market Context presentation leads with raw OHLCV values and provenance. That preserves advisory traceability, but it makes the surface feel like a provider payload inspector rather than a cognition aid. The operator must infer whether the instrument is ranging, compressing, breaking out, extended, or otherwise meaningful before the UI becomes useful.

**Acceptance Criteria:**

- Market-context presentation leads with an operator-readable interpretation before raw values.
- Raw OHLCV and provider provenance remain visible and distinguishable as advisory metadata.
- The interpretation does not become canonical truth or lifecycle authority.
- The surface makes current market behavior easier to understand without requiring the operator to mentally decode raw fields first.

**Out Of Scope:**

- Replacing normalized price contracts.
- Introducing AI-generated interpretation without a separate advisory-boundary decision.
- Removing raw provenance detail required for replay and auditability.

**Resolution Summary:**
Added deterministic interpretation fields to advisory market-context responses
and rendered those interpretations before raw OHLCV fields in both the shared
market-context rail and the Context Workbench while preserving raw values and
provider provenance.

**Completed Verification:**

- `uv run pytest tests\test_market_context_overlay.py`
- `npm.cmd run build`

---

## TF-F041: Connect Acquired Advisory Context To Opportunity Synthesis And Thesis Implications

**Status:** Done

**Classification:** enhancement

**Milestone:** M10E

**Branch:** `feature/tf-f041-context-to-synthesis-bridge`

**Affected Layer:** services, frontend

**Linked ADRs:** ADR-0010, ADR-0038

**Impacted Invariants:** UX Is Architectural, Workflow-Centric Architecture

**Source:** Opportunity Workspace discovery session captured on 2026-05-17.

**Problem:**
The right rail can display advisory market context while the center workspace remains largely unchanged. Context acquisition and workflow cognition are therefore disconnected: the trader can fetch information, but the Opportunity Workspace does not meaningfully reflect how that information changes opportunity posture, readiness, scenario evaluation, or thesis development.

**Acceptance Criteria:**

- Acquired advisory context can be reflected in Opportunity Workspace synthesis surfaces without becoming canonical truth.
- The workspace can show how context affects current opportunity interpretation, missing evidence, or thesis implications.
- Provider data remains advisory and provenance-preserving.
- The issue remains bounded to advisory synthesis; it does not alter lifecycle authority.

**Out Of Scope:**

- Auto-authoring a thesis from provider data.
- Automatically changing lifecycle state from advisory inputs.
- Solving the full future AI advisory layer.

**Resolution Summary:**
Added an advisory-only context handoff from the Context Workbench into the
Opportunity Workspace through local operational context, then introduced an
Opportunity synthesis surface that reflects acquired price posture, missing
evidence, and thesis implications without mutating canonical state.

**Completed Verification:**

- `npm.cmd run build`
- `uv run pytest tests\test_fundamentals_overlay.py tests\test_workspace_routing.py tests\test_workspace_state_contracts.py`

---

## TF-F040: Define Trader-Language Boundary Between Canonical Ontology And UX Copy

**Status:** Done

**Classification:** doctrine

**Milestone:** M10E

**Branch:** `docs/tf-f040-trader-language-boundary`

**Affected Layer:** docs, frontend

**Linked ADRs:** ADR-0012

**Impacted Invariants:** Terminology Stability, UX Is Architectural

**Source:** Opportunity Workspace discovery session captured on 2026-05-17.

**Problem:**
TradeForge currently exposes several internal ontology terms directly in operator-facing UX, including `candidate`, `scenario branches`, and visible provenance labels used as primary content. Canonical terminology is stable internally, but the system lacks an explicit boundary defining when operator-facing language should translate internal semantics into trader-native wording.

**Acceptance Criteria:**

- Runtime doctrine explicitly distinguishes canonical internal semantics from operator-facing language.
- Guidance exists for headings, prompts, panel names, empty states, and tooltips.
- The boundary preserves canonical terminology in the domain model while preventing avoidable ontology leakage into trader UX.
- Future frontend work can evaluate wording against a documented rule rather than ad hoc taste.

**Out Of Scope:**

- Renaming canonical domain entities.
- Rewriting all current UI copy in the same change.
- Changing event or lifecycle semantics.

**Resolution Summary:**
Added canonical trader-language doctrine in the knowledge base, extended UX doctrine with an explicit internal-semantics versus operator-language boundary, and updated the frontend design translation guide so future copy decisions can be evaluated against a stable rule instead of ad hoc taste.

**Completed Verification:**

- Confirmed `design/trader-language-doctrine.md` defines headings, prompts, empty states, provenance handling, and translation tests.
- Confirmed `UX_DOCTRINE.md` now carries the canonical trader-language principle.
- Confirmed `frontend/DESIGN.md` references the runtime translation rule for operator-facing copy.

---

## TF-F039: Require Recovery-Oriented Missing-Information States Across UX

**Status:** Done

**Classification:** doctrine

**Milestone:** M10E

**Branch:** `docs/tf-f039-missing-information-guidance`

**Affected Layer:** docs, frontend

**Linked ADRs:** none

**Impacted Invariants:** UX Is Architectural, Uncertainty Must Be Visible

**Source:** Opportunity Workspace discovery session captured on 2026-05-17.

**Problem:**
Several current surfaces report unavailable or absent information without explaining meaning, severity, continuity, or next action. The session surfaced this through `Fundamentals unavailable`, but the underlying gap is broader: TradeForge lacks a UX rule that missing-information states should answer what happened, why it matters, whether work can continue, and what the operator can do next.

**Acceptance Criteria:**

- Runtime UX doctrine defines the minimum content of a missing-information state.
- Missing states distinguish absence, not-yet-loaded state, failure, unsupported coverage, and intentional omission where relevant.
- Future UI surfaces can be reviewed against a consistent recovery-oriented standard.
- Guidance preserves uncertainty visibility rather than masking it.

**Out Of Scope:**

- Implementing every missing-state UI change immediately.
- Provider-specific retry behavior.
- Lifecycle changes.

**Resolution Summary:**
Added canonical missing-information doctrine in the KB, extended UX doctrine with a recovery-oriented rule, and updated frontend design guidance so future missing states must distinguish cause, consequence, continuity, and next action.

**Completed Verification:**

- Confirmed `design/missing-information-doctrine.md` defines distinct missing-state classes and required operator questions.
- Confirmed `UX_DOCTRINE.md` now carries the recovery-oriented missing-information principle.
- Confirmed `frontend/DESIGN.md` includes the corresponding runtime translation rule.

---

## TF-F038: Define Dedicated Context Workbench Workspace Concept

**Status:** Done

**Classification:** architectural

**Milestone:** M10E

**Branch:** `feature/tf-f038-context-workbench-concept`

**Affected Layer:** docs, domain, services, frontend

**Linked ADRs:** ADR-0012, ADR-0038, ADR-0040

**Impacted Invariants:** Workspaces Are Operational Environments, Workflow-Centric Architecture, UX Is Architectural

**Source:** Opportunity Workspace discovery session captured on 2026-05-17.

**Problem:**
The current Opportunity Workspace is being asked to support setup evaluation, context acquisition, provider inspection, and the early stages of research. The session surfaced a distinct operator need for a place devoted to gathering, inspecting, interpreting, and attaching advisory context before thesis or plan formation. That need appears semantically different from Opportunity evaluation itself.

**Acceptance Criteria:**

- The system evaluates whether a dedicated research/context workspace is required as a separate operational environment.
- The concept distinguishes context acquisition from opportunity evaluation and thesis formation.
- The proposed workspace owns a clear operational question and scope boundary.
- ADR evaluation is completed before implementation if the concept is accepted.

**Out Of Scope:**

- Implementing the workspace in this issue.
- Collapsing Opportunity, Thesis, and Research roles into one generic screen.
- Treating the workspace as a dashboard or settings view.

**Resolution Summary:**
Accepted the Context Workbench as a dedicated research-oriented workspace concept through ADR-0040 and added canonical design guidance defining its operational question, ownership boundary, candidate context families, and relationship to Opportunity and Thesis work.

**Completed Verification:**

- Confirmed `DOCS/adr/0040-context-workbench-workspace-concept.md` records the accepted workspace boundary.
- Confirmed `design/context-workbench.md` defines the workspace's operational question, owned responsibilities, exclusions, and downstream issue dependencies.

---

## TF-F037: Introduce Context Interpretation Layer Between Provider Payloads And Operator Cognition

**Status:** Done

**Classification:** architectural

**Milestone:** M10E

**Branch:** `feature/tf-f037-context-interpretation-layer`

**Affected Layer:** services, frontend

**Linked ADRs:** ADR-0010, ADR-0032, ADR-0038, ADR-0039

**Impacted Invariants:** AI Advisory Boundary, Derived State Must Remain Distinguishable, UX Is Architectural

**Source:** Opportunity Workspace discovery session captured on 2026-05-17.

**Problem:**
TradeForge currently has provider data and lifecycle workflow, but the session exposed a missing middle layer that translates fetched advisory data into operator-usable interpretation. Without that layer, the runtime can collect context while still failing to explain what it means for the decision process.

**Acceptance Criteria:**

- The architecture defines a bounded interpretation layer between normalized provider outputs and workspace presentation.
- The layer is explicitly advisory and does not mutate canonical state.
- The design preserves provenance and uncertainty while enabling operator-readable synthesis.
- ADR evaluation occurs before implementation because the change introduces a durable architectural layer.

**Out Of Scope:**

- Autonomous trade recommendations.
- Lifecycle transitions driven by provider data.
- Hiding raw data or uncertainty from the operator.

**Resolution Summary:**
Introduced the Context Interpretation Layer through ADR-0039 and canonical design doctrine so normalized advisory provider outputs can become operator-readable cognition without becoming canonical truth or lifecycle authority.

**Completed Verification:**

- Confirmed `DOCS/adr/0039-context-interpretation-layer.md` records the accepted interpretation boundary.
- Confirmed `design/context-interpretation-layer.md` defines inputs, outputs, authority limits, and the distinction between deterministic and future AI interpretation.

---

## TF-F036: Add Discretionary-Thinking Guidance To Early Opportunity Evaluation

**Status:** Done

**Classification:** enhancement

**Milestone:** M10E

**Branch:** `feature/tf-f036-opportunity-cognition-guidance`

**Affected Layer:** frontend

**Linked ADRs:** ADR-0012

**Impacted Invariants:** UX Is Architectural, Workflow-Centric Architecture

**Source:** Opportunity Workspace discovery session captured on 2026-05-17.

**Problem:**
The Opportunity Workspace currently reports state but offers limited guidance on how the operator should reason through an early setup. The session identified missing guidance around confirmation, invalidation, readiness, risk definition, and missing evidence.

**Acceptance Criteria:**

- Early opportunity surfaces guide the operator through the major questions needed before thesis development.
- Guidance remains advisory and does not collapse into automatic recommendation.
- Prompts distinguish what is known, what is missing, and what requires operator judgment.
- The workspace becomes more useful for structured discretionary thinking, not just lifecycle display.

**Out Of Scope:**

- Completing the thesis for the operator.
- Rule-engine enforcement changes.
- AI-generated recommendations.

**Resolution Summary:**
Added an advisory reasoning guide to the Opportunity Workspace covering
confirmation, invalidation, missing information, and operator judgment so the
surface supports discretionary evaluation before thesis formation.

**Completed Verification:**

- `npm.cmd run build`

---

## TF-F035: Translate Scenario-Branch UX Into Trader-Facing Conditional Reasoning

**Status:** Planned

**Classification:** enhancement

**Milestone:** M10E

**Branch:** `feature/tf-f035-scenario-language-translation`

**Affected Layer:** frontend

**Linked ADRs:** ADR-0012

**Impacted Invariants:** UX Is Architectural, Terminology Stability

**Source:** Opportunity Workspace discovery session captured on 2026-05-17.

**Problem:**
`Scenario Branches` is structurally correct but operator-facing language remains abstract. The user-facing task is conditional reasoning about bull cases, failed setups, invalidation, and alternate paths, not managing a graph concept.

**Acceptance Criteria:**

- Scenario-related UX uses trader-readable framing while preserving underlying canonical scenario semantics.
- Empty-state guidance explains the operator task in conditional-reasoning terms.
- The operator can understand why creating scenarios matters before planning.
- Canonical scenario models remain unchanged.

**Out Of Scope:**

- Redesigning scenario data structures.
- Adding new scenario event types.
- Changing lifecycle transitions.

**Resolution Summary:**
Translated scenario-facing UI copy into trader language: `Conditional Paths`,
`Bull Case`, `Failed Setup`, `Alternate Path`, and supporting empty-state
guidance now describe the operator task while preserving canonical scenario
events underneath.

**Completed Verification:**

- `npm.cmd run build`

---

## TF-F034: Distinguish Equity Fundamentals From ETF Context

**Status:** Done

**Classification:** enhancement

**Milestone:** M10E

**Branch:** `feature/tf-f034-instrument-aware-context-types`

**Affected Layer:** domain, services, frontend

**Linked ADRs:** ADR-0038

**Impacted Invariants:** Derived State Must Remain Distinguishable, Architectural Simplicity

**Source:** Opportunity Workspace discovery session captured on 2026-05-17.

**Problem:**
The session used EWY as an example where `Fundamentals unavailable` may be a misleading presentation because ETF context is not the same as company fundamentals. The system currently lacks instrument-aware treatment that can distinguish equity fundamentals from ETF-relevant context such as holdings, exposure, or macro sensitivity.

**Acceptance Criteria:**

- The external-context model distinguishes company-fundamentals coverage from ETF-relevant context.
- Unsupported or mismatched context is represented explicitly instead of collapsing into a generic unavailable state.
- Operator-facing UI can explain why one context type is absent and what alternative context is relevant.
- Existing fundamentals semantics remain intact for equities.

**Out Of Scope:**

- Full ETF analytics implementation.
- Expanding to all future security types at once.
- Treating absent ETF context as a provider failure when the issue is semantic mismatch.

**Resolution Summary:**
Introduced explicit instrument-kind and external-context-type semantics for
fundamentals overlays, returning an `unsupported` company-fundamentals state
for ETFs with an `etf_context` alternative instead of misclassifying that case
as provider failure. The Context Workbench now lets the operator declare
equity versus ETF when requesting context.

**Completed Verification:**

- `uv run pytest tests\test_fundamentals_overlay.py`
- `npm.cmd run build`

---

## TF-F033: Surface Advisory Provider Attempt Status And Fallback Outcomes

**Status:** Planned

**Classification:** enhancement

**Milestone:** TBD

**Branch:** `feature/tf-f033-provider-attempt-transparency`

**Affected Layer:** services, app, frontend

**Linked ADRs:** ADR-0038

**Impacted Invariants:** Derived State Must Remain Distinguishable, Replayability Is Foundational

**Source:** Opportunity Workspace discovery session captured on 2026-05-17.

**Problem:**
The operator can see selected providers and fallback order, but when data is absent there is no visible evidence of whether retrieval was attempted, which provider was used, whether fallback was tried, or why retrieval failed. This weakens the transparency promised by the capability-aware provider architecture.

**Acceptance Criteria:**

- Advisory context surfaces expose attempted provider order, selected provider, fallback usage, timestamps, and failure reasons where relevant.
- UI distinguishes configured provider state from actual acquisition attempts.
- Provider attempt information remains advisory and replay-preservable.
- Missing context can be understood without consulting logs.

**Out Of Scope:**

- Provider health-management systems.
- Automatic remediation or credential rotation.
- Changing provider preference semantics.

**Resolution Summary:**
Added explicit advisory provider-attempt records to the live price and
fundamentals acquisition paths, exposed attempt order / outcome / timestamp /
failure reason through the workspace APIs, and rendered those facts inside the
Context Workbench so unavailable states no longer require log inspection.

**Completed Verification:**

- `uv run pytest`
- `uv run pytest tests\test_market_snapshot_service.py tests\test_fundamentals_service.py tests\test_fundamentals_overlay.py tests\test_market_context_overlay.py`
- `uv run ruff check src\services\market\context.py src\services\market\snapshot_service.py src\services\market\fundamentals_service.py tests\test_fundamentals_service.py tests\test_fundamentals_overlay.py tests\test_market_context_overlay.py tests\test_market_snapshot_service.py`
- `npm.cmd run build`

---

## TF-F032: Add Explicit Advisory Context Acquisition Workflow

**Status:** Planned

**Classification:** enhancement

**Milestone:** TBD

**Branch:** `feature/tf-f032-context-acquisition-workflow`

**Affected Layer:** services, app, frontend

**Linked ADRs:** ADR-0010, ADR-0038, ADR-0039, ADR-0040

**Impacted Invariants:** UX Is Architectural, Workflow-Centric Architecture

**Source:** Opportunity Workspace discovery session captured on 2026-05-17.

**Problem:**
The current operator flow does not make advisory information acquisition explicit. Price loading exists, fundamentals may load elsewhere, and future context types are implied but not represented as a coherent workflow. The operator cannot clearly request or inspect distinct context domains such as fundamentals, catalysts, sector context, or technical context.

**Acceptance Criteria:**

- The runtime defines an explicit operator workflow for requesting advisory context by context family.
- The workflow distinguishes configured providers from actual information acquisition.
- Operator actions and resulting states make it clear what was requested, loaded, skipped, or unavailable.
- Context acquisition remains advisory and does not become lifecycle authority.

**Out Of Scope:**

- Implementing every possible context family at once.
- Automatically acquiring all context without operator intent.
- Turning context acquisition into a generic dashboard.

**Resolution Notes:**

- Added first-class `context-workbench` routing and workspace-state contract support.
- Added a dedicated frontend Context Workbench with explicit operator-requested acquisition for `Price / Technical` and `Fundamentals`.
- Surfaced per-family `not requested`, `loading`, `loaded`, and `unavailable` states while keeping provider configuration separate from acquisition actions.
- Preserved advisory-only boundaries; no lifecycle transitions or canonical events were introduced.
- Verification passed for focused workspace-route/state-contract tests plus frontend typecheck/build. Full-suite verification remains blocked locally because the rotated `TRADEFORGE_MASTER_KEY` does not decrypt the persisted provider credential payloads during API import.

---

## TF-F031: Interpret Unavailable-Context States With Operator Meaning And Next Actions

**Status:** Planned

**Classification:** enhancement

**Milestone:** TBD

**Branch:** `feature/tf-f031-context-empty-state-interpretation`

**Affected Layer:** frontend, services

**Linked ADRs:** ADR-0038

**Impacted Invariants:** UX Is Architectural, Uncertainty Must Be Visible

**Source:** Opportunity Workspace discovery session captured on 2026-05-17.

**Problem:**
`Fundamentals unavailable` currently reports a technical state but gives the trader no meaning, implication, severity, or next action. The operator cannot tell whether retrieval was never attempted, a provider failed, the instrument is unsupported, credentials are missing, or the absence is non-blocking.

**Acceptance Criteria:**

- Unavailable-context states distinguish the major causes that matter to the operator.
- The UI states what the absence means for current decision work and whether the operator can continue.
- The surface offers an appropriate next action or explanation where one exists.
- Advisory uncertainty remains visible rather than being hidden.

**Out Of Scope:**

- Building the full provider attempt history system.
- Full cross-product missing-state doctrine.
- Converting unavailable advisory context into a lifecycle blocker.

**Resolution Summary:**
Reworked unavailable advisory context copy so price and fundamentals surfaces
state what failed, what that means for current work, whether the operator can
continue, and what next action remains available.

**Completed Verification:**

- `npm.cmd run build`

---

## TF-F030: Replace Provenance-First Opportunity Panels With Cognition-First Synthesis Surfaces

**Status:** Done

**Classification:** enhancement

**Milestone:** M10E

**Branch:** `feature/tf-f030-opportunity-synthesis-surfaces`

**Affected Layer:** frontend, services

**Linked ADRs:** ADR-0012

**Impacted Invariants:** UX Is Architectural, Workflow-Centric Architecture

**Source:** Opportunity Workspace discovery session captured on 2026-05-17; screenshot `brainstorm session Screenshot 2026-05-17 142020.png`.

**Problem:**
The main body of the Opportunity Workspace is dominated by provenance-oriented boxes such as `Scenario References`, `Opportunity Candidates`, `Setup Quality`, and `Advisory Notes`. In their current form they communicate source categories more strongly than opportunity meaning, producing a visually large but cognitively thin region.

**Acceptance Criteria:**

- The primary Opportunity Workspace surfaces answer what is interesting now, why it matters, what is missing, and how mature the setup is.
- Provenance remains accessible but becomes secondary metadata rather than the dominant visual structure.
- Candidate surfaces can represent narrative, signals, readiness, missing confirmation, contradiction, and conditional paths.
- The resulting workspace better supports opportunity evaluation before thesis formation.

**Out Of Scope:**

- Removing provenance or replay metadata.
- Replacing event-sourced projections with mutable UI state.
- Completing context interpretation architecture inside the same issue.

**Resolution Summary:**
Reframed the Opportunity Workspace around evaluation surfaces answering what is
interesting now, why it matters, what is missing, and how mature the setup is,
while moving projection/provenance boxes behind a secondary details section.

**Completed Verification:**

- `npm.cmd run build`

---

## TF-F029: Replace Misleading Candidate Terminology In Operator-Facing UX

**Status:** Done

**Classification:** bug

**Milestone:** M10E

**Branch:** `feature/tf-f029-trader-facing-opportunity-language`

**Affected Layer:** frontend

**Linked ADRs:** ADR-0012

**Impacted Invariants:** UX Is Architectural, Terminology Stability

**Source:** Opportunity Workspace discovery session captured on 2026-05-17; screenshot `brainstorm session Screenshot 2026-05-17 142020.png`.

**Problem:**
`What candidate decisions are developing?` and related `candidate` wording are misleading inside a workspace entered for one selected symbol. The terms imply a scanner or portfolio-level decision surface and do not match how the operator naturally thinks about an early setup.

**Acceptance Criteria:**

- Opportunity Workspace headings and prompts use operator-facing wording that matches the actual single-symbol workflow.
- Copy no longer makes the operator infer the meaning of `candidate` from internal lifecycle semantics.
- Any chosen replacement language remains consistent across headings, explanatory text, and actions.
- Canonical internal terms remain available where required for implementation and documentation.

**Out Of Scope:**

- Renaming domain entities.
- Solving all broader trader-language doctrine questions.
- Redesigning the workspace layout.

**Resolution Summary:**
Replaced operator-facing `candidate` wording in the Opportunity flow with
single-symbol setup language and updated the runtime route question to match.

**Completed Verification:**

- `npm.cmd run build`
- `uv run pytest tests\test_workspace_routing.py`

---

## TF-F028: Add Persistent Instrument Identity To Decision Workspaces

**Status:** Done

**Classification:** enhancement

**Milestone:** M10E

**Branch:** `feature/tf-f028-workspace-instrument-identity`

**Affected Layer:** frontend

**Linked ADRs:** ADR-0012

**Impacted Invariants:** UX Is Architectural, Workflow Continuity Principle

**Source:** Opportunity Workspace discovery session captured on 2026-05-17; screenshot `brainstorm session Screenshot 2026-05-17 142020.png`.

**Problem:**
After entering a symbol-specific Opportunity Workspace, the main surface does not strongly anchor which instrument is being evaluated. The operator must rely on small sidebar context or infer identity indirectly, even though the trader’s cognitive frame is centered on the instrument rather than the internal decision id.

**Acceptance Criteria:**

- Symbol-specific workspaces present a persistent, prominent instrument identity anchor.
- The anchor supports at least ticker identity and relevant descriptive context appropriate to the workspace.
- Workspace headers make it immediately clear what instrument, context, and stage the operator is working on.
- The pattern is designed for continuity across later workspaces, not only one local screen.

**Out Of Scope:**

- Full quote terminal behavior.
- Redesigning every workspace in the same change.
- Replacing decision ids internally.

**Resolution Summary:**
Added a reusable instrument-identity banner to the Opportunity Workspace so the
active ticker and lifecycle stage are persistent first-class anchors during
single-symbol evaluation.

**Completed Verification:**

- `npm.cmd run build`

## TF-F027: Clarify Price Versus Fundamentals Provider Controls In Context Rail

**Status:** Done

**Classification:** bug

**Milestone:** TBD

**Branch:** `fix/tf-f027-provider-capability-rail-clarity`

**Affected Layer:** frontend

**Linked ADRs:** ADR-0038

**Impacted Invariants:** UX Is Architectural, Derived State Must Remain Distinguishable

**Source:** Operator observation captured on 2026-05-17 in `knowledge/raw/brainstorm-20260517-provider-capability-rail-clarity.md`.

**Problem:**
The Opportunity and Active Position context rail places a price-only `Market Context` loader directly above a provider configuration panel that only exposes the `fundamentals` capability. Because the rail does not show the `price` capability at all, changing the visible fundamentals provider makes the adjacent `Load` action appear as though it should stop using `yfinance`, even though that button correctly calls the separate price-data path.

**Acceptance Criteria:**

- The provider configuration panel visibly distinguishes `price` and `fundamentals` capabilities.
- The `Market Context` loader remains clearly attributable to the selected `price` provider.
- Fundamentals configuration remains editable without implying it controls price-data requests.
- Price and fundamentals contracts remain separate; no provider-boundary semantics change.

**Out Of Scope:**

- Reworking the market snapshot service into dynamic multi-provider routing.
- Moving fundamentals overlays into new workspaces.
- Changing provider rollout doctrine or fallback semantics.

**Resolution Summary:**
Expanded the context-rail provider panel to surface both `price` and `fundamentals` capability resolution. The fundamentals selector remains editable, while the rail now also shows which price provider the adjacent market-context loader is using so the two external-data paths are no longer visually conflated.

**Completed Verification:**

- `npm.cmd run typecheck`
- `npm.cmd run build`

**Regression Note:**

- `uv run pytest` could not complete in the current local environment because the rotated `TRADEFORGE_MASTER_KEY` no longer decrypts the existing `.keys.enc`, causing app import to fail during test collection before this frontend change is exercised.

## TF-F026: Forward Master Key Into Docker Runtime Container

**Status:** Done

**Classification:** bug

**Milestone:** TBD

**Branch:** `fix/tf-f026-compose-master-key-forwarding`

**Affected Layer:** infrastructure

**Linked ADRs:** ADR-0037

**Impacted Invariants:** Architectural Simplicity

**Source:** Operator startup failure captured on 2026-05-17 in `knowledge/raw/brainstorm-20260517-compose-master-key-forwarding.md`.

**Problem:**
When TradeForge is started through Docker Compose with credentialed providers configured, the `tradeforge` container exits with `MasterKeyNotConfiguredError` even when PowerShell shows `TRADEFORGE_MASTER_KEY` in the host session. The Compose service definition forwards `TRADEFORGE_DATABASE_URL` but does not forward `TRADEFORGE_MASTER_KEY`, so the runtime container cannot see the credential boundary entry point required by ADR-0037.

**Acceptance Criteria:**

- `docker-compose.yml` explicitly passes `TRADEFORGE_MASTER_KEY` into the `tradeforge` service.
- Compose fails fast with a clear configuration error when the host shell does not provide `TRADEFORGE_MASTER_KEY`.
- Operator documentation explains that Docker Compose requires the key in the shell that launches the stack.
- No credential semantics, storage model, or provider adapter boundaries change.

**Out Of Scope:**

- Introducing `.env` support for secrets.
- Changing credential encryption or storage behavior.
- Persisting provider-selection preferences.

**Resolution Summary:**
Forwarded `TRADEFORGE_MASTER_KEY` from the host environment into the runtime container through Compose interpolation and added a required-variable guard so missing configuration is detected before the app starts. Updated the credential setup guide to call out the Compose-specific requirement.

**Completed Verification:**

- `docker compose config` with `TRADEFORGE_MASTER_KEY` set
- Manual inspection of the rendered service environment confirms the runtime container receives the key
- `docker compose config` without `TRADEFORGE_MASTER_KEY` now fails before startup with a clear missing-variable message
- `uv run pytest`
- `npm.cmd run typecheck`
- `npm.cmd run build`

## TF-F025: Gate Frontend Workspace Loading When Runtime API Is Unavailable

**Status:** Done

**Classification:** bug

**Milestone:** TBD

**Branch:** `fix/tf-f025-runtime-unavailable-gate`

**Affected Layer:** frontend

**Linked ADRs:** none

**Impacted Invariants:** UX Is Architectural, Architectural Simplicity

**Source:** Frontend startup failure captured on 2026-05-16 in `knowledge/raw/20260516 feed back Bug.md`.

**Problem:**
When the frontend starts while the runtime API is unavailable on port `8000`, the application still mounts the full workspace graph and immediately issues multiple dependent API requests. The Vite proxy then emits repeated failures for `/health`, `/session`, `/workspaces/*`, and `/lifecycle/decisions`, leaving the operator with a scattered degraded state instead of one clear runtime-unavailable boundary.

**Acceptance Criteria:**

- Runtime availability is checked before workspace, context rail, and sidebar data fetches are allowed to mount.
- When the runtime API is unavailable, the frontend shows one explicit runtime-unavailable state instead of loading operational surfaces.
- Once the runtime API is available, normal workspace rendering proceeds without changing lifecycle or event semantics.
- Frontend regression coverage proves the unavailable and available states.

**Out Of Scope:**

- Changing backend startup behavior.
- Replacing the existing two-terminal local development workflow.
- Adding automatic backend process management from the frontend.

**Resolution Summary:**
Lifted runtime health into `App`, gated the session/workspace tree until `/health` succeeds, and added a single runtime-unavailable surface so an absent API no longer mounts the full operational workspace graph.

**Completed Verification:**

- Reproduced the source condition with frontend port `5173` available and runtime port `8000` unavailable.
- `npm.cmd run build`
- `uv run pytest`

**Residual Gap:**

- The frontend does not yet have a dedicated component-test harness; this issue is closed with build verification and direct scenario validation rather than automated UI regression coverage.


## TF-F024: Fix Documented Credential Setup Command Import Failure

**Status:** Done

**Classification:** bug

**Milestone:** TBD

**Branch:** `fix/tf-f024-credential-script-import-path`

**Affected Layer:** operational, scripts

**Linked ADRs:** ADR-0037

**Impacted Invariants:** Architectural Simplicity

**Source:** Operator credential-setup failure captured on 2026-05-16 in `knowledge/raw/brainstorm-20260516-credential-setup-import-failure.md`.

**Problem:**
The documented command `uv run python scripts\manage_credentials.py generate-master-key` fails from the repository root with `ModuleNotFoundError: No module named 'src'`. The credential setup guide therefore cannot be followed verbatim even though the script itself is present and the credential boundary depends on it for first-run setup.

**Acceptance Criteria:**

- The documented direct script command works from the repository root.
- Credential registration command remains functional through the same documented invocation style.
- Regression coverage executes the documented script path rather than only importing internal functions.
- `HOW-TO-SETUP-KEYS.md` remains accurate after the fix.

**Out Of Scope:**

- Redesigning credential management into a new CLI surface.
- Durable provider preference persistence.
- Any credential model changes.

**Resolution Summary:**
Added a direct-execution path bootstrap to `scripts/manage_credentials.py` so the documented command works from the repository root, and added subprocess regression tests covering the documented master-key and registration invocations.

**Completed Verification:**

- `uv run pytest tests\test_manage_credentials_script.py tests\test_credential.py tests\test_key_manager.py tests\test_credential_store.py`
- `uv run ruff check scripts\manage_credentials.py tests\test_manage_credentials_script.py`
- `uv run python scripts\manage_credentials.py generate-master-key`

---

## TF-F016: Capture Provider Capability Gap And Define M10D Architecture

**Status:** Done

**Classification:** architectural

**Milestone:** M10D

**Branch:** `docs/tf-f016-provider-capability-gap`

**Affected Layer:** docs, domain

**Linked ADRs:** ADR-0010, ADR-0032, ADR-0038

**Impacted Invariants:** Market Intelligence Is Interpreted Context, Derived State Must Remain Distinguishable, Architectural Simplicity, Replayability Is Foundational

**Source:** Field-observed provider-layer gap identified after M10C credential work and before M11 AI advisory preparation.

**Problem:**
The runtime now centralizes provider credentials, but the provider model is still flattened around the M9 OHLCV snapshot path. Credential setup already names providers with materially different capabilities, while the runtime still treats "provider" as if it primarily meant "price feed." That leaves future fundamentals work and M11 AI advisory work without a stable architectural statement of provider identity versus provider capability.

**Acceptance Criteria:**

- A raw knowledge-base brainstorm note captures the provider-capability gap without promoting it to canonical truth.
- `M10D` exists in the runtime roadmap before `M11`.
- `ADR-0038` is accepted.
- Runtime docs explicitly distinguish provider identity from provider capability.
- Runtime docs explain why the current OHLCV-only abstraction is insufficient for planned providers.

**Out Of Scope:**

- Runtime implementation of provider registry behavior.
- Fundamentals provider adapters.
- Workspace overlays beyond documentation of future scope.

**Resolution Summary:**
Captured the field-observed provider-capability gap as a raw KB brainstorm note, added `M10D` to the runtime roadmap before `M11`, accepted `ADR-0038`, and created the follow-on `M10D` issue set so later implementation work can proceed through explicit tracked scope.

**Completed Verification:**

- Confirmed the raw brainstorm note exists under the knowledge-base `knowledge/raw/` directory.
- Confirmed `M10D` appears before `M11` in `DOCS/Milestone_Roadmap_v2.md`.
- Confirmed `ADR-0038` exists under `DOCS/adr/`.
- Confirmed future M10D issues `TF-F017` through `TF-F023` are registered with bounded dependencies and acceptance criteria.

---

## TF-F017: Introduce Provider Registry And Capability Metadata Model

**Status:** Planned

**Classification:** architectural/enhancement

**Milestone:** M10D

**Branch:** `feature/tf-f017-provider-registry-capabilities`

**Affected Layer:** domain, services, app

**Linked ADRs:** ADR-0038

**Depends On:** TF-F016

**Acceptance Criteria:**

- A provider registry contract exists.
- Providers declare supported capabilities.
- The registry can resolve configured providers by capability through deterministic preferred-plus-ordered-fallback resolution.
- A global preferred provider and ordered fallback sequence per capability are modeled.
- The registry remains separate from credential storage.
- Resolution results are explicit enough to preserve advisory replay context without becoming canonical ledger truth.
- Tests prove registry behavior without external API calls.

**Resolution Summary:** Added capability descriptors, deterministic preferred-plus-fallback resolution, and a composition-time provider registry separate from credential storage.

---

## TF-F018: Split External Data Access Into Typed Capability Contracts

**Status:** Planned

**Classification:** refactor

**Milestone:** M10D

**Branch:** `feature/tf-f018-typed-external-data-contracts`

**Affected Layer:** domain, services, infrastructure

**Linked ADRs:** ADR-0032, ADR-0038

**Depends On:** TF-F017

**Acceptance Criteria:**

- The existing price path is represented by a typed price contract rather than the generic provider concept alone.
- A distinct fundamentals contract exists for company profile, statements, and ratios.
- Current price adapters remain functional through the new design.
- No provider-specific SDK shapes leak into services or workspace layers.
- Provenance requirements remain explicit across both contract families.

**Resolution Summary:** Preserved the existing normalized price contract while introducing a distinct fundamentals provider contract and normalized fundamentals artifacts.

---

## TF-F019: Add Fundamentals Data Model And Normalization Boundary

**Status:** Planned

**Classification:** feature

**Milestone:** M10D

**Branch:** `feature/tf-f019-fundamentals-normalization-boundary`

**Affected Layer:** domain, services

**Linked ADRs:** ADR-0010, ADR-0038

**Depends On:** TF-F018

**Acceptance Criteria:**

- Normalized advisory models exist for company profile, financial statements, and ratios.
- Each artifact carries provider provenance and `data_as_of`.
- Artifacts remain non-canonical and distinguishable from event-ledger truth.
- Validation and test fixtures cover incomplete or unavailable fundamentals data.

**Resolution Summary:** Added advisory fundamentals value objects for company profile, financial statements, ratios, and bundle-level provenance.

---

## TF-F020: Implement Initial Fundamentals Provider Adapters

**Status:** Planned

**Classification:** feature

**Milestone:** M10D

**Branch:** `feature/tf-f020-fundamentals-provider-adapters`

**Affected Layer:** infrastructure

**Linked ADRs:** ADR-0038

**Depends On:** TF-F019

**Rollout Doctrine:** Start with `fmp` as the primary fundamentals provider and `alpha_vantage` as the fallback provider so normalization discipline and capability divergence are tested early without widening initial complexity.

**Selection Principle:** Initial provider selection optimizes for architectural capability validation rather than long-term provider finality.

**Acceptance Criteria:**

- `fmp` and `alpha_vantage` implement the fundamentals contract.
- Adapters are credential-store compatible through the existing composition boundary.
- Adapters normalize provider-specific shapes into the shared fundamentals model.
- Mocked tests cover success, empty response, malformed response, and provider unavailability.

**Resolution Summary:** Added first-rollout `fmp` and `alpha_vantage` adapters with provider-specific normalization and mocked failure coverage.

---

## TF-F021: Expose Capability-Aware Provider Configuration And Transparency

**Status:** Planned

**Classification:** feature

**Milestone:** M10D

**Branch:** `feature/tf-f021-provider-capability-transparency`

**Affected Layer:** app, frontend

**Linked ADRs:** ADR-0038

**Depends On:** TF-F017, TF-F018

**Acceptance Criteria:**

- Runtime exposes configured providers and supported capabilities.
- Global preferred provider and ordered fallback sequence per capability are inspectable.
- Operator-facing configuration is editable and visible.
- UI surfaces provider provenance for both price and fundamentals data.
- UI communicates which provider is serving which capability, why it was selected, and whether a fallback or degraded-capability state is in effect.
- No UI flow implies external data is canonical truth.

**Out Of Scope:**

- Provider health/status management beyond visible degraded-capability state.

**Resolution Summary:** Added provider configuration inspection/update endpoints and a frontend configuration panel showing capability ownership, selected provider, and fallback order.

---

## TF-F022: Extend Workspace Context With Fundamentals Overlays

**Status:** Planned

**Classification:** feature

**Milestone:** M10D

**Branch:** `feature/tf-f022-fundamentals-workspace-overlays`

**Affected Layer:** services, app, frontend

**Linked ADRs:** ADR-0010, ADR-0038

**Depends On:** TF-F019, TF-F020, TF-F021

**Acceptance Criteria:**

- Relevant workspaces can request and render advisory fundamentals context.
- Initial fundamentals overlays appear in Opportunity and Thesis flows, not Plan flows.
- Fundamentals context remains separate from price context.
- Partial provider failures degrade explicitly rather than silently.
- Contextual summaries can consume typed fundamentals outputs without blurring authority boundaries.

**Resolution Summary:** Added advisory fundamentals overlays to Opportunity and Thesis flows while keeping them separate from price context and plan-stage authoring.

---

## TF-F023: M10D Verification And M11 Readiness Gate

**Status:** Planned

**Classification:** verification

**Milestone:** M10D

**Branch:** `docs/tf-f023-m10d-readiness-gate`

**Affected Layer:** docs, tests

**Linked ADRs:** ADR-0038

**Depends On:** TF-F016 through TF-F022

**Acceptance Criteria:**

- Documentation states the external data architecture `M11` may rely on.
- Regression tests cover registry resolution, price flow, fundamentals flow, provenance, and UI transparency.
- A checklist confirms AI advisory work no longer needs to infer provider semantics from the old OHLCV-only model.
- `M11` dependency notes reference completed `M10D`.

**Resolution Summary:** Added focused regression coverage for registry resolution, fundamentals normalization, adapter behavior, overlay APIs, and existing price-flow non-regression; roadmap dependency notes already point `M11` at completed `M10D`.

## TF-F012: Replace Centered Workspace Shell With Workstation-Oriented Operational Layout Model

**Status:** Done

**Classification:** enhancement

**Milestone:** TBD

**Branch:** `feature/tf-f012-workstation-layout-model`

**Affected Layer:** frontend

**Linked ADRs:** none currently required

**Impacted Invariants:** UX Is Architectural, Workspaces Are Operational Environments, Human Decision Sovereignty

**Source:** Screen real-estate feedback, 2026-05-16. `knowledge/raw/2026-05-16 feed back on screen real estate and design.md`; screenshot: `knowledge/raw/feedback on screen realestate Screenshot 2026-05-16 120442.png`.

**Problem:**
The current desktop workspace experience still behaves like a centered application shell rather than a workstation-oriented operational surface. The UI underuses available horizontal space, compresses active operational state into vertically stacked sections, and lacks a persistent contextual awareness region despite TradeForge doctrine favoring parallel cognition, continuity of context, and workspace-specific operational surfaces.

**Acceptance Criteria:**

- Operational desktop workspaces are no longer constrained by a centered document-style shell by default.
- A desktop three-zone composition model exists for operational workspaces: navigation, primary operational surface, contextual awareness rail.
- The Operating Workspace is converted first as the reference implementation.
- Canonical operational state remains visually distinct from advisory/contextual state.
- Narrow viewport behavior degrades safely without redefining the desktop workstation model.

**Out Of Scope:**

- Resizable panels.
- Detachable panels.
- Multi-monitor support.
- Full redesign of every workspace in one bounded change.

**Resolution Summary:**
Updated the frontend operational shell to use available desktop width, introduced an optional contextual awareness rail in the shared workspace layout primitive, and converted the Operating Workspace into the first three-zone workstation reference surface.

**Completed Verification:**

- `npm.cmd run typecheck`
- `npm.cmd run build`

---

## TF-F013: Formalize Three-Layer Design Architecture Between Doctrine, Workspace Composition, And Frontend Translation

**Status:** Done

**Classification:** doctrine

**Milestone:** TBD

**Branch:** `docs/tf-f013-three-layer-design-architecture`

**Affected Layer:** docs, design-doctrine

**Linked ADRs:** none currently required

**Impacted Invariants:** UX Is Architectural, Terminology Stability, Architectural Simplicity

**Source:** Design-boundary clarification notes, 2026-05-15 to 2026-05-16. `knowledge/raw/20260515-frontend-design-md-role-and-usage.md`; `knowledge/raw/recomnended section addition to 20260515-frontend-design-md-role-and-usage.md`; related drafts under `design/`.

**Problem:**
TradeForge now has an emergent three-layer design model, but the documentation boundary has not yet been normalized around it. The existing explanatory material still partially describes only design doctrine and frontend implementation translation, leaving the operational workspace architecture layer under-specified and creating room for future frontend drift.

**Acceptance Criteria:**

- The design documentation explicitly distinguishes cognitive doctrine, operational workspace architecture, and frontend implementation translation.
- Frontend translation is explicitly documented as non-authoritative over workspace meaning and operational composition doctrine.
- The relationship among `design/DESIGN_ARCHITECTURE.md`, the workspace-layout draft documents, and `frontend/DESIGN.md` is made explicit.
- The issue resolves the documentation gap without prematurely canonicalizing draft design artifacts.

**Out Of Scope:**

- Runtime frontend code changes.
- Immediate canonical promotion of all draft design documents.
- Broad rewrite of UX doctrine.

**Resolution Summary:**
Updated the frontend design-role note to document the three-layer design model explicitly and clarify that frontend implementation translates operational workspace architecture rather than owning it.

---

## TF-F014: Extend Workstation Zoning To Remaining Market-Context Workspaces

**Status:** Done

**Classification:** enhancement

**Milestone:** TBD

**Branch:** `feature/tf-f014-remaining-workspace-zoning`

**Affected Layer:** frontend

**Linked ADRs:** none currently required

**Impacted Invariants:** UX Is Architectural, Workspaces Are Operational Environments

**Source:** Post-`TF-F012` reassessment, 2026-05-16. `knowledge/processed/20260516-tf-f012-synthesis.md`; `knowledge/raw/20260516-tf-f014-diagnosis.md`.

**Problem:**
After the Operating Workspace became the first three-zone reference implementation, the remaining market-context workspaces still keep contextual panels inline with primary workflow content. `OpportunityWorkspace` and `ActivePositionWorkspace` now require a separate bounded follow-on pass to adopt workstation zoning without widening the completed `TF-F012` issue.

**Acceptance Criteria:**

- Remaining workspaces with persistent contextual market content are evaluated explicitly for right-rail adoption.
- Appropriate contextual panels move out of the primary workflow flow where that improves operational continuity.
- Workspace-specific composition differences are preserved instead of forcing identical layouts.
- The change remains bounded to layout composition, not lifecycle or event semantics.

**Resolution Summary:**
Moved persistent market context for the Opportunity and Active Position workspaces into the shared shell-level contextual rail while preserving their distinct primary workflow surfaces.

**Completed Verification:**

- `npm.cmd run typecheck`
- `npm.cmd run build`

---

## TF-F015: Fix Missing Return Path In Operational Attention Decision Spec

**Status:** Done

**Classification:** bug

**Milestone:** TBD

**Branch:** `fix/tf-f015-operational-attention-mypy-return`

**Affected Layer:** services

**Linked ADRs:** none currently required

**Impacted Invariants:** Deterministic Rule Evaluation, Architectural Simplicity

**Source:** Focused type-check verification during TF-F006 on 2026-05-16. `uv run mypy src\services\workspace_engine\attention.py` reports `src\services\workspace_engine\attention.py:291: error: Missing return statement [return]`.

**Problem:**
`_decision_item_spec()` in `src/services/workspace_engine/attention.py` declares a return type of `tuple[...] | None`, but the current `match` statement does not make the fallback return path explicit. The code currently fails strict mypy verification even though runtime behavior may be operationally unchanged for known lifecycle stages.

**Acceptance Criteria:**

- `_decision_item_spec()` has an explicit fallback return path that satisfies its declared `tuple[...] | None` contract.
- `uv run mypy src\services\workspace_engine\attention.py` passes.
- Existing operational attention queue behavior remains unchanged for all currently supported lifecycle stages.
- Focused regression coverage is added or updated if the implementation changes an observable code path.

**Out Of Scope:**

- Broader refactoring of the operational attention queue.
- Changes to lifecycle semantics, workspace routing, or attention prioritization.

**Resolution Summary:**
Added an explicit fallback `None` return path to `_decision_item_spec()` so the services-layer operational attention decision spec satisfies its declared nullable tuple contract. Supported lifecycle-stage behavior remains unchanged; the fallback only makes the fail-closed path explicit for type checking.

**Completed Verification:**

- `uv run mypy src\services\workspace_engine\attention.py`
- `uv run pytest tests\test_operational_attention_queues.py`
- `uv run ruff check src\services\workspace_engine\attention.py tests\test_operational_attention_queues.py`
- `uv run pytest` (692 passed; local `.keys.enc` temporarily hidden during test process and restored)
- `npm.cmd run typecheck` from `frontend\`
- `npm.cmd run build` from `frontend\`

---

Explicit roadmap checkpoint completed M9 Updated*Done*.
M10A COMPLETE 2026-05-14. All 15 issues done: M10AIS01-15.
TF-F001, TF-F002, TF-F003 — Post-M10A feedback issues from first operational walkthrough (2026-05-14). TF-F#### series = field-observed / feedback-originated issues, distinct from roadmap TF-#### series. Milestone TBD.
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

## TF-0065: Define AI Advisory Interfaces

**Status:** Planned

**Milestone:** M11

**Branch:** `feature/tf-0065-ai-advisory-interfaces`

**Affected Layer:** domain, services

**Linked ADRs:** ADR-0006

**Impacted Invariants:** Human Decision Sovereignty, AI Advisory Boundary, Derived State Must Remain Distinguishable, Lifecycle Authority, Replayability Is Foundational, Architectural Simplicity

**Problem:**
M11 introduces AI assistance, but the runtime does not yet expose a stable advisory contract that future AI implementations can target without leaking provider concerns into domain logic or creating hidden authority. Without explicit interfaces, later replay summarization, review assistance, and provenance work could drift into ad hoc service shapes or blur the distinction between advisory output and canonical workflow state.

**Acceptance Criteria:**

- A runtime AI advisory boundary exists as explicit interfaces/contracts separate from lifecycle authority and event persistence.
- Advisory requests and responses are modeled as non-canonical artifacts with explicit provenance and uncertainty fields.
- Advisory interfaces cannot append events, approve lifecycle transitions, or mutate canonical workflow state.
- The boundary is provider-agnostic so future LLM adapters can implement it without leaking provider concerns into domain logic.
- Tests prove advisory outputs remain distinguishable from canonical, derived, and inferred state.
- Relevant runtime documentation is updated so later M11 issues can build against a stable contract.

**Out Of Scope:**

- Concrete LLM provider adapters.
- Replay summarization assistance.
- Review assistance.
- Advisory provenance storage or query endpoints.

**Resolution Summary:**
Added the first M11 AI advisory boundary as provider-agnostic domain contracts and an orchestration-only advisory service. Advisory requests and responses are immutable non-canonical artifacts with explicit source references, provenance, uncertainty, and advisory authority. The service validates provider responses without importing event-store, lifecycle, persistence, broker, or app authority.

**Completed Verification:**

- `uv run pytest tests\test_ai_advisory_interfaces.py`
- `uv run ruff check src\domain\advisory src\services\advisory tests\test_ai_advisory_interfaces.py`
- `uv run mypy src\domain\advisory src\services\advisory tests\test_ai_advisory_interfaces.py`
- `uv run pytest` (699 passed; local `.keys.enc` temporarily hidden during test process and restored)
- M11 closeout: `uv run pytest` (704 passed; local `.keys.enc` temporarily hidden during test process and restored)
- M11 closeout: `npm.cmd run typecheck` from `frontend\`
- M11 closeout: `npm.cmd run build` from `frontend\`

---

## TF-0066: Implement Replay Summarization Assistance

**Status:** Done

**Milestone:** M11

**Branch:** `feature/m11-ai-advisory-boundary`

**Affected Layer:** services, domain

**Linked ADRs:** ADR-0006, ADR-0008

**Impacted Invariants:** AI Advisory Boundary, Replayability Is Foundational, Derived State Must Remain Distinguishable, Human Decision Sovereignty, Lifecycle Authority

**Depends On:** TF-0065

**Problem:**
M11 needs AI-assisted replay summarization, but replay must remain deterministic historical reconstruction over canonical events. Without a bounded replay advisory service, later summarization work could accidentally depend on live mutable state, hide source events, or blur generated summaries with replay truth.

**Acceptance Criteria:**

- A replay advisory service can build an `AdvisoryRequest` from a replay timeline or reconstruction without writing events.
- Replay advisory requests include source references to replay timeline entries or source events.
- Replay summaries are returned as advisory artifacts through the TF-0065 contract.
- The service has no lifecycle authority, event-store append path, broker dependency, or persistence responsibility.
- Tests prove replay summaries remain advisory and source-linked.

**Out Of Scope:**

- Concrete LLM provider adapters.
- Persisting advisory summaries.
- API endpoints or frontend replay UI changes.
- Changing replay timeline semantics.

**Resolution Summary:**
Added `ReplayAdvisoryService`, which turns existing `ReplayTimeline` entries into source-linked `AdvisoryRequest` values and delegates generation through the TF-0065 advisory boundary. Replay summaries remain non-canonical advisory responses with no event-store, lifecycle, persistence, API, frontend, or concrete LLM dependency.

**Completed Verification:**

- `uv run pytest tests\test_replay_advisory_service.py tests\test_ai_advisory_interfaces.py`
- `uv run ruff check src\domain\advisory src\services\advisory tests\test_ai_advisory_interfaces.py tests\test_replay_advisory_service.py`
- `uv run mypy src\domain\advisory src\services\advisory tests\test_ai_advisory_interfaces.py tests\test_replay_advisory_service.py`
- M11 closeout: `uv run pytest` (704 passed; local `.keys.enc` temporarily hidden during test process and restored)
- M11 closeout: `npm.cmd run typecheck` from `frontend\`
- M11 closeout: `npm.cmd run build` from `frontend\`

---

## TF-0067: Implement Review Assistance

**Status:** Done

**Milestone:** M11

**Branch:** `feature/m11-ai-advisory-boundary`

**Affected Layer:** services, domain

**Linked ADRs:** ADR-0006

**Impacted Invariants:** AI Advisory Boundary, Reflection And Review Are First-Class, Human Decision Sovereignty, Derived State Must Remain Distinguishable, Lifecycle Authority

**Depends On:** TF-0065

**Problem:**
Review assistance should help operators interpret completed decisions and reflection artifacts without becoming the review authority. Without a bounded review advisory service, AI review output could be confused with canonical review events or behavioral truth.

**Acceptance Criteria:**

- A review advisory service can build an advisory request from review artifacts and operator review questions.
- Review advisory outputs remain non-canonical `AdvisoryResponse` artifacts with provenance and uncertainty.
- The service cannot complete reviews, mutate review artifacts, append events, or change lifecycle state.
- Tests prove review assistance is source-linked and advisory-only.

**Out Of Scope:**

- Concrete LLM provider adapters.
- Behavioral intelligence or discipline scoring.
- Persisting advisory review output.
- API endpoints or frontend review UI changes.

**Resolution Summary:**
Added `ReviewAdvisoryService`, which turns structured `ReviewReflectionArtifact` values into source-linked `AdvisoryRequest` values and delegates generation through the TF-0065 advisory boundary. Review assistance remains non-canonical and cannot complete reviews, mutate review artifacts, append events, or change lifecycle state.

**Completed Verification:**

- `uv run pytest tests\test_review_advisory_service.py tests\test_replay_advisory_service.py tests\test_ai_advisory_interfaces.py`
- `uv run ruff check src\domain\advisory src\services\advisory tests\test_ai_advisory_interfaces.py tests\test_replay_advisory_service.py tests\test_review_advisory_service.py`
- `uv run mypy src\domain\advisory src\services\advisory tests\test_ai_advisory_interfaces.py tests\test_replay_advisory_service.py tests\test_review_advisory_service.py`
- M11 closeout: `uv run pytest` (704 passed; local `.keys.enc` temporarily hidden during test process and restored)
- M11 closeout: `npm.cmd run typecheck` from `frontend\`
- M11 closeout: `npm.cmd run build` from `frontend\`

---

## TF-0068: Implement Advisory Provenance Tracking

**Status:** Done

**Milestone:** M11

**Branch:** `feature/m11-ai-advisory-boundary`

**Affected Layer:** domain, services, infrastructure

**Linked ADRs:** ADR-0006

**Impacted Invariants:** AI Advisory Boundary, Historical Integrity, Replayability Is Foundational, Derived State Must Remain Distinguishable, Event Ledger Canonical Truth

**Depends On:** TF-0065, TF-0066, TF-0067

**Problem:**
AI advisory outputs must be reviewable and historically explainable. The runtime has an advisory response contract, but no provenance tracking port or storage adapter for preserving generated advisory artifacts outside the canonical event ledger.

**Acceptance Criteria:**

- An advisory provenance store port exists for recording and querying advisory responses.
- A non-canonical in-memory advisory provenance adapter exists for tests and local runtime composition.
- Provenance records preserve request identity, artifact kind, provider/model provenance, uncertainty, source references, and generated content.
- Provenance tracking does not append canonical events or mutate lifecycle state.
- Tests prove advisory provenance is distinguishable from event-ledger truth and queryable by request, artifact kind, and source reference.

**Out Of Scope:**

- Postgres advisory provenance persistence.
- User-facing advisory provenance APIs or frontend surfaces.
- Treating advisory records as canonical events.

**Resolution Summary:**
Added `AdvisoryProvenanceRecord`, an `AdvisoryProvenanceStore` port, a process-local `InMemoryAdvisoryProvenanceStore`, and `AdvisoryProvenanceService`. Advisory records preserve request identity, artifact kind, provider/model provenance, uncertainty, source references, content, and recording time without appending canonical events or mutating lifecycle state.

**Completed Verification:**

- `uv run pytest tests\test_advisory_provenance.py tests\test_review_advisory_service.py tests\test_replay_advisory_service.py tests\test_ai_advisory_interfaces.py`
- `uv run ruff check src\domain\advisory src\services\advisory src\infrastructure\advisory tests\test_ai_advisory_interfaces.py tests\test_replay_advisory_service.py tests\test_review_advisory_service.py tests\test_advisory_provenance.py`
- `uv run mypy src\domain\advisory src\services\advisory src\infrastructure\advisory tests\test_ai_advisory_interfaces.py tests\test_replay_advisory_service.py tests\test_review_advisory_service.py tests\test_advisory_provenance.py`
- M11 closeout: `uv run pytest` (704 passed; local `.keys.enc` temporarily hidden during test process and restored)
- M11 closeout: `npm.cmd run typecheck` from `frontend\`
- M11 closeout: `npm.cmd run build` from `frontend\`

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

## M10AIS13: Implement Replay Annotation System

**Status:** Done

**Milestone:** M10A

**Branch:** `feature/tf-0064-operational-attention-continuity`

**Affected Layer:** domain, api, frontend

**Linked ADRs:** ADR-0033, ADR-0035

**Impacted Invariants:** Replayability Is Foundational, Events Are Immutable, Reflection And Review Are First-Class

**Implementation Summary:** Created `src/domain/cognition/annotation.py` with `ReplayAnnotationArtifact` and `AnnotationType` StrEnum (`observation`, `question`, `insight`, `postmortem`). Validates sequence >= 0, annotated_event_type, note (required), and annotation_type (enum check). `decision.replay_annotation_created` events are appended directly (not lifecycle transitions); they appear in the replay timeline as `COGNITION` kind (covered by the EventDomain.DECISION → COGNITION mapping from M10AIS04). Added `POST /lifecycle/decisions/create-annotation` (validates fields, checks decision exists, appends annotation event) and `GET /lifecycle/decisions/{id}/annotations` (all annotations chronologically, filterable by sequence on frontend). 18 new tests (647 total). Created `AnnotationModal.tsx` with annotation_type select (Observation/Question/Insight/Postmortem with descriptions), note textarea, and `postCreateAnnotation()` call. Updated `ReplayWorkspace.tsx`: `annotationList` state fetched alongside cognitive snapshot on load; `annotatingEntry` state tracks which entry's modal is open; `AnnotationBadge` subcomponent shows type tag and note text beneath annotated entries; `TimelineEntryRow` gains `annotations` and `onAnnotate` props — "+ Note" button appears on every entry (stopPropagation prevents triggering the cognitive snapshot click); `AnnotationModal` rendered when `annotatingEntry` is set; re-fetches annotations after successful creation. Added `AnnotationType`, `Annotation`, `AnnotationList`, `postCreateAnnotation()`, `fetchAnnotations()` to runtime.ts.

**Acceptance Criteria:**

- Replay becomes cognitively interactive.

**Completed Verification:**

- `uv run pytest` — 647 passed (18 new tests: 9 unit + 9 integration)
- `npm.cmd run typecheck` — clean
- `npm.cmd run build` — clean (328.37 kB JS, 30.79 kB CSS)

---

## TF-F001: Add Iterative Revision Workflow For Thesis, Plan, And Assumptions

**Status:** Done

**Classification:** enhancement

**Milestone:** TBD

**Branch:** `feature/tf-f001-iterative-revision-workflow`

**Affected Layer:** domain, api, frontend

**Linked ADRs:** TBD

**Impacted Invariants:** Decision Lifecycle, Replayability Is Foundational, Human Decision Sovereignty

**Source:** First operational walkthrough — M10A, 2026-05-14. `knowledge/raw/first testing feedback 20260514.md` — Operational Gaps #1.

**Problem:**
The current workflow supports forward progression only. Once a thesis or plan is authored, there is no operational mechanism to revise thesis narrative or conviction, revise assumptions, revise invalidation conditions, revise plan rationale (entry, stop, target, sizing), or return to a prior cognitive stage after advisory review.

During the SMH walkthrough, the advisory system surfaced items requiring reconsideration (only 1 invalidation condition, only 1 execution assumption), but there was no revision path — only "proceed anyway" or abandon.

**Acceptance Criteria:**

- Operator can re-enter thesis authoring from the plan stage.
- Operator can re-enter plan authoring from the review stage.
- Revision history is preserved as replayable events — not silent overwrites.
- Advisory items link directly to the revision entry point.

---

## TF-F002: Introduce Conditional Execution State Between Approval And Execution

**Status:** Done

**Classification:** architectural

**Milestone:** TBD

**Branch:** `feature/tf-f002-awaiting-trigger-lifecycle-state`

**Affected Layer:** domain, api, frontend

**Linked ADRs:** TBD

**Impacted Invariants:** Decision Lifecycle, Lifecycle Authority, Replayability Is Foundational

**Source:** First operational walkthrough — M10A, 2026-05-14. `knowledge/raw/first testing feedback 20260514.md` — Operational Gaps #2.

**Problem:**
In real discretionary swing trading, approval often means "if conditions occur, I am prepared to execute" — not "I have already entered the trade." The SMH plan explicitly required a daily close above 585, rising volume, and continued semiconductor breadth participation before entry. The current lifecycle collapses Approval → Execution → Position too aggressively for condition-dependent entries.

**Missing Lifecycle Concept:**
Candidate names: Awaiting Trigger, Authorized Watch State, Conditional Execution State, Armed Opportunity.

Proposed canonical lifecycle extension:
```
Idea → Thesis → Plan → Approval → [Awaiting Trigger] → Execution → Position → Review
```

**Acceptance Criteria:**

- A lifecycle state exists between Approval and Execution representing conditional authorization.
- Operator can declare trigger conditions when entering the armed state.
- The system holds the plan in the armed state until the operator confirms conditions are met.
- The trigger confirmation is a replayable lifecycle event.
- The armed state is visible in the workspace with its declared trigger conditions.

---

## TF-F003: Expand Cognition Input Areas From CRUD-Form Style To Thinking-Space UX

**Status:** Done

**Classification:** enhancement

**Milestone:** TBD

**Branch:** `feature/tf-f003-cognition-ux-ergonomics`

**Affected Layer:** frontend

**Linked ADRs:** TBD

**Impacted Invariants:** UX Is Architectural, Human Decision Sovereignty

**Source:** First operational walkthrough — M10A, 2026-05-14. `knowledge/raw/first testing feedback 20260514.md` — Operational Gaps #3. Screenshot: `feedback Screenshot 2026-05-14 230304.png`.

**Problem:**
The current plan authoring form uses small textarea-style inputs that feel like CRUD forms and configuration panels rather than operational cognition environments. Entry Rationale, Stop Rationale, Target Rationale, Sizing Rationale, and Execution Assumptions fields are psychologically compressed for the level of discretionary reasoning being captured.

**Acceptance Criteria:**

- Rationale input fields have a significantly larger default height.
- Thesis narrative has a full-panel or expandable composing area.
- Visual treatment signals "compose and think" rather than "fill in a form."
- Changes are consistent with the structured cognition authoring philosophy and do not regress workflow functionality.

---

## TF-F004: Define Operational Credential Boundary — ADR And Credential Domain Model

**Status:** Done

**Classification:** architectural

**Milestone:** M10C

**Branch:** `feature/tf-f004-credential-boundary-design`

**Affected Layer:** security, domain, docs

**Linked ADRs:** ADR-0037

**Impacted Invariants:** Replayability Is Foundational, Architectural Simplicity, Historical Integrity

**Source:** Field-observed gap — no encrypted credential management exists for external provider API keys (Polygon, Alpaca, and planned: Alpha Vantage, FinancialModelingPrep, Finqual, LLM providers).

**Problem:**
Provider adapter API keys are currently accepted as constructor parameters with no secure storage, rotation, revocation, or barrier preventing keys from appearing in logs or version control. As provider count grows this becomes unmanageable. The gap also affects replay fidelity — credential status at historical points is operationally meaningful context.

**Acceptance Criteria:**

- ADR-0037 exists and is accepted.
- `Credential` domain model exists in `src/security/credential.py` with fields: `provider_id`, `credential_type`, `encrypted_payload`, `created_at`, `rotated_at`, `last_validated_at`, `status`, `provenance`.
- `CredentialStatus` enum defined: `active`, `revoked`, `expired`, `unknown`.
- Module boundary rule documented: no provider adapter imports from `src/security/`.

**Resolution Summary:**
Added the top-level `src/security/` boundary with immutable `Credential` and `CredentialStatus` domain types matching ADR-0037. The model includes replay-oriented credential metadata, validates required fields and temporal consistency, and leaves storage/decryption concerns for later M10C issues while preserving adapter independence from `src/security/`.

**Completed Verification:**

- `uv run pytest tests\test_credential.py`
- `uv run ruff check src\security tests\test_credential.py`

---

## TF-F005: Implement KeyManager And Encrypted Local Credential Store

**Status:** Done

**Classification:** enhancement

**Milestone:** M10C

**Branch:** `feature/tf-f005-credential-store-implementation`

**Affected Layer:** security, infrastructure

**Linked ADRs:** ADR-0037

**Impacted Invariants:** Architectural Simplicity, Historical Integrity

**Problem:**
No encrypted storage exists for provider credentials. Keys live as raw strings in environment or constructor calls. No Fernet encryption, no `.keys.enc` file, no `TRADEFORGE_MASTER_KEY` enforcement.

**Acceptance Criteria:**

- `TRADEFORGE_MASTER_KEY` loaded from OS environment only — not `.env`, not Git.
- `KeyManager` in `src/security/key_manager.py`: encrypt/decrypt using Fernet, master key loading with clear error if unset.
- `CredentialStore` in `src/security/credential_store.py`: read/write encrypted credentials to `.keys.enc`.
- `.keys.enc` added to `.gitignore`.
- CLI command or script to generate `TRADEFORGE_MASTER_KEY` and register initial credentials.
- Provider credentials: Polygon (`api_key`), Alpaca (`api_key` + `secret_key`), Alpha Vantage (`api_key`), FinancialModelingPrep (`api_key`), Finqual (`api_key`).
- Encrypted values never appear in logs, environment dumps, or error messages.
- Unit tests for KeyManager: encrypt → decrypt round-trip, wrong master key raises error.
- Unit tests for CredentialStore: write credential, read it back, status filtering.

**Resolution Summary:**
Implemented Fernet-backed credential encryption through `KeyManager`, added a JSON-backed local `CredentialStore` that persists encrypted payloads to `.keys.enc`, added a small `scripts/manage_credentials.py` command surface for master-key generation and initial provider registration, added `.keys.enc` to `.gitignore`, and declared the new `cryptography` runtime dependency.

**Completed Verification:**

- `uv run pytest tests\test_credential.py tests\test_key_manager.py tests\test_credential_store.py`
- `uv run ruff check src\security scripts\manage_credentials.py tests\test_credential.py tests\test_key_manager.py tests\test_credential_store.py`
- `uv run mypy src\security scripts\manage_credentials.py tests\test_credential.py tests\test_key_manager.py tests\test_credential_store.py`

---

## TF-F006: Wire All Provider Adapters Through CredentialStore At Composition Root

**Status:** Done

**Classification:** refactor

**Milestone:** M10C

**Branch:** `feature/tf-f006-provider-credential-wiring`

**Affected Layer:** app, infrastructure, security

**Linked ADRs:** ADR-0037

**Impacted Invariants:** Architectural Simplicity, Layer Separation

**Problem:**
`create_app()` in `src/app/api/application.py` currently wires `YFinanceProvider()` directly with no credential management. Polygon and Alpaca adapters exist but would need raw constructor injection. Alpha Vantage, FMP, Finqual adapters (planned) would follow the same unsafe pattern.

**Acceptance Criteria:**

- `create_app()` accepts an optional `credential_store: CredentialStore | None` parameter.
- When `credential_store` is provided (or initialized from `.keys.enc`), provider adapters receive decrypted credentials from the store — not from raw env vars or constructor parameters.
- `YFinanceProvider` remains keyless (no change).
- Polygon, Alpaca, and all future providers (Alpha Vantage, FMP, Finqual) are wired through `CredentialStore`.
- Provider adapters themselves have zero imports from `src/security/` — boundary enforced.
- Integration test: `create_app()` with injected `CredentialStore` serves market data correctly.
- All existing tests continue to pass (adapters still accept constructor injection for tests).

**Resolution Summary:**
Centralized default market-provider construction in `create_app()`, added optional `credential_store` injection, kept `yfinance` as the keyless default, and routed `polygon` and `alpaca` construction through decrypted `CredentialStore` payloads selected by `TRADEFORGE_MARKET_PROVIDER`. Provider adapters remain security-agnostic and continue to support constructor injection in their own tests.

**Completed Verification:**

- `uv run pytest tests\test_provider_credential_wiring.py tests\test_market_context_overlay.py`
- `uv run ruff check src\app\api\application.py tests\test_provider_credential_wiring.py`
- `uv run mypy --follow-imports=skip src\app\api\application.py tests\test_provider_credential_wiring.py`

---

## TF-F007: Credential Setup Guide, Rotation Documentation, And Keys-Out-Of-Git Enforcement

**Status:** Planned

**Classification:** operational

**Milestone:** M10C

**Branch:** `feature/tf-f007-credential-setup-documentation`

**Affected Layer:** docs, operational

**Linked ADRs:** ADR-0037

**Problem:**
No setup guide exists for credential initialization. No rotation procedure is documented. No `.gitignore` enforcement prevents accidental key commits.

**Provider coverage:**
- Polygon.io: `api_key` — https://polygon.io
- Alpaca: `api_key` + `secret_key` — https://alpaca.markets
- Alpha Vantage: `api_key` — https://www.alphavantage.co
- FinancialModelingPrep: `api_key` — https://financialmodelingprep.com
- Finqual: `api_key` — https://finqual.com

**Acceptance Criteria:**

- `HOW-TO-SETUP-KEYS.md` exists at project root covering: master key generation, credential registration for each provider, rotation procedure, revocation.
- `.gitignore` includes: `.keys.enc`, `TRADEFORGE_MASTER_KEY` (if ever written to file).
- `README.md` references the setup guide.
- Operator can set up all credentials in under 5 minutes following the guide.

**Resolution Summary:**
Added a root credential setup guide covering master-key generation, provider registration, provider selection, rotation, revocation, and secret-handling rules. Linked the guide from `README.md` and extended `.gitignore` with a defensive `TRADEFORGE_MASTER_KEY` guard in addition to `.keys.enc`.

**Completed Verification:**

- Manual review against `scripts\manage_credentials.py`
- Confirmed `.gitignore` contains both `.keys.enc` and `TRADEFORGE_MASTER_KEY`
- Confirmed `README.md` links to `HOW-TO-SETUP-KEYS.md`

---

## TF-F008: Wire PostgresEventStore As Default Runtime Persistence Via TRADEFORGE_DATABASE_URL

**Status:** Done

**Classification:** architectural

**Milestone:** M10B

**Branch:** `feature/tf-f008-postgres-default-persistence`

**Affected Layer:** app, infrastructure

**Linked ADRs:** ADR-0018 (Postgres event store persistence), ADR-0019 (projection persistence)

**Impacted Invariants:** Event Ledger Canonical Truth, Events Are Immutable, Replayability Is Foundational

**Source:** Second operational testing session — 2026-05-15. All decision data lost on server restart. `knowledge/raw/20260515-second-testing-session-persistence-observation.md`

**Problem:**
`create_app()` defaults to `InMemoryEventStore()`. All decision data is lost on server restart, container restart, or between testing sessions. Operators cannot resume prior decisions or accumulate a real decision history. `PostgresEventStore` already exists in `src/infrastructure/event_store/postgres.py` and reads from `TRADEFORGE_DATABASE_URL` via `PostgresConnectionSettings.from_environment()`. Wiring is the only gap.

**Acceptance Criteria:**

- `create_app()` checks for `TRADEFORGE_DATABASE_URL` in the environment at startup.
- If set: uses `PostgresEventStore()` as the default event store.
- If not set: falls back to `InMemoryEventStore()` (preserves demo and test behavior).
- Alembic migrations run on startup (or documented as a pre-start step) when Postgres is active.
- Server restart with `TRADEFORGE_DATABASE_URL` set preserves all prior decision events.
- All existing tests continue to pass (they inject `InMemoryEventStore` directly — unaffected).
- A decision created in one server session is retrievable after server restart.

**Out Of Scope:**

- Multi-user or remote database configuration.
- Postgres for market snapshot persistence (may follow separately).
- Connection pooling or production hardening.

---

## TF-F009: Implement All-Decisions Projection And Multi-Decision Navigation In Operating Workspace

**Status:** Done

**Classification:** enhancement

**Milestone:** M10B

**Branch:** `feature/tf-f009-multi-decision-navigation`

**Affected Layer:** backend (api, services), frontend (Operating Workspace)

**Linked ADRs:** ADR-0002 (Decision Lifecycle Engine), ADR-0004 (Workspace Projection Model)

**Impacted Invariants:** Workflow-Centric Architecture, Decision Lifecycle, Human Decision Sovereignty

**Source:** Second operational testing session — 2026-05-15. No way to navigate between concurrent decisions or see all active decisions in one surface.

**Problem:**
When an operator has decisions across multiple securities (SMH at Armed stage, NVDA at Thesis stage), there is no surface to see all active decisions and navigate between them. The Operating Workspace shows an attention queue for the current context but has no decision list. With Postgres persistence enabled (TF-F008), decisions accumulate — but there is no UI to surface them.

**Backend — new endpoint:**

`GET /lifecycle/decisions` — returns all decisions derived from the event store.

Each decision record:
```
{
  decision_id: str,
  symbol: str,
  current_stage: str,          # Idea, Thesis, Plan, Approval, Armed, Execution, Position, Review
  created_at: datetime,        # timestamp of trade_idea_created event
  last_updated_at: datetime,   # timestamp of most recent lifecycle event
  stage_updated_at: datetime   # timestamp of current stage entry
}
```

Derived by scanning all `trade_idea_created` events, grouping by decision_id,
and deriving current lifecycle stage from the event history per decision.

**Frontend — Operating Workspace:**

- Decision list panel showing all decisions: symbol, current stage badge, age
- Clicking any decision navigates to the appropriate workspace for that stage
  (using `STAGE_TO_WORKSPACE` routing already in `workspaceRouting.ts`)
- Stage badge colored by lifecycle position (idea/thesis = neutral, plan/approval/armed = attention, execution/position = active, review = complete)
- Empty state when no decisions exist

**Acceptance Criteria:**

- `GET /lifecycle/decisions` returns all decisions across all securities.
- Operating Workspace displays a decision list when decisions exist.
- Clicking a decision with stage "Armed" navigates to Active Position Workspace with that decision's context.
- Clicking a decision with stage "Plan" navigates to Plan Review Workspace.
- Decision list updates after creating a new trade idea.
- Empty state shown cleanly when no decisions exist.
- Works with both InMemory (ephemeral list) and Postgres (persistent list) event stores.

---

## TF-F010: Fix Thesis Narrative Minimum-Length Validation Gap In ThesisDevelopmentModal

**Status:** Done

**Classification:** bug

**Milestone:** M10B

**Branch:** `feature/tf-0064-operational-attention-continuity`

**Affected Layer:** frontend (ThesisDevelopmentModal)

**Linked ADRs:** none

**Impacted Invariants:** none

**Source:** Operational testing session — 2026-05-15. `POST /lifecycle/decisions/develop-thesis` returned 422 when narrative was shorter than 10 characters.

**Problem:**
The backend `DevelopThesisPayload` declares `narrative: str = Field(min_length=10)`. The frontend `ThesisDevelopmentModal` validated only that the narrative was non-empty (`!narrative.trim()`), with no minimum-length check. A narrative of 1–9 characters passed frontend validation and reached the backend, which returned 422 Unprocessable Entity with no user-visible explanation.

**Fix:**
Added a `narrative.trim().length < 10` guard in `handleSubmit` with a descriptive error message: *"Thesis narrative is too short — write at least a sentence explaining the core argument."*

**Acceptance Criteria:**

- Submitting a narrative shorter than 10 characters displays the descriptive message without reaching the backend.
- Valid narratives (10+ characters) submit successfully.
- No backend 422 is returned for this validation path.

---

## TF-F011: Fix Docker Compose Command To Start Uvicorn And Restore Operational Persistence

**Status:** Done

**Classification:** operational

**Milestone:** M10B

**Branch:** `feature/tf-0064-operational-attention-continuity`

**Affected Layer:** infrastructure (docker-compose.yml)

**Linked ADRs:** none

**Impacted Invariants:** Replayability Is Foundational

**Source:** Operational testing session — 2026-05-15. Container `tradeforge-tradeforge-1` was found stopped; server was running manually outside Docker without `TRADEFORGE_DATABASE_URL`, causing in-memory fallback and silent event loss.

**Problem:**
`command` in `docker-compose.yml` was a placeholder: `["uv", "run", "python", "--version"]`. Python prints the version and exits — the container stops immediately and the uvicorn server never starts. Because the server ran outside Docker, `TRADEFORGE_DATABASE_URL` (correctly defined in compose) never reached the app. `create_event_store()` resolved to `InMemoryEventStore`. Events created in the session were not written to Postgres `event_ledger` and were lost on process exit.

**Fix:**
- Replaced placeholder `command` with the uvicorn startup command: `["uv", "run", "uvicorn", "src.app.api.application:app", "--host", "0.0.0.0", "--port", "8000"]`
- Added `ports: - "8000:8000"` to the tradeforge service (was absent — only postgres had port mapping)
- Added `restart: unless-stopped` to both the tradeforge and postgres services

**Acceptance Criteria:**

- `docker compose up -d` starts the tradeforge container and it remains running.
- The API is accessible at `http://localhost:8000`.
- Events written via the API appear in the Postgres `event_ledger` table.
- Container survives host reboot without manual restart.

**Out Of Scope:**

- `.env` file support
- Named bridge network

**Completed Verification:**

- `docker compose config` — compose file is valid
- `docker compose up -d` — container starts and stays running
- `curl http://localhost:8000/health` — API responds
- `docker exec tradeforge-postgres-1 psql -U tradeforge -d tradeforge -c "SELECT count(*) FROM event_ledger;"` — confirms events reach Postgres

---

