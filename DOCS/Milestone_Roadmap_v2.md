
---
title: Milestone Roadmap v2
type: index
status: canonical
tags: [TradeForge, roadmap, milestones, architecture, cognition, workspaces]
created: 2026-05-09
updated: 2026-05-26
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

**Status:** Done

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
- TF-F007: Credential setup guide, rotation documentation, keys-out-of-Git enforcement (**Done**)

## Acceptance Meaning

- `TRADEFORGE_MASTER_KEY` is the sole entry point for all provider secret access.
- M11 (AI Advisory) can assume a proper credential boundary exists.
- No provider API key appears in logs, Git history, or `.env` files.
- Rotating a credential requires one command and no code change.
- All current and planned provider adapters are registered through `CredentialStore`.
- M11 (AI Advisory) can assume a proper credential boundary exists.
- Replay-aware credential status fields are present in the domain model for future use.

---

## M10D — Provider Capability Architecture And External Data Readiness

**Status:** Done

## Semantic Intent

Prepare a capability-aware external data layer before AI advisory work begins.

## Architectural Significance

M10C centralized provider credentials, but provider meaning remains flattened into the M9 market-snapshot path. The current runtime can answer which provider supplies normalized OHLCV context, but it does not yet model that one provider identity may support multiple distinct capabilities while another may support only one.

That gap matters before `M11`: provider credentials already cover providers with materially different data surfaces, and future AI advisory work must not infer provider semantics from an OHLCV-only abstraction.

`M10D` extends the provider model without replacing `ADR-0032`. `ADR-0032` remains the accepted boundary for normalized market snapshots. `M10D` adds a capability-aware architecture above that boundary so provider identity is no longer treated as synonymous with price capability.

## Canonical Concepts

- [[Market Intelligence Is Interpreted Context]]
- [[Derived State Must Remain Distinguishable]]
- [[Provider Boundary]]
- [[Provider Provenance]]
- [[Architectural Simplicity]]
- [[Replayability Is Foundational]]

## Scope

`M10D` introduces:

- price capability support
- fundamentals capability support
- a provider registry
- global preferred provider plus ordered fallback sequence per capability
- visible provider provenance and configuration
- typed external data contracts behind the registry

## Explicit Exclusions

`M10D` explicitly excludes:

- news, macro, estimates, and transcripts
- AI consumption of provider data
- autonomous routing beyond defined defaults or fallbacks
- broad external-data generalization beyond the first two capability families
- provider health/status management beyond visible degraded-capability state

## Initial Doctrine Decisions

- Fundamentals rollout begins with `fmp` as the primary provider and `alpha_vantage` as the fallback provider.
- Initial provider selection optimizes for architectural capability validation rather than long-term provider finality.
- Capability resolution is deterministic preferred-plus-ordered-fallback selection.
- Resolution choice, fallback use, missing capabilities, and degraded states must remain operator-visible and replay-preservable as advisory context.
- Operator-facing provider configuration is editable and visible in `M10D`; richer provider health/status management is deferred.
- Initial fundamentals overlays belong in Opportunity and Thesis flows, not Plan flows.

## Linked Runtime Issues

- TF-F016: Capture provider capability gap and define M10D architecture (**Done**)
- TF-F017: Introduce provider registry and capability metadata model (**Done**)
- TF-F018: Split external data access into typed capability contracts (**Done**)
- TF-F019: Add fundamentals data model and normalization boundary (**Done**)
- TF-F020: Implement initial fundamentals provider adapters (**Done**)
- TF-F021: Expose capability-aware provider configuration and transparency (**Done**)
- TF-F022: Extend workspace context with fundamentals overlays (**Done**)
- TF-F023: M10D verification and M11 readiness gate (**Done**)

## Acceptance Meaning

- Provider capability is explicit rather than inferred from provider identity.
- Price and fundamentals are represented by different typed contracts.
- Configured providers can be inspected and selected per capability.
- Provider resolution, fallback usage, and missing capabilities are visible to the operator.
- Workspaces show provenance for consumed external data.
- Fundamentals remain contextual external data, not canonical lifecycle truth.
- `M11` can depend on a stable provider layer that is not price-blind.

---

## M10E — Context Workbench And Advisory Context Acquisition

**Status:** Done

## Semantic Intent

Turn the capability-aware external-data foundation into a coherent
operator-facing research environment before AI advisory work begins.

## Architectural Significance

`M10D` established that provider identity and provider capability are different
concepts. It also introduced initial `price` and `fundamentals` contracts, but
the runtime still leaves operators with a fragmented experience: one visible
price load path, partial fundamentals surfaces, provider configuration without a
full acquisition workflow, and no dedicated workspace for gathering and
interpreting research context.

`M10E` closes that gap by defining the research/acquisition layer that sits
between normalized advisory provider outputs and later opportunity/thesis
workflows. It formalizes how the operator requests context, how the system
explains missing or failed context, how provider attempts remain transparent,
and whether a dedicated `Context Workbench` becomes a canonical workspace.

This milestone is intentionally placed before `M11`. AI advisory should enhance
an already explicit context-acquisition and interpretation model rather than
becoming the first place where that model is invented.

## Canonical Concepts

- [[UX Is Architectural]]
- [[Workspaces Are Operational Environments]]
- [[Workflow-Centric Architecture]]
- [[Derived State Must Remain Distinguishable]]
- [[Market Intelligence Is Interpreted Context]]
- [[Terminology Stability]]

## Scope

`M10E` introduces or resolves:

- trader-language boundary for operator-facing UX
- recovery-oriented missing-information doctrine
- context interpretation layer design
- dedicated Context Workbench workspace concept
- explicit advisory context acquisition workflow
- provider attempt / fallback transparency
- distinction between equity fundamentals and ETF-relevant context
- interpretation-first presentation of acquired market context
- bridge from acquired advisory context into later opportunity/thesis synthesis

