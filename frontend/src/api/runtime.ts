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

export type FundamentalsOverlay = {
  authority: "advisory";
  symbol: string;
  selected_provider_id: string | null;
  attempted_provider_ids: string[];
  used_fallback: boolean;
  is_available: boolean;
  fetched_at: string;
  errors: string[];
  company_name: string | null;
  sector: string | null;
  industry: string | null;
  revenue: string | null;
  net_income: string | null;
  price_earnings: string | null;
  return_on_equity: string | null;
  data_as_of: string | null;
};

export async function fetchFundamentalsContext(
  symbol: string,
  signal?: AbortSignal,
): Promise<FundamentalsOverlay> {
  const params = new URLSearchParams({ symbol });
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
