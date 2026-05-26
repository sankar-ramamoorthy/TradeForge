export type EntityReferencePayload = {
  entity_type: string;
  entity_id: string;
};

export type LifecycleTransitionRequest = {
  requested_stage: string;
  timestamp: string;
  persona_id: string;
  workspace_id: string | null;
  entity_references: EntityReferencePayload[];
  payload: Record<string, unknown>;
  provenance: Record<string, unknown>;
};

export type LifecycleValidationResult = {
  current_stage: string | null;
  requested_stage: string;
  is_valid: boolean;
  expected_stage: string | null;
  reason: string | null;
};

export type LifecycleTransitionResponse = {
  appended: boolean;
  event_type: string;
  timestamp: string;
  persona_id: string;
  workspace_id: string | null;
  validation: LifecycleValidationResult;
};

export type WorkspaceApiParams = {
  persona_id: string;
  persona_version: string;
  workspace_id: string;
  workflow_id?: string;
  decision_id?: string;
};

export type WorkspaceSourceEventReference = {
  event_type: string;
  timestamp_iso: string;
  entity_references: EntityReferencePayload[];
};

export type WorkspaceProjectionField = {
  name: string;
  authority: string;
  source_inputs: string[];
  source_event_count: number;
  source_event_types: string[];
  source_events: WorkspaceSourceEventReference[];
};

export type WorkspaceProjection = {
  route_id: string;
  authority: string;
  operational_question: string;
  lifecycle_state: { current_stage: string } | null;
  source_event_count: number;
  source_event_types: string[];
  fields: Record<string, WorkspaceProjectionField>;
  authority_boundaries: string[];
};

export type AttentionItemPriority = "low" | "medium" | "high" | "critical";

export type AttentionItem = {
  item_id: string;
  category: string;
  reason: string;
  priority: number;
  priority_label: AttentionItemPriority;
  route_id: string;
  explanation: string;
  lifecycle_stage: string | null;
  source_event_count: number;
  source_event_types: string[];
};

export type OperatingAttentionQueue = {
  authority: string;
  persona_id: string;
  persona_version: string;
  workspace_id: string;
  workflow_id: string | null;
  decision_id: string | null;
  items: AttentionItem[];
  authority_boundaries: string[];
};

export type RuntimeStatus = {
  status: "ok";
  runtime: "tradeforge";
  boundary: "http";
  owns_domain_rules: false;
};

export type RuntimeSession = {
  session_id: string;
  authority: "session";
  user: {
    user_id: string;
    display_name: string;
  };
  active_context: {
    persona_id: string;
    persona_version: string;
    workspace_id: string;
    selected_workflow_id: string | null;
    decision_id: string | null;
  };
  owns_persona_semantics: false;
  owns_lifecycle_authority: false;
  owns_event_truth: false;
};

async function readOperationalJson<T>(
  response: Response,
  label: string,
): Promise<T> {
  const contentType = response.headers.get("content-type") ?? "";
  const body = await response.text();
  const isJson = contentType.toLowerCase().includes("application/json");

  if (!isJson) {
    throw new Error(
      `${label} returned a non-JSON response. Check the local dev proxy and API route configuration.`,
    );
  }

  let parsed: unknown;
  try {
    parsed = body ? JSON.parse(body) : null;
  } catch {
    throw new Error(`${label} returned malformed JSON.`);
  }

  if (!response.ok) {
    const detail =
      typeof parsed === "object" && parsed !== null && "detail" in parsed
        ? String((parsed as { detail: unknown }).detail)
        : `HTTP ${response.status}`;
    throw new Error(`${label} failed: ${detail}`);
  }

  return parsed as T;
}

export async function fetchRuntimeStatus(
  signal?: AbortSignal
): Promise<RuntimeStatus> {
  const response = await fetch("/health", { signal });

  if (!response.ok) {
    throw new Error(`Runtime status request failed: ${response.status}`);
  }

  return response.json() as Promise<RuntimeStatus>;
}

export async function fetchRuntimeSession(
  signal?: AbortSignal
): Promise<RuntimeSession> {
  const response = await fetch("/session", { signal });

  if (!response.ok) {
    throw new Error(`Runtime session request failed: ${response.status}`);
  }

  return response.json() as Promise<RuntimeSession>;
}

function buildWorkspaceQuery(params: WorkspaceApiParams): string {
  const urlParams = new URLSearchParams();
  urlParams.set("persona_id", params.persona_id);
  urlParams.set("persona_version", params.persona_version);
  urlParams.set("workspace_id", params.workspace_id);
  if (params.workflow_id) urlParams.set("workflow_id", params.workflow_id);
  if (params.decision_id) urlParams.set("decision_id", params.decision_id);
  return urlParams.toString();
}

export async function fetchWorkspaceProjection(
  routeId: string,
  params: WorkspaceApiParams,
  signal?: AbortSignal,
): Promise<WorkspaceProjection> {
  const query = buildWorkspaceQuery(params);
  const response = await fetch(`/workspaces/${routeId}?${query}`, { signal });

  if (!response.ok) {
    throw new Error(`Workspace projection request failed: ${response.status}`);
  }

  return response.json() as Promise<WorkspaceProjection>;
}

