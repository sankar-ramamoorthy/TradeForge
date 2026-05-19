# AI Advisory Interfaces

## Purpose

TF-0065 defines the first runtime contract for AI advisory work in M11.

The contract gives later replay summarization, review assistance, and advisory
provenance issues a stable provider-agnostic boundary without introducing a
concrete LLM adapter.

## Authority

AI advisory artifacts are non-canonical.

They may summarize, rank, highlight, or suggest interpretations. They may not:

- append events
- approve lifecycle transitions
- execute trades
- mutate workspace state
- define historical truth
- hide provenance or uncertainty

ADR-0006 remains the governing runtime ADR.

## Runtime Contract

The contract lives in `src/domain/advisory/`.

Core types:

- `AdvisoryRequest`
- `AdvisoryResponse`
- `AdvisoryProvenance`
- `AdvisoryUncertainty`
- `AdvisorySourceReference`
- `AIAdvisoryProvider`

The services layer exposes `AIAdvisoryService` in `src/services/advisory/`.
It invokes a provider and validates that response identity, artifact kind, and
authority remain consistent with the request.

## Boundary

The TF-0065 boundary intentionally excludes:

- concrete LLM provider adapters
- advisory persistence
- replay summarization implementation
- review assistant implementation
- API endpoints
- frontend surfaces

Future provider adapters must implement `AIAdvisoryProvider` without leaking
provider-specific payloads into domain, workspace, lifecycle, or replay code.

Future persistence work must store advisory artifacts as advisory provenance
records, not canonical event-ledger truth.
