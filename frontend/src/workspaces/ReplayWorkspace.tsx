import { History } from "lucide-react";
import { type MouseEvent, useCallback, useEffect, useState } from "react";

import {
  fetchReplayTimeline,
  fetchWorkspaceProjection,
  fetchCognitiveSnapshot,
  fetchAnnotations,
  fetchBehaviorTimeline,
  type Annotation,
  type AnnotationList,
  type BehaviorTimeline,
  type CognitiveSnapshot,
  type ReplayTimeline,
  type ReplayTimelineEntry,
  type WorkspaceApiParams,
  type WorkspaceProjection,
} from "../api/runtime";
import { type WorkspaceContext } from "../workspaceRouting";
import { CognitiveSnapshotPanel } from "./CognitiveSnapshotPanel";
import { AnnotationModal } from "./AnnotationModal";
import { AdvisoryInterpretationPanel } from "./AdvisoryInterpretationPanel";

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

const KIND_LABELS: Record<string, string> = {
  lifecycle: "Lifecycle",
  cognition: "Cognition",
  execution: "Execution",
  review: "Review",
  system: "System",
};

const CONFIDENCE_LABELS: Record<number, string> = {
  1: "Speculative", 2: "Low", 3: "Moderate", 4: "High", 5: "Conviction",
};

const BRANCH_TYPE_LABELS: Record<string, string> = {
  primary: "Primary",
  alternative: "Alternative",
  invalidation: "Invalidation",
  regime_transition: "Regime Transition",
};

// ── Payload type guards ────────────────────────────────────────────────────

type ThesisPayloadData = {
  narrative: string;
  catalysts: string[];
  assumptions: string[];
  invalidation_conditions: string[];
  confidence_level: number;
  regime_alignment: string;
};

type PlanPayloadData = {
  entry_rationale: string;
  stop_rationale: string;
  target_rationale: string;
  sizing_rationale: string;
  execution_assumptions: string[];
  playbook_alignment: string;
};

function extractThesisPayload(
  payload: Record<string, unknown>,
): ThesisPayloadData | null {
  const t = payload["thesis"];
  if (!t || typeof t !== "object") return null;
  const thesis = t as Record<string, unknown>;
  const narrative = thesis["narrative"];
  if (typeof narrative !== "string" || !narrative) return null;
  return {
    narrative,
    catalysts: Array.isArray(thesis["catalysts"])
      ? (thesis["catalysts"] as unknown[]).filter((x): x is string => typeof x === "string")
      : [],
    assumptions: Array.isArray(thesis["assumptions"])
      ? (thesis["assumptions"] as unknown[]).filter((x): x is string => typeof x === "string")
      : [],
    invalidation_conditions: Array.isArray(thesis["invalidation_conditions"])
      ? (thesis["invalidation_conditions"] as unknown[]).filter(
          (x): x is string => typeof x === "string",
        )
      : [],
    confidence_level:
      typeof thesis["confidence_level"] === "number"
        ? (thesis["confidence_level"] as number)
        : 3,
    regime_alignment:
      typeof thesis["regime_alignment"] === "string"
        ? (thesis["regime_alignment"] as string)
        : "",
  };
}

type ScenarioBranchData = {
  branch_type: string;
  condition: string;
  implication: string;
  confidence: number;
  notes: string;
};

function extractScenarioBranchPayload(
  payload: Record<string, unknown>,
): ScenarioBranchData | null {
  const b = payload["branch"];
  if (!b || typeof b !== "object") return null;
  const branch = b as Record<string, unknown>;
  const condition = branch["condition"];
  if (typeof condition !== "string" || !condition) return null;
  return {
    branch_type: typeof branch["branch_type"] === "string" ? (branch["branch_type"] as string) : "",
    condition,
    implication: typeof branch["implication"] === "string" ? (branch["implication"] as string) : "",
    confidence: typeof branch["confidence"] === "number" ? (branch["confidence"] as number) : 3,
    notes: typeof branch["notes"] === "string" ? (branch["notes"] as string) : "",
  };
}