## Explicit Exclusions

`M10E` explicitly excludes:

- AI-generated advisory recommendations
- autonomous lifecycle changes from acquired context
- full news / macro / estimates / transcripts implementation
- generic support for every future security type
- replacing the existing normalized provider boundary

## Recommended Issue Order

### Foundation

1. `TF-F040` - Define trader-language boundary between canonical ontology and UX copy.
2. `TF-F039` - Require recovery-oriented missing-information states across UX.
3. `TF-F037` - Introduce context interpretation layer between provider payloads and operator cognition.

### Main Requirement Path

4. `TF-F038` - Define dedicated Context Workbench workspace concept.
5. `TF-F032` - Add explicit advisory context acquisition workflow.
6. `TF-F033` - Surface advisory provider attempt status and fallback outcomes.
7. `TF-F034` - Distinguish equity fundamentals from ETF context.

### Downstream Productization

8. `TF-F041` - Connect acquired advisory context to opportunity synthesis and thesis implications.
9. `TF-F042` - Reframe market-context presentation from raw payload first to interpretation first.
10. Opportunity Workspace refinement follow-ons:
    - `TF-F028`
    - `TF-F029`
    - `TF-F030`
    - `TF-F031`
    - `TF-F035`
    - `TF-F036`

## Linked Runtime Issues

- TF-F040: Define trader-language boundary between canonical ontology and UX copy
- TF-F039: Require recovery-oriented missing-information states across UX
- TF-F037: Introduce context interpretation layer between provider payloads and operator cognition
- TF-F038: Define dedicated Context Workbench workspace concept
- TF-F032: Add explicit advisory context acquisition workflow
- TF-F033: Surface advisory provider attempt status and fallback outcomes (**Done**)
- TF-F034: Distinguish equity fundamentals from ETF context (**Done**)
- TF-F041: Connect acquired advisory context to opportunity synthesis and thesis implications (**Done**)
- TF-F042: Reframe market-context presentation from raw payload first to interpretation first (**Done**)
- TF-F028: Add persistent instrument identity to decision workspaces (**Done**)
- TF-F029: Replace misleading candidate terminology in operator-facing UX (**Done**)
- TF-F030: Replace provenance-first Opportunity panels with cognition-first synthesis surfaces (**Done**)
- TF-F031: Interpret unavailable-context states with operator meaning and next actions (**Done**)
- TF-F035: Translate scenario-branch UX into trader-facing conditional reasoning (**Done**)
- TF-F036: Add discretionary-thinking guidance to early opportunity evaluation (**Done**)

## Acceptance Meaning

- TradeForge has an explicit operator-facing model for acquiring advisory context beyond OHLCV alone.
- The system distinguishes provider configuration from actual information acquisition.
- Missing and failed context states explain what happened, why it matters, and what the operator can do next.
- A dedicated research/context workspace boundary is either accepted and defined or explicitly rejected with rationale.
- Advisory context can be interpreted and later consumed by opportunity/thesis workflows without becoming canonical truth.
- `M11` can build AI advisory on top of a coherent context-acquisition layer instead of compensating for missing UX and workspace architecture.

---

## M11 — AI Advisory Boundary
Status: Done
## Semantic Intent
Introduce AI assistance without compromising human sovereignty.
## Architectural Significance
AI remains advisory rather than authoritative.
## Canonical Concepts

* [[AI Advisory Boundary]]
* [[Human Decision Sovereignty]]

## Linked Runtime Issues

* TF-0065: Define AI advisory interfaces (**Done**)
* TF-0066: Implement replay summarization assistance (**Done**)
* TF-0067: Implement review assistance (**Done**)
* TF-0068: Implement advisory provenance tracking (**Done**)

## Dependency Notes

* `M10E` must complete first so AI advisory work can consume explicit provider capabilities through a coherent context-acquisition and interpretation model rather than infer semantics from the older OHLCV-only path.

## Acceptance Meaning

* AI cannot mutate canonical state directly.
* AI cannot approve lifecycle transitions.
* AI outputs remain reviewable artifacts.

---

## Roadmap Evolution Note

M11 established the foundational AI advisory boundary. Later roadmap evolution expands beyond basic AI assistance into machine-assisted discretionary cognition, beginning with M12.

The active roadmap remains this file. `DOCS/Milestone_Roadmap_v3.md` is retained as the historical proposal/source artifact for the M12-M19 cognitive advisory evolution integrated here under TF-F044.

---

# Future Direction - Machine-Assisted Discretionary Cognition

TradeForge is no longer primarily evolving toward signal generation, autonomous trading, RL portfolio optimization, predictive automation, or algorithmic execution.

TradeForge is instead evolving toward:

```text
a replayable discretionary cognition operating system
```

The machine assists with broad market attention, candidate discovery, contextual enrichment, evidence accumulation, anomaly detection, historical comparison, memory persistence, advisory interpretation, and behavioral pattern surfacing.

The human remains responsible for judgment, ambiguity handling, discretionary interpretation, risk acceptance, plan approval, execution decisions, and accountability.

Core question:

```text
What deserves my attention?
What evidence exists?
What risks am I ignoring?
How am I reasoning?
Is my process improving?
```

TradeForge does not attempt to answer:

```text
What should I buy?
```

---

## M12 - Advisory Observation And Cognitive Evidence Layer

**Status:** Done

## Semantic Intent

Introduce machine-assisted evidence accumulation while preserving explicit separation between advisory observations and operator-owned lifecycle state.

## Architectural Significance

