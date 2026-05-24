---
title: AI Gateway And Route Alias Model
type: design-document
status: accepted
created: 2026-05-24
tags:
  - ai-gateway
  - litellm
  - route-aliases
  - ai-advisory
  - m13a
related_issues:
  - TF-F062
related_adrs:
  - ADR-0037
  - ADR-0041
  - ADR-0042
---

# AI Gateway And Route Alias Model

## Purpose

This document defines the M13A model for AI gateway routing.

TradeForge should ask for advisory roles, not raw model names. A gateway maps
those advisory roles to concrete model providers outside workflow logic.

## Core Model

LiteLLM is not an ordinary provider.

LiteLLM is an AI gateway:

- gateway URL
- credential boundary
- route catalog
- model router
- fallback boundary
- provider abstraction layer

TradeForge remains responsible for advisory task boundaries and authority
validation. LiteLLM remains responsible for routing requests to concrete
underlying model providers.

## Concept Distinctions

| Concept | Meaning |
|---|---|
| AI capability | A typed TradeForge function such as advisory generation or replay summarization |
| AI gateway | A configured routing boundary such as LiteLLM |
| Route alias | A TradeForge-facing semantic route such as `tf-reasoning` |
| Advisory role | The task intent, such as thesis critique or fast summary |
| Underlying provider | The concrete provider behind the gateway, such as Groq, OpenAI, Anthropic, NVIDIA NIM, Gemini, or Ollama |
| Model | The concrete model selected by the gateway |
| Fallback route | A backup route used when the preferred route is unavailable |

Route aliases are operational routing metadata. They are not canonical decision
facts and do not grant AI authority.

## Required Route Aliases

Initial M13A aliases:

| Advisory role | Route alias | Intended use |
|---|---|---|
| Fast Summary | `tf-fast` | Low-latency summaries and simple classification |
| Thesis Critique | `tf-reasoning` | Thesis review, plan critique, risk critique |
| Replay Analysis | `tf-long-context` | Replay summarization and historical reasoning over longer context |
| Cheap Classification | `tf-cheap` | Low-cost classification or formatting checks |
| Offline Local | `tf-local` | Local/offline fallback through Ollama or equivalent |

The exact underlying providers and models are operational configuration. They
must not become workflow semantics.

## Advisory Task Mapping

Representative mappings:

| TradeForge task | Preferred route alias |
|---|---|
| Replay summary | `tf-long-context` |
| Thesis review assistant | `tf-reasoning` |
| Advisory observation generation | `tf-reasoning` |
| Candidate screening | `tf-fast` |
| Lightweight validation/classification | `tf-cheap` |
| Offline/private draft support | `tf-local` |

Future implementation may let operators change mappings, but the initial model
should keep mappings explicit and operator-visible.

## Gateway Visibility

The provider governance surface should show:

- gateway provider identity
- gateway URL
- reachability
- last health probe
- available route aliases
- default advisory route
- route to underlying provider/model resolution when available
- fallback route where configured
- degraded route state

This visibility is operational. It does not make gateway state canonical truth.

## Runtime Boundary

Advisory services should depend on semantic advisory roles or route aliases.
They should not hardcode raw model strings in workflow logic.

The `AIAdvisoryProvider` boundary remains authoritative for validating advisory
responses:

- response identity matches request identity
- artifact kind matches request kind
- authority remains `ADVISORY`
- response cannot approve, execute, or mutate lifecycle state

## Credential Boundary

TradeForge stores only the gateway credential shape needed to call LiteLLM:

- `base_url`
- `api_key`
- default route/model metadata when needed

Underlying model-provider API keys should live in LiteLLM configuration or
operator environment variables used by the LiteLLM service. TradeForge should
not store every downstream model-provider key unless a future issue explicitly
changes the credential boundary.

## Replay And Provenance

Advisory artifacts should preserve enough provenance to interpret model routing
historically:

- gateway provider
- route alias requested
- underlying provider/model when returned or available
- timestamp
- advisory task kind

Replay must not call live LiteLLM to reconstruct historical route resolution.
If historical route resolution was not captured, replay should show that route
details are unavailable rather than infer them from current configuration.

## Deferred Features

The following are deferred:

- automatic hidden model selection
- cost optimization
- model quality scoring
- multi-agent orchestration
- editing LiteLLM config files from TradeForge
- direct provider adapters for each LLM vendor
- automatic AI task execution without explicit operator trigger or separately
  accepted opt-in rules

## Authority Boundary

No AI gateway route may:

- approve a plan
- execute a trade
- create lifecycle transitions
- promote advisory candidates automatically
- become source-of-truth state
- suppress uncertainty or provenance

AI gateway routing supports advisory cognition. It does not control the
decision lifecycle.

