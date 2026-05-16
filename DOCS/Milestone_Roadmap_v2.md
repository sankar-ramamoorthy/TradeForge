
---
title: Milestone Roadmap v2
type: index
status: canonical
tags: [TradeForge, roadmap, milestones, architecture, cognition, workspaces]
created: 2026-05-09
updated: 2026-05-13
supersedes: MILESTONE_ROADMAP_DEPRECATED.md
---

# Milestone Roadmap v2

## Purpose

This document defines the upgraded milestone roadmap for TradeForge.

This roadmap reflects the architectural realization that TradeForge is not primarily:

- a brokerage platform
- a charting system
- a dashboard application
- an autonomous trading bot

TradeForge is instead:

> a replayable discretionary cognition and workflow system for trading and investing operations.

This roadmap therefore organizes milestones around:

- semantic truth
- workflow continuity
- operational cognition
- replayability
- workspace architecture
- behavioral review
- disciplined decision infrastructure

rather than around isolated technical implementation tasks.

---

# Authority Model

Authority separation remains mandatory.

| Layer | Responsibility |
|---|---|
| Knowledge Base | semantic truth, cognition model, doctrine |
| Runtime Repo | implementation architecture and execution |
| GitHub Issues | execution tracking |
| ADRs | architectural decision history |
| Design Layer | workspace and interaction architecture |

---

# Core Architectural Principles

TradeForge remains governed by:

- event sourcing
- immutable ledger truth
- workflow-centric architecture
- replayability
- explicit review
- human decision sovereignty
- anti-dashboard UX
- cognition-first interaction design

---

# Alignment References

Core doctrine:

- [[INVARIANTS]]
- [[ARCHITECTURE]]
- [[UX_DOCTRINE]]
- [[WORKSPACES]]
- [[EVENT_TAXONOMY]]
- [[PERSONAS]]
- [[VISION]]

---

# M0 â€” Planning Discipline And Architectural Memory

**Status:** Done

## Semantic Intent

Establish durable architectural memory before implementation expansion.

## Architectural Significance

TradeForge requires explicit separation between:

- semantic truth
- runtime implementation
- execution tracking
- operational cognition

without collapsing architectural intent into code tasks.

## Canonical Concepts

- [[Architectural Memory]]
- [[Semantic Truth Layer]]
- [[Issue Register]]
- [[Milestone Roadmap]]

## Linked Runtime Issues

- TF-0001: Establish milestone roadmap and issue register (**Done**)

## Acceptance Meaning

- Semantic truth remains distinct from runtime implementation.
- Architectural reasoning remains durable and replayable.
- Execution tracking does not become semantic authority.

---

# M1 â€” Runtime Scaffold And Developer Environment

**Status:** Done

## Semantic Intent

Establish reproducible implementation infrastructure.

## Architectural Significance

Tooling supports runtime consistency but does not define TradeForge semantics.

## Linked Runtime Issues

- TF-0002: Create Python project scaffold with uv (**Done**)
- TF-0003: Add Dockerfile runtime environment (**Done**)
- TF-0004: Add Docker Compose local development setup (**Done**)
- TF-0005: Add pytest baseline and testing conventions (**Done**)
- TF-0006: Add lint/type/developer commands (**Done**)
- TF-0007: Add runtime README setup conventions (**Done**)

## Acceptance Meaning

- Runtime development is reproducible.
- Tooling remains subordinate to semantic truth.

---

# M1A â€” Canonical Entity Definitions

**Status:** Done

## Semantic Intent

Define stable semantic objects before runtime expansion.

## Architectural Significance

Canonical entities stabilize:

- workflow semantics
- event meaning
- replay integrity
- projection interpretation

## Canonical Entities

- [[TradeIdea]]
- [[TradeThesis]]
- [[TradePlan]]
- [[Scenario]]
- [[Workspace]]
- [[LifecycleEvent]]
- [[ReplaySession]]
- [[ReviewArtifact]]
- [[MarketContext]]
- [[ExecutionIntent]]

## Linked KB Issues

- KB-0001: Define canonical entity semantics (**Done**)

## Acceptance Meaning

- Runtime implementation cannot silently redefine core semantics.
- Event and replay systems depend on stable entity meaning.

---

# M2 â€” Event Ledger And Canonical Event Model

**Status:** Done

## Semantic Intent

Stabilize immutable event-backed truth.

## Architectural Significance

All durable state derives from immutable replayable events.

## Canonical Concepts

- [[Event Ledger]]
- [[Canonical State]]
- [[Derived State]]
- [[Replay System]]

## Linked Runtime Issues

- TF-0008: Define canonical event envelope (**Done**)
- TF-0009: Define append-only event store interface (**Done**)
- TF-0010: Implement in-memory event store adapter (**Done**)

## Acceptance Meaning

- Events remain factual rather than interpretive.
- Replayable truth becomes foundational.

---

# M3 â€” Decision Lifecycle Engine

