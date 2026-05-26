import { CheckCircle, Compass } from "lucide-react";
import { type MouseEvent, useCallback, useEffect, useRef, useState } from "react";
import { LifecycleProgressStrip, WorkflowGuidanceNote } from "./LifecycleProgress";

import {
  fetchWorkspaceProjection,
  fetchThesisArtifact,
  fetchPlanArtifact,
  fetchReviewReflection,
  fetchBehavioralClusters,
  fetchBehavioralSignals,
  fetchDecisionQualityMetrics,
  fetchEmotionalReflections,
  fetchRecurringMistakes,
  type BehavioralClusterList,
  type BehavioralSignalList,
  type DecisionQualityMetrics,
  type EmotionalReflectionList,
  type RecurringMistakeList,
  type ReviewReflectionArtifact,
  type ThesisArtifact,
  type TradePlanArtifact,
  type WorkspaceApiParams,
  type WorkspaceProjection,
} from "../api/runtime";
import { type WorkspaceContext } from "../workspaceRouting";
import { ReviewReflectionModal } from "./ReviewReflectionModal";

type TransitionState = "idle" | "open-review-modal" | "error";

const QUALITY_LABELS: Record<number, string> = {
  1: "Poor", 2: "Below average", 3: "Adequate", 4: "Good", 5: "Excellent",
};

const AUTHORITY_LABELS: Record<string, string> = {
  canonical: "Canonical", derived: "Derived",
  inferred: "Inferred", advisory: "Advisory",
};

const AUTHORITY_DESCRIPTIONS: Record<string, string> = {
  canonical: "Event-backed facts from the ledger.",
  derived: "Computed from source events and rules.",
  inferred: "Interpreted from derived state.",
  advisory: "Non-authoritative contextual notes.",
};

function FieldSurface({
  name, authority, sourceEventCount, sourceEventTypes,
}: {
  name: string; authority: string; sourceEventCount: number; sourceEventTypes: string[];
}) {
  const label = AUTHORITY_LABELS[authority] ?? authority;
  const desc = AUTHORITY_DESCRIPTIONS[authority] ?? "";
  return (
    <div className="field-surface" data-authority={authority} aria-label={`${name} — ${label}`}>
      <div className="field-surface-header">
        <span className="field-surface-name">{name.replace(/_/g, " ")}</span>
        <span className={`field-authority-badge authority-${authority}`}>{label}</span>
      </div>
      <p className="field-surface-desc">{desc}</p>
      {sourceEventCount > 0 ? (
        <div className="field-source-events">
          <span className="eyebrow">
            {sourceEventCount} source event{sourceEventCount !== 1 ? "s" : ""}
          </span>
          <div className="source-event-types">
            {sourceEventTypes.map((t) => <code className="event-type-tag" key={t}>{t}</code>)}
          </div>
        </div>
      ) : (
        <p className="field-no-data">No source events yet.</p>
      )}
    </div>
  );
}

function truncate(text: string, max: number): string {
  return text.length > max ? text.slice(0, max) + "…" : text;
}