export async function postLifecycleTransition(
  request: LifecycleTransitionRequest,
  signal?: AbortSignal,
): Promise<LifecycleTransitionResponse> {
  const response = await fetch("/lifecycle/transitions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
    signal,
  });

  if (!response.ok) {
    const detail = await response.json().catch(() => null);
    const message =
      typeof detail === "object" &&
      detail !== null &&
      "detail" in detail &&
      typeof (detail as Record<string, unknown>).detail === "object"
        ? ((detail as Record<string, { message?: string }>).detail?.message ??
          `Lifecycle transition failed: ${response.status}`)
        : `Lifecycle transition failed: ${response.status}`;
    throw new Error(message);
  }

  return response.json() as Promise<LifecycleTransitionResponse>;
}

export type ReplayTimelineEntry = {
  source_sequence: number;
  kind: string;
  event_type: string;
  event_domain: string;
  timestamp: string;
  persona_id: string;
  workspace_id: string | null;
  entity_references: EntityReferencePayload[];
  payload: Record<string, unknown>;
  provenance: Record<string, unknown>;
  lifecycle_stage: string | null;
};

export type ReplayTimeline = {
  authority: string;
  source_event_count: number;
  entries: ReplayTimelineEntry[];
};

export type MarketSnapshotOverlay = {
  symbol: string;
  provider_id: string;
  fetched_at: string;
  data_as_of: string;
  open: string;
  high: string;
  low: string;
  close: string;
  volume: number;
  regime: string;
  interpretation_headline: string;
  interpretation_detail: string;
};

export type MarketContextOverlay = {
  authority: "advisory";
  provider_id: string;
  fetched_at: string;
  available: MarketSnapshotOverlay[];
  unavailable_symbols: string[];
  is_complete: boolean;
  is_partial: boolean;
  is_empty: boolean;
  attempts: ProviderAttempt[];
};

export async function fetchMarketContext(
  symbols: string[],
  signal?: AbortSignal,
): Promise<MarketContextOverlay> {
  const urlParams = new URLSearchParams();
  urlParams.set("symbols", symbols.join(","));
  const response = await fetch(
    `/workspaces/market-context?${urlParams.toString()}`,
    { signal },
  );

  if (!response.ok) {
    throw new Error(`Market context request failed: ${response.status}`);
  }

  return response.json() as Promise<MarketContextOverlay>;
}

export type CapabilityResolution = {
  capability: string;
  preferred_provider_id: string;
  fallback_provider_ids: string[];
  configured_provider_ids: string[];
  selected_provider_id: string | null;
  used_fallback: boolean;
  is_available: boolean;
};

export type ProviderConfiguration = {
  authority: "advisory";
  providers: { provider_id: string; capabilities: string[] }[];
  resolutions: CapabilityResolution[];
};

export type ProviderGovernanceRouteAlias = {
  alias: string;
  advisory_role: string;
  advisory_usage_domain: string;
  configured: boolean;
  availability_status: "configured" | "not_configured" | "unknown";
  route_target_model: string | null;
  fallback_model: string | null;
  route_target_provider_id: string | null;
  fallback_provider_id: string | null;
  underlying_provider_id: string | null;
  reachability: "not_checked" | "available" | "unavailable" | "unknown";
};

export type ProviderGovernanceAiGateway = {
  gateway_id: "litellm";
  configured: boolean;
  status: "configured" | "not_configured" | "unavailable" | "unknown";
  provider_id: string | null;
  gateway_url: string | null;
  default_model: string | null;
  fallback_model: string | null;
  primary_provider_id: string | null;
  fallback_provider_id: string | null;
  underlying_provider_id: string | null;
  reachability: "not_checked" | "available" | "unavailable" | "unknown";
  route_aliases: ProviderGovernanceRouteAlias[];
  lifecycle_authority: false;
  execution_authority: false;
  event_ledger_authority: false;
};

export type ProviderGovernanceProvider = {
  provider_id: string;
  capabilities: string[];
  registry_configured: boolean;
  credential_required: boolean;
  credential_status: string;
  health_status: string;
  authority: "operational";
  is_canonical: false;
};

export type ProviderGovernanceDiagnosticSummary = {
  status: "ok" | "degraded" | "not_configured";
  retained_history_available: false;
  event_ledger_authority: false;
  diagnostic_classes: string[];
};

export type ProviderGovernance = {
  authority: "operational";
  is_canonical: false;
  generated_at: string;
  lifecycle_authority: false;
  event_ledger_writes: false;
  advisory_boundary: string[];
  providers: ProviderGovernanceProvider[];
  credentials: {
    provider_id: string;
    credential_required: boolean;
    configured: boolean;
    status: string;
    credential_record_status: string | null;
    rotated_at: string | null;
    last_validated_at: string | null;
    exposes_secret_values: false;
  }[];
  routes: CapabilityResolution[];
  diagnostics: ProviderGovernanceDiagnosticSummary;
  ai_gateway: ProviderGovernanceAiGateway;
};

