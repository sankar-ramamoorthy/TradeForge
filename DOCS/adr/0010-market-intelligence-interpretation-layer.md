# ADR 0010: Market Intelligence Interpretation Layer

## Status
Accepted

## Context
TradeForge needs market context to support situational awareness, scenario discovery, decision formation, exposure review, and reflection. Raw market data alone is not sufficient; operators need interpreted context such as regimes, macro conditions, volatility conditions, breadth conditions, thematic narratives, and playbook activation conditions.

At the same time, market interpretation is not canonical truth and does not produce decisions. If Market Intelligence directly generated trades, mutated workflows, or became authoritative state, it would violate event sourcing and lifecycle boundaries.

## Decision
TradeForge will use a Market Intelligence Layer to produce interpreted situational context from market observations and event-derived system context.

The Market Intelligence Layer may:

- interpret raw market observations into contextual understanding
- identify market regimes and conditions
- summarize macro and micro environments
- surface volatility, breadth, thematic, and playbook-relevant context
- condition scenario discovery
- support workspace briefing surfaces
- preserve uncertainty and conflicting signals

The Market Intelligence Layer must not:

- generate trade decisions
- execute trades
- mutate workflow state
- own lifecycle transitions
- define canonical truth
- bypass persona context
- hide uncertainty
- directly authorize scenario promotion into execution

Market events record observed market facts. Market Intelligence outputs are interpreted context and must remain separable from those facts. Persona context may shape interpretation weighting, but it does not make interpretation canonical.

## Rationale
TradeForge is designed to improve decision-making under uncertainty. Market Intelligence helps operators understand what is happening and why it may matter before any action is considered.

Separating market observations from market interpretations protects event integrity. It allows the system to preserve raw facts while also producing useful contextual views for scenarios, workspaces, and reviews.

Keeping Market Intelligence non-authoritative preserves the Decision Lifecycle Engine as the only workflow authority and keeps Scenario Discovery advisory.

## Alternatives Considered
Raw-data-only market handling was rejected because TradeForge needs interpreted situational context, not just data ingestion.

Market Intelligence as a signal generator was rejected because interpreted context is not a trade signal or execution instruction.

Market Intelligence owning lifecycle transitions was rejected because only the Decision Lifecycle Engine owns workflow state.

Market Intelligence as canonical truth was rejected because interpretations are derived or inferred, while canonical truth resides in events.

Persona-independent interpretation was rejected because TradeForge is persona-driven and market context must be weighted through persona context where applicable.

## Consequences
Market Intelligence outputs must be clearly distinguishable from canonical market observation events.

Scenario Discovery may consume Market Intelligence, but scenarios remain advisory hypotheses.

Workspace briefing surfaces may present Market Intelligence context, but the workspace remains a projection and not a state owner.

Review and replay must be able to reconstruct or reference the historical market context available at the time.

Implementation must preserve uncertainty, provenance where practical, persona-aware interpretation, and strict separation from lifecycle and execution authority.