M12 introduces the first true advisory cognition layer. Machine-originated observations become durable advisory artifacts, but they do not create lifecycle authority, execution authority, or operator commitment.

## Core Principle

TradeForge must distinguish between advisory space:

```text
Observation
Signal
Context
Interpretation
Candidate
```

and commitment space:

```text
Trade Idea
Thesis
Plan
Approval
Execution
```

## Canonical Concepts

* [[Advisory Observation]]
* [[Cognitive Evidence]]
* [[Evidence Accumulation]]
* [[Interpretation Artifact]]
* [[Advisory Candidate]]
* [[Contextual Observation]]
* [[Uncertainty Preservation]]
* [[Attention Allocation]]
* [[Human Decision Sovereignty]]

## Scope

M12 introduces advisory observation models, external research ingestion, evidence attachment, contextual interpretation artifacts, observation provenance, uncertainty metadata, candidate surfacing, advisory context persistence, thesis evidence linkage, and replay-visible advisory cognition.

## Explicit Exclusions

M12 excludes autonomous trade approval, autonomous trade execution, broker integration, AI-generated lifecycle transitions, hidden scoring engines, black-box trade recommendations, AI authority escalation, and autonomous capital allocation.

## Linked Runtime Issues

* TF-A001 (Done): Define AdvisoryObservation domain model
* TF-A002 (Done): Implement advisory observation event taxonomy
* TF-A003 (Done): Implement observation provenance persistence
* TF-A004 (Done): Implement uncertainty metadata support
* TF-A005 (Done): Implement replay-visible advisory observation timeline
* TF-A006 (Done): Implement evidence attachment framework
* TF-A007 (Done): Implement thesis evidence linkage
* TF-A008 (Done): Implement contextual interpretation artifacts
* TF-A009 (Done): Implement conflicting evidence surfacing
* TF-A010 (Done): Implement evidence aging/staleness visibility
* TF-A011 (Done): Implement advisory candidate ingestion pipeline
* TF-A012 (Done): Implement candidate review queue
* TF-A013 (Done): Implement operator candidate promotion workflow
* TF-A014 (Done): Prevent automated lifecycle promotion into TradeIdea
* TF-A015 (Done): Implement candidate provenance visualization
* TF-A016 (Done): Define external research cockpit import boundary
* TF-A017 (Done): Implement research artifact ingestion API
* TF-A018 (Done): Implement Codex/Claude-generated advisory artifact support
* TF-A019 (Done): Implement advisory markdown artifact persistence
* TF-A020 (Done): Implement replay-safe advisory snapshot capture

## Acceptance Meaning

* Machine-originated observations become first-class advisory artifacts.
* Human lifecycle authority remains preserved.
* Evidence becomes replayable and inspectable.
* Advisory cognition becomes operationally usable without becoming authoritative.

---

## M13 - Contextual Interpretation And Thesis Influence

**Status:** Done

## Semantic Intent

Transform raw advisory observations into contextual discretionary meaning.

## Architectural Significance

Raw data does not improve decisions unless interpreted within context. M13 models discretionary interpretation rather than simplistic indicator signaling.

## Core Principle

TradeForge should model:

```text
Observation
-> Interpretation
-> Contextual Weighting
-> Thesis Influence
```

not:

```text
Indicator -> Buy/Sell
```

## Canonical Concepts

* [[Interpretation Layer]]
* [[Contextual Weighting]]
* [[Thesis Influence]]
* [[Regime Sensitivity]]
* [[Probabilistic Cognition]]
* [[Conflicting Evidence]]
* [[Interpretive Uncertainty]]

## Scope

M13 introduces interpretation artifacts, contextual weighting, regime-aware weighting, thesis influence modeling, evidence conflict analysis, advisory confidence ranges, interpretation replay persistence, and probabilistic cognition overlays.

## Explicit Exclusions

M13 excludes deterministic predictive scoring, autonomous trade recommendations, opaque AI ranking systems, execution automation, and hidden optimization engines.

## LLM Adapter Prerequisites (must complete before TF-B014)

* TF-F045: Add LiteLLM credential shape to CredentialStore (**Done**)
* TF-F046: Implement OpenAICompatibleAdvisoryProvider (**Done**)
* TF-F047: Implement prompt template and service wiring for replay summary (**Done**)
* TF-F048: Implement prompt template and service wiring for thesis review assistant (**Done**)
* TF-F049: Implement prompt template and service wiring for advisory observation generation (**Done**)
* TF-F050: Implement prompt template and service wiring for candidate screening (**Done**)
* TF-F051: Add on-demand advisory API endpoints and frontend trigger surfaces (**Done**)
* TF-F052: Add advisory service health check to ProviderConfigurationPanel (**Done**)
* TF-F053: Validate NVIDIA NIM via LiteLLM and document credential shape (**Done**)
* TF-F054: Document automatic enrichment lifecycle hook points (**Done**)
* TF-F055: Implement UI-based credential management (**Done**)
* TF-F056: Fix missing default advisory provider bootstrap after merge (**Done**)

## Interpretation Domain And Infrastructure

* TF-B001: Define interpretation artifact schema (**Done**)
* TF-B002: Implement contextual weighting framework (**Done**)
* TF-B003: Implement regime-aware weighting model (**Done**)
* TF-B004: Implement conflicting evidence analysis (**Done**)
* TF-B005: Implement confidence-range representation (**Done**)
* TF-B006: Implement thesis evidence influence tracking (**Done**)
* TF-B007: Implement supporting vs weakening evidence classification (**Done**)
* TF-B008: Implement thesis drift detection (**Done**)
* TF-B009: Implement contextual contradiction surfacing (**Done**)

## Replay And UX Surfaces