function extractPlanPayload(
  payload: Record<string, unknown>,
): PlanPayloadData | null {
  const p = payload["plan"];
  if (!p || typeof p !== "object") return null;
  const plan = p as Record<string, unknown>;
  const entry = plan["entry_rationale"];
  if (typeof entry !== "string" || !entry) return null;
  return {
    entry_rationale: entry,
    stop_rationale:
      typeof plan["stop_rationale"] === "string"
        ? (plan["stop_rationale"] as string)
        : "",
    target_rationale:
      typeof plan["target_rationale"] === "string"
        ? (plan["target_rationale"] as string)
        : "",
    sizing_rationale:
      typeof plan["sizing_rationale"] === "string"
        ? (plan["sizing_rationale"] as string)
        : "",
    execution_assumptions: Array.isArray(plan["execution_assumptions"])
      ? (plan["execution_assumptions"] as unknown[]).filter(
          (x): x is string => typeof x === "string",
        )
      : [],
    playbook_alignment:
      typeof plan["playbook_alignment"] === "string"
        ? (plan["playbook_alignment"] as string)
        : "",
  };
}

function truncate(text: string, max: number): string {
  return text.length > max ? text.slice(0, max) + "…" : text;
}

// ── Cognitive artifact inline previews ────────────────────────────────────

function ThesisPayloadPreview({ thesis, eventType }: { thesis: ThesisPayloadData; eventType: string }) {
  const isRevision = eventType === "decision.thesis_revised";
  const convictionLabel = CONFIDENCE_LABELS[thesis.confidence_level] ?? String(thesis.confidence_level);

  return (
    <div className="cognitive-artifact-preview thesis-preview">
      <div className="cognitive-artifact-header">
        <span className="cognitive-artifact-type">
          {isRevision ? "Thesis Revision" : "Thesis"}
        </span>
        <span className="cognitive-conviction-badge">
          {convictionLabel} ({thesis.confidence_level}/5)
        </span>
        {thesis.regime_alignment ? (
          <span className="cognitive-regime-badge">{thesis.regime_alignment}</span>
        ) : null}
      </div>
      <p className="cognitive-narrative" title={thesis.narrative}>
        {truncate(thesis.narrative, 160)}
      </p>
      <div className="cognitive-counts">
        <span className="cognitive-count-item">
          {thesis.catalysts.length} catalyst{thesis.catalysts.length !== 1 ? "s" : ""}
        </span>
        <span className="cognitive-count-sep">·</span>
        <span className="cognitive-count-item">
          {thesis.invalidation_conditions.length} invalidation condition{thesis.invalidation_conditions.length !== 1 ? "s" : ""}
        </span>
        {thesis.assumptions.length > 0 ? (
          <>
            <span className="cognitive-count-sep">·</span>
            <span className="cognitive-count-item">
              {thesis.assumptions.length} assumption{thesis.assumptions.length !== 1 ? "s" : ""}
            </span>
          </>
        ) : null}
      </div>
    </div>
  );
}

function PlanPayloadPreview({ plan }: { plan: PlanPayloadData }) {
  return (
    <div className="cognitive-artifact-preview plan-preview">
      <div className="cognitive-artifact-header">
        <span className="cognitive-artifact-type">Trade Plan</span>
        {plan.playbook_alignment ? (
          <span className="cognitive-playbook-badge">{plan.playbook_alignment}</span>
        ) : null}
      </div>
      <p className="cognitive-entry-rationale" title={plan.entry_rationale}>
        <span className="cognitive-field-label">Entry: </span>
        {truncate(plan.entry_rationale, 130)}
      </p>
      <p className="cognitive-stop-rationale" title={plan.stop_rationale}>
        <span className="cognitive-field-label">Stop: </span>
        {truncate(plan.stop_rationale, 130)}
      </p>
      {plan.execution_assumptions.length > 0 ? (
        <div className="cognitive-counts">
          <span className="cognitive-count-item">
            {plan.execution_assumptions.length} execution assumption{plan.execution_assumptions.length !== 1 ? "s" : ""}
          </span>
        </div>
      ) : null}
    </div>
  );
}

