# ADR 0042: Contextual Interpretation And Thesis Influence

## Status
Accepted

## Context
M13 turns M12 advisory observations into non-authoritative contextual meaning.
Raw observations can be useful only when an operator can see what they may mean,
how much contextual weight they carry, whether they support or weaken a thesis,
and what uncertainty remains.

M13 must preserve the M11/M12 advisory boundary. It must not create trade ideas,
revise theses, approve plans, execute trades, or turn AI-generated text into
canonical truth.

## Decision
TradeForge will model `AdvisoryInterpretation` as a non-canonical advisory
artifact linked to one or more `AdvisoryObservation` IDs.

The canonical event ledger records only this capture fact:

```text
advisory.interpretation_captured
```

The event payload may include interpretation ID, artifact ID, linked observation
IDs, optional decision/thesis IDs, interpretation kind, thesis influence,
contextual weight, advisory confidence range, provenance summary, tags, and
captured timestamp.

The event payload must not include interpretation content, rationale,
recommendation authority, lifecycle transition intent, execution authority, or
buy/sell instructions.

Interpretation content, rationale, caveats, and provenance detail live in a
separate advisory interpretation store, distinct from `event_ledger`.

AI-assisted interpretation drafts use the existing `AIAdvisoryProvider` port and
are advisory-only. Drafts are not persisted and do not append events. Operator
acceptance or editing is required before an interpretation artifact is stored
and the capture event is appended.

## Consequences
M13 adds qualitative enums for interpretation kind, thesis influence,
contextual weight, and advisory confidence range. These fields are qualitative
metadata only; they are not predictive scores or recommendation signals.

Replay can show that an interpretation was captured and link to its advisory
artifact while keeping content outside canonical event truth.

Initial workspace surfaces may show interpretation summaries, influence labels,
weights, confidence ranges, provenance, caveats, and conflict visibility, but
must label the material advisory and non-canonical.

## Rejected Alternatives
Using `decision.*` events was rejected because interpretation artifacts do not
change lifecycle state.

Persisting AI draft content directly was rejected because drafts require
operator acceptance before becoming stored advisory artifacts.

Numeric scoring was rejected for M13 because it would imply a precision and
ranking authority the milestone explicitly excludes.
