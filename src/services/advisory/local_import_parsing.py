"""Local markdown import parsing for thesis and plan draft artifacts.

Moved from the API routes monolith in TF-RF009 (M-RF): parsing operator
business documents is orchestration-layer work, not HTTP-boundary work
(INVARIANTS section 9). Bodies are byte-identical to the monolith originals
except for imports and the removal of the private-name underscore prefix.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path

from src.domain.advisory import (
    AdvisoryArtifact,
    AdvisoryArtifactFormat,
    AdvisoryArtifactSourceReference,
    AdvisoryArtifactType,
    AdvisoryCaptureOrigin,
    AdvisorySourceKind,
    AdvisoryUncertaintyBand,
)

THESIS_IMPORT_SCHEMA_VERSION = "thesis_draft.v1"
THESIS_IMPORT_ROLE = "thesis_draft"
THESIS_IMPORT_FIELD_NAMES = frozenset(
    {
        "title",
        "narrative",
        "catalysts",
        "assumptions",
        "invalidation_conditions",
        "evidence_links",
        "notes",
    }
)
LOCAL_THESIS_IMPORT_DIR = Path("imports") / "incoming"
THESIS_IMPORT_SECTION_ALIASES = {
    "thesis narrative": "narrative",
    "narrative": "narrative",
    "catalysts": "catalysts",
    "assumptions": "assumptions",
    "invalidation conditions": "invalidation_conditions",
    "invalidation": "invalidation_conditions",
    "evidence links": "evidence_links",
    "notes": "notes",
}
PLAN_IMPORT_SCHEMA_VERSION = "plan_draft.v1"
PLAN_IMPORT_ROLE = "plan_draft"
PLAN_IMPORT_FIELD_NAMES = frozenset(
    {
        "entry_rationale",
        "stop_rationale",
        "target_rationale",
        "risk_notes",
    }
)
PLAN_IMPORT_PROHIBITED_FIELD_NAMES = frozenset(
    {
        "price",
        "entry_price",
        "stop_price",
        "target_price",
        "size",
        "sizing",
        "sizing_rationale",
        "quantity",
        "shares",
        "contracts",
        "order_type",
        "broker_order",
        "approval",
        "approved",
        "authorization",
        "execution_authorization",
        "execution_instructions",
    }
)
PLAN_IMPORT_SECTION_ALIASES = {
    "entry rationale": "entry_rationale",
    "entry": "entry_rationale",
    "stop rationale": "stop_rationale",
    "stop": "stop_rationale",
    "target rationale": "target_rationale",
    "target": "target_rationale",
    "risk notes": "risk_notes",
    "risk": "risk_notes",
}
THESIS_TRANSFER_SCHEMA_VERSION = "tradeforge.thesis_draft_transfer.v1"
THESIS_TRANSFER_KIND = "tradeforge_thesis_draft_transfer"
THESIS_TRANSFER_EXTENSION = ".tf-thesis-draft.json"


class LocalImportParseError(ValueError):
    """Raised when a local import file is recognized but invalid."""


def optional_string(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    return stripped or None


def string_list(value: object) -> list[str]:
    if isinstance(value, str):
        stripped = value.strip()
        return [stripped] if stripped else []
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]



def local_thesis_import_artifact_from_markdown(
    *,
    path: Path,
    persona_id: str,
    workspace_id: str,
    symbol: str,
    captured_at: datetime,
) -> AdvisoryArtifact | None:
    text = path.read_text(encoding="utf-8")
    frontmatter, body = split_markdown_frontmatter(text)
    if frontmatter.get("artifact_role") != THESIS_IMPORT_ROLE:
        return None
    if frontmatter.get("schema_version") != THESIS_IMPORT_SCHEMA_VERSION:
        return None
    if str(frontmatter.get("symbol", "")).strip().upper() != symbol:
        return None

    mapped_fields = mapped_fields_from_markdown_sections(body)
    if not any(mapped_fields.values()):
        return None

    metadata: dict[str, object] = {
        "artifact_role": THESIS_IMPORT_ROLE,
        "schema_version": THESIS_IMPORT_SCHEMA_VERSION,
        "symbol": symbol,
        "source": frontmatter.get("source", "local import"),
        "mapped_fields": mapped_fields,
        "local_import_file": path.name,
    }
    title = optional_string(frontmatter.get("title")) or path.stem.replace("_", " ")
    return AdvisoryArtifact(
        artifact_id=f"artifact-{uuid.uuid4()}",
        artifact_type=AdvisoryArtifactType.MARKDOWN_NOTE,
        artifact_format=AdvisoryArtifactFormat.MARKDOWN,
        title=title,
        body=body.strip() or text.strip(),
        source_references=(
            AdvisoryArtifactSourceReference(
                source_kind=AdvisorySourceKind.MARKDOWN_ARTIFACT,
                source_id=path.name,
                summary=f"Local thesis draft import from {path.name}",
            ),
        ),
        capture_origin=AdvisoryCaptureOrigin.OPERATOR_MANUAL,
        provenance_summary=f"operator local markdown import: {path.name}",
        uncertainty_band=AdvisoryUncertaintyBand.UNKNOWN,
        caveats=("Local import requires operator review before thesis promotion.",),
        persona_id=persona_id,
        workspace_id=workspace_id,
        captured_at=captured_at,
        metadata=metadata,
        tags=("thesis_draft", symbol),
    )


def local_thesis_import_artifact_from_transfer_json(
    *,
    path: Path,
    persona_id: str,
    workspace_id: str,
    symbol: str,
) -> AdvisoryArtifact:
    text = path.read_text(encoding="utf-8")
    try:
        transfer = json.loads(text)
    except json.JSONDecodeError as exc:
        raise LocalImportParseError("invalid JSON transfer file") from exc
    if not isinstance(transfer, dict):
        raise LocalImportParseError("transfer file must contain a JSON object")
    _validate_thesis_transfer(transfer, symbol)

    mapped_fields = transfer["mapped_fields"]
    source_references = tuple(
        _source_reference_from_transfer(reference)
        for reference in transfer["source_references"]
    )
    captured_at = _datetime_from_transfer(transfer["exported_at"])
    metadata: dict[str, object] = {
        "artifact_role": THESIS_IMPORT_ROLE,
        "schema_version": THESIS_IMPORT_SCHEMA_VERSION,
        "symbol": symbol,
        "source": transfer["source_system"],
        "mapped_fields": mapped_fields,
        "local_import_file": path.name,
        "transfer_schema_version": transfer["schema_version"],
        "transfer_id": transfer["transfer_id"],
        "submission_id": transfer["submission_id"],
        "submission_schema_version": transfer["submission_schema_version"],
        "submission_digest": transfer["submission_digest"],
        "m5_context": transfer["m5_context"],
        "advisory_boundary": transfer["advisory_boundary"],
    }
    return AdvisoryArtifact(
        artifact_id=f"artifact-{uuid.uuid4()}",
        artifact_type=AdvisoryArtifactType.IMPORTED_RESEARCH,
        artifact_format=AdvisoryArtifactFormat.JSON,
        title=str(transfer["title"]).strip(),
        body=json.dumps(transfer, ensure_ascii=True, sort_keys=True),
        source_references=source_references,
        capture_origin=AdvisoryCaptureOrigin.IMPORTED_RESEARCH,
        provenance_summary=str(transfer["provenance_summary"]).strip(),
        uncertainty_band=AdvisoryUncertaintyBand.UNKNOWN,
        caveats=tuple(string_list(transfer["caveats"])),
        persona_id=persona_id,
        workspace_id=workspace_id,
        captured_at=captured_at,
        metadata=metadata,
        tags=("thesis_draft", symbol, "research_cockpit_transfer"),
    )


def local_plan_import_artifact_from_markdown(
    *,
    path: Path,
    persona_id: str,
    workspace_id: str,
    decision_id: str,
    symbol: str,
    captured_at: datetime,
) -> AdvisoryArtifact | None:
    text = path.read_text(encoding="utf-8")
    frontmatter, body = split_markdown_frontmatter(text)
    if frontmatter.get("artifact_role") != PLAN_IMPORT_ROLE:
        return None
    if frontmatter.get("schema_version") != PLAN_IMPORT_SCHEMA_VERSION:
        return None
    if str(frontmatter.get("symbol", "")).strip().upper() != symbol:
        return None
    frontmatter_decision_id = optional_string(frontmatter.get("decision_id"))
    if frontmatter_decision_id is not None and frontmatter_decision_id != decision_id:
        return None

    mapped_fields = mapped_plan_fields_from_markdown_sections(body)
    if not any(mapped_fields.values()):
        return None

    metadata: dict[str, object] = {
        "artifact_role": PLAN_IMPORT_ROLE,
        "schema_version": PLAN_IMPORT_SCHEMA_VERSION,
        "symbol": symbol,
        "decision_id": decision_id,
        "source": frontmatter.get("source", "local import"),
        "mapped_fields": mapped_fields,
        "local_import_file": path.name,
    }
    title = optional_string(frontmatter.get("title")) or path.stem.replace("_", " ")
    return AdvisoryArtifact(
        artifact_id=f"artifact-{uuid.uuid4()}",
        artifact_type=AdvisoryArtifactType.MARKDOWN_NOTE,
        artifact_format=AdvisoryArtifactFormat.MARKDOWN,
        title=title,
        body=body.strip() or text.strip(),
        source_references=(
            AdvisoryArtifactSourceReference(
                source_kind=AdvisorySourceKind.MARKDOWN_ARTIFACT,
                source_id=path.name,
                summary=f"Local plan draft import from {path.name}",
            ),
        ),
        capture_origin=AdvisoryCaptureOrigin.OPERATOR_MANUAL,
        provenance_summary=f"operator local markdown import: {path.name}",
        uncertainty_band=AdvisoryUncertaintyBand.UNKNOWN,
        caveats=(
            "Local import requires operator review before plan creation.",
            "Local import has no sizing, approval, or execution authority.",
        ),
        persona_id=persona_id,
        workspace_id=workspace_id,
        captured_at=captured_at,
        metadata=metadata,
        tags=("plan_draft", symbol),
    )


def split_markdown_frontmatter(text: str) -> tuple[dict[str, object], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    end_index: int | None = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_index = index
            break
    if end_index is None:
        return {}, text
    frontmatter = parse_simple_yaml_frontmatter(lines[1:end_index])
    body = "\n".join(lines[end_index + 1 :])
    return frontmatter, body


def parse_simple_yaml_frontmatter(lines: list[str]) -> dict[str, object]:
    parsed: dict[str, object] = {}
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        clean_key = key.strip()
        clean_value = value.strip().strip("'\"")
        if clean_key:
            parsed[clean_key] = clean_value
    return parsed


def mapped_fields_from_markdown_sections(body: str) -> dict[str, object]:
    sections: dict[str, list[str]] = {}
    current_key: str | None = None
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            heading = stripped.lstrip("#").strip().lower()
            current_key = THESIS_IMPORT_SECTION_ALIASES.get(heading)
            if current_key is not None:
                sections.setdefault(current_key, [])
            continue
        if current_key is not None:
            sections[current_key].append(line)

    mapped: dict[str, object] = {}
    narrative = section_text(sections.get("narrative", []))
    if narrative:
        mapped["narrative"] = narrative
    notes = section_text(sections.get("notes", []))
    if notes:
        mapped["notes"] = notes
    for field_name in (
        "catalysts",
        "assumptions",
        "invalidation_conditions",
        "evidence_links",
    ):
        values = section_list(sections.get(field_name, []))
        if values:
            mapped[field_name] = values
    return mapped


def mapped_plan_fields_from_markdown_sections(body: str) -> dict[str, object]:
    sections: dict[str, list[str]] = {}
    current_key: str | None = None
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            heading = stripped.lstrip("#").strip().lower()
            current_key = PLAN_IMPORT_SECTION_ALIASES.get(heading)
            if current_key is not None:
                sections.setdefault(current_key, [])
            continue
        if current_key is not None:
            sections[current_key].append(line)

    mapped: dict[str, object] = {}
    for field_name in (
        "entry_rationale",
        "stop_rationale",
        "target_rationale",
    ):
        text = section_text(sections.get(field_name, []))
        if text:
            mapped[field_name] = text
    risk_notes = section_list(sections.get("risk_notes", []))
    if risk_notes:
        mapped["risk_notes"] = risk_notes
    return mapped


def section_text(lines: list[str]) -> str | None:
    text = "\n".join(line.strip() for line in lines).strip()
    return text or None


def section_list(lines: list[str]) -> list[str]:
    values: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(("- ", "* ")):
            stripped = stripped[2:].strip()
        values.append(stripped)
    return values


def local_import_already_persisted(
    artifacts: tuple[AdvisoryArtifact, ...],
    path: Path,
    symbol: str,
    artifact_role: str = THESIS_IMPORT_ROLE,
    decision_id: str | None = None,
) -> bool:
    return any(
        artifact.metadata.get("local_import_file") == path.name
        and str(artifact.metadata.get("symbol", "")).strip().upper() == symbol
        and artifact.metadata.get("artifact_role") == artifact_role
        and (
            decision_id is None
            or str(artifact.metadata.get("decision_id", "")).strip() == decision_id
        )
        for artifact in artifacts
    )


def local_transfer_already_persisted(
    artifacts: tuple[AdvisoryArtifact, ...],
    *,
    transfer_id: str,
    submission_id: str,
    submission_digest: str,
    symbol: str,
) -> bool:
    return any(
        str(artifact.metadata.get("transfer_id", "")).strip() == transfer_id
        or (
            str(artifact.metadata.get("submission_id", "")).strip() == submission_id
            and str(artifact.metadata.get("submission_digest", "")).strip()
            == submission_digest
            and str(artifact.metadata.get("symbol", "")).strip().upper() == symbol
            and artifact.metadata.get("artifact_role") == THESIS_IMPORT_ROLE
        )
        for artifact in artifacts
    )


def transfer_identity_from_file(path: Path) -> tuple[str, str, str] | None:
    try:
        transfer = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    if not isinstance(transfer, dict):
        return None
    transfer_id = optional_string(transfer.get("transfer_id"))
    submission_id = optional_string(transfer.get("submission_id"))
    submission_digest = optional_string(transfer.get("submission_digest"))
    if not transfer_id or not submission_id or not submission_digest:
        return None
    return transfer_id, submission_id, submission_digest


def transfer_file_symbol(path: Path) -> str | None:
    try:
        transfer = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    if not isinstance(transfer, dict):
        return None
    symbol = optional_string(transfer.get("symbol"))
    return symbol.upper() if symbol else None


def _validate_thesis_transfer(transfer: dict[object, object], symbol: str) -> None:
    required = {
        "schema_version",
        "transfer_kind",
        "artifact_role",
        "projection_schema_version",
        "transfer_id",
        "exported_at",
        "source_system",
        "submission_id",
        "submission_schema_version",
        "submission_digest",
        "symbol",
        "title",
        "mapped_fields",
        "provenance_summary",
        "source_references",
        "caveats",
        "m5_context",
        "advisory_boundary",
    }
    missing = sorted(required - {str(key) for key in transfer})
    if missing:
        raise LocalImportParseError(f"transfer missing required fields: {missing}")
    if transfer["schema_version"] != THESIS_TRANSFER_SCHEMA_VERSION:
        raise LocalImportParseError("unsupported transfer schema_version")
    if transfer["transfer_kind"] != THESIS_TRANSFER_KIND:
        raise LocalImportParseError("unsupported transfer_kind")
    if transfer["artifact_role"] != THESIS_IMPORT_ROLE:
        raise LocalImportParseError("transfer artifact_role must be thesis_draft")
    if transfer["projection_schema_version"] != THESIS_IMPORT_SCHEMA_VERSION:
        raise LocalImportParseError("unsupported projection_schema_version")
    if str(transfer["symbol"]).strip().upper() != symbol:
        raise LocalImportParseError("symbol_mismatch")
    if "persona_id" in transfer or "workspace_id" in transfer:
        raise LocalImportParseError("transfer must not carry persona or workspace IDs")
    for field in (
        "transfer_id",
        "source_system",
        "submission_id",
        "submission_schema_version",
        "submission_digest",
        "title",
        "provenance_summary",
    ):
        if optional_string(transfer[field]) is None:
            raise LocalImportParseError(f"{field} must not be empty")
    if not str(transfer["submission_digest"]).startswith("sha256:"):
        raise LocalImportParseError("submission_digest must be sha256")
    mapped_fields = transfer["mapped_fields"]
    if not isinstance(mapped_fields, dict):
        raise LocalImportParseError("mapped_fields must be an object")
    unknown_fields = sorted(
        str(field)
        for field in mapped_fields
        if str(field) not in THESIS_IMPORT_FIELD_NAMES
    )
    if unknown_fields:
        raise LocalImportParseError(f"unsupported mapped_fields: {unknown_fields}")
    if not any(_mapped_field_has_value(value) for value in mapped_fields.values()):
        raise LocalImportParseError("mapped_fields must contain at least one value")
    if not isinstance(transfer["source_references"], list) or not transfer[
        "source_references"
    ]:
        raise LocalImportParseError("source_references must not be empty")
    if not string_list(transfer["caveats"]):
        raise LocalImportParseError("caveats must not be empty")
    if not isinstance(transfer["m5_context"], dict):
        raise LocalImportParseError("m5_context must be an object")
    boundary = transfer["advisory_boundary"]
    if not isinstance(boundary, dict):
        raise LocalImportParseError("advisory_boundary must be an object")
    for field in (
        "advisory_only",
        "non_canonical",
        "no_lifecycle_authority",
        "no_execution_authority",
    ):
        if boundary.get(field) is not True:
            raise LocalImportParseError(f"{field} must be true")
    _datetime_from_transfer(transfer["exported_at"])


def _source_reference_from_transfer(
    reference: object,
) -> AdvisoryArtifactSourceReference:
    if not isinstance(reference, dict):
        raise LocalImportParseError("source reference must be an object")
    source_kind = optional_string(reference.get("source_kind"))
    source_id = optional_string(reference.get("source_id"))
    summary = optional_string(reference.get("summary"))
    if source_kind is None or source_id is None or summary is None:
        raise LocalImportParseError("source reference fields must not be empty")
    try:
        kind = AdvisorySourceKind(source_kind)
    except ValueError as exc:
        raise LocalImportParseError(f"unsupported source_kind: {source_kind}") from exc
    source_uri = optional_string(reference.get("source_uri"))
    return AdvisoryArtifactSourceReference(
        source_kind=kind,
        source_id=source_id,
        summary=summary,
        source_uri=source_uri,
    )


def _datetime_from_transfer(value: object) -> datetime:
    text = optional_string(value)
    if text is None:
        raise LocalImportParseError("exported_at must not be empty")
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise LocalImportParseError("exported_at must be ISO-8601") from exc


def _mapped_field_has_value(value: object) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(string_list(value))
    return False
