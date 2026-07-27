# TradeForge Runtime — AGENTS.md

## Purpose

This repository contains the runtime implementation of TradeForge.

It is an event-sourced, persona-driven, decision-lifecycle trading system.

This file defines **hard rules for all Codex-assisted development in this repository**.

---

# Core System Constraint

This repository is an **execution system only**.

It does NOT define:
- ontology
- semantics
- UX philosophy
- event meaning
- lifecycle rules

Those are defined in:

```
C:\Users\bosto\dockerstuff\TradeForge-Project\TradeForge-KnowledgeBase
```

The knowledge base is a sibling repository to this runtime checkout, not a
directory under `TradeForge/`. Codex MUST use the absolute path above when
checking semantic authority.

The Research Cockpit sibling repository at
`C:\Users\bosto\dockerstuff\TradeForge-Project\TradeForge-ResearchCockpit`
is an upstream evidence and research producer. Activate its context only for
research-production, advisory-handoff, import-boundary, or cross-repository
governance work. It has no TradeForge lifecycle, canonical-state, approval,
execution, or runtime implementation-planning authority.

---
# Runtime Semantic Activation Rule

Codex MUST use bounded semantic activation.

Do NOT load the entire knowledge base by default.

Before semantic loading:

1. Read:
   - C:\Users\bosto\dockerstuff\TradeForge-Project\TradeForge-KnowledgeBase\SEMANTIC_BOOTSTRAP.md
   - C:\Users\bosto\dockerstuff\TradeForge-Project\TradeForge-KnowledgeBase\INVARIANTS.md
   - C:\Users\bosto\dockerstuff\TradeForge-Project\TradeForge-KnowledgeBase\knowledge\index\runtime-context-map.md

2. Determine the dominant task category.

3. Load only the semantic domains relevant to the task.

Examples:

- persistence work should NOT load workspace doctrine
- replay work should NOT load UI doctrine
- API work should NOT load AI advisory doctrine

Canonical knowledge is authoritative when relevant.

Canonical knowledge is NOT globally active.

---

# Truth Hierarchy (Mandatory)

When in doubt, resolve authority in this order:

1. C:\Users\bosto\dockerstuff\TradeForge-Project\TradeForge-KnowledgeBase (semantic truth)
2. C:\Users\bosto\dockerstuff\TradeForge-Project\TradeForge\DOCS (implementation truth)
3. C:\Users\bosto\dockerstuff\TradeForge-Project\TradeForge\src (execution truth)

Code must NEVER override knowledge-base semantics.

---

# Hard Architecture Rules

## 1. Event Sourcing is non-negotiable

- all state must be derived from events
- event store is the only source of truth
- no hidden state allowed

---

## 2. Decision Lifecycle is strict

Allowed flow:

```
Idea → Thesis → Plan → Approval → Execution → Position → Review
```

Codex MUST NOT:
- skip stages
- collapse stages
- shortcut execution

---

## 3. Workspaces are NOT UI

Workspaces are:
- persistent decision environments
- event-derived projections
- cognitive state containers

NOT:
- dashboards
- tabs
- views

---

## 4. Personas affect interpretation only

Personas:
- influence ranking, weighting, interpretation
- do NOT mutate system state
- do NOT execute logic directly

---

## 5. AI is advisory only

AI may:
- rank scenarios
- summarize state
- suggest interpretations

AI may NOT:
- execute trades
- modify event ledger
- bypass lifecycle engine
- override deterministic rules

---
# Issue Discipline Rule

Every code change must be tied to a tracked issue.

Before writing or modifying code, Codex MUST identify:

1. issue ID
2. milestone
3. issue title
4. affected domain layer
5. impacted ADRs
6. impacted invariants
7. acceptance criteria

If no issue exists, Codex MUST stop and propose a new issue before implementation.

Codex MUST NOT:
- write untracked code
- implement exploratory changes without an issue
- combine unrelated issues in one change
- expand issue scope without explicit approval

Issue records are maintained in:

C:\Users\bosto\dockerstuff\TradeForge\DOCS\ISSUE_REGISTER.md

Milestone planning is maintained in:
C:\Users\bosto\dockerstuff\TradeForge\DOCS\Milestone_Roadmap_v2.md


GitHub issues may mirror these records, but the repository issue register remains the local planning source of truth.

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

# Coding Discipline Rules

## Before writing any code Codex MUST:

1. Confirm issue discipline:
   - issue ID exists
   - milestone is known
   - acceptance criteria are clear
   - change is within issue scope

2. Identify affected domain layer:
   - domain
   - services
   - infrastructure
   - app

3. Load only the semantic context required by the task category.

4. Verify against only the relevant runtime DOCS:
   - architecture consistency
   - ADR compliance

5. Produce explicit design plan (mandatory step)

6. Only then implement code

---

# Forbidden Patterns

Codex MUST NOT:

- “just implement it quickly”
- skip design reasoning
- merge domain + infrastructure logic
- introduce ad-hoc state storage
- bypass event model
- create hidden coupling between services

---

# Domain Integrity Rules

Domain layer must be:

- pure
- framework-agnostic
- event-aware only
- free of persistence logic

Infrastructure layer owns:
- databases
- brokers
- external APIs

Services layer owns:
- orchestration only
- no persistence logic

---

# Event Model Enforcement

Events must:

- represent facts, not interpretations
- be immutable
- be append-only
- be replayable

If something is not an event → it is not system truth.

---

# Failure Handling Rule

If Codex is uncertain:

STOP and ask for clarification OR propose a design phase.

Do NOT guess architecture.

---

# Design First Rule

No code without:

- explicit design reasoning
- event impact analysis
- lifecycle impact analysis

---


# Final Principle

> Correct architecture is more important than feature completion.

If a change improves speed but violates structure:
→ it is rejected
