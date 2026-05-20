import { ClipboardCheck } from "lucide-react";
import { LifecycleProgressStrip, WorkflowGuidanceNote } from "./LifecycleProgress";
import { type MouseEvent, useCallback, useEffect, useRef, useState } from "react";

import {
  fetchWorkspaceProjection,
  fetchThesisArtifact,
  fetchPlanArtifact,
  fetchPlanReadiness,
  postLifecycleTransition,
  type PlanReadiness,
  type ThesisArtifact,
  type TradePlanArtifact,
  type WorkspaceApiParams,
  type WorkspaceProjection,
} from "../api/runtime";
import { type WorkspaceContext } from "../workspaceRouting";
import { ThesisRevisionModal } from "./ThesisRevisionModal";
import { PlanRevisionModal } from "./PlanRevisionModal";
import { PlanDevelopmentModal } from "./PlanDevelopmentModal";
import { ArmPlanModal } from "./ArmPlanModal";
import { PlanReadinessPanel } from "./PlanReadinessPanel";
import { AdvisoryInterpretationPanel } from "./AdvisoryInterpretationPanel";

type TransitionState = "idle" | "transitioning" | "error";

const AUTHORITY_LABELS: Record<string, string> = {
  canonical: "Canonical",
  derived: "Derived",
  inferred: "Inferred",
  advisory: "Advisory",
};

const AUTHORITY_DESCRIPTIONS: Record<string, string> = {
  canonical: "Event-backed facts from the ledger.",
  derived: "Computed from source events and rules.",
  inferred: "Interpreted from derived state.",
  advisory: "Non-authoritative contextual notes.",
};

function FieldSurface({
  name,
  authority,
  sourceEventCount,
  sourceEventTypes,
}: {
  name: string;
  authority: string;
  sourceEventCount: number;
  sourceEventTypes: string[];
}) {
  const label = AUTHORITY_LABELS[authority] ?? authority;
  const desc = AUTHORITY_DESCRIPTIONS[authority] ?? "";
  const hasData = sourceEventCount > 0;

  return (
    <div
      className="field-surface"
      data-authority={authority}
      aria-label={`${name} — ${label}`}
    >
      <div className="field-surface-header">
        <span className="field-surface-name">
          {name.replace(/_/g, " ")}
        </span>
        <span className={`field-authority-badge authority-${authority}`}>
          {label}
        </span>
      </div>
      <p className="field-surface-desc">{desc}</p>
      {hasData ? (
        <div className="field-source-events">
          <span className="eyebrow">
            {sourceEventCount} source event{sourceEventCount !== 1 ? "s" : ""}
          </span>
          <div className="source-event-types">
            {sourceEventTypes.map((t) => (
              <code className="event-type-tag" key={t}>{t}</code>
            ))}
          </div>
        </div>
      ) : (
        <p className="field-no-data">No source events yet.</p>
      )}
    </div>
  );
}

type PlanReviewWorkspaceProps = {
  context: Required<WorkspaceContext>;
  onNavigate: (event: MouseEvent<HTMLAnchorElement>, href: string) => void;
  onNavigateProgrammatic?: (href: string) => void;
  onStageLoaded?: (stage: string | null) => void;
};

function ThesisContextPanel({
  thesis,
  onRevise,
  canRevise,
}: {
  thesis: ThesisArtifact;
  onRevise?: () => void;
  canRevise?: boolean;
}) {
  const CONFIDENCE_LABELS: Record<number, string> = {
    1: "Speculative", 2: "Low", 3: "Moderate", 4: "High", 5: "Conviction",
  };
  const isRevised = thesis.source_event_type === "decision.thesis_revised";
  return (
    <div className="thesis-context-panel" aria-label="Thesis foundation">
      <div className="thesis-context-header">
        <p className="eyebrow">
          Thesis Foundation
          {isRevised ? <span className="thesis-revision-badge"> — Revised</span> : null}
        </p>
        {canRevise && onRevise ? (
          <button
            className="thesis-revise-btn"
            onClick={onRevise}
            type="button"
          >
            Revise Thesis
          </button>
        ) : null}
      </div>
      <p className="thesis-context-narrative">{thesis.narrative}</p>
      {thesis.regime_alignment ? (
        <p className="thesis-context-regime">
          <span className="thesis-context-label">Regime:</span> {thesis.regime_alignment}
        </p>
      ) : null}
      <p className="thesis-context-conviction">
        Conviction: {CONFIDENCE_LABELS[thesis.confidence_level] ?? thesis.confidence_level} ({thesis.confidence_level}/5)
      </p>
      <div className="thesis-context-lists">
        <div className="thesis-context-list-group">
          <p className="thesis-context-label">Catalysts</p>
          <ul className="thesis-context-list">
            {thesis.catalysts.map((c) => <li key={c}>{c}</li>)}
          </ul>
        </div>
        <div className="thesis-context-list-group">
          <p className="thesis-context-label">Invalidation Conditions</p>
          <ul className="thesis-context-list">
            {thesis.invalidation_conditions.map((i) => <li key={i}>{i}</li>)}
          </ul>
        </div>
      </div>
    </div>
  );
}

