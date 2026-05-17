---
title: ADR-0038 - Provider Capability Registry And Typed External Data Contracts
status: accepted
date: 2026-05-16
milestone: M10D
deciders: [TradeForge architecture]
---

# ADR-0038 - Provider Capability Registry And Typed External Data Contracts

## Context

`ADR-0032` established the normalized boundary for external market snapshots.
That decision remains valid for OHLCV market context, provider provenance, replay
awareness, and adapter replaceability.

Since then, `M10C` has centralized provider credentials for a wider set of
planned providers: yfinance, Polygon, Alpaca, Alpha Vantage,
FinancialModelingPrep, and Finqual. Those providers do not expose one uniform
data surface. Some provide price data, some provide fundamentals, and some may
eventually provide more than one capability.

The current runtime still treats "provider" primarily as "price feed" because
its active external-data boundary is the M9 market snapshot path. That is now
too narrow for the next stage of the system. Future fundamentals work and
future AI advisory work need provider identity, provider capability, and typed
data contracts to be modeled separately.

## Decision

TradeForge will extend the external data architecture with a capability-aware
provider model.

### Provider Identity Versus Capability

Provider identity and provider capability are separate concepts.

- A provider identity names a configured external integration such as
  `yfinance`, `alpaca`, `alpha_vantage`, `fmp`, or `finqual`.
- A provider capability names a typed external-data family such as `price` or
  `fundamentals`.
- A configured provider may support one capability or several capabilities.

Provider identity must not be treated as synonymous with price capability.

### Provider Registry

A provider registry will act as the composition-time catalog of configured
providers and the capabilities they support.

The registry must:

- expose configured providers and declared capabilities
- resolve configured providers by capability through deterministic
  preferred-plus-ordered-fallback selection
- model one global preferred provider plus an ordered fallback sequence per
  capability
- remain separate from credential storage
- avoid embedding provider-specific SDK objects into domain or workspace layers

Credential ownership remains governed by `ADR-0037`.

Provider resolution must remain operator-visible. The runtime must make clear:

- which provider served a capability
- why that provider was selected
- whether fallback resolution occurred
- whether a capability is missing or degraded

Resolution context is replay-relevant advisory context because provider choice
changes what external information was visible at a decision point. It must be
preservable for replay without becoming canonical ledger truth.

### Typed Capability Contracts

External data must flow through typed capability contracts behind the registry.

The first two contract families are:

- a price contract, preserving the normalized market snapshot path established
  by `ADR-0032`
- a fundamentals contract, beginning with company profile, financial
  statements, and ratios

Typed contracts must normalize provider-specific responses before they reach
services or workspace consumers.

### Initial Rollout Doctrine

The first fundamentals rollout should use `fmp` as the primary provider and
`alpha_vantage` as the fallback provider. This exercises normalization
discipline and capability divergence early while keeping initial complexity
bounded.

Initial provider selection optimizes for architectural capability validation
rather than long-term provider finality. `fmp` and `alpha_vantage` are first
capability-shaping providers, not permanently blessed providers.

Operator-facing provider configuration in `M10D` should be editable and visible.
Richer provider health/status management is deferred beyond the first rollout.

Initial fundamentals overlays belong in Opportunity and Thesis flows. Plan flows
should not gain rich fundamentals overlays in the first rollout because plan
authoring should occur after thesis formation has already stabilized the main
contextual reasoning.

### Provenance And Authority

All external data artifacts must carry explicit provenance, including provider
identity and `data_as_of` semantics appropriate to the artifact family.

All external data remains:

- read-only
- advisory
- non-canonical
- distinguishable from event-ledger truth

No provider capability may:

- write canonical workflow state
- authorize lifecycle transitions
- obscure provider origin
- collapse advisory data into event truth

## Rationale

The M9 provider boundary was intentionally narrow because the first operational
need was normalized market context. That narrowness is now a limitation rather
than a virtue. Credential setup already proves that the runtime expects
providers with materially different capabilities, and keeping one generic
"provider" abstraction would force later fundamentals work into price-shaped
assumptions.

A small registry plus typed contracts keeps the architecture explicit without
inventing a generalized external-data framework too early. It preserves the
accepted M9 design, adds only the distinctions that are now operationally
necessary, and gives `M11` a stable provider layer to depend on.

## Alternatives Considered

**Expand the existing market snapshot provider protocol to cover every future
external data need:** Rejected. It would turn a clear OHLCV contract into a
mixed generic adapter shape and blur the boundary between price and
fundamentals.

**Create one registry per provider family without a shared capability model:**
Rejected. It would preserve fragmentation and still leave no runtime answer to
which configured provider serves which capability.

**Delay capability modeling until AI advisory work begins:** Rejected. That
would require AI-facing systems to infer provider semantics from an
underspecified layer and would move foundational architecture into the wrong
milestone.

## Consequences

- `ADR-0032` remains authoritative for normalized price snapshots.
- Provider-capability metadata becomes a first-class runtime concern in `M10D`.
- New fundamentals models and adapters must use a distinct typed contract.
- Provider inspection surfaces must communicate capability support and
  provenance explicitly.
- Initial fundamentals rollout uses `fmp` as primary and `alpha_vantage` as
  fallback to validate capability differentiation, normalization, degraded
  states, and fallback provenance early.
- `M11` may depend on a capability-aware external data layer, but it may not
  promote provider data into canonical truth.
