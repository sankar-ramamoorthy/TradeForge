from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from src.domain.market.capability import ProviderCapability
from src.domain.market.fundamentals import FundamentalsBundle
from src.domain.market.provider import (
    FundamentalsDataProvider,
    ProviderUnavailableError,
)
from src.domain.market.registry import ProviderRegistry


@dataclass(frozen=True, slots=True)
class FundamentalsFetchResult:
    symbol: str
    bundle: FundamentalsBundle | None
    attempted_provider_ids: tuple[str, ...]
    selected_provider_id: str | None
    error_reasons: tuple[str, ...]
    fetched_at: datetime

    @property
    def is_available(self) -> bool:
        return self.bundle is not None

    @property
    def used_fallback(self) -> bool:
        return (
            self.selected_provider_id is not None
            and bool(self.attempted_provider_ids)
            and self.selected_provider_id != self.attempted_provider_ids[0]
        )


class FundamentalsService:
    def __init__(
        self,
        registry: ProviderRegistry,
        providers: dict[str, FundamentalsDataProvider],
    ) -> None:
        self._registry = registry
        self._providers = providers

    def fetch(self, symbol: str) -> FundamentalsFetchResult:
        resolution = self._registry.resolve(ProviderCapability.FUNDAMENTALS)
        attempted: list[str] = []
        errors: list[str] = []
        fetched_at = datetime.now(UTC)

        for provider_id in (
            resolution.preferred_provider_id,
            *resolution.fallback_provider_ids,
        ):
            provider = self._providers.get(provider_id)
            if provider is None:
                continue
            attempted.append(provider_id)
            try:
                bundle = provider.fetch_fundamentals(symbol)
                return FundamentalsFetchResult(
                    symbol=symbol.upper(),
                    bundle=bundle,
                    attempted_provider_ids=tuple(attempted),
                    selected_provider_id=provider_id,
                    error_reasons=tuple(errors),
                    fetched_at=fetched_at,
                )
            except ProviderUnavailableError as exc:
                errors.append(f"{provider_id}: {exc.reason}")

        return FundamentalsFetchResult(
            symbol=symbol.upper(),
            bundle=None,
            attempted_provider_ids=tuple(attempted),
            selected_provider_id=None,
            error_reasons=tuple(errors),
            fetched_at=fetched_at,
        )
