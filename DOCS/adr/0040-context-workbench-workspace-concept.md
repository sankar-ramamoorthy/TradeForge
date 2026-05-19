---
title: ADR-0040 - Context Workbench Workspace Concept
status: accepted
date: 2026-05-17
milestone: M10E
deciders: [TradeForge architecture]
---

# ADR-0040 - Context Workbench Workspace Concept

## Context

The Opportunity Workspace currently carries setup evaluation, advisory context
inspection, provider visibility, and early research pressure. These are related
but not identical operator tasks. TradeForge already recognizes Research
Workspace semantics canonically, but the runtime lacks a concrete workspace
concept dedicated to gathering and interpreting context before thesis formation.

## Decision

TradeForge will define a dedicated **Context Workbench** workspace concept.

Its operational question is:

> What do I need to know about this instrument before deciding how to interpret it?

The Context Workbench will own:

- advisory context acquisition
- retrieval-state visibility
- provider-attempt transparency
- inspection of relevant context families
- operator-readable interpretation of acquired context
- selective handoff of relevant advisory context into later opportunity/thesis work

It will not own:

- lifecycle transitions
- thesis authoring
- trade planning
- execution actions
- canonical event truth

## Rationale

Opportunity evaluation asks whether a setup deserves development. Research
acquisition asks what the operator should know about the instrument. Combining
them indefinitely overloads the Opportunity Workspace and obscures workflow
meaning. A dedicated Context Workbench preserves workspace distinctness while
giving `M10E` a coherent home for context acquisition.

## Consequences

- Workspace architecture gains a concrete research-oriented workspace concept.
- Opportunity Workspace should eventually consume selected context rather than
  own all acquisition mechanics.
- `TF-F032`, `TF-F033`, `TF-F034`, and `TF-F041` should design against this
  workspace boundary.
- Runtime implementation is deferred to later bounded issues.