* TF-B010: Implement evidence impact replay overlays (**Done**)
* TF-B011: Implement interpretation-first operational surfaces (**Done**)
* TF-B012: Implement uncertainty-preserving UX patterns (**Done**)
* TF-B013: Implement probabilistic cognition summaries (**Done**)
* TF-B014: Implement evidence narrative generation (**Done**)
* TF-B015: Implement contextual reasoning timelines (**Done**)

## Acceptance Meaning

* Evidence gains contextual meaning rather than simplistic polarity.
* Interpretations become replayable cognitive artifacts.
* Operators gain structured probabilistic context rather than signals.

---

## M13A - Provider Governance And AI Gateway Configuration

**Status:** Done

## Semantic Intent

Formalize external systems governance and AI routing infrastructure before
behavioral intelligence and broader advisory expansion increase provider,
credential, gateway, and diagnostic complexity.

M13A stabilizes the operational control plane around external providers. It
does not introduce a new decision workspace, lifecycle authority, autonomous
execution path, or AI decision authority.

## Architectural Significance

M10C established the credential boundary. M10D established capability-aware
provider architecture. M10E established contextual acquisition workflows. M11,
M12, and M13 introduced AI advisory, advisory observations, and contextual
interpretation.

Together, those milestones created a larger operational gap: credential entry,
provider selection, capability routing, LiteLLM routing, health checks,
diagnostics, fallback state, and contextual provenance are too important to
remain collapsed into contextual workflow rails.

The core M13A distinction is:

```text
Credential != Provider != Capability != Model
```

LiteLLM must be treated as an AI gateway and routing boundary, not as a normal
one-key provider. TradeForge should request semantic advisory roles and
capabilities while gateway configuration maps those roles to concrete model
providers outside workflow logic.

## Canonical Concepts

* [[Provider Boundary]]
* [[Provider Provenance]]
* [[AI Advisory Boundary]]
* [[Derived State Must Remain Distinguishable]]
* [[Human Decision Sovereignty]]
* [[Replayability Is Foundational]]
* [[UX Is Architectural]]

## Scope

M13A introduces or resolves:

* provider governance control surface design
* credential lifecycle visibility beyond basic save/revoke
* provider health, validation, diagnostics, and degraded-state visibility
* capability-first routing governance for price, fundamentals, AI advisory, and future broker/paper trading
* LiteLLM as an AI gateway rather than an ordinary data provider
* AI route aliases such as fast summary, reasoning, long-context analysis, cheap classification, and local/offline routes
* contextual rail simplification so rails show provider status, provenance, freshness, fallback state, and configure links rather than long-form administration
* replay and provenance questions for provider route, health, fallback, and gateway state

## Explicit Exclusions

M13A explicitly excludes:

* autonomous trading
* AI decision authority
* AI plan approval
* automated broker execution
* broker automation expansion beyond governance modeling
* a generalized AI orchestration engine
* treating provider health, model output, or gateway state as canonical event-ledger truth
* replacing the existing M9 market snapshot boundary or M10D provider capability registry

## Recommended Issue Order

1. `TF-F059` - Formalize M13A provider governance roadmap (**Done**)
2. `TF-F060` - Define provider governance control surface design (**Done**)
3. `TF-F061` - Define capability routing governance model (**Done**)
4. `TF-F062` - Define AI gateway and route alias model (**Done**)
5. `TF-F063` - Define provider diagnostics and health history model (**Done**)
6. `TF-F064` - Implement provider governance read APIs (**Done**)
7. `TF-F065` - Implement credential validation and test workflow (**Done**)
8. `TF-F066` - Implement AI gateway route visibility (**Done**)
9. `TF-F067` - Implement provider governance frontend surface and rail cleanup (**Done**)
10. `TF-F068` - M13A verification and M14 readiness gate (**Done**)
11. `TF-F071` - Fix advisory thesis review event store loading (**Done, corrective feedback issue**)

## Linked Runtime Issues

* TF-F059: Formalize M13A provider governance roadmap (**Done**)
* TF-F060: Define provider governance control surface design (**Done**)
* TF-F061: Define capability routing governance model (**Done**)
* TF-F062: Define AI gateway and route alias model (**Done**)
* TF-F063: Define provider diagnostics and health history model (**Done**)
* TF-F064: Implement provider governance read APIs (**Done**)
* TF-F065: Implement credential validation and test workflow (**Done**)
* TF-F066: Implement AI gateway route visibility (**Done**)
* TF-F067: Implement provider governance frontend surface and rail cleanup (**Done**)
* TF-F068: M13A verification and M14 readiness gate (**Done**)
* TF-F071: Fix advisory thesis review event store loading (**Done, corrective feedback issue**)

## Acceptance Meaning

* Provider governance is modeled as an external systems control plane, not as a contextual rail form.
* Credential status, provider health, capability routing, gateway routing, fallback behavior, and diagnostics are distinguishable operational concerns.
* Contextual rails remain cognition-preserving surfaces focused on status, provenance, freshness, fallback, and advisory boundaries.
* LiteLLM routing is represented through gateway and route-alias concepts rather than hardcoded raw model names in workflow logic.
* External provider and AI gateway state remain advisory, non-canonical, and subordinate to human decision sovereignty.

---

## M13B - AI Gateway Governance And Managed Advisory Runtime

**Status:** Done

## Semantic Intent

Establish TradeForge as the governed operator-facing owner of the managed AI
advisory runtime.

M13B turns the M13A AI gateway foundation into a managed operational boundary:
operators choose advisory routes through TradeForge, TradeForge mediates access
to LiteLLM, and downstream LLM provider secrets are governed through the
TradeForge credential boundary.

## Architectural Significance

