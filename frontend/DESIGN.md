---
name: TradeForge Frontend Operational Layout
version: 0.1.0
status: runtime-translation
authority: runtime-frontend
semantic_authority:
  - ../DOCS/adr/0007-anti-dashboard-ux-decision.md
  - ../DOCS/adr/0012-workspace-architecture-model.md
  - ../DOCS/adr/0021-react-workspace-runtime.md
tokens:
  color:
    canvas: "#eef1ef"
    surface: "#ffffff"
    surface_muted: "#f9fbfa"
    surface_warm: "#f6f2eb"
    text: "#18201f"
    text_muted: "#56625f"
    text_subtle: "#6f7976"
    border: "#d5dcd8"
    border_active: "#2f7669"
    accent: "#2f7669"
    accent_surface: "#edf7f2"
    attention: "#856432"
    attention_surface: "#f4efe6"
    danger: "#b45f3a"
    danger_surface: "#fbede6"
  radius:
    control: "8px"
    surface: "8px"
  spacing:
    page_inline: "32px"
    panel: "24px"
    stack: "16px"
    compact: "10px"
  typography:
    family: "Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    letter_spacing: "0"
    body_line_height: "1.6"
layout:
  shell_max_width: "1220px"
  sidebar_width: "280px"
  breakpoint_stack: "860px"
  breakpoint_compact: "560px"
---

# TradeForge Frontend Operational Layout

## Purpose

This file translates TradeForge workspace and UX doctrine into frontend layout
tokens and implementation rules.

It is inspired by the `DESIGN.md` pattern, but it is not semantic doctrine. The
knowledge base and runtime ADRs remain authoritative for workspace meaning,
persona semantics, lifecycle authority, replay, and event truth.

## Authority Boundary

`frontend/DESIGN.md` may define:

- frontend design tokens;
- reusable layout primitives;
- component composition rules;
- visual hierarchy for operational surfaces;
- constraints that help prevent dashboard drift.

It must not define:

- workspace ontology;
- lifecycle semantics;
- event meaning;
- persona behavior;
- replay authority;
- product philosophy beyond runtime translation.

## Layout Model

The frontend layout is organized around a persona-scoped operational workspace:

- workspace briefing: orientation and authority boundary;
- workspace navigation: route entrypoints, not workspace truth;
- context panel: persona, workflow, and decision continuity;
- workspace surface: the active derived presentation surface;
- operational cards: scoped context/action/review regions;
- runtime boundary panel: explicit API/ledger authority reminder.

## Visual Principles

- Context before action.
- Dense but readable operational surfaces.
- Routes and panels should preserve decision continuity.
- Cards are for individual operational surfaces only.
- Page sections remain unframed layout structure.
- Avoid dashboard-style metric grids and detached action controls.
- Use icons for navigation and compact operational cues.
- Keep radius at 8px or less.
- Letter spacing remains `0`.

## Token Usage

CSS custom properties in `frontend/src/styles.css` should mirror the token names
above where practical. Token changes should be deliberate and checked against
anti-dashboard UX, workspace continuity, and readability.

## Implementation Boundary

Shared layout primitives belong in `frontend/src/operationalLayout.tsx`.

They should remain:

- presentation-only;
- API-boundary aware;
- reusable across M8 workspace implementations;
- independent of Python runtime internals;
- free of lifecycle/event mutation authority.
