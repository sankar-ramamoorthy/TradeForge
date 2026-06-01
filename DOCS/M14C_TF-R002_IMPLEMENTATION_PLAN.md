---
title: M14C TF-R002 Implementation Plan
type: design-plan
status: draft
created: 2026-05-28
updated: 2026-05-28
tags:
  - TradeForge
  - M14C
  - TF-R002
  - implementation-planning
  - Plan-Workspace
  - advisory-artifact
  - execution-boundary
  - replayability
sources:
  - "knowledge/raw/TF-R002 — Plan Workspace Import Mediation.md"
  - "knowledge/design/M14C_TF-R001_IMPLEMENTATION_PLAN.md"
  - "knowledge/processed/20260527-m14c-operator-cognition-bridge.md"
related_milestones:
  - M14C
related_issues:
  - TF-R001
  - TF-R002
  - M10AIS06
  - M10AIS07
related_adrs:
  - ADR-0001
  - ADR-0002
  - ADR-0004
  - ADR-0006
  - ADR-0033
  - ADR-0034
  - ADR-0035
  - ADR-0041
---

# M14C TF-R002 Implementation Plan

## Summary

`TF-R002` extends the successful `TF-R001` advisory import preview pattern from
Thesis authoring into Plan authoring.

The goal is not to import an executable plan. The goal is to mediate
plan-adjacent advisory rationale into the operator-owned Plan Development
workflow while preserving lifecycle authority, replayability, and strict
execution boundaries.

Plan imports are intentionally narrower and more guarded than thesis imports.
Imported material may assist entry, stop, target, and risk reasoning. It must
not populate prices, calculate sizing, approve a plan, arm a plan, create
orders, or authorize execution.

## Thin Slice

```text
plan_draft.v1 advisory artifact
    -> Plan Workspace import preview
    -> selective field acceptance
    -> operator edits and sizing confirmation
    -> manual Create Plan submission
    -> decision.plan_created with source provenance
    -> replay-visible advisory source context
```

## Scope

Included:

- deterministic `plan_draft.v1` mapping
- read-only plan import preview over advisory artifacts
- optional local markdown scan extension if it can reuse the TF-R001 path
- field-level acceptance for:
  - entry rationale
  - stop rationale
  - target rationale
  - risk notes
- operator edit tracking where feasible
- manual `Create Plan` submission through the existing lifecycle endpoint
- provenance carried on the resulting `decision.plan_created` event payload
- replay-visible advisory source context

Excluded:

- automatic price population
- automatic sizing
- broker integration
- order ticket generation
- plan approval
- plan arming
- execution authorization
- arbitrary AI parsing
- background watchers
- new canonical field-acceptance events
- universal import framework

## Schema Direction

Initial `plan_draft.v1` should be narrow and explicit.

Conceptual mapped field shape:

```yaml
artifact_type: plan_draft
schema_version: 1
symbol: ATKR
decision_id: optional-existing-decision-id
source:
  system: claude
  generated_at: 2026-05-28T00:00:00Z
plan:
  entry_rationale: >
    Why entry would be considered if conditions align.
  stop_rationale: >
    Why the invalidation or stop area matters.
  target_rationale: >
    Why the target area or exit logic matters.
  risk_notes:
    - Risk note requiring operator validation.
```

Prohibited mapped authority:

- exact broker order instructions
- account quantity
- position size
- calculated dollar risk
- approval decision
- arm/trigger authorization
- buy/sell command language as authoritative instruction

If such material appears in markdown prose, the deterministic mapper should not
turn it into lifecycle fields. It may be ignored, rejected, or shown only as
source text if the implementation can preserve clear advisory labeling.

## Integration Points

### Advisory Import Read Model

Add a plan import read path analogous to TF-R001:

```text
existing advisory artifact store
    -> filter persona/workspace/decision/symbol
    -> require artifact_role == plan_draft
    -> require schema_version == plan_draft.v1
    -> expose mapped fields and advisory authority flags
```

The read path is non-mutating. It must not append events.

### Local Scan

If implementation extends the TF-R001 local scan endpoint, the scan should
remain on-demand only and should ingest matching plan markdown as advisory
artifacts.

The scan must not:

- watch the filesystem
- create lifecycle events
- infer arbitrary plan fields from prose
- move into broker or pricing concerns

### Plan Development Modal

The Plan Development modal should gain an import preview panel only inside the
manual Plan authoring workflow.

Required UX distinctions:

- imported source material is advisory
- accepted draft text is not canonical
- edited text is operator-owned draft material
- only Create Plan submission creates lifecycle truth
- sizing remains operator-entered or explicitly operator-confirmed

Conflict handling can follow TF-R001:

