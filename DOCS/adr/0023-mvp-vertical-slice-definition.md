# ADR 0023: MVP Vertical Slice Definition

## Status
Accepted

## Context
Roadmap v2 defines TradeForge MVP v1 as a replayable discretionary cognition system, not an AI trader, broker replacement, charting platform, or dashboard product.

The team is pursuing a fast disciplined path. The main risk is allowing market intelligence, AI, behavioral intelligence, simulation, or polished UI breadth to enter MVP scope too early.

## Decision
TradeForge MVP v1 is the first usable operational workflow that supports:

```text
Idea
-> Thesis
-> Plan
-> Approval
-> Execution
-> Position
-> Replay
-> Review
```

The required MVP workspaces are:

- Operating Workspace
- Opportunity Workspace
- Plan Review Workspace
- Active Position Workspace
- Replay Workspace
- Review Workspace

MVP v1 requires durable persistence, API boundaries, workspace projections, replay, and review. It does not require live broker execution, autonomous AI, scenario intelligence, simulation, RL, or full market intelligence automation.

## Rationale
The MVP must prove disciplined workflow cognition and historical reconstructability. That is the smallest coherent product identity for TradeForge.

Defining the MVP this way protects the roadmap from attractive but downstream capabilities.

## Consequences
M4 through M8 are the MVP path.

Postgres, FastAPI, and React arrive in M7 after workspace contracts, replay/projector foundations, and persona workspace projections are defined.

M9 and later work is post-MVP unless explicitly pulled forward by a new decision.
