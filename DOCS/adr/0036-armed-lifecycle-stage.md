---
title: ADR-0036 — Armed Lifecycle Stage
status: accepted
date: 2026-05-15
milestone: TF-F002 (post-M10A feedback)
deciders: [TradeForge architecture]
---

# ADR-0036 — Armed Lifecycle Stage

## Context

The first operational walkthrough (M10A, 2026-05-14, SMH scenario) exposed a missing
lifecycle concept. After a plan is approved, the canonical flow compressed directly to
execution. But in real discretionary swing trading, approval typically means:

> "If the declared trigger conditions are met, I am authorized to execute."

Not:

> "I have already executed."

The SMH plan explicitly required a daily close above 585, rising volume, and continued
semiconductor breadth participation before entry. No lifecycle state existed to represent
"authorized and watching for trigger conditions." The operator was forced to either
record execution prematurely or abandon the flow.

This is recorded as TF-F002.

## Decision

A new mandatory lifecycle stage — **Armed** — is introduced between Approval and Execution.

New canonical lifecycle:

```text
Idea → Thesis → Plan → Approval → Armed → Execution → Position → Review
```

The Armed stage represents: the plan is authorized, trigger conditions have been
declared, and the operator is watching for those conditions to be satisfied before
committing to execution.

### New Event Type

`decision.plan_armed` is appended when the operator declares trigger conditions.

Payload must include:
- `trigger_conditions`: non-empty list of declared conditions (at least one required)
- `symbol`: ticker
- `revision_number`: 1 (first and only arm event per plan lifecycle)

This is a decision-domain event. The execution domain begins at `execution.order_submitted`.

### ARMED Is Mandatory

ARMED is not optional. The transition map changes from:

```
APPROVAL → EXECUTION
```

to:

```
APPROVAL → ARMED → EXECUTION
```

Rationale: real discretionary entries always have trigger conditions, even if they are
as simple as "execute at market open." Making ARMED mandatory enforces declaration of
those conditions and preserves the replayable record of why the entry was taken at
the specific moment it was.

An operator who wants immediate execution simply declares "Conditions already met —
executing now" as a trigger condition and immediately confirms execution.

### Stage Authority

The Armed stage does not represent partial execution. It represents:
- deliberate intent to execute
- declared trigger conditions
- the watching period before those conditions are confirmed

The lifecycle engine owns ARMED state authority, consistent with [[ADR-0002]].

### Endpoint

`POST /lifecycle/decisions/arm-plan` accepts trigger conditions and creates the
`decision.plan_armed` event via the lifecycle orchestration service.

`GET /lifecycle/decisions/{id}/arm` reads the trigger conditions for display.

## Rationale

ADR-0002 requires all lifecycle stages to be explicit, auditable, and event-backed.
The implicit "approval means I'll execute when I decide" gap created a lifecycle black
hole — the system could not replay what triggered the execution decision.

The Armed stage closes that gap. The trigger confirmation itself becomes a replayable
lifecycle event (`execution.order_submitted`), and the declared trigger conditions
are preserved in the `decision.plan_armed` event payload.

This preserves [[Replayability Is Foundational]]: a future replay can reconstruct
what conditions the operator declared before execution and compare them against
what actually happened in the market at that moment.

## Alternatives Considered

**Optional Armed stage (APPROVAL can go to ARMED or EXECUTION):** Rejected. The
current transition map is 1:1 per stage. Supporting multiple allowed next stages
requires a structural change to the transition validator. More importantly, making
ARMED optional removes the discipline — operators would skip it for "quick" trades,
which is precisely where trigger condition capture is most valuable.

**Approval-level trigger declaration (embed conditions in plan_approved payload):**
Rejected. The approval event confirms authorization of the plan as written. Trigger
conditions for execution timing are semantically distinct from plan authorization.
They deserve their own stage and event.

**ARMED → APPROVAL reversal (cancel arming):** Not included in this ADR. The operator
can handle changed conditions by recording execution as-is and capturing reasoning in
a review annotation. This may be revisited as a future TF-F issue.

## Consequences

- CANONICAL_LIFECYCLE_STAGES grows from 7 to 8 stages.
- ALLOWED_LIFECYCLE_TRANSITIONS changes: APPROVAL now advances to ARMED, ARMED advances to EXECUTION.
- All existing tests asserting on the 7-stage map must be updated.
- The Plan Review Workspace Approval-stage action changes from "Record Execution" to "Arm Plan."
- The Active Position Workspace gains Armed-state handling with trigger condition display.
- Replay reconstruction surfaces the declared trigger conditions alongside the execution moment.
- The LifecycleProgressStrip gains an 8th step.
