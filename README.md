# TradeForge Runtime
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/sankar-ramamoorthy/TradeForge)

> **Work in progress.** Core workflow is functional and demoable. Architecture and features are under active development.

TradeForge is an event-sourced, persona-driven decision support system for discretionary swing trading and investing.

It is **not** a trading bot, signal generator, broker integration, or autonomous execution system.

It is:

> A structured cognition and decision system — built around replayability, lifecycle integrity, and human decision sovereignty. It makes you write down why before you act, and holds you to it.

---

## What Works Now

### Decision lifecycle

Full 7-stage lifecycle: **Idea → Thesis → Plan → Approval → Execution → Position → Review**

- Start a new trade idea from the UI — no API calls, no curl
- Author a structured thesis: narrative, catalysts, assumptions, invalidation conditions, confidence, regime alignment
- Model conditional scenarios (primary, alternative, invalidation)
- Build a structured trade plan: entry rationale, stop rationale, target rationale, sizing rationale, execution assumptions
- Conditional execution state (Armed) — approved but waiting for trigger conditions
- Track position state through execution
- Structured review: thesis vs outcome, execution quality, discipline observations, lessons learned
- All lifecycle state derives from immutable events — replayable and auditable

### Replay

- Walk back through any completed decision and reconstruct what you believed at the time
- Replay reconstructs reasoning artifacts (thesis, scenarios, plan) alongside market context
- Does not depend on live APIs — pure event reconstruction

### Market context

- Price data via yfinance (no API key required), Polygon, or Alpaca
- Fundamentals via FMP or Alpha Vantage
- Capability-aware provider registry — price and fundamentals are separate contracts
- Context Workbench workspace for explicit advisory context acquisition
- Market regime interpretation (bull / bear / ranging / high-volatility)
- Provider provenance and fallback transparency surfaced in workspaces

### AI advisory (optional — requires LiteLLM or compatible endpoint)

Four on-demand advisory tasks, all accessible from workspaces:

- **Thesis review** — surfaces blind spots, missing assumptions, and regime misalignments in a structured thesis
- **Observation generation** — generates typed advisory observations (price action, fundamentals, risk, regime) for an instrument
- **Replay summary** — narrative summary of a completed decision replay
- **Candidate screening** — prioritizes the advisory candidate queue for operator attention

Advisory analytics on accumulated evidence:
- Thesis influence tracking (supporting / weakening / conflicting) over time
- Drift signal — detects when accumulated interpretations shift from supporting to weakening
- Conflict summary — flags opposing evidence for the same thesis
- Contextual reasoning timeline — chronological advisory reasoning per decision

All advisory outputs are non-canonical. They cannot approve plans, execute trades, mutate lifecycle state, or write authoritative decision events. Human decision sovereignty is mandatory.

### Advisory imports (local drop-folder)

Bring externally authored research into the Thesis and Plan workflows as non-canonical advisory artifacts:

- Drop markdown files into `imports/incoming/` (relative to the backend working directory)
- Files must declare front matter: `artifact_role: thesis_draft` with `schema_version: thesis_draft.v1` (or `artifact_role: plan_draft` with `schema_version: plan_draft.v1`) and a `symbol` matching the active workflow; plan drafts may pin a `decision_id`
- Scan on demand with the **Scan folder** action in the Thesis Development or Plan Development modal — no watchers, no background ingestion
- Thesis sections mapped deterministically from headings: Narrative, Catalysts, Assumptions, Invalidation Conditions, Evidence Links, Notes
- Plan sections mapped: entry, stop, and target rationale plus risk notes — prices, sizing, order, and approval fields are prohibited and never imported
- Thesis import previews show advisory source references, evidence links, notes, provenance, uncertainty, and caveats before field acceptance
- Accept, edit, or reject each imported field individually; manual submission remains the only lifecycle action
- Accepted/edited/rejected provenance rides on the normal `decision.thesis_created` / `decision.plan_created` event; replay labels it `Advisory source, operator-promoted thesis`

