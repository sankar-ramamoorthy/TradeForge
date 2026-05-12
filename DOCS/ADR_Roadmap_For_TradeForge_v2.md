---
title: ADR Roadmap For TradeForge v2
type: roadmap
status: draft
tags: [TradeForge, ADR, roadmap, architecture, workspaces]
created: 2026-05-10
updated: 2026-05-10
---

# ADR Roadmap For TradeForge v2

This document defines the recommended ADR sequencing strategy for TradeForge as the system evolves from:

```text id="adr1"
semantic architecture
```

into:

```text id="adr2"
an operational replayable cognition system
```

The purpose of this document is NOT to fully define ADR contents.

Instead, it defines:

* which ADRs are needed
* why they matter
* when they should appear
* what architectural layer they stabilize
* dependency ordering

---

# Core Principle

TradeForge ADRs should stabilize:

```text id="adr3"
semantic and operational boundaries
```

NOT merely implementation details.

ADRs are especially important because TradeForge contains multiple interacting architectural domains:

* event sourcing
* workflow orchestration
* replay systems
* workspace cognition
* operational UX
* behavioral review
* AI advisory boundaries
* adaptive systems

Without ADR discipline, these domains will blur together over time.

---

# Recommended ADR Layers

The ADR stack naturally falls into:

| Layer                  | Purpose                      |
| ---------------------- | ---------------------------- |
| Semantic Foundation    | Truth model and lifecycle    |
| Cognitive Architecture | Workspaces and replay        |
| Runtime Architecture   | Persistence/API/UI           |
| Operational UX         | Interaction doctrine         |
| Intelligence Layer     | AI and market interpretation |
| Adaptive Systems       | Simulation and RL            |

---

# ADR Sequencing Philosophy

The sequencing rule should be:

```text id="adr4"
stabilize semantics
before implementation expansion
```

and:

```text id="adr5"
stabilize cognition architecture
before AI augmentation
```

This is critically important.

---

# PHASE 1 â€” Semantic Foundation ADRs

These establish immutable architectural truth.

Most of these already exist conceptually.

---

# ADR-0001 â€” Event Sourcing Core Model

## Purpose

Define immutable event-backed truth.

## Why It Matters

Everything downstream depends on:

* replay
* projections
* review
* auditability

---

# ADR-0002 â€” Decision Lifecycle Engine

## Purpose

Define lifecycle authority.

## Why It Matters

TradeForge is workflow-centric rather than CRUD-centric.

---

# ADR-0003 â€” Canonical Event Taxonomy

## Purpose

Stabilize event meaning.

## Why It Matters

Replay collapses if event semantics drift.

---

# ADR-0004 â€” Workspace Projection Model

## Purpose

Define projections as derived operational surfaces.

## Why It Matters

Prevents projections/UI from becoming truth authority.

---

# ADR-0005 â€” Scenario Engine Architecture

## Purpose

Define advisory scenario modeling.

## Why It Matters

Prevents scenarios from becoming implicit execution authority.

---

# ADR-0006 â€” AI Advisory Boundary Model

## Purpose

Preserve human decision sovereignty.

## Why It Matters

Prevents AI from mutating canonical state or lifecycle authority.

---

# ADR-0007 â€” Anti-Dashboard UX Decision

## Purpose

Establish cognition-first operational UX.

## Why It Matters

This is one of the most important TradeForge differentiators.

This ADR should explicitly define:

* anti-dopamine principles
* workflow-centric interaction
* operational calmness
* decision-state-centric UI
* replay-first cognition

---

# ADR-0008 â€” Replay System Design

## Purpose

Define replay as first-class architecture.

## Why It Matters

Replay is core product identity.

---

# ADR-0009 â€” Persona Interpretation Model

## Purpose

Define persona-aware interpretation boundaries.

## Why It Matters

Interpretation must not mutate truth.

---

# ADR-0010 â€” Market Intelligence Interpretation Layer

## Purpose

Separate context interpretation from authority.

## Why It Matters

Market intelligence remains advisory.

---

# ADR-0011 â€” Runtime Development Environment

## Purpose

Stabilize runtime tooling and environment conventions.

---

# IMPORTANT OBSERVATION

The existing ADR stack is already surprisingly coherent.

The next ADR wave is where the real evolution occurs.

---

# PHASE 2 â€” Workspace And Cognitive Architecture ADRs

These are now REQUIRED because the product direction clarified dramatically today.

These are probably the highest-priority new ADRs.

---

# ADR-0012 â€” Workspace Architecture Model

## Status

Accepted - created 2026-05-10

## Priority

VERY HIGH

## Purpose

Define workspaces as:

```text id="adr6"
operational cognition environments
```

rather than UI screens.

## Must Define

* workspace semantics
* workspace boundaries
* operational continuity
* attention management
* workflow-state-centric interaction

---

# ADR-0013 â€” Operational Attention Model

## Status

Accepted - created 2026-05-10

## Priority

VERY HIGH

## Purpose

Define:

* decision queues
* alerts
* operational obligations
* review obligations
* attention prioritization

## Why It Matters

TradeForge is fundamentally:

```text id="adr7"
an attention-management system
```

for discretionary cognition.

---

# ADR-0014 â€” Replay-Centric UX Model

## Status

Accepted - created 2026-05-10

## Priority

VERY HIGH

## Purpose

Define replay-aware interaction architecture.

## Must Define

