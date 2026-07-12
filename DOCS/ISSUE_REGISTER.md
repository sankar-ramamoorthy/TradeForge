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

Roadmap v2 is the active milestone direction. This register now tracks runtime implementation through completed M14 and active M14C while preserving the earlier MVP record for reference.


---

## Issue Series

| Series | Pattern | Purpose |
|---|---|---|
| Roadmap issues | `TF-####` | Planned milestone implementation work — sequential, roadmap-tied |
| Feedback issues | `TF-F###` | Field-observed bugs, enhancements, and architectural gaps discovered during testing or operation |
| Paper trading | `TF-P###` | M-PT paper execution boundary work |
| API refactor | `TF-RF###` | M-RF routes.py decomposition phases |
| DI conversion | `TF-RF2-###` | M-RF2 FastAPI Depends() conversion phases |
| Frontend refactor | `TF-RFE###` | M-RF-FE frontend API client decomposition phases |
| Ease of use | `EZ-##` / `EV-##` / `RAMP-##` / `GOV-##` | M-EZ onboarding, evidence density, entry ramp, and governance calibration work |

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
| TF-A008 | Done | M12 | Implement contextual interpretation artifacts | `feature/m12-advisory-observation-foundation` |
| TF-A009 | Done | M12 | Implement conflicting evidence surfacing | `feature/m12-advisory-observation-foundation` |
| TF-A010 | Done | M12 | Implement evidence aging/staleness visibility | `feature/m12-advisory-observation-foundation` |
| TF-A011 | Done | M12 | Implement advisory candidate ingestion pipeline | `feature/m12-advisory-observation-foundation` |
| TF-A012 | Done | M12 | Implement candidate review queue | `feature/m12-advisory-observation-foundation` |
| TF-A013 | Done | M12 | Implement operator candidate promotion workflow | `feature/m12-advisory-observation-foundation` |
| TF-A014 | Done | M12 | Prevent automated lifecycle promotion into TradeIdea | `feature/m12-advisory-observation-foundation` |
| TF-A015 | Done | M12 | Implement candidate provenance visualization | `feature/m12-advisory-observation-foundation` |
| TF-A016 | Done | M12 | Define external research cockpit import boundary | `feature/m12-advisory-observation-foundation` |
| TF-A017 | Done | M12 | Implement research artifact ingestion API | `feature/m12-advisory-observation-foundation` |
| TF-A018 | Done | M12 | Implement Codex/Claude-generated advisory artifact support | `feature/m12-advisory-observation-foundation` |
| TF-A019 | Done | M12 | Implement advisory markdown artifact persistence | `feature/m12-advisory-observation-foundation` |
| TF-A020 | Done | M12 | Implement replay-safe advisory snapshot capture | `feature/m12-advisory-observation-foundation` |
| TF-B001 | Done | M13 | Define interpretation artifact schema | `feature/m13-contextual-interpretation-thesis-influence` |
| TF-B002 | Done | M13 | Implement contextual weighting framework | `feature/m13-contextual-interpretation-thesis-influence` |
| TF-B003 | Done | M13 | Implement regime-aware weighting model | `feature/m13-contextual-interpretation-thesis-influence` |
| TF-B004 | Done | M13 | Implement conflicting evidence analysis | `feature/m13-contextual-interpretation-thesis-influence` |
| TF-B005 | Done | M13 | Implement confidence-range representation | `feature/m13-contextual-interpretation-thesis-influence` |
| TF-B006 | Done | M13 | Implement thesis evidence influence tracking | `feature/m13-contextual-interpretation-thesis-influence` |
| TF-B007 | Done | M13 | Implement supporting vs weakening evidence classification | `feature/m13-contextual-interpretation-thesis-influence` |
| TF-B008 | Done | M13 | Implement thesis drift detection | `feature/m13-contextual-interpretation-thesis-influence` |
| TF-B009 | Done | M13 | Implement contextual contradiction surfacing | `feature/m13-contextual-interpretation-thesis-influence` |
| TF-B010 | Done | M13 | Implement evidence impact replay overlays | `feature/m13-contextual-interpretation-thesis-influence` |
| TF-B011 | Done | M13 | Implement interpretation-first operational surfaces | `feature/m13-contextual-interpretation-thesis-influence` |
| TF-B012 | Done | M13 | Implement uncertainty-preserving UX patterns | `feature/m13-contextual-interpretation-thesis-influence` |
| TF-B013 | Done | M13 | Implement probabilistic cognition summaries | `feature/m13-contextual-interpretation-thesis-influence` |
| TF-B014 | Done | M13 | Implement evidence narrative generation | `feature/m13-contextual-interpretation-thesis-influence` |
| TF-B015 | Done | M13 | Implement contextual reasoning timelines | `feature/m13-contextual-interpretation-thesis-influence` |
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
| TF-F045 | Done | M13 | Add LiteLLM credential shape to CredentialStore | `feature/tf-f045-litellm-credential-shape` |
| TF-F046 | Done | M13 | Implement OpenAICompatibleAdvisoryProvider | `feature/tf-f046-openai-compatible-advisory-provider` |
| TF-F047 | Done | M13 | Implement prompt template and service wiring for replay summary | `feature/tf-f047-advisory-replay-summary-prompt` |
| TF-F048 | Done | M13 | Implement prompt template and service wiring for thesis review assistant | `feature/tf-f048-advisory-thesis-review-prompt` |
| TF-F049 | Done | M13 | Implement prompt template and service wiring for advisory observation generation | `feature/tf-f049-advisory-observation-generation-prompt` |
| TF-F050 | Done | M13 | Implement prompt template and service wiring for candidate screening | `feature/tf-f050-advisory-candidate-screening-prompt` |
| TF-F051 | Done | M13 | Add on-demand advisory API endpoints and frontend trigger surfaces | `feature/tf-f051-advisory-on-demand-endpoints` |
| TF-F052 | Done | M13 | Add advisory service health check to ProviderConfigurationPanel | `feature/tf-f052-advisory-health-check` |
| TF-F053 | Done | M13 | Validate NVIDIA NIM via LiteLLM and document credential shape | `docs/tf-f053-nvidia-nim-litellm-validation` |
| TF-F054 | Done | M13 | Document automatic enrichment lifecycle hook points | `docs/tf-f054-auto-enrichment-hook-points` |
| TF-F055 | Done | M13 | Implement UI-Based Credential Management | `feature/tf-f055-ui-credential-management` |
| TF-F056 | Done | M13 | Fix missing default advisory provider bootstrap after merge | `fix/tf-f056-default-advisory-provider-bootstrap` |
| TF-F057 | Done | M13 | Add optional LiteLLM Docker Compose runtime service | `feature/tf-f057-litellm-compose-service` |
| TF-F058 | Done | M13 | Allow frontend npm commands from repository root | `fix/tf-f058-root-npm-frontend-scripts` |
| TF-F059 | Done | M13A | Formalize M13A provider governance roadmap | `docs/tf-f059-m13a-provider-governance-roadmap` |
| TF-F060 | Done | M13A | Define provider governance control surface design | `docs/tf-f060-provider-governance-control-surface` |
| TF-F061 | Done | M13A | Define capability routing governance model | `docs/tf-f061-capability-routing-governance` |
| TF-F062 | Done | M13A | Define AI gateway and route alias model | `docs/tf-f062-ai-gateway-route-aliases` |
| TF-F063 | Done | M13A | Define provider diagnostics and health history model | `docs/tf-f063-provider-diagnostics-health-history` |
| TF-F064 | Done | M13A | Implement provider governance read APIs | `feature/tf-f064-provider-governance-read-apis` |
| TF-F065 | Done | M13A | Implement credential validation and test workflow | `feature/tf-f065-credential-validation-test-workflow` |
| TF-F066 | Done | M13A | Implement AI gateway route visibility | `feature/tf-f066-ai-gateway-route-visibility` |
| TF-F067 | Done | M13A | Implement provider governance frontend surface and rail cleanup | `feature/tf-f067-provider-governance-surface` |
| TF-F068 | Done | M13A | M13A verification and M14 readiness gate | `docs/tf-f068-m13a-readiness-gate` |
| TF-F069 | Done | M14 | Provider governance UI broken — JSON parse failure on load | `fix/tf-f069-provider-governance-json-parse` |
| TF-F070 | Done | M13A | Advisory Route Diagnostics And Explicit Advisory Invocation | `feature/tf-f070-advisory-route-diagnostics` |
| TF-F071 | Done | M13A | Fix Advisory Thesis Review Event Store Loading | `fix/tf-f071-advisory-thesis-review-event-read` |
| TF-F072 | Done | M13B | Global Advisory Model Selection | `feature/tf-f072-global-advisory-model-selection` |
| TF-F073 | Done | M13B | Internalize LiteLLM Gateway Network Boundary | `feature/tf-f073-internalize-litellm-gateway-boundary` |
| TF-F074 | Done | M13B | Governed LLM Provider Secret Management | `feature/tf-f074-governed-llm-provider-secrets` |
| TF-F075 | Done | M13B | Implement Stateless LiteLLM Request-Time Credential Composition | `feature/tf-f075-litellm-secret-injection` |
| TF-F076 | Done | M13B | Replace LiteLLM route-probing healthcheck with non-invasive readiness check | `fix/tf-f076-litellm-readiness-healthcheck` |
| TF-F077 | Done | M14C | Verify ATKR Thesis Local Import Feedback | `fix/tf-f077-atkr-thesis-import-feedback` |
| TF-C001 | Done | M14 | Detect recurring sizing violations | `feature/tf-c001-recurring-sizing-violations` |
| TF-C002 | Done | M14 | Detect impulsive execution patterns | `feature/tf-c002-impulsive-execution-patterns` |
| TF-C003 | Done | M14 | Implement process deviation overlays | `feature/tf-c003-process-deviation-overlays` |
| TF-C004 | Done | M14 | Implement behavioral clustering | `feature/tf-c004-behavioral-clustering` |
| TF-C005 | Done | M14 | Implement recurring mistake analysis | `feature/tf-c005-recurring-mistake-analysis` |
| TF-C006 | Done | M14 | Implement discipline deterioration signals | `feature/tf-c006-discipline-deterioration-signals` |
| TF-C007 | Done | M14 | Implement thesis attachment analysis | `feature/tf-c007-thesis-attachment-analysis` |
| TF-C008 | Done | M14 | Implement emotional reflection overlays | `feature/tf-c008-emotional-reflection-overlays` |
| TF-C009 | Done | M14 | Implement operator behavior timelines | `feature/tf-c009-operator-behavior-timelines` |
| TF-C010 | Done | M14 | Implement decision-quality review metrics | `feature/tf-c010-decision-quality-review-metrics` |
| TF-R001 | Done | M14C | Thesis Workspace Advisory Import Preview | `feature/m14c-thesis-import-workflow` |
| TF-R002 | Done | M14C | Plan Workspace Advisory Import Mediation | `feature/m14c-plan-import-mediation` |
| TF-P001 | Planned | M-PT | ADR — paper execution boundary model | `docs/tf-p001-paper-execution-adr` |
| TF-P002 | Planned | M-PT | Register M-PT issues and roadmap entry | `docs/tf-p002-mpt-registration` |
| TF-P003 | Planned | M-PT | Paper order domain model and validation | `feature/tf-p003-paper-order-domain` |
| TF-P004 | Planned | M-PT | ExecutionPort protocol and Alpaca paper adapter | `feature/tf-p004-alpaca-paper-adapter` |
| TF-P005 | Planned | M-PT | In-memory FakeExecutionAdapter | `feature/tf-p005-fake-execution-adapter` |
| TF-P006 | Planned | M-PT | ExecutionOrchestrationService | `feature/tf-p006-execution-orchestration` |
| TF-P007 | Planned | M-PT | OrderSyncService polling reconciliation | `feature/tf-p007-order-sync-service` |
| TF-P008 | Planned | M-PT | Armed-trigger evaluation to attention queue | `feature/tf-p008-armed-trigger-attention` |
| TF-P009 | Planned | M-PT | Execution API routes | `feature/tf-p009-execution-routes` |
| TF-P010 | Planned | M-PT | Paper execution workspace surfaces | `feature/tf-p010-execution-workspaces` |
| TF-P011 | Planned | M-PT | Execution-quality facts in review projections | `feature/tf-p011-execution-quality-review` |
| TF-P012 | Planned | M-PT | Docs, demo flow, and KB synthesis | `docs/tf-p012-mpt-closeout` |
| EZ-01 | Planned | M-EZ | Postgres-by-default single compose stack | `feature/ez-01-single-compose-stack` |
| EZ-02 | Planned | M-EZ | In-app first-run wizard for master key setup | `feature/ez-02-first-run-wizard` |
| EZ-03 | Planned | M-EZ | Documentation truth pass | `docs/ez-03-doc-truth-pass` |
| EV-01 | Planned | M-EZ | Scheduled market snapshot job | `feature/ev-01-scheduled-snapshots` |
| EV-02 | Planned | M-EZ | Watchlist as first-class pre-lifecycle object | `feature/ev-02-watchlist` |
| EV-03 | Planned | M-EZ | Per-symbol evidence panel | `feature/ev-03-evidence-panel` |
| EV-04 | Planned | M-EZ | Basic price chart component | `feature/ev-04-price-chart` |
| RAMP-01 | Planned | M-EZ | Quick-capture idea tier | `feature/ramp-01-quick-capture` |
| RAMP-02 | Planned | M-EZ | Guided first-decision mode | `feature/ramp-02-guided-first-decision` |
| RAMP-03 | Planned | M-EZ | Operator identity profiles | `feature/ramp-03-operator-identity` |
| GOV-01 | Planned | M-EZ | Two-tier issue discipline documentation | `docs/gov-01-two-tier-discipline` |
| GOV-02 | Planned | M-EZ | Knowledge base hygiene pass | `docs/gov-02-kb-hygiene` |
| TF-RF001 | Planned | M-RF | OpenAPI contract snapshot test | `refactor/tf-rf001-openapi-snapshot` |
| TF-RF002 | Planned | M-RF | Extract deps.py service accessors | `refactor/tf-rf002-deps-extraction` |
| TF-RF003 | Planned | M-RF | Create routes package; move runtime and behavioral | `refactor/tf-rf003-routes-package` |
| TF-RF004 | Planned | M-RF | Move replay, provenance, and market routers | `refactor/tf-rf004-replay-market` |
| TF-RF005 | Planned | M-RF | Move workspace router | `refactor/tf-rf005-workspace` |
| TF-RF006 | Planned | M-RF | Move lifecycle router | `refactor/tf-rf006-lifecycle` |
| TF-RF007 | Planned | M-RF | Move advisory router family | `refactor/tf-rf007-advisory` |
| TF-RF008 | Planned | M-RF | Move governance router | `refactor/tf-rf008-governance` |
| TF-RF009 | Planned | M-RF | Move local import parsing to services layer | `refactor/tf-rf009-import-parsing` |
| TF-RF010 | Planned | M-RF | Final assembly and monolith deletion | `refactor/tf-rf010-assembly` |
| TF-RF2-001 | Planned | M-RF2 | Accessor inventory and conversion baseline | `refactor/tf-rf2-001-inventory` |
| TF-RF2-002 | Planned | M-RF2 | Rename accessors to public get_* names | `refactor/tf-rf2-002-accessor-renames` |
| TF-RF2-003 | Planned | M-RF2 | Convert handler-direct call sites to Depends | `refactor/tf-rf2-003-handler-depends` |
| TF-RF2-004 | Planned | M-RF2 | Convert request-taking helpers to explicit params | `refactor/tf-rf2-004-helper-params` |
| TF-RF2-005 | Planned | M-RF2 | Dependency override demonstration test | `refactor/tf-rf2-005-override-test` |
| TF-RF2-006 | Planned | M-RF2 | M-RF2 closeout and gates | `refactor/tf-rf2-006-closeout` |
| TF-RFE001 | Planned | M-RF-FE | Extract http.ts request helper | `refactor/tf-rfe001-http-helper` |
| TF-RFE002 | Planned | M-RF-FE | Move behavioral and replay client modules | `refactor/tf-rfe002-behavioral-replay` |
| TF-RFE003 | Planned | M-RF-FE | Move workspace and market client modules | `refactor/tf-rfe003-workspace-market` |
| TF-RFE004 | Planned | M-RF-FE | Move lifecycle client module | `refactor/tf-rfe004-lifecycle` |
| TF-RFE005 | Planned | M-RF-FE | Move advisory, generation, and imports modules | `refactor/tf-rfe005-advisory` |
| TF-RFE006 | Planned | M-RF-FE | Move governance client module | `refactor/tf-rfe006-governance` |
| TF-RFE007 | Planned | M-RF-FE | Error-handling unification via requestJson | `refactor/tf-rfe007-error-unification` |
| TF-RFE008 | Planned | M-RF-FE | M-RF-FE closeout and barrel decision | `refactor/tf-rfe008-closeout` |

## TF-C001: Detect Recurring Sizing Violations

**Status:** Done

**Classification:** feature / behavioral intelligence

**Milestone:** M14

**Branch:** `feature/tf-c001-recurring-sizing-violations`

**Affected Layer:** domain, services, app, tests, docs

**Linked ADRs:** ADR-0001, ADR-0002, ADR-0008, ADR-0033, ADR-0035, ADR-0044

**Impacted Invariants:** Event Ledger Canonical Truth, Events Are Immutable, Replayability Is Foundational, Derived State Must Remain Distinguishable, Reflection And Review Are First-Class, Deterministic Rule Evaluation, Human Decision Sovereignty

**Depends On:** M13B completion, structured plan artifacts, structured review reflection artifacts, replay timeline foundation

**Problem:**
M14 behavioral intelligence needs a deterministic, replayable first signal
before introducing clustering, AI-assisted behavioral interpretation, or
decision-quality metrics. Sizing discipline is the best initial vertical slice
because structured plans already capture sizing rationale and structured
reviews already capture discipline observations, behavioral observations, and
execution quality.

**Scope:**

- Add a pure domain detector for sizing discipline signals derived from event
  history.
- Detect sizing process concerns from structured `decision.plan_created` /
  `decision.plan_revised` and `review.review_completed` payloads.
- Include source event references, severity, recurrence count, and derived
  authority metadata.
- Add a read-only behavioral signal service and API.
- Support persona, workspace, and decision filtering.
- Preserve graceful handling for legacy or incomplete events.

**Acceptance Criteria:**

- Recurring sizing violations are detected deterministically from event history.
- Signals are returned with `authority: derived` and `is_canonical: false`.
- Signals include source event references sufficient for replay and audit.
- Filtering by persona, workspace, and decision is supported.
- The read API does not append events or mutate lifecycle state.
- Legacy events without structured review or plan payloads do not fail signal
  generation.
- Tests cover recurring detection, clean-review exclusion, read API behavior,
  filtering, and no event-ledger writes.

**Out Of Scope:**

- Lifecycle gates or approval-blocking behavior.
- Broker execution or position sizing automation.
- AI-generated behavioral conclusions.
- Behavioral clustering.
- Decision-quality scoring.
- New canonical behavioral event types.
- Frontend overlays; deferred to TF-C003.

**ADR Checkpoint:**
ADR-0044 records the decision to model M14 behavioral signals as deterministic,
derived read models rather than canonical event-ledger facts.

**Resolution Summary:**
Implemented `SizingViolationDetector` as a pure domain component and
`BehavioralSignalReadService` as a read-only derived projection over the event
store. Added `GET /behavioral/signals` with optional persona, workspace, and
decision filters. Responses expose derived/non-canonical authority, recurrence
counts, severity, timestamps, and source event references.

**Completed Verification:**

- `uv run pytest tests/test_behavioral_signals.py tests/test_replay_timeline.py tests/test_create_plan_workflow.py tests/test_complete_review_workflow.py`
- `uv run mypy src\domain\behavioral src\services\behavioral src\app\api\application.py src\app\api\routes.py tests\test_behavioral_signals.py`
- `uv run ruff check src\domain\behavioral src\services\behavioral tests\test_behavioral_signals.py`
- `git diff --check`

---

## TF-C002: Detect Impulsive Execution Patterns

**Status:** Done

**Classification:** feature / behavioral intelligence

**Milestone:** M14

**Branch:** `feature/tf-c002-impulsive-execution-patterns`

**Affected Layer:** domain, services, app, tests

**Linked ADRs:** ADR-0001, ADR-0002, ADR-0008, ADR-0033, ADR-0035, ADR-0044

**Impacted Invariants:** Lifecycle Authority, Replayability Is Foundational, Derived State Must Remain Distinguishable, Deterministic Rule Evaluation, Human Decision Sovereignty

**Problem:**
Operators need review-visible detection of execution timing and process
deviation patterns, especially when execution follows approval/arming too
quickly or ignores explicit plan assumptions.

**Acceptance Criteria:**

- Impulsive execution signals are derived from lifecycle timestamps and
  structured plan context.
- Outputs remain deterministic, replayable, and non-canonical.
- Source event references explain every signal.
- No lifecycle transition, approval gate, or execution authority is introduced.

**Resolution Summary:**
Extended the deterministic behavioral signal detector with
`impulsive_execution` signals derived from approval, arming, execution timing,
structured plan context, and operator-authored review language. Signals remain
derived, source-linked, and read-only.

**Completed Verification:**

- `uv run pytest tests\test_behavioral_signals.py`
- `uv run mypy src\domain\behavioral src\services\behavioral src\app\api\routes.py tests\test_behavioral_signals.py`

