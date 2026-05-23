from __future__ import annotations

from dataclasses import dataclass

from src.domain.advisory.interpretation import ContextualWeight
from src.domain.market.snapshot import MarketRegime


@dataclass(frozen=True, slots=True)
class RegimeWeightSuggestion:
    """Advisory suggestion for contextual weight given market regime.

    Non-canonical — operator decides whether to apply the suggestion.
    """

    suggested_weight: ContextualWeight
    regime: MarketRegime
    rationale: str
    is_advisory: bool = True
    is_canonical: bool = False


_REGIME_WEIGHT_MAP: dict[MarketRegime, tuple[ContextualWeight, str]] = {
    MarketRegime.BULL: (
        ContextualWeight.HIGH,
        "Bull regime: price action and momentum observations typically carry high weight.",  # noqa: E501
    ),
    MarketRegime.BEAR: (
        ContextualWeight.WATCH,
        "Bear regime: risk and downside observations warrant close attention; "
        "upside observations should be treated cautiously.",
    ),
    MarketRegime.RANGING: (
        ContextualWeight.MEDIUM,
        "Ranging regime: observations have moderate weight; "
        "breakout confirmation is needed before elevating.",
    ),
    MarketRegime.HIGH_VOLATILITY: (
        ContextualWeight.WATCH,
        "High-volatility regime: all observations require heightened scrutiny; "
        "signals may reverse quickly.",
    ),
    MarketRegime.LOW_VOLATILITY: (
        ContextualWeight.LOW,
        "Low-volatility regime: context observations have lower urgency; "
        "conditions may persist but offer limited edge.",
    ),
    MarketRegime.UNKNOWN: (
        ContextualWeight.MEDIUM,
        "Unknown regime: insufficient context to adjust weight; "
        "apply standard medium weight until regime is clearer.",
    ),
}


class RegimeContextWeightService:
    """Suggests ContextualWeight for advisory interpretations based on market regime.

    This is an advisory-only service. It does not automatically apply weights
    to interpretations. The operator reviews the suggestion and assigns weight
    during interpretation capture.
    """

    def suggest_weight(self, regime: MarketRegime) -> RegimeWeightSuggestion:
        weight, rationale = _REGIME_WEIGHT_MAP[regime]
        return RegimeWeightSuggestion(
            suggested_weight=weight,
            regime=regime,
            rationale=rationale,
        )