function ScenarioBranchPreview({ branch }: { branch: ScenarioBranchData }) {
  const typeLabel = BRANCH_TYPE_LABELS[branch.branch_type] ?? branch.branch_type;
  return (
    <div className="cognitive-artifact-preview scenario-preview">
      <div className="cognitive-artifact-header">
        <span className="cognitive-artifact-type">Scenario</span>
        <span className={`cognitive-branch-type-badge branch-${branch.branch_type}`}>
          {typeLabel}
        </span>
        <span className="cognitive-conviction-badge">
          {branch.confidence}/5
        </span>
      </div>
      <p className="cognitive-narrative" title={branch.condition}>
        <span className="cognitive-field-label">If: </span>
        {truncate(branch.condition, 130)}
      </p>
      <p className="cognitive-narrative" title={branch.implication}>
        <span className="cognitive-field-label">Then: </span>
        {truncate(branch.implication, 130)}
      </p>
      {branch.notes ? (
        <p className="cognitive-count-item">{truncate(branch.notes, 80)}</p>
      ) : null}
    </div>
  );
}

// ── Cognitive snapshot summary ─────────────────────────────────────────────

const THESIS_EVENT_TYPES = new Set([
  "decision.thesis_created",
  "decision.thesis_revised",
]);

function CognitiveSnapshotSummary({ entries }: { entries: ReplayTimelineEntry[] }) {
  let latestThesis: ThesisPayloadData | null = null;
  let latestThesisType = "";
  let latestPlan: PlanPayloadData | null = null;
  let thesisEventCount = 0;
  let scenarioBranchCount = 0;

  for (const entry of entries) {
    if (THESIS_EVENT_TYPES.has(entry.event_type)) {
      const t = extractThesisPayload(entry.payload);
      if (t) {
        latestThesis = t;
        latestThesisType = entry.event_type;
        thesisEventCount += 1;
      }
    }
    if (entry.event_type === "decision.plan_created") {
      const p = extractPlanPayload(entry.payload);
      if (p) latestPlan = p;
    }
    if (entry.event_type === "decision.scenario_branch_created") {
      const b = extractScenarioBranchPayload(entry.payload);
      if (b) scenarioBranchCount += 1;
    }
  }

  if (!latestThesis && !latestPlan && scenarioBranchCount === 0) return null;

  const isRevised = thesisEventCount > 1 || latestThesisType === "decision.thesis_revised";

  return (
    <div className="cognitive-snapshot-summary" aria-label="Cognitive snapshot">
      <p className="eyebrow">
        Cognitive Snapshot
        <span className="cognitive-snapshot-note"> — latest operator reasoning at this point in replay</span>
      </p>

      {latestThesis ? (
        <div className="cognitive-snapshot-thesis">
          <p className="cognitive-snapshot-label">
            Thesis
            {isRevised ? (
              <span className="cognitive-revised-indicator">
                {" "}— {thesisEventCount > 1 ? `${thesisEventCount} versions` : "revised"}
              </span>
            ) : null}
          </p>
          <p className="cognitive-snapshot-narrative" title={latestThesis.narrative}>
            {truncate(latestThesis.narrative, 200)}
          </p>
          <div className="cognitive-snapshot-meta">
            <span className="cognitive-conviction-badge">
              {CONFIDENCE_LABELS[latestThesis.confidence_level] ?? latestThesis.confidence_level}
              {" "}({latestThesis.confidence_level}/5)
            </span>
            {latestThesis.regime_alignment ? (
              <span className="cognitive-regime-badge">{latestThesis.regime_alignment}</span>
            ) : null}
          </div>
        </div>
      ) : null}

      {latestPlan ? (
        <div className="cognitive-snapshot-plan">
          <p className="cognitive-snapshot-label">Plan</p>
          <p className="cognitive-snapshot-entry" title={latestPlan.entry_rationale}>
            <span className="cognitive-field-label">Entry: </span>
            {truncate(latestPlan.entry_rationale, 160)}
          </p>
          {latestPlan.playbook_alignment ? (
            <span className="cognitive-playbook-badge">{latestPlan.playbook_alignment}</span>
          ) : null}
        </div>
      ) : null}

      {scenarioBranchCount > 0 ? (
        <div className="cognitive-snapshot-plan">
          <p className="cognitive-snapshot-label">Scenario Branches</p>
          <p className="cognitive-snapshot-entry">
            {scenarioBranchCount} scenario branch{scenarioBranchCount !== 1 ? "es" : ""} defined
          </p>
        </div>
      ) : null}

      <p className="cognitive-snapshot-authority">
        Derived from event payloads — not canonical truth.
      </p>
    </div>
  );
}

