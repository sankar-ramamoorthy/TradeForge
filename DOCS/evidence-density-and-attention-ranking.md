# Evidence Density And Attention Ranking

**Issue:** EV-00  
**Milestone:** M-EZ  
**Status:** Implemented 2026-07-12  
**Authority:** Runtime design note

## Authority Boundary

Evidence Density is an advisory read model. It can refresh market snapshots,
rank symbols, and surface evidence gaps, but it cannot create lifecycle
transitions, execute trades, or mutate canonical decision state.

The only EV canonical facts introduced by this slice are operator watchlist
intent events:

- `market.watchlist_entry_added`
- `market.watchlist_entry_updated`

Market snapshots remain non-canonical advisory artifacts in the snapshot
archive. Rankings and evidence panels are derived from watchlist facts,
decision lifecycle facts, and archived snapshots.

## Eligible Symbols

A symbol is eligible for evidence refresh and ranking when at least one source
applies:

- `active-decision`: a non-review decision references the ticker.
- `watchlist`: an active watchlist entry references the ticker.
- `operator-pinned`: an active watchlist entry is pinned by the operator.

Review-stage decisions are excluded. Watchlist CRUD must not emit decision
lifecycle events.

## Freshness States

The first EV slice uses a 24-hour freshness window over
`snapshot.provenance.data_as_of`.

- `fresh`: latest persisted snapshot is at most 24 hours old.
- `stale`: latest persisted snapshot is older than 24 hours.
- `missing`: no persisted snapshot exists for the symbol.
- `provider-degraded`: reserved for provider outage history.
- `intentionally-unavailable`: reserved for unsupported instruments.

## Ranking Semantics

Ranking is deterministic and transparent. No AI score is used. Each item
contains the reason codes and weights that produced its priority score.

Initial reason codes:

- `operator-pinned-priority`: 40
- `missing-evidence`: 35
- `active-decision-review-needed`: 30
- `stale-evidence`: 25
- `meaningful-price-change`: 15
- `watchlist-monitoring`: 10
- `unusual-volume`: 10

Initial market thresholds:

- meaningful price change: absolute open-to-close move of at least 3 percent
- unusual volume: volume of at least 50,000,000

Ties sort by score descending, freshness label, then symbol.

## Runtime Surfaces

The runtime exposes:

- `/evidence/watchlist`
- `/evidence/eligibility`
- `/evidence/refresh/run`
- `/evidence/ranking`
- `/evidence/symbols/{symbol}`

The Operating Workspace renders ranked evidence attention and watchlist entry.
The Opportunity Workspace renders the per-symbol evidence panel and the basic
chart from archived advisory snapshots.