function PlanContextPanel({
  plan,
  canRevise,
  onRevise,
}: {
  plan: TradePlanArtifact;
  canRevise?: boolean;
  onRevise?: () => void;
}) {
  const isRevised = plan.source_event_type === "decision.plan_revised";
  return (
    <div className="thesis-context-panel" aria-label="Trade plan">
      <div className="thesis-context-header">
        <p className="eyebrow">
          Trade Plan
          {isRevised ? <span className="thesis-revision-badge"> — Revised</span> : null}
        </p>
        {canRevise && onRevise ? (
          <button
            className="thesis-revise-btn"
            onClick={onRevise}
            type="button"
          >
            Revise Plan
          </button>
        ) : null}
      </div>
      <div className="plan-rationale-grid">
        <div className="plan-rationale-item">
          <p className="thesis-context-label">Entry</p>
          <p className="plan-rationale-text">{plan.entry_rationale}</p>
        </div>
        <div className="plan-rationale-item">
          <p className="thesis-context-label">Stop</p>
          <p className="plan-rationale-text">{plan.stop_rationale}</p>
        </div>
        <div className="plan-rationale-item">
          <p className="thesis-context-label">Target</p>
          <p className="plan-rationale-text">{plan.target_rationale}</p>
        </div>
        <div className="plan-rationale-item">
          <p className="thesis-context-label">Sizing</p>
          <p className="plan-rationale-text">{plan.sizing_rationale}</p>
        </div>
      </div>
      {plan.execution_assumptions.length > 0 ? (
        <div className="thesis-context-list-group">
          <p className="thesis-context-label">Execution Assumptions</p>
          <ul className="thesis-context-list">
            {plan.execution_assumptions.map((a) => <li key={a}>{a}</li>)}
          </ul>
        </div>
      ) : null}
      {plan.playbook_alignment ? (
        <p className="thesis-context-regime">
          <span className="thesis-context-label">Playbook:</span>{" "}
          {plan.playbook_alignment}
        </p>
      ) : null}
    </div>
  );
}