// ── Timeline entry row ─────────────────────────────────────────────────────

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

const ANNOTATION_TYPE_LABELS: Record<string, string> = {
  observation: "Observation",
  question: "Question",
  insight: "Insight",
  postmortem: "Postmortem",
};

function AnnotationBadge({ annotation }: { annotation: Annotation }) {
  return (
    <div className="annotation-badge" aria-label={`Annotation: ${annotation.annotation_type}`}>
      <span className={`annotation-type-tag ann-${annotation.annotation_type}`}>
        {ANNOTATION_TYPE_LABELS[annotation.annotation_type] ?? annotation.annotation_type}
      </span>
      <p className="annotation-note-text">{annotation.note}</p>
    </div>
  );
}

function BehaviorTimelinePanel({ timeline }: { timeline: BehaviorTimeline | null }) {
  if (!timeline || timeline.total_count === 0) return null;
  return (
    <div className="behavioral-review-panel" aria-label="Operator behavior timeline">
      <div className="behavioral-panel-header">
        <div>
          <p className="eyebrow">Behavior Timeline</p>
          <p className="behavioral-authority-note">
            Chronological derived signals reconstructed from event history.
          </p>
        </div>
        <span className="field-authority-badge authority-derived">Derived</span>
      </div>
      <ol className="behavior-timeline-list">
        {timeline.entries.map((entry) => (
          <li className="behavior-timeline-entry" key={entry.entry_id}>
            <span className="behavioral-signal-type">{entry.entry_type.replace(/_/g, " ")}</span>
            <p>{entry.summary}</p>
            <p className="behavioral-source-note">
              {new Date(entry.timestamp).toLocaleString()} · {entry.source_signal_ids.length} source signal
              {entry.source_signal_ids.length !== 1 ? "s" : ""}
            </p>
          </li>
        ))}
      </ol>
    </div>
  );
}

function TimelineEntryRow({
  entry,
  isSelected,
  onClick,
  annotations,
  onAnnotate,
}: {
  entry: ReplayTimelineEntry;
  isSelected?: boolean;
  onClick?: (timestamp: string) => void;
  annotations?: Annotation[];
  onAnnotate?: (sequence: number, eventType: string) => void;
}) {
  const kindLabel = KIND_LABELS[entry.kind] ?? entry.kind;
  const ts = new Date(entry.timestamp).toLocaleString(undefined, {
    dateStyle: "short",
    timeStyle: "medium",
  });

  const thesisData = THESIS_EVENT_TYPES.has(entry.event_type)
    ? extractThesisPayload(entry.payload)
    : null;
  const planData =
    entry.event_type === "decision.plan_created"
      ? extractPlanPayload(entry.payload)
      : null;
  const branchData =
    entry.event_type === "decision.scenario_branch_created"
      ? extractScenarioBranchPayload(entry.payload)
      : null;

  return (
    <li
      className={`timeline-entry${isSelected ? " timeline-entry-selected" : ""}${onClick ? " timeline-entry-clickable" : ""}`}
      data-kind={entry.kind}
      aria-label={`${kindLabel}: ${entry.event_type}`}
      onClick={onClick ? () => onClick(entry.timestamp) : undefined}
      role={onClick ? "button" : undefined}
      tabIndex={onClick ? 0 : undefined}
      onKeyDown={onClick ? (e) => { if (e.key === "Enter" || e.key === " ") onClick(entry.timestamp); } : undefined}
    >
      <div className="timeline-entry-header">
        <span className={`timeline-kind-badge kind-${entry.kind}`}>
          {kindLabel}
        </span>
        <code className="timeline-event-type">{entry.event_type}</code>
        {entry.lifecycle_stage ? (
          <span className="timeline-stage-tag">{entry.lifecycle_stage}</span>
        ) : null}
      </div>
      <div className="timeline-entry-meta">
        <span className="eyebrow">#{entry.source_sequence}</span>
        <span className="timeline-timestamp">{ts}</span>
      </div>
      {thesisData ? (
        <ThesisPayloadPreview eventType={entry.event_type} thesis={thesisData} />
      ) : planData ? (
        <PlanPayloadPreview plan={planData} />
      ) : branchData ? (
        <ScenarioBranchPreview branch={branchData} />
      ) : null}

      {annotations && annotations.length > 0 ? (
        <div className="timeline-annotations">
          {annotations.map((ann, i) => (
            <AnnotationBadge annotation={ann} key={i} />
          ))}
        </div>
      ) : null}

      {onAnnotate ? (
        <button
          aria-label={`Add note to event ${entry.source_sequence}`}
          className="annotation-add-btn"
          onClick={(e) => {
            e.stopPropagation();
            onAnnotate(entry.source_sequence, entry.event_type);
          }}
          type="button"
        >
          + Note
        </button>
      ) : null}
    </li>
  );
}

