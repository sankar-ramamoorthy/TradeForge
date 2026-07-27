---
title: Runtime ↔ KB Development Workflow
type: architecture-doc
status: canonical
tags:
  - TradeForge
  - architecture
  - development-workflow
  - replayability
  - semantic-governance
  - knowledge-base
created: 2026-05-08
updated: 2026-07-27
related:
  - runtime-kb-development-loop
  - ADR
  - replayability
  - semantic-stabilization
  - ontology-governance
kb_canonical_playbook: >
  ../TradeForge-KnowledgeBase/playbooks/development/runtime-kb-development-loop.md
kb_related:
  - "[[ARCHITECTURE]]"
  - "[[EVENT_TAXONOMY]]"
  - "[[EXECUTION_CONTRACT]]"
  - "[[INVARIANTS]]"
  - "[[Replay Session]]"
  - "[[Decision Lifecycle]]"
---

# Runtime ↔ KB Development Workflow

## Purpose

This document explains the architectural reasoning behind the three-repository
TradeForge development workflow.

It describes:
- why the workflow exists
- why the Knowledge Base (KB) is separate from the runtime repository
- why the Research Cockpit is a bounded upstream producer rather than runtime
  authority
- how semantic stabilization occurs
- how replayability applies to development itself
- how architecture governance is enforced

This is NOT the canonical operational playbook.

The canonical workflow definition lives in:

```
../TradeForge-KnowledgeBase/playbooks/development/runtime-kb-development-loop.md
```

This document exists to explain the architectural intent of that workflow.

---

# Core Architectural Principle

TradeForge development is itself treated as a replayable cognition system.

The system is intentionally designed so future humans and future agents can reconstruct:

- why work occurred
- what architectural assumptions existed
- what semantic context informed implementation
- what tradeoffs were made
- what ontology decisions evolved
- what replay implications existed

This is fundamentally different from:
- generic software documentation
- ad hoc issue implementation
- feature-first development

TradeForge development prioritizes:
- replayability
- semantic consistency
- architecture integrity
- workflow discipline
- ontology stability

Correctness and reconstructability are considered more important than implementation speed.

---

# Why Three Repositories Exist

TradeForge intentionally separates:

## 1. Runtime Repository

Purpose:
- executable implementation
- lifecycle engine
- event systems
- projections
- replay systems
- integrations
- runtime workflows

The runtime repository answers:

> “How does the system execute?”

---

## 2. Knowledge Base Repository

Purpose:
- semantic stabilization
- ontology governance
- architecture doctrine
- workflow cognition
- prompts
- playbooks
- reusable reasoning systems
- replayable project memory

The KB answers:

> “Why does the system exist and what do concepts mean?”

---

## 3. Research Cockpit Repository

Purpose:
- upstream evidence and research production
- source provenance
- research history
- quality evaluation
- advisory submission production
- optional TradeForge-compatible projections

The Research Cockpit answers:

> "What source-backed advisory research can be produced upstream?"

Research Cockpit context is bounded. Activate it only for
research-production, advisory-handoff, import-boundary, or cross-repository
governance work.

The Research Cockpit does not own TradeForge lifecycle state, canonical Event
Ledger truth, approval, execution, or runtime implementation planning.

---

# Architectural Separation Principle

The runtime repository is optimized for:
- implementation
- execution
- bounded engineering work
- runtime correctness

The KB is optimized for:
- semantic continuity
- architectural memory
- replayable reasoning
- ontology stabilization
- workflow governance

The Research Cockpit is optimized for:
- evidence assembly
- provenance preservation
- local research history
- quality evaluation
- advisory producer contracts

This separation intentionally prevents:
- implementation drift
- ontology drift
- architecture erosion
- undocumented semantic evolution
- advisory producer context from becoming runtime authority

---

# Replayability Doctrine

Replayability applies to:
- trading workflows
- decision workflows
- architecture evolution
- development workflows

TradeForge development itself is treated as replayable operational cognition.

This means the system should support reconstruction of:
- implementation reasoning
- architectural decisions
- milestone evolution
- workflow assumptions
- semantic transitions
- ontology refinement

The workflow exists to preserve that continuity.

---

# Development as Progressive Stabilization

TradeForge development follows progressive semantic refinement.

Knowledge evolves through:

```text
raw discovery
    ↓
processed synthesis
    ↓
topic refinement
    ↓
canonical entity definition
    ↓
architectural stabilization
```

This mirrors the broader TradeForge architecture philosophy:
- explicit state transitions
- replayable evolution
- deterministic authority
- progressive refinement

---

# Why Raw Notes Exist

Raw notes preserve:
- unstable reasoning
- exploratory architecture
- implementation observations
- transient cognition
- unresolved tradeoffs

