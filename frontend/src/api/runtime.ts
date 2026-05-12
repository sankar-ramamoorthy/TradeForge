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
