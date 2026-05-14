 Now I have the full picture. Let me give you a clear, honest rundown of the current demo experience.

  ---
  Running TradeForge as a Swing Trader

  What exists right now

  The full M9 stack is functional: event-sourced lifecycle, 6 workspaces, market context overlays with regime
  classification, provenance tracking, and snapshot persistence. However, the UI is backend-first — there is no "New
  Trade Idea" button yet. You bootstrap a decision via a direct API call, then the workspaces drive everything from
  there. That one seam is honest to document.

  ---
  Step 1 — Start the backend

  No Postgres needed — the default app uses an in-memory event store.

  uv run uvicorn src.app.api.application:app --host 127.0.0.1 --port 8000 --reload

  You'll see the FastAPI startup. The backend is now running at http://localhost:8000. The interactive API docs are at
  http://localhost:8000/docs.

  ---
  Step 2 — Start the frontend

  cd frontend
  npm install   # first time only
  npm run dev

  Open http://localhost:5173. You'll see the Operating Workspace — the daily attention surface. It'll be empty (no
  decisions yet).

  ---
  Step 3 — Seed a trade idea (the one manual step)

  This is the current bootstrap gap. Post an Idea lifecycle event via the API. You can do this from the Swagger docs at
  http://localhost:8000/docs or via curl:

	  curl -X POST http://localhost:8000/lifecycle/transitions `
		-H "Content-Type: application/json" `
		-d '{
		  "requested_stage": "Idea",
		  "persona_id": "persona.swing",
		  "workspace_id": "workspace.operating",
		  "entity_references": [{"entity_type": "decision", "entity_id": "swing-001"}],
		  "payload": {"symbol": "AAPL", "thesis_seed": "Breakout above 200d MA on volume"},
		  "provenance": {"actor": "human", "source": "manual-seed"}
		}'
		
 Invoke-RestMethod -Method Post -Uri "http://localhost:8000/lifecycle/transitions" -Headers @{"Content-Type"="application/json"} -Body ('{"requested_stage":"Idea","persona_id":"persona.swing","workspace_id":"workspace.operating","timestamp":"' + (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ") + '","entity_references":[{"entity_type":"decision","entity_id":"swing-001"}],"payload":{"symbol":"AAPL","thesis_seed":"Breakout above 200d MA on volume"},"provenance":{"actor":"human","source":"manual-seed"}}')
 

  After this, refresh the Operating Workspace — it will show an attention item directing you to the Opportunity
  Workspace.

  ---
  Step 4 — Walk through the lifecycle

  The workspace URLs carry context via query params. The nav sidebar links to each workspace. To maintain context across
   workspaces, append these params to the URL (or click the nav links after the first workspace loads them):

  ?persona_id=persona.swing&persona_version=v1&workspace_id=workspace.operating&decision_id=swing-001

  Operating Workspace (/operating) — your daily attention surface. Shows what needs your decision right now. After
  seeding the idea, you'll see "New Idea: develop thesis."

  Opportunity Workspace (/opportunity) — pre-decision cognition surface. Loads your workspace projection showing the
  Idea stage. Click "Develop Thesis" to advance to Thesis stage. The market context panel is on this screen — enter AAPL
   (or any symbol) to pull advisory OHLCV data and regime classification.

  Plan Review Workspace (/plan-review) — risk authorization surface. From Thesis stage, click "Create Plan" → then
  "Authorize Plan" (deliberate two-step, framed as risk acceptance not a brokerage BUY button).

  Active Position Workspace (/active-position) — supervision surface. Click "Record Execution" then "Record Position
  Opened". The market context panel here lets you track the current price against your thesis.

  Replay Workspace (/replay) — full event timeline of everything that happened. See each lifecycle transition in
  sequence, with timestamps and provenance. Verify the history is intact.

  Review Workspace (/review) — reflection surface. Click "Complete Review" to close the workflow with a durable review
  event. The system explicitly separates decision quality from outcome.

  ---
  Using the seeded demo (no internet required)

  The SeededMarketDataProvider (TF-0051) gives you deterministic data for AAPL, TSLA, NVDA, SPY, QQQ, GLD, TLT without
  live API calls. To run the backend in seeded mode, create a small startup script:

  # run_demo.py  (in the TradeForge root)
  import uvicorn
  from src.app.api.application import create_app
  from src.infrastructure.market.in_memory_snapshot_store import InMemoryMarketSnapshotStore
  from src.infrastructure.market.seeded_provider import SeededMarketDataProvider
  from src.infrastructure.market.in_memory_provenance_store import InMemoryProvenanceStore
  from src.services.market.regime_interpreter import SingleBarRegimeInterpreter
  from src.services.market.snapshot_service import MarketSnapshotService
  from src.services.market.snapshot_query import MarketSnapshotQueryService
  from src.services.market.provenance_query import ProvenanceQueryService

  prov_store = InMemoryProvenanceStore()
  snap_store = InMemoryMarketSnapshotStore()
  market_svc = MarketSnapshotService(
      SeededMarketDataProvider(),
      SingleBarRegimeInterpreter(),
      provenance_store=prov_store,
      snapshot_persistence_store=snap_store,
  )
  app = create_app(
      market_snapshot_service=market_svc,
      provenance_query_service=ProvenanceQueryService(prov_store),
      market_snapshot_query_service=MarketSnapshotQueryService(snap_store),
  )

  if __name__ == "__main__":
      uvicorn.run(app, host="127.0.0.1", port=8000)

  uv run python run_demo.py

  In the market context panels, enter any of: AAPL, TSLA, NVDA, SPY, QQQ, GLD, TLT. Each returns a different regime
  (BULL, HIGH_VOLATILITY, RANGING, BEAR, LOW_VOLATILITY) so the advisory overlay is visually meaningful even without
  live data.

  ---
  What the advisory endpoints show

  Once market data is fetched, you can inspect the advisory layer directly:

  Endpoint: GET /workspaces/market-context?symbols=AAPL,TSLA
  What it shows: OHLCV + regime per symbol
  ────────────────────────────────────────
  Endpoint: GET
    /workspaces/contextual-summary?persona_id=persona.swing&persona_version=v1&workspace_id=workspace.operating&symbols=
  AAPL
  What it shows: Combined workspace state + market notes
  ────────────────────────────────────────
  Endpoint: GET /provenance/market-data
  What it shows: Every fetch interaction this session
  ────────────────────────────────────────
  Endpoint: GET /market/snapshots
  What it shows: Full OHLCV archive with persistence IDs

  ---
  Honest gaps at this stage

  Gap: No "New Trade Idea" button in UI
  Impact: Requires one curl or Swagger call to bootstrap
  ────────────────────────────────────────
  Gap: No multi-decision selector
  Impact: Only one active decision at a time in the demo
  ────────────────────────────────────────
  Gap: No ticker auto-extraction from lifecycle events
  Impact: You manually type symbols into the market panels
  ────────────────────────────────────────
  Gap: In-memory only
  Impact: Restart loses all state; Postgres wiring (TF-0024-0026) exists but isn't used in the default demo mode
  ────────────────────────────────────────
  Gap: No authentication UI
  Impact: Local session provider only; no login screen

  These are M10+ territory items, not gaps in what was promised for M9.

  ---
  The swing trader experience in a sentence

  You post one API call to start a trade idea on AAPL, then click through six workspaces that enforce your own process —
   develop thesis, review risk, authorize deliberately, supervise the position, replay the decision, reflect on it. The
  market context panels give you advisory OHLCV and regime context at each stage. Nothing executes for you. That's the
  point.