---

## TF-C003: Implement Process Deviation Overlays

**Status:** Done

**Classification:** feature / behavioral UX

**Milestone:** M14

**Branch:** `feature/tf-c003-process-deviation-overlays`

**Affected Layer:** services, app, frontend, tests

**Linked ADRs:** ADR-0001, ADR-0004, ADR-0007, ADR-0008, ADR-0012, ADR-0014, ADR-0044

**Impacted Invariants:** UX Is Architectural, Workspaces Are Operational Environments, Derived State Must Remain Distinguishable, Replayability Is Foundational

**Problem:**
Behavioral signals become operationally useful only when review and replay
surfaces show process deviations with source context and authority boundaries.

**Acceptance Criteria:**

- Review/replay/workspace surfaces can display TF-C001 and TF-C002 signals.
- Overlays clearly distinguish derived behavioral signals from canonical facts.
- Source events are inspectable from the overlay context.
- The UI does not become a dashboard-style analytics surface.

**Resolution Summary:**
Added review and replay behavioral panels that display derived signals,
clusters, mistakes, emotional reflection terms, behavior timeline entries, and
quality metrics with explicit derived/non-canonical authority labels.

**Completed Verification:**

- `npm.cmd run typecheck`
- `npm.cmd run build`

---

## TF-C004: Implement Behavioral Clustering

**Status:** Done

**Classification:** feature / behavioral intelligence

**Milestone:** M14

**Branch:** `feature/tf-c004-behavioral-clustering`

**Affected Layer:** domain, services, app, tests

**Linked ADRs:** ADR-0001, ADR-0006, ADR-0008, ADR-0009, ADR-0044

**Impacted Invariants:** AI Advisory Boundary, Derived State Must Remain Distinguishable, Persona-Scoped Operation, Replayability Is Foundational

**Acceptance Criteria:**

- Clustering builds on deterministic behavioral signals.
- Cluster outputs remain advisory or derived, never canonical truth.
- Persona scope is preserved.

**Resolution Summary:**
Added deterministic behavioral clusters grouped by persona, workspace, and
signal type. Cluster output preserves source signal IDs, severity, and
derived/non-canonical authority metadata.

**Completed Verification:**

- `uv run pytest tests\test_behavioral_signals.py`
- `uv run mypy src\domain\behavioral src\services\behavioral src\app\api\routes.py tests\test_behavioral_signals.py`

---

## TF-C005: Implement Recurring Mistake Analysis

**Status:** Done

**Classification:** feature / behavioral intelligence

**Milestone:** M14

**Branch:** `feature/tf-c005-recurring-mistake-analysis`

**Affected Layer:** domain, services, app, tests

**Linked ADRs:** ADR-0001, ADR-0008, ADR-0033, ADR-0035, ADR-0044

**Impacted Invariants:** Reflection And Review Are First-Class, Deterministic Rule Evaluation, Derived State Must Remain Distinguishable

**Acceptance Criteria:**

- Recurring mistake analysis aggregates deterministic signals and structured
  review reflections.
- The analysis separates decision process from trade outcome.
- Outputs remain replayable and source-linked.

**Resolution Summary:**
Added recurring mistake analysis over deterministic behavioral signals and
structured review reflections. The analysis reports process categories,
decision counts, signal counts, review quality averages, source signal IDs, and
source event references without scoring trades or outcomes.

**Completed Verification:**

- `uv run pytest tests\test_behavioral_signals.py`
- `uv run mypy src\domain\behavioral src\services\behavioral src\app\api\routes.py tests\test_behavioral_signals.py`

---

## TF-C006: Implement Discipline Deterioration Signals

**Status:** Done

**Classification:** feature / behavioral intelligence

**Milestone:** M14

**Branch:** `feature/tf-c006-discipline-deterioration-signals`

**Affected Layer:** domain, services, app, tests

**Linked ADRs:** ADR-0001, ADR-0008, ADR-0033, ADR-0044

**Impacted Invariants:** Replayability Is Foundational, Deterministic Rule Evaluation, Historical Integrity

**Acceptance Criteria:**

- Deterioration signals are based on longitudinal process signals, not P&L.
- Time windows and recurrence logic are explicit and deterministic.
- Signals remain derived and non-canonical.

**Resolution Summary:**
Added discipline deterioration signals that compare recent deterministic
process signals against an earlier baseline window. The logic uses explicit
window counts and never depends on P&L or live external state.

**Completed Verification:**

- `uv run pytest tests\test_behavioral_signals.py`
- `uv run mypy src\domain\behavioral src\services\behavioral src\app\api\routes.py tests\test_behavioral_signals.py`

---

## TF-C007: Implement Thesis Attachment Analysis

**Status:** Done

**Classification:** feature / behavioral intelligence

**Milestone:** M14

**Branch:** `feature/tf-c007-thesis-attachment-analysis`

**Affected Layer:** domain, services, app, tests

**Linked ADRs:** ADR-0001, ADR-0008, ADR-0033, ADR-0035, ADR-0042, ADR-0044

**Impacted Invariants:** Historical Integrity, Derived State Must Remain Distinguishable, Reflection And Review Are First-Class

**Acceptance Criteria:**

- Analysis uses thesis artifacts, revisions, invalidation conditions, evidence
  influence, and review reflections where available.
- The system does not infer emotional state as fact.
- Results remain review context, not lifecycle authority.

**Resolution Summary:**
Added thesis attachment analysis from thesis revisions, confidence changes,
invalidation-condition review coverage, and operator-authored reflection text.
The result is derived review context and does not label operator emotion as
fact or alter lifecycle authority.

**Completed Verification:**

- `uv run pytest tests\test_behavioral_signals.py`
- `uv run mypy src\domain\behavioral src\services\behavioral src\app\api\routes.py tests\test_behavioral_signals.py`

---

## TF-C008: Implement Emotional Reflection Overlays

**Status:** Done

**Classification:** feature / behavioral review

**Milestone:** M14

**Branch:** `feature/tf-c008-emotional-reflection-overlays`

**Affected Layer:** services, app, frontend, tests

**Linked ADRs:** ADR-0006, ADR-0007, ADR-0008, ADR-0033, ADR-0044

**Impacted Invariants:** AI Advisory Boundary, Human Decision Sovereignty, Derived State Must Remain Distinguishable, UX Is Architectural

**Acceptance Criteria:**

- Emotional context starts from operator-authored review text or explicitly
  accepted advisory artifacts.
- AI-generated emotional interpretation remains advisory and non-canonical.
- Overlays are review aids, not labels of operator truth.

**Resolution Summary:**
Added emotional reflection overlays based only on operator-authored review text.
The API and frontend present detected terms as derived review context, not as
operator-truth labels or AI-generated emotional facts.

**Completed Verification:**

- `uv run pytest tests\test_behavioral_signals.py`
- `npm.cmd run build`

---

## TF-C009: Implement Operator Behavior Timelines

**Status:** Done

**Classification:** feature / behavioral replay

**Milestone:** M14

**Branch:** `feature/tf-c009-operator-behavior-timelines`

**Affected Layer:** domain, services, app, frontend, tests

**Linked ADRs:** ADR-0001, ADR-0008, ADR-0014, ADR-0035, ADR-0044

**Impacted Invariants:** Replayability Is Foundational, Historical Integrity, Derived State Must Remain Distinguishable

**Acceptance Criteria:**

- Behavior timelines compose deterministic signals chronologically.
- Timeline entries preserve source event references and authority metadata.
- Timelines reconstruct without live APIs, current AI output, or mutable UI
  state.

**Resolution Summary:**
Added behavior timeline projection entries built chronologically from
deterministic behavioral signals. Entries preserve timestamps, source signal
IDs, source event references, and derived/non-canonical authority metadata.

**Completed Verification:**

- `uv run pytest tests\test_behavioral_signals.py`
- `npm.cmd run build`

---

## TF-C010: Implement Decision-Quality Review Metrics

**Status:** Done

**Classification:** feature / behavioral review

**Milestone:** M14

**Branch:** `feature/tf-c010-decision-quality-review-metrics`

**Affected Layer:** domain, services, app, frontend, tests

**Linked ADRs:** ADR-0001, ADR-0008, ADR-0033, ADR-0035, ADR-0044

**Impacted Invariants:** Reflection And Review Are First-Class, Human Decision Sovereignty, Derived State Must Remain Distinguishable, Deterministic Rule Evaluation

**Acceptance Criteria:**

- Metrics separate decision quality, execution quality, and outcome quality.
- Metrics remain reflective review context, not trading scores or approval
  gates.
- Metric calculations are deterministic and source-linked.

**Resolution Summary:**
Added decision-quality review metrics that keep decision quality, execution
quality, and bounded outcome context separate. Metrics are deterministic,
source-linked, reflective review context and do not become approval gates or
trading scores.

**Completed Verification:**

- `uv run pytest tests\test_behavioral_signals.py`
- `uv run mypy src\domain\behavioral src\services\behavioral src\app\api\routes.py tests\test_behavioral_signals.py`
- `npm.cmd run build`

---

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

**Status:** Done

**Classification:** architectural

**Milestone:** M12

**Branch:** `feature/m12-advisory-observation-foundation`

**Affected Layer:** domain, services, infrastructure, app

**Linked ADRs:** ADR-0006, ADR-0039, ADR-0041, ADR-0042

**Impacted Invariants:** AI Advisory Boundary, Derived State Must Remain Distinguishable, Human Decision Sovereignty, Terminology Stability

**Problem:**
Some advisory observations need lightweight contextual framing so the operator can understand what environment the observation belongs to, but M12 must not implement M13 thesis influence, weighting, scoring, or recommendation semantics.

**Implementation Summary:**
Implemented lightweight `ContextualObservationArtifact` metadata attached to advisory observations. Contextual artifacts can preserve regime notes, market context references, source links, provenance summary, and caveats as non-canonical advisory observation context. The implementation keeps M13 `AdvisoryInterpretation` semantics out of scope: no thesis influence, contextual weight, confidence range, buy/sell direction, lifecycle transition intent, or execution authority is introduced. Contextual artifact content persists in the advisory observation artifact store and is excluded from canonical capture events.

**Validation:**

- `uv run pytest tests\test_advisory_observation.py`

**Acceptance Criteria:**

- M12 contextual artifacts are stored as non-canonical advisory context attached to observations.
- Contextual artifacts may include regime notes, relevant market context references, caveats, provenance, and source links.
- Contextual artifacts do not include thesis influence, contextual weight, advisory confidence range, buy/sell direction, lifecycle transition intent, or execution authority.
- The implementation explicitly labels M13 `AdvisoryInterpretation` semantics as out of scope for this issue.
- Contextual artifact content persists outside `event_ledger`; canonical events record capture facts only when required by ADR-0041.

---

## TF-A009: Implement Conflicting Evidence Surfacing

**Status:** Done

**Classification:** enhancement

**Milestone:** M12

**Branch:** `feature/m12-advisory-observation-foundation`

**Affected Layer:** services, app, frontend

**Linked ADRs:** ADR-0006, ADR-0039, ADR-0041, ADR-0042

**Impacted Invariants:** Human Decision Sovereignty, AI Advisory Boundary, Derived State Must Remain Distinguishable, Historical Integrity

**Problem:**
Operators need visibility when advisory evidence points in different directions, but M12 must surface conflict without turning it into scoring, thesis influence, recommendation authority, or automated decision guidance.

**Implementation Summary:**
Implemented qualitative conflict visibility for advisory observations through explicit `EvidenceConflictMarker` metadata and operator caveat-derived unresolved conflict markers. API read/list responses expose conflict markers as advisory/non-canonical metadata while preserving source IDs and caveats. Conflict markers do not rank, score, approve, reject, promote, or derive thesis influence.

**Validation:**

- `uv run pytest tests\test_advisory_observation.py`

**Acceptance Criteria:**

- Advisory observation list/read workflows can expose conflict markers derived from explicit evidence metadata or operator-provided caveats.
- Conflicting evidence surfacing preserves source references and caveats for each side of the conflict.
- Conflict labels are qualitative advisory metadata only and do not rank, score, approve, reject, or promote observations.
- M13 supporting/weakening classification and thesis influence semantics remain out of scope.
- UI/API responses label conflict information as advisory and non-canonical.

---

## TF-A010: Implement Evidence Aging/Staleness Visibility

**Status:** Done

**Classification:** enhancement

**Milestone:** M12

**Branch:** `feature/m12-advisory-observation-foundation`

**Affected Layer:** domain, services, app, frontend

**Linked ADRs:** ADR-0006, ADR-0041

**Impacted Invariants:** Historical Integrity, Replayability Is Foundational, AI Advisory Boundary, Derived State Must Remain Distinguishable

**Problem:**
Advisory evidence changes operational relevance over time. Operators need staleness visibility without the system mutating historical evidence or hiding uncertainty.

**Implementation Summary:**
Implemented derived evidence staleness visibility in advisory observation API responses. Evidence records preserve captured/source timestamps, while response staleness metadata is computed deterministically from stored evidence timestamps and the observation capture timestamp. Staleness labels are derived advisory metadata only and do not mutate, delete, rewrite, or downgrade historical observations.

**Validation:**

- `uv run pytest tests\test_advisory_observation.py`

**Acceptance Criteria:**

- Evidence records preserve original captured timestamp and optional source timestamp.
- Derived staleness metadata is computed from timestamps and deterministic configuration, not stored as canonical truth.
- Staleness views distinguish current derived freshness from historical capture facts.
- Staleness labels do not invalidate, delete, rewrite, or silently downgrade historical observations.
- API/UI responses preserve uncertainty and caveats alongside staleness information.

---

## TF-A011: Implement Advisory Candidate Ingestion Pipeline

**Status:** Done

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

**Resolution Summary:**
Added `AdvisoryCandidate` as a non-canonical advisory view backed by advisory observation artifact persistence. Candidate ingestion writes through the advisory observation capture service, appends only `advisory.observation_captured`, and exposes create/read/list APIs under `/advisory/candidates`.

**Completed Verification:**

- `uv run pytest tests\test_advisory_candidate.py tests\test_advisory_observation.py`
- `uv run pytest`
- `uv run mypy src\domain\advisory src\services\advisory src\app\api tests\test_advisory_candidate.py`
- `uv run ruff check src\domain\advisory\candidate.py src\services\advisory\candidate.py tests\test_advisory_candidate.py`

---

## TF-A012: Implement Candidate Review Queue

**Status:** Done

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

**Resolution Summary:**
Added a derived `CandidateReviewQueueService` scoped by persona and workspace with deterministic ordering by captured timestamp descending, then candidate ID. The Opportunity Workspace now surfaces advisory candidates with inspect, session-local dismiss, and explicit begin-workflow actions.

**Completed Verification:**

- `uv run pytest tests\test_advisory_candidate.py tests\test_advisory_observation.py`
- `uv run pytest`
- `npm.cmd run build`
- `uv run mypy src\domain\advisory src\services\advisory src\app\api tests\test_advisory_candidate.py`

---

## TF-A013: Implement Operator Candidate Promotion Workflow

**Status:** Done

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

**Resolution Summary:**
Extended the existing new trade idea workflow with optional advisory candidate traceability. Promotion requires an explicit operator action, prefilled candidate context remains editable in the existing modal, and the resulting lifecycle event remains a normal human-owned `decision.trade_idea_created` event with advisory candidate references for traceability only.

**Completed Verification:**

- `uv run pytest tests\test_advisory_candidate.py tests\test_advisory_observation.py`
- `uv run pytest`
- `npm.cmd run build`
- `uv run mypy src\domain\advisory src\services\advisory src\app\api tests\test_advisory_candidate.py`

---

## TF-A014: Prevent Automated Lifecycle Promotion Into TradeIdea

**Status:** Done

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

**Resolution Summary:**
Added explicit operator-promotion intent validation for advisory-candidate promotion and forbids extra lifecycle-command fields on advisory candidate payloads. Advisory ingestion and artifact ingestion paths reject lifecycle authority, recommendation authority, and execution intent attempts.

**Completed Verification:**

- `uv run pytest tests\test_advisory_candidate.py tests\test_advisory_artifact.py`
- `uv run pytest`
- `npm.cmd run build`

---

## TF-A015: Implement Candidate Provenance Visualization

**Status:** Done

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

**Resolution Summary:**
Expanded the candidate review queue detail surface with read-only advisory provenance, candidate/artifact identifiers, source references, evidence artifact IDs, uncertainty, caveats, and captured timestamp. The UI labels provenance as advisory and explicitly excludes scores, execution authority, and lifecycle commands.

**Completed Verification:**

- `npm.cmd run build`
- `uv run pytest tests\test_advisory_candidate.py`

---

## TF-A016: Define External Research Cockpit Import Boundary

**Status:** Done

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

**Resolution Summary:**
Added `DOCS/advisory-artifact-boundary.md` and an `AdvisoryArtifact` domain boundary for imported research, generated advisory artifacts, and markdown advisory artifacts. Imported research requires `imported_research` origin, persists outside `event_ledger`, and can be linked as evidence without becoming canonical truth.

**Completed Verification:**

- `uv run pytest tests\test_advisory_artifact.py`
- `uv run pytest`

---

## TF-A017: Implement Research Artifact Ingestion API

**Status:** Done

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

**Resolution Summary:**
Added `/advisory/artifacts` create/read/list APIs backed by in-memory and Postgres advisory artifact stores. The endpoint accepts source references, provenance, uncertainty, caveats, persona/workspace, metadata, tags, and captured timestamp while rejecting lifecycle authority and canonical recommendation claims.

**Completed Verification:**

- `uv run pytest tests\test_advisory_artifact.py`
- `uv run pytest`

---

## TF-A018: Implement Codex/Claude-Generated Advisory Artifact Support

**Status:** Done

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

**Resolution Summary:**
Generated advisory artifacts now use the same non-canonical artifact boundary with required `codex_generated` or `claude_generated` capture origins. Generated artifacts require source references, provenance, uncertainty, caveats, persona/workspace, and captured timestamp, and they do not append lifecycle or decision events.

**Completed Verification:**

- `uv run pytest tests\test_advisory_artifact.py`
- `uv run pytest`

---

## TF-A019: Implement Advisory Markdown Artifact Persistence

**Status:** Done

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

**Resolution Summary:**
Added markdown advisory artifact persistence with metadata, provenance, caveats, uncertainty, source references, and artifact retrieval/list filters. Markdown bodies remain inert stored text; script-bearing markdown is rejected, and markdown artifact IDs can be linked through `CognitiveEvidence.artifact_id`.

**Completed Verification:**

- `uv run pytest tests\test_advisory_artifact.py`
- `uv run pytest`

---

## TF-A020: Implement Replay-Safe Advisory Snapshot Capture

**Status:** Done

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

**Resolution Summary:**
Artifact ingestion now records a replay-safe advisory snapshot containing captured timestamp, metadata copy, source reference count, caveat count, and body SHA-256 digest. Snapshots remain non-canonical and are returned by advisory artifact APIs without rewriting existing artifacts or ledger events.

**Completed Verification:**

- `uv run pytest tests\test_advisory_artifact.py`
- `uv run pytest`

---

## TF-B001: Define Interpretation Artifact Schema

**Status:** Done

**Classification:** architectural

**Milestone:** M13

**Branch:** `feature/m13-contextual-interpretation-thesis-influence`

**Affected Layer:** domain, services, docs

**Linked ADRs:** ADR-0001, ADR-0006, ADR-0008, ADR-0041, ADR-0042

**Impacted Invariants:** Human Decision Sovereignty, Event Ledger Canonical Truth, Events Are Immutable, Replayability Is Foundational, AI Advisory Boundary, Derived State Must Remain Distinguishable, Terminology Stability

**Problem:**
M13 needs a durable interpretation artifact schema so advisory observations can gain contextual meaning without becoming lifecycle truth, recommendations, thesis revisions, approvals, or execution instructions.

**Implementation Context (M12 Foundation):**
`AdvisoryInterpretation`, `InterpretationKind`, `ThesisInfluence`, `ContextualWeight`, `AdvisoryConfidenceRange`, and `AdvisoryInterpretationStore` were fully defined in M12 (`src/domain/advisory/interpretation.py`). `PostgresAdvisoryInterpretationStore` and `InMemoryAdvisoryInterpretationStore` are also in place. `AdvisoryInterpretationCaptureService` appends `advisory.interpretation_captured` capture-fact events. `InterpretationDraftService` builds AI-assisted interpretation drafts via the `AIAdvisoryProvider` port. This issue verifies schema completeness against ADR-0042, adds any missing test coverage, and confirms the schema is correctly exposed via API.

**Acceptance Criteria:**

- `AdvisoryInterpretation` exists as a non-canonical advisory artifact linked to at least one `AdvisoryObservation` ID.
- Schema captures interpretation ID, artifact ID, linked observation IDs, optional decision/thesis IDs, interpretation kind, thesis influence, contextual weight, confidence range, provenance, caveats, tags, and captured timestamp.
- Interpretation content and rationale persist outside `event_ledger`.
- `advisory.interpretation_captured` records capture facts only and excludes interpretation body text, rationale, recommendations, lifecycle intent, and execution authority.
- Schema validation rejects buy/sell instructions, lifecycle transition intent, plan approval language, and execution instructions as authoritative fields.

---

## TF-B002: Implement Contextual Weighting Framework

**Status:** Done

**Classification:** enhancement

**Milestone:** M13

**Branch:** `feature/m13-contextual-interpretation-thesis-influence`

