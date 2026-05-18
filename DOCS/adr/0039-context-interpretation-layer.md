---
title: ADR-0039 - Context Interpretation Layer
status: accepted
date: 2026-05-17
milestone: M10E
deciders: [TradeForge architecture]
---

# ADR-0039 - Context Interpretation Layer

## Context

`ADR-0032` and `ADR-0038` define normalized external-data boundaries and typed
provider capabilities. The runtime can fetch advisory data, but normalized data
alone is not yet operator cognition. Current surfaces risk exposing payloads
directly and forcing the trader to perform all interpretation mentally.

## Decision

TradeForge will introduce a bounded **Context Interpretation Layer** between
normalized advisory provider outputs and workspace presentation.

The layer will:

- consume normalized advisory context artifacts
- produce operator-readable derived interpretations
- preserve provenance and uncertainty
- remain advisory and non-canonical
- be available to workspace surfaces and later advisory systems

The layer will not:

- write canonical events
- mutate lifecycle state
- execute trades
- hide underlying source artifacts
- collapse deterministic interpretation and future AI interpretation into one authority class

## Rationale

Provider normalization solves interoperability, not cognition. A discretionary
trader needs to understand what fetched context means for the current decision,
not only inspect payload fields. Keeping interpretation in an explicit bounded
layer prevents raw data dumps in UX while preserving the advisory boundary.

## Consequences

- Workspace surfaces may consume interpreted advisory context rather than only
  raw provider artifacts.
- Raw provider artifacts and interpreted outputs must remain distinguishable.
- Later AI advisory work may build on the same boundary, but AI-generated
  interpretation must remain separable from deterministic derived interpretation.
- `M10E` may design workflows and workspaces around both acquisition and
  interpretation without redefining canonical truth.

