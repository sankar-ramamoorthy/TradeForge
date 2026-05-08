# ADR 0006: AI Advisory Boundary Model

## Status
Accepted

## Context
TradeForge may use AI to summarize context, rank scenarios, cluster information, explain uncertainty, highlight anomalies, and assist review. These capabilities can improve situational awareness and reduce cognitive load.

However, TradeForge is not an autonomous trading system. Human operators retain decision sovereignty, the Event Ledger remains canonical truth, and the Decision Lifecycle Engine remains the only lifecycle authority.

Without a strict AI boundary, AI output could be mistaken for canonical truth, execution authority, lifecycle approval, or deterministic rule evaluation.

## Decision
AI systems in TradeForge are advisory only.

AI may:

- summarize market and workspace context
- rank or cluster scenarios
- suggest interpretations
- highlight anomalies and risks
- assist with review reconstruction
- propose candidate actions for human evaluation
- explain uncertainty where practical

AI must not:

- execute trades
- approve plans
- mutate lifecycle state
- write immutable ledger events directly
- override deterministic lifecycle rules
- bypass the Decision Lifecycle Engine
- define workspace state
- conceal uncertainty or provenance
- fabricate historical events

AI-generated outputs are advisory artifacts. They may influence interpretation, prioritization, or review, but they are not canonical truth. If an AI suggestion becomes part of a workflow, it must pass through deterministic system layers and human-controlled lifecycle gates before any canonical event is recorded.

## Rationale
AI is useful as a context amplifier, but it is not a system controller. TradeForge exists to improve disciplined human decision-making under uncertainty, not to replace operator judgment.

The advisory boundary protects event integrity, replayability, lifecycle authority, and human decision sovereignty. It also keeps AI outputs accountable by requiring provenance and by separating suggestions from facts.

This design allows AI to improve perception and review while preventing it from becoming an unreviewable source of action.

## Alternatives Considered
Autonomous AI trading was rejected because it violates human decision sovereignty and the AI advisory invariant.

AI-written canonical events were rejected because canonical truth must come from deterministic system actions or human-controlled workflows.

AI-approved lifecycle transitions were rejected because only the Decision Lifecycle Engine may validate and advance lifecycle state.

AI-defined workspace state was rejected because workspaces are projections over event-derived and deterministic context.

Opaque AI recommendations were rejected because uncertainty and provenance must remain visible where practical.

## Consequences
All AI integrations must be designed as advisory components.

AI output must remain distinguishable from canonical state, derived state, and inferred state.

Any AI-assisted path to action must route through the Decision Lifecycle Engine and preserve human approval.

Review and replay must not depend on current AI output for historical truth.

AI features may improve ranking, summarization, and review, but they may not create hidden authority or bypass deterministic controls.