M13A proved LiteLLM advisory invocation, provider governance visibility, smoke
testing, route stabilization, and diagnostics. It also left an intentional
boundary: TradeForge stored the LiteLLM gateway credential, while downstream
LLM provider keys lived in LiteLLM configuration or operator environment.

M13B changes that boundary for the managed advisory runtime. TradeForge becomes
the governed owner of downstream LLM provider secrets and the sole
operator-facing advisory gateway.

The core M13B distinction is:

```text
Operator
  -> TradeForge Provider Governance
  -> encrypted LLM provider credential governance
  -> global advisory model selection
  -> TradeForge advisory boundary
  -> internal LiteLLM runtime
  -> vendor model providers
```

## Canonical Concepts

* [[AI Advisory Boundary]]
* [[Human Decision Sovereignty]]
* [[Provider Boundary]]
* [[Provider Provenance]]
* [[Derived State Must Remain Distinguishable]]
* [[Replayability Is Foundational]]
* [[Operational Credential Boundary]]

## Scope

M13B introduces or resolves:

* global advisory model and route selection
* LiteLLM model discovery through TradeForge
* operator-selected primary advisory model or route
* optional fallback advisory model or route
* removal of hardcoded advisory model names from workflow logic
* advisory-wide use of the selected configuration
* non-canonical smoke testing for the selected route
* internal-only LiteLLM runtime exposure by default
* TradeForge-mediated advisory access to LiteLLM
* local debugging workflow for internal LiteLLM access
* governed downstream LLM provider secret management
* encrypted Groq, NVIDIA NIM, OpenAI, Anthropic, Google-style provider keys
* runtime decryption only inside the trusted backend advisory boundary
* stateless request-time provider credential composition for LiteLLM calls
* explicit rotation and reload semantics
* non-invasive LiteLLM readiness checks that do not probe model providers

## Explicit Exclusions

M13B explicitly excludes:

* autonomous trading
* AI decision authority
* AI plan approval
* lifecycle transitions from AI output
* direct vendor SDK bypass from advisory workflow code
* generalized AI orchestration
* multi-agent runtime governance
* automatic hidden model selection
* dynamic per-task routing policies
* dynamic LiteLLM YAML editing unless separately scoped
* Kubernetes secrets or external vault integration
* broker execution expansion

## Linked Runtime Issues

* TF-F072: Global Advisory Model Selection (**Done**)
* TF-F073: Internalize LiteLLM Gateway Network Boundary (**Done**)
* TF-F074: Governed LLM Provider Secret Management (**Done**)
* TF-F075: Implement Stateless LiteLLM Request-Time Credential Composition (**Done**)
* TF-F076: Replace LiteLLM route-probing healthcheck with non-invasive readiness check (**Done**)

## Acceptance Meaning

* TradeForge is the operator-facing advisory gateway.
* LiteLLM is treated as managed internal infrastructure by default.
* Advisory workflow code does not depend on hardcoded raw model names.
* Downstream LLM vendor keys are governed by TradeForge credential storage.
* Provider secrets are masked in UI/API responses and decrypted only inside the
  trusted backend advisory request path.
* LiteLLM remains stateless for managed local advisory runtime operation:
  TradeForge resolves explicit provider/model selection and supplies the
  required provider credential per request.
* LiteLLM readiness checks do not perform provider/model route probing.
* AI gateway routing and provider-secret state remain operational,
  non-canonical, and subordinate to human decision sovereignty.

---

## M14 - Behavioral Intelligence And Cognitive Auditability

**Status:** Done

## Semantic Intent

Expose recurring behavioral patterns, discipline failures, and cognitive drift.

## Architectural Significance

M14 introduces cognitive auditability as a first-class capability so review can evaluate decision process quality rather than outcome alone.

## Canonical Concepts

* [[Behavioral Pattern]]
* [[Discipline Drift]]
* [[Cognitive Auditability]]
* [[Process Degradation]]
* [[Decision Quality]]
* [[Emotional Context]]
* [[Behavioral Replay]]

## Scope

M14 introduces recurring behavioral pattern detection, process violation tracking, discipline analysis, emotional reflection overlays, thesis deterioration analysis, risk management behavior analysis, recurring mistake identification, and cognitive consistency analysis.

## Linked Runtime Issues

* TF-C001: Detect recurring sizing violations (**Done**)
* TF-C002: Detect impulsive execution patterns (**Done**)
* TF-C003: Implement process deviation overlays (**Done**)
* TF-C004: Implement behavioral clustering (**Done**)
* TF-C005: Implement recurring mistake analysis (**Done**)
* TF-C006: Implement discipline deterioration signals (**Done**)
* TF-C007: Implement thesis attachment analysis (**Done**)
* TF-C008: Implement emotional reflection overlays (**Done**)
* TF-C009: Implement operator behavior timelines (**Done**)
* TF-C010: Implement decision-quality review metrics (**Done**)

## Acceptance Meaning

* Behavioral drift becomes visible and replayable.
* Review evolves beyond outcome analysis alone.

---

## M14C - Thesis Import Workflow And Advisory Dropoff

**Status:** Done

## Semantic Intent

Bridge durable advisory cognition into operator-owned Thesis authoring without
allowing advisory material to become lifecycle authority.

## Architectural Significance

M14C turns the M12 advisory artifact substrate into a practical operator
workflow. It adds explicit import dropoff and preview paths for thesis and
plan-adjacent advisory artifacts while preserving the Decision Lifecycle Engine
as the only owner of canonical lifecycle progression.

## Canonical Concepts

* [[Advisory Artifact]]
* [[Persona Workspace]]
* [[Decision Lifecycle Engine]]
* [[Event Ledger]]
* [[Replay System]]

## Scope

