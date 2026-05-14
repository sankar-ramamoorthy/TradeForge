from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class AnnotationType(StrEnum):
    OBSERVATION = "observation"
    QUESTION = "question"
    INSIGHT = "insight"
    POSTMORTEM = "postmortem"


ANNOTATION_TYPES = frozenset(t.value for t in AnnotationType)


class ReplayAnnotationArtifactValidationError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class ReplayAnnotationArtifact:
    """Replay-attached operator annotation on a specific timeline event.

    Annotations make replay cognitively interactive — operators record
    observations, questions, insights, and postmortem notes on any event.
    Stored as immutable enrichment events; not lifecycle transitions.
    """

    sequence: int
    annotated_event_type: str
    note: str
    annotation_type: AnnotationType

    @classmethod
    def create(
        cls,
        sequence: int,
        annotated_event_type: str,
        note: str,
        annotation_type: str,
    ) -> ReplayAnnotationArtifact:
        """Validate and create a ReplayAnnotationArtifact."""
        if sequence < 0:
            raise ReplayAnnotationArtifactValidationError(
                "sequence must be a non-negative integer"
            )

        annotated_event_type = annotated_event_type.strip()
        if not annotated_event_type:
            raise ReplayAnnotationArtifactValidationError(
                "annotated_event_type is required"
            )

        note = note.strip()
        if not note:
            raise ReplayAnnotationArtifactValidationError("note is required")

        if annotation_type not in ANNOTATION_TYPES:
            raise ReplayAnnotationArtifactValidationError(
                f"annotation_type must be one of: {', '.join(sorted(ANNOTATION_TYPES))}"
            )

        return cls(
            sequence=sequence,
            annotated_event_type=annotated_event_type,
            note=note,
            annotation_type=AnnotationType(annotation_type),
        )

    def to_payload(self) -> dict[str, object]:
        return {
            "annotation": {
                "sequence": self.sequence,
                "annotated_event_type": self.annotated_event_type,
                "note": self.note,
                "annotation_type": self.annotation_type.value,
            }
        }

    @classmethod
    def from_payload(
        cls, payload: dict[str, object]
    ) -> ReplayAnnotationArtifact | None:
        ann = payload.get("annotation")
        if not isinstance(ann, dict):
            return None

        note = ann.get("note", "")
        if not isinstance(note, str) or not note:
            return None

        sequence = ann.get("sequence", -1)
        annotated_event_type = ann.get("annotated_event_type", "")
        annotation_type = ann.get("annotation_type", "observation")

        if not isinstance(annotation_type, str) or annotation_type not in ANNOTATION_TYPES:
            return None

        return cls(
            sequence=int(sequence) if isinstance(sequence, int) else 0,
            annotated_event_type=str(annotated_event_type) if isinstance(annotated_event_type, str) else "",
            note=note,
            annotation_type=AnnotationType(annotation_type),
        )
