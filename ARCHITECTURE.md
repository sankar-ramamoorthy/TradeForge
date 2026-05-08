# TradeForge — Architecture Overview

## System Purpose

TradeForge is a persona-driven, workflow-centric, decision lifecycle system for trading and investing.

It is designed to improve:
- situational awareness
- decision quality
- execution discipline
- reflective learning

It is NOT a trading bot or signal system.

---

# 1. High-Level System Architecture

TradeForge is structured as a layered system:

```text
Persona Layer
    ↓
Workspace Layer
    ↓
Market Intelligence + Scenario Engine
    ↓
Decision Lifecycle Engine
    ↓
Event Store (Canonical Truth)
    ↓
Replay / Review System
    ↓
External Integrations (Broker, Data, UI)
```

---

# 2. Architectural Layers

## 2.1 Persona Layer

Responsible for:
- defining behavioral context
- shaping interpretation of market conditions
- influencing scenario weighting

Key principle:
> Personas do NOT change system state — they change interpretation.

---

## 2.2 Workspace Layer

A workspace is a persistent decision environment.

It contains:
- active positions (projection)
- decision queue
- watchlist / opportunities
- briefing context
- review artifacts

Key principle:
> Workspaces are derived views of event history, not stored dashboards.

---

## 2.3 Market Intelligence + Scenario Engine

This layer transforms raw data into structured understanding.

Responsibilities:
- normalize market data
- detect regime shifts
- generate scenarios
- rank opportunities
- contextualize macro environment

Key principle:
> This layer produces candidates, not decisions.

---

## 2.4 Decision Lifecycle Engine

Core workflow system that governs decision progression:

```text
Idea → Thesis → Plan → Approval → Execution → Position → Review
```

Responsibilities:
- enforce lifecycle transitions
- validate stage correctness
- block invalid shortcuts
- emit lifecycle events

Key principle:
> No decision bypasses lifecycle stages.

---

## 2.5 Event Store (System of Record)

The event store is the **canonical truth layer**.

Responsibilities:
- store immutable events
- provide replay capability
- reconstruct system state
- support auditability

Key principle:
> If it is not an event, it does not exist.

---

## 2.6 Replay / Review System

Reconstructs past system states for learning and analysis.

Responsibilities:
- rebuild historical workspace states
- replay decision flows
- analyze outcome vs intent
- support learning loops

Key principle:
> Replay is a first-class feature, not an afterthought.

---

## 2.7 External Integration Layer

Connects to:
- brokers
- market data feeds
- news sources
- execution APIs

Key principle:
> External systems are unreliable inputs, not truth sources.

---

# 3. Data Flow Model

```text
External Data
     ↓
Market Intelligence Layer
     ↓
Scenario Engine
     ↓
Decision Lifecycle Engine
     ↓
Event Store (append-only)
     ↓
Workspace + Replay Projections
     ↓
UI / User Decision Surface
```

---

# 4. Core System Principles

## 4.1 Event Sourcing is Mandatory
All state is derived from events.

## 4.2 Lifecycle Integrity
Decisions cannot skip stages.

## 4.3 Persona-Driven Interpretation
Interpretation varies by persona, not structure.

## 4.4 AI is Advisory Only
AI may:
- rank
- summarize
- cluster

AI may NOT:
- execute trades
- mutate event store
- bypass lifecycle rules

## 4.5 Replayability is Required
All system states must be reconstructable from events.

---

# 5. Module Boundaries (src/)

```
src/
├── domain/
│   ├── events/
│   ├── lifecycle/
│   ├── models/
│
├── services/
│   ├── decision_engine/
│   ├── scenario_engine/
│   ├── market_intelligence/
│   ├── workspace_engine/
│
├── infrastructure/
│   ├── event_store/
│   ├── broker_adapters/
│
├── app/
│   ├── api/
│   ├── cli/
```

---

# 6. Strict Separation Rules

## Domain Layer
- pure logic
- no persistence
- no external dependencies

## Services Layer
- orchestration only
- no direct persistence logic

## Infrastructure Layer
- database + APIs + brokers only

## App Layer
- entrypoints only (CLI/API/UI)

---

# 7. Architectural Stability Rule

This architecture is **not flexible by default**.

Changes require:
- ADR creation
- impact on event model
- lifecycle validation
- workspace consistency check

---

# Final Principle

TradeForge is a system for structured decision-making under uncertainty.

Architecture exists to enforce:
- clarity
- discipline
- auditability
- cognitive continuity