# TradeForge — System Invariants

## Purpose

This document defines non-negotiable truths about the TradeForge system.

If any invariant is violated, the system design is considered invalid.

---

# 1. Event Sourcing Invariant

All system state MUST be derived from events.

- No hidden state is allowed
- No direct state mutation is allowed
- Event store is the canonical source of truth

> If it is not an event, it does not exist.

---

# 2. Decision Lifecycle Invariant

All decisions MUST follow this lifecycle:

```
Idea → Thesis → Plan → Approval → Execution → Position → Review
```

Rules:
- No stage can be skipped
- No stage can be merged
- No direct Idea → Position transitions

---

# 3. Workspace Invariant

Workspaces are:

- derived projections of event history
- not stored dashboards
- not independent state holders

Workspaces MUST always be reconstructable.

---

# 4. Persona Invariant

Personas:

- influence interpretation only
- do NOT modify system state
- do NOT bypass lifecycle rules

---

# 5. AI Authority Invariant

AI systems are strictly advisory.

AI MAY:
- rank scenarios
- summarize state
- cluster information
- suggest interpretations

AI MUST NOT:
- execute trades
- mutate event store
- override lifecycle engine
- bypass deterministic rules

---

# 6. Scenario Invariant

Scenarios are:

- hypotheses about future states
- not trade signals
- not execution instructions

Scenarios MUST be explicitly evaluated before any action.

---

# 7. Event Integrity Invariant

Events must:

- be immutable
- be append-only
- represent facts, not interpretations

Invalid event types:
- "predictions"
- "assumptions"
- "suggestions"

---

# 8. Replay Invariant

The system MUST support full replayability:

- any state can be reconstructed from events
- no reliance on external live APIs for truth
- deterministic reconstruction required

---

# 9. Layer Separation Invariant

Strict separation:

- domain = pure logic
- services = orchestration only
- infrastructure = external systems only
- app = entrypoints only

No cross-layer contamination allowed.

---

# 10. Architectural Drift Invariant

Any change that:
- breaks event sourcing
- breaks lifecycle rules
- breaks workspace derivation

MUST be rejected or rewritten via ADR.

---

# Final Principle

TradeForge correctness is defined by invariants, not implementation.