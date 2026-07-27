# CLAUDE.md

# TradeForge Runtime — Claude Bootstrap

This repository contains the runtime implementation of TradeForge.

TradeForge is an event-sourced, workflow-centric, decision-support system for investing and trading workflows.

This repository contains executable architecture and runtime implementation.

It does NOT define canonical semantic truth.

Canonical doctrine lives in:

```text
C:\Users\bosto\dockerstuff\TradeForge-Project\TradeForge-KnowledgeBase
```

The Research Cockpit sibling repository at
`C:\Users\bosto\dockerstuff\TradeForge-Project\TradeForge-ResearchCockpit`
is an upstream evidence and research producer. Activate its context only for
research-production, advisory-handoff, import-boundary, or cross-repository
governance work. It has no TradeForge lifecycle, canonical-state, approval,
execution, or runtime implementation-planning authority.

---

# Core Rule

Canonical does not mean globally active.

Canonical means authoritative when relevant.

Use bounded semantic activation.

Do NOT load the entire knowledge base by default.

---

# Mandatory Runtime Boot Sequence

## 1. Always Read

Before implementation work, read:

```text
C:\Users\bosto\dockerstuff\TradeForge-Project\TradeForge-KnowledgeBase\SEMANTIC_BOOTSTRAP.md
C:\Users\bosto\dockerstuff\TradeForge-Project\TradeForge-KnowledgeBase\INVARIANTS.md
C:\Users\bosto\dockerstuff\TradeForge-Project\TradeForge-KnowledgeBase\knowledge\index\runtime-context-map.md
```

These define:

- invariant boundaries
- semantic operating rules
- runtime activation discipline
- architecture constraints

---

## 2. Determine Task Category

Identify the dominant task category.

Examples:

- lifecycle transitions
- replay systems
- persistence infrastructure
- API boundaries
- workspace projections
- deterministic rules
- event ledger work
- ontology alignment

---

## 3. Load Only Relevant Semantic Context

Consult:

```text
C:\Users\bosto\dockerstuff\TradeForge-Project\TradeForge-KnowledgeBase\knowledge\index\runtime-context-map.md
```

Load only the semantic domains relevant to the task.

Examples:

- persistence work should not load workspace doctrine
- replay work should not load AI advisory doctrine
- API work should not load replay architecture

Escalate context breadth only when necessary.

---

# Truth Hierarchy

When contradictions exist, resolve authority in this order:

1. knowledge base doctrine
2. runtime DOCS
3. runtime implementation

Code must never silently override semantic doctrine.

---

# Runtime Constraints

## Event Sourcing Is Mandatory

- all durable state derives from events
- events are immutable
- projections are derived views
- replayability is foundational

## Decision Lifecycle Is Strict

Canonical lifecycle:

```text
Idea → Thesis → Plan → Approval → Execution → Position → Review
```

Do not collapse lifecycle stages.

Do not bypass workflow constraints.

## AI Is Advisory Only

AI may:

- summarize
- rank
- contextualize
- surface scenarios

AI may NOT:

- execute trades
- mutate canonical state
- bypass lifecycle rules
- override deterministic controls

Human decision sovereignty is mandatory.

---

# Issue Discipline

All implementation work must map to a tracked issue.

Before implementation:

- identify issue ID
- identify milestone
- identify affected domain layer
- identify impacted invariants
- identify affected ADRs
- confirm acceptance criteria

Do not implement untracked work.

Do not silently expand issue scope.

---

# Two-Tier Issue Discipline

TradeForge uses issue ceremony proportional to architectural risk.

## Tier A - Full Ceremony Required

Use Tier A for changes that touch any of:

- domain models or lifecycle semantics
- event taxonomy, Event Ledger behavior, replay, or projections
- persistence, migrations, transaction boundaries, or repository adapters
- security, credentials, authentication, sessions, or operator identity
- AI advisory boundaries, provider governance, import mediation, or execution
  boundaries
- backend API contracts, schemas, route behavior, or cross-repository
  authority boundaries

Tier A work requires a single tracked issue with explicit issue ID, milestone,
affected layer, linked ADRs or ADR impact, impacted invariants, acceptance
criteria, validation plan, planning-state updates, and a focused commit/PR.
Do not batch unrelated Tier A issues.

## Tier B - Lightweight Batch Allowed

Tier B may be used only for low-risk changes such as:

- frontend copy, labels, spacing, styling, and layout polish that does not
  change workflow semantics
- documentation wording, formatting, link repair, or status cleanup
- test fixture naming or comments that do not change behavior

Tier B work may batch related low-risk items under one registered issue when
the issue names the allowed files, the acceptance criteria are explicit, and
validation remains appropriate to the touched surface.

Tier B does not waive issue tracking, branch discipline, validation, or the
requirement to preserve lifecycle, event, replay, security, advisory, and
execution boundaries.

---

# Runtime Design Rules

Before writing code:

1. determine affected architectural layer
2. load only relevant semantic context
3. inspect only relevant runtime DOCS
4. evaluate event impact
5. evaluate lifecycle impact
6. produce explicit design reasoning
7. only then implement code

If semantic alignment has not occurred:

STOP.

---

# Domain Integrity Rules

Domain layer must remain:

- framework-agnostic
- persistence-free
- deterministic
- event-aware only

Infrastructure owns:

- databases
- external APIs
- brokers
- adapters

Services own orchestration only.

---

# Forbidden Patterns

Do NOT:

- bypass the event model
- introduce hidden mutable state
- merge domain and infrastructure logic
- create ad-hoc coupling
- skip design reasoning
- implement “quick hacks”
- silently redefine ontology

---

# Failure Handling Rule

If uncertain:

- stop
- ask for clarification
- propose a design phase

Do not guess architecture.

---

# Repository Navigation

Relevant runtime documentation:

```text
TradeForge/DOCS/
TradeForge/DOCS/ADR/
```

Primary semantic navigation:

```text
C:\Users\bosto\dockerstuff\TradeForge-Project\TradeForge-KnowledgeBase\knowledge\index\README.md
```

Primary activation routing:

```text
C:\Users\bosto\dockerstuff\TradeForge-Project\TradeForge-KnowledgeBase\knowledge\index\runtime-context-map.md
```

---

# Final Principle

Correct architecture is more important than rapid implementation.

TradeForge exists to support:

- disciplined decision-making
- replayable workflows
- structured cognition
- deterministic architecture
- reflective learning
- long-term operational consistency
