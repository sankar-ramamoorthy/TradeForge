---
title: Provider Governance Control Surface
type: design-document
status: accepted
created: 2026-05-24
tags:
  - provider-governance
  - ai-gateway
  - capability-routing
  - credentials
  - operational-ux
  - m13a
related_issues:
  - TF-F060
related_adrs:
  - ADR-0032
  - ADR-0037
  - ADR-0038
---

# Provider Governance Control Surface

## Purpose

M13A defines provider governance as an external systems control plane, not as
a contextual workflow rail and not as a canonical decision workspace.

The control surface exists to make operational trust visible:

- which external systems are configured
- which capabilities they serve
- whether credentials are usable
- whether fallback or degraded states are active
- whether the AI gateway is reachable
- which advisory route aliases are available
- what diagnostics require operator attention

The surface supports operation of external advisory infrastructure. It does not
own lifecycle state, workflow decisions, trade authorization, execution, or
canonical event truth.

## Boundary

The central M13A distinction is:

```text
Credential != Provider != Capability != Model
```

The control surface must keep those concepts visually and structurally
separate.

| Concept | Meaning | Control surface responsibility |
|---|---|---|
| Credential | Access material for an external system | Show configured, missing, invalid, revoked, untested, validation state |
| Provider | Named external integration | Show identity, capability support, health, provenance |
| Capability | Typed external function | Show primary provider, fallback order, current resolution |
| Gateway | Provider that routes to underlying systems | Show gateway reachability and route aliases |
| Model | Concrete LLM selected behind a gateway | Show only as operational routing metadata |

LiteLLM is represented as an AI gateway and routing boundary, not as an ordinary
single-provider data source.

## Surface Structure

The provider governance surface should include these modules.

### Overview

The overview answers whether external systems are usable now.

Required content:

- market data status
- broker provider status, even if not yet implemented
- AI gateway status
- credential health summary
- fallback and degraded-state warnings
- last validation sweep
- advisory/non-canonical boundary reminder

### Credentials

Credential management belongs in this surface, not in contextual workflow
rails.

Required content:

- configured, missing, invalid, revoked, and untested states
- masked secret display only
- validation/test action
- last validation timestamp
- rotation flow
- removal flow
- explicit master-key unavailable state

`TRADEFORGE_MASTER_KEY` remains OS environment configuration. It must not be
entered, stored, or changed through the browser UI.

### Market Data Providers

This module shows providers that serve market data capabilities such as price
snapshots and fundamentals.

Required content:

- provider identity
- declared capabilities
- configured credential status
- health state
- last validation timestamp
- recent fallback or degraded behavior
- provenance fields surfaced by downstream context panels

### Broker Providers

This module reserves the governance boundary for future broker or paper-trading
providers.

Required content for M13A:

- visible placeholder state when no broker provider is active
- explicit statement that broker configuration does not authorize execution
- distinction between future broker capability governance and current lifecycle
  authority

### AI Gateway

This module represents LiteLLM as a gateway.

Required content:

- gateway URL
- reachability
- latency or last probe result when available
- default advisory route
- available route aliases
- underlying provider/model resolution when available
- degraded and fallback state

TradeForge should request semantic advisory roles. Gateway configuration maps
those roles to concrete providers and models outside workflow logic.

Representative route aliases:

| Role | Route alias |
|---|---|
| Fast Summary | `tf-fast` |
| Thesis Critique | `tf-reasoning` |
| Replay Analysis | `tf-long-context` |
| Cheap Classification | `tf-cheap` |
| Offline Local | `tf-local` |

### Capability Routing

Capability routing is configured by typed capability, not by raw vendor.

Representative display:

```text
Price Snapshots
  Primary: yfinance
  Fallback: polygon

Fundamentals
  Primary: fmp
  Fallback: alpha_vantage

AI Advisory
  Primary: litellm
```

The first M13A implementation should preserve deterministic primary plus
ordered fallback routing. More complex routing policies are deferred.

### Diagnostics

Diagnostics make external-system trust visible.

Representative diagnostic classes:

- provider unreachable
- credential invalid
- route unavailable
- quota exceeded
- fallback triggered
- latency spike
- validation succeeded
- validation failed
- replay nondeterminism warning

Diagnostics must remain distinguishable from canonical decision facts.

## Contextual Rail Rule

Contextual rails should be informational and provenance-oriented.

Rails may show:

- current capability
- selected provider
- fallback provider
- health state
- freshness
- last snapshot or validation timestamp
- advisory/non-canonical boundary
- link to configure

Rails must not host:

- long-form credential entry
- route management
- model selection
- diagnostics administration
- provider governance policy editing

This preserves workflow cognition and prevents provider administration from
competing with decision context.

## Navigation Rule

The runtime may expose the surface through a route or module named Provider
Configuration or Provider Governance. It must not redefine the canonical
workspace model.

Provider governance is not a Persona Workspace because it does not own persona
cognition, lifecycle progression, opportunity evaluation, exposure awareness,
or review continuity.

## Authority Boundaries

The provider governance surface must not:

- write lifecycle events
- approve plans
- execute trades
- create TradeIdeas
- promote advisory candidates
- make AI output canonical
- hide provider provenance
- imply external provider data is source-of-truth state

All provider, gateway, and diagnostic state remains operational, advisory, and
non-canonical unless a future ADR explicitly changes that boundary.

