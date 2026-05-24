---
title: Capability Routing Governance Model
type: design-document
status: accepted
created: 2026-05-24
tags:
  - provider-governance
  - capability-routing
  - provider-registry
  - m13a
related_issues:
  - TF-F061
related_adrs:
  - ADR-0032
  - ADR-0038
---

# Capability Routing Governance Model

## Purpose

This document defines the M13A governance model for capability-first external
provider routing.

TradeForge should reason in capabilities and operational roles before raw
vendor names. Provider identity remains visible for provenance, but workflow
logic should depend on typed capabilities.

## Core Distinctions

Capability routing preserves these distinctions:

| Concept | Meaning |
|---|---|
| Provider identity | A named external integration such as `yfinance`, `fmp`, `alpha_vantage`, `alpaca`, or `litellm` |
| Provider capability | A typed external function such as price, fundamentals, AI advisory, or broker/paper trading |
| Configured provider | A provider with sufficient credential/configuration material to be considered available for a capability |
| Preferred provider | The operator-selected primary provider for a capability |
| Fallback provider | An ordered backup provider for a capability |
| Selected provider | The provider that actually served, or would currently serve, a capability |
| Capability route | The deterministic preferred plus fallback path for one capability |

Provider identity must not be treated as synonymous with price capability.

## Default Routing Policy

M13A preserves the M10D routing policy:

```text
selected_provider = first usable provider from [preferred, ...fallbacks]
```

This is deterministic primary plus ordered fallback routing.

M13A does not introduce weighted routing, hidden scoring, workspace-aware
routing, autonomous provider choice, or cost optimization.

## Initial Capability Families

### Price Snapshots

Purpose:

- current or recent market price context
- OHLCV snapshot support
- technical regime context

Representative route:

```text
Price Snapshots
  Primary: yfinance
  Fallback: polygon
```

Price snapshot outputs remain market context, not lifecycle truth.

### Fundamentals

Purpose:

- company profile
- statements
- ratios
- business context

Representative route:

```text
Fundamentals
  Primary: fmp
  Fallback: alpha_vantage
```

Fundamentals remain advisory external context. Missing fundamentals should be
shown as missing context, not as a workflow blocker by default.

### AI Advisory

Purpose:

- replay summary
- thesis critique
- advisory observation generation
- candidate screening
- future advisory enrichment

Representative route:

```text
AI Advisory
  Primary: litellm
```

`litellm` is a gateway provider. The AI advisory capability route selects the
gateway. Route aliases inside the gateway select underlying model providers.

### Broker Or Paper Trading

Purpose:

- future broker or paper-trading connectivity
- future execution-provider governance

Representative route:

```text
Paper Trading
  Primary: alpaca
```

Broker capability governance does not authorize execution. Decision lifecycle
authority and human approval remain separate.

## Operator Visibility Requirements

Every capability route should expose:

- capability name
- preferred provider
- fallback provider order
- currently selected provider
- configured provider set
- unavailable or degraded providers
- fallback reason when fallback occurs
- advisory/non-canonical boundary where applicable

When external data is consumed by a workspace or advisory task, the output must
preserve provider provenance. The operator should be able to tell which provider
served the context and whether fallback resolution was involved.

## Replay And Provenance

Capability resolution can be replay-relevant because it changes what external
context was visible to the operator.

M13A does not make route configuration canonical event-ledger truth by default.
Historical replay must not call live providers to reconstruct historical route
state. If a replay view needs provider route context, it must rely on captured
historical provenance or explicitly show that route context is unavailable.

## Failure States

Capability governance should distinguish:

- no provider configured
- credential missing
- credential invalid
- provider unreachable
- provider lacks capability
- quota exceeded
- fallback selected
- capability unsupported
- data unavailable despite route availability

These states are operational context. They do not mutate lifecycle state.

## Deferred Policies

The following are deferred beyond the M13A default model:

- weighted provider routing
- cost-aware routing
- workspace-scoped provider preferences
- persona-scoped provider preferences
- automatic provider quality scoring
- hidden adaptive routing
- broker execution routing

Future policy expansion must preserve operator visibility and replay
interpretability.

## Authority Boundary

No capability route may:

- write canonical workflow state
- authorize lifecycle transitions
- approve a trade plan
- execute a trade
- hide provider origin
- collapse advisory data into event truth

Capability routing is operational governance for external-system context. It is
not decision authority.

