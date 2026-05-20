from __future__ import annotations

from src.domain.advisory import (
    AdvisoryInterpretation,
    AdvisoryInterpretationQuery,
    AdvisoryInterpretationStore,
)


class InMemoryAdvisoryInterpretationStore:
    """Non-canonical in-memory advisory interpretation artifact store."""

    def __init__(self) -> None:
        self._interpretations: dict[str, AdvisoryInterpretation] = {}

    def persist(self, interpretation: AdvisoryInterpretation) -> None:
        self._interpretations[interpretation.interpretation_id] = interpretation

    def get(self, interpretation_id: str) -> AdvisoryInterpretation | None:
        return self._interpretations.get(interpretation_id)

    def list(
        self,
        query: AdvisoryInterpretationQuery,
    ) -> tuple[AdvisoryInterpretation, ...]:
        records = [
            interpretation
            for interpretation in self._interpretations.values()
            if _matches(query, interpretation)
        ]
        return tuple(sorted(records, key=lambda item: item.captured_at))


def _matches(
    query: AdvisoryInterpretationQuery,
    interpretation: AdvisoryInterpretation,
) -> bool:
    if interpretation.persona_id != query.persona_id:
        return False
    if interpretation.workspace_id != query.workspace_id:
        return False
    if (
        query.decision_id is not None
        and interpretation.decision_id != query.decision_id
    ):
        return False
    if query.thesis_id is not None and interpretation.thesis_id != query.thesis_id:
        return False
    if (
        query.observation_id is not None
        and query.observation_id not in interpretation.observation_ids
    ):
        return False
    if (
        query.interpretation_kind is not None
        and interpretation.interpretation_kind is not query.interpretation_kind
    ):
        return False
    if (
        query.thesis_influence is not None
        and interpretation.thesis_influence is not query.thesis_influence
    ):
        return False
    if (
        query.capture_origin is not None
        and interpretation.capture_origin is not query.capture_origin
    ):
        return False
    if query.source_kind is not None and query.source_kind not in (
        interpretation.source_kinds
    ):
        return False
    return True


def store_satisfies_protocol(
    store: AdvisoryInterpretationStore,
) -> AdvisoryInterpretationStore:
    return store
