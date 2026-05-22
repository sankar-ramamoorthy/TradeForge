from __future__ import annotations

import hashlib
from dataclasses import replace

from src.domain.advisory import (
    AdvisoryArtifact,
    AdvisoryArtifactFormat,
    AdvisoryArtifactQuery,
    AdvisoryArtifactSnapshot,
    AdvisoryArtifactStore,
    AdvisoryArtifactType,
    AdvisoryCaptureOrigin,
)

_FORBIDDEN_ARTIFACT_FIELDS = frozenset(
    {
        "recommendation",
        "buy_sell_instruction",
        "lifecycle_transition_intent",
        "execution_authority",
        "approval_intent",
        "canonical_truth",
        "trade_idea",
    }
)


class AdvisoryArtifactIngestionService:
    """Persists non-canonical advisory artifacts with replay-safe snapshots."""

    def __init__(self, artifact_store: AdvisoryArtifactStore) -> None:
        self._artifact_store = artifact_store

    def ingest(self, artifact: AdvisoryArtifact) -> AdvisoryArtifact:
        _validate_artifact_boundary(artifact)
        with_snapshot = replace(
            artifact,
            snapshot=AdvisoryArtifactSnapshot(
                captured_at=artifact.captured_at,
                metadata=dict(artifact.metadata),
                source_reference_count=len(artifact.source_references),
                caveat_count=len(artifact.caveats),
                body_sha256=hashlib.sha256(
                    artifact.body.encode("utf-8")
                ).hexdigest(),
            ),
        )
        self._artifact_store.persist(with_snapshot)
        return with_snapshot


class AdvisoryArtifactQueryService:
    def __init__(self, artifact_store: AdvisoryArtifactStore) -> None:
        self._artifact_store = artifact_store

    def get(self, artifact_id: str) -> AdvisoryArtifact | None:
        if not artifact_id.strip():
            raise ValueError("artifact_id must not be empty")
        return self._artifact_store.get(artifact_id)

    def list(
        self,
        query: AdvisoryArtifactQuery,
    ) -> tuple[AdvisoryArtifact, ...]:
        return self._artifact_store.list(query)


def _validate_artifact_boundary(artifact: AdvisoryArtifact) -> None:
    if artifact.artifact_format is AdvisoryArtifactFormat.MARKDOWN:
        _reject_active_markdown(artifact.body)
    if artifact.artifact_type is AdvisoryArtifactType.GENERATED_ADVISORY and (
        artifact.capture_origin
        not in {
            AdvisoryCaptureOrigin.CODEX_GENERATED,
            AdvisoryCaptureOrigin.CLAUDE_GENERATED,
        }
    ):
        raise ValueError("generated artifacts require generated capture origin")
    if artifact.artifact_type is AdvisoryArtifactType.IMPORTED_RESEARCH and (
        artifact.capture_origin is not AdvisoryCaptureOrigin.IMPORTED_RESEARCH
    ):
        raise ValueError("imported research requires imported_research origin")

    forbidden = set(artifact.metadata).intersection(_FORBIDDEN_ARTIFACT_FIELDS)
    lowered_body = artifact.body.lower()
    if forbidden or any(field in lowered_body for field in _FORBIDDEN_ARTIFACT_FIELDS):
        raise ValueError(
            "advisory artifacts cannot bypass the decision lifecycle or "
            "assert canonical recommendation authority"
        )


def _reject_active_markdown(body: str) -> None:
    lowered = body.lower()
    if "<script" in lowered or "javascript:" in lowered:
        raise ValueError("markdown artifacts cannot contain executable script content")