The sibling TradeForge Research Cockpit may produce advisory submissions and
TradeForge-compatible projections for this boundary. Those artifacts remain
non-canonical until TradeForge validates them, previews them for the operator,
and the operator submits a normal lifecycle action. Artifact delivery alone
does not create a Thesis, TradeIdea, approval, execution, or Event Ledger fact.

### Provider governance

- Dedicated **Provider Governance** surface at `/workspaces/provider-governance` — separate operational control plane, not a workspace rail
- Configure provider API keys from the browser — no terminal required after initial master key setup
- Masked field display (last 4 characters of secrets shown)
- Credential validation workflow — test a credential without saving, or validate an existing one on demand
- Provider registry reloads automatically after credential changes — no restart required
- Revoke credentials with audit trail preserved
- LiteLLM surfaced as an AI gateway with named route aliases — not treated as an ordinary data provider
- AI gateway route visibility: fast-summary, reasoning, long-context, and classification routes are distinguishable operational concerns
- Advisory route selection and smoke tests are exposed through Provider Governance and remain non-canonical
- Downstream LLM provider secrets are governed through the same encrypted boundary and resolved only for the individual advisory request that needs them
- Capability routing governance: `Credential != Provider != Capability != Model`
- Contextual rails show provider status, provenance, freshness, and a configure link — long-form administration lives in the governance surface

---

## Quick Start

No broker account, no API keys, no database required. The default runtime uses an in-memory event store and yfinance for market data.

**Terminal 1 — Backend**

```bash
uv sync
uv run uvicorn src.app.api.application:app --host 127.0.0.1 --port 8000 --reload
```

**Terminal 2 — Frontend**

```bash
npm run install:frontend
npm run dev
```

Open **http://localhost:5173**

**Demo flow:**
1. Operating Workspace opens. Click **Start Demo** to seed an AAPL breakout scenario (Idea → Thesis → Plan in one click).
2. Click **Authorize Plan → Record Execution** → auto-navigated to Active Position.
3. Click **Record Position Opened → Begin Position Review** → auto-navigated to Review.
4. Complete the structured review. Full lifecycle in under two minutes.

Or start a fresh decision with **New Trade Idea** (top right of Operating Workspace).

> Events are in-memory by default — restarting the backend clears decisions. Use Docker + Postgres for persistence.

---

## Developer Setup

### Prerequisites