M14C introduces deterministic local markdown thesis-draft import, advisory
artifact preview inside lifecycle authoring modals, selective operator field
acceptance, field-level provenance preservation, plan import mediation, and
replay-visible advisory source context.

M14C does not introduce filesystem watchers, autonomous parsing, AI-generated
lifecycle mutation, automatic thesis or plan creation, automatic price
population, sizing, approval, broker integration, or execution.

## Linked Runtime Issues

* TF-R001: Thesis Workspace advisory import preview and local markdown dropoff
  (**Done**)
* TF-R002: Plan Workspace advisory import mediation
  (**Done**)

## Acceptance Meaning

* Operators can drop a structured markdown thesis draft into `imports/incoming`
  and explicitly scan it into advisory artifact storage.
* Thesis import previews remain advisory and non-canonical until the operator
  manually submits the Thesis workflow.
* Plan import previews may assist entry, stop, target, and risk-note rationale
  only through explicit operator acceptance and manual Create Plan submission.
* Plan imports do not populate prices, calculate sizing, approve plans, create
  broker orders, or authorize execution.
* Replay can show imported advisory source context without confusing it with
  canonical lifecycle truth.
* Cross-repository validation against the Research Cockpit M5 review-ready
  advisory submission completed under RC-039 and TF-F081. One receiver-side
  correction was made in TradeForge; no Cockpit producer correction was
  required.

---

## M15 - Replayable Cognitive Reconstruction

**Status:** Planned

**Evidence Density Slice:** Implemented 2026-07-12 (EV-00 through EV-05).

## Semantic Intent

Reconstruct historical discretionary cognition with high-fidelity replayable context.

## Architectural Significance

Replay evolves from what happened toward what was believed, why it was believed, what evidence existed, and what was ignored.

## Canonical Concepts

* [[Cognitive Replay]]
* [[Historical Reasoning]]
* [[Belief Reconstruction]]
* [[Context Snapshot]]
* [[Conviction Evolution]]
* [[Replayable Cognition]]

## Scope

M15 introduces point-in-time cognitive reconstruction, contextual evidence snapshots, historical belief reconstruction, conviction evolution replay, operator reasoning timelines, ignored evidence analysis, replay-attached advisory state, and regime-aware replay reconstruction.

## Linked Runtime Issues

* TF-D001: Implement point-in-time cognition reconstruction
* TF-D002: Implement advisory state replay snapshots
* TF-D003: Implement historical evidence reconstruction
* TF-D004: Implement conviction evolution timelines
* TF-D005: Implement ignored-evidence overlays
* TF-D006: Implement contextual replay comparisons
* TF-D007: Implement replay-linked interpretation history
* TF-D008: Implement replay-attached uncertainty state

## Acceptance Meaning

* Replay reconstructs cognition rather than only workflows.
* Operators can inspect historical reasoning honestly.
* Cognitive hindsight analysis becomes operationally meaningful.

---

## M16 - Attention Allocation And Opportunity Funnel

**Status:** Planned

## Semantic Intent

Help operators allocate limited cognitive bandwidth effectively.

## Architectural Significance

The core problem is often attention scarcity rather than prediction. M16 focuses on what deserves operator attention today.

## Canonical Concepts

* [[Attention Allocation]]
* [[Opportunity Funnel]]
* [[Candidate Queue]]
* [[Operational Prioritization]]
* [[Cognitive Load]]
* [[Advisory Queue]]

## Scope

M16 introduces attention ranking systems, operator cognitive queues, opportunity prioritization, contextual urgency overlays, candidate clustering, regime-aware surfacing, watchlist cognition flows, and discretionary workload management.

## Linked Runtime Issues

* TF-E001: Implement operator attention queues
* TF-E002: Implement contextual opportunity ranking
* TF-E003: Implement cognitive load management overlays
* TF-E004: Implement opportunity clustering
* TF-E005: Implement watchlist cognition workflows
* TF-E006: Implement regime-aware attention prioritization
* TF-E007: Implement stale-opportunity decay logic
* TF-E008: Implement discretionary focus tracking

## Acceptance Meaning

* TradeForge evolves into a discretionary opportunity funnel.
* The system assists attention allocation rather than prediction alone.

---

## M17 - Simulation And Regime Experimentation

**Status:** Planned

## Semantic Intent

Enable replayable hypothetical experimentation across different market environments.

## Scope

M17 introduces hypothetical replay branching, regime simulation, thesis stress testing, alternative decision-path exploration, scenario experimentation, and cognitive what-if analysis.

## Acceptance Meaning

* Historical and hypothetical replay become composable.
* Cognitive experimentation becomes possible without creating execution authority.

---

## M18 - Adaptive Advisory Research Infrastructure

**Status:** Planned

## Semantic Intent

Introduce adaptive research experimentation while preserving human sovereignty.

## Scope

M18 introduces adaptive evidence weighting research, RL experimentation sandboxing, advisory ranking experimentation, historical pattern research, and non-authoritative adaptive overlays.

## Acceptance Meaning

* RL and adaptive systems remain research/advisory infrastructure.
* Human sovereignty remains preserved.
* Adaptive infrastructure depends on replayable historical truth.

---

## M19 - Long-Horizon Cognitive Performance Analysis

**Status:** Planned

## Semantic Intent

Measure discretionary cognition quality longitudinally across years of operational history.

## Scope

M19 introduces long-term decision quality analysis, thesis category performance, operator growth tracking, regime-specific cognition analysis, historical behavioral evolution, and evidence usefulness analysis.

## Acceptance Meaning

* TradeForge can evaluate whether its advisory and cognitive structures actually improve long-term operator process.
* Cognitive performance analysis remains reflective and advisory, not lifecycle or execution authority.

