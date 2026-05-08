# TradeForge Runtime System

TradeForge is an event-sourced, persona-driven, workflow-centric decision support system for trading and investing workflows.

This repository contains the executable runtime implementation of TradeForge.

It is NOT:

* a generic trading bot
* a CRUD trade tracker
* a signal generator
* a dashboard-centric brokerage application
* an autonomous trading system

TradeForge is:

> a structured cognition and decision system for trading workflows.

---

# Runtime Purpose

This repository implements:

* event-sourced workflow execution
* decision lifecycle orchestration
* scenario analysis systems
* market intelligence systems
* replay/review infrastructure
* operational workspaces
* deterministic rule enforcement

The canonical semantic and architectural doctrine lives in:

```text
C:\Users\bosto\dockerstuff\knowledge-base\TradeForge\
```

---

# Core Architectural Principles

## Event Sourcing

All durable state derives from immutable events.

The event ledger is canonical runtime truth.

Projections are derived views only.

---

## Decision Lifecycle Integrity

Canonical lifecycle:

```text
Idea → Thesis → Plan → Approval → Execution → Position → Review
```

Lifecycle stages must not be collapsed or bypassed.

---

## Replayability

The system must support deterministic replay and review of:

* market context
* workflow state
* decision state
* active positions
* scenarios
* rule evaluations
* reviews and annotations

Replayability is a first-class architectural concern.

---

## AI Governance

AI is advisory only.

AI may:

* summarize
* rank
* contextualize
* surface scenarios

AI may NOT:

* mutate canonical state
* bypass lifecycle controls
* execute trades
* override deterministic rules

---

# Repository Structure

```text
TradeForge/
├── DOCS/
│   └── adr/
│
├── src/
│   ├── app/
│   ├── domain/
│   ├── infrastructure/
│   └── services/
│
├── tests/
│
├── AGENTS.md
├── ARCHITECTURE.md
├── INVARIANTS.md
├── PROJECT.md
└── README.md
```

---

# Source Structure

## src/domain/

Pure domain model and event semantics.

Contains:

* entities
* value objects
* lifecycle rules
* domain events
* invariant enforcement

No infrastructure concerns allowed.

---

## src/services/

Application orchestration layer.

Coordinates:

* workflows
* lifecycle transitions
* scenario processing
* workspace orchestration
* replay orchestration

Services do NOT own persistence semantics.

---

## src/infrastructure/

Infrastructure adapters and runtime integrations.

Contains:

* event store implementations
* broker adapters
* persistence adapters
* external API integrations

Infrastructure must not redefine domain semantics.

---

## src/app/

Runtime entrypoints.

Examples:

* CLI
* API
* background processes

---

# Runtime Documentation

## DOCS/

Contains:

* runtime architecture
* ADRs
* implementation decisions
* technical domain mappings
* event schema evolution

---

# Development Workflow

Before implementation work:

1. Load semantic context from:

   * SEMANTIC_BOOTSTRAP.md
   * INVARIANTS.md
   * ARCHITECTURE.md

2. Identify:

   * affected architecture layer
   * impacted invariants
   * lifecycle impact
   * event model impact

3. Produce explicit design reasoning.

4. Only then implement.

See:

```text
AGENTS.md
```

for mandatory operational rules.

---

# Relationship to Knowledge Base

This runtime repository executes the system.

The knowledge-base repository defines:

* semantic truth
* ontology
* workflow semantics
* architectural doctrine
* AI governance philosophy
* cognition structure

Knowledge-base repository:

```text
C:\Users\bosto\dockerstuff\knowledge-base\TradeForge\
```

---

# Current Status

TradeForge is currently in active architectural and foundational implementation development.

Primary focus areas:

* event ledger foundation
* lifecycle engine
* deterministic replayability
* scenario analysis
* workspace cognition systems
* semantic/runtime alignment

---

# Final Principle

Correct architecture is more important than rapid feature delivery.

When uncertain:

* preserve invariants
* preserve replayability
* preserve semantic consistency
* preserve lifecycle integrity
* prefer explicit design over shortcuts