export async function fetchProviderGovernance(
  signal?: AbortSignal,
): Promise<ProviderGovernance> {
  const response = await fetch("/provider-governance", { signal });
  if (!response.ok) {
    throw new Error(`Provider governance request failed: ${response.status}`);
  }
  return response.json() as Promise<ProviderGovernance>;
}

export async function fetchProviderGovernanceAiGateway(
  signal?: AbortSignal,
): Promise<ProviderGovernanceAiGateway> {
  const response = await fetch("/provider-governance/ai-gateway", { signal });
  if (!response.ok) {
    throw new Error(`AI gateway visibility request failed: ${response.status}`);
  }
  return response.json() as Promise<ProviderGovernanceAiGateway>;
}

export type AdvisoryModelSelection = {
  gateway_id: "litellm";
  configured: boolean;
  discovery_status: "available" | "unavailable" | "not_configured";
  available_models: string[];
  selected_primary_model: string | null;
  selected_fallback_model: string | null;
  selected_primary_provider_id: string | null;
  selected_fallback_provider_id: string | null;
  gateway_url: string | null;
  authority: "operational";
  is_canonical: false;
  lifecycle_authority: false;
  execution_authority: false;
  event_ledger_writes: false;
};

export async function fetchAdvisoryModelSelection(
  signal?: AbortSignal,
): Promise<AdvisoryModelSelection> {
  const response = await fetch(
    "/provider-governance/ai-gateway/model-selection",
    { signal },
  );
  return readOperationalJson<AdvisoryModelSelection>(
    response,
    "Advisory model selection request",
  );
}

export async function updateAdvisoryModelSelection(
  selection: {
    primary_provider_id: string;
    primary_model: string;
    fallback_provider_id: string | null;
    fallback_model: string | null;
  },
  signal?: AbortSignal,
): Promise<AdvisoryModelSelection> {
  const response = await fetch(
    "/provider-governance/ai-gateway/model-selection",
    {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(selection),
      signal,
    },
  );
  return readOperationalJson<AdvisoryModelSelection>(
    response,
    "Advisory model selection update",
  );
}

export type LLMProviderSecretInjection = {
  gateway_id: "litellm";
  authority: "operational";
  is_canonical: false;
  exposes_secret_values: false;
  runtime_decryption_boundary: "composition";
  reload_semantics: "credential_write_triggers_provider_reload";
  injectable_environment_variables: string[];
  provider_secrets: {
    provider_id: string;
    display_name: string;
    litellm_environment_variable: string;
    configured: boolean;
    available_for_runtime_injection: boolean;
  }[];
  lifecycle_authority: false;
  execution_authority: false;
  event_ledger_writes: false;
};

export async function fetchLLMProviderSecretInjection(
  signal?: AbortSignal,
): Promise<LLMProviderSecretInjection> {
  const response = await fetch(
    "/provider-governance/ai-gateway/provider-secret-injection",
    { signal },
  );
  return readOperationalJson<LLMProviderSecretInjection>(
    response,
    "LLM provider secret injection request",
  );
}

export async function fetchProviderConfiguration(
  signal?: AbortSignal,
): Promise<ProviderConfiguration> {
  const response = await fetch("/workspaces/provider-configuration", { signal });
  if (!response.ok) {
    throw new Error(`Provider configuration request failed: ${response.status}`);
  }
  return response.json() as Promise<ProviderConfiguration>;
}

export async function updateProviderPreference(
  capability: string,
  preferred_provider_id: string,
  fallback_provider_ids: string[],
  signal?: AbortSignal,
): Promise<ProviderConfiguration> {
  const response = await fetch(`/workspaces/provider-configuration/${capability}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ preferred_provider_id, fallback_provider_ids }),
    signal,
  });
  if (!response.ok) {
    throw new Error(`Provider preference update failed: ${response.status}`);
  }
  return response.json() as Promise<ProviderConfiguration>;
}

// --------------------------------------------------------------------------- //
// Credential management (TF-F055)                                              //
// --------------------------------------------------------------------------- //

export type ProviderCredentialField = {
  name: string;
  label: string;
  secret: boolean;
  optional?: boolean;
};

export const PROVIDER_CREDENTIAL_SCHEMAS: Record<string, ProviderCredentialField[]> = {
  yfinance: [],
  polygon: [{ name: "api_key", label: "API Key", secret: true }],
  alpaca: [
    { name: "api_key", label: "API Key", secret: true },
    { name: "secret_key", label: "Secret Key", secret: true },
  ],
  fmp: [{ name: "api_key", label: "API Key", secret: true }],
  alpha_vantage: [{ name: "api_key", label: "API Key", secret: true }],
  llm_groq: [{ name: "api_key", label: "API Key", secret: true }],
  llm_nvidia_nim: [{ name: "api_key", label: "API Key", secret: true }],
  llm_openai: [{ name: "api_key", label: "API Key", secret: true }],
  llm_anthropic: [{ name: "api_key", label: "API Key", secret: true }],
  llm_google: [{ name: "api_key", label: "API Key", secret: true }],
  litellm: [
    { name: "base_url", label: "Base URL", secret: false },
    { name: "api_key", label: "API Key", secret: true },
  ],
};

export type CredentialFieldStatus = {
  name: string;
  masked_value: string | null;
  display_value: string | null;
};

export type CredentialStatus = {
  provider_id: string;
  configured: boolean;
  status: string | null;
  rotated_at: string | null;
  last_validated_at: string | null;
  fields: CredentialFieldStatus[];
  master_key_configured: boolean;
};

export type CredentialListResponse = {
  credentials: CredentialStatus[];
  master_key_configured: boolean;
};

export async function fetchCredentials(
  signal?: AbortSignal,
): Promise<CredentialListResponse> {
  const response = await fetch("/admin/credentials", { signal });
  if (!response.ok) {
    throw new Error(`Credential list request failed: ${response.status}`);
  }
  return response.json() as Promise<CredentialListResponse>;
}

export async function updateCredential(
  provider_id: string,
  fields: Record<string, string>,
  signal?: AbortSignal,
): Promise<CredentialStatus> {
  const response = await fetch(`/admin/credentials/${provider_id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ fields }),
    signal,
  });
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`Credential update failed (${response.status}): ${detail}`);
  }
  return response.json() as Promise<CredentialStatus>;
}

