import {
  Activity,
  ClipboardCheck,
  Compass,
  History,
  Lightbulb,
  type LucideIcon,
  ShieldCheck,
} from "lucide-react";

export const WORKSPACE_CONTEXT_KEYS = [
  "persona_id",
  "persona_version",
  "workspace_id",
  "selected_workflow_id",
  "decision_id",
] as const;

export type WorkspaceContextKey = (typeof WORKSPACE_CONTEXT_KEYS)[number];

export type WorkspaceRouteId =
  | "operating"
  | "opportunity"
  | "plan-review"
  | "active-position"
  | "replay"
  | "review";

export type WorkspaceContext = Partial<Record<WorkspaceContextKey, string>>;

export type WorkspaceRouteDefinition = {
  id: WorkspaceRouteId;
  name: string;
  path: `/workspaces/${WorkspaceRouteId}`;
  operationalQuestion: string;
  contextSurface: string;
  authorityBoundary: string;
  Icon: LucideIcon;
};

export const DEFAULT_WORKSPACE_CONTEXT: Required<WorkspaceContext> = {
  persona_id: "persona.swing",
  persona_version: "2026-05-11",
  workspace_id: "workspace.operating",
  selected_workflow_id: "",
  decision_id: "",
};

export const WORKSPACE_ROUTES: readonly WorkspaceRouteDefinition[] = [
  {
    id: "operating",
    name: "Operating Workspace",
    path: "/workspaces/operating",
    operationalQuestion: "What requires operational attention now?",
    contextSurface: "Decision queue, active exposure, alerts, and review obligations.",
    authorityBoundary: "Routes attention to API-backed workflow surfaces.",
    Icon: Activity,
  },
  {
    id: "opportunity",
    name: "Opportunity Workspace",
    path: "/workspaces/opportunity",
    operationalQuestion: "What candidate decisions are developing?",
    contextSurface: "Ideas, theses in formation, setup context, and risk conditions.",
    authorityBoundary: "Supports scenario reasoning without generating trade authority.",
    Icon: Lightbulb,
  },
  {
    id: "plan-review",
    name: "Plan Review Workspace",
    path: "/workspaces/plan-review",
    operationalQuestion: "What risk is being intentionally authorized?",
    contextSurface: "Plan context, rule checks, risk model, and approval readiness.",
    authorityBoundary: "Approval must still route through lifecycle APIs.",
    Icon: ClipboardCheck,
  },
  {
    id: "active-position",
    name: "Active Position Workspace",
    path: "/workspaces/active-position",
    operationalQuestion: "What current exposure requires supervision?",
    contextSurface: "Position state, thesis integrity, risk, notes, and timeline.",
    authorityBoundary: "Position actions remain workflow-aware and API-mediated.",
    Icon: ShieldCheck,
  },
  {
    id: "replay",
    name: "Replay Workspace",
    path: "/workspaces/replay",
    operationalQuestion: "What historical context must be reconstructed?",
    contextSurface: "Replay timeline, visible context, source events, and annotations.",
    authorityBoundary: "Reconstruction depends on replay services, not client state.",
    Icon: History,
  },
  {
    id: "review",
    name: "Review Workspace",
    path: "/workspaces/review",
    operationalQuestion: "What should be learned from the decision?",
    contextSurface: "Review artifacts, rule adherence, replay highlights, and lessons.",
    authorityBoundary: "Review completion must be event-backed through runtime services.",
    Icon: Compass,
  },
] as const;

export const DEFAULT_WORKSPACE_ROUTE = WORKSPACE_ROUTES[0];

export const STAGE_TO_WORKSPACE: Partial<Record<string, WorkspaceRouteId>> = {
  Idea: "opportunity",
  Thesis: "plan-review",
  Plan: "plan-review",
  Approval: "plan-review",
  Execution: "active-position",
  Position: "active-position",
  Review: "review",
};

export function getRecommendedWorkspace(
  stage: string | null,
): WorkspaceRouteId | null {
  if (!stage) return null;
  return STAGE_TO_WORKSPACE[stage] ?? null;
}

export function findWorkspaceRoute(
  pathname: string,
): WorkspaceRouteDefinition {
  return (
    WORKSPACE_ROUTES.find((route) => route.path === pathname) ??
    DEFAULT_WORKSPACE_ROUTE
  );
}

export function readWorkspaceContext(search: string): WorkspaceContext {
  const params = new URLSearchParams(search);

  return WORKSPACE_CONTEXT_KEYS.reduce<WorkspaceContext>((context, key) => {
    const value = params.get(key);
    if (value !== null && value.trim() !== "") {
      context[key] = value;
    }

    return context;
  }, {});
}

export function mergeWorkspaceContext(
  context: WorkspaceContext,
  defaults: WorkspaceContext = DEFAULT_WORKSPACE_CONTEXT,
): Required<WorkspaceContext> {
  return {
    ...DEFAULT_WORKSPACE_CONTEXT,
    ...defaults,
    ...context,
  };
}

export function buildWorkspaceHref(
  route: WorkspaceRouteDefinition,
  context: WorkspaceContext,
): string {
  const decisionId = context.decision_id;
  const query =
    decisionId && decisionId.trim()
      ? `?decision_id=${encodeURIComponent(decisionId)}`
      : "";
  return `${route.path}${query}`;
}