Raw notes are intentionally:
- non-canonical
- noisy
- disposable
- exploratory

Their purpose is preserving cognition before stabilization occurs.

This is important because:
- future architectural reasoning may depend on discarded alternatives
- ontology evolution must remain reconstructable
- implementation assumptions should not disappear silently

---

# Why Knowledge Processing Exists

Raw captures are processed because:
- uncontrolled raw knowledge creates semantic drift
- architecture concepts require stabilization
- ontology requires consistency
- terminology must remain canonical

Processing transforms:
- implementation observations
- exploratory notes
- architecture reasoning

into:
- stable semantic knowledge
- workflow doctrine
- ontology references
- reusable cognition structures

This processing step is mandatory.

---

# Why ADR Validation Exists

TradeForge treats architecture decisions as first-class artifacts.

ADRs exist to preserve:
- architectural rationale
- tradeoffs
- rejected alternatives
- future-facing implications

Missing ADRs create:
- hidden architecture drift
- unreplayable decisions
- semantic inconsistency
- future implementation ambiguity

Therefore:
- ADR evaluation occurs before implementation
- architecture reasoning precedes code generation

---

# Why Semantic Initialization Exists

TradeForge explicitly prohibits implementation without semantic initialization.

Before implementation work:
- architecture doctrine
- invariants
- glossary
- event taxonomy
- execution contract
- relevant skills

must be loaded first.

This exists to prevent:
- ontology drift
- lifecycle corruption
- inconsistent terminology
- architecture erosion
- hidden assumptions

TradeForge treats semantic context as an execution dependency.

---

# Why Operational State Synchronization Exists

Implementation is not considered complete until:
- milestone roadmap is updated
- issue register is updated
- implementation state matches operational tracking state

This rule exists because stale planning state creates:
- replay failures
- milestone ambiguity
- architectural confusion
- future planning corruption

Operational state documents are treated as authoritative planning systems.

---

# Why Milestone Transitions Are Manual

Milestone transitions are treated as architectural stabilization events.

TradeForge intentionally avoids:
- fully automated milestone transitions
- opaque merge workflows
- hidden stabilization boundaries

Milestone transitions are semantic checkpoints.

They often imply:
- architectural consolidation
- ontology stabilization
- replay checkpoints
- ADR review
- workflow stabilization

Correct stabilization is considered more important than automation throughput.

---

# KB Knowledge Architecture

The KB is NOT intended to behave like:
- static documentation
- disconnected notes
- linear specifications
- generic wiki pages

The KB is evolving toward:
- semantic graph structures
- replayable cognition systems
- reusable reasoning architectures
- long-term architectural memory

Key structures include:
- ontology
- workflows
- playbooks
- prompts
- skills
- entities
- topics

Together these form a reusable cognition framework for both humans and agents.

---

# AI Governance Implications

TradeForge development follows the same AI governance philosophy as the runtime system.

AI systems are:
- advisory
- assistive
- contextual
- bounded

AI systems are NOT:
- authoritative
- ontology owners
- lifecycle controllers
- canonical truth sources

Deterministic architectural doctrine remains canonical.

This principle applies equally to:
- runtime systems
- KB evolution
- implementation workflows

---

# Development Replayability

One of the primary goals of the workflow is preserving development replayability.

Future agents should be able to reconstruct:
- why a milestone evolved
- why an ADR was created
- what assumptions existed
- what semantic context governed implementation
- what concepts changed over time

TradeForge treats architecture evolution as part of the system memory itself.

---

# Relationship to the Runtime Architecture

This workflow directly supports the broader TradeForge architecture described in:

- `ARCHITECTURE.md`
- `EVENT_TAXONOMY.md`
- `INVARIANTS.md`
- `EXECUTION_CONTRACT.md`

Specifically:
- event sourcing philosophy
- replayability doctrine
- workflow-centric architecture
- deterministic authority
- semantic consistency
- bounded AI governance

The development workflow is intentionally aligned with those same principles.

---

# Relationship to the Canonical Playbook

This document explains:
- why the workflow exists
- what architectural problems it solves
- why stabilization matters

The canonical operational procedure lives in:

```
../TradeForge-KnowledgeBase/playbooks/development/runtime-kb-development-loop.md
```

Operational execution rules should be modified there.

This document should remain:
- explanatory
- architectural
- doctrine-oriented

---

# Final Principle

TradeForge development is designed to preserve:

- replayable reasoning
- semantic continuity
- ontology stability
- architectural memory
- workflow integrity

The three-repository workflow exists to ensure the system remains:
- explainable
- reconstructable
- governable
- semantically coherent
- resilient against architectural drift

Architecture is not treated as documentation.

Architecture is treated as durable operational cognition.
