import {
  initNewTradeIdea,
  postLifecycleTransition,
} from "./api/runtime";
import { setActiveDecision, type ActiveDecisionRecord } from "./activeDecision";

export const DEMO_SEED = {
  symbol: "AAPL",
  initial_thesis:
    "Breakout above the 200-day moving average on above-average volume. " +
    "Technology sector momentum remains intact with strong institutional " +
    "participation. Clear entry at current levels with defined risk below " +
    "recent consolidation lows.",
  plan_notes:
    "Entry on confirmed breakout close. Position sized at 2% portfolio risk. " +
    "Stop loss 3% below entry. Primary target at prior all-time high resistance. " +
    "Secondary target at 10% extension. Review thesis drift weekly.",
} as const;

export type DemoFlowResult = {
  decisionId: string;
  symbol: string;
  record: ActiveDecisionRecord;
};

export async function runDemoFlow(options: {
  personaId: string;
  personaVersion: string;
  workspaceId: string;
}): Promise<DemoFlowResult> {
  const { personaId, personaVersion, workspaceId } = options;

  const init = await initNewTradeIdea({
    symbol: DEMO_SEED.symbol,
    initial_thesis: DEMO_SEED.initial_thesis,
    persona_id: personaId,
    workspace_id: workspaceId,
  });

  const decisionRef = [
    { entity_type: "decision", entity_id: init.decision_id },
    { entity_type: "ticker", entity_id: init.symbol },
  ];

  await postLifecycleTransition({
    requested_stage: "Thesis",
    timestamp: new Date().toISOString(),
    persona_id: personaId,
    workspace_id: workspaceId,
    entity_references: decisionRef,
    payload: { thesis: DEMO_SEED.initial_thesis },
    provenance: { actor: "demo", source: "guided-demo-mode" },
  });

  await postLifecycleTransition({
    requested_stage: "Plan",
    timestamp: new Date().toISOString(),
    persona_id: personaId,
    workspace_id: workspaceId,
    entity_references: decisionRef,
    payload: { plan: DEMO_SEED.plan_notes },
    provenance: { actor: "demo", source: "guided-demo-mode" },
  });

  const record: ActiveDecisionRecord = {
    decision_id: init.decision_id,
    symbol: init.symbol,
    persona_id: personaId,
    persona_version: personaVersion,
    created_at: init.timestamp,
    is_demo: true,
  };

  setActiveDecision(record);

  return { decisionId: init.decision_id, symbol: init.symbol, record };
}
