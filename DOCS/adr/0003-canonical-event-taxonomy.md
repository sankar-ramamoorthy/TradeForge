# ADR 0003: Canonical Event Taxonomy

## Status
Accepted

## Context
TradeForge depends on event sourcing for canonical truth, lifecycle reconstruction, replayability, auditability, and workflow integrity. ADR 0001 establishes the Event Ledger as the source of truth, and ADR 0002 establishes the Decision Lifecycle Engine as the authority for workflow progression.

Those decisions require a stable taxonomy for events. Without a canonical event taxonomy, different subsystems could create overlapping event meanings, mix facts with interpretations, encode UI state as truth, or allow advisory systems to appear authoritative.

The taxonomy must preserve the TradeForge distinction between canonical state, derived state, inferred state, and advisory interpretation.

## Decision
TradeForge will use a canonical event taxonomy organized into bounded event domains:

```text
persona.*
workspace.*
market.*
scenario.*
decision.*
execution.*
review.*
system.*
```

Each domain defines a bounded event space and must preserve its authority boundary.

Persona events record facts about operator context and reasoning mode, such as persona creation, activation, deactivation, and versioned changes. Persona events may affect interpretation downstream, but personas do not execute trades or override lifecycle rules.

Workspace events record facts about persona-scoped operational environments, such as workspace creation, opening, closing, and context updates. Workspace events do not make workspaces canonical state holders; workspace surfaces remain projections over event history.

Market events record observed market facts, such as market data received, price updates, volume spikes, volatility regime changes, and macro events detected. Market events are observations, not trade decisions.

Scenario events record advisory scenario activity, such as scenarios generated, ranked, invalidated, or promoted to a watchlist. Scenario events represent hypotheses and attention-routing artifacts, not decisions, trade signals, or execution instructions.

Decision events record human workflow facts controlled by the Decision Lifecycle Engine, such as trade ideas created, theses created, plans created, plans approved or rejected, decisions queued, and decisions executed. Decision events are explicit, user-driven, lifecycle-controlled facts.

Execution events record interaction with external systems, such as orders submitted, modified, cancelled, fills received, positions opened, and positions closed. Execution events reflect external reality and execution feedback, not internal intent or lifecycle authorization.

Review events record reflection and learning artifacts, such as reviews started, reviews completed, outcomes evaluated, rule violations detected, and behavioral insights recorded. Review events are first-class workflow outputs.

System events record infrastructure and operational facts, such as system initialization, projection rebuilds, cache invalidation, and data sync completion. System events support observability and reconstruction but do not define domain semantics.

All events must be fact-first, immutable, timestamped, replayable, contextually grounded, and named in past tense with explicit action language. Conceptually, events must carry event type, timestamp, persona context, workspace context when applicable, entity references, structured payload, and provenance metadata.

Invalid event patterns include predictions, assumptions, suggestions, UI states, derived metrics, AI summaries, emotional labels, and interpretive quality judgments. These may exist as advisory or derived artifacts, but they are not canonical events unless represented as a fact that happened in the correct bounded event domain.

## Rationale
A canonical taxonomy prevents event meaning from drifting as the runtime grows. It gives every subsystem a clear place to record facts while preserving strict authority boundaries.

The taxonomy also supports deterministic replay. Rebuilding lifecycle state, workspace surfaces, exposure views, scenario history, and review artifacts requires event categories to be stable, explicit, and semantically narrow.

Separating market observations, scenario hypotheses, lifecycle decisions, execution feedback, and review artifacts prevents the system from confusing interpreted context with canonical truth. This keeps scenarios and AI advisory, keeps the lifecycle engine authoritative, and keeps workspaces reconstructable.

## Alternatives Considered
An unstructured event stream was rejected because it would allow terminology drift, inconsistent payload meanings, and ambiguous replay behavior.

A CRUD-derived event model was rejected because it would encode database operations rather than domain facts and workflow transitions.

A single generic event category was rejected because it would hide authority boundaries between personas, workspaces, market observations, scenarios, decisions, execution, review, and system operations.

Interpretive events such as bullish signals, confidence labels, quality scores, and AI conclusions were rejected because they are not facts. They are derived or inferred interpretations and must not become canonical truth.

UI events as domain truth were rejected because UI surfaces are projections and must not own canonical state or lifecycle progression.

Execution-only taxonomy was rejected because broker interaction is only one part of the decision lifecycle and cannot reconstruct operator intent, thesis formation, approval, review, or workspace context.

## Consequences
All new event types must be assigned to one canonical event domain and preserve that domain's authority boundary.

Event names must describe facts that happened, not interpretations of what those facts mean.

Lifecycle-critical events must remain under decision and execution domains as appropriate, with lifecycle progression controlled by the Decision Lifecycle Engine.

Scenario and AI outputs must remain advisory unless a deterministic system action or human-controlled workflow creates a valid fact event.

Projections, workspaces, dashboards, rankings, summaries, and review views must consume events without becoming canonical sources themselves.

The taxonomy may evolve, but changes must be deliberate, documented, replay-compatible, and aligned with the knowledge-base invariants.
