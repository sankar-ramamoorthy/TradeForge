# Tasks: Ollama Remote Advisory Route

**Input**: Design documents from `specs/001-ollama-remote-advisory-route/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Included because TF-F088 changes advisory routing and provider governance behavior.

**Organization**: Tasks are grouped by user story for independent validation.

## Phase 1: Setup

- [x] T001 Confirm `feature/tf-f088-ollama-remote` is not `main` in TradeForge
- [x] T002 [P] Review TF-F088 issue scope in `DOCS/ISSUE_REGISTER.md`
- [x] T003 [P] Review relevant advisory routing code in `src/infrastructure/advisory/`

---

## Phase 2: Foundational

- [x] T004 Add governed Ollama route constants/config helpers in `src/infrastructure/advisory/litellm_request_composer.py`
- [x] T005 Add focused resolver tests for remote/local/auto Ollama routes in `tests/test_litellm_request_composer.py`

---

## Phase 3: User Story 1 - Select Remote Ollama Advisory Backend (Priority: P1) MVP

**Goal**: Operators can select `ollama-remote` and request composition uses the remote base without direct adapter bypass.

**Independent Test**: Resolver/composer tests prove `ollama-remote` uses the remote base and fails when the route is not configured.

- [x] T006 [US1] Implement explicit `ollama-remote` resolution in `src/infrastructure/advisory/litellm_request_composer.py`
- [x] T007 [US1] Add Provider Governance API visibility for `ollama-remote` in `src/app/api/routes/governance.py`
- [x] T008 [US1] Add `ollama-remote` to model provider choices in `frontend/src/workspaces/ProviderGovernanceWorkspace.tsx`
- [x] T009 [P] [US1] Add API tests for `ollama-remote` provider visibility and model selection in `tests/test_provider_governance_api.py`

---

## Phase 4: User Story 2 - Distinguish Local And Auto Ollama Routes (Priority: P2)

**Goal**: Operators can distinguish local and auto route behavior, with fallback limited to `ollama-auto`.

**Independent Test**: Resolver tests verify local is explicit and auto resolves remote-or-local through a bounded probe.

- [x] T010 [US2] Implement `ollama-local` and `ollama-auto` resolution in `src/infrastructure/advisory/litellm_request_composer.py`
- [x] T011 [US2] Add Provider Governance API visibility for local/auto routes in `src/app/api/routes/governance.py`
- [x] T012 [US2] Add local/auto options to `frontend/src/workspaces/ProviderGovernanceWorkspace.tsx`
- [x] T013 [P] [US2] Add resolver tests for explicit local and auto fallback behavior in `tests/test_litellm_request_composer.py`

---

## Phase 5: User Story 3 - Preserve Advisory Route Provenance (Priority: P3)

**Goal**: Advisory responses and smoke tests report selected/resolved provider identity and model.

**Independent Test**: Provider and smoke-test tests verify backend provider/model identity and no Event Ledger writes.

- [x] T014 [US3] Preserve resolved provider identity through advisory generation in `src/infrastructure/advisory/openai_compatible_provider.py`
- [x] T015 [P] [US3] Add advisory provenance tests in `tests/test_openai_compatible_provider.py`
- [x] T016 [P] [US3] Add smoke-test provider identity coverage in `tests/test_provider_governance_api.py`

---

## Final Phase: Polish & Cross-Cutting Concerns

- [x] T017 Update TF-F088 status/evidence in `DOCS/ISSUE_REGISTER.md`
- [x] T018 Run focused backend tests from `quickstart.md`
- [x] T019 Run lint/type/frontend validation as practical for touched surfaces

## Dependencies & Execution Order

- Setup before Foundational.
- Foundational before all user stories.
- US1 is MVP and should complete before US2/US3.
- US2 depends on Foundational and can proceed after US1 constants are in place.
- US3 depends on resolved-provider behavior from US1/US2.

## Parallel Opportunities

- T002 and T003 can run in parallel.
- API, frontend, and focused tests can be edited in parallel after resolver behavior is stable.
- T015 and T016 can be authored independently after T014.

## Implementation Strategy

Complete US1 first, validate request composition and API selection, then add auto/local distinction, then provenance and smoke-test coverage.
