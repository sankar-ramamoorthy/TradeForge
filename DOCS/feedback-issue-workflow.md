---
title: Feedback Issue Workflow
type: architecture-doc
status: canonical
tags:
  - TradeForge
  - architecture
  - feedback-workflow
  - bug-fixing
  - operational-testing
  - development-workflow
created: 2026-05-15
updated: 2026-05-15
related:
  - feedback-issue-development-loop
  - runtime-kb-development-workflow
  - ISSUE_REGISTER
  - replayability
  - semantic-stabilization
kb_canonical_playbook: >
  knowledge-base/TradeForge/playbooks/development/feedback-issue-development-loop.md
kb_related:
  - "[[INVARIANTS]]"
  - "[[Decision Lifecycle]]"
  - "[[Replayability Is Foundational]]"
  - "[[UX Is Architectural]]"
  - "[[Human Decision Sovereignty]]"
issue_series: TF-F###
see_also:
  - DOCS/runtime-kb-development-workflow.md
---

# Feedback Issue Workflow

## Purpose

This document explains the architectural reasoning behind the TradeForge feedback issue workflow.

It describes:
- why a separate workflow exists for feedback-originated issues
- how it differs from the milestone development loop
- what the TF-F### issue series represents
- how diagnosis and feedback closure govern this workflow

This is NOT the canonical operational playbook.

The canonical workflow definition lives in:

```
knowledge-base/TradeForge/playbooks/development/feedback-issue-development-loop.md
```

---

# What a Feedback Issue Is

Feedback issues originate from:
- operational walkthroughs
- user testing sessions
- live system observation
- architectural realizations discovered during use

They are captured in the `TF-F###` issue series and registered in `DOCS/ISSUE_REGISTER.md`.

Feedback issues are distinct from roadmap issues (`TF-####`) because:
- they are not pre-planned
- they are discovered, not designed
- they may challenge existing architectural assumptions
- they require diagnosis before planning

---

# Why a Separate Workflow Exists

The [[Runtime ↔ KB Development Loop]] is optimized for milestone feature work:
- architecture-first planning
- full ADR evaluation
- heavy KB stabilization cycles
- milestone roadmap alignment

Feedback issues need a structurally different starting point.

The feedback workflow front-loads **diagnosis** rather than planning.

The workflow exists to answer:
> "What is actually wrong — and what is the minimum correct change?"

rather than:
> "What is the next thing to build?"

---

# Core Differences From the Milestone Loop

| Concern | Milestone Loop | Feedback Loop |
|---|---|---|
| Starting point | Roadmap issue selection | Diagnosed operational gap |
| Phase 1 | Select from roadmap | Triage TF-F register + understand source |
| Planning weight | Full architecture-first planning | Diagnosis → scoped approach |
| KB stabilization | Full raw → processed → topics | Lightweight — processed note sufficient |
| ADR checkpoint | Mandatory evaluation | Conditional — required only if architectural |
| Regression check | Implicit in testing | Explicit mandatory phase |
| Completion signal | Milestone state sync | Feedback loop closure + TF-F status update |

---

# The TF-F### Issue Series

`TF-F###` issues are field-observed issues — gaps discovered through operational use rather than pre-planned.

Each TF-F issue carries a classification:

- `bug` — incorrect behavior or broken functionality
- `enhancement` — new or extended capability identified through use
- `architectural` — structural gap requiring lifecycle, event model, or domain model change
- `doctrine` — governance or principle gap
- `refactor` — internal restructuring needed
- `operational` — tooling or deployment gap

Classification determines which phases of the feedback loop are mandatory.

Architectural classification triggers mandatory ADR evaluation.

---

# Diagnosis as a First-Class Phase

Unlike milestone work — where requirements are pre-defined — feedback issues require root cause reasoning before any implementation approach is formed.

Diagnosis answers:
- What is the observable gap?
- What is causing it architecturally?
- What invariants are relevant?
- What is the minimum correct scope of change?
- What should explicitly remain out of scope?

Diagnosis is not optional. Implementing without diagnosis risks:
- scope creep
- treating symptoms rather than causes
- incorrect invariant assumptions
- unnecessary architectural change

---

# Feedback Loop Closure

Every feedback issue must be explicitly closed against its source.

This means:
- the fix is verified against the original observation
- the TF-F register is updated with resolution notes
- any remaining or follow-on gaps are captured as new TF-F issues
- the processed KB note references the original raw feedback source

Closure is not complete when the code is merged.

Closure is complete when the original operational gap is demonstrably resolved.

---

# ADR Implications

Not all feedback issues require ADRs.

ADR evaluation is mandatory when the fix involves:
- lifecycle state changes (e.g., introducing a new lifecycle stage)
- event model changes
- domain model changes
- invariant boundary changes
- new bounded contexts
- durable architectural decisions with future-facing implications

ADR evaluation is optional when the fix is:
- a UI/UX enhancement within existing architecture
- a bug fix with no architectural implications
- a configuration or ergonomic change

The TF-F classification field (`architectural`) is the trigger for mandatory ADR evaluation.

---

# KB Implications

Feedback issues produce lighter KB artifacts than milestone features.

Typical KB output for a feedback issue:

- one raw capture (diagnosis reasoning)
- one processed note (synthesis + resolution)
- entity or topic updates only if a new concept is stabilized

Full KB stabilization cycles (topics → entities → ontology) are reserved for feedback issues that surface genuinely new architectural concepts — such as a previously unnamed lifecycle state.

---

# Relationship to the Milestone Loop

The feedback loop does not replace the milestone loop.

When a feedback issue is significant enough to become a planned milestone feature (e.g., TF-F002 evolving into a full lifecycle state milestone), it transitions from the feedback loop into the milestone loop at that point.

The feedback loop governs the issue through triage, diagnosis, and initial resolution.

The milestone loop governs the issue if it is promoted into planned roadmap work.

---

# Final Principle

Feedback issues represent the system learning from itself.

Operational walkthroughs expose gaps that pre-planned architecture cannot fully anticipate.

The feedback workflow exists to ensure those gaps are:
- diagnosed correctly
- resolved at the right scope
- preserved as replayable operational knowledge
- closed against the original observation

Feedback is not noise. Feedback is the system revealing its own invariant boundaries under real use.
