# Implementation Plan: Ollama Remote Advisory Route

**Branch**: `feature/tf-f088-ollama-remote` | **Date**: 2026-08-13 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/001-ollama-remote-advisory-route/spec.md`

## Summary

Add governed Ollama provider-route identities for remote, local, and auto advisory routing while preserving the existing LiteLLM gateway boundary. The implementation will extend request-time provider credential resolution, provider governance visibility, Provider Governance UI selection, and tests for route composition, fallback behavior, and advisory provenance.

## Technical Context

**Language/Version**: Python 3.12 backend, TypeScript/React frontend

**Primary Dependencies**: FastAPI, OpenAI-compatible client, LiteLLM gateway, pytest, Vite/React

**Storage**: Existing encrypted credential store for model selection; environment variables for Ollama URL/model hints

**Testing**: `uv run pytest` focused backend tests; frontend type/build checks for UI changes when practical

**Target Platform**: Local Docker/Windows development runtime with optional remote Ollama host

**Project Type**: Web application with Python API and React frontend

**Performance Goals**: `ollama-auto` reachability probe must be bounded and short enough not to make normal advisory route composition feel blocked

**Constraints**: No direct TradeForge-to-Ollama adapter, no canonical event writes, no lifecycle/execution authority, no secret exposure

**Scale/Scope**: One provider-governance feature touching advisory routing, diagnostics, and UI selection only

## Constitution Check

- Existing doctrine remains authoritative: Pass. TF-F088 issue scope and KB invariants bound the change.
- Event-sourced lifecycle integrity: Pass. No new events, lifecycle states, projections, or replay facts are introduced.
- Human decision sovereignty and advisory boundaries: Pass. The feature only chooses advisory providers and surfaces diagnostics.
- Issue-first governance: Pass. Work is tied to TF-F088 / M13B.
- Replayability, provenance, and validation: Pass. Provenance is an acceptance criterion; tests will verify provider/model identity and absence of Event Ledger writes.

## Project Structure

### Documentation (this feature)

```text
specs/001-ollama-remote-advisory-route/
|-- spec.md
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts/
|   `-- provider-governance-ai-gateway.md
|-- checklists/
|   `-- requirements.md
`-- tasks.md
```

### Source Code (repository root)

```text
src/
|-- infrastructure/advisory/
|   |-- litellm_request_composer.py
|   `-- openai_compatible_provider.py
|-- app/api/routes/
|   `-- governance.py
|-- security/
|   `-- advisory_model_selection.py

frontend/
`-- src/workspaces/
    `-- ProviderGovernanceWorkspace.tsx

tests/
|-- test_litellm_request_composer.py
|-- test_openai_compatible_provider.py
`-- test_provider_governance_api.py
```

**Structure Decision**: Extend existing advisory infrastructure, provider governance API routes, frontend provider selector, and focused tests. Do not add new services or adapters.

## Phase 0: Research

See [research.md](./research.md).

## Phase 1: Design

See [data-model.md](./data-model.md), [contracts/provider-governance-ai-gateway.md](./contracts/provider-governance-ai-gateway.md), and [quickstart.md](./quickstart.md).

## Complexity Tracking

No constitution violations are introduced.