export async function revokeCredential(
  provider_id: string,
  signal?: AbortSignal,
): Promise<CredentialStatus> {
  const response = await fetch(`/admin/credentials/${provider_id}`, {
    method: "DELETE",
    signal,
  });
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`Credential revoke failed (${response.status}): ${detail}`);
  }
  return response.json() as Promise<CredentialStatus>;
}

export async function validateCredential(
  provider_id: string,
  signal?: AbortSignal,
): Promise<CredentialStatus> {
  const response = await fetch(`/admin/credentials/${provider_id}/validate`, {
    method: "POST",
    signal,
  });
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`Credential validation failed (${response.status}): ${detail}`);
  }
  return response.json() as Promise<CredentialStatus>;
}

// --------------------------------------------------------------------------- //

export type FundamentalsOverlay = {
  authority: "advisory";
  symbol: string;
  instrument_kind: "equity" | "etf" | "unknown";
  requested_context_type: "company_fundamentals" | "etf_context";
  coverage_status: "available" | "unavailable" | "unsupported";
  alternative_context_type: "company_fundamentals" | "etf_context" | null;
  selected_provider_id: string | null;
  attempted_provider_ids: string[];
  used_fallback: boolean;
  is_available: boolean;
  fetched_at: string;
  errors: string[];
  attempts: ProviderAttempt[];
  company_name: string | null;
  sector: string | null;
  industry: string | null;
  revenue: string | null;
  net_income: string | null;
  price_earnings: string | null;
  return_on_equity: string | null;
  data_as_of: string | null;
};

export type ProviderAttempt = {
  provider_id: string;
  attempted_at: string;
  outcome: "success" | "failure";
  failure_reason: string | null;
};

export async function fetchFundamentalsContext(
  symbol: string,
  instrumentKind: "equity" | "etf" | "unknown" = "equity",
  signal?: AbortSignal,
): Promise<FundamentalsOverlay> {
  const params = new URLSearchParams({ symbol, instrument_kind: instrumentKind });
  const response = await fetch(`/workspaces/fundamentals-context?${params}`, { signal });
  if (!response.ok) {
    throw new Error(`Fundamentals context request failed: ${response.status}`);
  }
  return response.json() as Promise<FundamentalsOverlay>;
}

export type ContextualMarketNote = {
  symbol: string;
  close: string;
  regime: string;
  provider_id: string;
  data_as_of: string;
  is_advisory: boolean;
};

export type ContextualSummary = {
  authority: "derived";
  persona_id: string;
  workspace_id: string;
  operational_headline: string;
  operational_details: string[];
  market_context_notes: ContextualMarketNote[];
  market_context_available: boolean;
  source_inputs: string[];
  authority_boundaries: string[];
};

export type AdvisoryInterpretation = {
  interpretation_id: string;
  artifact_id: string;
  observation_ids: string[];
  interpretation_kind: string;
  thesis_influence: string;
  contextual_weight: string;
  confidence_range: string;
  content: string;
  rationale: string;
  provenance_summary: string;
  caveats: string[];
  persona_id: string;
  workspace_id: string;
  capture_origin: string;
  decision_id: string | null;
  thesis_id: string | null;
  source_kinds: string[];
  tags: string[];
  captured_at: string;
  authority: "advisory";
  is_canonical: false;
  canonical_event_type: "advisory.interpretation_captured";
};

export type AdvisoryInterpretationList = {
  authority: "advisory";
  is_canonical: false;
  total_count: number;
  interpretations: AdvisoryInterpretation[];
};

export type AdvisoryGeneratedResponse = {
  request_id: string;
  artifact_kind: string;
  content: string;
  source_references: {
    source_kind: string;
    source_id: string;
    description: string | null;
  }[];
  caveats: string[];
  confidence: number;
  provenance: {
    provider_id: string;
    provider_version: string;
    model_id: string;
    generated_at: string;
    prompt_version: string | null;
  };
  authority: "advisory";
  is_canonical: false;
  requires_operator_acceptance: true;
};

