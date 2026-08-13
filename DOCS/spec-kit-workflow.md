# Spec Kit Workflow

## Purpose

GitHub Spec Kit is adopted in TradeForge as prospective planning
infrastructure. It preserves feature specifications, clarifications, technical
plans, and task breakdowns before implementation starts.

Spec Kit does not replace TradeForge doctrine, ADRs, the runtime issue
register, or milestone evidence.

## Authority

Spec Kit artifacts sit below existing project authority:

```text
Knowledge Base invariants and doctrine
-> accepted ADRs
-> runtime issue register and milestone roadmap
-> runtime architecture documentation
-> Spec Kit constitution
-> feature specs, plans, and tasks
-> implementation
```

If a spec conflicts with a higher authority, update the spec or open the
appropriate ADR/governance work before coding.

## Installed Shape

Spec Kit was initialized with:

```text
specify version: 0.15.1
integration: codex
script type: powershell
skills: enabled
```

Tracked project files include:

```text
.specify/
.agents/skills/speckit-*/
```

Feature artifacts belong under:

```text
specs/
```

## Workflow

Use Spec Kit for major features and meaningful defect families:

```text
registered issue
-> $speckit-specify
-> $speckit-clarify when ambiguity remains
-> $speckit-plan
-> $speckit-tasks
-> implementation
-> tests and milestone evidence
```

Small Tier B documentation, copy, or styling changes may remain on the existing
issue-first path when the issue register clearly bounds scope and validation.

## First Trial

The first prospective Spec Kit trial is:

```text
001-execution-position-integrity
```

It is tied to:

- `TF-F086`: Position Open Transition Must Capture Actual Execution Details
- `TF-F087`: Completed Review Must Not Imply Position Closed Without Close Event

Do not implement those issues as part of Spec Kit adoption. Run them through
specification, clarification, planning, and task generation first.

## Local Commands

Check the installed CLI:

```powershell
specify version
specify check
```

Create the next feature spec from the TradeForge repo root:

```text
$speckit-specify Record actual execution details before deriving an open position, and prevent completed review from implying a closed position without close evidence.
```

Then continue with:

```text
$speckit-clarify
$speckit-plan
$speckit-tasks
```