// ── Main workspace ─────────────────────────────────────────────────────────

type ReplayWorkspaceProps = {
  context: Required<WorkspaceContext>;
  onNavigate: (event: MouseEvent<HTMLAnchorElement>, href: string) => void;
};

export function ReplayWorkspace({ context }: ReplayWorkspaceProps) {
  const [projection, setProjection] = useState<WorkspaceProjection | null>(null);
  const [timeline, setTimeline] = useState<ReplayTimeline | null>(null);
  const [cognitiveSnapshot, setCognitiveSnapshot] = useState<CognitiveSnapshot | null>(null);
  const [selectedEntryTimestamp, setSelectedEntryTimestamp] = useState<string | null>(null);
  const [annotationList, setAnnotationList] = useState<AnnotationList | null>(null);
  const [behaviorTimeline, setBehaviorTimeline] = useState<BehaviorTimeline | null>(null);
  const [annotatingEntry, setAnnotatingEntry] = useState<{ sequence: number; eventType: string } | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);

  const params: WorkspaceApiParams = {
    persona_id: context.persona_id,
    persona_version: context.persona_version,
    workspace_id: context.workspace_id,
    workflow_id: context.selected_workflow_id || undefined,
    decision_id: context.decision_id || undefined,
  };

  useEffect(() => {
    const controller = new AbortController();

    Promise.all([
      fetchWorkspaceProjection("replay", params, controller.signal),
      fetchReplayTimeline(controller.signal),
    ])
      .then(([projectionData, timelineData]) => {
        setProjection(projectionData);
        setTimeline(timelineData);
        setLoadError(null);
      })
      .catch((err: unknown) => {
        if (err instanceof DOMException && err.name === "AbortError") return;
        setLoadError(
          err instanceof Error ? err.message : "Failed to load replay workspace",
        );
      });

    if (context.decision_id) {
      fetchCognitiveSnapshot(context.decision_id, undefined, controller.signal)
        .then(setCognitiveSnapshot)
        .catch((err: unknown) => {
          if (err instanceof DOMException && err.name === "AbortError") return;
        });
      fetchAnnotations(context.decision_id, controller.signal)
        .then(setAnnotationList)
        .catch((err: unknown) => {
          if (err instanceof DOMException && err.name === "AbortError") return;
        });
      fetchBehaviorTimeline(
        {
          persona_id: context.persona_id,
          workspace_id: context.workspace_id,
          decision_id: context.decision_id,
        },
        controller.signal,
      )
        .then(setBehaviorTimeline)
        .catch((err: unknown) => {
          if (err instanceof DOMException && err.name === "AbortError") return;
        });
    }

    return () => controller.abort();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [
    context.persona_id,
    context.persona_version,
    context.workspace_id,
    context.selected_workflow_id,
    context.decision_id,
  ]);

  const handleEntryClick = useCallback(
    (timestamp: string) => {
      if (!context.decision_id) return;
      setSelectedEntryTimestamp(timestamp);
      fetchCognitiveSnapshot(context.decision_id, timestamp)
        .then(setCognitiveSnapshot)
        .catch(() => {});
    },
    [context.decision_id],
  );

  const handleClearSelection = useCallback(() => {
    setSelectedEntryTimestamp(null);
    if (context.decision_id) {
      fetchCognitiveSnapshot(context.decision_id)
        .then(setCognitiveSnapshot)
        .catch(() => {});
    }
  }, [context.decision_id]);

  const fieldOrder = [
    "event_timeline_references",
    "reconstructed_workspace_state",
    "historical_interpretation",
    "advisory_replay_summary",
  ];

  return (
    <section
      className="workspace-surface"
      aria-labelledby="replay-workspace-title"
    >
      <div className="surface-title">
        <History aria-hidden="true" />
        <div>
          <p className="eyebrow">Replay Workspace</p>
          <h1 id="replay-workspace-title">
            What historical context must be reconstructed?
          </h1>
        </div>
      </div>

      {loadError ? (
        <div className="runtime-error">{loadError}</div>
      ) : null}

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
        </>
      ) : null}

      {timeline !== null ? (
        <div className="replay-timeline-section">
          <p className="eyebrow">
            Replay Timeline — {timeline.source_event_count} source event
            {timeline.source_event_count !== 1 ? "s" : ""}
          </p>

          {timeline.entries.length === 0 ? (
            <p className="field-no-data">
              No replayable events in the ledger yet.
            </p>
          ) : (
            <>
              {cognitiveSnapshot && context.decision_id ? (
                <CognitiveSnapshotPanel
                  onClearSelection={handleClearSelection}
                  selectedTimestamp={selectedEntryTimestamp}
                  snapshot={cognitiveSnapshot}
                />
              ) : (
                <CognitiveSnapshotSummary entries={timeline.entries} />
              )}
              <p className="cognitive-snapshot-authority">
                {context.decision_id
                  ? "Click a timeline entry to reconstruct cognitive state at that moment."
                  : null}
              </p>
              {annotatingEntry && context.decision_id ? (
                <AnnotationModal
                  context={context}
                  eventType={annotatingEntry.eventType}
                  onCancel={() => setAnnotatingEntry(null)}
                  onSuccess={() => {
                    setAnnotatingEntry(null);
                    if (context.decision_id) {
                      fetchAnnotations(context.decision_id)
                        .then(setAnnotationList)
                        .catch(() => {});
                    }
                  }}
                  sequence={annotatingEntry.sequence}
                />
              ) : null}

              <ol className="timeline-entries" aria-label="Replay timeline">
                {timeline.entries.map((entry) => {
                  const entryAnnotations = annotationList?.annotations.filter(
                    (a) => a.sequence === entry.source_sequence,
                  );
                  return (
                    <TimelineEntryRow
                      annotations={entryAnnotations}
                      entry={entry}
                      isSelected={selectedEntryTimestamp === entry.timestamp}
                      key={`${entry.source_sequence}-${entry.event_type}`}
                      onAnnotate={
                        context.decision_id
                          ? (seq, evtType) =>
                              setAnnotatingEntry({ sequence: seq, eventType: evtType })
                          : undefined
                      }
                      onClick={context.decision_id ? handleEntryClick : undefined}
                    />
                  );
                })}
              </ol>
            </>
          )}

          <p className="timeline-authority-note">
            {timeline.authority} — reconstructed from event ledger, not live APIs.
          </p>
        </div>
      ) : null}

      <BehaviorTimelinePanel timeline={behaviorTimeline} />

      <AdvisoryInterpretationPanel
        context={context}
        title="Replay-visible interpretation artifacts"
      />

      {projection !== null ? (
        <div className="projection-metadata">
          <span className="eyebrow">Projection Basis</span>
          <p className="projection-detail">
            {projection.authority} — {projection.source_event_count} source events
          </p>
        </div>
      ) : null}
    </section>
  );
}
