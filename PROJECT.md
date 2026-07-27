# TradeForge - Project State

## Purpose

This file defines the current runtime focus of development.

The knowledge base remains the semantic authority for doctrine, invariants,
ontology, and workflow meaning. This runtime repository is the implementation
authority for executable behavior.

---

# Current Phase

Phase: M-EZ product-readiness sequence

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

1. Keep `DOCS/Milestone_Roadmap_v2.md` as the single active runtime roadmap.
   `DOCS/MILESTONE_ROADMAP_DEPRECATED.md` and `DOCS/Milestone_Roadmap_v3.md`
   are historical source artifacts only.
2. Preserve M14C advisory import boundaries: imported research is advisory
   draft material until the operator submits normal lifecycle workflows.
3. Prepare planned near-term work:
   - operator walkthrough before selecting M-RF-FE, M-RF2, M-PT, Research
     Cockpit intake, or additional usability work
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
- GOV-01 two-tier issue discipline is documented in the runtime agent
  bootstrap files.
- GOV-02 bounded Knowledge Base hygiene is complete.
- EZ-01 single Compose startup is complete.
- EZ-02 first-run master key setup is complete.
- EZ-03 documentation truth pass is complete.
- RAMP-01 quick-capture idea tier is complete.
- RAMP-02 guided first-decision mode is complete.

Planned:

- operator walkthrough and evidence-based next-stream selection
- M-RF-FE, M-RF2, M-PT, RAMP-03, and M15+ remain deferred until operator
  validation or concrete blockers justify activation

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
