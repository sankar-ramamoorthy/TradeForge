import { useEffect, useState } from "react";
import {
  fetchScenarioBranches,
  fetchThesisArtifact,
  fetchPlanArtifact,
  type ScenarioBranch,
  type ThesisArtifact,
  type TradePlanArtifact,
} from "../api/runtime";

const CONFIDENCE_LABELS: Record<number, string> = {
  1: "Speculative", 2: "Low", 3: "Moderate", 4: "High", 5: "Conviction",
};

const BRANCH_TYPE_LABELS: Record<string, string> = {
  primary: "Primary",
  alternative: "Alternative",
  invalidation: "Invalidation",
  regime_transition: "Regime Transition",
};

function truncate(text: string, max: number): string {
  return text.length > max ? text.slice(0, max) + "…" : text;
}

function ThesisSummary({ thesis }: { thesis: ThesisArtifact }) {
  const isRevised = thesis.source_event_type === "decision.thesis_revised";
  return (
    <div className="continuity-section">
      <p className="thesis-context-label">
        Original Thesis
        {isRevised ? <span className="cognitive-revised-indicator"> — Revised</span> : null}
      </p>
      <p className="continuity-narrative" title={thesis.narrative}>
        {truncate(thesis.narrative, 200)}
      </p>
      <div className="continuity-meta">
        <span className="cognitive-conviction-badge">
          {CONFIDENCE_LABELS[thesis.confidence_level] ?? thesis.confidence_level}
          {" "}({thesis.confidence_level}/5)
        </span>
        {thesis.regime_alignment ? (
          <span className="cognitive-regime-badge">{thesis.regime_alignment}</span>
        ) : null}
        <span className="continuity-invalidation-hint">
          {thesis.invalidation_conditions.length} invalidation condition
          {thesis.invalidation_conditions.length !== 1 ? "s" : ""}
        </span>
      </div>
      {thesis.invalidation_conditions.length > 0 ? (
        <div className="continuity-invalidation-list">
          <p className="thesis-context-label">Watch for (invalidation):</p>
          <ul className="thesis-context-list">
            {thesis.invalidation_conditions.map((c) => (
              <li key={c}>{c}</li>
            ))}
          </ul>
        </div>
      ) : null}
    </div>
  );
}

function PlanSummary({ plan }: { plan: TradePlanArtifact }) {
  return (
    <div className="continuity-section">
      <p className="thesis-context-label">
        Plan Reference
        {plan.playbook_alignment ? (
          <span className="cognitive-playbook-badge"> {plan.playbook_alignment}</span>
        ) : null}
      </p>
      <div className="continuity-plan-levels">
        <div className="continuity-level">
          <span className="cognitive-field-label">Entry: </span>
          <span title={plan.entry_rationale}>{truncate(plan.entry_rationale, 100)}</span>
        </div>
        <div className="continuity-level">
          <span className="cognitive-field-label">Stop: </span>
          <span title={plan.stop_rationale}>{truncate(plan.stop_rationale, 100)}</span>
        </div>
        <div className="continuity-level">
          <span className="cognitive-field-label">Target: </span>
          <span title={plan.target_rationale}>{truncate(plan.target_rationale, 100)}</span>
        </div>
      </div>
    </div>
  );
}

function ScenarioSummary({ branches }: { branches: ScenarioBranch[] }) {
  if (branches.length === 0) return null;

  const invalidation = branches.filter((b) => b.branch_type === "invalidation");
  const primary = branches.filter((b) => b.branch_type === "primary");

  const counts = branches.reduce<Record<string, number>>((acc, b) => {
    acc[b.branch_type] = (acc[b.branch_type] ?? 0) + 1;
    return acc;
  }, {});

  return (
    <div className="continuity-section">
      <p className="thesis-context-label">
        Scenario Branches ({branches.length})
        <span className="continuity-meta">
          {" "}{Object.entries(counts).map(([t, n]) =>
            `${n} ${BRANCH_TYPE_LABELS[t] ?? t}`
          ).join(" · ")}
        </span>
      </p>
      {invalidation.length > 0 ? (
        <div className="continuity-invalidation-list">
          <p className="thesis-context-label">Invalidation scenarios:</p>
          {invalidation.map((b, i) => (
            <p key={i} className="continuity-branch-item">
              <span className="cognitive-field-label">If: </span>
              {truncate(b.condition, 100)}
              <span className="cognitive-field-label"> → </span>
              {truncate(b.implication, 80)}
            </p>
          ))}
        </div>
      ) : null}
      {primary.length > 0 && invalidation.length === 0 ? (
        <div>
          {primary.slice(0, 1).map((b, i) => (
            <p key={i} className="continuity-branch-item">
              <span className={`cognitive-branch-type-badge branch-${b.branch_type}`}>
                Primary
              </span>
              {" "}{truncate(b.condition, 100)}
            </p>
          ))}
        </div>
      ) : null}
    </div>
  );
}

type Props = {
  decisionId: string;
  label?: string;
};

type CognitionState = {
  thesis: ThesisArtifact | null;
  plan: TradePlanArtifact | null;
  branches: ScenarioBranch[];
};

export function CognitiveContinuityPanel({ decisionId, label }: Props) {
  const [cognition, setCognition] = useState<CognitionState | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    const signal = controller.signal;

    Promise.all([
      fetchThesisArtifact(decisionId, signal).catch(() => null),
      fetchPlanArtifact(decisionId, signal).catch(() => null),
      fetchScenarioBranches(decisionId, signal)
        .then((list) => list.branches)
        .catch(() => [] as ScenarioBranch[]),
    ]).then(([thesis, plan, branches]) => {
      if (!signal.aborted) {
        setCognition({ thesis, plan, branches });
      }
    });

    return () => controller.abort();
  }, [decisionId]);

  if (!cognition) return null;
  if (!cognition.thesis && !cognition.plan && cognition.branches.length === 0) {
    return null;
  }

  return (
    <div
      className="cognitive-continuity-panel"
      aria-label={label ?? "Decision context"}
    >
      <p className="eyebrow">{label ?? "Decision Cognitive Context"}</p>

      {cognition.thesis ? (
        <ThesisSummary thesis={cognition.thesis} />
      ) : null}

      {cognition.plan ? (
        <PlanSummary plan={cognition.plan} />
      ) : null}

      <ScenarioSummary branches={cognition.branches} />

      <p className="cognitive-snapshot-authority">
        Derived from event payloads — not canonical truth.
      </p>
    </div>
  );
}