export type AdvisoryRouteSmokeTestResponse = {
  gateway_id: "litellm";
  status: "available" | "unavailable" | "not_configured";
  diagnostic_message: string;
  provider_id: string | null;
  model_id: string | null;
  generated_at: string | null;
  content_preview: string | null;
  authority: "operational";
  is_canonical: false;
  lifecycle_authority: false;
  execution_authority: false;
  event_ledger_writes: false;
  advisory_response_authority: "advisory" | null;
};

export type AdvisoryCandidate = {
  candidate_id: string;
  symbol: string;
  summary: string;
  rationale: string;
  evidence: {
    evidence_id: string;
    source_kind: string;
    source_id: string;
    summary: string;
    observed_at: string | null;
    source_uri: string | null;
    artifact_id: string | null;
    captured_at: string | null;
    provenance_summary: string | null;
    caveats: string[];
    conflict_marker: string | null;
  }[];
  capture_origin: string;
  provenance_summary: string;
  uncertainty_band: string;
  caveats: string[];
  persona_id: string;
  workspace_id: string;
  source_observation_ids: string[];
  tags: string[];
  captured_at: string;
  authority: "advisory";
  is_canonical: false;
  canonical_event_type: "advisory.observation_captured";
  lifecycle_authority: false;
};

export type CandidateReviewQueue = {
  authority: "derived";
  is_canonical: false;
  persona_id: string;
  workspace_id: string;
  ordering: "captured_at_desc_then_candidate_id_asc";
  total_count: number;
  candidates: AdvisoryCandidate[];
};

export async function fetchCandidateReviewQueue(
  params: {
    persona_id: string;
    workspace_id: string;
    dismissed_candidate_ids?: string[];
  },
  signal?: AbortSignal,
): Promise<CandidateReviewQueue> {
  const urlParams = new URLSearchParams();
  urlParams.set("persona_id", params.persona_id);
  urlParams.set("workspace_id", params.workspace_id);
  for (const candidateId of params.dismissed_candidate_ids ?? []) {
    urlParams.append("dismissed_candidate_id", candidateId);
  }
  const response = await fetch(
    `/advisory/candidates/review-queue?${urlParams.toString()}`,
    { signal },
  );

  return readOperationalJson<CandidateReviewQueue>(
    response,
    "Candidate review queue request",
  );
}

export async function fetchAdvisoryInterpretations(
  params: {
    persona_id: string;
    workspace_id: string;
    decision_id?: string;
    thesis_id?: string;
  },
  signal?: AbortSignal,
): Promise<AdvisoryInterpretationList> {
  const urlParams = new URLSearchParams();
  urlParams.set("persona_id", params.persona_id);
  urlParams.set("workspace_id", params.workspace_id);
  if (params.decision_id) urlParams.set("decision_id", params.decision_id);
  if (params.thesis_id) urlParams.set("thesis_id", params.thesis_id);
  const response = await fetch(
    `/advisory/interpretations?${urlParams.toString()}`,
    { signal },
  );

  return readOperationalJson<AdvisoryInterpretationList>(
    response,
    "Advisory interpretations request",
  );
}

export async function generateThesisReview(
  params: {
    decision_id: string;
    persona_id: string;
    workspace_id: string;
    operator_question?: string;
  },
  signal?: AbortSignal,
): Promise<AdvisoryGeneratedResponse> {
  const response = await fetch("/advisory/thesis-review", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params),
    signal,
  });

  return readOperationalJson<AdvisoryGeneratedResponse>(
    response,
    "Advisory thesis review request",
  );
}

export async function smokeTestAdvisoryRoute(
  signal?: AbortSignal,
): Promise<AdvisoryRouteSmokeTestResponse> {
  const response = await fetch("/provider-governance/ai-gateway/smoke-test", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({}),
    signal,
  });

  return readOperationalJson<AdvisoryRouteSmokeTestResponse>(
    response,
    "Advisory route smoke test",
  );
}

export async function fetchContextualSummary(
  params: WorkspaceApiParams,
  symbols?: string[],
  signal?: AbortSignal,
): Promise<ContextualSummary> {
  const urlParams = new URLSearchParams();
  urlParams.set("persona_id", params.persona_id);
  urlParams.set("persona_version", params.persona_version);
  urlParams.set("workspace_id", params.workspace_id);
  if (params.workflow_id) urlParams.set("workflow_id", params.workflow_id);
  if (params.decision_id) urlParams.set("decision_id", params.decision_id);
  if (symbols && symbols.length > 0) {
    urlParams.set("symbols", symbols.join(","));
  }
  const response = await fetch(
    `/workspaces/contextual-summary?${urlParams.toString()}`,
    { signal },
  );

  if (!response.ok) {
    throw new Error(`Contextual summary request failed: ${response.status}`);
  }

  return response.json() as Promise<ContextualSummary>;
}

export async function fetchReplayTimeline(
  signal?: AbortSignal,
): Promise<ReplayTimeline> {
  const response = await fetch("/replay/timeline", { signal });

  if (!response.ok) {
    throw new Error(`Replay timeline request failed: ${response.status}`);
  }

  return response.json() as Promise<ReplayTimeline>;
}