**Affected Layer:** domain, services, app

**Linked ADRs:** ADR-0006, ADR-0039, ADR-0041, ADR-0042

**Impacted Invariants:** AI Advisory Boundary, Derived State Must Remain Distinguishable, Human Decision Sovereignty, Deterministic Rule Evaluation

**Problem:**
Operators need qualitative contextual weight for interpretations, but the system must avoid hidden scoring engines, deterministic predictive scoring, and recommendation authority.

**Implementation Context (M12 Foundation):**
`ContextualWeight` enum (`low`, `medium`, `high`, `watch`) is defined in M12 (`src/domain/advisory/interpretation.py`) and is a required field on `AdvisoryInterpretation`. The store and query layer already filters by contextual weight. This issue adds a qualitative weight-assignment service that recommends contextual weight based on observation kind and available regime context, and API surfaces that expose weight clearly in interpretation responses.

**Acceptance Criteria:**

- Fixed qualitative contextual weight enum exists for M13 interpretation metadata.
- Contextual weight is stored as advisory metadata on `AdvisoryInterpretation`, not canonical decision state.
- Contextual weight cannot create, revise, approve, reject, or execute lifecycle artifacts.
- API responses label contextual weight as advisory and non-canonical.
- Numeric scoring, opaque ranking, and automated trade recommendation behavior are explicitly out of scope.

---

## TF-B003: Implement Regime-Aware Weighting Model

**Status:** Done

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

**Status:** Done

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

**Status:** Done

**Classification:** enhancement

**Milestone:** M13

**Branch:** `feature/m13-contextual-interpretation-thesis-influence`

**Affected Layer:** domain, services, app

**Linked ADRs:** ADR-0006, ADR-0041, ADR-0042

**Impacted Invariants:** AI Advisory Boundary, Derived State Must Remain Distinguishable, Human Decision Sovereignty, Terminology Stability

**Problem:**
Operators need uncertainty-preserving confidence ranges for interpretations, but M13 must avoid false precision and numeric prediction.

**Implementation Context (M12 Foundation):**
`AdvisoryConfidenceRange` enum (`low`, `medium`, `high`, `unknown`) is defined in M12 (`src/domain/advisory/interpretation.py`) and is a required field on `AdvisoryInterpretation`. This issue adds UX surfaces that display confidence ranges visually and API endpoint coverage that returns confidence range as an explicit advisory metadata field in interpretation queries and summaries.

**Acceptance Criteria:**

- Fixed qualitative advisory confidence range enum exists for `AdvisoryInterpretation`.
- Confidence range requires caveats and provenance when persisted.
- Confidence range is exposed as advisory metadata only.
- Invalid confidence range values fail validation.
- Numeric prediction, probability-as-authority, and hidden model scores are rejected or out of scope.

---

## TF-B006: Implement Thesis Evidence Influence Tracking

**Status:** Done

**Classification:** architectural

**Milestone:** M13

**Branch:** `feature/m13-contextual-interpretation-thesis-influence`

**Affected Layer:** domain, services, app, replay

**Linked ADRs:** ADR-0002, ADR-0006, ADR-0033, ADR-0041, ADR-0042

**Impacted Invariants:** Human Decision Sovereignty, Lifecycle Authority, AI Advisory Boundary, Derived State Must Remain Distinguishable

**Problem:**
Operators need to see how interpreted advisory evidence may influence an existing thesis, while preserving that the system does not revise the thesis or own lifecycle authority.

**Implementation Context (M12 Foundation):**
`ThesisInfluence` enum and the optional `thesis_id` linkage on `AdvisoryInterpretation` were implemented in M12. `ThesisInfluenceSummary` — which counts interpretations by influence label for a given thesis — is implemented in `src/services/advisory/interpretation.py`. This issue extends tracking to expose influence over time (not only current counts), adds API surfaces for thesis influence history, and wires the influence summary into the relevant workspace panel.

**Acceptance Criteria:**

- Interpretations may optionally reference a thesis and store qualitative thesis influence metadata.
- Thesis influence tracking is advisory and does not mutate thesis artifact content or append thesis revision events.
- Influence metadata preserves linked observation IDs, interpretation ID, caveats, provenance, and captured timestamp.
- API responses distinguish advisory influence from canonical thesis content.
- Operator-owned thesis revision remains a separate lifecycle or artifact workflow.

---

## TF-B007: Implement Supporting Vs Weakening Evidence Classification

**Status:** Done

**Classification:** enhancement

**Milestone:** M13

**Branch:** `feature/m13-contextual-interpretation-thesis-influence`

**Affected Layer:** domain, services, app

**Linked ADRs:** ADR-0006, ADR-0041, ADR-0042

**Impacted Invariants:** Human Decision Sovereignty, AI Advisory Boundary, Derived State Must Remain Distinguishable, Terminology Stability

**Problem:**
Interpretations need qualitative classification for whether evidence appears to support, weaken, complicate, or remain neutral toward a thesis, without becoming an automated thesis judgment.

**Implementation Context (M12 Foundation):**
`ThesisInfluence` enum values `SUPPORTING`, `WEAKENING`, `CONFLICTING`, `MIXED`, `NEUTRAL`, `UNKNOWN` are defined in M12. Query filtering by `thesis_influence` is also in place. This issue adds the operator-facing API and workspace surfaces that present the supporting vs weakening evidence split clearly, grouped by linked thesis, with caveats and source provenance visible.

**Acceptance Criteria:**

- Fixed qualitative thesis influence classification exists for support, weaken, neutral, mixed, and unknown cases.
- Classification requires linked observations or evidence references.
- Classification is advisory metadata and cannot revise thesis content, promote lifecycle state, approve plans, or execute trades.
- Mixed or unknown classifications preserve uncertainty and caveats.
- API/UI responses label classification as advisory and non-canonical.

---

## TF-B008: Implement Thesis Drift Detection

**Status:** Done

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

**Status:** Done

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

**Status:** Done

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

**Status:** Done

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

**Status:** Done

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

**Status:** Done

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

**Status:** Done

**Classification:** enhancement

**Milestone:** M13

**Branch:** `feature/m13-contextual-interpretation-thesis-influence`

**Affected Layer:** services, app

**Linked ADRs:** ADR-0006, ADR-0041, ADR-0042

**Impacted Invariants:** AI Advisory Boundary, Human Decision Sovereignty, Historical Integrity, Derived State Must Remain Distinguishable

**Problem:**
Operators need narrative explanations of evidence and interpretation context, including AI-assisted drafts, but generated narratives must require operator acceptance before persistence and must not become canonical truth.

**Dependency:**
TF-F046 (`OpenAICompatibleAdvisoryProvider`) is complete and wired. AI-assisted draft generation can exercise the concrete `AIAdvisoryProvider` boundary.

**Acceptance Criteria:**

- AI-assisted narrative drafts use the existing `AIAdvisoryProvider` boundary.
- Draft narratives are not persisted and do not append events until explicitly accepted or edited by the operator.
- Accepted narratives persist as non-canonical advisory interpretation artifact content.
- Narrative capture appends only allowed advisory capture facts and excludes generated rationale from canonical event truth.
- Generated narratives preserve source IDs, provenance, caveats, uncertainty, and advisory/non-canonical labels.

---

## TF-B015: Implement Contextual Reasoning Timelines

**Status:** Done

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

Current planning now extends through completed M14. TF-C001 through TF-C010 are complete behavioral intelligence work.
TF-F#### series = field-observed / feedback-originated issues, distinct from roadmap TF-#### series.
Historical MVP and M10A notes are retained above for traceability.


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

## TF-F045: Add LiteLLM Credential Shape To CredentialStore

**Status:** Done

**Classification:** enhancement

**Milestone:** M13

**Branch:** `feature/tf-f045-litellm-credential-shape`

**Affected Layer:** domain, security

**Linked ADRs:** ADR-0037

**Impacted Invariants:** Derived State Must Remain Distinguishable, Architectural Simplicity, Historical Integrity

**Source:** LLM adapter strategy session 2026-05-22. See `DOCS/llm-adapter-strategy.md`.

**Problem:**
`CredentialStore` manages market data provider credentials but has no credential shape for LLM providers. M13 advisory tasks (TF-F046–TF-F050) need a concrete LLM provider configured through the existing credential boundary. Without this, the `OpenAICompatibleAdvisoryProvider` cannot retrieve its endpoint or key at runtime without leaking them into code or environment files.

**Scope:**
Add a `litellm` provider type to the security domain with credential fields `base_url`, `api_key`, and `default_model`. Register it through `CredentialStore` using the same `KeyManager` encryption path as existing market data credentials. The credential CLI workflow for setting and rotating LiteLLM credentials must match the existing provider credential workflow.

**Acceptance Criteria:**

- `CredentialStore` can store and retrieve a `litellm` credential with `base_url`, `api_key`, and `default_model` fields.
- LiteLLM credential is encrypted at rest under `TRADEFORGE_MASTER_KEY` using the existing `KeyManager`.
- No LiteLLM base URL, API key, or model string appears in application code, `.env` files, or git history.
- Setting and rotating LiteLLM credentials uses the same CLI workflow as existing market data credentials.
- Credential retrieval fails with a clear error if no `litellm` credential has been configured.

**Resolution Summary:**
Added a typed LiteLLM credential payload under the security boundary with `base_url`, `api_key`, and `default_model` fields. The existing `CredentialStore` remains the encrypted storage mechanism, while `create_litellm_credential()` and `get_litellm_credential()` provide the provider-specific shape and clear not-configured failure. Extended `scripts/manage_credentials.py register litellm` so setting or rotating LiteLLM credentials uses the same encrypted `.keys.enc` workflow as existing providers.

**Completed Verification:**

- `uv run pytest tests\test_credential.py tests\test_key_manager.py tests\test_credential_store.py tests\test_manage_credentials_script.py`
- `uv run ruff check src\security scripts\manage_credentials.py tests\test_credential.py tests\test_key_manager.py tests\test_credential_store.py tests\test_manage_credentials_script.py`
- `uv run mypy src\security scripts\manage_credentials.py tests\test_credential.py tests\test_key_manager.py tests\test_credential_store.py tests\test_manage_credentials_script.py`

---

## TF-F046: Implement OpenAICompatibleAdvisoryProvider

**Status:** Done

**Classification:** architectural

**Milestone:** M13

**Branch:** `feature/tf-f046-openai-compatible-advisory-provider`

**Affected Layer:** infrastructure/advisory, services/advisory, app

**Linked ADRs:** ADR-0006, ADR-0037, ADR-0041, ADR-0042

**Impacted Invariants:** AI Advisory Boundary, Human Decision Sovereignty, Derived State Must Remain Distinguishable

**Source:** LLM adapter strategy session 2026-05-22. See `DOCS/llm-adapter-strategy.md`.

**Problem:**
The `AIAdvisoryProvider` protocol in `src/domain/advisory/` has no concrete implementation. `InterpretationDraftService`, `ReplayAdvisoryService`, and `ReviewAdvisoryService` cannot generate advisory content until a provider is wired. M13 advisory tasks cannot function without this.

**Scope:**
Implement `OpenAICompatibleAdvisoryProvider` in `src/infrastructure/advisory/openai_compatible_provider.py`. Reads `base_url`, `api_key`, and `default_model` from `CredentialStore` via the `litellm` credential shape (TF-F045). Calls the OpenAI chat completions API format (`POST /v1/chat/completions`). This format is supported by LiteLLM, Groq, NVIDIA NIM, and Ollama — provider routing is handled by LiteLLM configuration, not by the adapter. The adapter validates that all responses maintain `authority=ADVISORY`, matching `request_id`, and matching `artifact_kind`. Injected at `create_app()` composition root only.

**Acceptance Criteria:**

- `OpenAICompatibleAdvisoryProvider` implements the `AIAdvisoryProvider` protocol.
- Provider reads all credentials from `CredentialStore`. No key, base URL, or model string in code.
- Provider calls LiteLLM (or any OpenAI-compatible endpoint) using the `/v1/chat/completions` format.
- `AIAdvisoryService.generate()` validates responses for `authority=ADVISORY`, `request_id` match, and `artifact_kind` match.
- Provider is injected only at the composition root. Domain, lifecycle, and replay layers have no import dependency on it.
- If LiteLLM is unreachable, advisory calls raise a typed `AdvisoryProviderUnavailableError` that the API layer handles gracefully without affecting lifecycle operations.
- `InMemoryAdvisoryProvider` stub remains available for tests and demo mode.

---

## TF-F047: Implement Prompt Template And Service Wiring For Replay Summary

**Status:** Done

**Classification:** enhancement

**Milestone:** M13

**Branch:** `feature/tf-f047-advisory-replay-summary-prompt`

**Affected Layer:** services/advisory, app

**Linked ADRs:** ADR-0006, ADR-0008, ADR-0041

**Impacted Invariants:** AI Advisory Boundary, Replayability Is Foundational, Human Decision Sovereignty

**Source:** LLM adapter strategy session 2026-05-22. See `DOCS/llm-adapter-strategy.md`.

**Problem:**
`ReplayAdvisoryService` exists as a boundary but has no prompt serialization logic. Replay summaries cannot be generated until a prompt template packages replay timeline data into an `AdvisoryRequest`. This is the lowest-risk advisory task and the first one to validate the adapter end-to-end.

**Scope:**
Add prompt serializer to `ReplayAdvisoryService` that packages replay timeline events (lifecycle transitions, advisory capture facts, cognitive artifact snapshots) into an `AdvisoryRequest` with `artifact_kind=REPLAY_SUMMARY`. System prompt instructs the LLM to summarize without issuing recommendations, lifecycle transitions, or buy/sell instructions. Add `POST /advisory/replay-summary` API endpoint that accepts a `decision_id` and returns an `AdvisoryResponse`. Generated summary is returned but not persisted — it is an ephemeral advisory output, not a replay event.

**Acceptance Criteria:**

- `ReplayAdvisoryService` serializes replay timeline context into a valid `AdvisoryRequest`.
- System prompt explicitly prohibits recommendation authority, lifecycle transition suggestions, and buy/sell instructions.
- Response maintains `authority=ADVISORY` and does not append events.
- `POST /advisory/replay-summary` accepts a `decision_id` and returns an advisory summary response.
- Response includes source references, provenance summary, and advisory/non-canonical label.
- Empty or insufficient replay timeline returns a graceful advisory-null response, not a server error.

---

## TF-F048: Implement Prompt Template And Service Wiring For Thesis Review Assistant

**Status:** Done

**Classification:** enhancement

**Milestone:** M13

**Branch:** `feature/tf-f048-advisory-thesis-review-prompt`

**Affected Layer:** services/advisory, app

**Linked ADRs:** ADR-0006, ADR-0033, ADR-0041, ADR-0042

**Impacted Invariants:** AI Advisory Boundary, Human Decision Sovereignty, Lifecycle Authority

**Source:** LLM adapter strategy session 2026-05-22. See `DOCS/llm-adapter-strategy.md`.

**Problem:**
No prompt template exists to package a structured thesis artifact into an `AdvisoryRequest`. Operators cannot request advisory review of thesis assumptions, invalidation conditions, or regime alignment through the system. This is the highest operator-value advisory task.

**Scope:**
Add prompt serializer that packages thesis narrative, catalysts, assumptions, invalidation conditions, regime alignment, and confidence level into an `AdvisoryRequest` with `artifact_kind=THESIS_REVIEW`. System prompt instructs the LLM to surface blind spots, missing assumptions, unstated risks, and regime misalignments — without issuing buy/sell instructions, lifecycle recommendations, or plan approval language. Add `POST /advisory/thesis-review` API endpoint accepting `thesis_id`.

**Acceptance Criteria:**

- Thesis review prompt includes all structured thesis fields without lifecycle authority fields.
- System prompt explicitly prohibits buy/sell instructions, lifecycle recommendations, and plan approval language.
- Response maintains `authority=ADVISORY`.
- `POST /advisory/thesis-review` accepts `thesis_id` and returns advisory response.
- Empty or minimal thesis fields return a graceful advisory-null response indicating insufficient context.

---

## TF-F049: Implement Prompt Template And Service Wiring For Advisory Observation Generation

**Status:** Done

**Classification:** enhancement

**Milestone:** M13

**Branch:** `feature/tf-f049-advisory-observation-generation-prompt`

**Affected Layer:** services/advisory, app

**Linked ADRs:** ADR-0006, ADR-0038, ADR-0041, ADR-0042

**Impacted Invariants:** AI Advisory Boundary, Human Decision Sovereignty, Derived State Must Remain Distinguishable, Market Intelligence Is Interpreted Context

**Source:** LLM adapter strategy session 2026-05-22. See `DOCS/llm-adapter-strategy.md`.

**Problem:**
No prompt template exists to generate typed advisory observations from market context. Operators must manually enter all observations or import external documents. The M12 advisory observation pipeline has no LLM-assisted generation path.

**Scope:**
Add `ObservationGenerationAdvisoryService` that packages ticker, market snapshot (price context), fundamentals bundle, and market regime into an `AdvisoryRequest` with `artifact_kind=OBSERVATION_GENERATION`. LLM prompt requests discrete observations across specified `ObservationKind` values. Response is parsed into candidate `AdvisoryObservation` inputs. Operator must explicitly accept before observations are captured — auto-persistence is prohibited per ADR-0042. Accepted observations use `capture_origin=claude_generated`. Add `POST /advisory/generate-observations` API endpoint.

**Acceptance Criteria:**

- Observation generation prompt includes ticker, price context, fundamentals, and regime context.
- System prompt prohibits buy/sell instructions, lifecycle authority, and recommendation framing.
- Response is structured to produce multiple discrete typed observations.
- Operator must explicitly accept before observations are captured. No auto-persist path.
- Accepted observations set `capture_origin=claude_generated` or `capture_origin=codex_generated`.
- `POST /advisory/generate-observations` returns candidate observations for operator review.

---

## TF-F050: Implement Prompt Template And Service Wiring For Candidate Screening

**Status:** Done

**Classification:** enhancement

**Milestone:** M13

**Branch:** `feature/tf-f050-advisory-candidate-screening-prompt`

**Affected Layer:** services/advisory, app

**Linked ADRs:** ADR-0006, ADR-0041

**Impacted Invariants:** AI Advisory Boundary, Human Decision Sovereignty, Derived State Must Remain Distinguishable

**Source:** LLM adapter strategy session 2026-05-22. See `DOCS/llm-adapter-strategy.md`.

**Problem:**
The advisory candidate queue can accumulate candidates faster than an operator can manually triage. No LLM-assisted screening path exists to help the operator decide which candidates deserve attention first.

**Scope:**
Add `CandidateScreeningAdvisoryService` that packages candidate queue contents (ticker, observation summaries, evidence, provenance, uncertainty) into an `AdvisoryRequest` with `artifact_kind=CANDIDATE_SCREENING`. System prompt requests qualitative attention-ranking rationale. Response is returned as advisory commentary only and does not modify candidate records, candidate status, or lifecycle state. Add `POST /advisory/screen-candidates` API endpoint.

**Acceptance Criteria:**

- Screening prompt includes all candidate context fields without lifecycle authority fields.
- System prompt explicitly prohibits candidate promotion, lifecycle changes, buy/sell instructions, and recommendation authority.
- Response maintains `authority=ADVISORY` and does not modify any candidate records.
- `POST /advisory/screen-candidates` returns advisory commentary only.
- Empty candidate queue returns a graceful advisory-null response.

---

## TF-F051: Add On-Demand Advisory API Endpoints And Frontend Trigger Surfaces

**Status:** Done

**Classification:** enhancement

**Milestone:** M13

**Branch:** `feature/tf-f051-advisory-on-demand-endpoints`

**Affected Layer:** app/routes, frontend

**Linked ADRs:** ADR-0006, ADR-0020, ADR-0021, ADR-0042

**Impacted Invariants:** AI Advisory Boundary, Human Decision Sovereignty, UX Is Architectural

**Source:** LLM adapter strategy session 2026-05-22. See `DOCS/llm-adapter-strategy.md`.

**Problem:**
The four advisory task services (TF-F047–TF-F050) need operator-facing trigger surfaces in relevant workspaces. Without API endpoints and frontend buttons, the advisory generation capability is backend-only and not usable from the UI.

**Scope:**
Wire API routes for all four advisory tasks to the FastAPI application. Add frontend trigger buttons in contextually appropriate workspaces: replay summary in `ReplayWorkspace`, thesis review in the thesis authoring surface, observation generation in `ContextWorkbenchWorkspace` or `OpportunityWorkspace`, candidate screening in `OperatingWorkspace` or the advisory panel. All buttons are explicit on-demand triggers only — nothing fires automatically.

**Acceptance Criteria:**

- Four API endpoints are exposed and respond correctly.
- Frontend surfaces include trigger buttons for all four advisory tasks in appropriate workspaces.
- Advisory responses render as clearly labelled non-canonical advisory panels with provenance and caveats visible.
- No automatic triggers. All advisory generation requires explicit operator action.
- Loading states, error states, and LiteLLM unavailability are handled gracefully in the UI.
- Advisory panels do not include approve, execute, buy/sell, or lifecycle-transition controls.

---

## TF-F052: Add Advisory Service Health Check To ProviderConfigurationPanel

**Status:** Done

**Classification:** enhancement

**Milestone:** M13

**Branch:** `feature/tf-f052-advisory-health-check`

**Affected Layer:** app, frontend

**Linked ADRs:** ADR-0006, ADR-0020, ADR-0038

