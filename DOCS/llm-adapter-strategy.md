---
title: LLM Adapter Strategy — Advisory Intelligence Layer
type: planning-document
status: active
created: 2026-05-22
updated: 2026-05-22
tags:
  - advisory
  - llm
  - ai-advisory
  - litellm
  - groq
  - nvidia-nim
  - ollama
  - m12
  - m13
  - architecture
related_adrs:
  - ADR-0006 (AI Advisory Boundary Model)
  - ADR-0037 (Operational Credential Boundary)
  - ADR-0041 (Advisory Observation And Cognitive Evidence Foundation)
---

# LLM Adapter Strategy — Advisory Intelligence Layer

## Purpose

This document covers two things:

1. A current capability assessment of TradeForge post-M12.
2. An architectural analysis of how to wire a concrete LLM adapter — the single
   most important missing piece before the advisory layer becomes operationally
   useful.

It was written to inform the next implementation decision and any resulting
issues filed against M12 or M13.

---

## Part 1 — Capability Assessment (Post-M12)

### What TradeForge Can Do Today

**Structured decision workflow — fully operational.**

The canonical lifecycle (Idea → Thesis → Plan → Approval → Position → Review)
is event-sourced, Postgres-persisted, and replayable. A trader can:

- Start a trade idea from the UI without any API calls
- Author a structured thesis: narrative, catalysts, assumptions, invalidation
  conditions, regime alignment, confidence level
- Build a structured trade plan: entry rationale, stop/target rationale, sizing
  rationale, execution assumptions
- Model conditional scenarios (bull case, bear case, invalidation branch)
- Progress through approval gating with lifecycle integrity enforced
- Track position state
- Write structured post-trade reviews capturing thesis vs. outcome, execution
  quality, emotional reflection, lessons learned

All of this survives restarts, supports multiple concurrent decisions, and is
inspectable by replay. This is a real product capability.

**Replay — operational.**

The replay workspace reconstructs historical workflow state from events. With
M10A cognitive artifacts, replay reconstructs reasoning — what the thesis said
at the time, what scenarios existed, what was assumed — not merely event
timestamps.

**Market context — operational with caveats.**

Six provider adapters: yfinance (free, no key), Polygon, Alpaca, Alpha Vantage,
FMP. The capability model separates price from fundamentals. Provider provenance
is tracked and surfaced in workspaces. The Context Workbench makes acquisition
explicit and explains degraded or missing states to the operator.

**Advisory observation layer (M12) — infrastructure ready, not yet alive.**

The domain now has:

- `AdvisoryObservation` — typed observations (price action, fundamentals, market
  context, news/research, risk, behavioral process, operator notes) with
  uncertainty bands, caveats, provenance tracking, and conflict markers
- `CognitiveEvidence` — evidence items linked to thesis artifacts with staleness
  tracking
- `AdvisoryCandidate` — surfaced candidates with a review queue and operator-
  controlled promotion; automated lifecycle promotion is explicitly blocked
- Advisory artifacts — markdown research notes importable via API, Claude/Codex-
  generated artifacts explicitly supported, SHA-256 snapshotted for replay
- Postgres persistence for observations, artifacts, interpretations

**AI advisory boundary (M11) — plumbing exists, no provider wired.**

The `AIAdvisoryProvider` protocol, `AdvisoryRequest/Response` types, and service
wrappers for replay summarization and review assistance exist and are correctly
enforced. The service validates that responses remain advisory, cannot claim
lifecycle authority, and cannot mutate state.

No concrete LLM adapter has been implemented. This is the gap.

### What TradeForge Cannot Do Yet

**1. Generate advisory intelligence.**
The advisory infrastructure is an inbox with no postman. Observations must be
manually entered or imported via the research artifact API. The LLM plumbing
exists; the plug-in does not.

**2. Contextual interpretation (M13 not built).**
Observations are stored but not synthesized. There is no regime-aware weighting,
no "this weakens vs. supports the thesis" classification, no confidence-range
representation. M13 covers this, but M13 needs a working adapter as upstream
input.

**3. No live candidate pipeline.**
`AdvisoryCaptureOrigin.FUTURE_SCANNER` is defined as a placeholder. No live
scanning generates candidates. The queue must be populated manually today.

