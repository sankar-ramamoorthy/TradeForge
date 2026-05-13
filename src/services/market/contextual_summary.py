from __future__ import annotations

from dataclasses import dataclass

from src.domain.events import EventStore
from src.domain.personas import PersonaContext
from src.services.market.context import MarketContextRequest
from src.services.market.snapshot_service import MarketSnapshotService
from src.services.workspace_engine.routing import WorkspaceRouteId
from src.services.workspace_engine.summaries import WorkspaceSummaryReadService


@dataclass(frozen=True, slots=True)
class MarketContextNote:
    """Advisory market context annotation for a single symbol.

    Always advisory — close price and regime are non-canonical derived context.
    """

    symbol: str
    close: str
    regime: str
    provider_id: str
    data_as_of_iso: str
    is_advisory: bool = True


@dataclass(frozen=True, slots=True)
class ContextualOperationalSummary:
    """Combined workspace state + advisory market context operational summary.

    Combines the operating workspace summary (derived from event history)
    with optional market context notes (advisory from provider). Neither
    component is canonical truth. Does not authorize lifecycle transitions.
    """

    authority: str
    persona_id: str
    workspace_id: str
    operational_headline: str
    operational_details: tuple[str, ...]
    market_context_notes: tuple[MarketContextNote, ...]
    market_context_available: bool
    source_inputs: tuple[str, ...]
    authority_boundaries: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "operational_details", tuple(self.operational_details))
        object.__setattr__(
            self, "market_context_notes", tuple(self.market_context_notes)
        )
        object.__setattr__(self, "source_inputs", tuple(self.source_inputs))
        object.__setattr__(
            self, "authority_boundaries", tuple(self.authority_boundaries)
        )


_AUTHORITY_BOUNDARIES = (
    "Contextual summary is derived state, not canonical truth.",
    "Market context is advisory and non-authoritative.",
    "Summary does not authorize lifecycle transitions or execution.",
)


class ContextualSummaryService:
    """Combines workspace operational summaries with advisory market context.

    Wraps WorkspaceSummaryReadService and an optional MarketSnapshotService.
    When market snapshot service is absent or no symbols are requested,
    market context notes are empty and the summary remains workspace-only.
    """

    def __init__(
        self,
        event_store: EventStore,
        market_snapshot_service: MarketSnapshotService | None = None,
    ) -> None:
        self._workspace_summary_svc = WorkspaceSummaryReadService(event_store)
        self._market_svc = market_snapshot_service

    def summarize_for(
        self,
        persona_context: PersonaContext,
        symbols: tuple[str, ...] = (),
    ) -> ContextualOperationalSummary:
        """Return a contextual operational summary for the given persona context.

        Workspace summary is always derived from event history. Market context
        notes are added when symbols are requested and a market service is
        available; absent market data produces an empty market_context_notes tuple.
        """
        summary_set = self._workspace_summary_svc.summaries_for(persona_context)
        operating = summary_set.summaries.get(WorkspaceRouteId.OPERATING)

        market_notes = self._fetch_market_notes(symbols)

        return ContextualOperationalSummary(
            authority="derived",
            persona_id=persona_context.profile.persona_version.persona_id,
            workspace_id=persona_context.workspace_id,
            operational_headline=(
                operating.headline if operating else "No operational context available"
            ),
            operational_details=operating.details if operating else (),
            market_context_notes=market_notes,
            market_context_available=bool(market_notes),
            source_inputs=(
                ("workspace_summaries", "market_context")
                if market_notes
                else ("workspace_summaries",)
            ),
            authority_boundaries=_AUTHORITY_BOUNDARIES,
        )

    def _fetch_market_notes(
        self, symbols: tuple[str, ...]
    ) -> tuple[MarketContextNote, ...]:
        if not symbols or self._market_svc is None:
            return ()
        try:
            result = self._market_svc.fetch_context(
                MarketContextRequest(symbols=symbols)
            )
            return tuple(
                MarketContextNote(
                    symbol=snap.symbol,
                    close=str(snap.price.close),
                    regime=snap.regime.value,
                    provider_id=snap.provider_id,
                    data_as_of_iso=snap.provenance.data_as_of.isoformat(),
                )
                for snap in result.available
            )
        except Exception:
            return ()
