# ADR 0005: Scenario Engine Architecture

## Status
Accepted

## Context
TradeForge uses Scenario Discovery to surface opportunities, risks, watchlist changes, anomalies, and candidate setups. A Scenario is a structured hypothesis about a potential market opportunity or risk.

Scenarios are useful because they focus attention and support decision formation, but they are not decisions, trades, positions, execution instructions, or canonical truth. If the scenario layer owned lifecycle state or execution authority, it would bypass the Decision Lifecycle Engine and violate human decision sovereignty.

## Decision
TradeForge will implement the Scenario Discovery Engine as an advisory candidate-generation and ranking layer.

The Scenario Discovery Engine may:

- generate scenarios from market intelligence and event-derived context
- rank opportunities and risks
- cluster signals into structured hypotheses
- identify anomalies and watchlist changes
- surface scenarios into workspace opportunity surfaces
- support promotion into human-controlled decision workflows

The Scenario Discovery Engine must not:

- own workflow state
- approve decisions
- execute trades
- create positions
- bypass lifecycle stages
- mutate lifecycle state
- write canonical decision or execution events directly
- become the source of truth for trade intent

Scenario events may record facts about scenario generation, ranking, invalidation, or watchlist promotion. Those events record advisory activity only. A scenario can inform a Trade Idea, but the lifecycle must still proceed through Idea, Thesis, Plan, Approval, Execution, Position, and Review.

## Rationale
Scenario Discovery improves operational awareness by turning interpreted market context into candidate hypotheses. It helps the operator see what may matter without making those hypotheses authoritative.

Keeping the scenario layer advisory preserves strict lifecycle boundaries. It ensures that a scenario must pass through human-controlled decision formation before it can affect execution.

This separation also improves replay and review. Historical analysis can distinguish between what the system surfaced, what the operator accepted, what was rejected, and what eventually became a decision.

## Alternatives Considered
Scenario-as-signal design was rejected because scenarios are hypotheses, not trade signals or execution instructions.

Scenario-to-execution workflows were rejected because they skip thesis formation, planning, approval, and human decision control.

Scenario-owned lifecycle state was rejected because the Decision Lifecycle Engine is the only lifecycle authority.

AI-driven autonomous scenario execution was rejected because AI and advisory engines may not execute trades or approve workflows.

Treating scenario rankings as canonical truth was rejected because rankings are derived or inferred interpretation, not facts.

## Consequences
Scenario outputs must be clearly labeled and handled as advisory hypotheses.

Workspace opportunity surfaces may show ranked scenarios, but those rankings do not authorize action.

Any path from scenario to action must enter the Decision Lifecycle Engine at the proper stage and remain event-backed.

Scenario history should remain replayable so reviews can compare surfaced hypotheses, operator decisions, and outcomes.

Implementation must preserve separation between Market Intelligence, Scenario Discovery, Decision Lifecycle, and Execution contexts.