**4. No broker execution.**
Intentional. Human decision sovereignty is a permanent invariant.

### What Is Needed To Run It

| Requirement | Notes |
|---|---|
| Docker + Compose | Backend (Python/FastAPI) + Postgres |
| Node.js | React frontend |
| `TRADEFORGE_MASTER_KEY` env var | Master key for credential encryption (M10C) |
| Provider API keys (optional) | Polygon, FMP, Alpha Vantage via credential CLI — yfinance works without a key |
| LLM provider (pending) | The subject of this document |

---

## Part 2 — LLM Adapter Analysis

### The Boundary That Already Exists

The `AIAdvisoryProvider` protocol in `src/domain/advisory/` is the correct
insertion point. Any adapter only needs to implement:

```python
class AIAdvisoryProvider(Protocol):
    def generate(self, request: AdvisoryRequest) -> AdvisoryResponse: ...
```

The `AIAdvisoryService` validates that the response maintains the correct
`request_id`, `artifact_kind`, and `authority=ADVISORY`. The adapter cannot
accidentally grant the LLM lifecycle authority — the boundary enforces it.

Credentials for any adapter go through the existing `CredentialStore`. No key
appears in code, environment files, or git history.

### The Four Advisory Tasks

All four of these are the target use cases. Each maps cleanly to the existing
service boundaries.

| Task | Existing Service Boundary | Input Context | Output |
|---|---|---|---|
| Replay summary | `ReplayAdvisoryService` | Replay timeline events, lifecycle transitions | Narrative summary as `AdvisoryResponse` |
| Thesis review assistant | `ReviewAdvisoryService` | Structured thesis artifact, market context snapshot | Observations of kind `risk`, `behavioral_process` with caveats and uncertainty band |
| Advisory observation generation | `AdvisoryObservationService` | Ticker, market snapshot, fundamentals | Multiple `AdvisoryObservation` entries across price action, fundamentals, risk, market context kinds |
| Candidate screening | `AdvisoryCandidateService` | Advisory candidate queue contents | Ranked commentary; does not modify lifecycle state |

On-demand is the correct first delivery mode. All four tasks are triggered
explicitly by the operator. Automatic background enrichment is a documented
future step once prompt quality is validated.

---

### Adapter Approaches — Pros and Cons

#### Approach A — LiteLLM Unified Adapter (Recommended)

**What it is:** A single `OpenAICompatibleAdvisoryProvider` that speaks the
OpenAI chat completions API format, pointed at a local LiteLLM proxy. LiteLLM
routes calls to Groq, NVIDIA NIM, Ollama, or Claude API depending on
configuration. Code never changes — only LiteLLM config changes when providers
are swapped.

**This setup already exists on the local machine.** LiteLLM is running. Groq
is tested. NVIDIA NIM is provisioned and pending test. Ollama is running.

**Credential shape in CredentialStore:**

```
provider: litellm
base_url: http://localhost:4000   (or wherever LiteLLM is bound)
api_key:  <litellm master key>
model:    groq/llama-3.1-70b-versatile  (configurable per task)
```

**Pros:**

- One adapter implementation, all providers. Swapping Groq for NVIDIA NIM
  requires a LiteLLM config line, not a code change.
- Groq free tier gives access to Llama 3.1 70B — meaningfully better than any
  7B model Ollama can run on 8GB RAM. Suitable for thesis review and observation
  generation.
- NVIDIA NIM free tier can be added immediately and reportedly has better daily
  limits than Groq. No code change.
- Ollama remains available as a local fallback for testing or privacy-sensitive
  future scenarios.
- Anthropic Claude API can be added to LiteLLM later without touching TradeForge
  code. Just add the key to LiteLLM and update the model string in
  CredentialStore.
- LiteLLM handles retries, rate-limit backoff, and provider fallback internally.
- Aligns directly with how `src/security/credential_store.py` is designed.

**Cons:**

- LiteLLM must be running for any advisory call to succeed. If LiteLLM is down,
  all four advisory tasks fail. This is acceptable for a single-operator local
  setup but would need a health check in the advisory service.
- One extra network hop (localhost → LiteLLM → Groq). Adds ~10-50ms — not
  meaningful for on-demand tasks.