**Impacted Invariants:** UX Is Architectural, AI Advisory Boundary, Architectural Simplicity

**Source:** LLM adapter strategy session 2026-05-22. See `DOCS/llm-adapter-strategy.md`.

**Problem:**
Operators have no visibility into whether the LiteLLM advisory service is reachable before attempting an advisory task. Silent failures (LiteLLM down, no credential configured) produce confusing errors deep inside advisory panels.

**Scope:**
Add `GET /advisory/health` endpoint that checks LiteLLM reachability via a lightweight probe (not a full generation call — no tokens consumed). Returns one of: `available`, `unavailable` (LiteLLM unreachable), or `not_configured` (no `litellm` credential in `CredentialStore`). Surface the result in `ProviderConfigurationPanel` alongside market data provider status.

**Acceptance Criteria:**

- `GET /advisory/health` returns a status distinguishing `available`, `unavailable`, and `not_configured`.
- Health probe does not consume tokens or trigger advisory generation.
- `ProviderConfigurationPanel` shows advisory service status.
- A health check failure does not affect lifecycle, replay, or market data operations.
- `not_configured` state clearly guides the operator toward credential setup.

---

## TF-F053: Validate NVIDIA NIM Via LiteLLM And Document Credential Shape

**Status:** Done

**Classification:** investigation

**Milestone:** M13

**Branch:** `docs/tf-f053-nvidia-nim-litellm-validation`

**Affected Layer:** docs

**Linked ADRs:** ADR-0037

**Impacted Invariants:** Architectural Simplicity

**Source:** LLM adapter strategy session 2026-05-22. See `DOCS/llm-adapter-strategy.md`. NVIDIA NIM free tier is provisioned but untested.

**Problem:**
NVIDIA NIM free tier has been provisioned but not validated via LiteLLM. Rate limits, model strings, and token constraints are undocumented. Without this, the claim that NVIDIA NIM can be added as a LiteLLM route without code changes is unverified.

**Scope:**
Configure NVIDIA NIM as a model route in LiteLLM. Test a basic chat completion call through LiteLLM. Confirm the LiteLLM model string format for at least one NIM model (e.g., `nvidia/meta/llama-3.1-70b-instruct`). Document confirmed rate limits, daily token budgets, and any response format differences. Update `DOCS/llm-adapter-strategy.md` with confirmed NIM credential shape, model strings, and a comparison against Groq free-tier limits. No code changes required in TradeForge.

**Acceptance Criteria:**

- NVIDIA NIM successfully responds to a chat completion call routed through LiteLLM.
- Confirmed LiteLLM model string documented for at least one NIM model.
- `DOCS/llm-adapter-strategy.md` updated with NIM credential shape and confirmed rate limits.
- No TradeForge application code changes required — NIM is a LiteLLM configuration addition.

---

## TF-F054: Document Automatic Enrichment Lifecycle Hook Points

**Status:** Done

**Classification:** documentation

**Milestone:** M13

**Branch:** `docs/tf-f054-auto-enrichment-hook-points`

**Affected Layer:** docs, knowledge-base

**Linked ADRs:** ADR-0006, ADR-0042

**Impacted Invariants:** AI Advisory Boundary, Human Decision Sovereignty, Replayability Is Foundational

**Source:** LLM adapter strategy session 2026-05-22. See `DOCS/llm-adapter-strategy.md`. Automatic enrichment is explicitly deferred from the current on-demand implementation but the hook points need to be specified before the pattern drifts.

**Problem:**
The strategy document defers automatic advisory enrichment on lifecycle events to a future step, but no document specifies which lifecycle events are candidates for automatic triggers, what gating conditions apply, or what the failure behavior should be. Without this, the transition from on-demand to automatic enrichment has no specified shape.

**Scope:**
Define — in `DOCS/llm-adapter-strategy.md` or a new `DOCS/advisory-enrichment-trigger-model.md` — the candidate lifecycle events for automatic advisory enrichment (e.g., thesis captured → observation generation, lifecycle transition to Plan → thesis review, replay session completed → replay summary), the gating conditions for each hook (existing observation coverage, provider availability, per-decision operator opt-in), and the failure behavior (silent skip, degraded-state surface, operator notification). Document explicitly states that automatic enrichment is deferred; this is a specification for when it is eventually implemented.

**Acceptance Criteria:**

- At least six lifecycle events are documented as automatic enrichment candidates.
- Each candidate hook specifies: trigger event, advisory task, gating conditions, failure behavior.
- Document explicitly states automatic enrichment is deferred from current implementation.
- No runtime code changes.

---


## TF-F055: Implement UI-Based Credential Management

**Status:** Done

**Classification:** enhancement

**Milestone:** M13

**Branch:** `feature/tf-f055-ui-credential-management`

**Affected Layer:** security, app, frontend, docs

**Linked ADRs:** ADR-0037 (amended)

**Impacted Invariants:** Architectural Simplicity, Derived State Must Remain Distinguishable, Historical Integrity

**Source:** Operational friction identified after M10C implementation. Entering API keys via CLI is cumbersome for routine operation.

**Problem:**
Entering and rotating provider API keys requires terminal access and knowledge of the `manage_credentials.py` CLI. An operator should be able to configure market data and AI provider credentials from the browser UI without touching a terminal after the initial master key setup.

**Scope:**
- `ProviderBootstrapService` in `src/app/api/application.py` — in-process provider reload after credential change
- `src/app/api/admin_routes.py` (new) — `GET/PUT/DELETE /admin/credentials/{provider_id}`
- `frontend/src/api/runtime.ts` — `PROVIDER_CREDENTIAL_SCHEMAS`, `fetchCredentials()`, `updateCredential()`, `revokeCredential()`
- `frontend/src/workspaces/ProviderConfigurationPanel.tsx` — credential section with inline forms
- `DOCS/adr/0037-operational-credential-boundary.md` — amendment section
- `DOCS/credential-ui-strategy.md` (new) — design document
- Fix `_default_fundamentals_providers()` to only call `KeyManager` when credentials to decrypt actually exist

**Acceptance Criteria:**

- Operator can enter, view (masked), and rotate provider credentials from the ProviderConfigurationPanel.
- Secrets are never returned from GET — only last 4 characters of secret fields shown.
- TRADEFORGE_MASTER_KEY remains in the OS environment; it cannot be configured via UI.
- Providers reload automatically after credential save — no restart required.
- PUT returns 503 if master key is not set in the environment.
- DELETE sets status=REVOKED and preserves the record for audit trail.
- yfinance shows as always-active with no credential required.
- litellm base_url and default_model (non-secret) display in full.
- 13 new tests covering all credential management scenarios.

**Resolution Summary:**
Implemented `ProviderBootstrapService` attached to `app.state.provider_bootstrap` with a `reload()` method that rebuilds market/fundamentals/registry services in-place. Added `/admin/credentials` endpoints that encrypt via `KeyManager`, write to `CredentialStore`, and trigger reload. Extended `ProviderConfigurationPanel` with per-provider credential rows (configured badge, masked field display, inline form, revoke button). Added `PROVIDER_CREDENTIAL_SCHEMAS` static registry and three API functions to `runtime.ts`. Fixed `_default_fundamentals_providers()` to only invoke `KeyManager` when credentials actually exist, preventing `MasterKeyNotConfiguredError` in test environments with empty stores.

**Completed Verification:**

- `uv run pytest` — 745 tests pass
- `uv run mypy src tests` — no type errors
- `uv run ruff check .` — no lint errors
- `npm.cmd run typecheck && npm.cmd run build` — frontend compiles cleanly

---

## TF-F056: Fix Missing Default Advisory Provider Bootstrap After Merge

**Status:** Done

**Classification:** bug

**Milestone:** M13

**Branch:** `fix/tf-f056-default-advisory-provider-bootstrap`

**Affected Layer:** app, infrastructure/advisory, security

**Linked ADRs:** ADR-0006, ADR-0037

**Impacted Invariants:** AI Advisory Boundary, Human Decision Sovereignty, Architectural Simplicity

**Source:** Docker startup feedback captured in `knowledge/raw/feedback docker compose up bug.md`.

**Problem:**
`docker compose up` crashes during application import because `create_app()` calls `_default_advisory_provider(_credential_store)` but `_default_advisory_provider` is not defined. The missing helper appears to have been lost during a merge conflict resolution.

**Scope:**
Restore the default advisory provider bootstrap helper in `src/app/api/application.py`. The helper should return `None` when LiteLLM credentials are absent or unreadable, and construct `OpenAICompatibleAdvisoryProvider` only when the existing `CredentialStore` contains a valid `litellm` credential that can be decrypted through `KeyManager`.

**Acceptance Criteria:**

- `create_app()` starts without raising `NameError` when no LiteLLM credential is configured.
- `GET /advisory/health` returns `not_configured` when no advisory provider can be built.
- `create_app()` builds an `OpenAICompatibleAdvisoryProvider` when a valid `litellm` credential is present.
- Missing or unreadable LiteLLM credentials do not prevent lifecycle, replay, workspace, market, or admin routes from starting.
- No lifecycle, replay, event, credential schema, frontend, or Docker Compose behavior changes are introduced.

**Resolution Summary:**
Restored `_default_advisory_provider()` in `src/app/api/application.py`. The composition helper now returns `None` when LiteLLM credentials are absent, missing a master key, unreadable, or invalid, preserving app startup and advisory not-configured behavior. When a valid `litellm` credential is present, it constructs `OpenAICompatibleAdvisoryProvider` from the existing credential boundary. Also restored the missing `MasterKeyNotConfiguredError` import used by provider reload.

**Completed Verification:**

- `uv run pytest tests\test_default_advisory_provider_bootstrap.py tests\test_advisory_schema_m13_verification.py tests\test_admin_credentials.py tests\test_openai_compatible_provider.py tests\test_credential_store.py`
- `uv run pytest`
- `uv run ruff check src\app\api\application.py tests\test_default_advisory_provider_bootstrap.py`
- `uv run mypy src\app\api\application.py tests\test_default_advisory_provider_bootstrap.py`
- `npm.cmd run typecheck`
- `npm.cmd run build`
- `docker compose run --rm tradeforge uv run python -c "from src.app.api.application import app; print(app.title)"`

---

## TF-F057: Add Optional LiteLLM Docker Compose Runtime Service

**Status:** Done

**Classification:** operational

**Milestone:** M13

**Branch:** `feature/tf-f057-litellm-compose-service`

**Affected Layer:** infrastructure, docs

**Linked ADRs:** ADR-0011, ADR-0037, ADR-0041, ADR-0042

**Impacted Invariants:** AI Advisory Boundary, Human Decision Sovereignty, Architectural Simplicity, Derived State Must Remain Distinguishable

**Source:** Operator observation captured on 2026-05-23 in `knowledge/raw/brainstorm-20260523-litellm-compose-runtime.md`.

**Problem:**
TradeForge has a LiteLLM-backed advisory provider and documentation assumes a local LiteLLM proxy is available at `http://localhost:4000`, but the Docker Compose runtime only starts TradeForge and Postgres. Operators who run the local stack do not have a reproducible LiteLLM service to host the OpenAI-compatible advisory endpoint.

**Scope:**
Add an optional LiteLLM service to `docker-compose.yml`, expose it on host port `4000`, add a secret-free LiteLLM config file that reads provider API keys from environment variables, update setup documentation with host-vs-container base URL guidance, and add focused compose/documentation tests. The service must remain optional and must not make AI advisory mandatory for lifecycle, replay, market context, or credential-management workflows.

**Acceptance Criteria:**

- `docker-compose.yml` defines a LiteLLM service that exposes port `4000`.
- The LiteLLM service is optional and does not break the default TradeForge + Postgres runtime when provider API keys are absent.
- LiteLLM provider API keys are read from operator environment variables and are not committed to Git.
- Documentation explains when to use `http://localhost:4000` versus `http://litellm:4000` for the TradeForge `litellm` credential.
- The Compose configuration validates with `docker compose config`.
- Focused tests verify the Compose LiteLLM service and secret-free configuration.

**Implementation Summary:**
Added an optional `litellm` service under the Compose `advisory` profile, exposed on host port `4000`, using the official LiteLLM Docker image documented by LiteLLM. Added `litellm_config.yaml` with model aliases for Groq, NVIDIA NIM, and Ollama while reading all provider keys from environment variables. Updated README and credential setup docs to distinguish `http://localhost:4000` for host-run backend from `http://litellm:4000` for container-run backend. Added focused tests covering the Compose service and secret-free config.

**Completed Verification:**

- `uv run pytest tests\test_postgres_compose.py`
- `docker compose config`
- `docker compose --profile advisory config`
- `uv run pytest`
- `npm.cmd run typecheck`
- `npm.cmd run build`
- `docker compose --profile advisory up -d litellm`
- `docker compose --profile advisory ps litellm` confirms `tradeforge-litellm-1` is running and publishes `0.0.0.0:4000->4000/tcp`
- `Invoke-WebRequest http://localhost:4000/health/readiness` returns HTTP 200 with `status=healthy`

---

## TF-F058: Allow Frontend npm Commands From Repository Root

**Status:** Done

**Classification:** bug

**Milestone:** M13

**Branch:** `fix/tf-f058-root-npm-frontend-scripts`

**Affected Layer:** developer tooling, docs

**Linked ADRs:** ADR-0011, ADR-0021

**Impacted Invariants:** Architectural Simplicity, UX Is Architectural, Domain Integrity Rules

**Source:** Operator terminal failure captured on 2026-05-23 in `knowledge/raw/brainstorm-20260523-root-npm-dev-enoent.md`.

**Problem:**
Running `npm run dev` from the repository root fails with `ENOENT` because the frontend package lives under `frontend/` and there is no root `package.json`. The documented workflow says to `cd frontend`, but the failure mode is a generic npm error rather than a TradeForge-specific operational path.

**Scope:**
Add a root npm script shim that delegates common frontend commands to `frontend/`, update README command examples, and add a focused test to ensure the root scripts remain thin delegations. The frontend package remains under `frontend/` per ADR-0021.

**Acceptance Criteria:**

- `npm run dev` from the repository root resolves to the frontend Vite dev command.
- Root `typecheck`, `build`, and `lint` scripts delegate to the frontend package.
- Root `package.json` does not duplicate frontend dependencies.
- README documents root-level frontend commands.
- Focused tests verify root script delegation.

**Resolution Summary:**
Added a root `package.json` that delegates common npm commands to the existing frontend package through `npm --prefix frontend`. The root package owns no dependencies and does not move or duplicate the React/Vite frontend boundary. README quick-start and frontend setup now use root-level commands, including `npm run install:frontend` for dependency installation.

**Completed Verification:**

- `uv run pytest tests\test_frontend_root_scripts.py`
- `npm.cmd run dev -- --help`
- `uv run pytest`
- `npm.cmd run typecheck`
- `npm.cmd run build`

---

## TF-F059: Formalize M13A Provider Governance Roadmap

**Status:** Done

**Classification:** planning

**Milestone:** M13A

**Branch:** `docs/tf-f059-m13a-provider-governance-roadmap`

**Affected Layer:** docs, knowledge-base

**Linked ADRs:** ADR-0006, ADR-0032, ADR-0037, ADR-0038, ADR-0041, ADR-0042

**Impacted Invariants:** Human Decision Sovereignty, AI Advisory Boundary, Derived State Must Remain Distinguishable, Replayability Is Foundational, UX Is Architectural, Architectural Simplicity

**Source:** Processed M13A synthesis captured in `knowledge/processed/20260523-provider-governance-ai-gateway-configuration-synthesis.md` and supporting raw notes.

**Problem:**
Provider credentials, provider selection, capability routing, LiteLLM routing, health checks, diagnostics, fallback behavior, and contextual provenance have grown into a larger external-systems governance problem. Roadmap v2 did not yet contain M13A, and the local issue register did not break the work into trackable implementation issues.

**Scope:**
Add `M13A - Provider Governance And AI Gateway Configuration` to Roadmap v2 between M13 and M14. Add detailed issue-register entries for TF-F059 through TF-F068. Capture the planning pass in the knowledge-base raw folder for traceability.

**Acceptance Criteria:**

- Roadmap v2 includes M13A as a planned milestone.
- M13A is framed as external systems governance and AI routing infrastructure.
- The issue register includes TF-F059 through TF-F068 with titles, milestones, affected layers, ADRs, invariants, problem statements, scope, and acceptance criteria.
- M13A explicitly preserves human decision sovereignty and the AI advisory boundary.
- M13A distinguishes `Credential != Provider != Capability != Model`.
- No runtime behavior changes are introduced by this issue.

**Resolution Summary:**
Added M13A to Roadmap v2, added detailed M13A issue entries to the local issue register, and captured the plan in the knowledge-base raw folder. Reverted an earlier accidental frontend rail change that was based on a narrower interpretation of provider configuration.

---

## TF-F060: Define Provider Governance Control Surface Design

**Status:** Done

**Classification:** design

**Milestone:** M13A

**Branch:** `docs/tf-f060-provider-governance-control-surface`

**Affected Layer:** docs, frontend/design

**Linked ADRs:** ADR-0032, ADR-0037, ADR-0038

**Impacted Invariants:** UX Is Architectural, Workflow-Centric Architecture, Derived State Must Remain Distinguishable, Human Decision Sovereignty

**Source:** M13A synthesis and source raw notes describing provider configuration as an operational control plane rather than a right-rail form.

**Problem:**
The current provider configuration surface is embedded in contextual workflow rails. That mixes contextual cognition, provider administration, credential management, capability routing, and infrastructure diagnostics in a cramped surface. This risks making provider governance look like a small settings form instead of an explicit external-systems control plane.

**Scope:**
Create a design note for the provider governance control surface. The design must define the intended modules: Overview, Credentials, Market Data Providers, Broker Providers, AI Gateway, Capability Routing, and Diagnostics. It must clarify that this surface is not a canonical decision workspace, even if the runtime routes to a page or module named Provider Configuration.

**Acceptance Criteria:**

- A design document defines the provider governance surface, navigation model, and major sections.
- The design explicitly separates governance/admin concerns from contextual workflow cognition.
- Contextual rails are specified as status, provenance, freshness, fallback, advisory warning, and configure-link surfaces only.
- The design includes visible advisory/non-canonical boundary language.
- The design does not introduce lifecycle actions, trade execution actions, or AI decision authority.

**Out Of Scope:**

- Implementing the frontend surface.
- Implementing new API endpoints.
- Changing provider routing behavior.

**Resolution Summary:**
Added `DOCS/provider-governance-control-surface.md`, defining Provider Governance as an external-systems control surface rather than a canonical workspace. The design specifies Overview, Credentials, Market Data Providers, Broker Providers, AI Gateway, Capability Routing, Diagnostics, contextual rail rules, navigation boundaries, and authority limits.

**Completed Verification:**

- `git diff --check`
- `rg -n "Provider Governance Control Surface|Contextual Rail Rule|TF-F060" DOCS`

---

## TF-F061: Define Capability Routing Governance Model

**Status:** Done

**Classification:** design

**Milestone:** M13A

**Branch:** `docs/tf-f061-capability-routing-governance`

**Affected Layer:** docs, app/services

**Linked ADRs:** ADR-0032, ADR-0038

**Impacted Invariants:** Derived State Must Remain Distinguishable, Replayability Is Foundational, Architectural Simplicity

**Source:** M10D provider capability architecture and M13A synthesis.

**Problem:**
TradeForge already separates provider identity from provider capability, but governance of capability routes remains shallow. As provider count grows, operator-facing configuration must continue to reason in capabilities and advisory intent rather than raw vendors.

**Scope:**
Define the governance model for capability-first routing. Cover price snapshots, fundamentals, AI advisory, and future broker/paper trading as separate capabilities. Preserve deterministic primary plus ordered fallback routing as the default policy unless a future issue explicitly changes it.

**Acceptance Criteria:**

- The model documents provider identity, provider capability, configured provider, selected provider, and fallback route as distinct concepts.
- The model preserves deterministic primary plus ordered fallback routing for M13A.
- The model specifies what route/provenance data should be visible to operators.
- The model identifies replay-relevant route data without declaring it canonical event-ledger truth.
- The model states that provider capability outputs remain read-only, advisory, and non-authoritative.

**Out Of Scope:**

- Weighted routing policies.
- Workspace-scoped routing policies.
- Broker execution integration.

**Resolution Summary:**
Added `DOCS/capability-routing-governance-model.md`, defining capability-first provider routing for M13A. The model preserves deterministic preferred-plus-fallback selection, distinguishes provider identity from provider capability and selected provider, specifies operator visibility requirements, and records replay/provenance constraints without making route state canonical ledger truth.

**Completed Verification:**

- `git diff --check`
- `rg -n "Capability Routing Governance Model|Default Routing Policy|TF-F061" DOCS`

---

## TF-F062: Define AI Gateway And Route Alias Model

**Status:** Done

**Classification:** design

**Milestone:** M13A

**Branch:** `docs/tf-f062-ai-gateway-route-aliases`

**Affected Layer:** docs, infrastructure/advisory, services/advisory

**Linked ADRs:** ADR-0006, ADR-0037, ADR-0041, ADR-0042

**Impacted Invariants:** AI Advisory Boundary, Human Decision Sovereignty, Derived State Must Remain Distinguishable, Terminology Stability

**Source:** M13A synthesis and LLM adapter strategy.

