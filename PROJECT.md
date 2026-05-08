# TradeForge — Project State

## Purpose

This file defines the current focus of development.

It is the "working memory" of the system.

---

# Current Phase

Phase: System Foundation & Vertical Slice Design

We are currently building:

- core architecture definition
- event-driven foundation
- decision lifecycle engine
- workspace model
- scenario engine scaffolding

---

# Current Priority

1. Finalize architecture + invariants (DONE IN PROGRESS)
2. Define ADR structure
3. Design first vertical slice:
   - Trade Idea → Thesis → Plan → Execution → Event → Replay

---

# Immediate Next Steps

## 1. ADR System Bootstrapping
- Event Sourcing core decision
- Lifecycle engine decision
- Workspace projection model

## 2. First Vertical Slice Design
Define full flow:

```
Idea creation
→ scenario generation
→ ranking
→ lifecycle progression
→ event emission
→ workspace update
→ replay capability
```

---

# Not in Scope (for now)

- broker integration
- live trading execution
- ML model training
- advanced UI polish
- performance optimization

---

# Active Focus Principle

We are not building features.

We are building:

> a structured decision-making system under uncertainty

---

# Success Criteria (Current Phase)

- lifecycle correctness enforced
- event sourcing fully consistent
- workspace derivation works
- replay is possible end-to-end
- no architectural drift between layers

---

# Final Note

Every feature must serve decision clarity, not complexity.