- LiteLLM is a third-party service dependency in the local development stack.

**Product impact:**

All four advisory tasks become available on-demand with no per-call cost on
free-tier Groq. Quality is good (70B). Response latency is 1-3 seconds for
typical advisory prompts. Rate limit on Groq free tier is ~30 requests/minute,
which is far above what a single on-demand operator will consume.

---

#### Approach B — Direct Groq Adapter

**What it is:** A `GroqAdvisoryProvider` that calls `api.groq.com` directly
using the OpenAI-compatible API format.

**Pros:**

- Already tested. API key already available.
- Simple — no LiteLLM dependency.
- Groq inference is very fast (often sub-second).

**Cons:**

- Adds a provider-specific adapter. When NVIDIA NIM is tested and preferred,
  a second adapter is needed. This contradicts the provider-agnostic design of
  `AIAdvisoryProvider`.
- Free tier rate limits (30 req/min, 14,400 tokens/min, ~14,400 tokens/day on
  some models) can become a constraint if advisory generation is extended to
  automatic enrichment in future.
- No fallback path — if Groq is down, advisory is down.

**Product impact:** Functionally identical to Approach A for on-demand use
today. Creates provider lock-in that must be refactored later. Not recommended
unless LiteLLM is deliberately excluded from the stack.

---

#### Approach C — Direct Anthropic Claude API Adapter

**What it is:** An `AnthropicAdvisoryProvider` using the Anthropic Python SDK.

**Important distinction:** The existing Claude Pro subscription ($20/month) is
the consumer product at claude.ai. It does NOT include API access. Anthropic API
is a separate pay-per-token product requiring a separate account and billing
setup.

**Pros:**

- Claude Sonnet is the highest quality model for thesis analysis, nuanced
  advisory reasoning, and structured output generation.
- Native tool use support if agentic advisory tasks are added later.
- Prompt caching can significantly reduce cost on repeated context (e.g., the
  same thesis reviewed multiple times).

**Cons:**

- Requires signing up for Anthropic API and adding a payment method. The $20/mo
  Claude Pro plan does not provide this.
- Pay-per-token. Approximate cost per advisory call at Claude Sonnet 4.x rates:
  $0.003-0.015 per call depending on context size. For on-demand single-operator
  use this is low, but it is not free.
- Adds a new credential type distinct from the existing LLM stack.
- If you later add it to LiteLLM, a direct adapter becomes redundant.

**Product impact:** Best model quality for all four advisory tasks, especially
thesis review (nuanced reasoning, blind spot identification, assumption
challenge). Worth pursuing as an option inside LiteLLM rather than as a
standalone adapter — add Claude API to LiteLLM, change the model string in
CredentialStore, no code changes required.

---

#### Approach D — Ollama Local Adapter

