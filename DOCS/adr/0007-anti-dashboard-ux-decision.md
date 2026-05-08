# ADR 0007: Anti-Dashboard UX Decision

## Status
Accepted

## Context
TradeForge UX is part of the architecture because interface structure shapes decision quality, situational awareness, cognitive load, workflow continuity, and review behavior.

The system is workflow-centric and persona-driven. It is not a generic dashboard, CRUD application, data feed, or navigation-heavy analytics tool.

If TradeForge were designed around dashboards, it would encourage fragmented attention, disconnected data views, and action without sufficient context. That would weaken the workspace model and lifecycle discipline.

## Decision
TradeForge rejects dashboard-centric UX as the primary interaction model.

The primary UX unit is the Persona Workspace: a persona-scoped operational decision environment. UI surfaces are projections into that workspace and must support cognition, workflow continuity, and explicit decision responsibility.

TradeForge UX must prioritize:

- context before action
- workflow continuity
- decision-centric surfaces
- persona-scoped interpretation
- active risk and exposure awareness
- visible uncertainty
- reflection and review
- relevance over maximum information density

The canonical workspace surfaces are:

- Briefing Surface for situational awareness
- Opportunity Surface for scenario candidates
- Exposure Surface for active commitments and risk
- Decision Queue for required lifecycle actions
- Review Surface for replay, evaluation, and learning

Navigation is secondary to cognition. UI must not treat workspaces as tabs, pages, or dashboards. Actions must be presented only after sufficient context is established.

## Rationale
TradeForge exists to improve disciplined decision-making under uncertainty. Dashboard-centric interfaces optimize for displaying data, while TradeForge must optimize for understanding, responsibility, and workflow integrity.

Persona Workspaces help preserve the thread of a decision over time. Decision surfaces keep the operator oriented around what is happening, why it matters, what needs attention, what exposure exists, and what can be learned.

Rejecting dashboard-first design also protects the event and lifecycle architecture. UI surfaces remain projections and cannot silently become state owners or workflow authorities.

## Alternatives Considered
Dashboard-first UX was rejected because it makes the system data-centric rather than decision-centric.

Navigation-first UX was rejected because it fragments operational cognition and encourages browsing rather than workflow execution.

CRUD entity screens as the primary UX were rejected because TradeForge is not an entity-management application.

Raw feed interfaces were rejected because they maximize information volume instead of interpretability and relevance.

AI-chat-as-primary-interface was rejected because AI may assist context, but it cannot replace decision surfaces or lifecycle controls.

## Consequences
UI design must begin from workspace cognition and decision workflow, not from dashboards or generic pages.

All user-facing surfaces must preserve the distinction between canonical facts, derived projections, inferred interpretations, and AI advisory content.

Actions must remain tied to lifecycle context and must not appear as detached controls.

Information density should be adaptive and relevance-driven.

Review and reflection remain first-class UX surfaces, not secondary analytics.
