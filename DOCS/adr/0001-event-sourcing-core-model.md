# ADR 0001: Event Sourcing Core Model

## Status
Accepted

## Context
TradeForge is an event-sourced decision-support system. Its runtime must preserve a strict distinction between canonical truth, derived state, inferred state, external system state, and advisory interpretation.

The system supports persona-scoped workspaces, scenario discovery, decision workflows, execution integration, replay, and review. These subsystems all need a shared truth model that prevents hidden mutable state, preserves historical integrity, and allows deterministic reconstruction of past decisions.

Without a canonical event model, workspaces could become stored dashboards, projections could become competing truth, broker state could override system memory, and AI outputs could be mistaken for authoritative facts. That would violate TradeForge invariants and make lifecycle replay unreliable.

## Decision
TradeForge will use an immutable append-only Event Ledger as the canonical source of truth for all durable system state.

All material state must be derived from events. Events represent facts that happened, not opinions, predictions, summaries, UI states, or AI interpretations. Historical events must never be mutated or deleted. Corrections must be represented by new events.

Derived state, including projections, workspace surfaces, dashboards, summaries, rankings, watchlists, and read models, is non-authoritative. Inferred state, including market regimes, scenario probabilities, clustering, and AI-generated interpretations, is advisory and must remain distinguishable from canonical state.

Replay must reconstruct system state from the Event Ledger, deterministic rules, and optional historical snapshots. Replay must not depend on live market APIs, mutable broker state, UI state, or current AI output.

External systems, including brokers and market data providers, are not canonical truth. Interactions with external systems may produce execution or market observation events, but the external systems themselves do not own TradeForge state.

## Rationale
Event sourcing is required to make TradeForge replayable, auditable, and workflow-correct. The system exists to support disciplined decision-making under uncertainty, which requires knowing what happened, when it happened, under which persona and workspace context, and how later decisions were reached.

An append-only Event Ledger preserves temporal ordering and historical integrity. It allows workspaces, decision queues, exposure views, scenario surfaces, and review artifacts to be reconstructed instead of trusted as independent state holders.

This model also enforces the AI advisory boundary. AI systems may summarize, rank, cluster, and suggest interpretations, but their outputs are not facts unless a deterministic system layer or human-controlled workflow records an appropriate event.

## Alternatives Considered
CRUD-first persistence was rejected because mutable entity records obscure historical transitions and make replay dependent on current database state.

Mutable current-state tables as the source of truth were rejected because they create hidden state and make corrections indistinguishable from original facts.

Broker or external API state as canonical truth was rejected because external systems are volatile, outside TradeForge control, and insufficient to reconstruct internal decision context.

Projection-authored truth was rejected because projections are derived views. Allowing projections to become authoritative would make workspace and UI state compete with the Event Ledger.

AI-authored truth was rejected because AI is advisory only and must not mutate canonical state, execute trades, approve decisions, or override deterministic rules.

## Consequences
Every durable workflow change must be represented as an immutable event.

All read models and workspace surfaces must be rebuildable from events and deterministic rules.

Corrections require compensating or corrective events rather than mutation of prior records.

Implementation must preserve strict layer separation: domain logic remains pure and event-aware, services orchestrate workflows, infrastructure stores and integrates external systems, and app entrypoints expose behavior.

Development may require more explicit event modeling than a CRUD design, but the trade-off is required for auditability, replayability, and lifecycle integrity.
