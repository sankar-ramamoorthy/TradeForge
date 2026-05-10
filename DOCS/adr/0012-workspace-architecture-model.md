# ADR 0012: Workspace Architecture Model

## Status
Accepted

## Context
TradeForge has clarified from a backend-semantic system into a workspace-centric operational cognition system. Existing ADRs already establish event truth, lifecycle authority, workspace projections, anti-dashboard UX, replay, and persona interpretation.

The next risk is treating MVP workspaces as pages, screens, dashboards, or React routes. That would collapse the distinction between operational cognition and UI presentation.

## Decision
TradeForge will model MVP workspaces as operational cognition environments expressed through derived workspace projections and UI surfaces.

The MVP workspace set is:

- Operating Workspace
- Opportunity Workspace
- Plan Review Workspace
- Active Position Workspace
- Replay Workspace
- Review Workspace
- Market Context Workspace
- Playbooks / Doctrine Workspace

Workspace routes and screens are UI entrypoints only. They do not own canonical state, lifecycle transitions, or event truth.

Each workspace must define:

- operational question
- projection/read-model contract
- allowed lifecycle-aware actions
- replay requirements
- authority boundaries

## Rationale
TradeForge exists to improve disciplined decision-making under uncertainty. Workspaces are where cognition becomes operational: attention, context, risk, lifecycle state, replay, and review must remain coherent.

Explicit workspace architecture prevents dashboard drift and keeps React routing from becoming accidental domain architecture.

## Consequences
M4 must stay lean: define workspace routing and state contracts, not full UI implementation.

Workspace implementation must consume derived read models and route actions through lifecycle/API boundaries.

Design artifacts in the KB `design/` directory remain draft guidance until validated by ADRs, projection contracts, and runtime behavior.