export type NewTradeIdeaRequest = {
  symbol: string;
  initial_thesis?: string;
  persona_id: string;
  workspace_id: string;
  source_advisory_candidate_id?: string;
  advisory_candidate_promotion_intent?: "operator_promotes_advisory_candidate";
};

export type NewTradeIdeaResponse = {
  decision_id: string;
  symbol: string;
  event_type: string;
  timestamp: string;
};

export async function initNewTradeIdea(
  request: NewTradeIdeaRequest,
  signal?: AbortSignal,
): Promise<NewTradeIdeaResponse> {
  const response = await fetch("/lifecycle/decisions/init", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
    signal,
  });

  if (!response.ok) {
    const detail = await response.json().catch(() => null);
    const message =
      typeof detail === "object" &&
      detail !== null &&
      "detail" in detail &&
      typeof (detail as Record<string, unknown>).detail === "object"
        ? ((detail as Record<string, { message?: string }>).detail?.message ??
          `Trade idea initialization failed: ${response.status}`)
        : `Trade idea initialization failed: ${response.status}`;
    throw new Error(message);
  }

  return response.json() as Promise<NewTradeIdeaResponse>;
}

export type DevelopThesisRequest = {
  decision_id: string;
  symbol: string;
  narrative: string;
  catalysts: string[];
  assumptions: string[];
  invalidation_conditions: string[];
  confidence_level: number;
  regime_alignment?: string;
  persona_id: string;
  workspace_id: string;
};

export type DevelopThesisResponse = {
  decision_id: string;
  event_type: string;
  timestamp: string;
};

export async function postDevelopThesis(
  request: DevelopThesisRequest,
  signal?: AbortSignal,
): Promise<DevelopThesisResponse> {
  const response = await fetch("/lifecycle/decisions/develop-thesis", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
    signal,
  });

  if (!response.ok) {
    const detail = await response.json().catch(() => null);
    const message =
      typeof detail === "object" &&
      detail !== null &&
      "detail" in detail
        ? typeof (detail as Record<string, unknown>).detail === "object"
          ? ((detail as Record<string, { message?: string }>).detail?.message ??
            `Thesis development failed: ${response.status}`)
          : typeof (detail as Record<string, unknown>).detail === "string"
          ? String((detail as Record<string, unknown>).detail)
          : `Thesis development failed: ${response.status}`
        : `Thesis development failed: ${response.status}`;
    throw new Error(message);
  }

  return response.json() as Promise<DevelopThesisResponse>;
}

export type ThesisArtifact = {
  decision_id: string;
  symbol: string;
  narrative: string;
  catalysts: string[];
  assumptions: string[];
  invalidation_conditions: string[];
  confidence_level: number;
  regime_alignment: string;
  source_event_type: string;
  event_timestamp: string;
};

export async function fetchThesisArtifact(
  decisionId: string,
  signal?: AbortSignal,
): Promise<ThesisArtifact | null> {
  const response = await fetch(`/lifecycle/decisions/${encodeURIComponent(decisionId)}/thesis`, { signal });

  if (response.status === 404) {
    return null;
  }

  if (!response.ok) {
    throw new Error(`Thesis artifact request failed: ${response.status}`);
  }

  return response.json() as Promise<ThesisArtifact>;
}

export type CreatePlanRequest = {
  decision_id: string;
  symbol: string;
  entry_rationale: string;
  stop_rationale: string;
  target_rationale: string;
  sizing_rationale: string;
  execution_assumptions: string[];
  playbook_alignment?: string;
  persona_id: string;
  workspace_id: string;
};

export type CreatePlanResponse = {
  decision_id: string;
  event_type: string;
  timestamp: string;
};

export type TradePlanArtifact = {
  decision_id: string;
  symbol: string;
  entry_rationale: string;
  stop_rationale: string;
  target_rationale: string;
  sizing_rationale: string;
  execution_assumptions: string[];
  playbook_alignment: string;
  source_event_type: string;
  event_timestamp: string;
};

export async function postCreatePlan(
  request: CreatePlanRequest,
  signal?: AbortSignal,
): Promise<CreatePlanResponse> {
  const response = await fetch("/lifecycle/decisions/create-plan", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
    signal,
  });

  if (!response.ok) {
    const detail = await response.json().catch(() => null);
    const message =
      typeof detail === "object" && detail !== null && "detail" in detail
        ? typeof (detail as Record<string, unknown>).detail === "object"
          ? ((detail as Record<string, { message?: string }>).detail?.message ??
            `Plan creation failed: ${response.status}`)
          : `Plan creation failed: ${response.status}`
        : `Plan creation failed: ${response.status}`;
    throw new Error(message);
  }

  return response.json() as Promise<CreatePlanResponse>;
}

export async function fetchPlanArtifact(
  decisionId: string,
  signal?: AbortSignal,
): Promise<TradePlanArtifact | null> {
  const response = await fetch(
    `/lifecycle/decisions/${encodeURIComponent(decisionId)}/plan`,
    { signal },
  );

  if (response.status === 404) {
    return null;
  }

  if (!response.ok) {
    throw new Error(`Plan artifact request failed: ${response.status}`);
  }

  return response.json() as Promise<TradePlanArtifact>;
}

