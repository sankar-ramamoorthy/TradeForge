# ADR 0013: Operational Attention Model

## Status
Accepted

## Context
The MVP UI clarified that TradeForge is not centered on market movement. It is centered on what requires thoughtful human attention: pending decisions, risk, review obligations, workflow violations, thesis changes, and active exposure.

Without an explicit attention model, the Operating Workspace can drift into dashboard sprawl or ticker-first presentation.

## Decision
TradeForge will model operational attention as derived queue state, not canonical truth.

Operational attention may include:

- decisions awaiting review or approval
- theses needing revision
- plans awaiting conditions
- active positions requiring review
- risk or rule violations
- overdue review artifacts
- relevant context changes

Attention queues are derived from events, lifecycle state, deterministic rules, persona context, and workspace projection logic.

Attention queues do not authorize execution, approve plans, or mutate lifecycle state.

## Rationale
The system should answer what matters now before presenting actions. This supports context-before-action UX, human decision sovereignty, and replayable workflow discipline.

## Consequences
MVP workspaces must organize attention by workflow state and responsibility rather than by ticker movement alone.

Queue items must explain why attention is required and preserve references to source events or derived inputs.

AI may later help summarize attention, but it must not own queue authority.