export function PlanReviewWorkspace({ context, onNavigateProgrammatic, onStageLoaded }: PlanReviewWorkspaceProps) {
  const [projection, setProjection] = useState<WorkspaceProjection | null>(null);
  const [thesis, setThesis] = useState<ThesisArtifact | null>(null);
  const [plan, setPlan] = useState<TradePlanArtifact | null>(null);
  const [readiness, setReadiness] = useState<PlanReadiness | null>(null);
  const [showRevisionModal, setShowRevisionModal] = useState(false);
  const [showPlanRevisionModal, setShowPlanRevisionModal] = useState(false);
  const [showPlanModal, setShowPlanModal] = useState(false);
  const [showArmPlanModal, setShowArmPlanModal] = useState(false);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [transitionState, setTransitionState] = useState<TransitionState>("idle");
  const [transitionError, setTransitionError] = useState<string | null>(null);
  const fetchControllerRef = useRef<AbortController | null>(null);

  const params: WorkspaceApiParams = {
    persona_id: context.persona_id,
    persona_version: context.persona_version,
    workspace_id: context.workspace_id,
    workflow_id: context.selected_workflow_id || undefined,
    decision_id: context.decision_id || undefined,
  };

  const loadProjection = useCallback(
    (signal: AbortSignal) => {
      fetchWorkspaceProjection("plan-review", params, signal)
        .then((data) => {
          setProjection(data);
          setLoadError(null);
          onStageLoaded?.(data.lifecycle_state?.current_stage ?? null);
        })
        .catch((err: unknown) => {
          if (err instanceof DOMException && err.name === "AbortError") return;
          setLoadError(
            err instanceof Error ? err.message : "Failed to load plan review workspace",
          );
        });

      if (context.decision_id) {
        fetchThesisArtifact(context.decision_id, signal)
          .then((artifact) => setThesis(artifact))
          .catch((err: unknown) => {
            if (err instanceof DOMException && err.name === "AbortError") return;
          });
        fetchPlanArtifact(context.decision_id, signal)
          .then((artifact) => setPlan(artifact))
          .catch((err: unknown) => {
            if (err instanceof DOMException && err.name === "AbortError") return;
          });
        fetchPlanReadiness(context.decision_id, signal)
          .then((r) => setReadiness(r))
          .catch((err: unknown) => {
            if (err instanceof DOMException && err.name === "AbortError") return;
          });
      }
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [
      context.persona_id,
      context.persona_version,
      context.workspace_id,
      context.selected_workflow_id,
      context.decision_id,
    ],
  );

  useEffect(() => {
    const controller = new AbortController();
    fetchControllerRef.current = controller;
    loadProjection(controller.signal);
    return () => controller.abort();
  }, [loadProjection]);

  const lifecycleStage = projection?.lifecycle_state?.current_stage ?? null;
  const canCreatePlan = lifecycleStage === "Thesis";
  const canAuthorizePlan = lifecycleStage === "Plan";
  const canArmPlan = lifecycleStage === "Approval";

  function makeTransitionHandler(requestedStage: string, nextHref?: string) {
    return function () {
      setTransitionState("transitioning");
      setTransitionError(null);

      postLifecycleTransition({
        requested_stage: requestedStage,
        timestamp: new Date().toISOString(),
        persona_id: context.persona_id,
        workspace_id: context.workspace_id,
        entity_references: context.decision_id
          ? [{ entity_type: "decision", entity_id: context.decision_id }]
          : [],
        payload: {},
        provenance: { actor: "human", source: "plan-review-workspace" },
      })
        .then(() => {
          setTransitionState("idle");
          if (nextHref) {
            onNavigateProgrammatic?.(nextHref);
          } else {
            const controller = new AbortController();
            fetchControllerRef.current = controller;
            loadProjection(controller.signal);
          }
        })
        .catch((err: unknown) => {
          setTransitionState("error");
          setTransitionError(
            err instanceof Error ? err.message : "Lifecycle transition failed",
          );
        });
    };
  }

  const handleCreatePlan = () => setShowPlanModal(true);
  const handleAuthorizePlan = makeTransitionHandler("Approval");
  const armPlanSuccessHref =
    "/workspaces/active-position" +
    (context.decision_id
      ? `?decision_id=${encodeURIComponent(context.decision_id)}`
      : "");

  const fieldOrder = ["thesis_content", "plan_references", "risk_review", "rule_evaluation"];

  return (
    <section
      className="workspace-surface"
      aria-labelledby="plan-review-workspace-title"
    >
      <div className="surface-title">
        <ClipboardCheck aria-hidden="true" />
        <div>
          <p className="eyebrow">Plan Review Workspace</p>
          <h1 id="plan-review-workspace-title">
            What risk is being intentionally authorized?
          </h1>
        </div>
      </div>

      {loadError ? (
        <div className="runtime-error">{loadError}</div>
      ) : null}

      <LifecycleProgressStrip currentStage={lifecycleStage} />
      <WorkflowGuidanceNote currentStage={lifecycleStage} />

      {projection !== null ? (
        <>
          <div className="field-surfaces-grid">
            {fieldOrder.map((name) => {
              const field = projection.fields[name];
              if (!field) return null;
              return (
                <FieldSurface
                  authority={field.authority}
                  key={name}
                  name={name}
                  sourceEventCount={field.source_event_count}
                  sourceEventTypes={field.source_event_types}
                />
              );
            })}
          </div>

          {thesis && showRevisionModal ? (
            <ThesisRevisionModal
              context={context}
              currentThesis={thesis}
              onCancel={() => setShowRevisionModal(false)}
              onSuccess={() => {
                setShowRevisionModal(false);
                if (context.decision_id) {
                  fetchThesisArtifact(context.decision_id).then(setThesis).catch(() => {});
                }
              }}
              symbol={thesis.symbol}
            />
          ) : null}

          {thesis ? (
            <ThesisContextPanel
              canRevise={lifecycleStage === "Thesis" || lifecycleStage === "Plan"}
              onRevise={() => setShowRevisionModal(true)}
              thesis={thesis}
            />
          ) : null}

          {plan && showPlanRevisionModal ? (
            <PlanRevisionModal
              context={context}
              currentPlan={plan}
              onCancel={() => setShowPlanRevisionModal(false)}
              onSuccess={() => {
                setShowPlanRevisionModal(false);
                if (context.decision_id) {
                  fetchPlanArtifact(context.decision_id).then(setPlan).catch(() => {});
                }
              }}
              symbol={plan.symbol}
            />
          ) : null}

          {plan ? (
            <PlanContextPanel
              canRevise={lifecycleStage === "Plan"}
              onRevise={() => setShowPlanRevisionModal(true)}
              plan={plan}
            />
          ) : null}

          <AdvisoryInterpretationPanel
            context={context}
            title="Evidence influence and caveats"
          />

          {showPlanModal && context.decision_id ? (
            <PlanDevelopmentModal
              context={context}
              onCancel={() => setShowPlanModal(false)}
              onSuccess={() => {
                setShowPlanModal(false);
                const controller = new AbortController();
                fetchControllerRef.current = controller;
                loadProjection(controller.signal);
                if (context.decision_id) {
                  fetchPlanArtifact(context.decision_id).then(setPlan).catch(() => {});
                }
              }}
              symbol={thesis?.symbol ?? plan?.symbol ?? ""}
            />
          ) : null}

          {canCreatePlan ? (
            <div className="lifecycle-action-surface">
              <p className="eyebrow">Available Lifecycle Action</p>
              <p className="lifecycle-action-note">
                The thesis is ready for a plan. Define your structured execution intent —
                entry, stop, target, and sizing rationale become replayable cognitive artifacts.
              </p>
              <button
                className="lifecycle-action-btn"
                onClick={handleCreatePlan}
                type="button"
              >
                Create Plan
              </button>
            </div>
          ) : canAuthorizePlan ? (
            <>
              {readiness ? <PlanReadinessPanel readiness={readiness} /> : null}
              <div className="lifecycle-action-surface">
                <p className="eyebrow">Available Lifecycle Action</p>
                <p className="lifecycle-action-note">
                  Authorizing a plan confirms deliberate risk acceptance. The lifecycle
                  service validates the transition before appending an event — this is
                  not trade execution.
                </p>
                {transitionError ? (
                  <div className="runtime-error">{transitionError}</div>
                ) : null}
                <button
                  className="lifecycle-action-btn"
                  disabled={transitionState === "transitioning"}
                  onClick={handleAuthorizePlan}
                  type="button"
                >
                  {transitionState === "transitioning"
                    ? "Requesting transition…"
                    : "Authorize Plan"}
                </button>
              </div>
            </>
          ) : canArmPlan ? (
            <>
              {showArmPlanModal && context.decision_id ? (
                <ArmPlanModal
                  context={context}
                  onCancel={() => setShowArmPlanModal(false)}
                  onSuccess={() => {
                    setShowArmPlanModal(false);
                    onNavigateProgrammatic?.(armPlanSuccessHref);
                  }}
                  symbol={plan?.symbol ?? thesis?.symbol ?? ""}
                />
              ) : null}
              <div className="lifecycle-action-surface">
                <p className="eyebrow">Available Lifecycle Action</p>
                <p className="lifecycle-action-note">
                  The plan is authorized. Declare the trigger conditions that must
                  be met before the order is placed — this arms the plan and moves
                  it into active supervision.
                </p>
                <button
                  className="lifecycle-action-btn"
                  onClick={() => setShowArmPlanModal(true)}
                  type="button"
                >
                  Arm Plan
                </button>
              </div>
            </>
          ) : null}

          <div
            className="attention-authority-note"
            aria-label="Authority boundaries"
          >
            {projection.authority_boundaries.map((boundary) => (
              <p className="authority-boundary" key={boundary}>
                {boundary}
              </p>
            ))}
          </div>

          <div className="projection-metadata">
            <span className="eyebrow">Projection Basis</span>
            <p className="projection-detail">
              {projection.authority} — {projection.source_event_count} source events
            </p>
          </div>
        </>
      ) : null}
    </section>
  );
}
