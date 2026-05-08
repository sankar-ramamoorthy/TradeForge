# ADR 0009: Persona Interpretation Model

## Status
Accepted

## Context
TradeForge is persona-driven. A Persona is a behavioral and cognitive mode that defines how the system interprets information, prioritizes decisions, ranks scenarios, frames risk, and structures workflow emphasis.

Personas are not users, user profiles, permissions, trading moods, UI preferences, or account identities. If personas were treated as mutable user preferences or execution authorities, they would destabilize replay and violate lifecycle authority.

## Decision
TradeForge will model Personas as stable interpretation and prioritization contexts.

Personas may influence:

- market interpretation weighting
- scenario generation bias
- scenario ranking and thresholds
- risk framing
- workflow urgency and queue prioritization
- approval strictness
- workspace emphasis
- review interpretation lens

Personas must not:

- execute trades
- own event authority
- mutate canonical state directly
- bypass lifecycle rules
- approve plans autonomously
- replace the Decision Lifecycle Engine
- switch implicitly during active workflows

A Persona must be explicitly activated in workspace context. Persona context must remain consistent across workspace sessions, decision cycles, replay sessions, and review analysis.

Persona evolution must be versioned so historical replay can preserve the persona state and interpretation context that existed at the time.

## Rationale
Personas encode how decisions are made, not who is making them. They allow TradeForge to adapt interpretation and prioritization without becoming globally uniform or generic.

Keeping personas interpretive preserves clear authority boundaries. Personas can shape what matters and how strongly it is weighted, but facts still come from events and lifecycle transitions still come from the Decision Lifecycle Engine.

Versioned persona context also protects replay. Historical decisions must be interpreted through the persona state that existed when the workflow occurred, not through a later changed persona.

## Alternatives Considered
User profiles as personas were rejected because users are identities, while personas are decision behavior models.

UI preferences as personas were rejected because personas are architectural interpretation models, not interface settings.

Implicit persona switching was rejected because it would destabilize workflow context and replay.

Persona-owned execution authority was rejected because personas influence interpretation only and must not execute trades or approve decisions.

Mutable-in-hindsight personas were rejected because historical replay must preserve original interpretation context.

## Consequences
All operational workflows must carry persona context where applicable.

Workspace behavior, scenario ranking, market interpretation, decision queue emphasis, and review framing may vary by persona.

Persona changes must be explicit, versioned, and replay-compatible.

Personas must remain separate from users, permissions, UI preferences, and execution authority.

Implementations must preserve persona influence without allowing personas to mutate canonical state or bypass lifecycle controls.