---

# Near-Term Product Milestones (registered 2026-07-09)

The following milestones originate from the 2026-07-09 comprehensive product
audit (knowledge base:
`knowledge/raw/20260709-comprehensive-product-audit.md`). They are
deliberately prioritized AHEAD of M15 through M19: the audit concluded that
paper execution, ease of use, and evidence density close the operational
loop that the cognitive milestones (M15+) will later deepen. M15 through M19
remain planned and unchanged.

Each milestone has a detailed implementation plan in the knowledge base
(paths cited per milestone) and registered issues in
`DOCS/ISSUE_REGISTER.md`.

---

## M-PT - Paper Execution And Outcome Truth

**Status:** Planned

## Semantic Intent

Close the decision lifecycle loop with real broker facts at zero financial
risk. Execution and Position stages gain paper-broker-backed order
submission, fill reconciliation, and outcome truth, so Review reflects
actual fills rather than hand-entered numbers.

## Architectural Significance

Introduces the first execution boundary: an ExecutionPort with an Alpaca
paper adapter (`paper=True` hardcoded) and a deterministic fake adapter.
Broker interactions are recorded as immutable `PaperOrder*` events; the
Event Ledger remains canonical and broker state is reconciled into events,
never trusted live. Order submission is human-command-only; a three-layer
guard makes live trading structurally impossible and an import-boundary
test proves advisory code cannot reach the execution service.

## Canonical Concepts

Human Decision Sovereignty, Event Ledger Canonical Truth, Provider Boundary,
Replayability Is Foundational.

## Scope

Paper order domain model and event taxonomy; ExecutionPort + Alpaca paper
adapter + fake adapter; ExecutionOrchestrationService; polling
OrderSyncService; Armed-trigger evaluation surfacing attention items (never
auto-submitting); execution API routes in a dedicated router file; workspace
surfaces with persistent PAPER badges; execution-quality facts in review
projections.

## Explicit Exclusions

Live-money trading in any form; AI-triggered or automated order submission;
auto-submit on Armed triggers (future dedicated ADR required); websocket
streaming; broker portfolio import.

## Linked Runtime Issues

TF-P001 through TF-P012 (see issue register).

## Detailed Plan

`knowledge/raw/20260709-paper-trading-implementation-plan.md`

## Acceptance Meaning

* A plan can be paper-executed, tracked to fill, and reviewed against actual
  outcome data end to end.
* Replaying a decision containing paper events makes zero broker calls.
* Human sovereignty and the AI advisory boundary remain fully intact.

---

## M-EZ - Ease Of Use, Evidence Density, And Entry Ramp

**Status:** Planned

## Semantic Intent

Make TradeForge usable by a household (operator + family): one-command
start, evidence that arrives without being asked for, and a low-friction
entry ramp — without weakening lifecycle rigor at the Approval gate.

## Architectural Significance

Addresses the audit's core diagnosis ("the product models cognition better
than it models evidence") and the onboarding wall. The 2026-07-12 Evidence
Density refinement narrows the next product-value slice: define evidence and
attention-ranking authority first, then ship snapshots, watchlist, transparent
ranking, per-symbol evidence, and charting. This prevents automated evidence
collection from becoming a larger unranked list. M-EZ also introduces the
first background scheduling capability (snapshot refresh), a pre-lifecycle
watchlist object, deterministic per-symbol evidence surfaces, operator
identity on canonical events (extending ADR-0022), and a documented two-tier
issue discipline.

## Scope

Postgres-by-default single compose stack serving the built frontend; in-app
first-run wizard replacing the CLI master-key step; documentation truth pass
(empty DOCS files, stale PROJECT.md, single roadmap authority); Evidence
Density design authority; scheduled snapshot job; watchlist; transparent
attention ranking; per-symbol evidence panel answering the blue-pin questions;
one price chart component; quick-capture idea tier with draft-status stub
thesis; guided first-decision mode; operator identity profiles; two-tier issue
discipline documentation; KB hygiene pass.

## Explicit Exclusions

Multi-tenant hosting and real authentication; mobile apps; additional
advisory analytics; any weakening of the structured thesis requirement at
Approval; dashboard-style reorganization (ADR-0007 stands — charts are
visual evidence inside decision surfaces, not dashboard organization).

## Linked Runtime Issues

EZ-01 through EZ-03, EV-00 through EV-05, RAMP-01 through RAMP-03,
GOV-01 through GOV-02 (see issue register).

Corrective feedback closed against the EV slice:

- TF-F078: Proxy Evidence API Routes In Vite Dev Server (**Done**)
- TF-F079: Return Partial Alpha Vantage Fundamentals From Overview (**Done**)

## Detailed Plan

`knowledge/raw/20260709-product-viability-and-ease-of-use-roadmap.md`

Evidence Density refinement:
`knowledge/processed/20260712-evidence-density-attention-ranking-synthesis.md`
and `knowledge/topics/evidence-density-and-attention-ranking.md`

Runtime authority:
`DOCS/evidence-density-and-attention-ranking.md`

## Acceptance Meaning

* A family member can start the system with one command, capture an idea in
  under two minutes, and see real evidence without configuring anything.
* Evidence density catches up with the cognitive framework.
* Attention ranking is transparent, deterministic, provenance-backed, and
  explicitly not a buy/sell recommendation or lifecycle authority.
* Governance overhead is calibrated to change risk, not applied uniformly.
* GOV-01 is complete: runtime agent bootstrap files now distinguish Tier A
  full-ceremony work from Tier B bounded low-risk batch work.
* GOV-02 is complete: bounded KB hygiene removed the oversized raw LiteLLM
  log from tracked raw knowledge, consolidated root raw notes into
  `knowledge/raw/`, and marked M15 `TF-D001` through `TF-D008` deferred.
