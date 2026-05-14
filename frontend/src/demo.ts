import {
  initNewTradeIdea,
  postLifecycleTransition,
} from "./api/runtime";
import { setActiveDecision, type ActiveDecisionRecord } from "./activeDecision";

export type DemoScenario = {
  id: string;
  symbol: string;
  name: string;
  description: string;
  targetStage: "Plan" | "Approval" | "Position" | "Review";
  landingPath: string;
  initial_thesis: string;
  plan_notes: string;
  approval_notes?: string;
  execution_notes?: string;
  position_notes?: string;
  review_notes?: string;
};

export const DEMO_SCENARIOS: DemoScenario[] = [
  {
    id: "aapl-breakout",
    symbol: "AAPL",
    name: "Breakout Swing Trade",
    description:
      "Momentum breakout above the 200-day MA on above-average volume. " +
      "Experience the plan authorization workflow — thesis capture, risk review, and approval.",
    targetStage: "Plan",
    landingPath: "/workspaces/plan-review",
    initial_thesis:
      "Breakout above the 200-day moving average on above-average volume. " +
      "Technology sector momentum remains intact with strong institutional " +
      "participation. Clear entry at current levels with defined risk below " +
      "recent consolidation lows.",
    plan_notes:
      "Entry on confirmed breakout close. Position sized at 2% portfolio risk. " +
      "Stop loss 3% below entry. Primary target at prior all-time high resistance. " +
      "Secondary target at 10% extension. Review thesis drift weekly.",
  },
  {
    id: "tsla-complete",
    symbol: "TSLA",
    name: "Completed Lifecycle Review",
    description:
      "A fully closed trade — from thesis through execution to disciplined review. " +
      "Explore the Replay Workspace to reconstruct the complete 7-stage decision history.",
    targetStage: "Review",
    landingPath: "/workspaces/replay",
    initial_thesis:
      "EV sector rotational opportunity following earnings miss. " +
      "Oversold technical condition with clear catalyst for mean reversion. " +
      "Risk/reward favors a long position at key support with defined downside.",
    plan_notes:
      "Entry at support level with 1.5% portfolio risk. " +
      "Stop below recent swing low. Primary target at 50% retracement of decline. " +
      "Momentum confirmation required before full position entry.",
    approval_notes: "Approved at support test. Full position allocation authorized.",
    execution_notes:
      "Filled at target entry across two sessions. Partial fill on day one.",
    position_notes:
      "Position held for 12 days. Thesis intact at mid-hold review.",
    review_notes:
      "Trade closed at primary target. Process adherence strong — entry, stop, and " +
      "target all honored per plan. Thesis resolved as expected. " +
      "Improvement area: quicker partial scaling as target approached.",
  },
  {
    id: "nvda-position",
    symbol: "NVDA",
    name: "Active Position Management",
    description:
      "A live position in the AI infrastructure theme. The trade is in the position " +
      "management phase — monitor thesis integrity and prepare for disciplined review.",
    targetStage: "Position",
    landingPath: "/workspaces/active-position",
    initial_thesis:
      "AI infrastructure demand driving sustained earnings outperformance. " +
      "Data center GPU cycle remains early-stage with strong forward guidance. " +
      "Sector leadership intact despite broader market volatility.",
    plan_notes:
      "Long-duration position with 3% portfolio allocation. " +
      "Stop at key technical support. Review trigger on any guidance revision. " +
      "Primary target at prior resistance zone.",
    approval_notes: "Approved on fundamental and technical confirmation.",
    execution_notes: "Staged entry over 3 sessions at target zone.",
    position_notes:
      "Position in active management — thesis intact after quarterly earnings beat.",
  },
  {
    id: "spy-exit",
    symbol: "SPY",
    name: "Disciplined Exit Review",
    description:
      "A regime-transition index trade that has completed review. Explore how the " +
      "system separates decision process quality from outcome in the review workflow.",
    targetStage: "Review",
    landingPath: "/workspaces/review",
    initial_thesis:
      "Broad market regime transition from risk-off to neutral. " +
      "Index rebalancing opportunity at key support with defined risk-reward. " +
      "Macro environment improving with declining volatility signal.",
    plan_notes:
      "Index exposure with 2% portfolio allocation. Entry at tested support. " +
      "Hard stop below consolidation zone. Exit on regime deterioration signal.",
    approval_notes: "Approved after regime signal confirmation.",
    execution_notes: "Filled at target. Full index position active.",
    position_notes:
      "Position held through volatility event. Regime shifted mid-hold.",
    review_notes:
      "Exited below original target due to regime deterioration signal. " +
      "Decision process sound — thesis shifted and exit rule applied correctly. " +
      "Outcome: small loss. Process quality: high. Exit discipline worked as designed.",
  },
];

export type DemoFlowResult = {
  decisionId: string;
  symbol: string;
  record: ActiveDecisionRecord;
};

export async function runDemoFlow(
  scenario: DemoScenario,
  options: {
    personaId: string;
    personaVersion: string;
    workspaceId: string;
  },
): Promise<DemoFlowResult> {
  const { personaId, personaVersion, workspaceId } = options;

  const init = await initNewTradeIdea({
    symbol: scenario.symbol,
    initial_thesis: scenario.initial_thesis,
    persona_id: personaId,
    workspace_id: workspaceId,
  });

  const decisionRef = [
    { entity_type: "decision", entity_id: init.decision_id },
    { entity_type: "ticker", entity_id: init.symbol },
  ];

  const base = {
    timestamp: new Date().toISOString(),
    persona_id: personaId,
    workspace_id: workspaceId,
    entity_references: decisionRef,
    provenance: { actor: "demo", source: "guided-demo-mode" },
  };

  await postLifecycleTransition({
    ...base,
    requested_stage: "Thesis",
    payload: { thesis: scenario.initial_thesis },
  });

  await postLifecycleTransition({
    ...base,
    requested_stage: "Plan",
    payload: { plan: scenario.plan_notes },
  });

  const needsApproval =
    scenario.targetStage === "Approval" ||
    scenario.targetStage === "Position" ||
    scenario.targetStage === "Review";

  if (needsApproval) {
    await postLifecycleTransition({
      ...base,
      requested_stage: "Approval",
      payload: { notes: scenario.approval_notes ?? "Approved." },
    });
  }

  const needsPosition =
    scenario.targetStage === "Position" || scenario.targetStage === "Review";

  if (needsPosition) {
    await postLifecycleTransition({
      ...base,
      requested_stage: "Execution",
      payload: { notes: scenario.execution_notes ?? "Executed." },
    });

    await postLifecycleTransition({
      ...base,
      requested_stage: "Position",
      payload: { notes: scenario.position_notes ?? "Position active." },
    });
  }

  if (scenario.targetStage === "Review") {
    await postLifecycleTransition({
      ...base,
      requested_stage: "Review",
      payload: { review: scenario.review_notes ?? "Review complete." },
    });
  }

  const record: ActiveDecisionRecord = {
    decision_id: init.decision_id,
    symbol: init.symbol,
    persona_id: personaId,
    persona_version: personaVersion,
    created_at: init.timestamp,
    is_demo: true,
    scenario_name: scenario.name,
  };

  setActiveDecision(record);

  return { decisionId: init.decision_id, symbol: init.symbol, record };
}
