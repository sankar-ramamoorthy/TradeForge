from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import datetime

from src.domain.advisory.contracts import AdvisoryAuthority
from src.domain.advisory.observation import (
    AdvisoryCaptureOrigin,
    AdvisoryObservation,
    AdvisoryUncertaintyBand,
    CognitiveEvidence,
    ObservationKind,
)


@dataclass(frozen=True, slots=True)
class AdvisoryCandidate:
    candidate_id: str
    symbol: str
    summary: str
    rationale: str
    evidence: tuple[CognitiveEvidence, ...]
    capture_origin: AdvisoryCaptureOrigin
    provenance_summary: str
    uncertainty_band: AdvisoryUncertaintyBand
    caveats: tuple[str, ...]
    persona_id: str
    workspace_id: str
    captured_at: datetime
    source_observation_ids: tuple[str, ...] = field(default_factory=tuple)
    tags: tuple[str, ...] = field(default_factory=tuple)
    authority: AdvisoryAuthority = AdvisoryAuthority.ADVISORY

    def __post_init__(self) -> None:
        _require_non_empty("candidate_id", self.candidate_id)
        _require_non_empty("symbol", self.symbol)
        _require_non_empty("summary", self.summary)
        _require_non_empty("rationale", self.rationale)
        _require_non_empty("provenance_summary", self.provenance_summary)
        _require_non_empty("persona_id", self.persona_id)
        _require_non_empty("workspace_id", self.workspace_id)
        if not self.evidence:
            raise ValueError("evidence must not be empty")
        if self.authority is not AdvisoryAuthority.ADVISORY:
            raise ValueError("advisory candidates must remain advisory")

        object.__setattr__(self, "symbol", self.symbol.strip().upper())
        object.__setattr__(self, "evidence", tuple(self.evidence))
        object.__setattr__(
            self,
            "caveats",
            _normalized_non_empty_tuple("caveats", self.caveats),
        )
        object.__setattr__(
            self,
            "source_observation_ids",
            tuple(
                source_id.strip()
                for source_id in self.source_observation_ids
                if source_id.strip()
            ),
        )
        object.__setattr__(
            self,
            "tags",
            tuple(tag.strip() for tag in self.tags if tag.strip()),
        )

    @property
    def is_advisory(self) -> bool:
        return True

    @property
    def is_canonical(self) -> bool:
        return False

    def to_observation(self) -> AdvisoryObservation:
        return AdvisoryObservation(
            observation_id=self.candidate_id,
            artifact_id=f"artifact-{self.candidate_id}",
            observation_kind=ObservationKind.ADVISORY_CANDIDATE,
            content=json.dumps(
                {
                    "symbol": self.symbol,
                    "summary": self.summary,
                    "rationale": self.rationale,
                    "source_observation_ids": list(self.source_observation_ids),
                },
                sort_keys=True,
            ),
            evidence=self.evidence,
            capture_origin=self.capture_origin,
            provenance_summary=self.provenance_summary,
            uncertainty_band=self.uncertainty_band,
            caveats=self.caveats,
            persona_id=self.persona_id,
            workspace_id=self.workspace_id,
            captured_at=self.captured_at,
            tags=self.tags,
        )

    @classmethod
    def from_observation(cls, observation: AdvisoryObservation) -> AdvisoryCandidate:
        if observation.observation_kind is not ObservationKind.ADVISORY_CANDIDATE:
            raise ValueError("observation is not an advisory candidate")
        try:
            content = json.loads(observation.content)
        except json.JSONDecodeError as exc:
            raise ValueError("candidate content is not valid JSON") from exc
        if not isinstance(content, dict):
            raise ValueError("candidate content must be an object")
        source_observation_ids = content.get("source_observation_ids", [])
        if not isinstance(source_observation_ids, list):
            raise ValueError("candidate source_observation_ids must be a list")
        return cls(
            candidate_id=observation.observation_id,
            symbol=str(content["symbol"]),
            summary=str(content["summary"]),
            rationale=str(content["rationale"]),
            evidence=observation.evidence,
            capture_origin=observation.capture_origin,
            provenance_summary=observation.provenance_summary,
            uncertainty_band=observation.uncertainty_band,
            caveats=observation.caveats,
            persona_id=observation.persona_id,
            workspace_id=observation.workspace_id,
            captured_at=observation.captured_at,
            source_observation_ids=tuple(str(item) for item in source_observation_ids),
            tags=observation.tags,
        )


def _require_non_empty(name: str, value: str) -> None:
    if not value.strip():
        raise ValueError(f"{name} must not be empty")


def _normalized_non_empty_tuple(name: str, values: Iterable[str]) -> tuple[str, ...]:
    normalized = tuple(value.strip() for value in values if value.strip())
    if not normalized:
        raise ValueError(f"{name} must not be empty")
    return normalized