**Problem:**
LiteLLM is currently easy to treat as one provider with one credential and one model string. Architecturally, LiteLLM is a gateway and routing boundary that can map TradeForge advisory roles to multiple underlying providers and models. Hardcoding raw model names into workflow logic would weaken provider flexibility and replay interpretation.

**Scope:**
Define LiteLLM as an AI gateway and define TradeForge-facing route aliases. Representative aliases include `tf-fast`, `tf-reasoning`, `tf-long-context`, `tf-cheap`, and `tf-local`. Define how advisory tasks should refer to semantic roles rather than raw model names.

**Acceptance Criteria:**

- LiteLLM is documented as gateway, model router, and policy boundary.
- AI route aliases are documented as TradeForge-facing operational roles, not canonical decision facts.
- The model distinguishes route alias, gateway URL, underlying provider, model, fallback route, and advisory usage domain.
- Advisory services must not depend on raw provider/model names in workflow logic once route aliases are implemented.
- The document preserves AI advisory-only authority and excludes buy/sell, approval, and lifecycle-transition authority.

**Out Of Scope:**

- Implementing a generalized orchestration engine.
- Adding new LLM providers directly to TradeForge.
- Automatic model selection by hidden heuristics.

**Resolution Summary:**
Added `DOCS/ai-gateway-route-alias-model.md`, defining LiteLLM as an AI gateway and route boundary rather than an ordinary provider. The model defines route aliases, advisory task mappings, gateway visibility requirements, credential boundary rules, replay/provenance expectations, and authority limits.

**Completed Verification:**

- `git diff --check`
- `rg -n "AI Gateway And Route Alias Model|tf-reasoning|TF-F062" DOCS`

---

## TF-F063: Define Provider Diagnostics And Health History Model

**Status:** Done

**Classification:** design

**Milestone:** M13A

**Branch:** `docs/tf-f063-provider-diagnostics-health-history`

**Affected Layer:** docs, app, infrastructure

**Linked ADRs:** ADR-0032, ADR-0037, ADR-0038, ADR-0042

**Impacted Invariants:** Replayability Is Foundational, Derived State Must Remain Distinguishable, Historical Integrity, Architectural Simplicity

**Source:** M13A synthesis open questions about provider health, route availability, validation, and replay implications.

**Problem:**
Provider and gateway failures are operationally meaningful, but the system does not yet distinguish ephemeral health state, retained diagnostic history, replay-visible route provenance, and canonical event-ledger truth. Without a model, later implementation may either lose useful diagnostics or over-promote provider state into canonical events.

**Scope:**
Define diagnostics and health-history semantics for provider unreachable, credential invalid, route unavailable, quota exceeded, fallback triggered, latency spike, validation succeeded, validation failed, and replay nondeterminism warning.

**Acceptance Criteria:**

- The model distinguishes ephemeral health, retained operational diagnostics, replay-visible context, and canonical event truth.
- The model defines which diagnostic fields are operator-visible.
- The model defines whether each diagnostic class is session-only, retained as operational history, or captured through advisory provenance.
- Replay reconstruction must not call live providers to reconstruct historical health or route state.
- The model explicitly avoids event-ledger writes for provider health unless a future ADR authorizes them.

**Out Of Scope:**

- Implementing storage for diagnostics.
- Adding health check endpoints.
- Changing event taxonomy.

**Resolution Summary:**
Added `DOCS/provider-diagnostics-health-history-model.md`, defining diagnostic state classes, provider/gateway diagnostic categories, retention rules, operator visibility, replay rules, and event taxonomy implications. The model keeps provider health and diagnostics operational by default and avoids promoting them into canonical event-ledger truth.

**Completed Verification:**

- `git diff --check`
- `rg -n "Provider Diagnostics And Health History Model|Replay Nondeterminism Warning|TF-F063" DOCS`

---

## TF-F064: Implement Provider Governance Read APIs

**Status:** Done

**Classification:** feature

**Milestone:** M13A

**Branch:** `feature/tf-f064-provider-governance-read-apis`

**Affected Layer:** app, services, security

**Linked ADRs:** ADR-0032, ADR-0037, ADR-0038, ADR-0042

**Impacted Invariants:** Derived State Must Remain Distinguishable, AI Advisory Boundary, Human Decision Sovereignty, Architectural Simplicity

**Depends On:** TF-F060, TF-F061, TF-F062, TF-F063

**Problem:**
The frontend cannot render a real provider governance control surface from the current narrow rail-oriented endpoints alone. It needs a read model that combines provider registry, capability routing, credential status, health summary, advisory boundary metadata, and AI gateway status without exposing secrets.

**Scope:**
Add read-only provider governance API contracts and composition logic. The APIs expose configured providers, supported capabilities, current resolution, credential status, health/diagnostic summary, and AI gateway status. They must not return secret values.

**Acceptance Criteria:**

- API contracts expose provider governance overview data without returning secrets.
- Capability route data includes primary, fallback, selected provider, and degraded/fallback state where available.
- Credential data includes configured/missing/revoked/invalid/untested status without plaintext secrets.
- AI gateway data includes reachability and configured route aliases where available.
- Responses clearly distinguish operational/advisory state from canonical lifecycle state.
- Existing lifecycle, replay, workspace, market context, and advisory endpoints continue to behave unchanged.

**Out Of Scope:**

- Credential writes.
- Route writes.
- Diagnostics persistence unless defined by TF-F063 and explicitly scoped.

**Resolution Summary:**
Implemented `GET /provider-governance` as a read-only operational governance
API. The response composes provider descriptors, credential status without
credential values, capability route resolution, diagnostic class metadata, and
LiteLLM AI gateway route-alias metadata. The endpoint marks the read model as
non-canonical, lifecycle-authority false, and event-ledger-writes false.

**Completed Verification:**

- `uv run pytest tests/test_provider_governance_api.py tests/test_fundamentals_overlay.py tests/test_admin_credentials.py tests/test_default_advisory_provider_bootstrap.py`
- `uv run mypy src\app\api\routes.py tests\test_provider_governance_api.py`
- `uv run ruff check tests\test_provider_governance_api.py`
- `git diff --check`

**Verification Note:**
Full `uv run ruff check src\app\api\routes.py tests\test_provider_governance_api.py`
still reports pre-existing long-line and FastAPI `Query(...)` default findings
in `src/app/api/routes.py` outside the TF-F064 changes. TF-F064 import ordering
was fixed with `ruff --fix`, and the new test file passes ruff.

---

## TF-F065: Implement Credential Validation And Test Workflow

**Status:** Done

**Classification:** feature

**Milestone:** M13A

**Branch:** `feature/tf-f065-credential-validation-test-workflow`

**Affected Layer:** security, app, frontend

**Linked ADRs:** ADR-0037, ADR-0038

**Impacted Invariants:** Derived State Must Remain Distinguishable, Historical Integrity, Architectural Simplicity

**Depends On:** TF-F060, TF-F063, TF-F064

**Problem:**
UI credential management can save, mask, rotate, and revoke credentials, but operators still lack explicit validation/test workflow, last validation timestamp, and clear invalid versus untested state. This can create false confidence that configured credentials are operationally usable.

**Scope:**
Add credential validation/test behavior for configured providers. Surface configured, missing, invalid, revoked, and untested states. Preserve the master-key rule: `TRADEFORGE_MASTER_KEY` remains OS environment configuration and cannot be set through UI.

**Acceptance Criteria:**

- Operators can trigger a validation/test action for supported provider credentials.
- Validation records last validation timestamp and visible success/failure state.
- Invalid credentials are distinguishable from missing, revoked, and untested credentials.
- Validation failures show safe operator-facing failure reasons without leaking secrets.
- Credential rotation and removal remain available and auditable.
- Secrets are never returned in API responses or written to logs.

**Out Of Scope:**

- Automatic credential rotation.
- External secrets managers.
- Making credential status canonical event-ledger truth.

**Resolution Summary:**
Added explicit credential validation through
`POST /admin/credentials/{provider_id}/validate`. Validation decrypts the
saved credential with the OS-provided master key, verifies required fields,
persists `last_validated_at` on success, and marks unreadable or malformed
credentials as `invalid` without exposing secret values. Added `invalid` to
credential status, surfaced `last_validated_at` in credential status responses,
updated provider governance status mapping, and added a frontend API helper for
triggering validation.

**Completed Verification:**

- `uv run pytest tests/test_admin_credentials.py tests/test_provider_governance_api.py tests/test_default_advisory_provider_bootstrap.py`
- `uv run mypy src\app\api\admin_routes.py src\app\api\routes.py tests\test_admin_credentials.py tests\test_provider_governance_api.py`
- `uv run ruff check src\app\api\admin_routes.py tests\test_admin_credentials.py tests\test_provider_governance_api.py`
- `npm.cmd run typecheck`
- `git diff --check`

---

## TF-F066: Implement AI Gateway Route Visibility

**Status:** Done

**Classification:** feature

**Milestone:** M13A

**Branch:** `feature/tf-f066-ai-gateway-route-visibility`

**Affected Layer:** infrastructure/advisory, app, frontend

**Linked ADRs:** ADR-0006, ADR-0037, ADR-0041, ADR-0042

**Impacted Invariants:** AI Advisory Boundary, Human Decision Sovereignty, Derived State Must Remain Distinguishable, UX Is Architectural

**Depends On:** TF-F062, TF-F064

**Problem:**
Operators can configure a LiteLLM credential, but the UI does not make clear that LiteLLM is a gateway with route aliases and underlying model/provider resolution. Advisory failures or degraded route behavior can therefore appear as generic AI errors.

**Scope:**
Expose LiteLLM gateway reachability, configured gateway URL, default advisory route, route aliases, underlying provider/model resolution where available, degraded/fallback state, and advisory usage domains.

**Acceptance Criteria:**

- Provider governance surfaces show LiteLLM as AI gateway, not ordinary data provider.
- Route aliases are visible with advisory roles such as fast summary, reasoning, long-context analysis, cheap classification, and local/offline where configured.
- Gateway reachability and route availability are visible without consuming generation tokens.
- Underlying provider/model details are shown only as operational routing metadata, not workflow semantics.
- Advisory services remain explicit operator-triggered assistance and cannot approve, execute, or transition lifecycle state.

**Out Of Scope:**

- Editing LiteLLM's external config file from TradeForge unless separately scoped.
- Multi-agent orchestration.
- Cost optimization engines.

**Resolution Summary:**
Extended provider governance AI gateway visibility and added
`GET /provider-governance/ai-gateway`. The endpoint exposes LiteLLM as gateway
metadata, safely showing gateway URL, default model/route target, inferred
underlying provider, route aliases, advisory usage domains, route availability,
and non-generative reachability state without returning API keys. Frontend API
types and a fetch helper were added for the AI gateway visibility read model.

**Completed Verification:**

- `uv run pytest tests/test_provider_governance_api.py tests/test_default_advisory_provider_bootstrap.py`
- `uv run mypy src\app\api\routes.py tests\test_provider_governance_api.py`
- `uv run ruff check tests\test_provider_governance_api.py`
- `npm.cmd run typecheck`

---

## TF-F067: Implement Provider Governance Frontend Surface And Rail Cleanup

**Status:** Done

**Classification:** feature

**Milestone:** M13A

**Branch:** `feature/tf-f067-provider-governance-surface`

**Affected Layer:** frontend

**Linked ADRs:** ADR-0021, ADR-0032, ADR-0037, ADR-0038, ADR-0042

**Impacted Invariants:** UX Is Architectural, Workspaces Are Operational Environments, Workflow-Centric Architecture, Derived State Must Remain Distinguishable

**Depends On:** TF-F060, TF-F064, TF-F065, TF-F066

**Problem:**
Contextual rails currently carry provider administration controls that compete with decision cognition. M13A requires a dedicated provider governance surface while preserving rails as contextual, provenance-oriented surfaces.

**Scope:**
Implement the provider governance frontend surface and simplify contextual rails. The surface should expose Overview, Credentials, Market Data Providers, Broker Providers, AI Gateway, Capability Routing, and Diagnostics as defined by TF-F060. Rails should show provider source, selected capability, health, freshness, fallback, advisory boundary, and a configure link.

**Acceptance Criteria:**

- A provider governance surface is reachable from the application shell/navigation without being represented as a canonical decision workspace.
- Credential administration no longer lives as long-form right-rail workflow UI.
- Contextual rails remain focused on decision context, provenance, freshness, fallback, health, and advisory warnings.
- The surface renders credential status, capability routing, AI gateway status, and diagnostics from provider governance read APIs.
- UI copy preserves advisory/non-canonical boundaries and does not imply provider data owns lifecycle truth.
- Existing decision workspaces remain usable without configuring non-required providers.

**Out Of Scope:**

- Full visual redesign of all workspaces.
- Autonomous provider selection policies.
- Broker execution workflows.

**Resolution Summary:**
Added a dedicated Provider Governance frontend surface at
`/workspaces/provider-governance`, reachable from shell navigation. The surface
renders provider governance overview data, diagnostics, LiteLLM AI gateway
route visibility, existing provider routing controls, credential management,
and the credential validation action. Contextual rails now use a compact
provider status rail with selected price/fundamentals providers, fallback
summary, AI gateway status, and a configure link instead of long-form
credential administration.

**Completed Verification:**

- `npm.cmd run typecheck`
- `npm.cmd run build`
- `uv run pytest tests/test_provider_governance_api.py tests/test_admin_credentials.py`

---

## TF-F068: M13A Verification And M14 Readiness Gate

**Status:** Done

**Classification:** verification

**Milestone:** M13A

**Branch:** `docs/tf-f068-m13a-readiness-gate`

**Affected Layer:** docs, app, frontend, tests

**Linked ADRs:** ADR-0006, ADR-0032, ADR-0037, ADR-0038, ADR-0041, ADR-0042

**Impacted Invariants:** Human Decision Sovereignty, AI Advisory Boundary, Derived State Must Remain Distinguishable, Replayability Is Foundational, UX Is Architectural

**Depends On:** TF-F060, TF-F061, TF-F062, TF-F063, TF-F064, TF-F065, TF-F066, TF-F067

**Problem:**
Before M14 behavioral intelligence work begins, provider governance must be verified as an operational support layer that does not create lifecycle authority, AI authority, or hidden canonical state.

**Scope:**
Run the M13A readiness gate. Verify docs, APIs, frontend surfaces, diagnostics, credential workflows, gateway route visibility, and rail cleanup against M13A acceptance meaning and system invariants.

**Acceptance Criteria:**

- M13A implementation issues are complete or explicitly deferred with rationale.
- Provider governance does not mutate lifecycle state or write canonical decision facts.
- AI gateway and route alias behavior remains advisory and operator-visible.
- Credential and diagnostic APIs do not leak secrets.
- Replay-facing provider/gateway provenance is either captured historically or explicitly marked unavailable; replay does not call live providers to reconstruct historical external-system state.
- Frontend typecheck/build and focused backend tests pass.
- Roadmap v2 and issue register are updated with M13A completion status when accepted.

**Out Of Scope:**

- Starting M14 implementation.
- Expanding AI advisory beyond accepted M13A boundaries.

**Resolution Summary:**
Added `DOCS/m13a-readiness-gate.md` and accepted M13A as complete. Verified
that provider governance remains operational/advisory, does not mutate
lifecycle state, does not write canonical decision facts, does not leak
secrets, preserves AI advisory boundaries, and moves long-form provider
administration out of contextual rails.

**Completed Verification:**

- `uv run pytest tests/test_provider_governance_api.py tests/test_admin_credentials.py tests/test_fundamentals_overlay.py tests/test_default_advisory_provider_bootstrap.py`
- `uv run mypy src\app\api\admin_routes.py src\app\api\routes.py src\security\credential.py tests\test_admin_credentials.py tests\test_provider_governance_api.py`
- `npm.cmd run typecheck`
- `npm.cmd run build`
- `git diff --check`

---

## TF-F069: Provider Governance UI Broken — JSON Parse Failure On Load

**Status:** Done

**Classification:** bug

**Milestone:** M14

**Branch:** `fix/tf-f069-provider-governance-json-parse`

**Affected Layer:** frontend, api

**Linked ADRs:** ADR-0032, ADR-0037, ADR-0038

**Impacted Invariants:** UX Is Architectural

**Depends On:** TF-F067

**Problem:**
The Provider Governance section of the UI fails to render on load. The user sees only three lines (skeleton/empty state) with no content. The browser console reports:

```
JSON.parse: unexpected character at line 1 column 1 of the JSON data
```

This indicates the frontend is receiving a non-JSON response (likely an HTML error page, empty body, or plain-text error) from the provider governance API endpoint instead of a valid JSON payload. The root cause is unknown — candidates include the API route not being mounted, returning a 404 HTML page, the backend throwing an unhandled exception before JSON serialization, or a misconfigured Content-Type header.

**Scope:**

- Identify which provider governance API endpoint is returning non-JSON.
- Confirm whether the backend route is mounted and reachable.
- Fix the API to return valid JSON in all cases (success and error).
- Ensure the frontend handles API errors gracefully with a visible error state rather than a silent empty/skeleton render.

**Acceptance Criteria:**

- The Provider Governance section loads and displays content without a JSON parse error.
- The browser console is free of JSON parse errors on the Provider Governance route.
- If the API returns an error, the frontend displays an explicit error message rather than an empty skeleton.
- Backend returns `Content-Type: application/json` for all provider governance endpoints.
- Existing provider governance tests continue to pass.

**Out Of Scope:**

- Redesigning the provider governance UI layout.
- Adding new provider governance features.

**Resolution Summary:**
Root cause: `/provider-governance` and `/admin` were missing from `frontend/vite.config.ts`.
Vite served the React SPA shell (HTML) instead of proxying to the backend; `.json()` threw on
the HTML response. Fix: added both proxy entries. No backend changes, no ADR required.

**Verified:**

- Provider Governance workspace loads content without JSON parse error.
- `frontend/vite.config.ts` proxy table extended with `/provider-governance` and `/admin`.
- Raw KB capture: `knowledge-base/TradeForge/raw/TF-F069-provider-governance-json-parse.md`
- Processed note: `knowledge-base/TradeForge/knowledge/processed/TF-F069-provider-governance-json-parse.md`

---

## TF-F070: Advisory Route Diagnostics And Explicit Advisory Invocation

**Status:** Done

**Classification:** enhancement / operational

**Milestone:** M13A

**Branch:** `feature/tf-f070-advisory-route-diagnostics`

**Affected Layer:** frontend, app, infrastructure/advisory

**Linked ADRs:** ADR-0001, ADR-0003, ADR-0032, ADR-0037, ADR-0038, ADR-0041, ADR-0042

**Impacted Invariants:** AI Advisory Boundary, Human Decision Sovereignty, Derived State Must Remain Distinguishable, Replayability Is Foundational, UX Is Architectural, Architectural Simplicity

**Depends On:** TF-F051, TF-F052, TF-F064, TF-F066, TF-F067, TF-F069

**Source:** `knowledge/raw/brainstorm-20260524-litellm-advisory-routing-test-gap.md` and `knowledge/raw/TF-F069 Provider governance page not working.md`.

**Problem:**
Operators cannot clearly determine whether advisory routes are functioning, whether LiteLLM is reachable, whether advisory generation was actually invoked, or whether failures come from frontend proxying, TradeForge API handling, LiteLLM routing, or the underlying model provider. During local Vite development, `/advisory/*` routes are not proxied to the backend, causing HTML responses to be parsed as JSON and surfacing misleading `JSON.parse: unexpected character at line 1 column 1` errors in advisory panels.

The current Plan Review Workspace can imply advisory interpretation may happen automatically after thesis creation, while the architecture intends explicit operator-invoked advisory actions. Operational diagnostics must make advisory invocation visible without adding background generation, lifecycle authority, or canonical event writes.

**Diagnosis:**
Direct testing confirmed local Ollama works, LiteLLM exposes configured model aliases, and the `tradeforge-ollama` route can complete a chat request through LiteLLM. TradeForge logs for the ANET workflow showed lifecycle and workspace requests, but no `/advisory/thesis-review`, `/advisory/generate-observations`, `/advisory/replay-summary`, or equivalent AI generation call. LiteLLM logs showed no matching `/v1/chat/completions` call from that workflow. The observed JSON parse failure is therefore likely a frontend local-dev routing problem for `/advisory/*`, not proof that LiteLLM or Ollama failed.

**Scope:**

- Add `/advisory` to the Vite local-development proxy table.
- Improve advisory API failure handling so non-JSON or proxy failures render operator-facing diagnostics instead of raw JSON parse errors.
- Add an explicit "Generate Advisory Review" action in the Plan Review Workspace that invokes the existing thesis-review advisory path on operator command.
- Surface advisory invocation state in the Plan Review Workspace, including not invoked, running, succeeded, and failed states.
- Add a minimal non-canonical advisory route smoke test in the provider governance / AI gateway surface that verifies the configured advisory route can receive a tiny diagnostic prompt.
- Keep smoke-test results as operational metadata only; do not create canonical event-ledger facts.

**Out Of Scope:**

- Autonomous advisory generation.
- Persistent AI memory.
- A generalized orchestration engine.
- Multi-agent workflows.
- Automatic lifecycle intervention.
- Hidden background advisory calls.
- New lifecycle stages or lifecycle transition behavior.
- Editing external LiteLLM configuration from TradeForge.

**Acceptance Criteria:**