export type ReadinessCheck = {
  check_id: string;
  label: string;
  passed: boolean;
  advisory: boolean;
  message: string;
};

export type PlanReadiness = {
  decision_id: string;
  current_stage: string | null;
  next_allowed_transition: string | null;
  has_structured_thesis: boolean;
  has_structured_plan: boolean;
  can_proceed_to_approval: boolean;
  checks: ReadinessCheck[];
  authority: "derived";
};

export async function fetchPlanReadiness(
  decisionId: string,
  signal?: AbortSignal,
): Promise<PlanReadiness> {
  const response = await fetch(
    `/lifecycle/decisions/${encodeURIComponent(decisionId)}/plan-readiness`,
    { signal },
  );

  if (!response.ok) {
    throw new Error(`Plan readiness request failed: ${response.status}`);
  }

  return response.json() as Promise<PlanReadiness>;
}

export type CompleteReviewRequest = {
  decision_id: string;
  symbol: string;
  thesis_vs_outcome: string;
  decision_quality: number;
  execution_quality: number;
  discipline_observations: string;
  lessons_learned: string[];
  behavioral_observations?: string;
  persona_id: string;
  workspace_id: string;
};

export type CompleteReviewResponse = {
  decision_id: string;
  event_type: string;
  timestamp: string;
};

export type ReviewReflectionArtifact = {
  decision_id: string;
  symbol: string;
  thesis_vs_outcome: string;
  decision_quality: number;
  execution_quality: number;
  discipline_observations: string;
  lessons_learned: string[];
  behavioral_observations: string;
  source_event_type: string;
  event_timestamp: string;
};

export async function postCompleteReview(
  request: CompleteReviewRequest,
  signal?: AbortSignal,
): Promise<CompleteReviewResponse> {
  const response = await fetch("/lifecycle/decisions/complete-review", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
    signal,
  });

  if (!response.ok) {
    const detail = await response.json().catch(() => null);
    const message =
      typeof detail === "object" && detail !== null && "detail" in detail
        ? typeof (detail as Record<string, unknown>).detail === "object"
          ? ((detail as Record<string, { message?: string }>).detail?.message ??
            `Review completion failed: ${response.status}`)
          : `Review completion failed: ${response.status}`
        : `Review completion failed: ${response.status}`;
    throw new Error(message);
  }

  return response.json() as Promise<CompleteReviewResponse>;
}

export async function fetchReviewReflection(
  decisionId: string,
  signal?: AbortSignal,
): Promise<ReviewReflectionArtifact | null> {
  const response = await fetch(
    `/lifecycle/decisions/${encodeURIComponent(decisionId)}/review`,
    { signal },
  );

  if (response.status === 404) return null;

  if (!response.ok) {
    throw new Error(`Review reflection request failed: ${response.status}`);
  }

  return response.json() as Promise<ReviewReflectionArtifact>;
}

export type ScenarioBranchType =
  | "primary"
  | "alternative"
  | "invalidation"
  | "regime_transition";

export type CreateScenarioBranchRequest = {
  decision_id: string;
  branch_type: ScenarioBranchType;
  condition: string;
  implication: string;
  confidence: number;
  notes?: string;
  persona_id: string;
  workspace_id: string;
};

export type ScenarioBranch = {
  branch_type: ScenarioBranchType;
  condition: string;
  implication: string;
  confidence: number;
  notes: string;
  event_timestamp: string;
};

export type ScenarioBranchList = {
  decision_id: string;
  total_branches: number;
  branches: ScenarioBranch[];
};

export async function postCreateScenarioBranch(
  request: CreateScenarioBranchRequest,
  signal?: AbortSignal,
): Promise<{ decision_id: string; branch_type: string; event_type: string; timestamp: string }> {
  const response = await fetch("/lifecycle/decisions/create-scenario-branch", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
    signal,
  });

  if (!response.ok) {
    const detail = await response.json().catch(() => null);
    const message =
      typeof detail === "object" && detail !== null && "detail" in detail
        ? typeof (detail as Record<string, unknown>).detail === "object"
          ? ((detail as Record<string, { message?: string }>).detail?.message ??
            `Scenario branch creation failed: ${response.status}`)
          : `Scenario branch creation failed: ${response.status}`
        : `Scenario branch creation failed: ${response.status}`;
    throw new Error(message);
  }

  return response.json() as Promise<{ decision_id: string; branch_type: string; event_type: string; timestamp: string }>;
}

export async function fetchScenarioBranches(
  decisionId: string,
  signal?: AbortSignal,
): Promise<ScenarioBranchList> {
  const response = await fetch(
    `/lifecycle/decisions/${encodeURIComponent(decisionId)}/scenario-branches`,
    { signal },
  );

  if (!response.ok) {
    throw new Error(`Scenario branches request failed: ${response.status}`);
  }

  return response.json() as Promise<ScenarioBranchList>;
}

export type CognitiveSnapshotThesis = {
  narrative: string;
  catalysts: string[];
  assumptions: string[];
  invalidation_conditions: string[];
  confidence_level: number;
  regime_alignment: string;
  event_type: string;
  event_timestamp: string;
};

