# ADR 0022: Authentication And Operational Identity

## Status

Accepted

## Context

TradeForge M7 needs a minimal session model before the MVP workspaces become
operational. The risk is conflating a user account, a runtime session, and a
Persona. That would violate the persona interpretation model and weaken replay,
because historical decisions must preserve the persona context that shaped
interpretation at the time.

TF-0034 does not introduce a full multi-user authorization system. It introduces
the runtime boundary needed to keep identity, session continuity, and persona
activation distinct.

## Decision

TradeForge will model operational identity through three separate concepts:

- User identity: who is using the runtime.
- Runtime session: the current application continuity context.
- Active workspace context: the explicitly selected persona, persona version,
  workspace, workflow, and decision focus.

The session model may provide defaults for workspace continuity, but it must not
become canonical event truth, lifecycle authority, persona semantics, or a
permission system. Persona activation remains explicit inside the active
workspace context and is not inferred from the user identity.

The M7 implementation will expose a read-only local session endpoint through the
FastAPI boundary. Later authentication work may replace the provider, but it
must preserve this separation.

## Consequences

- Frontend workspace context can initialize from the session boundary.
- User/session identity remains visibly separate from Persona.
- Session reads do not append events or mutate lifecycle state.
- Replay remains event-backed and does not depend on mutable browser session
  state.
- Full authorization, credential handling, and multi-user policy are deferred.

## Invariants Preserved

- Persona: a persona remains a decision behavior model, not a user.
- Workspace: session context supports workspace continuity without owning
  workspace truth.
- Replay: historical reconstruction remains event-backed.
- Human Decision Sovereignty: session identity does not authorize lifecycle
  decisions.

## Rejected Alternatives

### Treat user profile as persona

Rejected because user identity and persona interpretation have different
semantic roles.

### Store active workspace truth in browser state

Rejected because browser/session state is mutable presentation state, not
canonical truth.

### Implement full authorization in M7

Rejected because TF-0034 only needs the boundary required for MVP workspace
continuity. Full multi-user authorization remains out of scope.