- append
- replace
- reject
- leave unchanged

## Provenance Model

Minimum submitted provenance:

- source advisory artifact ID
- artifact role and schema version
- capture origin/source system where available
- accepted fields
- rejected fields where available
- edited-after-import indicators where feasible
- created plan lifecycle event reference through normal event metadata

Suggested payload location:

```text
decision.plan_created.payload.m14c_import_provenance
```

The canonical plan remains the structured `plan` payload created by the
operator. Import provenance explains source influence; it is not execution
authority.

## Event Impact

No new canonical event type is planned.

Canonical:

- `decision.plan_created`

Non-canonical:

- plan import previews
- accepted draft fields before submission
- source advisory artifact content
- advisory risk notes before explicit operator submission

Existing advisory capture semantics from M12 remain valid for durable advisory
artifact existence. TF-R002 should not introduce a second advisory persistence
system.

## Lifecycle Impact

TF-R002 operates only at the Thesis -> Plan authoring boundary.

It must not affect:

- Idea -> Thesis
- Plan -> Approval
- Approval -> Armed or Execution
- broker execution
- position creation
- review completion

Plan import preview cannot advance lifecycle state. Manual Create Plan
submission remains the only transition path.

## Replay Impact

Replay should answer:

- Which advisory artifact influenced this plan?
- Which plan-adjacent fields were accepted?
- Which accepted fields were edited?
- Did sizing remain operator-entered or operator-confirmed?
- Which `decision.plan_created` event resulted?

Replay must not imply:

- the advisory artifact approved the plan
- imported rationale authorized execution
- imported risk notes calculated position size
- broker orders existed because an import existed

## Affected Runtime Areas

Expected files and modules:

- `src/app/api/routes.py`
- advisory artifact read-model helpers already touched by TF-R001
- lifecycle create-plan request/response models
- `frontend/src/api/runtime.ts`
- `frontend/src/workspaces/PlanDevelopmentModal.tsx`
- `frontend/src/workspaces/PlanReviewWorkspace.tsx`
- `frontend/src/workspaces/ReplayWorkspace.tsx`
- backend tests for advisory artifacts and create-plan workflow
- frontend typecheck/build

The exact module split should follow the final TF-R001 implementation shape.

## Validation Against Invariants

- Human Decision Sovereignty: preserved because the operator must select,
  edit, and submit the plan.
- Event Ledger Canonical Truth: preserved because only
  `decision.plan_created` creates canonical plan state.
- Lifecycle Authority: preserved because import preview is read-only and
  lifecycle transition remains gated by `create-plan`.
- AI Advisory Boundary: preserved because imported artifacts remain advisory.
- Derived State Must Remain Distinguishable: preserved through advisory labels,
  import provenance, and replay wording.
- Replayability: preserved by storing source provenance on the lifecycle event
  and avoiding live external dependencies.
- Workspaces Are Operational Environments: preserved by embedding mediation in
  the Plan authoring workflow rather than creating detached dashboard controls.

## Implementation Sequence

1. Confirm TF-R001 route, metadata, provenance, and frontend state shapes.
2. Define deterministic `plan_draft.v1` mapped fields and rejection rules.
3. Add backend plan import listing and optional local scan support.
4. Extend create-plan validation to accept optional provenance and validate
   source advisory artifact IDs.
5. Add Plan Development import preview controls.
6. Preserve import provenance on manual plan submission.
7. Extend replay display for plan import provenance.
8. Add targeted backend tests.
9. Run frontend typecheck/build and `git diff --check`.
10. Update operator documentation after manual workflow validation.

## Testing Plan

Backend:

- plan import listing filters by persona, workspace, decision, symbol, role,
  and schema version
- read endpoint does not append events
- unsupported mapped fields are ignored or rejected
- missing source advisory artifact IDs fail create-plan with 422
- create-plan accepts valid import provenance and emits normal
  `decision.plan_created`
- import preview cannot approve, arm, execute, or create broker intent

Frontend:

- Plan Development modal renders advisory import preview
- accept/reject/edit flow preserves local draft state
- sizing field is not auto-filled from imported advisory material
- manual Create Plan remains the only submit action
- typecheck and production build pass

Replay:

- plan import provenance is visible on plan events
- replay labels advisory source context without execution-authority wording

## ADR Checkpoint

No new ADR is required if TF-R002 remains a narrow extension of:

- ADR-0034 for structured plan authoring
- ADR-0041 for durable non-canonical advisory artifacts
- ADR-0035 for replay rendering from event payloads

Prepare a new ADR only if implementation introduces a reusable import mediation
architecture, new canonical import events, or a durable cross-workspace
selective promotion model.