**Status:** Done

## Semantic Intent

Stabilize workflow authority.

## Architectural Significance

TradeForge is workflow-centric rather than CRUD-centric.

## Canonical Lifecycle

```text
Idea
â†’ Thesis
â†’ Plan
â†’ Approval
â†’ Execution
â†’ Position
â†’ Review
````

## Linked Runtime Issues

* TF-0011: Define lifecycle state model (**Done**)
* TF-0012: Implement lifecycle transition validator (**Done**)
* TF-0013: Implement lifecycle orchestration service (**Done**)

## Acceptance Meaning

* Explicit lifecycle authority exists.
* Human approval remains mandatory.
* Workflow continuity becomes canonical.

---

# M4 â€” Workspace And Cognitive Architecture

**Status:** Done

## Semantic Intent

Define TradeForge as a workspace-centric operational cognition system.

## Architectural Significance

TradeForge workspaces are operational cognitive environments rather than dashboards or screens.

## Canonical Concepts

* [[Workspace]]
* [[Decision Queue]]
* [[Replay Workspace]]
* [[Review Workspace]]
* [[Behavioral Signals]]
* [[Thesis Drift]]

## Linked KB Issues

* KB-0002: Introduce design directory structure (**Done - draft design layer introduced 2026-05-10**)
* KB-0003: Define workspace architecture doctrine
* KB-0004: Define navigation model
* KB-0005: Define operational workspace model
* KB-0006: Define interaction pattern model
* KB-0007: Define replay-centric UX doctrine

## Linked Runtime Issues

* TF-0014: Create workspace routing model (**Done**)
* TF-0015: Define workspace state contracts (**Done**)

## Acceptance Meaning

* Draft design architecture is established without superseding KB doctrine.
* Workspaces are prepared for canonical stabilization through ADRs and projection contracts.
* UX becomes cognition-first and workflow-centric.
* Anti-dashboard principles become explicit doctrine.

---

# M5 â€” Replay And Projection Foundation

**Status:** Done

## Semantic Intent

Make replay and derived operational state foundational capabilities.

## Architectural Significance

Replay reconstructs cognition while projections provide discardable operational read models.

## Canonical Concepts

* [[Replay System]]
* [[Projection]]
* [[Derived State]]
* [[Operational Surface]]

## Linked Runtime Issues

* TF-0016: Implement replay projector foundation (**Done**)
* TF-0017: Implement projection rebuild pipeline (**Done**)
* TF-0018: Implement replay timeline engine (**Done**)
* TF-0019: Implement historical reconstruction pipeline (**Done**)

## Acceptance Meaning

* Replay reconstructs historical workflow state.
* Projections remain rebuildable and non-authoritative.

---

# M6 â€” Persona Workspace Projection Layer

**Status:** Done

## Semantic Intent

Define persona-scoped operational workspaces.

## Architectural Significance

Operational interpretation becomes persona-aware without mutating canonical truth.

## Canonical Concepts

* [[Persona]]
* [[Persona Workspace]]
* [[Opportunity Workspace]]
* [[Review Workspace]]
* [[Market Context Workspace]]

## Linked Runtime Issues

* TF-0020: Define persona context model (**Done**)
* TF-0021: Implement workspace projection read models (**Done**)
* TF-0022: Implement operational attention queues (**Done**)
* TF-0023: Implement context-aware workspace summaries (**Done**)

## Acceptance Meaning

* Workspaces become operational cognition environments.
* Personas shape interpretation but not truth.

---

# M7 â€” MVP Runtime Infrastructure

**Status:** Done

## Semantic Intent

Establish the runtime infrastructure required for a real operational MVP.

## Architectural Significance

TradeForge transitions from conceptual architecture into usable operational software.

## Canonical Concepts

* [[Operational Runtime]]
* [[Projection Persistence]]
* [[Workspace Runtime]]

## Linked Runtime Issues

### Persistence

* TF-0024: Add Postgres persistence layer (**Done**)
* TF-0025: Add Alembic migration infrastructure (**Done**)
* TF-0026: Persist canonical event ledger (**Done**)

### API Layer

* TF-0027: Add FastAPI application runtime (**Done**)
* TF-0028: Add lifecycle API endpoints (**Done**)
* TF-0029: Add replay API endpoints (**Done**)
* TF-0030: Add workspace projection APIs (**Done**)

### Frontend Runtime

* TF-0031: Create React frontend scaffold (**Done**)
* TF-0032: Add workspace routing system (**Done**)
* TF-0033: Add shared operational layout system (**Done**)
* TF-0034: Add authentication/session model (**Done**)

## Acceptance Meaning

* TradeForge becomes deployable as a real application.
* Durable persistence exists.
* Workspaces become operationally usable.

---

# M8 â€” First Operational MVP Vertical Slice

**Status:** Done

## Semantic Intent

Demonstrate the first complete replayable operational workflow.

## Architectural Significance

TradeForge proves itself as a replayable discretionary cognition system.

## MVP Scope

The MVP vertical slice must support:

```text
Idea
â†’ Thesis
â†’ Plan
â†’ Approval
â†’ Position
â†’ Replay
â†’ Review
```

## Required Workspaces

* Operating Workspace
* Opportunity Workspace
* Plan Review Workspace
* Active Position Workspace
* Replay Workspace
* Review Workspace

## Linked Runtime Issues

* TF-0035: Implement Operating Workspace (**Done**)
* TF-0036: Implement Opportunity Workspace (**Done**)
* TF-0037: Implement Plan Review Workspace (**Done**)
* TF-0038: Implement Active Position Workspace (**Done**)
* TF-0039: Implement Replay Workspace (**Done**)
* TF-0040: Implement Review Workspace (**Done**)
* TF-0041: Implement first replayable lifecycle flow (**Done**)

## Acceptance Meaning

* Lifecycle continuity is operational.
* Replay and review are first-class capabilities.
* Workspace state derives from canonical events.
* MVP v1 becomes operationally usable.

---


# M9 — Market Context and Provider Layer

**Status:** Done

## Semantic Intent

Introduce real-world market context through read-only provider boundaries without compromising replayability or human decision sovereignty.

## Architectural Significance

Market data augments operational cognition rather than becoming execution authority.

TradeForge remains:

```text
a replayable discretionary cognition system
```

rather than:

* a brokerage platform
* a charting terminal
* an automated trading engine
* a market-scanning dashboard

## Core Principle

External market context is:

```text
read-only
advisory
replay-aware where possible
non-canonical
```

Canonical truth continues to derive only from:

* lifecycle events
* review artifacts
* workflow decisions
* replayable event history

## Canonical Concepts

* [[Market Context]]
* [[Market Snapshot]]
* [[Provider Boundary]]
* [[Scenario]]
* [[Market Regime]]
* [[Contextual Interpretation]]
* [[Advisory Overlay]]

## MVP M9 Scope

M9 introduces:

* read-only market data
* provider normalization
* contextual workspace overlays
* market snapshots
* regime interpretation
* advisory operational context

M9 explicitly excludes:

* live broker execution
* autonomous AI decisions
* automated trade placement
* websocket infrastructure
* high-frequency streaming
* RL systems
* autonomous scanning agents

## Recommended Initial Providers

Initial provider integrations may include:

* yfinance
* Massive.com / Polygon
* Alpaca market data

Provider selection must remain:

```text
replaceable
normalized
non-authoritative
```

## Linked Runtime Issues

### Provider Infrastructure

* TF-0042: Define provider boundary interfaces (**Done**)
* TF-0043: Implement normalized market snapshot model (**Done**)
* TF-0044: Add read-only yfinance provider adapter (**Done**)
* TF-0045: Add Massive.com market data adapter (**Done**)
* TF-0046: Add Alpaca market data adapter (**Done**)

### Workspace Context

* TF-0047: Implement market context workspace overlays (**Done**)
* TF-0048: Implement market regime interpretation model (**Done**)
* TF-0049: Implement contextual operational summaries (**Done**)
* TF-0050: Implement provider provenance tracking (**Done**)

### Demo Enablement

* TF-0051: Add seeded demo market context flow (**Done**)
* TF-0052: Add replay-compatible market snapshot persistence strategy (**Done**)

## Acceptance Meaning

* Real-world market context becomes visible.
* Workspace cognition becomes operationally believable.
* Provider data remains advisory.
* Replay boundaries remain explicit.
* External APIs do not become canonical truth.
* Human lifecycle authority remains preserved.

---


---

# M10 — Operational Workflow UX And Demoability

**Status:** Done

---

## Semantic Intent

Transform TradeForge from an architecturally operational system into a human-operable discretionary cognition environment.

---

## Architectural Significance

TradeForge has established:

* replayable workflow authority
* workspace cognition
* lifecycle continuity
* market context augmentation
* event-backed operational truth

However, operational usability remains overly developer-centric.

M10 stabilizes the operational interaction layer required for:

* human workflow continuity
* friction-light cognition
* guided operational flow
* trader-oriented onboarding
* demoability
* operational coherence

without compromising:

* replayability
* semantic integrity
* lifecycle authority
* human decision sovereignty

TradeForge therefore evolves from:

```text id="rcljmo"
an architecturally operational cognition platform
```

toward:

```text id="itjwm7"
a human-operable discretionary trading workflow system
```

---

## Core Principle

Operational workflow enforcement should feel:

```text id="oq7g3k"
continuous
context-aware
intentional
operationally natural
```

rather than:

```text id="b2c1eu"
procedural
fragmented
developer-oriented
```

The workflow architecture remains authoritative while interaction friction becomes subordinate to cognition.

---

## Canonical Concepts

* [[Operational Continuity]]
* [[Guided Workflow]]
* [[Workflow Ergonomics]]
* [[Demoability]]
* [[Decision Context]]
* [[Workspace Cohesion]]
* [[Operational Navigation]]
* [[Attention Continuity]]
* [[Lifecycle Bootstrapping]]

---

## M10 Scope

M10 introduces:

* guided lifecycle onboarding
* friction-light workflow progression
* automatic operational context propagation
* persistent active decision continuity
* cross-workspace operational cohesion
* seeded guided demo flows
* simplified lifecycle initialization
* trader-oriented workflow ergonomics
* operational navigation stabilization
* workspace continuity infrastructure

M10 explicitly excludes:

* autonomous AI execution
* AI trade approval
* broker integration
* automated trade execution
* RL systems
* strategy automation
* autonomous scanning agents

---

# Linked Runtime Issues

---

## Lifecycle Bootstrapping

### TF-0053 — Implement New Trade Idea Workflow (**Done**)

#### Purpose

Replace manual lifecycle bootstrapping through API calls with an operational workflow-native entry experience.

#### Scope

Introduce:

* “New Trade Idea” workflow entry
* symbol initialization
* thesis seed capture
* persona association
* workspace initialization
* canonical lifecycle event creation

#### Acceptance Criteria

* No curl/API call required to initiate workflow.
* New decisions initialize through operational UI flow.
* Lifecycle integrity remains event-backed.

---

### TF-0054 — Implement Persistent Active Decision Context (**Done**)

#### Purpose

Stabilize operational continuity across workspace transitions.

#### Scope

Introduce:

* active decision persistence
* session continuity
* workspace restoration
* operational context recovery

#### Acceptance Criteria

* Active decision context survives navigation.
* Manual query parameter propagation is eliminated.
* Workspace continuity becomes operationally stable.

---

### TF-0055 — Eliminate Manual Workspace Context Propagation (**Done**)

#### Purpose

Remove developer-centric routing dependencies from operational workflow usage.

#### Scope

Remove dependency on:

* manual query params
* explicit workspace identifiers in navigation
* manual persona propagation

Introduce:

* centralized operational context resolution
* shared workflow state

#### Acceptance Criteria

* Workspaces automatically resolve active operational context.
* Manual URL parameter workflows are unnecessary.

---

# Guided Operational Flow

---

### TF-0056 — Implement Guided Lifecycle Navigation (**Done**)

#### Purpose

Make lifecycle progression cognitively explicit and operationally discoverable.

#### Scope

Introduce:

* guided lifecycle progression
* contextual next-step navigation
* stage-aware operational prompts
* workspace progression awareness

#### Acceptance Criteria

* Users can understand operational progression without architectural knowledge.
* Workflow continuity becomes visually understandable.

---

### TF-0057 — Implement Operational Workflow Continuity Model (**Done**)

#### Purpose

Ensure workspace transitions feel continuous rather than fragmented.

#### Scope

Introduce:

* workflow continuity state
* operational breadcrumbs
* cross-workspace decision awareness
* lifecycle continuity indicators

#### Acceptance Criteria

* Workspace movement preserves cognitive continuity.
* The system feels like one operational environment rather than disconnected screens.

---

# Demoability Infrastructure

---

### TF-0058 — Implement Guided Demo Mode (**Done**)

#### Purpose

Create a deterministic operational walkthrough experience for demonstrations and onboarding.

#### Scope

Introduce:

* guided operational walkthroughs
* deterministic seeded lifecycle flows
* stage-by-stage progression
* operational explanation overlays

#### Acceptance Criteria

* A user can experience TradeForge without manual setup.
* Demo flow remains replayable and deterministic.

---

### TF-0059 — Implement Seeded Replayable Demo Scenarios (**Done**)

#### Purpose

Provide realistic operational scenarios for demonstrations and replay workflows.

#### Scope

Introduce seeded scenarios for:

* breakout swing trade
* failed thesis drift
* regime transition
* disciplined exit review

#### Acceptance Criteria

* Replay workspaces contain meaningful operational examples.
* Demo scenarios illustrate workflow philosophy.

---

### TF-0060 — Implement One-Click Operational Walkthrough (**Done**)

#### Purpose

Reduce operational onboarding friction.

#### Scope

Introduce:

* one-click demo initialization
* automatic scenario loading
* operational workspace initialization
* guided workflow activation

#### Acceptance Criteria

* A complete operational walkthrough launches from a single entry point.

---

### TF-0061 — Implement Operational Onboarding Flow (**Done**)

#### Purpose

Introduce trader-oriented onboarding aligned with TradeForge philosophy.

#### Scope

Introduce onboarding for:

* lifecycle philosophy
* workspace meaning
* review-centric workflow
* decision sovereignty
* replay concepts

#### Acceptance Criteria

* New users understand the system philosophically before operationally.

---

# Workspace Cohesion

---

### TF-0062 — Implement Cross-Workspace Context Persistence (**Done**)

#### Purpose

Stabilize operational cognition across all workspace surfaces.

#### Scope

Introduce:

* shared operational state
* cross-workspace context memory
* synchronized decision context
* operational continuity services

#### Acceptance Criteria

* Workspace transitions preserve operational meaning.

---

### TF-0063 — Stabilize Workspace Transition Ergonomics (**Done**)

#### Purpose

Reduce operational friction between cognitive environments.

#### Scope

Improve:

* navigation flow
* transition clarity
* workspace movement behavior
* contextual navigation stability

#### Acceptance Criteria

* Workspace transitions feel operationally deliberate rather than technical.

---

### TF-0064 — Implement Operational Attention Continuity (**Done**)

#### Purpose

Preserve trader attention state throughout workflow progression.

#### Scope

Introduce:

* operational attention queues
* persistent focus state
* workflow reminders
* stage-aware operational surfacing

#### Acceptance Criteria

* Important operational context is not lost during workflow progression.

---

# Acceptance Meaning

* TradeForge becomes operationally demoable.
* Human traders can operate workflows without architectural knowledge.
* Workflow continuity becomes operationally natural.
* Replayability remains foundational.
* Lifecycle authority remains preserved.
* Cognition-first interaction architecture becomes operationally believable.
* The system transitions from architecture demonstration toward usable operational product experience.

---
# M10A — Structured Decision Authoring And Cognitive Capture

**Status:** Done

---

# Semantic Intent

Transform lifecycle progression from event-only workflow continuity into durable replayable operator cognition.

---

# Architectural Significance

TradeForge currently preserves:

* lifecycle continuity
* replayable workflow state
* canonical event authority
* operational workspace cohesion

However, lifecycle stages presently contain limited structured operator reasoning.

M10A introduces:

```text
durable cognitive artifacts
```

that preserve:

* why decisions existed
* what assumptions mattered
* what scenarios were considered
* how risk was framed
* what invalidated the idea
* how the operator reasoned through uncertainty

TradeForge therefore evolves from:

```text
workflow replay
```

toward:

```text
replayable discretionary cognition
```

---

# Core Principle

Lifecycle stages must preserve:

```text
operator reasoning
```

not merely:

```text
workflow transition existence
```

Replay should eventually reconstruct:

* environmental context
* thesis evolution
* decision assumptions
* scenario branching
* plan intent
* discipline quality
* review reflection

without collapsing cognition into unstructured journaling.

---

# Canonical Concepts

* [[Decision Artifact]]
* [[Structured Thesis]]
* [[Trade Narrative]]
* [[Scenario Branch]]
* [[Decision Assumption]]
* [[Decision Invalidation]]
* [[Execution Intent]]
* [[Playbook Alignment]]
* [[Review Reflection]]
* [[Cognitive Evidence]]
* [[Replay Annotation]]
* [[Cognitive Snapshot]]

---

# Architectural Themes

M10A establishes:

```text
structured cognition persistence
```

before introducing:

* AI advisory systems
* behavioral intelligence
* simulation intelligence
* RL experimentation

This milestone therefore becomes foundational for:

* M11
* M12
* M13
* M14

---

# Scope

M10A introduces:

* structured thesis authoring
* structured trade plan authoring
* review reflection capture
* scenario branch modeling
* cognitive evidence capture
* replay-attached reasoning artifacts
* thesis invalidation tracking
* decision rationale persistence
* playbook alignment surfaces
* cognition-aware replay enrichment

M10A explicitly excludes:

* AI-generated thesis mutation
* autonomous trade planning
* broker execution
* strategy automation
* RL systems
* autonomous approval systems

---

# ADR Requirements

M10A likely requires new ADRs because this milestone changes:

* canonical cognition persistence
* event semantics
* replay reconstruction depth
* projection interpretation
* operator artifact modeling

These are architectural decisions, not merely UI additions.

---

# Required ADRs

---

## ADR-00X — Structured Cognitive Artifact Model

### Purpose

Define canonical modeling strategy for durable operator cognition artifacts.

### Decision Areas

* artifact boundaries
* structured vs freeform cognition
* replay persistence strategy
* attachment to lifecycle stages
* mutation/editing rules
* historical versioning
* event ownership

### Why Required

This changes canonical semantic persistence.

---

## ADR-00Y — Thesis And Plan Authoring Architecture

### Purpose

Define separation between:

* TradeIdea
* TradeThesis
* TradePlan
* ScenarioBranch
* ReviewReflection

### Decision Areas

* ownership boundaries
* projection responsibilities
* validation model
* replay reconstruction semantics
* plan/thesis lifecycle relationship

### Why Required

This stabilizes workflow cognition semantics.

---

## ADR-00Z — Replay Cognitive Reconstruction Strategy

### Purpose

Define how replay reconstructs operator reasoning over time.

### Decision Areas

* temporal cognition snapshots
* annotation reconstruction
* evidence replay
* thesis drift representation
* scenario evolution
* derived vs canonical replay views

### Why Required

Replay semantics fundamentally deepen here.

---

# Linked KB Issues

---

## KB-M10A-001 — Define Structured Thesis Semantics

### Purpose

Define canonical structure for replayable trade thesis artifacts.

### Scope

Define:

* thesis narrative
* catalysts
* assumptions
* invalidation conditions
* regime alignment
* supporting evidence
* confidence semantics

---

## KB-M10A-002 — Define Structured Trade Plan Semantics

### Purpose

Define canonical structure for executable discretionary intent.

### Scope

Define:

* entry rationale
* stop rationale
* target rationale
* sizing rationale
* execution assumptions
* risk framing
* playbook alignment

---

## KB-M10A-003 — Define Scenario Branch Semantics

### Purpose

Formalize conditional reasoning pathways.

### Scope

Define:

* primary scenario
* alternative scenarios
* invalidation branches
* regime transitions
* branching replay semantics

---

## KB-M10A-004 — Define Review Reflection Semantics

### Purpose

Formalize durable post-decision learning artifacts.

### Scope

Define:

* thesis vs outcome comparison
* execution quality
* discipline analysis
* emotional reflection
* lessons learned
* behavioral observations

---

## KB-M10A-005 — Define Cognitive Replay Semantics

### Purpose

Define how cognition reconstructs during replay.

### Scope

Define:

* replay annotations
* cognition timelines
* reasoning snapshots
* thesis evolution
* replay visibility boundaries

---

# Linked Runtime Issues

---

# Structured Thesis Authoring

---

## M10AIS01 — Implement Structured Thesis Domain Model

### Purpose

Introduce canonical thesis artifact persistence.

### Scope

Implement:

* thesis entity model
* structured thesis schema
* lifecycle linkage
* persistence contracts

### Acceptance Criteria

* Thesis artifacts persist independently from lifecycle markers.
* Thesis becomes replayable cognition rather than stage metadata.

---

## M10AIS02 — Implement Thesis Authoring Workspace

### Purpose

Provide operator-facing structured thesis composition.

### Scope

Add thesis editing support for:

* narrative
* catalysts
* assumptions
* invalidation
* regime alignment
* confidence
* supporting evidence

### Acceptance Criteria

* Traders can compose durable structured thesis artifacts.
* Thesis authoring becomes operationally usable.

---

## M10AIS03 — Implement Thesis Revision History

### Purpose

Preserve thesis evolution over time.

### Scope

Introduce:

* thesis revisions
* immutable revision snapshots
* revision timestamps
* replay visibility

### Acceptance Criteria

* Replay can reconstruct thesis evolution chronologically.

---

# Scenario Modeling

---

## M10AIS04 — Implement Scenario Branch Modeling

### Purpose

Capture conditional reasoning structures.

### Scope

Support:

* primary scenario
* alternative scenario
* invalidation pathway
* regime transition branch

### Acceptance Criteria

* Trade cognition can branch conditionally.

---

## M10AIS05 — Implement Scenario Visualization Projection

### Purpose

Expose scenario structures operationally.

### Scope

Add:

* scenario summaries
* branch indicators
* replay-linked scenario projections

### Acceptance Criteria

* Operators can understand scenario relationships visually.

---

# Structured Trade Planning

---

## M10AIS06 — Implement Structured Trade Plan Domain Model

### Purpose

Persist structured execution intent.

### Scope

Implement:

* entry conditions
* stop rationale
* target rationale
* sizing rationale
* execution assumptions
* playbook alignment

### Acceptance Criteria

* Trade plans become durable cognitive artifacts.

---

## M10AIS07 — Implement Trade Plan Authoring Workspace

### Purpose

Provide operational trade planning surface.

### Scope

Support:

* structured plan composition
* risk framing
* execution reasoning
* discretionary notes
* scenario linkage

### Acceptance Criteria

* Plans become operationally authorable.

---

## M10AIS08 — Implement Plan Validation Preview Layer

### Purpose

Surface lifecycle and rule implications before approval.

### Scope

Show:

* lifecycle readiness
* missing cognition fields
* rule previews
* risk consistency indicators

### Acceptance Criteria

* Operators receive cognition-aware planning guidance.

---

# Replay Enrichment

---

## M10AIS09 — Implement Replay Cognitive Artifact Timeline

### Purpose

Integrate cognition artifacts into replay.

### Scope

Replay displays:

* thesis snapshots
* plan revisions
* scenario evolution
* review annotations

### Acceptance Criteria

* Replay reconstructs reasoning, not merely events.

---

## M10AIS10 — Implement Cognitive Snapshot Reconstruction

### Purpose

Reconstruct operator cognition at historical timestamps.

### Scope

Support:

* point-in-time thesis state
* scenario visibility
* assumption state
* contextual evidence snapshots

### Acceptance Criteria

* Historical reasoning becomes reconstructable.

---

# Review Enrichment

---

## M10AIS11 — Implement Structured Review Reflection Model

### Purpose

Persist semantically meaningful review artifacts.

### Scope

Support:

* thesis vs outcome
* discipline quality
* execution quality
* emotional reflection
* lessons learned

### Acceptance Criteria

* Reviews become durable learning artifacts.

---

## M10AIS12 — Implement Review Reflection Workspace

### Purpose

Provide replay-aware review composition environment.

### Scope

Support:

* structured reflection entry
* replay-linked observations
* behavioral commentary
* lesson capture

### Acceptance Criteria

* Review becomes operationally meaningful.

---

# Replay Annotation Infrastructure

---

## M10AIS13 — Implement Replay Annotation System

### Purpose

Allow replay-attached operator annotations.

### Scope

Support:

* replay notes
* timeline annotations
* contextual observations
* postmortem tagging

### Acceptance Criteria

* Replay becomes cognitively interactive.

---

# Playbook Alignment

---

## M10AIS14 — Implement Playbook Alignment Projection Layer

### Purpose

Associate trades with discretionary operational playbooks.

### Scope

Support:

* playbook tagging
* alignment summaries
* replay filtering
* behavioral grouping

### Acceptance Criteria

* Decisions become operationally classifiable.

---

# Workspace Cohesion

---

## M10AIS15 — Implement Cross-Workspace Cognitive Continuity

### Purpose

Preserve authored cognition across workspace transitions.

### Scope

Ensure:

* thesis visibility
* plan continuity
* scenario continuity
* review continuity

### Acceptance Criteria

* Cognition persists naturally across operational movement.

---

# Acceptance Meaning

* Replay reconstructs operator reasoning rather than only workflow state.
* Thesis and plan become durable cognitive artifacts.
* Structured cognition becomes canonical operational truth.
* Review becomes semantically meaningful.
* AI advisory systems gain rich historical cognition context.
* Behavioral intelligence gains replayable reasoning input.
* Simulation infrastructure gains structured semantic inputs.
* TradeForge evolves from workflow replay toward true discretionary cognition reconstruction.

---

## M10B — Postgres Persistence And Multi-Decision Operational Surface

**Status:** Done

## Semantic Intent

Wire durable event persistence and introduce a multi-decision navigation surface so
operators can work across multiple securities, log out, and return to prior decisions
without data loss. This unblocks meaningful real-world operational testing and is a
prerequisite for the Operating Workspace becoming a genuine decision management surface.

## Architectural Significance

TradeForge's event-sourced architecture was designed for durability from the start.
`PostgresEventStore` is already implemented (TF-0024 through TF-0026). The missing piece
is wiring it as the default runtime persistence layer and surfacing all persisted decisions
through the Operating Workspace.

Without persistence:
- Every server restart wipes all decisions
- Testing is limited to single-session demos
- The Operating Workspace attention queue is ephemeral
- Multiple concurrent decisions (SMH at Armed + NVDA at Thesis) cannot survive a restart

With persistence:
- Decisions survive server restarts, deployments, and logout/login cycles
- The Operating Workspace becomes a true decision management surface
- Multi-security workflows are fully supported
- The full lifecycle — from Idea through Review — is durable and replayable

## Canonical Concepts

- [[Replayability Is Foundational]]
- [[Event Ledger Canonical Truth]]
- [[Events Are Immutable]]
- [[Workflow-Centric Architecture]]

## Linked Runtime Issues

- TF-F008: Wire PostgresEventStore as default runtime persistence via TRADEFORGE_DATABASE_URL (**Done**)
- TF-F009: Implement all-decisions projection and multi-decision navigation in Operating Workspace (**Done**)
- TF-F010: Fix thesis narrative minimum-length validation gap in ThesisDevelopmentModal (**Done**)

## Acceptance Meaning

- Server restart does not lose any decision data.
- Operator can work on SMH, NVDA, and any other stock simultaneously and return to each.
- Operating Workspace lists all active decisions by ticker, stage, and date.
- Operator can navigate directly from the decision list to any workspace for any decision.
- InMemory store remains available for test environments and demo mode.
- Frontend thesis authoring validation prevents avoidable backend 422 responses during operational use.

---

## M10C — Operational Credential Boundary

**Status:** Planned

## Semantic Intent

Establish a secure, auditable credential management layer for all external provider
integrations before AI advisory work (M11) introduces LLM provider keys.

## Architectural Significance

As TradeForge connects to an expanding set of external data providers — Polygon, Alpaca,
Alpha Vantage, FinancialModelingPrep, Finqual, and LLM providers — the current pattern
of raw constructor-parameter key injection becomes unmanageable and architecturally
incorrect. Provider credentials are operational capabilities with lifecycle (creation,
rotation, revocation, expiry), not configuration trivia.

This milestone introduces `src/security/` as a top-level architectural boundary,
governing how all external provider secrets are stored, decrypted, and delivered to
adapters. The composition root (`create_app()`) is the sole caller of the credential
store. No provider adapter imports from `src/security/`.

The `Credential` domain model is also designed with replay safety in mind: credential
status at historical points (expired, revoked, entitlement change) is operationally
meaningful context for future replay reconstruction.

M10B is prerequisite to M11 — AI advisory work will introduce LLM provider credentials
that must be managed through the same boundary from day one.

## Canonical Concepts

- [[Operational Credential Boundary]]
- [[Replayability Is Foundational]]
- [[Layer Separation]]
- [[Architectural Simplicity]]

## Provider Coverage

| Provider | Credential Shape | Purpose |
|---|---|---|
| yFinance | none | Free market data, default provider |
| Polygon.io | `api_key` | Real-time and historical data |
| Alpaca | `api_key` + `secret_key` | Market data + future execution |
| Alpha Vantage | `api_key` | Fundamental + technical data |
| FinancialModelingPrep | `api_key` | Financial statements + ratios |
| Finqual | `api_key` | Quantitative financial data |
| LLM providers (M11+) | `api_key` | Advisory AI boundary |

## Linked Runtime Issues

- TF-F004: Define operational credential boundary — ADR and Credential domain model (**Done**)
- TF-F005: Implement KeyManager and encrypted local credential store (**Done**)
- TF-F006: Wire all provider adapters through CredentialStore at composition root (**Done**)
- TF-F007: Credential setup guide, rotation documentation, keys-out-of-Git enforcement

## Acceptance Meaning

- `TRADEFORGE_MASTER_KEY` is the sole entry point for all provider secret access.
- M11 (AI Advisory) can assume a proper credential boundary exists.
- No provider API key appears in logs, Git history, or `.env` files.
- Rotating a credential requires one command and no code change.
- All current and planned provider adapters are registered through `CredentialStore`.
- M11 (AI Advisory) can assume a proper credential boundary exists.
- Replay-aware credential status fields are present in the domain model for future use.

---

## M11 — AI Advisory Boundary
Status: Planned
## Semantic Intent
Introduce AI assistance without compromising human sovereignty.
## Architectural Significance
AI remains advisory rather than authoritative.
## Canonical Concepts

* [[AI Advisory Boundary]]
* [[Human Decision Sovereignty]]

## Linked Runtime Issues

* TF-0065: Define AI advisory interfaces
* TF-0066: Implement replay summarization assistance
* TF-0067: Implement review assistance
* TF-0068: Implement advisory provenance tracking

## Acceptance Meaning

* AI cannot mutate canonical state directly.
* AI cannot approve lifecycle transitions.
* AI outputs remain reviewable artifacts.

---

## M12 — Behavioral Intelligence And Adaptive Review
Status: Planned
## Semantic Intent
Detect recurring behavioral and discipline patterns.
## Architectural Significance
TradeForge evolves from replay infrastructure into adaptive operational cognition.
## Canonical Concepts

* [[Behavioral Signal]]
* [[Discipline Pattern]]
* [[Adaptive Review]]

## Linked Runtime Issues

* TF-0069: Detect recurring behavioral patterns
* TF-0070: Implement discipline signal engine
* TF-0071: Implement review clustering
* TF-0071: Implement historical behavior overlays

## Acceptance Meaning

* Behavioral learning becomes operational.
* Pattern recognition augments review quality.


---

## M13 — Simulation And Scenario Engine
Status: Planned
## Semantic Intent
Enable simulated operational cognition environments.
## Architectural Significance
Simulation supports hypothetical replay, regime experimentation, and strategy stress testing.
## Canonical Concepts

* [[Simulation]]
* [[Scenario Replay]]
* [[Hypothetical Lifecycle]]

## Linked Runtime Issues

* TF-0073: Implement simulation event environment
* TF-0074: Implement hypothetical replay branching
* TF-0075: Implement regime simulation engine
* TF-0076: Implement simulated workspace playback

## Acceptance Meaning

* Historical and hypothetical replay become composable.
* Cognitive experimentation becomes possible.


---

## M14 — Adaptive AI And RL Infrastructure
Status: Planned
## Semantic Intent
Introduce adaptive behavioral and reinforcement-learning infrastructure.
## Architectural Significance
Adaptive systems remain subordinate to replayable human cognition.
## Canonical Concepts

* [[Adaptive Cognition]]
* [[RL Advisory System]]
* [[Behavioral Adaptation]]

## Linked Runtime Issues

* TF-0077: Define RL experimentation boundaries
* TF-0078: Implement adaptive scenario evaluation
* TF-0079: Implement reinforcement-learning research environment
* TF-0080: Implement adaptive playbook experimentation

## Acceptance Meaning

* RL remains advisory and experimental.
* Human sovereignty remains preserved.
* Adaptive infrastructure depends on replayable historical truth.


---


