# Data Model: Ollama Remote Advisory Route

## Advisory Provider Route

Represents an operator-selectable provider identity used for advisory model routing.

Fields:

- `provider_id`: One of `ollama`, `ollama-remote`, `ollama-local`, `ollama-auto`, or existing governed LLM provider IDs.
- `credential_required`: False for Ollama routes.
- `configured`: Whether the route can be attempted with current operational configuration.
- `capabilities`: Operational capabilities surfaced by Provider Governance.

Validation:

- Provider IDs must be non-blank.
- Explicit `ollama-remote` requires a remote URL to be attemptable.
- Explicit `ollama-local` uses the local URL path and does not fallback.
- `ollama-auto` may resolve to remote or local after a bounded probe.

## Ollama Backend Configuration

Represents operational URL/model hints for Ollama routes.

Fields:

- `OLLAMA_REMOTE_URL`: Remote Ollama base URL.
- `OLLAMA_REMOTE_MODEL`: Optional remote model hint.
- `OLLAMA_LOCAL_URL`: Local Ollama base URL.
- `OLLAMA_LOCAL_MODEL`: Optional local model hint.
- `OLLAMA_API_BASE`: Legacy single-Ollama base URL.

Validation:

- Blank URL values are treated as missing.
- Local defaults remain compatible with existing `ollama` behavior.
- Model hints do not install or provision models.

## Advisory Provenance

Represents non-canonical response metadata.

Fields:

- `provider_id`: Selected/resolved provider identity.
- `provider_version`: Advisory provider adapter version.
- `model_id`: Model returned or requested.
- `generated_at`: Response timestamp.
- `prompt_version`: Prompt version.

Validation:

- Provider identity must not imply lifecycle, execution, event, or canonical authority.
- For `ollama-auto`, provenance records the concrete resolved backend.
