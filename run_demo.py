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