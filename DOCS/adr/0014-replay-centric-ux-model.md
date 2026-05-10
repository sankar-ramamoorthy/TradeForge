# ADR 0014: Replay-Centric UX Model

## Status
Accepted

## Context
Replay is a core TradeForge invariant and product differentiator. The MVP workspace model clarified that replay is not a report, trade history page, backtest, or screenshot timeline. It is cognitive reconstruction.

If replay UX is treated as an analytics feature, the system will fail to preserve what the operator believed, what context existed, what changed, and how decisions evolved.

## Decision
TradeForge UX will treat replay as a first-class interaction model.

Replay surfaces must reconstruct:

- lifecycle sequence
- event-backed workflow transitions
- rule evaluations
- execution actions
- notes and review artifacts
- historical market/context snapshots where available
- thesis evolution and decision-relevant changes

Replay UI consumes deterministic replay projections. It must not depend on live APIs, current UI state, current AI output, or mutable projections as truth.

Replay narratives, if present, must remain evidence-linked and advisory.

## Rationale
Replay is how TradeForge preserves cognitive memory. It supports review, behavioral learning, decision quality analysis, and long-term adaptation.

A replay-centric UX also acts as an architecture test: if a workflow cannot be replayed, it likely contains hidden state or unclear authority.

## Consequences
M5 must implement replay/projector foundations before workspace UI productization.

Replay Timeline becomes a core interaction pattern.

Review Workspace must link back to replay moments rather than only summarizing outcome.
