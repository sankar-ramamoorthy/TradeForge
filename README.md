# TradeForge Runtime
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/sankar-ramamoorthy/TradeForge)

> **Work in progress.** Core workflow is functional and demoable. Architecture and features are under active development.

TradeForge is an event-sourced, persona-driven, workflow-centric decision support system for discretionary trading and investing.

It is NOT:

* a generic trading bot
* a CRUD trade tracker
* a signal generator
* a dashboard-centric brokerage application
* an autonomous trading system

TradeForge is:

> a structured cognition and decision system for discretionary trading workflows — built around replayability, lifecycle integrity, and human decision sovereignty.

---

## What Works Now

* Full 7-stage decision lifecycle: **Idea → Thesis → Plan → Approval → Execution → Position → Review**
* Event-sourced workflow — all state derives from immutable ledger events
* Six operational workspaces with lifecycle progress tracking and contextual guidance
* New Trade Idea entry flow — no API calls required
* Active decision context that persists across workspace navigation
* Guided demo mode — seed a realistic AAPL breakout trade in one click
* Market context overlays through provider adapters, with yfinance available without credentials
* Deterministic replay and historical reconstruction
* Postgres-backed event ledger (optional; defaults to in-memory)
* AI advisory boundary: advisory interfaces, replay assistance, review assistance, provenance tracking, and OpenAI-compatible provider wiring through LiteLLM
* Advisory observation and cognitive evidence layer: observations, evidence attachments, provenance, uncertainty, replay-visible capture facts, conflict markers, staleness visibility, advisory artifacts, and advisory candidate review
* Contextual interpretation and thesis influence layer: interpretation artifacts, contextual weighting, confidence ranges, regime-aware weighting suggestions, conflict summaries, drift signals, cognition summaries, and reasoning timelines

AI and advisory outputs remain non-canonical. They cannot approve plans, execute trades, mutate lifecycle state, or write authoritative decision events.

---

## Try It (Two Terminals)

No broker account, no API keys, no database required. The default runtime uses an in-memory event store.

**Terminal 1 — Backend**

```bash
uv sync
uv run uvicorn src.app.api.application:app --host 127.0.0.1 --port 8000 --reload
```

**Terminal 2 — Frontend**

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173** in your browser.

**Demo flow:**
1. The Operating Workspace opens. Click **"Start Demo"** to seed an AAPL breakout scenario (seeds Idea → Thesis → Plan in one click).
2. You land in Plan Review at the Plan stage — progress strip shows `✓ Idea  ✓ Thesis  ● Plan`.
3. Click **Authorize Plan** → **Record Execution** → auto-navigated to Active Position.
4. Click **Record Position Opened** → **Begin Position Review** → auto-navigated to Review.
5. Complete the review. The full lifecycle runs in under two minutes.

Or start a fresh decision with the **New Trade Idea** button (top right of Operating Workspace).

> **Note:** the event store is in-memory by default. Restarting the backend clears all decisions. Click "×" on the sidebar badge to clear and start fresh.

---

## Architecture

### Core principles

**Event sourcing** — All durable state derives from immutable events. The event ledger is canonical truth. Projections are derived and discardable.

**Decision lifecycle integrity** — The canonical lifecycle is `Idea → Thesis → Plan → Approval → Execution → Position → Review`. Stages cannot be collapsed or bypassed.

**Replayability** — All material workflows support deterministic reconstruction from event history. Replay does not depend on live APIs or mutable external state.

**AI is advisory only** — AI may summarize, rank, and contextualize. It may not mutate canonical state, bypass lifecycle controls, execute trades, or override deterministic rules. Human decision sovereignty is mandatory.

**Workspace-centric, not dashboard-centric** — Workspaces are operational cognition environments, not generic screens or tabs.

---

### Repository structure

```
src/
├── app/           HTTP boundary (FastAPI)
├── domain/        Pure domain model — events, lifecycle, personas
├── infrastructure/  Adapters — event store, market data, persistence
└── services/      Orchestration — lifecycle, replay, workspace, market

frontend/
└── src/           React workspace runtime

tests/             Pytest regression and integration suite
DOCS/
└── adr/           Architecture Decision Records
```

---

### Layer rules

| Layer | Owns | Must not |
|---|---|---|
| `domain/` | entities, value objects, lifecycle rules, event types, advisory contracts | import infrastructure, persistence, or framework code |
| `services/` | workflow orchestration, projection services, advisory capture/query flows | own persistence or define domain rules |
| `infrastructure/` | event store, advisory stores, market adapters, Postgres | redefine domain semantics |
| `app/` | HTTP routes, FastAPI wiring | own domain rules or lifecycle authority |
| `frontend/` | workspace UI, API consumption | treat browser state as canonical truth |

---

## Developer Setup

### Prerequisites

* Python 3.12+ with [uv](https://docs.astral.sh/uv/)
* Node.js 18+ with npm
* Docker + Docker Compose (optional — only needed for Postgres)

### Backend

```bash
uv sync
uv run pytest
uv run ruff check .        # lint
uv run mypy src tests      # type check
```

Provider keys are optional for the default `yfinance` workflow. For Polygon,
Alpaca, or other credentialed providers, follow
[`HOW-TO-SETUP-KEYS.md`](HOW-TO-SETUP-KEYS.md).

For AI advisory generation, configure a LiteLLM/OpenAI-compatible endpoint with
the encrypted credential store:

```bash
uv run python scripts/manage_credentials.py register litellm --base-url "http://localhost:4000" --api-key "<litellm-key>" --default-model "<model-name>"
```

Without a configured LiteLLM credential, lifecycle, market context, replay, and
manual advisory workflows still run; AI generation endpoints report advisory
service as not configured.

### Frontend

```bash
cd frontend
npm install
npm run typecheck
npm run lint
npm run build
```

### With Postgres (optional)

```bash
docker compose up -d postgres
uv run alembic upgrade head
```

Then start the backend as normal — it will use Postgres for the event ledger.

### ADRs

Architecture decisions are recorded in `DOCS/adr/`. Read them before making structural changes.

Key ADRs:
* `0001` — Event sourcing core model
* `0002` — Decision lifecycle engine
* `0006` — AI advisory boundary model
* `0008` — Replay system design
* `0032` — External provider boundary model
* `0041` — Advisory observation and cognitive evidence foundation
* `0042` — Contextual interpretation and thesis influence

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
| M11 | Done | AI advisory boundary, replay/review assistance, provenance |
| M12 | Done | Advisory observation and cognitive evidence layer |
| M13 | Done | Contextual interpretation and thesis influence |
| M14+ | Planned | Behavioral intelligence, cognitive replay, attention allocation, simulation |

---

## Contributing

This is a solo architectural project in active development. The codebase is public for transparency and learning, not for general contribution at this stage.

If you have questions or observations, open an issue.

---

*TradeForge — structured cognition for discretionary trading.*
