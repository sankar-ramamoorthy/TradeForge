# TF-F084 / RC-041 Transfer Contract

## Purpose

Define the first human-usable Research Cockpit to TradeForge handoff slice.
The transfer remains advisory-only and non-canonical until a TradeForge
operator accepts fields in the Thesis Import Preview and submits the normal
Develop Thesis workflow.

## Contract

- File extension: `.tf-thesis-draft.json`
- Serialization: UTF-8 JSON object
- Directory: `imports/incoming`
- Schema version: `tradeforge.thesis_draft_transfer.v1`
- Transfer kind: `tradeforge_thesis_draft_transfer`
- Artifact role: `thesis_draft`
- Projection schema: `thesis_draft.v1`

Required top-level fields:

- `schema_version`
- `transfer_kind`
- `artifact_role`
- `projection_schema_version`
- `transfer_id`
- `exported_at`
- `source_system`
- `submission_id`
- `submission_schema_version`
- `submission_digest`
- `symbol`
- `title`
- `mapped_fields`
- `provenance_summary`
- `source_references`
- `caveats`
- `m5_context`
- `advisory_boundary`

`mapped_fields` may contain only:

- `title`
- `narrative`
- `catalysts`
- `assumptions`
- `invalidation_conditions`
- `evidence_links`
- `notes`

`source_references` entries contain `source_kind`, `source_id`, `summary`, and
optional `source_uri`.

`m5_context` preserves submission context needed for audit and operator
review: `quality`, `source_packet_ids`, `risk_markers`, `operator_question`,
and `created_at`.

## Status Semantics

TradeForge scan status is per file:

- `imported`: valid transfer persisted as an advisory artifact
- `duplicate`: same transfer already persisted for the active persona and
  workspace
- `symbol_mismatch`: file symbol does not match the active symbol
- `invalid`: unreadable, malformed, unsupported, incomplete, or boundary
  violating file

The scan response reports received, imported, duplicate, skipped, and rejected
counts plus per-file status and human-readable reason.

## Ownership

- Research Cockpit owns producing a valid transfer file from a selected M5
  submission.
- TradeForge owns directory discovery, validation, active persona/workspace
  assignment, duplicate detection, advisory artifact persistence, status
  reporting, Thesis Import Preview visibility, and all lifecycle mediation.
- The transfer file does not carry TradeForge persona or workspace authority.
- File delivery never creates a TradeIdea, Thesis, approval, execution, or
  Event Ledger fact.

## First Slice

1. Run one Cockpit command against a valid M5 submission.
2. Export one `.tf-thesis-draft.json` file.
3. Place it in `imports/incoming`.
4. Run the TradeForge scan from the Thesis Development modal.
5. See symbol matched and import available status.
6. Preview mapped fields in Thesis Import Preview.

