
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

**Status:** Planned

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
* TF-0049: Implement contextual operational summaries
* TF-0050: Implement provider provenance tracking

### Demo Enablement

* TF-0051: Add seeded demo market context flow
* TF-0052: Add replay-compatible market snapshot persistence strategy

## Acceptance Meaning

* Real-world market context becomes visible.
* Workspace cognition becomes operationally believable.
* Provider data remains advisory.
* Replay boundaries remain explicit.
* External APIs do not become canonical truth.
* Human lifecycle authority remains preserved.

---


## M10 — AI Advisory Boundary
Status: Planned
## Semantic Intent
Introduce AI assistance without compromising human sovereignty.
## Architectural Significance
AI remains advisory rather than authoritative.
## Canonical Concepts

* [[AI Advisory Boundary]]
* [[Human Decision Sovereignty]]

## Linked Runtime Issues

* TF-0053: Define AI advisory interfaces
* TF-0054: Implement replay summarization assistance
* TF-0055: Implement review assistance
* TF-0056: Implement advisory provenance tracking

## Acceptance Meaning

* AI cannot mutate canonical state directly.
* AI cannot approve lifecycle transitions.
* AI outputs remain reviewable artifacts.

---

## M11 — Behavioral Intelligence And Adaptive Review
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

* TF-0057: Detect recurring behavioral patterns
* TF-0058: Implement discipline signal engine
* TF-0059: Implement review clustering
* TF-0060: Implement historical behavior overlays

## Acceptance Meaning

* Behavioral learning becomes operational.
* Pattern recognition augments review quality.


---

## M12 — Simulation And Scenario Engine
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

* TF-0061: Implement simulation event environment
* TF-0062: Implement hypothetical replay branching
* TF-0063: Implement regime simulation engine
* TF-0064: Implement simulated workspace playback

## Acceptance Meaning

* Historical and hypothetical replay become composable.
* Cognitive experimentation becomes possible.


---

## M13 — Adaptive AI And RL Infrastructure
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

* TF-0065: Define RL experimentation boundaries
* TF-0066: Implement adaptive scenario evaluation
* TF-0067: Implement reinforcement-learning research environment
* TF-0068: Implement adaptive playbook experimentation

## Acceptance Meaning

* RL remains advisory and experimental.
* Human sovereignty remains preserved.
* Adaptive infrastructure depends on replayable historical truth.


---


