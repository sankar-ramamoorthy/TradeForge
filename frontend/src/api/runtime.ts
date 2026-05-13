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

export type WorkspaceProjectionField = {
  name: string;
  authority: string;
  source_inputs: string[];
  source_event_count: number;
  source_event_types: string[];
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

export async function fetchReplayTimeline(
  signal?: AbortSignal,
): Promise<ReplayTimeline> {
  const response = await fetch("/replay/timeline", { signal });

  if (!response.ok) {
    throw new Error(`Replay timeline request failed: ${response.status}`);
  }

  return response.json() as Promise<ReplayTimeline>;
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
