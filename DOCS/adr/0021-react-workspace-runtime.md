# ADR 0021: React Workspace Runtime

## Status

Accepted

## Context

M7 introduces the frontend runtime after the FastAPI boundary and workspace
projection APIs exist. The frontend must make TradeForge operationally usable
without becoming a competing owner of workspace semantics, lifecycle state,
event truth, replay behavior, or persona interpretation.

The immediate need is a React and TypeScript scaffold for later workspace
implementation. Routing, shared operational layout, session/auth behavior, and
full workspace screens remain separately tracked issues.

## Decision

TradeForge will use a Vite React TypeScript frontend under `frontend/`.

The React runtime is a presentation and interaction boundary over the FastAPI
runtime. It may request runtime status and derived workspace projections through
HTTP APIs. It must not import Python runtime internals, access event store
adapters, own lifecycle transitions, persist workspace truth in browser state,
or treat routes as workspace authority.

The initial scaffold may include a minimal workspace runtime shell to verify
that the application starts, TypeScript is enabled, and API boundary assumptions
are explicit. Full workspace routing belongs to TF-0032. Shared operational
layout primitives belong to TF-0033. Session and identity behavior belongs to
TF-0034.

## Consequences

- Frontend code has a dedicated runtime boundary.
- API consumption is explicit and isolated from event ledger internals.
- Workspaces remain persona-scoped operational environments, not React pages.
- The scaffold can run independently while later M7/M8 issues add real
  workspace behavior.

## Invariants Preserved

- Workspace: React surfaces project workspace state but do not define it.
- UX Is Architectural: the scaffold avoids dashboard-first composition.
- Event Sourcing: browser state is not canonical truth.
- Decision Lifecycle: lifecycle authority remains in domain/services/API.
- Replay: replay truth remains derived from event history, not client state.

## Rejected Alternatives

### Put React at the repository root

Rejected because frontend tooling should remain isolated from Python runtime
tooling and source layout.

### Build full workspace routing in the scaffold

Rejected because routing is scoped to TF-0032 and should be designed against
the accepted workspace runtime boundary.

### Let React consume event store data directly

Rejected because the frontend must consume API read models and lifecycle
service boundaries rather than canonical storage internals.
