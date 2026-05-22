from __future__ import annotations

from src.domain.advisory import (
    AdvisoryArtifact,
    AdvisoryArtifactQuery,
    AdvisoryArtifactStore,
)


class InMemoryAdvisoryArtifactStore:
    """Non-canonical in-memory advisory artifact store."""

    def __init__(self) -> None:
        self._artifacts: dict[str, AdvisoryArtifact] = {}

    def persist(self, artifact: AdvisoryArtifact) -> None:
        self._artifacts[artifact.artifact_id] = artifact

    def get(self, artifact_id: str) -> AdvisoryArtifact | None:
        return self._artifacts.get(artifact_id)

    def list(self, query: AdvisoryArtifactQuery) -> tuple[AdvisoryArtifact, ...]:
        records = [
            artifact
            for artifact in self._artifacts.values()
            if _matches(query, artifact)
        ]
        return tuple(
            sorted(
                records,
                key=lambda artifact: (
                    -artifact.captured_at.timestamp(),
                    artifact.artifact_id,
                ),
            )
        )


def _matches(query: AdvisoryArtifactQuery, artifact: AdvisoryArtifact) -> bool:
    if artifact.persona_id != query.persona_id:
        return False
    if artifact.workspace_id != query.workspace_id:
        return False
    if (
        query.artifact_type is not None
        and artifact.artifact_type is not query.artifact_type
    ):
        return False
    if (
        query.artifact_format is not None
        and artifact.artifact_format is not query.artifact_format
    ):
        return False
    if (
        query.capture_origin is not None
        and artifact.capture_origin is not query.capture_origin
    ):
        return False
    return True


def store_satisfies_protocol(
    store: AdvisoryArtifactStore,
) -> AdvisoryArtifactStore:
    return store
