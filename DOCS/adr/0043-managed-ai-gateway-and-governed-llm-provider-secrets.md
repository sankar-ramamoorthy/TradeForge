---
title: ADR-0043 - Managed AI Gateway And Governed LLM Provider Secrets
status: accepted
date: 2026-05-25
milestone: M13B
deciders: [TradeForge architecture]
supersedes_boundary:
  - ADR-0037
  - DOCS/ai-gateway-route-alias-model.md
related_issues:
  - TF-F072
  - TF-F073
  - TF-F074
  - TF-F075
---

# ADR-0043 - Managed AI Gateway And Governed LLM Provider Secrets

## Context

M13A accepted LiteLLM as the AI gateway and route-alias boundary. That model
intentionally kept downstream LLM vendor keys outside TradeForge: TradeForge
stored the LiteLLM gateway credential, while provider keys for Groq, NVIDIA
NIM, OpenAI, Anthropic, Google, and similar vendors lived in LiteLLM
configuration or operator environment variables.

M13B changes that boundary. The managed advisory runtime now requires
TradeForge to own operator-facing model selection, the internal LiteLLM
network boundary, and governed downstream LLM provider secret management.

This is not a semantic change to AI authority. AI remains advisory only.

## Decision

TradeForge becomes the operator-facing advisory gateway and governance owner
for the managed AI runtime.

### Managed LiteLLM Boundary

LiteLLM is managed internal infrastructure. It should be reachable by
TradeForge through internal runtime networking and should not be directly
operator-facing by default.

Browser and host workflows must access advisory behavior through TradeForge,
not by calling LiteLLM directly.

### Advisory Model Selection

TradeForge owns global advisory model or route selection:

- discover available LiteLLM models/routes through TradeForge
- allow one primary advisory model/route
- allow one optional fallback advisory model/route
- remove hardcoded advisory model names from workflow logic
- use the selected configuration advisory-wide
- smoke-test the selected route through TradeForge

The selected route is operational configuration. It is not canonical decision
truth and does not grant AI lifecycle authority.

### Downstream LLM Provider Secrets

TradeForge becomes the governed owner of downstream LLM provider keys used by
the managed advisory runtime.

Provider secrets include Groq, NVIDIA NIM, OpenAI, Anthropic, Google, and
similar LLM vendor credentials.

Rules:

- provider secrets are stored encrypted at rest in `.keys.enc`
- API and UI responses return masked values only
- `TRADEFORGE_MASTER_KEY` remains OS environment configuration
- runtime decryption occurs only at the composition boundary
- LiteLLM receives provider secrets only through per-request composition
- rotation and reload semantics must be explicit
- plaintext secrets must not be logged, returned, committed, or embedded in
  static LiteLLM config

### Runtime Composition

TradeForge injects decrypted provider secrets into individual managed LiteLLM
requests at advisory generation time. Provider adapters and advisory workflow
code must remain unaware of storage and decryption mechanics.

The composition boundary remains the only place where encrypted TradeForge
credentials become runtime inputs for external systems.

**Implementation note (TF-F075):** The accepted M13B path is stateless LiteLLM
operation. TradeForge stores the LiteLLM gateway credential separately from
advisory model selection. Model selection is stored as explicit provider/model
pairs. `LLMProviderCredentialResolver` resolves the selected provider ID,
decrypts the active provider key only when needed, and treats Ollama as a
keyless internal provider with configured API base. `LiteLLMRequestComposer`
then builds the `/chat/completions` request with the selected model and
request-scoped `api_key` / `api_base` values only when required.

**Rejected history:** The earlier TF-F075 design used LiteLLM
`POST /config/update`, `LiteLLMGatewayAdminClient`, `DATABASE_URL`,
`STORE_MODEL_IN_DB=True`, and a separate `litellm_proxy` database. That path
was rejected for M13B because it moved TradeForge credential authority into
LiteLLM DB-backed mutable config, introduced gateway schema migration coupling,
and made saved model strings too influential once explicit provider IDs exist.

### Replay And Provenance

Advisory artifacts should preserve enough provenance to interpret historical
advisory output:

- TradeForge advisory task kind
- selected route or model alias
- fallback route when used
- gateway identity
- underlying provider/model when returned or available
- timestamp

Replay must not call live LiteLLM or live vendor providers to reconstruct
historical route or secret state. Missing historical route details should be
shown as unavailable rather than inferred from current configuration.

## Authority Boundary

This ADR does not change lifecycle authority.

AI may summarize, critique, classify, rank, and contextualize. AI may not:

- execute trades
- approve plans
- create or skip lifecycle transitions
- promote advisory candidates automatically
- write canonical event-ledger facts directly
- override deterministic rules
- become source-of-truth state

TradeForge owns the advisory boundary. The human operator owns decisions.

## Exclusions

This ADR explicitly excludes:

- autonomous trading
- AI approval authority
- direct vendor SDK bypass from advisory workflow code
- generalized AI orchestration
- multi-agent runtime governance
- automatic hidden model choice
- cost optimization engines
- Kubernetes secrets or external vault integration
- broker execution expansion

## Consequences

- M13B supersedes the M13A assumption that downstream LLM provider keys live
  outside TradeForge.
- `DOCS/ai-gateway-route-alias-model.md` remains useful for route concepts, but
  its credential-boundary section is superseded for the managed advisory
  runtime.
- TF-F072, TF-F073, and TF-F074 must be implemented as a coherent governance
  slice, not as unrelated UI, Docker, and credential cleanup.
- Existing AI advisory and provider-governance invariants remain active.
- No event types are added by this ADR.

## Alternatives Considered

Keeping downstream LLM provider keys in LiteLLM configuration was rejected for
the managed advisory runtime because it splits credential governance between
TradeForge and a gateway file.

Direct vendor SDK adapters in TradeForge advisory services were rejected
because they bypass LiteLLM as the managed gateway and multiply provider-specific
routing behavior in workflow code.

Combining model selection, network internalization, and provider secret
governance into one implementation issue was rejected because it would blur
operator UX, infrastructure boundary, and security semantics.