- `/advisory/*` routes proxy correctly during Vite local development.
- Advisory API failures display operational diagnostics instead of raw JSON parse errors.
- Plan Review Workspace includes an explicit operator-invoked advisory review action.
- Advisory invocation does not automatically occur during lifecycle transitions.
- Provider governance UI can perform a non-canonical advisory route smoke test.
- Smoke tests do not create canonical ledger events.
- Advisory diagnostics remain operational metadata only.
- Advisory output remains visibly non-canonical and cannot approve, execute, or transition lifecycle state.
- Focused backend tests cover provider governance smoke-test behavior, and frontend typecheck/build cover the explicit advisory invocation and diagnostic API contracts.

**ADR Checkpoint:**
No ADR is expected for the first implementation if it remains within existing AI advisory, provider governance, and operational diagnostic boundaries. ADR evaluation must be revisited if implementation introduces durable diagnostic history, new event types, automatic advisory invocation, lifecycle changes, or a new orchestration boundary.

**Resolution Summary:**
Added local-development proxy coverage for `/advisory`, `/provider-governance`,
and `/admin` so frontend requests reach the FastAPI runtime instead of parsing
the Vite HTML shell. Added operational JSON parsing for advisory fetches so
non-JSON and malformed responses produce explicit operator diagnostics.

Plan Review now exposes an explicit operator-triggered "Generate Advisory
Review" action that calls the existing `/advisory/thesis-review` route and
surfaces invocation state as not invoked, running, succeeded, or failed. The
action remains non-canonical and does not create lifecycle transitions.

Provider Governance now includes a non-canonical AI gateway smoke test backed
by `POST /provider-governance/ai-gateway/smoke-test`. The endpoint performs a
minimal advisory provider call when configured, reports unavailable or
not-configured states as operational metadata, and does not write canonical
event-ledger facts.

Provider credential reload now refreshes the in-process LiteLLM advisory
provider so a saved LiteLLM credential can become active without restarting the
backend.

**Completed Verification:**

- `uv run pytest tests/test_provider_governance_api.py tests/test_default_advisory_provider_bootstrap.py`
- `uv run mypy src\app\api\routes.py tests\test_provider_governance_api.py`
- `npm.cmd run typecheck`
- `npm.cmd run build`
- `git diff --check`

**Verification Note:**
`uv run ruff check src\app\api\routes.py tests\test_provider_governance_api.py`
still reports existing line-length and FastAPI `Query(...)` default findings in
`src/app/api/routes.py`. The new TF-F070 long-line finding was fixed; the
remaining ruff findings are outside this issue's change scope.

---

## TF-F071: Fix Advisory Thesis Review Event Store Loading

**Status:** Done

**Classification:** bug

**Milestone:** M13A

**Branch:** `fix/tf-f071-advisory-thesis-review-event-read`

**Affected Layer:** app

**Linked ADRs:** ADR-0001, ADR-0006, ADR-0018, ADR-0020, ADR-0041, ADR-0042

**Impacted Invariants:** Event Ledger Canonical Truth, Replayability Is Foundational, AI Advisory Boundary, Derived State Must Remain Distinguishable, Human Decision Sovereignty

**Depends On:** TF-F070

**Source:** `knowledge/raw/Generate-advisory-resulting-in error.md`

**Problem:**
After TF-F070 made advisory invocation explicit and fixed local routing, the
`POST /advisory/thesis-review` endpoint is reached successfully but crashes
before invoking LiteLLM. Runtime logs show:

```text
AttributeError: 'PostgresEventStore' object has no attribute 'load'
```

The route assumes an obsolete event-store method while the canonical
`EventStore` port exposes `read_events()` for deterministic replay reads.

**Scope:**

- Align advisory thesis review context reconstruction with the canonical
  event-store read interface.
- Filter event history to the requested decision before selecting the latest
  thesis artifact.
- Preserve advisory-only behavior with no canonical event writes.
- Add regression coverage for an event store that implements `read_events()`
  but not `load()`.

**Acceptance Criteria:**

- `POST /advisory/thesis-review` no longer crashes when the runtime uses
  `PostgresEventStore`.
- The route reconstructs thesis context through the canonical event-store port.
- The route returns advisory output when a thesis artifact exists for the
  requested decision.
- Missing thesis artifacts still return a controlled `404`.
- Advisory generation does not append lifecycle events or canonical ledger
  facts.
- Focused backend tests pass.

**Out Of Scope:**

- New advisory orchestration behavior.
- New event types or event schema changes.
- Automatic advisory generation.
- Provider, LiteLLM, or credential changes.

**ADR Checkpoint:**
No ADR is required. The fix uses the existing event-store port and reinforces
existing advisory and replay boundaries without changing lifecycle state,
event schema, domain model structure, or bounded contexts.

**Resolution Summary:**
Replaced the advisory thesis-review route's obsolete `event_store.load(...)`
call with the canonical `read_events()` event-store port. The route now filters
event history to the requested decision, reconstructs the latest structured
thesis artifact from event payloads, and invokes the advisory provider without
writing canonical events or mutating lifecycle state.

Added regression coverage for an event store that implements `append()` and
`read_events()` only, matching the domain port and `PostgresEventStore`
behavior. The test verifies successful advisory generation, controlled `404`
for missing thesis artifacts, and zero event appends.

**Completed Verification:**

- `uv run pytest tests/test_advisory_thesis_review_api.py tests/test_provider_governance_api.py tests/test_default_advisory_provider_bootstrap.py`
- `uv run mypy src\app\api\routes.py tests\test_advisory_thesis_review_api.py`
- `uv run ruff check tests\test_advisory_thesis_review_api.py`
- `npm.cmd run typecheck`
- `npm.cmd run build`
- `git diff --check`

---

## TF-F072: Global Advisory Model Selection

**Status:** Done

**Classification:** feature / governance

**Milestone:** M13B

**Branch:** `feature/tf-f072-global-advisory-model-selection`

**Affected Layer:** app, services/advisory, infrastructure/advisory, frontend

**Linked ADRs:** ADR-0006, ADR-0037, ADR-0041, ADR-0042, ADR-0043

**Impacted Invariants:** AI Advisory Boundary, Human Decision Sovereignty, Derived State Must Remain Distinguishable, Replayability Is Foundational, UX Is Architectural, Architectural Simplicity

**Depends On:** TF-F062, TF-F066, TF-F067, TF-F070, TF-F071

**Source:** `knowledge/raw/archived/brainstorm-20260525-m13b-ai-gateway-governance.md`; processed synthesis `knowledge/processed/20260525-m13b-ai-gateway-governance-synthesis.md`.

**Problem:**
Advisory generation can be invoked through LiteLLM, but operator control over
the selected advisory model or route remains indirect. Workflow logic and
runtime configuration can still depend on raw model names or static gateway
defaults, making it hard to choose a primary advisory model, define a fallback,
or smoke-test the selected route through the TradeForge governance surface.

**Scope:**

- Discover available LiteLLM models/routes through TradeForge.
- Let the operator choose one primary advisory model or route.
- Let the operator choose one optional fallback model or route.
- Store the selected advisory configuration through the governed runtime
  configuration or credential boundary defined by M13B.
- Apply the selected configuration advisory-wide.
- Remove hardcoded advisory model names from workflow logic.
- Smoke-test the selected route through TradeForge.
- Surface selected-route state in Provider Governance without treating it as
  canonical decision truth.

**Acceptance Criteria:**

- Provider Governance lists available LiteLLM models/routes through TradeForge.
- The operator can select a primary advisory model/route and optional fallback.
- Advisory calls use the selected primary/fallback configuration consistently.
- Existing advisory tasks do not hardcode raw model names in workflow logic.
- The selected route can be smoke-tested through TradeForge.
- Smoke-test results remain operational metadata and do not append canonical
  event-ledger facts.
- Route provenance needed for advisory artifact interpretation is captured when
  advisory output is persisted or shown.
- AI output remains advisory and cannot approve, execute, or transition
  lifecycle state.

**Out Of Scope:**

- Per-task dynamic routing policies.
- Automatic hidden model choice.
- Cost optimization engines.
- Multi-agent orchestration.
- Direct Anthropic, OpenAI, Google, Groq, or NVIDIA SDK bypass.
- Editing LiteLLM YAML directly unless separately scoped.

**Resolution Summary:**
Added global advisory model selection through Provider Governance. The existing
encrypted `litellm` credential now supports optional `fallback_model` while
preserving `default_model` as the selected primary route. The OpenAI-compatible
advisory provider can discover LiteLLM models, uses the selected primary route
for all advisory calls, and falls back only when the primary route is
unavailable.

Added `GET /provider-governance/ai-gateway/model-selection` and
`PUT /provider-governance/ai-gateway/model-selection`. Updates are operational
configuration changes stored in `.keys.enc`; they reload the in-process
advisory provider and do not append canonical event-ledger facts. The Provider
Governance frontend surface now lets operators choose primary and fallback
routes from discovered LiteLLM models.

**Completed Verification:**

- `uv run pytest tests/test_credential_store.py tests/test_admin_credentials.py tests/test_openai_compatible_provider.py tests/test_provider_governance_api.py tests/test_default_advisory_provider_bootstrap.py`
- `uv run mypy src\security\litellm_credential.py src\infrastructure\advisory\openai_compatible_provider.py src\app\api\routes.py src\app\api\admin_routes.py tests\test_credential_store.py tests\test_openai_compatible_provider.py tests\test_provider_governance_api.py`
- `uv run ruff check src\security\litellm_credential.py src\infrastructure\advisory\openai_compatible_provider.py tests\test_credential_store.py tests\test_openai_compatible_provider.py tests\test_provider_governance_api.py scripts\manage_credentials.py`
- `npm.cmd run typecheck`
- `npm.cmd run build`

---

## TF-F073: Internalize LiteLLM Gateway Network Boundary

**Status:** Done

**Classification:** enhancement / infrastructure governance

**Milestone:** M13B

**Branch:** `feature/tf-f073-internalize-litellm-gateway-boundary`

**Affected Layer:** infrastructure, app, docs, tests

**Linked ADRs:** ADR-0006, ADR-0011, ADR-0037, ADR-0041, ADR-0042, ADR-0043

**Impacted Invariants:** AI Advisory Boundary, Human Decision Sovereignty, Derived State Must Remain Distinguishable, Replayability Is Foundational, Architectural Simplicity

**Depends On:** TF-F057, TF-F066, TF-F067, TF-F070, TF-F072

**Source:** `knowledge/raw/archived/brainstorm-20260525-m13b-ai-gateway-governance.md`; processed synthesis `knowledge/processed/20260525-m13b-ai-gateway-governance-synthesis.md`.

**Problem:**
The optional LiteLLM Compose service was introduced as a reachable local service
on host port `4000`. That was useful for initial validation, but it weakens the
intended advisory boundary because browser or host workflows can call LiteLLM
outside TradeForge. The managed advisory runtime requires TradeForge to be the
sole operator-facing gateway while LiteLLM runs as internal infrastructure.

**Scope:**

- Remove public host exposure for LiteLLM by default.
- Make LiteLLM reachable through Docker-internal networking by TradeForge.
- Require browser and operator workflows to access advisory behavior through
  TradeForge.
- Update advisory configuration defaults for containerized runtime access.
- Keep Provider Governance and AI gateway smoke tests working through
  TradeForge.
- Document the local debugging workflow when direct LiteLLM inspection is
  needed.
- Preserve LiteLLM as managed advisory gateway infrastructure, not a canonical
  decision system.

**Acceptance Criteria:**

- LiteLLM is not exposed on `localhost:4000` by default.
- Browser access cannot bypass TradeForge to invoke LiteLLM in the default
  Compose runtime.
- TradeForge advisory workflows continue functioning through internal network
  access.
- Provider Governance route visibility and smoke tests continue working through
  TradeForge.
- Local debugging instructions explain any explicit opt-in direct LiteLLM access
  path.
- Docker and runtime documentation describe LiteLLM as managed internal
  advisory infrastructure.
- No lifecycle, event ledger, or advisory authority semantics change.

**Out Of Scope:**

- Dynamic model registry implementation beyond TF-F072 requirements.
- Automated route orchestration.
- Per-task routing policies.
- Direct vendor SDK bypass.
- Distributed inference infrastructure.
- Kubernetes networking, vault integration, or production platform hardening.

**Resolution Summary:**
Internalized the default LiteLLM Compose boundary by removing the host
`4000:4000` publication from `docker-compose.yml` and using Docker-internal
`expose: "4000"` instead. TradeForge-mediated advisory access continues through
the configured gateway URL, with managed runtime docs pointing at
`http://litellm:4000`.

Added `docker-compose.litellm-debug.yml` as an explicit local debugging
override that publishes `4000:4000` only when intentionally included. Updated
README and credential setup documentation to describe TradeForge as the normal
operator-facing advisory boundary and the override as temporary inspection
workflow.

**Completed Verification:**

- `uv run pytest tests/test_postgres_compose.py tests/test_provider_governance_api.py tests/test_default_advisory_provider_bootstrap.py`
- `docker compose config`
- `docker compose --profile advisory config`
- `docker compose --profile advisory -f docker-compose.yml -f docker-compose.litellm-debug.yml config`

---

## TF-F074: Governed LLM Provider Secret Management

**Status:** Done

**Classification:** feature / security governance

**Milestone:** M13B

**Branch:** `feature/tf-f074-governed-llm-provider-secrets`

**Affected Layer:** security, app, infrastructure/advisory, frontend, docs, tests

**Linked ADRs:** ADR-0006, ADR-0037, ADR-0041, ADR-0042, ADR-0043

**Impacted Invariants:** AI Advisory Boundary, Human Decision Sovereignty, Derived State Must Remain Distinguishable, Replayability Is Foundational, Architectural Simplicity

**Depends On:** TF-F045, TF-F055, TF-F065, TF-F066, TF-F067, TF-F072, TF-F073

**Source:** `knowledge/raw/archived/brainstorm-20260525-m13b-ai-gateway-governance.md`; processed synthesis `knowledge/processed/20260525-m13b-ai-gateway-governance-synthesis.md`.

**Problem:**
M13A treated TradeForge as the owner of the LiteLLM gateway credential while
downstream LLM vendor keys remained in LiteLLM configuration or operator
environment. For the managed advisory runtime, that split leaves provider
secret lifecycle, masking, rotation, reload, and provenance outside the
TradeForge governance surface.

**Scope:**

- Extend governed credential handling to downstream LLM provider keys such as
  Groq, NVIDIA NIM, OpenAI, Anthropic, Google, and similar providers.
- Store provider secrets encrypted at rest in `.keys.enc`.
- Mask secrets in API and UI responses.
- Keep `TRADEFORGE_MASTER_KEY` as OS environment configuration only.
- Decrypt provider secrets only at the runtime composition boundary.
- Define managed injection of provider secrets into the LiteLLM runtime.
- Define rotation and reload semantics for changed provider secrets.
- Ensure plaintext secrets are never logged, returned, committed, or stored in
  static LiteLLM config.

**Acceptance Criteria:**

- TradeForge can persist supported downstream LLM provider keys in `.keys.enc`.
- Provider Governance shows configured/missing/invalid/revoked/untested states
  without returning plaintext secrets.
- API responses mask secret fields consistently.
- Runtime composition can decrypt provider secrets and inject them into managed
  LiteLLM without exposing them to workflow logic.
- Credential rotation semantics are documented and tested.
- Reload semantics are explicit for both TradeForge advisory provider state and
  LiteLLM runtime injection.
- Existing market-data credential behavior remains intact.
- Advisory workflows remain non-canonical and cannot write lifecycle events or
  execute trades.

**Out Of Scope:**

- Storing `TRADEFORGE_MASTER_KEY` in UI, `.env`, Git, or `.keys.enc`.
- External vault, cloud secrets manager, or Kubernetes secrets integration.
- Direct vendor SDK adapters for advisory workflow code.
- Generalized orchestration or multi-agent runtime management.
- Broker credential changes.
- Changing event taxonomy or lifecycle authority.

**Resolution Summary:**
Added governed downstream LLM provider credential schemas for `llm_groq`,
`llm_nvidia_nim`, `llm_openai`, `llm_anthropic`, and `llm_google`. These keys
use the existing encrypted `.keys.enc` credential boundary, are masked in API
and UI responses, and can be managed through the admin credential API,
Provider Governance frontend, and credential CLI.

Added a composition-boundary LiteLLM provider environment projection that
decrypts active downstream LLM provider secrets only during app composition or
provider reload. Provider Governance now exposes
`GET /provider-governance/ai-gateway/provider-secret-injection`, which reports
configured/injected status and target LiteLLM environment variable names without
returning secret values. LiteLLM config now references Groq, NVIDIA NIM,
OpenAI, Anthropic, and Google environment variables without embedding secrets.

**Completed Verification:**

- `uv run pytest tests/test_llm_provider_secrets.py tests/test_admin_credentials.py tests/test_provider_governance_api.py tests/test_postgres_compose.py tests/test_manage_credentials_script.py tests/test_credential_store.py`
- `uv run mypy src\security src\app\api\application.py src\app\api\admin_routes.py src\app\api\routes.py tests\test_llm_provider_secrets.py tests\test_admin_credentials.py tests\test_provider_governance_api.py`
- `uv run ruff check src\security src\app\api\application.py src\app\api\admin_routes.py tests\test_llm_provider_secrets.py tests\test_admin_credentials.py tests\test_provider_governance_api.py tests\test_manage_credentials_script.py tests\test_postgres_compose.py scripts\manage_credentials.py`
- `npm.cmd run typecheck`
- `npm.cmd run build`
- `docker compose --profile advisory config`

---

## TF-F075: Implement Stateless LiteLLM Request-Time Credential Composition

**Status:** Done

**Classification:** corrective / security governance / infrastructure

**Milestone:** M13B (corrective against TF-F074)

**Branch:** `feature/tf-f075-litellm-secret-injection`

**Affected Layer:** infrastructure/advisory, app, docs, tests

**Linked ADRs:** ADR-0043

**Impacted Invariants:** AI Advisory Boundary, Derived State Must Remain Distinguishable, Architectural Simplicity

**Depends On:** TF-F074, ADR-0043

**Source:** `knowledge/raw/brainstorm-20260525-tf-f074-litellm-secret-injection-gap.md`; `knowledge/processed/20260526-tf-f075-stateless-litellm-request-time-injection-synthesis.md`; final TF-F075 stateless LiteLLM plan (2026-05-26)

**Problem:**
TF-F075 initially attempted to solve governed downstream LLM provider secrets by
pushing decrypted keys into LiteLLM with `/config/update`. Validation showed
that path required LiteLLM DB-backed mutable config and coupled TradeForge to a
separate `litellm_proxy` schema. The design also left model strings too
authoritative after explicit provider IDs existed.

The corrected M13B boundary is stateless LiteLLM: TradeForge owns provider
credentials and advisory model selection, resolves the explicit provider ID at
request time, and composes each LiteLLM `/chat/completions` request with only
the secret material required for that request.

**Scope:**

- Split LiteLLM gateway credentials from advisory model selection.
- Persist model selection as explicit provider/model pairs.
- Add request-time `LLMProviderCredentialResolver` and
  `LiteLLMRequestComposer`.
- Remove `LiteLLMGatewayAdminClient`, `/config/update`, LiteLLM DB vars,
  provider API key env vars, and `litellm_proxy` init SQL.
- Keep LiteLLM internal-only and pin it to an explicit image tag.
- Update governance API/UI labels from injected state to runtime availability.

**Acceptance Criteria:**

- LiteLLM has no TradeForge-managed DB, no `STORE_MODEL_IN_DB`, and no
  `/config/update` dependency.
- LiteLLM service receives no downstream provider API keys in environment.
- LiteLLM remains internal-only by default with `expose: "4000"`.
- Advisory model selection stores explicit `primary_provider_id`,
  `primary_model`, optional `fallback_provider_id`, and optional
  `fallback_model`.
- Legacy `litellm.default_model` / `fallback_model` values are read only as
  compatibility fallback; saving writes explicit provider IDs.
- Saved model strings alone cannot determine credential authority.
- Missing, revoked, invalid, or absent required provider credentials make the
  advisory provider unavailable without logging or returning plaintext secrets.

**Out Of Scope:**

- Changes to `.keys.enc` format or `TRADEFORGE_MASTER_KEY` model.
- Kubernetes secrets or external vault integration.
- Frontend label changes beyond corrected flag semantics.

**Rejected History:**

Option A added `LiteLLMGatewayAdminClient`,
`scripts/postgres-init/02-litellm-db.sql`, LiteLLM `DATABASE_URL`,
`STORE_MODEL_IN_DB=True`, and provider API key environment variables so
TradeForge could call LiteLLM `POST /config/update`. That implementation is
preserved here as rejected history. It was rejected because it required LiteLLM
DB-backed mutable config, introduced migration/version coupling, and put a
gateway-owned config database in the credential authority path.

**Resolution Summary:**

Added `AdvisoryModelSelectionConfig` stored separately from the `litellm`
gateway credential. The `litellm` credential now represents gateway
`base_url` and master `api_key`; legacy `default_model` and `fallback_model`
fields remain readable only for compatibility. Saving through
`PUT /provider-governance/ai-gateway/model-selection` writes explicit provider
IDs.

Added `LLMProviderCredentialResolver` and `LiteLLMRequestComposer`. Groq,
NVIDIA NIM, OpenAI, Anthropic, and Google resolve through encrypted provider
credentials. Ollama resolves as a keyless internal provider with configured API
base. `OpenAICompatibleAdvisoryProvider` composes primary and fallback
LiteLLM requests independently and reports advisory unavailable when required
credentials are missing, revoked, or invalid.

