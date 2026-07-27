import {
  initNewTradeIdea,
  postCompleteReview,
  postCreatePlan,
  postDevelopThesis,
  postLifecycleTransition,
} from "./api/runtime";
import { setActiveDecision } from "./activeDecision";

const STORAGE_KEY = "tradeforge.walkthrough_session";
const WALKTHROUGH_SYMBOL = "AAPL";
const WALKTHROUGH_THESIS =
  "AAPL is testing a breakout above a widely watched moving average. " +
  "I want to see whether volume confirms demand before treating the idea as actionable.";
const WALKTHROUGH_PLAN = {
  entry_rationale:
    "Enter only if price closes above resistance with volume confirming demand.",
  stop_rationale:
    "Exit if price closes back below the breakout level, because that invalidates the setup.",
  target_rationale:
    "Use the prior measured range to define a first target with at least two-to-one reward to risk.",
  sizing_rationale:
    "Size small enough that a stop loss costs no more than one planned risk unit.",
  execution_assumptions: [
    "Liquidity remains normal at the planned entry.",
    "No earnings event occurs before the first target window.",
  ],
  playbook_alignment: "guided-first-decision",
};
const WALKTHROUGH_REVIEW = {
  thesis_vs_outcome:
    "The walkthrough decision followed the written thesis and plan, so the review focuses on process discipline.",
  decision_quality: 4,
  execution_quality: 4,
  discipline_observations:
    "Each lifecycle step was recorded explicitly before moving to the next stage.",
  lessons_learned: [
    "Write the reason before planning the action.",
    "Review the process even when the example outcome is theoretical.",
  ],
  behavioral_observations:
    "Guided mode emphasizes sequencing over prediction.",
};

type WalkthroughAction =
  | "develop_thesis"
  | "create_plan"
  | "approve_plan"
  | "record_execution"
  | "complete_review"
  | "none";

export type WalkthroughGlossaryTerm = {
  term: string;
  definition: string;
};

export type WalkthroughStepDef = {
  stepIndex: number;
  totalSteps: number;
  workspacePath: string;
  title: string;
  explanation: string;
  actionLabel: string;
  action: WalkthroughAction;
  glossary: WalkthroughGlossaryTerm[];
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
    title: "Start With An Idea",
    explanation:
      "Guided mode created one example AAPL idea. It is not ready for action until you write the reason.",
    actionLabel: "Write the reason",
    action: "develop_thesis",
    glossary: [
      { term: "Idea", definition: "A symbol and early reason worth investigating." },
      { term: "Thesis", definition: "The written reason this idea might be worth acting on." },
    ],
    transitionStages: ["Thesis"],
    nextWorkspacePath: "/workspaces/opportunity",
  },
  {
    stepIndex: 1,
    totalSteps: TOTAL,
    workspacePath: "/workspaces/opportunity",
    title: "Turn The Reason Into A Plan",
    explanation:
      "The thesis is recorded. Next, define the entry, stop, target, sizing, and assumptions.",
    actionLabel: "Create the plan",
    action: "create_plan",
    glossary: [
      { term: "Plan", definition: "The written rules for entry, stop, target, and sizing." },
    ],
    transitionStages: ["Plan"],
    nextWorkspacePath: "/workspaces/plan-review",
  },
  {
    stepIndex: 2,
    totalSteps: TOTAL,
    workspacePath: "/workspaces/plan-review",
    title: "Approve Deliberately",
    explanation:
      "Approval confirms that the idea, reason, and plan are complete enough to act on.",
    actionLabel: "Approve the plan",
    action: "approve_plan",
    glossary: [
      { term: "Approval", definition: "A deliberate decision that the written plan may be acted on." },
    ],
    transitionStages: ["Approval"],
    nextWorkspacePath: "/workspaces/plan-review",
  },
  {
    stepIndex: 3,
    totalSteps: TOTAL,
    workspacePath: "/workspaces/plan-review",
    title: "Record A Theoretical Action",
    explanation:
      "No broker connection is needed. Guided mode records a theoretical execution and open position.",
    actionLabel: "Record theoretical execution",
    action: "record_execution",
    glossary: [
      { term: "Execution", definition: "A record that the plan was acted on." },
      { term: "Position", definition: "The period after entry while the idea is monitored." },
    ],
    transitionStages: ["Execution", "Position"],
    nextWorkspacePath: "/workspaces/active-position",
  },
  {
    stepIndex: 4,
    totalSteps: TOTAL,
    workspacePath: "/workspaces/active-position",
    title: "Close The Loop With Review",
    explanation:
      "The example position is open. Now record what the decision process showed you.",
    actionLabel: "Complete the review",
    action: "complete_review",
    glossary: [
      { term: "Review", definition: "A written reflection on process quality and lessons learned." },
    ],
    transitionStages: ["Review"],
    nextWorkspacePath: "/workspaces/review",
  },
  {
    stepIndex: 5,
    totalSteps: TOTAL,
    workspacePath: "/workspaces/review",
    title: "Inspect The Replay",
    explanation:
      "The lifecycle is complete. Replay shows the recorded path from idea through review.",
    actionLabel: "Open replay",
    action: "none",
    glossary: [
      { term: "Replay", definition: "A reconstruction of the decision from recorded events." },
    ],
    transitionStages: [],
    nextWorkspacePath: "/workspaces/replay",
  },
  {
    stepIndex: 6,
    totalSteps: TOTAL,
    workspacePath: "/workspaces/replay",
    title: "First Decision Complete",
    explanation:
      "You completed one guided lifecycle: idea, thesis, plan, approval, execution, position, review, and replay.",
    actionLabel: "Finish Walkthrough",
    action: "none",
    glossary: [],
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
    // localStorage can fail in private browsing or locked-down environments.
  }
}

export function clearWalkthroughSession(): void {
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch {
    // localStorage can fail in private browsing or locked-down environments.
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
    capture_mode: "quick_capture",
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
  if (step.action === "develop_thesis") {
    await postDevelopThesis({
      decision_id: session.decision_id,
      symbol: session.symbol,
      narrative: WALKTHROUGH_THESIS,
      catalysts: ["Breakout attempt", "Constructive relative strength"],
      assumptions: ["Market conditions remain supportive"],
      invalidation_conditions: [
        "Close back below the breakout level",
        "Volume fails to confirm demand",
      ],
      confidence_level: 3,
      regime_alignment: "Guided example, not a recommendation.",
      persona_id: session.persona_id,
      workspace_id: session.workspace_id,
    });
    return;
  }

  if (step.action === "create_plan") {
    await postCreatePlan({
      decision_id: session.decision_id,
      symbol: session.symbol,
      ...WALKTHROUGH_PLAN,
      persona_id: session.persona_id,
      workspace_id: session.workspace_id,
    });
    return;
  }

  if (step.action === "complete_review") {
    await postCompleteReview({
      decision_id: session.decision_id,
      symbol: session.symbol,
      ...WALKTHROUGH_REVIEW,
      persona_id: session.persona_id,
      workspace_id: session.workspace_id,
    });
    return;
  }

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
    provenance: { actor: "walkthrough", source: "guided-first-decision" },
  };

  for (const stageName of step.transitionStages) {
    await postLifecycleTransition({
      ...base,
      requested_stage: stageName,
      payload: { source: "guided-first-decision" },
    });
  }
}