- Python 3.12+ with [uv](https://docs.astral.sh/uv/)
- Node.js 18+ with npm
- Docker + Docker Compose (optional — only needed for Postgres)

### Backend

```bash
uv sync
uv run pytest
uv run ruff check .
uv run mypy src tests
```

### Frontend

```bash
npm run install:frontend
npm run typecheck
npm run lint
npm run build
```

### Credentials

**Master key** — generate once and set in the OS environment:

```bash
uv run python scripts/manage_credentials.py generate-master-key
# Copy the output and set it:
# Windows: $env:TRADEFORGE_MASTER_KEY = "<generated-value>"
# Linux/Mac: export TRADEFORGE_MASTER_KEY=<generated-value>
```

**Provider API keys** — enter from the UI (ProviderConfigurationPanel) once the master key is configured. Or via CLI:

```bash
uv run python scripts/manage_credentials.py register fmp --api-key "<key>"
uv run python scripts/manage_credentials.py register litellm \
  --base-url "http://litellm:4000" \
  --api-key "<key>"
```

Provider Governance stores advisory model selection separately from the LiteLLM
gateway credential. Select explicit provider/model pairs through TradeForge
without creating canonical event-ledger facts.

Downstream LLM provider keys can also be stored through the same encrypted
credential boundary using provider IDs such as `llm_groq`, `llm_nvidia_nim`,
`llm_openai`, `llm_anthropic`, and `llm_google`. TradeForge masks these values
in API/UI responses and decrypts them only inside the trusted backend advisory
request path. LiteLLM receives the required provider credential per
`/chat/completions` request; downstream provider keys are not configured in
LiteLLM environment variables or static config.

See [`HOW-TO-SETUP-KEYS.md`](HOW-TO-SETUP-KEYS.md) for full credential setup.

### With Postgres (recommended for real use)

```bash
docker compose up -d postgres
uv run alembic upgrade head
```

Start the backend normally — it uses Postgres for the event ledger when `TRADEFORGE_DATABASE_URL` is set.

### AI advisory

AI advisory requires an OpenAI-compatible endpoint — LiteLLM pointing at Groq, NVIDIA NIM, or Ollama. Configure the `litellm` credential (see above), then advisory endpoints become available in the UI.

To run LiteLLM through Docker Compose:

```bash
docker compose --profile advisory up -d litellm
```

Use `http://litellm:4000` as the LiteLLM base URL when TradeForge runs inside
Docker Compose. LiteLLM is not exposed on `localhost:4000` by default; browser
and operator workflows should go through TradeForge. For temporary local
inspection, start with the explicit debug override:

```bash
docker compose --profile advisory -f docker-compose.yml -f docker-compose.litellm-debug.yml up -d litellm
```

Without a LiteLLM credential: lifecycle, market context, replay, and manual advisory artifact workflows all work normally. AI generation endpoints report `not_configured`.

---

## Architecture

### Core principles

**Event sourcing** — All durable state derives from immutable events. The event ledger is canonical truth. Projections are derived and discardable.

**Decision lifecycle integrity** — `Idea → Thesis → Plan → Approval → Execution → Position → Review`. Stages cannot be collapsed or bypassed.

**Replayability** — All material workflows support deterministic reconstruction from event history. Replay does not depend on live APIs.

**AI is advisory only** — AI may summarize, rank, and contextualize. It may not mutate canonical state, approve plans, execute trades, or bypass lifecycle controls.

**Workspace-centric, not dashboard-centric** — Workspaces are operational cognition environments, not generic screens.

### Repository structure

```
src/
├── app/            HTTP boundary (FastAPI; per-domain routers in api/routes/)
├── domain/         Pure domain — events, lifecycle, advisory contracts
├── infrastructure/ Adapters — event store, market, advisory stores
├── security/       Credential boundary (KeyManager, CredentialStore)
└── services/       Orchestration — lifecycle, replay, workspace, advisory

frontend/
└── src/            React workspace runtime

tests/              Pytest suite (700+ tests)
DOCS/
├── adr/            Architecture Decision Records
└── *.md            Strategy and design documents
```

### Layer rules

| Layer | Owns | Must not |
|---|---|---|
| `domain/` | entities, lifecycle rules, event types, advisory contracts | import infrastructure, persistence, or framework code |
| `security/` | credential encryption, key management | import domain or service logic |
| `services/` | workflow orchestration, advisory capture/query | own persistence or define domain rules |
| `infrastructure/` | event store, advisory stores, market adapters, Postgres | redefine domain semantics |
| `app/` | HTTP routes, FastAPI wiring, composition root | own domain rules or lifecycle authority |
| `frontend/` | workspace UI, API consumption | treat browser state as canonical truth |

---

## Milestone Status

| Milestone | Status | Focus |
|---|---|---|
| M0–M1 | Done | Planning discipline, runtime scaffold |
| M2–M3 | Done | Event ledger, lifecycle engine |
| M4–M6 | Done | Workspace architecture, replay, persona projection |
| M7 | Done | Postgres, FastAPI, React runtime |
| M8 | Done | First replayable MVP lifecycle flow |
| M9 | Done | Market context, provider boundary, advisory overlays |
| M10 | Done | Operational UX, demoability, guided workflow |
| M10A–E | Done | Structured cognition, credential boundary, provider capability, context workbench |
| M11 | Done | AI advisory boundary, replay/review assistance, provenance |
| M12 | Done | Advisory observation and cognitive evidence layer |
| M13 | Done | Contextual interpretation and thesis influence |
| M13A | Done | Provider governance, AI gateway configuration, credential validation, route visibility |
| M13B | Done | Managed advisory runtime, route selection, governed provider secrets, and stateless LiteLLM request-time composition |
| M14 | Done | Behavioral intelligence and cognitive auditability |
| M15+ | Planned | Cognitive replay, attention allocation, simulation, adaptive research |

---

## Contributing

This is a solo architectural project in active development. The codebase is public for transparency and learning, not for general contribution at this stage.

If you have questions or observations, open an issue.

---

*TradeForge — structured cognition for discretionary trading.*
