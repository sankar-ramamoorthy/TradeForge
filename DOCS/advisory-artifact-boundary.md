# Advisory Artifact Boundary

## Purpose

Advisory artifacts store imported research, generated advisory notes, and
markdown cognition outside the canonical event ledger.

They are durable advisory context, not lifecycle authority.

## Boundary Rules

- Advisory artifact content is non-canonical.
- Artifact persistence does not append decision, approval, execution, review, or
  lifecycle events.
- Imported research must use `imported_research` capture origin.
- Codex/Claude generated artifacts must use `codex_generated` or
  `claude_generated` capture origin.
- Markdown artifacts are stored as inert text. Runtime rejects script-bearing
  markdown such as `<script>` blocks or `javascript:` links.
- Artifact metadata and body text may not assert lifecycle transition intent,
  approval intent, execution authority, buy/sell instructions, or canonical
  recommendation truth.

## Replay Implications

Each artifact stores a replay-safe snapshot containing:

- captured timestamp
- source reference count
- caveat count
- metadata copy
- body SHA-256 digest

Replay can inspect artifact identifiers and snapshot metadata without depending
on live providers, current AI output, or mutable external research sources.
Canonical event history remains limited to event facts; artifact bodies remain
advisory content outside `event_ledger`.

## Evidence Links

Advisory observations and candidates may reference artifact IDs through
`CognitiveEvidence.artifact_id`. Those links preserve provenance and historical
inspection paths without granting artifacts lifecycle authority.