Removed startup/reload gateway secret push state, the LiteLLM admin client,
LiteLLM DB vars, provider key env vars, and `02-litellm-db.sql`. The Compose
LiteLLM image is pinned to `docker.litellm.ai/berriai/litellm:v1.72.6-stable`
and remains internal-only with `expose: "4000"`.

**Completed Verification:**

- `uv run pytest tests/test_default_advisory_provider_bootstrap.py tests/test_openai_compatible_provider.py tests/test_provider_governance_api.py tests/test_credential_store.py tests/test_postgres_compose.py`
- `uv run mypy src/infrastructure/advisory/litellm_request_composer.py src/infrastructure/advisory/openai_compatible_provider.py src/security/advisory_model_selection.py src/app/api/application.py src/app/api/routes.py`
- `uv run ruff check src/infrastructure/advisory/litellm_request_composer.py src/infrastructure/advisory/openai_compatible_provider.py src/security/advisory_model_selection.py src/app/api/application.py src/app/api/routes.py tests/test_provider_governance_api.py tests/test_postgres_compose.py`
- `npm.cmd run typecheck`
- `npm.cmd run build`
- `docker compose --profile advisory config`
- Targeted backend slice passes.
- docker-compose advisory config preserves internal-only LiteLLM exposure.
- LiteLLM healthcheck probes authenticate correctly.
- Request-time composition replaces LiteLLM config mutation.

---

## TF-F076: Replace LiteLLM route-probing healthcheck with non-invasive readiness check

**Status:** Done

**Classification:** corrective / operational infrastructure

**Milestone:** M13B

**Branch:** `fix/tf-f076-litellm-readiness-healthcheck`

**Affected Layer:** infrastructure, docs, tests

**Linked ADRs:** ADR-0043

**Impacted Invariants:** AI Advisory Boundary, Derived State Must Remain Distinguishable, Replayability Is Foundational, Architectural Simplicity

**Depends On:** TF-F073, TF-F075, ADR-0043

**Source:** `knowledge/raw/brainstorm-20260526-litellm-independent-provider-attempts.md`; `knowledge/raw/logs from litellm container.txt`; LiteLLM health documentation for `/health` and `/health/readiness`.

**Problem:**
Field logs showed LiteLLM attempting Groq, Gemini, OpenAI, and Anthropic routes
while the managed advisory runtime was otherwise validating the selected NVIDIA
NIM path. LiteLLM documentation distinguishes `/health` as comprehensive model
health monitoring that makes real LLM API calls, while `/health/readiness`
checks whether the proxy is ready to accept requests. The Compose healthcheck
used `/health`, so Docker liveness/readiness could trigger provider route
probes even when TradeForge had not made an advisory request.

**Scope:**

- Replace the LiteLLM Docker healthcheck endpoint with `/health/readiness`.
- Preserve LiteLLM as internal-only Compose infrastructure.
- Preserve `LITELLM_MASTER_KEY` authentication in the healthcheck.
- Keep stateless LiteLLM configuration and request-time credential
  composition intact.
- Add static tests that prevent Compose from regressing to model-probing
  `/health`.
- Record lightweight diagnostic and planning artifacts for the feedback loop.

**Acceptance Criteria:**

