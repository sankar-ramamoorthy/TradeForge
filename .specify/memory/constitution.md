<!--
Sync Impact Report
Version change: none -> 1.0.0
Modified principles:
- Template placeholder principles -> TradeForge constitutional principles
Added sections:
- Runtime Authority Hierarchy
- Spec Kit Operating Rules
- Development Workflow And Quality Gates
Removed sections:
- Template placeholder sections
Follow-up TODOs:
- None
-->

# TradeForge Spec Kit Constitution

## Core Principles

### I. Existing TradeForge Doctrine Is Authoritative

Spec Kit artifacts MUST remain subordinate to the existing TradeForge truth
hierarchy: Knowledge Base doctrine and invariants, accepted ADRs, runtime issue
register entries, milestone roadmap, runtime documentation, and then code.
Specifications may clarify future work, but they MUST NOT silently redefine
TradeForge ontology, lifecycle semantics, event meaning, AI authority, replay
requirements, or cross-repository ownership.

### II. Event-Sourced Lifecycle Integrity Is Non-Negotiable

Every feature specification and plan MUST preserve the append-only Event Ledger
as canonical truth and the strict decision lifecycle:

```text
Idea -> Thesis -> Plan -> Approval -> Execution -> Position -> Review
```

Specs MUST distinguish planned intent, operator decisions, execution facts,
derived projections, and advisory interpretation. A specification that creates
or changes canonical state MUST identify the event facts, replay behavior, and
lifecycle authority impact before implementation tasks are accepted.

### III. Human Decision Sovereignty And Advisory Boundaries Hold

AI systems, market intelligence, Research Cockpit imports, provider outputs, and
generated Spec Kit artifacts are advisory unless explicitly accepted through
TradeForge-owned operator workflows. Specs MUST NOT grant AI, external
providers, background jobs, or sibling repositories authority to approve plans,
execute trades, mutate the Event Ledger, or bypass lifecycle controls.

### IV. Issue-First Governance Remains Required

Spec Kit does not replace the local issue register, milestones, ADRs, or PR
discipline. Every implementation feature MUST be tied to an authorized issue
with known milestone, scope, impacted layers, acceptance criteria, validation
plan, and branch. Spec Kit artifacts are prospective planning artifacts that
make issue work clearer; they do not authorize untracked code.

### V. Replayability, Provenance, And Validation Are Required

Material workflow behavior MUST be replayable from immutable historical facts.
Specs and plans MUST state how provenance, uncertainty, derived state, and
validation evidence will be preserved. Completion requires tests appropriate to
the affected surface and documented verification results; skipped validation
MUST be explicit with the reason.

## Runtime Authority Hierarchy

When Spec Kit artifacts conflict with existing project authority, resolve the
conflict in this order:

1. `../TradeForge-KnowledgeBase/INVARIANTS.md`
2. Canonical Knowledge Base ontology, doctrine, and runtime context map
3. Accepted runtime ADRs
4. `DOCS/ISSUE_REGISTER.md` and `DOCS/Milestone_Roadmap_v2.md`
5. Runtime architecture documentation
6. Spec Kit constitution
7. Feature `spec.md`, `plan.md`, `tasks.md`, and generated checklists
8. Runtime implementation

If a future spec needs to contradict a higher authority, it MUST stop and route
the change through the appropriate ADR, doctrine, or issue-governance process.

## Spec Kit Operating Rules

Spec Kit applies prospectively. Historical milestones and completed issues MUST
NOT be bulk-retrofitted into specs unless a future issue explicitly authorizes a
targeted migration.

Major features and meaningful defect families SHOULD use the full sequence:

```text
registered issue
-> $speckit-specify
-> $speckit-clarify when ambiguity remains
-> $speckit-plan
-> $speckit-tasks
-> implementation
-> tests and milestone evidence
```

Small Tier B changes may use the existing issue-first process without full Spec
Kit ceremony when the local issue register clearly bounds the files, acceptance
criteria, and validation.

Spec Kit feature directories live under `specs/` and MUST be named for the
prospective feature or defect family, not for completed historical work. The
first trial feature after this adoption is `001-execution-position-integrity`,
tied to `TF-F086` and `TF-F087`.

## Development Workflow And Quality Gates

Before implementation, agents MUST:

1. Confirm the active branch is not `main`.
2. Confirm the work is tied to an authorized runtime issue.
3. Load bounded semantic context from the Knowledge Base for the task category.
4. Check relevant ADRs and runtime documentation.
5. Complete the applicable Spec Kit phase for in-scope work.
6. Identify event, lifecycle, replay, AI advisory, and cross-repository impact.
7. Define validation commands before editing code.

Implementation tasks MUST remain scoped to the issue and spec. Pull requests
MUST summarize behavior changes, validation performed, residual risks, and any
deviations from the spec or constitution.

## Governance

This constitution governs Spec Kit usage inside the TradeForge runtime
repository only. It does not alter the independent governance of
`TradeForge-KnowledgeBase` or `TradeForge-ResearchCockpit`.

Amendments require a tracked governance issue, a focused branch, a clear
version bump, and an updated sync impact report. Versioning follows semantic
versioning:

- MAJOR: removes or redefines a constitutional principle or authority boundary.
- MINOR: adds a new principle, section, or materially expanded governance rule.
- PATCH: clarifies wording without changing governance meaning.

Compliance is checked during Spec Kit planning, task generation, code review,
and PR closeout. Existing TradeForge architecture remains authoritative where
this constitution is incomplete.

**Version**: 1.0.0 | **Ratified**: 2026-08-13 | **Last Amended**: 2026-08-13
