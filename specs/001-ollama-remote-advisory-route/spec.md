# Feature Specification: Ollama Remote Advisory Route

**Feature Branch**: `feature/tf-f088-ollama-remote`

**Created**: 2026-08-13

**Status**: Implemented

**Input**: User description: "lets work on the ollama remote etc now. There must be an issue."

## User Scenarios & Testing

### User Story 1 - Select Remote Ollama Advisory Backend (Priority: P1)

An operator can select `ollama-remote` as the primary or fallback advisory model provider so advisory generation can use a separately hosted GPU Ollama instance through the governed LiteLLM gateway.

**Why this priority**: This is the core operator need behind TF-F088 and enables the remote backend without making it mandatory.

**Independent Test**: Configure the advisory model route with `ollama-remote`, run provider governance discovery and request composition tests, and verify the route uses the remote Ollama base without exposing secrets or writing canonical events.

**Acceptance Scenarios**:

1. **Given** the provider governance workspace is loaded, **When** the operator chooses a primary or fallback advisory provider, **Then** `ollama-remote` is available alongside existing LLM provider identities.
2. **Given** `ollama-remote` is selected and configured with a remote URL, **When** an advisory request is composed, **Then** the request routes through LiteLLM with the remote Ollama API base and keyless provider identity.
3. **Given** `ollama-remote` is selected but unavailable, **When** an advisory request is attempted, **Then** advisory generation reports provider unavailable and does not mutate lifecycle, execution, import, replay, or canonical event state.

---

### User Story 2 - Distinguish Local And Auto Ollama Routes (Priority: P2)

An operator can distinguish legacy `ollama`, explicit `ollama-local`, explicit `ollama-remote`, and remote-preferred `ollama-auto` routes so local and remote behavior is visible and governed.

**Why this priority**: It prevents hidden fallback and makes remote/local behavior auditable.

**Independent Test**: Resolve each Ollama provider identity independently and verify only `ollama-auto` may choose a different backend after a bounded remote reachability check.

**Acceptance Scenarios**:

1. **Given** `ollama-local` is selected, **When** the local URL is configured, **Then** requests use the local Ollama base and do not fall back to remote.
2. **Given** `ollama-auto` is selected and the remote URL is reachable, **When** a request is composed, **Then** the resolved advisory backend is `ollama-remote`.
3. **Given** `ollama-auto` is selected and the remote URL is not reachable, **When** a request is composed, **Then** the resolved advisory backend is `ollama-local`.

---

### User Story 3 - Preserve Advisory Route Provenance (Priority: P3)

Operators and diagnostic screens can see which governed provider identity and model produced an advisory output or smoke-test result.

**Why this priority**: Advisory artifacts must preserve provenance and distinguish generated interpretation from canonical truth.

**Independent Test**: Generate or fake an advisory response through an explicit Ollama route and verify the provenance and smoke-test response report the selected backend identity and model without exposing credentials.

**Acceptance Scenarios**:

1. **Given** an advisory request succeeds through `ollama-remote`, **When** the response is returned, **Then** provenance reports provider `ollama-remote` and the model used.
2. **Given** an advisory route smoke test runs, **When** the response is returned, **Then** it reports the backend provider identity, model, and advisory authority without event ledger writes.

### Edge Cases

- Remote URL is unset for explicit `ollama-remote`.
- Remote host is configured but offline, slow, or returns an error.
- `ollama-auto` has no remote URL configured.
- Fallback model/provider selection is configured, but the primary and fallback model are identical.
- Smoke tests fail while canonical workflow screens remain usable.

## Requirements

### Functional Requirements

- **FR-001**: Provider Governance MUST expose `ollama-remote` as a governed keyless advisory provider route.
- **FR-002**: Provider Governance MUST expose `ollama-local` and `ollama-auto` if they can be implemented without bypassing the LiteLLM gateway.
- **FR-003**: The advisory model selection flow MUST allow `ollama-remote`, `ollama-local`, and `ollama-auto` as primary or fallback provider identities.
- **FR-004**: Explicit `ollama-remote` and `ollama-local` selections MUST NOT silently fall back to another Ollama backend.
- **FR-005**: `ollama-auto` MAY perform a bounded remote reachability check and choose local Ollama when remote is unavailable.
- **FR-006**: Remote and local Ollama routes MUST be configurable through environment/configuration paths for separate URLs and default model hints.
- **FR-007**: Advisory request composition MUST send Ollama route requests through the existing LiteLLM gateway boundary.
- **FR-008**: Advisory responses and smoke-test diagnostics MUST preserve the selected/resolved provider identity and model without exposing secret values.
- **FR-009**: Provider failure MUST be reported as advisory-provider unavailable and MUST NOT block lifecycle, replay, imports, execution, or canonical state.
- **FR-010**: The feature MUST NOT add execution, approval, lifecycle, broker, or Event Ledger authority.

### Key Entities

- **Advisory Provider Route**: A governed operator-selectable provider identity used for advisory model routing.
- **Ollama Backend Configuration**: URL and model hint values for local, remote, and auto Ollama behavior.
- **Advisory Provenance**: Non-canonical response metadata identifying provider, version, model, timestamp, and prompt version.

## Success Criteria

### Measurable Outcomes

- **SC-001**: `ollama-remote` can be selected as primary or fallback advisory provider in Provider Governance.
- **SC-002**: Request-composition tests prove `ollama-remote` uses a remote API base distinct from local Ollama.
- **SC-003**: Tests prove explicit `ollama-remote`/`ollama-local` do not fall back silently and `ollama-auto` is the only fallback route.
- **SC-004**: Smoke-test and advisory provenance tests report the selected/resolved provider identity and model.
- **SC-005**: Provider-governance and advisory tests pass without any Event Ledger append during selection or smoke testing.

## Assumptions

- The existing LiteLLM gateway remains the outbound LLM adapter.
- Ollama models continue to use LiteLLM-compatible model identifiers such as `ollama/<model>`.
- Environment/configuration paths are acceptable for this issue; full credential-store-managed URL editing can be added later if needed.
- `OLLAMA_REMOTE_MODEL` and `OLLAMA_LOCAL_MODEL` are model hints for discovery/default display, not model installation instructions.
- Network reachability checks are bounded and operational only; they are not canonical evidence.
