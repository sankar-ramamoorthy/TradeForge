# Research: Ollama Remote Advisory Route

## Decision: Keep LiteLLM as the only outbound advisory adapter

**Rationale**: TF-F088 explicitly keeps direct TradeForge-to-Ollama adapters out of scope. The existing `OpenAICompatibleAdvisoryProvider` and request composer already support request-scoped provider routing through LiteLLM.

**Alternatives considered**: A direct Ollama adapter was rejected because it would bypass the managed gateway boundary and expand advisory infrastructure scope.

## Decision: Treat Ollama remote/local/auto as keyless provider routes

**Rationale**: Ollama does not require a per-provider API key in the current local model. URL/model configuration is operational routing configuration, not secret material.

**Alternatives considered**: Adding encrypted credential schemas for Ollama URLs was deferred because TF-F088 accepts documented environment/configuration paths and does not require Provider Governance URL editing.

## Decision: Explicit remote/local routes never fallback

**Rationale**: Hidden fallback would obscure provenance and make diagnostics misleading. TF-F088 only permits fallback behavior for `ollama-auto`.

**Alternatives considered**: Sharing fallback behavior across all Ollama routes was rejected because it violates the issue acceptance criteria.

## Decision: `ollama-auto` resolves to the backend it actually uses

**Rationale**: Provenance needs to identify the selected backend identity. Returning `ollama-remote` or `ollama-local` after the bounded probe keeps generated advisory metadata auditable.

**Alternatives considered**: Reporting `ollama-auto` in provenance was rejected because it hides the concrete backend used for generation.
