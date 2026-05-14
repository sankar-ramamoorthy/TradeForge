import { initNewTradeIdea, postLifecycleTransition } from "./api/runtime";
import { setActiveDecision } from "./activeDecision";

const STORAGE_KEY = "tradeforge.walkthrough_session";
const WALKTHROUGH_SYMBOL = "AAPL";
const WALKTHROUGH_THESIS =
  "Breakout above the 200-day moving average on above-average volume. " +
  "Technology sector momentum intact with strong institutional participation.";

export type WalkthroughStepDef = {
  stepIndex: number;
  totalSteps: number;
  workspacePath: string;
  title: string;
  explanation: string;
  actionLabel: string;
  transitionStages: string[];
  nextWorkspacePath: string | null;
};

export type WalkthroughSession = {
  decision_id: string;
  symbol: string;
  persona_id: string;
  persona_version: string;
  workspace_id: string;
  current_step_index: number;
  active: boolean;
};

const TOTAL = 7;

export const WALKTHROUGH_STEPS: WalkthroughStepDef[] = [
  {
    stepIndex: 0,
    totalSteps: TOTAL,
    workspacePath: "/workspaces/operating",
    title: "The Operating Workspace",
    explanation:
      "This is the Operating Workspace — your daily hub for what requires " +
      "attention. A new AAPL trade idea has just been initialized and appears " +
      "in your decision queue, awaiting thesis development.",
    actionLabel: "Develop the Thesis →",
    transitionStages: ["Thesis"],
    nextWorkspacePath: "/workspaces/opportunity",
  },
  {
    stepIndex: 1,
    totalSteps: TOTAL,
    workspacePath: "/workspaces/opportunity",
    title: "The Opportunity Workspace",
    explanation:
      "The Opportunity Workspace is where you examine and formalize the thesis " +
      "behind a trade idea. Every decision begins with an explicit thesis — a " +
      "structured reason grounded in observable conditions, not a gut feeling.",
    actionLabel: "Create the Plan →",
    transitionStages: ["Plan"],
    nextWorkspacePath: "/workspaces/plan-review",
  },
  {
    stepIndex: 2,
    totalSteps: TOTAL,
    workspacePath: "/workspaces/plan-review",
    title: "Plan Review — Document the Plan",
    explanation:
      "The Plan Review Workspace captures your explicit trade plan: entry, " +
      "position sizing, stop loss, and targets. A written plan separates " +
      "disciplined decision-making from reactive action. Plans must be explicit " +
      "before they can be authorized.",
    actionLabel: "Authorize the Plan →",
    transitionStages: ["Approval"],
    nextWorkspacePath: "/workspaces/plan-review",
  },
  {
    stepIndex: 3,
    totalSteps: TOTAL,
    workspacePath: "/workspaces/plan-review",
    title: "Plan Review — Authorize",
    explanation:
      "Authorization is a deliberate commitment checkpoint. You're confirming " +
      "that the plan meets your criteria and you'll execute it exactly as written. " +
      "This becomes an immutable event in your decision ledger — it cannot be revised.",
    actionLabel: "Record Execution and Open Position →",
    transitionStages: ["Execution", "Position"],
    nextWorkspacePath: "/workspaces/active-position",
  },
  {
    stepIndex: 4,
    totalSteps: TOTAL,
    workspacePath: "/workspaces/active-position",
    title: "Active Position Workspace",
    explanation:
      "The Active Position Workspace shows your open trade in full context. " +
      "Here you monitor thesis integrity — the original reason you entered. " +
      "Positions are managed against the thesis, not the P&L ticker.",
    actionLabel: "Begin the Review →",
    transitionStages: ["Review"],
    nextWorkspacePath: "/workspaces/review",
  },
  {
    stepIndex: 5,
    totalSteps: TOTAL,
    workspacePath: "/workspaces/review",
    title: "Review Workspace",
    explanation:
      "The Review Workspace captures what you learned. TradeForge deliberately " +
      "separates decision process quality from outcome — a disciplined process can " +
      "produce a loss; a sloppy one can produce a winner. Review builds long-term " +
      "operational discipline, not just attribution.",
    actionLabel: "Explore the Replay →",
    transitionStages: [],
    nextWorkspacePath: "/workspaces/replay",
  },
  {
    stepIndex: 6,
    totalSteps: TOTAL,
    workspacePath: "/workspaces/replay",
    title: "Replay Workspace — Complete",
    explanation:
      "The Replay Workspace reconstructs your complete decision history from " +
      "immutable events. Every stage — Idea through Review — is preserved and " +
      "replayable. This is TradeForge: structured operational cognition with " +
      "permanent, auditable memory.",
    actionLabel: "Finish Walkthrough",
    transitionStages: [],
    nextWorkspacePath: null,
  },
];

export function getWalkthroughSession(): WalkthroughSession | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as unknown;
    if (
      typeof parsed === "object" &&
      parsed !== null &&
      "decision_id" in parsed &&
      "active" in parsed &&
      typeof (parsed as Record<string, unknown>).decision_id === "string"
    ) {
      return parsed as WalkthroughSession;
    }
    return null;
  } catch {
    return null;
  }
}

export function setWalkthroughSession(session: WalkthroughSession): void {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(session));
  } catch {
    // fail silently
  }
}

export function clearWalkthroughSession(): void {
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch {
    // fail silently
  }
}

export type WalkthroughInitResult = {
  session: WalkthroughSession;
};

export async function initWalkthrough(options: {
  personaId: string;
  personaVersion: string;
  workspaceId: string;
}): Promise<WalkthroughInitResult> {
  const { personaId, personaVersion, workspaceId } = options;

  const init = await initNewTradeIdea({
    symbol: WALKTHROUGH_SYMBOL,
    initial_thesis: WALKTHROUGH_THESIS,
    persona_id: personaId,
    workspace_id: workspaceId,
  });

  const session: WalkthroughSession = {
    decision_id: init.decision_id,
    symbol: init.symbol,
    persona_id: personaId,
    persona_version: personaVersion,
    workspace_id: workspaceId,
    current_step_index: 0,
    active: true,
  };

  setWalkthroughSession(session);

  setActiveDecision({
    decision_id: init.decision_id,
    symbol: init.symbol,
    persona_id: personaId,
    persona_version: personaVersion,
    created_at: init.timestamp,
  });

  return { session };
}

export async function advanceWalkthroughStep(
  session: WalkthroughSession,
  step: WalkthroughStepDef,
): Promise<void> {
  if (step.transitionStages.length === 0) return;

  const decisionRef = [
    { entity_type: "decision", entity_id: session.decision_id },
    { entity_type: "ticker", entity_id: session.symbol },
  ];

  const base = {
    timestamp: new Date().toISOString(),
    persona_id: session.persona_id,
    workspace_id: session.workspace_id,
    entity_references: decisionRef,
    provenance: { actor: "walkthrough", source: "guided-walkthrough" },
  };

  for (const stageName of step.transitionStages) {
    await postLifecycleTransition({
      ...base,
      requested_stage: stageName,
      payload: { source: "guided-walkthrough" },
    });
  }
}
