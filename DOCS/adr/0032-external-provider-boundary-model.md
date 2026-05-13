# ADR 0032: External Provider Boundary Model

## Status
Accepted

## Context
TradeForge M9 introduces real-world market context through external data providers (yfinance, Polygon/Massive.com, Alpaca). Without an explicit boundary model, provider data risks leaking into canonical event state, becoming implicit execution authority, or breaking replay integrity.

TradeForge is a replayable discretionary cognition system. All external market data must remain:

- read-only
- advisory
- non-canonical
- normalized across providers
- traceable through provenance

Provider selection must also remain replaceable without architectural impact.

## Decision
All external market data providers must connect to TradeForge through a normalized provider boundary interface.

The provider boundary must:

- expose a normalized market snapshot contract independent of any single provider's API
- enforce read-only data flow — provider adapters may not write to the event ledger
- record provider provenance on all market context outputs (provider identity, timestamp, data version)
- remain replaceable — swapping yfinance for Alpaca must not require changes to workspace or lifecycle layers
- remain replay-aware — market snapshots must be persistable for historical reconstruction without becoming canonical truth

The provider boundary must not:

- write lifecycle events
- authorize lifecycle transitions
- mutate canonical workflow state
- become an execution authority
- hide data provenance or provider origin
- be coupled to a single vendor's SDK or schema

Market snapshots produced by the boundary are derived operational context, not canonical facts.

## Rationale
Provider normalization protects the event sourcing boundary. If each provider's API shape leaked into workspace projections or lifecycle services, replacing a provider would require surgical changes across multiple layers.

Provenance tracking preserves replay integrity. Historical reconstructions must be able to reference which provider and version supplied the context visible at the time of a decision.

Read-only enforcement preserves human decision sovereignty. No automated provider feed should be able to produce lifecycle transitions or execution instructions.

Replaceability keeps the provider layer subordinate to architecture. yfinance is appropriate for development and demonstration; Polygon or Alpaca may be appropriate for production. The boundary model must support this transition without architectural change.

## Alternatives Considered
Direct provider SDK calls from workspace projectors were rejected because provider schema changes would propagate through the workspace layer and break projection contracts.

Provider data stored directly in the event ledger as canonical events was rejected because external market data is not an internal business fact — it is advisory context.

Single-provider lock-in was rejected because provider availability, cost, and reliability differ by environment.

## Consequences
All provider adapters (yfinance, Polygon/Massive.com, Alpaca) must implement the normalized snapshot interface defined in TF-0042.

Workspace overlays and market context summaries must consume the normalized snapshot contract, not adapter-specific shapes.

Provider provenance fields must be included on all market context outputs delivered to workspaces.

The demo seed flow (TF-0051) must use the same normalized boundary as live providers to prevent demo/production divergence.

Replay-compatible snapshot persistence (TF-0052) must store snapshots as derived artifacts with explicit provenance, not as canonical events.
