import { ClipboardCheck } from "lucide-react";
import { LifecycleProgressStrip, WorkflowGuidanceNote } from "./LifecycleProgress";
import { type MouseEvent, useCallback, useEffect, useRef, useState } from "react";

import {
  fetchWorkspaceProjection,
  postLifecycleTransition,
  type WorkspaceApiParams,
  type WorkspaceProjection,
} from "../api/runtime";
import { type WorkspaceContext } from "../workspaceRouting";

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
};

export function PlanReviewWorkspace({ context }: PlanReviewWorkspaceProps) {
  const [projection, setProjection] = useState<WorkspaceProjection | null>(null);
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
        })
        .catch((err: unknown) => {
          if (err instanceof DOMException && err.name === "AbortError") return;
          setLoadError(
            err instanceof Error ? err.message : "Failed to load plan review workspace",
          );
        });
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
  const canRecordExecution = lifecycleStage === "Approval";

  function makeTransitionHandler(requestedStage: string) {
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
          const controller = new AbortController();
          fetchControllerRef.current = controller;
          loadProjection(controller.signal);
        })
        .catch((err: unknown) => {
          setTransitionState("error");
          setTransitionError(
            err instanceof Error ? err.message : "Lifecycle transition failed",
          );
        });
    };
  }

  const handleCreatePlan = makeTransitionHandler("Plan");
  const handleAuthorizePlan = makeTransitionHandler("Approval");
  const handleRecordExecution = makeTransitionHandler("Execution");

  const fieldOrder = ["plan_references", "risk_review", "rule_evaluation"];

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

          {canCreatePlan ? (
            <div className="lifecycle-action-surface">
              <p className="eyebrow">Available Lifecycle Action</p>
              <p className="lifecycle-action-note">
                The thesis is ready for a plan. Creating a plan records the
                structured intent before approval. The lifecycle service validates
                the transition before appending an event.
              </p>
              {transitionError ? (
                <div className="runtime-error">{transitionError}</div>
              ) : null}
              <button
                className="lifecycle-action-btn"
                disabled={transitionState === "transitioning"}
                onClick={handleCreatePlan}
                type="button"
              >
                {transitionState === "transitioning"
                  ? "Requesting transition…"
                  : "Create Plan"}
              </button>
            </div>
          ) : canAuthorizePlan ? (
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
          ) : canRecordExecution ? (
            <div className="lifecycle-action-surface">
              <p className="eyebrow">Available Lifecycle Action</p>
              <p className="lifecycle-action-note">
                The plan is approved. Recording execution acknowledges that the
                order workflow has been initiated. This is a manual record for
                MVP — live broker sync is out of scope.
              </p>
              {transitionError ? (
                <div className="runtime-error">{transitionError}</div>
              ) : null}
              <button
                className="lifecycle-action-btn"
                disabled={transitionState === "transitioning"}
                onClick={handleRecordExecution}
                type="button"
              >
                {transitionState === "transitioning"
                  ? "Requesting transition…"
                  : "Record Execution"}
              </button>
            </div>
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