* EZ-01 is complete: Docker Compose now builds a Postgres-backed TradeForge
  runtime image, runs migrations on startup, and serves the built frontend from
  the API origin at `http://localhost:8000`.

---

## M-RF - API Boundary Decomposition

**Status:** Complete (2026-07-12; TF-RF001 through TF-RF010 landed, OpenAPI
snapshot byte-identical throughout. Deviations recorded in the issue
register: `_validated_import_field_names` stayed at the API boundary because
it raises HTTPException; `lifecycle.py` (2,082 lines) and `advisory.py`
(1,634 lines) exceed the aspirational ~800-line ceiling because the plan's
stronger rule — models, mappers, and handlers travel together per domain —
won.)

## Semantic Intent

Decompose the 7,504-line `src/app/api/routes.py` monolith (82 routes, ~162
response models, service accessors, mappers, and an embedded markdown import
subsystem) into per-domain router modules with zero behavior change.

## Architectural Significance

Pure structural refactor inside the ADR-0020 boundary, gated by a committed
OpenAPI contract snapshot that must remain byte-identical across all phases.
Includes one deliberate layer correction: markdown import parsing moves from
the HTTP layer to `src/services/advisory/local_import_parsing.py`
(Layer Separation invariant). Reduces collateral-edit risk for AI-assisted
implementation of all subsequent milestones.

## Scope

OpenAPI snapshot harness; `deps.py` accessor extraction; per-domain modules
under `src/app/api/routes/` (runtime, behavioral, replay, provenance,
market, workspace, lifecycle, advisory x3, governance); import-parsing layer
correction; final assembly and monolith deletion.

## Explicit Exclusions

Route, schema, or behavior changes of any kind; Depends() conversion
(deferred to M-RF2); error-handling changes; async conversions.

## Linked Runtime Issues

TF-RF001 through TF-RF010 (see issue register).

## Detailed Plan

`knowledge/raw/20260709-routes-refactor-implementation-plan.md`

## Acceptance Meaning

* No file in `src/app/api/` exceeds ~800 lines; the OpenAPI contract is
  provably unchanged; layer separation is restored for import parsing.

---

## M-RF-FE - Frontend API Client Decomposition

**Status:** Planned

## Semantic Intent

Decompose the 1,856-line `frontend/src/api/runtime.ts` client (~95 types,
~55 fetchers, 33 importing files) into per-domain modules mirroring M-RF
backend names, and unify the two-class error handling onto the
`readOperationalJson` pattern.

## Architectural Significance

The barrel re-export keeps all 33 importers compiling unchanged, making
TypeScript strict mode the refactor harness. The error-handling unification
(final phase, explicitly semantic) closes the failure mode behind TF-F069
at the ~49 call sites that hand-roll response parsing.

## Scope

`http.ts` request helper; per-domain client modules (lifecycle, replay,
workspace, market, advisory, generation, imports, behavioral, governance);
error-handling unification; closeout with module map in `frontend/DESIGN.md`.

## Explicit Exclusions

Endpoint or type shape changes; state-management or react-query adoption;
OpenAPI type generation (recorded as deferred follow-up); test-runner
introduction (deferred).

## Linked Runtime Issues

TF-RFE001 through TF-RFE008 (see issue register).

## Detailed Plan

`knowledge/raw/20260709-frontend-api-client-refactor-plan.md`

## Acceptance Meaning

* Client modules mirror backend router domains one-to-one; every API call
  site shares one guarded request path; typecheck/build stay green
  throughout.

---

## M-RF2 - API Dependency Injection

**Status:** Planned (unblocked 2026-07-12 — M-RF complete)

## Semantic Intent

Convert route handlers from service-locator acquisition
(`request.app.state` accessors) to declared FastAPI dependency injection
(`Annotated[..., Depends(get_x)]`).

## Architectural Significance

Handlers declare their dependencies; tests gain `dependency_overrides`;
future cross-cutting dependencies (operator identity from RAMP-03,
execution-boundary guards from M-PT) become declarable. The OpenAPI snapshot
from M-RF remains byte-identical throughout — dependency functions take
exactly one parameter (`request: Request`), guaranteeing no schema change.

## Scope

Accessor inventory and classification; public `get_*` renames; handler
conversion one module per commit; request-taking helper conversion to
explicit parameters; one demonstration override test; closeout gates.

## Explicit Exclusions

Changes to `create_app()` wiring or its keyword-argument test plumbing;
rewrites of existing tests; behavior or schema changes of any kind.

## Linked Runtime Issues

TF-RF2-001 through TF-RF2-006 (see issue register).

## Detailed Plan

`knowledge/raw/20260709-depends-injection-conversion-plan.md`

## Acceptance Meaning

* Dependencies are visible in handler signatures; a service can be swapped
  in one test line; the API contract is provably unchanged.

---

# Recommended Near-Term Sequence

```text
Completed foundation:
1. M-RF (API decomposition)
2. EV-00 through EV-05 (Evidence Density vertical slice)
3. M14C TF-R001/TF-R002 plus TF-F081 receiver correction

Next runtime sequence:
1. GOV-01 (runtime governance clarification) - complete
2. GOV-02 coordination (bounded KB hygiene only where it prevents current
   project truth from being understood) - complete
3. EZ-01 - complete
4. EZ-02 - next
5. EZ-03
6. RAMP-01
7. RAMP-02
8. Operator walkthrough
9. Evidence-based next-milestone decision

Deferred until operator validation or a concrete blocker changes priority:
- RAMP-03
- M-PT
- M-RF2
- M-RF-FE
- M15 through M19
- Research Cockpit intake expansion
```

---