export type CognitiveSnapshotPlan = {
  entry_rationale: string;
  stop_rationale: string;
  target_rationale: string;
  sizing_rationale: string;
  execution_assumptions: string[];
  playbook_alignment: string;
  event_timestamp: string;
};

export type CognitiveSnapshotBranch = {
  branch_type: string;
  condition: string;
  implication: string;
  confidence: number;
  notes: string;
  event_timestamp: string;
};

export type CognitiveSnapshot = {
  decision_id: string;
  snapshot_at: string;
  event_count_at_snapshot: number;
  current_stage: string | null;
  thesis: CognitiveSnapshotThesis | null;
  plan: CognitiveSnapshotPlan | null;
  scenario_branches: CognitiveSnapshotBranch[];
  authority: "derived";
};

export async function fetchCognitiveSnapshot(
  decisionId: string,
  at?: string,
  signal?: AbortSignal,
): Promise<CognitiveSnapshot> {
  const urlParams = new URLSearchParams();
  if (at) urlParams.set("at", at);
  const query = urlParams.toString();
  const response = await fetch(
    `/lifecycle/decisions/${encodeURIComponent(decisionId)}/cognitive-snapshot${query ? `?${query}` : ""}`,
    { signal },
  );

  if (!response.ok) {
    throw new Error(`Cognitive snapshot request failed: ${response.status}`);
  }

  return response.json() as Promise<CognitiveSnapshot>;
}

export type AnnotationType =
  | "observation"
  | "question"
  | "insight"
  | "postmortem";

export type Annotation = {
  sequence: number;
  annotated_event_type: string;
  note: string;
  annotation_type: AnnotationType;
  created_at: string;
};

export type AnnotationList = {
  decision_id: string;
  total_annotations: number;
  annotations: Annotation[];
};

export async function postCreateAnnotation(
  request: {
    decision_id: string;
    sequence: number;
    annotated_event_type: string;
    note: string;
    annotation_type: AnnotationType;
    persona_id: string;
    workspace_id: string;
  },
  signal?: AbortSignal,
): Promise<{ decision_id: string; sequence: number; event_type: string; timestamp: string }> {
  const response = await fetch("/lifecycle/decisions/create-annotation", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
    signal,
  });

  if (!response.ok) {
    const detail = await response.json().catch(() => null);
    const message =
      typeof detail === "object" && detail !== null && "detail" in detail
        ? typeof (detail as Record<string, unknown>).detail === "object"
          ? ((detail as Record<string, { message?: string }>).detail?.message ??
            `Annotation creation failed: ${response.status}`)
          : `Annotation creation failed: ${response.status}`
        : `Annotation creation failed: ${response.status}`;
    throw new Error(message);
  }

  return response.json() as Promise<{ decision_id: string; sequence: number; event_type: string; timestamp: string }>;
}

export async function fetchAnnotations(
  decisionId: string,
  signal?: AbortSignal,
): Promise<AnnotationList> {
  const response = await fetch(
    `/lifecycle/decisions/${encodeURIComponent(decisionId)}/annotations`,
    { signal },
  );

  if (!response.ok) {
    throw new Error(`Annotations request failed: ${response.status}`);
  }

  return response.json() as Promise<AnnotationList>;
}

export type PlaybookAlignedDecision = {
  decision_id: string;
  symbol: string;
  current_stage: string | null;
};

export type PlaybookGroup = {
  playbook_name: string;
  decision_count: number;
  decisions: PlaybookAlignedDecision[];
};

export type PlaybookSummary = {
  playbooks: PlaybookGroup[];
  unaligned_decision_count: number;
  total_decisions_with_plan: number;
  authority: "derived";
};

export async function fetchPlaybookSummary(
  signal?: AbortSignal,
): Promise<PlaybookSummary> {
  const response = await fetch("/workspaces/playbook-summary", { signal });

  if (!response.ok) {
    throw new Error(`Playbook summary request failed: ${response.status}`);
  }

  return response.json() as Promise<PlaybookSummary>;
}

export type DecisionSummary = {
  decision_id: string;
  symbol: string;
  current_stage: string | null;
  created_at: string;
  last_updated_at: string;
};

export type DecisionListResponse = {
  decisions: DecisionSummary[];
  total: number;
};

export async function fetchDecisionList(
  signal?: AbortSignal,
): Promise<DecisionListResponse> {
  const response = await fetch("/lifecycle/decisions", { signal });
  if (!response.ok) {
    throw new Error(`Decision list request failed: ${response.status}`);
  }
  return response.json() as Promise<DecisionListResponse>;
}

export async function fetchOperatingAttentionQueue(
  params: WorkspaceApiParams,
  signal?: AbortSignal,
): Promise<OperatingAttentionQueue> {
  const query = buildWorkspaceQuery(params);
  const response = await fetch(
    `/workspaces/operating/attention?${query}`,
    { signal },
  );

  if (!response.ok) {
    throw new Error(`Attention queue request failed: ${response.status}`);
  }

  return response.json() as Promise<OperatingAttentionQueue>;
}
