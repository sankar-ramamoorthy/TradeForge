from datetime import UTC, datetime
from pathlib import Path

from src.domain.advisory import (
    AdvisoryArtifactKind,
    AdvisoryAuthority,
    AdvisoryProvenance,
    AdvisoryProvenanceRecord,
    AdvisoryResponse,
    AdvisorySourceKind,
    AdvisorySourceReference,
    AdvisoryUncertainty,
)
from src.infrastructure.advisory import InMemoryAdvisoryProvenanceStore
from src.services.advisory import AdvisoryProvenanceService


def _response(
    request_id: str = "request-1",
    artifact_kind: AdvisoryArtifactKind = AdvisoryArtifactKind.REPLAY_SUMMARY,
    source_id: str = "sequence:1",
) -> AdvisoryResponse:
    return AdvisoryResponse(
        request_id=request_id,
        artifact_kind=artifact_kind,
        content="Advisory content.",
        provenance=AdvisoryProvenance(
            provider_id="test-ai",
            provider_version="0.1",
            model_id="test-model",
            generated_at=datetime(2026, 5, 19, 18, 0, tzinfo=UTC),
        ),
        uncertainty=AdvisoryUncertainty(
            confidence=0.6,
            caveats=("Stored as advisory provenance only.",),
        ),
        source_references=(
            AdvisorySourceReference(
                source_kind=AdvisorySourceKind.REPLAY_TIMELINE_ENTRY,
                source_id=source_id,
            ),
        ),
    )


def test_advisory_provenance_records_remain_non_canonical() -> None:
    record = AdvisoryProvenanceRecord(
        response=_response(),
        recorded_at=datetime(2026, 5, 19, 18, 1, tzinfo=UTC),
    )

    assert record.authority is AdvisoryAuthority.ADVISORY
    assert record.provider_id == "test-ai"
    assert not hasattr(record, "event_type")
    assert not hasattr(record, "append")


def test_in_memory_advisory_provenance_store_queries_records() -> None:
    store = InMemoryAdvisoryProvenanceStore()
    service = AdvisoryProvenanceService(store)
    replay_record = service.record_response(
        _response(),
        recorded_at=datetime(2026, 5, 19, 18, 1, tzinfo=UTC),
    )
    review_record = service.record_response(
        _response(
            request_id="request-2",
            artifact_kind=AdvisoryArtifactKind.REVIEW_ASSISTANCE,
            source_id="review:decision-123",
        ),
        recorded_at=datetime(2026, 5, 19, 18, 2, tzinfo=UTC),
    )

    assert service.get("request-1") == replay_record
    assert service.list_by_artifact_kind(
        AdvisoryArtifactKind.REVIEW_ASSISTANCE
    ) == (review_record,)
    assert service.list_by_source(
        AdvisorySourceKind.REPLAY_TIMELINE_ENTRY,
        "sequence:1",
    ) == (replay_record,)


def test_advisory_provenance_boundaries_do_not_import_authority_layers() -> None:
    domain_text = Path("src/domain/advisory/provenance.py").read_text(
        encoding="utf-8"
    )
    service_text = Path("src/services/advisory/provenance.py").read_text(
        encoding="utf-8"
    )
    adapter_text = Path(
        "src/infrastructure/advisory/in_memory_provenance_store.py"
    ).read_text(encoding="utf-8")

    for module_text in (domain_text, service_text, adapter_text):
        assert "src.app" not in module_text
        assert "src.services.lifecycle" not in module_text
        assert "EventStore" not in module_text
        assert ".append(" not in module_text
