# ADR 0011: Runtime Development Environment

## Status
Accepted

## Context
TradeForge needs a reproducible local runtime foundation before domain implementation begins. The repository is expected to use Python, `uv`, Docker, and Docker Compose for development and test execution.

This environment decision supports implementation consistency, but it does not define TradeForge semantics. Event sourcing, lifecycle authority, workspace meaning, persona interpretation, scenario boundaries, replay rules, and AI governance remain defined by the knowledge base and ADRs 0001 through 0010.

Without an explicit environment decision, early implementation work could drift across local Python versions, dependency managers, container assumptions, and test commands.

## Decision
TradeForge will use `uv`, `pyproject.toml`, Docker Compose, and a Python 3.12 slim `uv` base image for reproducible local development.

The runtime Dockerfile will use:

```text
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
```

The development environment will provide:

- Python project metadata in `pyproject.toml`
- dependency management through `uv`
- local service orchestration through `docker-compose.yml`
- a repeatable test command
- documented developer setup commands
- lint, type, and development command conventions

This decision is infrastructure-scoped only. Docker, Compose, and `uv` are execution environment tools. They do not define event semantics, lifecycle rules, domain models, workspace behavior, AI authority, or canonical truth.

## Rationale
A reproducible runtime foundation should exist before the first domain implementation issue. This keeps the event model and lifecycle code testable from the beginning and prevents environment-specific assumptions from leaking into domain design.

Using `uv` keeps Python dependency and command execution fast and consistent. Using Docker Compose provides a stable local development entrypoint that can later host infrastructure services without forcing distributed architecture prematurely.

Keeping this ADR infrastructure-scoped preserves the TradeForge truth hierarchy: environment tooling supports implementation but never overrides semantic or architectural rules.

## Alternatives Considered
Ad hoc local Python setup was rejected because it would make tests and dependency management inconsistent across machines.

Pip-only dependency management was rejected because the project intends to standardize on `uv`.

Deferring Docker until later was rejected because container assumptions are expected soon and should be captured before runtime code begins.

Treating Docker Compose as architectural distribution was rejected because TradeForge remains a modular monolith unless future ADRs explicitly decide otherwise.

Encoding domain rules in Docker, Compose, or project tooling was rejected because environment tooling must not define system semantics.

## Consequences
Runtime implementation begins with environment scaffold issues before domain code.

Domain issues can rely on a repeatable Python, `uv`, Docker, and test baseline.

Future infrastructure additions must preserve the distinction between execution environment and domain architecture.

The environment may evolve, but changes must remain documented and must not redefine TradeForge invariants.