function ReviewFoundationPanel({
  thesis, plan,
}: {
  thesis: ThesisArtifact | null;
  plan: TradePlanArtifact | null;
}) {
  if (!thesis && !plan) return null;
  return (
    <div className="review-foundation-panel" aria-label="Decision context for review">
      <p className="eyebrow">Decision Context</p>
      <p className="review-foundation-note">
        Review your original reasoning before recording your reflection.
      </p>
      {thesis ? (
        <div className="review-foundation-section">
          <p className="thesis-context-label">Original Thesis</p>
          <p className="review-foundation-text" title={thesis.narrative}>
            {truncate(thesis.narrative, 200)}
          </p>
          <p className="review-foundation-meta">
            Conviction: {thesis.confidence_level}/5
            {thesis.regime_alignment ? ` · Regime: ${thesis.regime_alignment}` : ""}
          </p>
        </div>
      ) : null}
      {plan ? (
        <div className="review-foundation-section">
          <p className="thesis-context-label">Original Plan</p>
          <p className="review-foundation-text" title={plan.entry_rationale}>
            <span className="cognitive-field-label">Entry: </span>
            {truncate(plan.entry_rationale, 160)}
          </p>
          {plan.playbook_alignment ? (
            <span className="cognitive-playbook-badge">{plan.playbook_alignment}</span>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}

function ReviewReflectionPanel({ reflection }: { reflection: ReviewReflectionArtifact }) {
  return (
    <div className="review-reflection-panel" aria-label="Review reflection">
      <p className="eyebrow">Review Reflection</p>
      <div className="review-reflection-outcome">
        <p className="thesis-context-label">Thesis vs Outcome</p>
        <p className="review-reflection-text">{reflection.thesis_vs_outcome}</p>
      </div>
      <div className="review-quality-grid">
        <div className="review-quality-item">
          <p className="thesis-context-label">Decision Quality</p>
          <p className="review-quality-value">
            {QUALITY_LABELS[reflection.decision_quality] ?? reflection.decision_quality}
            {" "}({reflection.decision_quality}/5)
          </p>
        </div>
        <div className="review-quality-item">
          <p className="thesis-context-label">Execution Quality</p>
          <p className="review-quality-value">
            {QUALITY_LABELS[reflection.execution_quality] ?? reflection.execution_quality}
            {" "}({reflection.execution_quality}/5)
          </p>
        </div>
      </div>
      <div className="review-reflection-section">
        <p className="thesis-context-label">Discipline Observations</p>
        <p className="review-reflection-text">{reflection.discipline_observations}</p>
      </div>
      <div className="review-reflection-section">
        <p className="thesis-context-label">Lessons Learned</p>
        <ul className="thesis-context-list">
          {reflection.lessons_learned.map((l) => <li key={l}>{l}</li>)}
        </ul>
      </div>
      {reflection.behavioral_observations ? (
        <div className="review-reflection-section">
          <p className="thesis-context-label">Behavioral Observations</p>
          <p className="review-reflection-text">{reflection.behavioral_observations}</p>
        </div>
      ) : null}
    </div>
  );
}

function BehavioralReviewPanel({
  signals,
  clusters,
  mistakes,
  emotional,
  metrics,
}: {
  signals: BehavioralSignalList | null;
  clusters: BehavioralClusterList | null;
  mistakes: RecurringMistakeList | null;
  emotional: EmotionalReflectionList | null;
  metrics: DecisionQualityMetrics | null;
}) {
  if (!signals && !clusters && !mistakes && !emotional && !metrics) return null;
  return (
    <div className="behavioral-review-panel" aria-label="Derived behavioral review context">
      <div className="behavioral-panel-header">
        <div>
          <p className="eyebrow">Behavioral Audit</p>
          <p className="behavioral-authority-note">
            Derived review context from event history. Not canonical truth or lifecycle authority.
          </p>
        </div>
        <span className="field-authority-badge authority-derived">Derived</span>
      </div>

      {metrics && metrics.total_count > 0 ? (
        <div className="behavioral-metric-row">
          <div>
            <p className="thesis-context-label">Decision Quality</p>
            <p className="review-quality-value">{metrics.average_decision_quality ?? "n/a"}/5</p>
          </div>
          <div>
            <p className="thesis-context-label">Execution Quality</p>
            <p className="review-quality-value">{metrics.average_execution_quality ?? "n/a"}/5</p>
          </div>
          <div>
            <p className="thesis-context-label">Process Signals</p>
            <p className="review-quality-value">
              {metrics.metrics.reduce((sum, metric) => sum + metric.process_signal_count, 0)}
            </p>
          </div>
        </div>
      ) : null}

      {signals && signals.total_count > 0 ? (
        <div className="behavioral-signal-list">
          {signals.signals.map((signal) => (
            <div className="behavioral-signal-item" data-severity={signal.severity} key={signal.signal_id}>
              <span className="behavioral-signal-type">{signal.signal_type.replace(/_/g, " ")}</span>
              <p>{signal.summary}</p>
              <p className="behavioral-source-note">
                {signal.source_event_refs.length} source event{signal.source_event_refs.length !== 1 ? "s" : ""}
                {signal.recurring ? ` · recurring ${signal.recurrence_count} times` : ""}
              </p>
            </div>
          ))}
        </div>
      ) : null}

      <div className="behavioral-summary-grid">
        <div>
          <p className="thesis-context-label">Clusters</p>
          <p className="behavioral-count">{clusters?.total_count ?? 0}</p>
        </div>
        <div>
          <p className="thesis-context-label">Recurring Mistakes</p>
          <p className="behavioral-count">{mistakes?.total_count ?? 0}</p>
        </div>
        <div>
          <p className="thesis-context-label">Emotional Reflection Terms</p>
          <p className="behavioral-count">
            {emotional?.overlays.reduce((sum, overlay) => sum + overlay.emotional_terms.length, 0) ?? 0}
          </p>
        </div>
      </div>
    </div>
  );
}

type ReviewWorkspaceProps = {
  context: Required<WorkspaceContext>;
  onNavigate: (event: MouseEvent<HTMLAnchorElement>, href: string) => void;
  onStageLoaded?: (stage: string | null) => void;
};

export function ReviewWorkspace({ context, onStageLoaded }: ReviewWorkspaceProps) {
  const [projection, setProjection] = useState<WorkspaceProjection | null>(null);
  const [thesis, setThesis] = useState<ThesisArtifact | null>(null);
  const [plan, setPlan] = useState<TradePlanArtifact | null>(null);
  const [reflection, setReflection] = useState<ReviewReflectionArtifact | null>(null);
  const [behavioralSignals, setBehavioralSignals] = useState<BehavioralSignalList | null>(null);
  const [behavioralClusters, setBehavioralClusters] = useState<BehavioralClusterList | null>(null);
  const [recurringMistakes, setRecurringMistakes] = useState<RecurringMistakeList | null>(null);
  const [emotionalReflections, setEmotionalReflections] = useState<EmotionalReflectionList | null>(null);
  const [qualityMetrics, setQualityMetrics] = useState<DecisionQualityMetrics | null>(null);
  const [showReviewModal, setShowReviewModal] = useState(false);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [, setTransitionState] = useState<TransitionState>("idle");
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
      fetchWorkspaceProjection("review", params, signal)
        .then((data) => {
          setProjection(data);
          setLoadError(null);
          onStageLoaded?.(data.lifecycle_state?.current_stage ?? null);
        })
        .catch((err: unknown) => {
          if (err instanceof DOMException && err.name === "AbortError") return;
          setLoadError(
            err instanceof Error ? err.message : "Failed to load review workspace",
          );
        });

      if (context.decision_id) {
        fetchThesisArtifact(context.decision_id, signal)
          .then(setThesis)
          .catch((err: unknown) => {
            if (err instanceof DOMException && err.name === "AbortError") return;
          });
        fetchPlanArtifact(context.decision_id, signal)
          .then(setPlan)
          .catch((err: unknown) => {
            if (err instanceof DOMException && err.name === "AbortError") return;
          });
        fetchReviewReflection(context.decision_id, signal)
          .then(setReflection)
          .catch((err: unknown) => {
            if (err instanceof DOMException && err.name === "AbortError") return;
          });
        const behavioralParams = {
          persona_id: context.persona_id,
          workspace_id: context.workspace_id,
          decision_id: context.decision_id,
        };
        fetchBehavioralSignals(behavioralParams, signal).then(setBehavioralSignals).catch(() => {});
        fetchBehavioralClusters(behavioralParams, signal).then(setBehavioralClusters).catch(() => {});
        fetchRecurringMistakes(behavioralParams, signal).then(setRecurringMistakes).catch(() => {});
        fetchEmotionalReflections(behavioralParams, signal).then(setEmotionalReflections).catch(() => {});
        fetchDecisionQualityMetrics(behavioralParams, signal).then(setQualityMetrics).catch(() => {});
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
  const canCompleteReview = lifecycleStage === "Position";
  const reviewComplete = lifecycleStage === "Review";

  function handleReviewSuccess() {
    setShowReviewModal(false);
    setTransitionState("idle");
    const controller = new AbortController();
    fetchControllerRef.current = controller;
    loadProjection(controller.signal);
  }

  const fieldOrder = ["review_references", "decision_quality_context", "behavioral_signal"];

  return (
    <section className="workspace-surface" aria-labelledby="review-workspace-title">
      <div className="surface-title">
        <Compass aria-hidden="true" />
        <div>
          <p className="eyebrow">Review Workspace</p>
          <h1 id="review-workspace-title">What should be learned from the decision?</h1>
        </div>
      </div>

      {loadError ? <div className="runtime-error">{loadError}</div> : null}

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

          <ReviewFoundationPanel plan={plan} thesis={thesis} />

          {reflection ? <ReviewReflectionPanel reflection={reflection} /> : null}

          <BehavioralReviewPanel
            clusters={behavioralClusters}
            emotional={emotionalReflections}
            metrics={qualityMetrics}
            mistakes={recurringMistakes}
            signals={behavioralSignals}
          />

          {showReviewModal && context.decision_id ? (
            <ReviewReflectionModal
              context={context}
              onCancel={() => setShowReviewModal(false)}
              onSuccess={handleReviewSuccess}
              symbol={thesis?.symbol ?? plan?.symbol ?? ""}
            />
          ) : null}

          {reviewComplete ? (
            <div className="lifecycle-complete-surface" aria-label="Review complete">
              <CheckCircle aria-hidden="true" />
              <div>
                <p className="eyebrow">Review Recorded</p>
                <p className="lifecycle-action-note">
                  This decision has completed the full lifecycle. The review reflection
                  is a durable learning artifact in the event ledger.
                </p>
              </div>
            </div>
          ) : canCompleteReview ? (
            <div className="lifecycle-action-surface">
              <p className="eyebrow">Available Lifecycle Action</p>
              <p className="lifecycle-action-note">
                Record a structured reflection — thesis vs outcome, decision quality,
                execution quality, and lessons learned become replayable learning artifacts.
              </p>
              <button
                className="lifecycle-action-btn"
                onClick={() => setShowReviewModal(true)}
                type="button"
              >
                Complete Review
              </button>
            </div>
          ) : null}

          <div className="attention-authority-note" aria-label="Authority boundaries">
            {projection.authority_boundaries.map((boundary) => (
              <p className="authority-boundary" key={boundary}>{boundary}</p>
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
