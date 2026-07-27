# TradeForge - Project State

## Purpose

This file defines the current runtime focus of development.

The knowledge base remains the semantic authority for doctrine, invariants,
ontology, and workflow meaning. This runtime repository is the implementation
authority for executable behavior.

---

# Current Phase

Phase: Post-M14C operational sync and near-term product/refactor preparation

The runtime currently supports:

- event-sourced decision lifecycle operation
- persona-scoped operational workspaces
- deterministic replay and review
- provider-backed market context and provenance
- optional AI advisory through governed provider boundaries
- local advisory import mediation for Thesis and Plan authoring
- Evidence Density surfaces for watchlist, ranking, per-symbol evidence, and
  chart context

---

# Current Priority

1. Keep runtime docs and the knowledge base synchronized after implementation
   milestones.
2. Preserve M14C advisory import boundaries: imported research is advisory
   draft material until the operator submits normal lifecycle workflows.
3. Prepare planned near-term work:
   - M-RF-FE frontend API client decomposition
   - M-RF2 FastAPI dependency injection conversion
   - M-PT paper execution and outcome truth
   - remaining M-EZ ease-of-use, ramp, and governance work
4. Reassess M15 cognitive replay after product and evidence workflows have more
   runtime usage behind them.

---

# Current Runtime Truth

Completed since the older foundation phase:

- M0 through M14 are complete.
- M14C Thesis and Plan advisory import mediation is implemented.
- EV-00 through EV-05 are implemented as the Evidence Density slice.
- M-RF backend API route decomposition is complete.
- TF-F078 and TF-F079 closed immediate Evidence API/provider feedback.

Planned:

- M-RF-FE
- M-RF2
- M-PT
- remaining M-EZ ramp/governance items
- M15 and later cognitive roadmap milestones

---

# Not In Scope

- live-money trading
- autonomous trade execution
- AI approval or lifecycle mutation
- broker state as canonical truth
- dashboard-centric reorganization
- broad architecture rewrites outside tracked issues

---

# Active Focus Principle

We are not building an autonomous trading system.

We are building:

> a structured decision-making system under uncertainty

Every feature must preserve human decision sovereignty, event-ledger truth,
replayability, and workflow integrity.