* replay-linked workflows
* replay navigation
* timeline semantics
* historical reconstruction principles

---

# ADR-0015 â€” Behavioral Signal Architecture

## Priority

HIGH

## Purpose

Define behavioral observation boundaries.

## Must Clarify

* what is behavioral
* what is inferred
* what is canonical
* what is advisory

This becomes MASSIVE later.

---

# ADR-0016 â€” Thesis Drift Model

## Priority

HIGH

## Purpose

Define how thesis evolution and decay are represented.

## Why It Matters

This is becoming one of TradeForgeâ€™s unique concepts.

---

# ADR-0017 â€” Review And Reflective Learning Model

## Priority

HIGH

## Purpose

Define structured review semantics.

## Must Clarify

* decision quality vs outcome quality
* lessons
* reflective artifacts
* operational learning

---

# PHASE 3 â€” Runtime Infrastructure ADRs

These become important once MVP implementation begins.

---

# ADR-0018 â€” Postgres Event Store Persistence

## Purpose

Define durable event persistence architecture.

## Why It Matters

Replayable cognition requires durable immutable history.

---

# ADR-0019 â€” Projection Persistence Architecture

## Purpose

Define rebuildable projection storage.

## Why It Matters

Prevents projections from silently becoming truth authority.

---

# ADR-0020 â€” FastAPI Runtime Boundary

## Purpose

Define application orchestration boundary.

---

# ADR-0021 â€” React Workspace Runtime

## Status

Accepted - created 2026-05-12

## Purpose

Define workspace runtime architecture.

## Must Clarify

* routing
* workspace lifecycle
* operational layout
* replay-aware navigation

---

# ADR-0022 â€” Authentication And Operational Identity

## Status

Accepted - created 2026-05-12

## Purpose

Define identity, sessions, and operational isolation.

---

# PHASE 4 â€” MVP Productization ADRs

These stabilize the actual operational product.

---

# ADR-0023 â€” MVP Vertical Slice Definition

## Status

Accepted - created 2026-05-10

## Priority

VERY HIGH

## Purpose

Explicitly define:

```text id="adr8"
what TradeForge MVP v1 actually is
```

This ADR is critically important.

---

# ADR-0024 â€” Operating Workspace Design Doctrine

## Purpose

Stabilize the home operational workspace.

---

# ADR-0025 â€” Opportunity Workspace Design Doctrine

## Purpose

Define structured opportunity development.

---

# ADR-0026 â€” Plan Review Workspace Doctrine

## Purpose

Define intentional risk authorization.

---

# ADR-0027 â€” Active Position Workspace Doctrine

## Purpose

Define live decision-state supervision.

---

# ADR-0028 â€” Replay Workspace Doctrine

## Purpose

Define cognitive reconstruction UX.

This becomes one of the most important ADRs in the entire system.

---

# ADR-0029 â€” Review Workspace Doctrine

## Purpose

Define reflective learning architecture.

---

# ADR-0030 â€” Market Context Workspace Doctrine

## Purpose

Define contextual intelligence surfaces.

---

# ADR-0031 â€” Playbook And Doctrine Workspace

## Purpose

Define explicit operational doctrine management.

---

# PHASE 5 â€” Intelligence Layer ADRs

These should happen ONLY after the MVP cognition system is operational.

This sequencing matters enormously.

---

# ADR-0032 â€” Market Regime Interpretation Model

## Purpose

Define contextual market interpretation semantics.

---

# ADR-0033 â€” Scenario Discovery Model

## Purpose

Define scenario generation boundaries.

---

# ADR-0034 â€” AI Replay Assistance

## Purpose

Define AI replay summarization and reconstruction assistance.

---

# ADR-0035 â€” AI Review Assistance

## Purpose

Define AI-assisted reflective review.

---

# ADR-0036 â€” Advisory Provenance Model

## Purpose

Define explainability and provenance requirements.

---

# PHASE 6 â€” Adaptive Systems ADRs

These are future-state ADRs.

Do NOT introduce these too early.

---

# ADR-0037 â€” Behavioral Pattern Detection Architecture

## Purpose

Define adaptive behavioral analysis.

---

# ADR-0038 â€” Simulation Engine Architecture

## Purpose

Define hypothetical replay and simulation.

---

# ADR-0039 â€” Scenario Branching Replay Model

## Purpose

Define alternate replay path semantics.

---

# ADR-0040 â€” RL Experimentation Boundary

## Purpose

Define safe RL experimentation constraints.

This should remain VERY downstream.

---

# Recommended Immediate ADR Priority

If I were sequencing the next ADR work TODAY:

| Priority | ADR                                 |
| -------- | ----------------------------------- |
| 1        | Workspace Architecture Model        |
| 2        | Replay-Centric UX Model             |
| 3        | Operational Attention Model         |
| 4        | MVP Vertical Slice Definition       |
| 5        | Operating Workspace Design Doctrine |
| 6        | Review Workspace Doctrine           |
| 7        | Replay Workspace Doctrine           |
| 8        | Thesis Drift Model                  |
| 9        | Behavioral Signal Architecture      |
| 10       | Postgres Event Store Persistence    |

---

# Most Important Architectural Realization

The biggest evolution is this:

Originally the architecture was drifting toward:

```text id="adr9"
event sourcing + AI trading
```

Now it is clearly becoming:

```text id="adr10"
replayable operational cognition infrastructure
```

That is a dramatically more coherent and differentiated system direction.


