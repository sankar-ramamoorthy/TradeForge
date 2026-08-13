# Contract: Provider Governance AI Gateway

## Provider List

Provider Governance response includes keyless Ollama route providers:

- `ollama`
- `ollama-local`
- `ollama-remote`
- `ollama-auto`

Each provider remains operational and non-canonical:

- `authority`: `operational`
- `is_canonical`: `false`
- `credential_required`: `false`

## Model Selection

The AI gateway model-selection payload accepts Ollama route identities for:

- `primary_provider_id`
- `fallback_provider_id`

The model fields continue to carry LiteLLM-compatible model identifiers.

## Smoke Test

The AI gateway smoke-test response reports:

- `provider_id`: selected/resolved advisory provider identity
- `model_id`: advisory model used
- `advisory_response_authority`: `advisory`
- no lifecycle, execution, or Event Ledger authority

## Error Behavior

Explicit remote/local route failure is reported as provider unavailable. Only `ollama-auto` may choose a different Ollama backend after a bounded reachability check.