- LiteLLM Compose healthcheck calls `/health/readiness`.
- LiteLLM Compose healthcheck does not call model-probing `/health`.
- LiteLLM remains internal-only by default with `expose: "4000"`.
- LiteLLM service receives no downstream provider API keys such as
  `GROQ_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or
  `GOOGLE_API_KEY`.
- `LITELLM_MASTER_KEY` remains configured for the LiteLLM service.
- `litellm_config.yaml` wildcard routes are unchanged in this issue.
- No public API, domain model, event schema, credential schema, or frontend
  interface changes are made.

**Out Of Scope:**

- Changing LiteLLM wildcard route definitions.
- Adding downstream provider keys to LiteLLM environment.
- Reintroducing LiteLLM DB-backed mutable configuration.
- Provider model selection or fallback policy changes.
- Public API, frontend, domain, lifecycle, event schema, or credential schema
  changes.

**ADR Checkpoint:**
No new ADR is required. The change reinforces ADR-0043 by keeping LiteLLM as
managed internal advisory infrastructure while preventing Docker readiness from
performing provider/model validation outside explicit TradeForge-mediated
diagnostics or advisory requests.

**Resolution Summary:**
Replaced the LiteLLM Docker healthcheck URL from `/health` to
`/health/readiness`. The healthcheck remains authenticated with
`LITELLM_MASTER_KEY`, LiteLLM remains internal-only, and no downstream provider
API keys were added to Compose.

Added regression coverage in `tests/test_postgres_compose.py` to assert the
readiness endpoint is used, the model-probing health endpoint is not used, and
provider API keys remain absent from the LiteLLM service environment.

**Completed Verification:**

- `uv run pytest tests/test_postgres_compose.py`
- `docker compose --profile advisory config`
- `docker compose --profile advisory up -d`
- LiteLLM idle log window showed repeated `GET /health/readiness` checks and
  no provider fallback errors.
- `POST /provider-governance/ai-gateway/smoke-test` returned `status:
  available` through the TradeForge API using
  `nvidia_nim/meta/llama-3.1-70b-instruct`.
- Post-smoke LiteLLM logs showed the explicit `/chat/completions` request and
  no Groq, Gemini, OpenAI, or Anthropic fallback attempts.

---

## TF-F077: Verify ATKR Thesis Local Import Feedback

**Status:** Done

**Classification:** operational feedback / verification

**Milestone:** M14C

**Branch:** `fix/tf-f077-atkr-thesis-import-feedback`

**Affected Layer:** app, tests

**Linked ADRs:** ADR-0001, ADR-0002, ADR-0034, ADR-0041

**Impacted Invariants:** Human Decision Sovereignty, Event Ledger Canonical Truth, Lifecycle Authority, AI Advisory Boundary, Derived State Must Remain Distinguishable, Replayability Is Foundational

**Source:** Operator feedback on 2026-05-28 using
`imports/incoming/ATKR_thesis_draft.md`.

**Problem:**
Operator feedback initially showed the Plan Import Preview scanning
`imports/incoming` and importing zero files with the message
`No eligible plan draft artifacts for ATKR`. The operator then clarified the
intended artifact was `ATKR_thesis_draft.md`.

The observed UI was the plan import path, whose correct behavior is to ignore
`thesis_draft.v1` artifacts. The thesis import scanner already accepts the
reported `ATKR_thesis_draft.md` shape and imports it as a non-canonical
advisory artifact.

**Scope:**

- Verify the live thesis scan endpoint against the reported ATKR file.
- Confirm the imported artifact appears in the thesis import preview endpoint.
- Preserve the distinction between thesis and plan import routes.
- Avoid runtime code changes when the implemented behavior is already correct.

**Acceptance Criteria:**

- `POST /advisory/thesis-imports/scan-local` imports the reported
  `ATKR_thesis_draft.md` file.
- `GET /advisory/thesis-imports` returns the ATKR thesis import preview.
- The imported advisory artifact remains non-canonical and does not append
  Event Ledger records.
- Plan import preview continues to reject thesis artifacts.
- No new thesis fields are inferred beyond the existing deterministic markdown
  section mapping.

**Out Of Scope:**

- AI parsing from arbitrary prose.
- Plan import YAML-body mapping.
- Frontend workflow changes.
- New event types, lifecycle transitions, or advisory artifact schemas.
- Automatic thesis creation or lifecycle advancement.

**ADR Checkpoint:**
No new ADR is required. This is an operational verification issue inside the
existing TF-R001 advisory import boundary and does not change event, lifecycle,
domain, or workspace semantics.

**Resolution Summary:**
No runtime code change was required. The live backend successfully imported the
reported ATKR thesis file through the thesis scan route. The pasted failure came
from the Plan Import Preview, which correctly ignores `thesis_draft.v1`
artifacts.

**Verification Completed:**

- `uv run pytest tests\test_advisory_artifact.py -k local_thesis_import_scan -q`
- `POST /advisory/thesis-imports/scan-local?persona_id=persona.swing&workspace_id=workspace.context&symbol=ATKR`
  returned `scanned_count: 2` and `imported_count: 1`.
- `GET /advisory/thesis-imports?persona_id=persona.swing&workspace_id=workspace.context&symbol=ATKR`
  returned `total_count: 1`.

---

## TF-R001: Thesis Workspace Advisory Import Preview

**Status:** Done

**Classification:** feature / lifecycle UX / advisory traceability

**Milestone:** M14C

**Branch:** `feature/m14c-thesis-import-workflow`

**Affected Layer:** app, services/advisory read model, frontend, tests

**Linked ADRs:** ADR-0001, ADR-0002, ADR-0034, ADR-0035, ADR-0041

**Impacted Invariants:** Human Decision Sovereignty, Event Ledger Canonical Truth, Lifecycle Authority, AI Advisory Boundary, Derived State Must Remain Distinguishable, Replayability Is Foundational

**Source:**
Runtime implementation plan for M14C TF-R001; KB synthesis
`knowledge/processed/20260527-tf-r001-local-thesis-import-dropoff-synthesis.md`;
raw implementation capture
`knowledge/raw/archived/Implemented the missing operator dropoff side.md`;
manual feedback
`knowledge/raw/feed back Local.md thesis import scan failed`; diagnosis
`knowledge/raw/20260527-tf-r001-scan-not-found-diagnosis.md`.

**Problem:**
Operators need a controlled way to bring durable advisory research artifacts into
the Thesis authoring workflow without allowing advisory cognition to create,
approve, or mutate lifecycle state.

**Scope:**

- Expose a read-only thesis import preview over existing advisory artifacts.
- Add an on-demand local drop-folder scan for `imports/incoming/*.md` so
  operators can create advisory thesis-draft artifacts without calling the API
  manually.
- Restrict TF-R001 import mapping to deterministic `thesis_draft.v1`
  `metadata.mapped_fields`.
- Allow operators to selectively accept advisory fields into the existing Thesis
  draft UI.
- Preserve accepted, edited, and rejected import field provenance on the normal
  `decision.thesis_created` event.
- Show import provenance in replay as advisory source context only.

**Acceptance Criteria:**

- Markdown files dropped in `imports/incoming` with thesis-draft front matter
  can be scanned on demand into non-canonical advisory artifacts.
- `GET /advisory/thesis-imports` returns only matching persona, workspace,
  symbol, and `artifact_role == "thesis_draft"` artifacts.
- The endpoint returns advisory authority flags and never appends events.
- Unsupported or unmapped artifacts are ignored rather than inferred from prose.
- `POST /lifecycle/decisions/develop-thesis` accepts optional import provenance
  while preserving human workflow provenance and lifecycle authority.
- Missing source advisory artifact IDs are rejected with a clear 422.
- The Thesis Development modal shows advisory, non-canonical import previews and
  keeps manual Develop Thesis submission as the only lifecycle action.
- Replay renders import provenance as `Advisory source, operator-promoted thesis`.

**Out Of Scope:**

- Watchers, background orchestration, AI parsing, automatic thesis creation,
  conviction assignment, sizing, approval, execution, and new canonical event
  types for field acceptance.

**Implementation Summary:**
Added a read-only thesis import preview API over existing advisory artifacts:
`GET /advisory/thesis-imports`. The endpoint returns only advisory,
non-canonical `thesis_draft.v1` artifacts matching persona, workspace, and
symbol, with deterministic field mapping from `metadata.mapped_fields`.

Added an on-demand local markdown dropoff path:
`POST /advisory/thesis-imports/scan-local`. The scan reads
`imports/incoming/*.md`, parses simple front matter plus thesis sections,
persists matching files as non-canonical advisory markdown artifacts, and does
not append Event Ledger records.

Extended `POST /lifecycle/decisions/develop-thesis` with optional import
provenance fields. The normal `decision.thesis_created` event remains the only
canonical lifecycle fact, with advisory import provenance stored as source
context under `m14c_import_provenance`.

Updated `ThesisDevelopmentModal` with an Import Preview panel, a local
`Scan folder` action, per-field accept/reject controls, append/replace conflict
handling, imported/edited badges, and provenance submission. Replay now labels
imported context as `Advisory source, operator-promoted thesis`.

**Verification Completed:**

- `uv run pytest tests\test_advisory_artifact.py tests\test_develop_thesis_workflow.py`
- `uv run mypy src\app\api\routes.py tests\test_advisory_artifact.py`
- `uv run ruff check src\app\api\routes.py tests\test_advisory_artifact.py --select F`
- `npm.cmd run typecheck`
- `npm.cmd run build`
- `git diff --check`

**Closure (2026-07-11):**

- Backend alignment: the 2026-05-27 `{"detail":"Not Found"}` failure was a
  stale running server; the aligned backend verification recorded above
  (`scan-local` returning `scanned_count: 2, imported_count: 1`, preview
  returning `total_count: 1` for ATKR) confirms the route set is exposed.
- Automated regression re-verified at closure:
  `uv run pytest tests/test_advisory_artifact.py tests/test_develop_thesis_workflow.py`
  — 19 passed.
- Operator documentation added to `README.md` under
  `Advisory imports (local drop-folder)` (covers TF-R001 thesis imports and
  TF-R002 plan imports).
- Closed by operator direction ahead of commissioning M-RF.

---

## TF-R002: Plan Workspace Advisory Import Mediation

**Status:** Done

**Classification:** feature / lifecycle UX / advisory traceability / execution-boundary protection

**Milestone:** M14C

**Branch:** `feature/m14c-plan-import-mediation`

**Affected Layer:** app, services/advisory read model, frontend, tests

**Linked ADRs:** ADR-0001, ADR-0002, ADR-0004, ADR-0006, ADR-0033, ADR-0034, ADR-0035, ADR-0041

**Impacted Invariants:** Human Decision Sovereignty, Event Ledger Canonical Truth, Lifecycle Authority, AI Advisory Boundary, Derived State Must Remain Distinguishable, Replayability Is Foundational, Workspaces Are Operational Environments

**Depends On:** TF-R001, M10AIS06, M10AIS07, ADR-0034, ADR-0041

**Source:**
`knowledge/raw/TF-R002 — Plan Workspace Import Mediation.md`;
TF-R001 implementation pattern; M14C operator cognition bridge planning.

**Problem:**
Operators need a controlled way to bring advisory plan-adjacent rationale into
the Plan authoring workflow without allowing imported material to populate
order prices, calculate sizing, approve plans, authorize execution, or create
broker-facing intent.

Plan imports are more sensitive than thesis imports because they sit adjacent
to risk acceptance and later execution. The runtime needs an explicit mediation
surface that lets advisory material assist plan authorship while preserving
operator-owned structured plan creation through the existing
`decision.plan_created` lifecycle event.

**Scope:**

- Extend the TF-R001 import-preview pattern to the Plan Review workspace and
  Plan Development modal.
- Support deterministic `plan_draft.v1` advisory artifact mapping for:
  `entry_rationale`, `stop_rationale`, `target_rationale`, and `risk_notes`.
- Expose a read-only plan import preview over existing advisory artifacts for
  the active persona, workspace, decision, and symbol.
- Optionally extend the on-demand local markdown scan to ingest matching
  plan-draft files as non-canonical advisory artifacts.
- Allow operators to selectively accept entry, stop, target, and risk-note
  advisory fields into the editable plan draft.
- Preserve accepted, rejected, and edited import provenance on the normal
  `decision.plan_created` event when the operator manually submits the plan.
- Keep `sizing_rationale` explicitly operator-authored or operator-confirmed;
  imported material may be visible as context but must not auto-fill sizing.
- Show replay provenance as advisory source context only after manual plan
  submission.

**Acceptance Criteria:**

- `GET /advisory/plan-imports` returns only matching persona, workspace,
  decision, symbol, and `artifact_role == "plan_draft"` artifacts.
- The plan import endpoint returns advisory authority flags and never appends
  Event Ledger records.
- Unsupported, unmapped, execution-authorizing, broker-order, or sizing
  artifacts are ignored or rejected rather than inferred from prose.
- Markdown files with `plan_draft.v1` front matter can be scanned on demand
  into non-canonical advisory artifacts if the TF-R001 local scan path is
  extended for this slice.
- The Plan Development modal shows advisory, non-canonical import previews and
  keeps manual Create Plan submission as the only lifecycle action.
- Operators can accept, reject, append, replace, or edit imported
  `entry_rationale`, `stop_rationale`, `target_rationale`, and `risk_notes`
  before plan submission.
- Imported `risk_notes` are treated as advisory planning context and may only
  enter the submitted plan through explicit operator action in an existing
  plan field, such as execution assumptions or revised rationale text.
- `sizing_rationale` remains manually entered or explicitly confirmed by the
  operator and is never automatically populated from import material.
- `POST /lifecycle/decisions/create-plan` accepts optional import provenance
  while preserving human workflow provenance and lifecycle authority.
- Missing source advisory artifact IDs are rejected with a clear 422.
- Replay renders plan import provenance as
  `Advisory source, operator-authored plan` or equivalent wording that does not
  imply advisory execution authority.

**Out Of Scope:**

- Automatic price population.
- Automatic sizing, risk calculation, or quantity suggestion.
- Broker integration, order tickets, or execution instructions.
- Automatic plan creation, plan approval, plan arming, or execution
  authorization.
- Background filesystem watchers or polling daemons.
- AI parsing from arbitrary prose.
- New canonical event types for field acceptance.
- Universal import framework or cross-workspace import center.

**Design Plan:**

1. Reuse the TF-R001 pattern: advisory artifacts are the durable non-canonical
   source; import preview endpoints are read-only; lifecycle events are created
   only by existing authoring endpoints.
2. Define a narrow `plan_draft.v1` mapping. Accepted source fields are limited
   to entry rationale, stop rationale, target rationale, and risk notes.
   Numeric prices, quantities, order types, approval language, execution
   instructions, and sizing directives are not mapped.
3. Add a plan-import read model that filters by persona, workspace, decision,
   symbol, artifact role, and schema version. The service should not infer plan
   fields from prose outside deterministic `metadata.mapped_fields`.
4. Extend Plan Development UI with an Import Preview panel only while the
   active decision is in Thesis stage and plan creation is available. The panel
   should mirror TF-R001 accept/reject/edit provenance controls but label all
   imported content advisory and non-canonical.
5. Extend plan submission provenance by adding optional
   `m14c_import_provenance` metadata to the normal
   `decision.plan_created` payload. The canonical fact remains the operator
   plan event, not the advisory source artifact.
6. Extend replay rendering to show advisory source context on plan events
   without treating imported material as execution authority.
7. Add targeted backend, frontend typecheck/build, and replay/provenance tests.

**Event Impact Analysis:**

- No new canonical event type is planned.
- Advisory artifact capture may continue to use existing M12 advisory capture
  semantics where applicable.
- `decision.plan_created` remains the canonical lifecycle event for plan
  creation.
- Import acceptance before submission remains draft UI/read-model state, not
  event truth.
- Submitted import provenance is event payload metadata that explains source
  influence; it does not make advisory content authoritative.

**Lifecycle Impact Analysis:**

- The allowed lifecycle flow remains Idea -> Thesis -> Plan -> Approval ->
  Execution -> Position -> Review.
- TF-R002 operates only inside the Thesis -> Plan authoring gate.
- Import preview and field acceptance cannot advance lifecycle state.
- Approval, arming, execution, and broker activity remain untouched.

**Replay Impact Analysis:**

- Replay should be able to show that a plan was operator-authored using
  advisory source context.
- Replay must not depend on live filesystem paths, current advisory provider
  output, mutable UI state, or broker APIs.
- Replay labels must distinguish advisory source material from the canonical
  `decision.plan_created` fact.

**Testing Strategy:**

- Backend tests for `plan_draft.v1` filtering, advisory flags, unsupported
  artifact rejection, missing source artifact validation, and create-plan
  provenance payloads.
- Lifecycle tests proving import preview does not append events and cannot
  advance Thesis -> Plan without manual plan submission.
- Frontend typecheck/build for Plan Development modal import controls.
- Replay rendering test or targeted frontend coverage for plan import
  provenance labels if the existing test structure supports it.

**ADR Checkpoint:**

No new ADR is required before implementation if TF-R002 remains a direct
extension of ADR-0034 and ADR-0041. Create an ADR only if implementation
introduces a durable generic import framework, new import state vocabulary,
new canonical events, or a reusable cross-workspace selective promotion
architecture beyond thesis and plan slices.

**Resolution Summary:**
Implemented a Plan Workspace advisory import mediation path parallel to
TF-R001 while preserving stricter execution-boundary controls.

Added `GET /advisory/plan-imports` for read-only `plan_draft.v1` import
previews filtered by persona, workspace, decision, and symbol. Added
`POST /advisory/plan-imports/scan-local` for on-demand local markdown scan into
non-canonical advisory artifacts. The plan mapper supports only
`entry_rationale`, `stop_rationale`, `target_rationale`, and `risk_notes`, and
ignores artifacts that attempt prohibited mapped authority such as sizing,
prices, quantities, broker orders, approval, or execution instructions.

Extended `POST /lifecycle/decisions/create-plan` with optional import
provenance validation. Missing or non-matching source advisory artifact IDs are
rejected with 422. Valid provenance is stored on the normal
`decision.plan_created` payload under `m14c_import_provenance`; the canonical
plan remains the operator-authored lifecycle event.

Updated Plan Development UI with advisory plan import previews, local scan,
field accept/reject controls, edited/unchanged import markers, and provenance
submission. `sizing_rationale` remains manually authored and is never
auto-filled by import mediation. Replay now labels plan import provenance as
`Advisory source, operator-authored plan` and shows explicit no-sizing,
no-approval, and no-execution authority flags.

**Verification Completed:**

- `uv run pytest tests\test_advisory_artifact.py tests\test_create_plan_workflow.py tests\test_develop_thesis_workflow.py`
- `uv run mypy src\app\api\routes.py tests\test_advisory_artifact.py tests\test_create_plan_workflow.py`
- `uv run ruff check src\app\api\routes.py tests\test_advisory_artifact.py tests\test_create_plan_workflow.py --select F`
- `npm.cmd run typecheck`
- `npm.cmd run build`
- `git diff --check`

---

# M-PT — Paper Execution And Outcome Truth (registered 2026-07-09)

Detailed authoritative plan for all TF-P issues:
`knowledge/raw/20260709-paper-trading-implementation-plan.md`
(TradeForge-KnowledgeBase repository). Entries below are register-level
summaries; the KB plan holds full scope, guard design, and testing strategy.

Shared invariant frame for all TF-P issues: Human Decision Sovereignty,
Event Ledger Canonical Truth, Lifecycle Authority, AI Advisory Boundary,
Replayability Is Foundational, Layer Separation.

---

## TF-P001: ADR — Paper Execution Boundary Model

**Status:** Planned

**Milestone:** M-PT

**Branch:** `docs/tf-p001-paper-execution-adr`

**Affected Layer:** docs (ADR), KB event taxonomy

**Linked ADRs:** new ADR; relates to ADR-0001, ADR-0002, ADR-0032, ADR-0036

**Problem:** No architectural decision exists for broker-backed paper
execution: port contract, event taxonomy, replay safety, human-command-only
invocation.

**Scope:** Author the ADR covering ExecutionPort, paper-only scope, the
`PaperOrder*` event family, broker-as-reconciled-external-system, and the
three-layer paper guard. Update KB `EVENT_TAXONOMY.md` and glossary.

**Acceptance Criteria:** ADR accepted; no invariant weakened; event names
carry the `Paper` prefix.

**Out Of Scope:** Live trading in any form; auto-submit on Armed triggers.

---

## TF-P002: Register M-PT Issues And Roadmap Entry

**Status:** Planned

**Milestone:** M-PT

**Branch:** `docs/tf-p002-mpt-registration`

**Affected Layer:** docs

**Scope:** Verify/complete this register section and the roadmap entry after
TF-P001 lands (ADR number backfilled into all TF-P entries).

**Acceptance Criteria:** Register and roadmap agree with the accepted ADR.

---

## TF-P003: Paper Order Domain Model And Validation

**Status:** Planned

**Milestone:** M-PT

**Branch:** `feature/tf-p003-paper-order-domain`

**Affected Layer:** domain, tests

**Linked ADRs:** TF-P001 ADR, ADR-0001, ADR-0002

**Problem:** No domain representation exists for order intent, order state,
or fill facts.

**Scope:** New `src/domain/execution/` package: `PaperOrderIntent`, order
state machine, pure validators (plan stage, qty, limit-price rules), the
`PaperOrder*` event dataclasses. `mode` literal-fixed to `"paper"` (guard
layer 1). No I/O or SDK imports.

**Acceptance Criteria:** State machine and validator tests pass; non-paper
intent construction raises; domain purity preserved.

**Out Of Scope:** Broker calls; service orchestration; UI.

---

## TF-P004: ExecutionPort Protocol And Alpaca Paper Adapter

**Status:** Planned

**Milestone:** M-PT

**Branch:** `feature/tf-p004-alpaca-paper-adapter`

**Affected Layer:** domain (port), infrastructure, tests

**Linked ADRs:** TF-P001 ADR, ADR-0032, ADR-0037

**Scope:** ExecutionPort protocol (submit/cancel/status/open-orders/
position); `AlpacaPaperExecutionAdapter` with `TradingClient(paper=True)`
hardcoded (guard layer 2); credential resolution via existing CredentialStore
alpaca shape at composition root; typed error mapping; broker timestamps and
order ids preserved for provenance.

**Acceptance Criteria:** Mocked-SDK tests prove `paper=True` construction,
response mapping, and error mapping.

**Out Of Scope:** Live-mode configuration; streaming/websockets.

---

## TF-P005: In-Memory FakeExecutionAdapter

**Status:** Planned

**Milestone:** M-PT

**Branch:** `feature/tf-p005-fake-execution-adapter`

**Affected Layer:** infrastructure, tests

**Scope:** Deterministic ExecutionPort fake with scriptable fills
(instant-fill and never-fill modes); default adapter when no Alpaca
credential exists; simulated fills at persisted snapshot prices.

**Acceptance Criteria:** Whole execution feature operable with zero
credentials; fake is the service-test backbone.

---

## TF-P006: ExecutionOrchestrationService

**Status:** Planned

**Milestone:** M-PT

**Branch:** `feature/tf-p006-execution-orchestration`

**Affected Layer:** services, tests

**Linked ADRs:** TF-P001 ADR, ADR-0002

**Problem:** Order submission must be validated against lifecycle state and
recorded as events, invocable only by explicit human command.

**Scope:** `submit_paper_order` / `cancel_paper_order` taking operator
command objects; lifecycle-stage validation (Approved/Armed only); event
append on broker ack; drive Approval to Execution transition through
LifecycleOrchestrationService; import-boundary test proving no dependency
path from `src/services/advisory/` (guard layer 3).

**Acceptance Criteria:** Stage-rejection tests; no event written on broker
failure; advisory import-boundary test green.

**Out Of Scope:** Background sync; AI-triggered submission (forbidden
permanently).

---

## TF-P007: OrderSyncService Polling Reconciliation

**Status:** Planned

**Milestone:** M-PT

**Branch:** `feature/tf-p007-order-sync-service`

**Affected Layer:** services, app (lifespan), tests

**Scope:** Background asyncio polling task (default 30s, env-configurable):
fetch status for ledger-open orders; idempotently append observed
status-change events (dedupe on broker order id + status + fill qty);
graceful degradation on broker unavailability.

**Acceptance Criteria:** Idempotent re-poll test; partial-fill sequence
test; no fabricated events; append-only.

**Out Of Scope:** Websocket streaming; Armed-trigger evaluation (TF-P008).

---

## TF-P008: Armed-Trigger Evaluation To Attention Queue

**Status:** Planned

**Milestone:** M-PT

**Branch:** `feature/tf-p008-armed-trigger-attention`

**Affected Layer:** services, tests

**Scope:** Sync-loop extension evaluating Armed plans structured price
triggers against latest persisted snapshots; on match, raise an attention
item ("trigger met — review and submit?") in the operational attention
queue. Never auto-submits.

**Acceptance Criteria:** Trigger match produces attention item only; no
order submission path exists from trigger evaluation.

**Out Of Scope:** Auto-submit on trigger (requires future dedicated ADR).

---

## TF-P009: Execution API Routes

**Status:** Planned

**Milestone:** M-PT

**Branch:** `feature/tf-p009-execution-routes`

**Affected Layer:** app, tests

**Linked ADRs:** ADR-0020

**Scope:** New router file (NOT routes.py; `routes/execution.py` if M-RF has
landed): POST paper-orders, POST cancel, GET orders by decision, GET
positions by decision.

**Acceptance Criteria:** FastAPI tests per existing conventions; endpoints
require explicit command payloads.

---

## TF-P010: Paper Execution Workspace Surfaces

**Status:** Planned

**Milestone:** M-PT

**Branch:** `feature/tf-p010-execution-workspaces`

**Affected Layer:** frontend

**Scope:** Plan Review submit panel (Approved/Armed only, prefilled from
plan, explicit confirm dialog); Active Position order-status panel + cancel;
persistent PAPER badge on all execution surfaces; Review workspace shows
actual-fill facts beside manual reflection inputs.

**Acceptance Criteria:** Typecheck + build green; PAPER badge present on
every execution surface; confirm dialog restates symbol/side/qty/price.

---

## TF-P011: Execution-Quality Facts In Review Projections

**Status:** Planned

**Milestone:** M-PT

**Branch:** `feature/tf-p011-execution-quality-review`

**Affected Layer:** services (projections), domain (read models), tests

**Linked ADRs:** ADR-0044

**Scope:** Deterministic derived fields from broker facts: planned vs actual
entry, slippage, holding period, realized P&L; feed behavioral signals
(sizing deviation from real fills). Authority-labeled `derived`.

**Acceptance Criteria:** Deterministic tests; authority labels present;
no approval gating from metrics.

---

## TF-P012: M-PT Docs, Demo Flow, And KB Synthesis

**Status:** Planned

**Milestone:** M-PT

**Branch:** `docs/tf-p012-mpt-closeout`

**Affected Layer:** docs, KB

**Scope:** README paper-trading quickstart; HOW-TO-SETUP-KEYS paper note;
demo flow option on FakeExecutionAdapter; KB processed synthesis.

**Acceptance Criteria:** Fresh-clone quickstart verified; register/roadmap
statuses synchronized.

---

# M-EZ — Ease Of Use, Evidence Density, And Entry Ramp (registered 2026-07-09)

Detailed authoritative plan:
`knowledge/raw/20260709-product-viability-and-ease-of-use-roadmap.md`
(TradeForge-KnowledgeBase repository).

---

## EZ-01: Postgres-By-Default Single Compose Stack

**Status:** Planned

**Milestone:** M-EZ

**Branch:** `feature/ez-01-single-compose-stack`

**Affected Layer:** infrastructure (compose/Dockerfile), app (static serving)

**Scope:** `docker compose up` yields postgres + backend + served frontend
build at one URL; `alembic upgrade head` on container start; frontend build
stage in runtime image or nginx sidecar.

**Acceptance Criteria:** Fresh machine with Docker, one command, working
persistent app in browser; no uv/Node/second terminal.

---

## EZ-02: In-App First-Run Wizard

**Status:** Planned

**Milestone:** M-EZ

**Branch:** `feature/ez-02-first-run-wizard`

**Affected Layer:** app, security, frontend

**Linked ADRs:** ADR-0037

**Scope:** Setup mode when no master key and no `.keys.enc`: UI generates
master key, shows once, persists to compose-mounted env file (documented
trust tradeoff); credentials remain optional (yfinance default).

**Acceptance Criteria:** No terminal needed after `docker compose up`;
existing CLI path still works; secrets never logged.

---

## EZ-03: Documentation Truth Pass

**Status:** Planned

**Milestone:** M-EZ

**Branch:** `docs/ez-03-doc-truth-pass`

**Affected Layer:** docs

**Scope:** Fill or delete empty `DOCS/architecture.md`, `DOCS/domain-model.md`,
`DOCS/event-schema.md`; rewrite stale `PROJECT.md`; consolidate to a single
authoritative roadmap file.

**Acceptance Criteria:** No empty docs; PROJECT.md reflects current state;
one roadmap authority.

---

## EV-01: Scheduled Market Snapshot Job

**Status:** Planned

**Milestone:** M-EZ

**Branch:** `feature/ev-01-scheduled-snapshots`

**Affected Layer:** services, app (lifespan), tests

**Linked ADRs:** ADR-0010, ADR-0032, ADR-0038

**Scope:** In-process background refresh of snapshots for symbols on active
decisions + watchlist; configurable cadence (hourly market hours, daily
close otherwise); persists through existing snapshot boundary with
provenance; replay never calls live APIs.

**Acceptance Criteria:** Cadence configurable; failures degrade gracefully;
snapshots provenance-tagged.

---

## EV-02: Watchlist As First-Class Pre-Lifecycle Object

**Status:** Planned

**Milestone:** M-EZ

**Branch:** `feature/ev-02-watchlist`

**Affected Layer:** domain, services, app, frontend

**Scope:** Watchlist entry = symbol + one-line rationale + date;
pre-lifecycle (not a TradeIdea); feeds EV-01 scanning and Opportunity
Workspace; promotable to TradeIdea by explicit operator action.

**Acceptance Criteria:** No lifecycle events from watchlist CRUD; promotion
creates a canonical TradeIdea via existing workflow only.

---

## EV-03: Per-Symbol Evidence Panel

**Status:** Planned

**Milestone:** M-EZ

**Branch:** `feature/ev-03-evidence-panel`

**Affected Layer:** services, app, frontend

**Scope:** Deterministic evidence answering the blue-pin questions: last
price, % change, volume vs average, 52w distance, next earnings, prior
high/low and moving-average levels, fundamentals snapshot via existing
adapters. Every fact timestamped + provider-tagged. AI interpretation stays
a separate advisory overlay.

**Acceptance Criteria:** Panel renders with yfinance-only (no keys);
deterministic values test-covered; provenance visible.

---

## EV-04: Basic Price Chart Component

**Status:** Planned

**Milestone:** M-EZ

**Branch:** `feature/ev-04-price-chart`

**Affected Layer:** frontend, app (bars endpoint if needed)

**Linked ADRs:** ADR-0007 (compliance note: visual evidence inside a
decision surface, not dashboard organization)

**Scope:** One reusable candlestick/line chart fed from persisted
snapshots/bars; embedded in evidence panel and decision workspaces.

**Acceptance Criteria:** Renders from persisted data only; typecheck +
build green.

---

## RAMP-01: Quick-Capture Idea Tier

**Status:** Planned

**Milestone:** M-EZ

**Branch:** `feature/ramp-01-quick-capture`

**Affected Layer:** app, frontend, services

**Linked ADRs:** ADR-0002, ADR-0034

**Scope:** "Jot an idea" input (symbol + 2 sentences) creating a TradeIdea
with draft-status stub thesis; full structured thesis remains mandatory at
Approval gate.

**Acceptance Criteria:** Lifecycle unchanged; Approval blocked until thesis
complete; capture takes under 30 seconds.

---

## RAMP-02: Guided First-Decision Mode

**Status:** Planned

**Milestone:** M-EZ

**Branch:** `feature/ramp-02-guided-first-decision`

**Affected Layer:** frontend

**Scope:** Extend existing walkthrough/onboarding assets into a
persona-neutral guided path with plain-language labels and a beginner
glossary layer.

**Acceptance Criteria:** A non-trader can complete one full lifecycle with
guidance only.

---

## RAMP-03: Operator Identity Profiles

**Status:** Planned

**Milestone:** M-EZ

**Branch:** `feature/ramp-03-operator-identity`

**Affected Layer:** domain (events), services, app, frontend

**Linked ADRs:** ADR-0022 (extends)

**Scope:** Named operator profiles (household trust tier, no passwords);
explicit `operator_id` on new canonical events; workspace filtering by
operator.

**Acceptance Criteria:** Two operators keep separate decision histories;
prior events remain valid (migration/back-compat defined in planning).

---

## GOV-01: Two-Tier Issue Discipline Documentation

**Status:** Planned

**Milestone:** M-EZ

**Branch:** `docs/gov-01-two-tier-discipline`

**Affected Layer:** docs (AGENTS.md, CLAUDE.md)

**Scope:** Document Tier A (full ceremony: domain/events/lifecycle/
persistence/security/advisory boundary) vs Tier B (batch issues: frontend
copy/layout/styling/docs).

**Acceptance Criteria:** Both agent bootstrap files updated consistently.

---

## GOV-02: Knowledge Base Hygiene Pass

**Status:** Planned

**Milestone:** M-EZ

**Branch:** `docs/gov-02-kb-hygiene` (KB repository work)

**Affected Layer:** knowledge base repository

**Scope:** Archive 4.1 MB litellm log out of `knowledge/raw/`; consolidate
root `raw/` into `knowledge/raw/`; mark M15 TF-D001 through TF-D008
explicitly deferred (or register them).

**Acceptance Criteria:** Single raw location; no oversized binaries/logs in
raw; M15 issue status unambiguous.

---

# M-RF — API Boundary Decomposition (registered 2026-07-09)

Detailed authoritative plan (full per-phase scope, target structure, agent
guardrails): `knowledge/raw/20260709-routes-refactor-implementation-plan.md`
(TradeForge-KnowledgeBase repository).

Shared frame for all TF-RF issues — **Status:** Planned; **Milestone:** M-RF;
**Affected Layer:** app, tests (TF-RF009 also services); **Linked ADRs:**
ADR-0020; **Impacted Invariants:** Layer Separation (semantics unchanged);
**Shared acceptance criteria:** OpenAPI contract snapshot byte-identical;
`uv run pytest`, `ruff`, `mypy` green; every moved symbol defined exactly
once; move-only (no renames, no behavior change) except where an issue below
states otherwise.

- **TF-RF001** — OpenAPI contract snapshot test. Create
  `tests/test_api_contract_snapshot.py` + committed snapshot of
  `app.openapi()` and the route table. The golden gate for all later phases.
- **TF-RF002** — Extract the ~30 `_x_service_from(request)` accessors to
  `src/app/api/deps.py`, names verbatim.
- **TF-RF003** — Create `src/app/api/routes/` package; move `runtime` and
  `behavioral` domains (handlers + models + mappers) as pattern-setters.
- **TF-RF004** — Move `replay`, `provenance`, `market` domains.
- **TF-RF005** — Move `workspace` domain incl. attention/playbook mappers.
- **TF-RF006** — Move `lifecycle` domain (largest; includes mid-file
  `ThesisArtifactResponse`; shared `EntityReferencePayload` may seed
  `shared_schemas.py`).
- **TF-RF007** — Move advisory family as three modules: `advisory`,
  `advisory_generation`, `advisory_analytics` (incl. mid-file model block).
- **TF-RF008** — Move governance endpoints + helpers; path fidelity wins
  over router-tag tidiness.
- **TF-RF009** — SEMANTIC MOVE: relocate markdown import parsing
  (~2722–3078 of the monolith) to
  `src/services/advisory/local_import_parsing.py` (layer correction,
  INVARIANTS section 9); moved bodies byte-identical except imports/prefix.
- **TF-RF010** — Assemble routers in `routes/__init__.py`; repoint
  `application.py`; delete `routes.py`; update architecture docs.

---

# M-RF2 — API Dependency Injection (registered 2026-07-09)

**Blocked on:** M-RF complete (TF-RF010 landed). Detailed authoritative,
self-contained plan:
`knowledge/raw/20260709-depends-injection-conversion-plan.md`
(TradeForge-KnowledgeBase repository).

Shared frame for all TF-RF2 issues — **Status:** Planned; **Milestone:**
M-RF2; **Affected Layer:** app, tests; **Linked ADRs:** ADR-0020;
**Shared acceptance criteria:** OpenAPI snapshot byte-identical throughout
(dependency functions take exactly one parameter, `request: Request`);
existing tests pass unmodified; full gates green per phase.

- **TF-RF2-001** — Accessor inventory: classify call sites handler-direct
  (Class H) vs helper-internal (Class F); list exclusions.
- **TF-RF2-002** — Rename accessors to public `get_*` names; full call-site
  sweep; grep gates (old names zero, new names defined once).
- **TF-RF2-003** — Convert Class H sites to
  `Annotated[Type, Depends(get_x)]`, one module per commit; drop `request`
  param only where nothing else uses it.
- **TF-RF2-004** — Convert request-taking helpers to explicit service
  parameters; helpers needing 4+ services may keep `request` (documented).
- **TF-RF2-005** — Add one `tests/test_dependency_overrides.py`
  demonstration test using `app.dependency_overrides`.
- **TF-RF2-006** — Closeout: grep gates, snapshot diff empty across the
  milestone, KB synthesis; record deferred idea (create_app kwarg plumbing
  simplification).

---

# M-RF-FE — Frontend API Client Decomposition (registered 2026-07-09)

Detailed authoritative plan:
`knowledge/raw/20260709-frontend-api-client-refactor-plan.md`
(TradeForge-KnowledgeBase repository). Independent of M-RF; land both before
M-PT frontend work.

Shared frame for all TF-RFE issues — **Status:** Planned; **Milestone:**
M-RF-FE; **Affected Layer:** frontend; **Shared acceptance criteria:**
`npm run typecheck` and `npm run build` green per phase; `runtime.ts` barrel
keeps every symbol importable at all times (33 importers untouched);
each moved symbol defined exactly once under `src/api/`; move-only except
TF-RFE007.

- **TF-RFE001** — Extract `http.ts`: move `readOperationalJson`, add
  `requestJson<T>` wrapper; do not touch the ~49 hand-rolled fetch sites.
- **TF-RFE002** — Move `behavioral.ts` + `replay.ts` (pattern-setters).
- **TF-RFE003** — Move `workspace.ts` + `market.ts` (incl. query builders).
- **TF-RFE004** — Move `lifecycle.ts` (largest; `shared.ts` decision point
  for `EntityReferencePayload`).
- **TF-RFE005** — Move `advisory.ts`, `advisoryGeneration.ts`, `imports.ts`.
- **TF-RFE006** — Move `governance.ts` (incl. credentials +
  `PROVIDER_CREDENTIAL_SCHEMAS`); `runtime.ts` retains barrel + runtime
  status/session fetchers.
- **TF-RFE007** — SEMANTIC PHASE: convert ~49 hand-rolled fetch sites to
  `requestJson`; pre-grep workspaces for error-message string matching;
  per-domain commits; manual failure-path smoke per domain; zero raw
  `fetch(` outside `http.ts` afterward.
- **TF-RFE008** — Closeout: barrel end-state decision, `frontend/DESIGN.md`
  module map, KB synthesis; register deferred OpenAPI-generated-types and
  vitest ideas.

---
