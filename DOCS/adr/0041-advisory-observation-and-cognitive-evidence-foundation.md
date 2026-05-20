# ADR 0041: Advisory Observation And Cognitive Evidence Foundation

## Status
Accepted

## Context
M12 introduces the first durable pre-lifecycle advisory cognition layer. TradeForge
needs to capture machine- or operator-supplied observations, preserve evidence,
provenance, uncertainty, and replay visibility, and still prevent advisory
artifacts from becoming lifecycle authority.

Existing M11 advisory interfaces define non-canonical AI outputs and provenance,
but they intentionally exclude persistence, API endpoints, and event-backed
capture facts. M12 closes that foundation gap without introducing scanners,
candidate queues, thesis influence scoring, or autonomous promotion to trade
ideas.

## Decision
TradeForge will model advisory observations as non-canonical durable artifacts
with a canonical capture fact.

The canonical event domain expands to include:

```text
advisory.*
```

The first event type is:

```text
advisory.observation_captured
```

This event records only that an advisory observation artifact was captured at a
time in a persona/workspace context. Its payload may include `observation_id`,
`artifact_id`, `observation_kind`, `capture_origin`, optional `decision_id`,
optional `thesis_id`, source references, provenance summary, qualitative
uncertainty band, tags, and captured timestamp.

The event must not contain recommendation authority, lifecycle transition
intent, execution authority, buy/sell instructions, or the generated advisory
content as canonical truth.

Observation content and evidence live in a separate advisory artifact store.
That store is durable and queryable, but it is explicitly non-canonical. It may
hold observation text, evidence references, provenance details, caveats, tags,
capture origin, persona/workspace context, and optional decision/thesis context.

The services layer owns the capture flow:

1. validate advisory observation contract
2. persist the non-canonical advisory artifact
3. append `advisory.observation_captured`

Replay includes advisory capture events so historical reconstruction can show
that the observation existed and link to the advisory artifact, while preserving
the distinction between event truth and non-canonical advisory content.

## Rationale
Advisory cognition is useful only if it is durable, provenance-aware, and
replay-visible. However, storing full generated content in the Event Ledger
would blur canonical truth with interpretation. Separating the capture fact from
the artifact content preserves event-sourcing integrity while allowing operators
to inspect what evidence existed at the time.

Qualitative uncertainty bands keep M12 from implying false precision or hidden
scoring authority. Optional decision/thesis links are contextual only; support,
weakening, conflict, and thesis influence semantics are deferred to M13.

Capture origin is modeled as a fixed value so later trust modeling, evidence
quality review, source weighting, behavioral analysis, and replay analysis can
distinguish operator manual captures from provider imports, generated advisory
artifacts, imported research, replay annotations, and future scanner output.

## Consequences
The `advisory` event domain becomes a canonical domain, but only for factual
advisory-system events.

Advisory artifact stores must remain separate from `event_ledger` and must label
returned content as advisory and non-canonical.

APIs may create, retrieve, and list advisory observations, but responses must
make the advisory/non-canonical boundary explicit.

Replay can show advisory capture facts and artifact identifiers, but replay must
not require live providers, current AI output, mutable UI state, or advisory
artifact content to reconstruct canonical event history.

## Rejected Alternatives
Storing full observation content in the Event Ledger was rejected because it
would make generated or operator-supplied interpretation appear canonical.

Using existing `decision.*` events was rejected because advisory observations
are pre-lifecycle or contextual artifacts and must not imply lifecycle progress.

Modeling observations as recommendations was rejected because M12 does not
answer what to buy, approve plans, execute trades, or promote candidates.

Hidden confidence scores were rejected because M12 needs uncertainty
preservation, not opaque ranking authority.