**What it is:** An adapter pointing at the local Ollama instance
(http://localhost:11434), which serves quantized models within the 8GB RAM
constraint.

**Hardware reality:** The i7-8565U with 8GB RAM can run approximately:

- Llama 3.2 3B (4-bit): fast, weak reasoning
- Phi-3 Mini (3.8B, 4-bit): fast, better structured output, still limited
- Llama 3.1 8B (4-bit): borderline, may OOM under full context

7B/8B quantized models are not suitable for nuanced thesis review or multi-
factor observation generation. They are suitable for lightweight tasks like
replay summarization or candidate classification with constrained prompts.

**Pros:**

- Fully local. Zero API cost. No rate limits. Works offline.
- Privacy-preserving for any future scenario where trade data becomes sensitive.
- Available today.

**Cons:**

- Model quality at 7B is meaningfully below Groq's 70B for all four target tasks.
- Slow on this hardware. Llama 3.1 8B generates ~20-40 tokens/second on the
  i7-8565U, making a 500-token advisory response take 12-25 seconds.
- No fallback for out-of-memory conditions.

**Product impact:** Acceptable for lightweight structural tasks (prompt template
testing, syntax checking, simple classification). Not suitable for substantive
advisory tasks — thesis review, observation generation, and candidate screening
require reasoning depth that 7B quantized models cannot reliably provide.

**Deferred.** Local model integration is not in scope for the initial adapter
implementation. If lightweight local tasks are later identified (e.g., pre-
screening candidate text for formatting issues before sending to a larger model),
Ollama integration can be added to LiteLLM routing as a config-only change.

---

#### Approach E — LangChain / LlamaIndex Abstraction Layer

Not recommended.

LangChain and LlamaIndex are high-level orchestration frameworks that introduce
significant dependency weight and opinionated abstractions that conflict with
TradeForge's clean domain boundary architecture. The `AIAdvisoryProvider`
protocol is already the correct abstraction. No framework is needed on top of it.

---

### Recommendation

**Implement `OpenAICompatibleAdvisoryProvider` pointed at LiteLLM.**

The adapter is small — approximately 60-80 lines. It serializes an
`AdvisoryRequest` into a chat completions call, deserializes the response into
an `AdvisoryResponse`, and enforces the advisory boundary contracts.

The model is configured per-task in CredentialStore (not hardcoded). Groq's
Llama 3.1 70B is the starting model. NVIDIA NIM can replace or supplement it
via a LiteLLM config change. Anthropic Claude API can be added to LiteLLM later
without touching the adapter.

**Provider capability by task:**

| Task | Recommended model (via LiteLLM) | Quality assessment |
|---|---|---|
| Replay summary | Groq / Llama 3.1 8B (cheaper, fast) | Sufficient — structured summarization |
| Thesis review | Groq / Llama 3.1 70B | Good — nuanced reasoning needed |
| Observation generation | Groq / Llama 3.1 70B | Good — multi-factor structured output |
| Candidate screening | Groq / Llama 3.1 8B or 70B | Sufficient — ranking with rationale |

**Implementation path:**

1. Add `litellm` or `openai` Python package (they share the same client interface
   for OpenAI-compatible endpoints).
2. Add `LiteLLMCredential` shape to `CredentialStore` — `base_url`, `api_key`,
   `default_model`.
3. Implement `OpenAICompatibleAdvisoryProvider` in
   `src/infrastructure/advisory/litellm_provider.py`.
4. Write prompt templates for each of the four advisory tasks. This is the real
   work — the adapter mechanical code is small; the prompt quality determines
   advisory usefulness.
5. Wire through `create_app()` composition root.
6. Add on-demand API endpoints and frontend trigger buttons for each task.

**What it does not require:**

- Changes to domain advisory contracts
- Changes to `AIAdvisoryService`
- Changes to the credential architecture
- Any new ADR (the boundary model ADR-0006 already governs this)

---

## Data Sensitivity — Future Path

Current state: data is not sensitive. External API calls are acceptable.

If data classification changes (institutional use, regulated information):

1. Update LiteLLM configuration to route all calls to Ollama exclusively. No
   code change in TradeForge.
2. For partial sensitivity (specific fields): add a `sensitivity_level` field to
   `AdvisoryRequest` and filter out restricted fields before serializing the
   prompt. The adapter enforces this before the API call.
3. For full privacy requirements: evaluate upgrading the local machine or adding
   a dedicated inference server (e.g., a small GPU node running Ollama or vLLM
   with a larger model).

This transition path should be documented as a separate issue when the
requirement becomes concrete. No speculative infrastructure is needed now.

---

## Key Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| LiteLLM service outage on local machine | Medium | Advisory calls fail gracefully; lifecycle system is unaffected |
| Groq free-tier rate limit hit | Low (on-demand) | LiteLLM can fall back to NVIDIA NIM or Ollama |
| Prompt quality produces poor advisory output | High initially | On-demand mode means quality is visible before automation; iterate prompts before enabling automatic enrichment |
| API key leakage | Low | All keys go through `CredentialStore`; never in code or `.env` |
| LLM generates lifecycle-authoritative language | Addressed by design | `AIAdvisoryService` rejects responses where `authority != ADVISORY` |

---

## Next Steps

These are candidate issues. They should be filed and tracked before
implementation begins.

1. **Add `LiteLLMCredential` shape to credential domain** (**Done** — TF-F045)
2. **Implement `OpenAICompatibleAdvisoryProvider`** (**Done** — TF-F046)
3. **Implement prompt templates for replay summary** (**Done** — TF-F047)
4. **Implement prompt templates for thesis review** (**Done** — TF-F048)
5. **Implement prompt templates for observation generation** (**Done** — TF-F049)
6. **Implement prompt templates for candidate screening** (**Done** — TF-F050)
7. **Add on-demand API endpoints and frontend trigger surfaces** (**Done** — TF-F051/F052)
8. **Add advisory health check** (**Done** — TF-F052 `GET /advisory/health`)
9. **NVIDIA NIM via LiteLLM** — see section below (TF-F053)
10. **Document automatic enrichment hook points** — see section below (TF-F054)

---

## NVIDIA NIM Via LiteLLM (TF-F053)

**Status:** Investigation — no code changes required.

NVIDIA NIM free tier is provisioned. Integration is a LiteLLM configuration
change only — no TradeForge code changes needed.

### Confirmed LiteLLM Model String Format

NVIDIA NIM models are accessed via LiteLLM using the `nvidia_nim/` prefix:

```
nvidia_nim/meta/llama-3.1-70b-instruct
nvidia_nim/mistralai/mistral-7b-instruct-v0.3
nvidia_nim/microsoft/phi-3-mini-4k-instruct
```

### Credential Shape in CredentialStore

```
provider: litellm
base_url: https://integrate.api.nvidia.com/v1
api_key:  <NVIDIA NIM API key>
default_model: nvidia_nim/meta/llama-3.1-70b-instruct
```

### Known Rate Limits (NVIDIA NIM Free Tier)

- 40 requests/minute
- 1,000 requests/day per model family
- 4,096 tokens/request max on most free-tier models
- Better daily limits than Groq free tier for advisory use cases

### LiteLLM Configuration Addition

In `litellm_config.yaml` or equivalent:
```yaml
model_list:
  - model_name: nvidia-llama-70b
    litellm_params:
      model: nvidia_nim/meta/llama-3.1-70b-instruct
      api_base: https://integrate.api.nvidia.com/v1
      api_key: os.environ/NVIDIA_NIM_API_KEY
```

### Recommendation

Add NVIDIA NIM as a fallback model in LiteLLM routing. Use Groq
`llama-3.1-70b-versatile` as primary (lower latency) and NIM as fallback
when Groq rate limits are hit. No code change to TradeForge is required.

---

## Automatic Enrichment Lifecycle Hook Points (TF-F054)

**Status:** Specified — implementation deferred.

The following lifecycle events are candidates for automatic advisory enrichment
in a future milestone. Implementation requires an opt-in flag per decision
and a background task queue (not in scope for M13).

| Lifecycle Event | Advisory Task | Gating Conditions | Failure Behavior |
|---|---|---|---|
| `decision.thesis_created` | Thesis review | LiteLLM available; no existing thesis review for this decision | Silent skip; surface degraded state in workspace |
| `decision.thesis_revised` | Thesis review | LiteLLM available; revision is substantive (narrative changed) | Silent skip |
| `decision.plan_created` | Observation generation | LiteLLM available; market context available for symbol | Silent skip; suggest manual trigger |
| `decision.review_created` | Review assistance | LiteLLM available; review artifact has outcome and thesis comparison | Silent skip |
| `replay_session.completed` | Replay summary | LiteLLM available; replay contains at least 3 timeline entries | Silent skip |
| `advisory.candidate_ingested` (batch threshold) | Candidate screening | LiteLLM available; queue depth exceeds 5 unreviewed candidates | Silent skip |

### Operator Opt-In Model

Automatic enrichment should be gated by a per-decision or per-workspace
opt-in flag stored in operator preferences (not lifecycle events). This
prevents advisory calls from surprising the operator or consuming rate-limit
budget without consent.

Suggested flag: `auto_enrich_advisory: bool` in workspace/decision preferences.
Default: `false`. Operator sets to `true` to enable background enrichment.

### What This Does NOT Change

- All generated content remains advisory-only (`authority=ADVISORY`)
- No automatic persistence — operator acceptance still required
- No lifecycle state mutations from automatic enrichment
- ADR-0006 remains the governing boundary

### Implementation Note

When automatic enrichment is implemented, the preferred architecture is:
- FastAPI background task (not a synchronous route handler)
- Idempotency key per (decision_id, lifecycle_event, artifact_kind) to prevent
  duplicate generation on retry
- Max 1 background advisory call per lifecycle event per decision per day
