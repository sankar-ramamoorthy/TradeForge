# Quickstart: Ollama Remote Advisory Route

## Prerequisites

- LiteLLM gateway credential configured in TradeForge.
- Optional remote Ollama host URL available in `OLLAMA_REMOTE_URL`.
- Optional model hints in `OLLAMA_REMOTE_MODEL` and `OLLAMA_LOCAL_MODEL`.

## Validation

1. Run focused backend tests:

```powershell
uv run pytest tests/test_litellm_request_composer.py tests/test_openai_compatible_provider.py tests/test_provider_governance_api.py
```

2. Run backend lint/type checks for non-trivial code changes:

```powershell
uv run ruff check .
uv run mypy src tests
```

3. Run frontend validation if the Provider Governance UI changes:

```powershell
npm run typecheck
npm run build
```

## Expected Outcomes

- Provider Governance lists Ollama route identities.
- The Provider Governance model-selection UI includes remote/local/auto Ollama options.
- `ollama-remote` composes a LiteLLM request with the remote API base when configured.
- Explicit remote/local route failures are provider-unavailable errors.
- `ollama-auto` falls back only after a bounded remote probe.
- Smoke tests report advisory provider/model provenance and do not write Event Ledger events.
