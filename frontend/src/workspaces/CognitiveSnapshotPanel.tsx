import {
  type CognitiveSnapshot,
  type CognitiveSnapshotBranch,
} from "../api/runtime";

const CONFIDENCE_LABELS: Record<number, string> = {
  1: "Speculative", 2: "Low", 3: "Moderate", 4: "High", 5: "Conviction",
};

const LIKELIHOOD_LABELS: Record<number, string> = {
  1: "Unlikely", 2: "Possible", 3: "Likely", 4: "Probable", 5: "Expected",
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

function BranchSummary({ branches }: { branches: CognitiveSnapshotBranch[] }) {
  if (branches.length === 0) return null;

  const counts = branches.reduce<Record<string, number>>((acc, b) => {
    acc[b.branch_type] = (acc[b.branch_type] ?? 0) + 1;
    return acc;
  }, {});

  return (
    <div className="cognitive-snapshot-section">
      <p className="thesis-context-label">Scenario Branches ({branches.length})</p>
      <div className="cognitive-snapshot-branch-summary">
        {Object.entries(counts).map(([type, count]) => (
          <span
            className={`cognitive-branch-type-badge branch-${type}`}
            key={type}
          >
            {count} {BRANCH_TYPE_LABELS[type] ?? type}
          </span>
        ))}
      </div>
      {branches.slice(0, 2).map((b, i) => (
        <p className="cognitive-snapshot-branch-item" key={i}>
          <span className={`cognitive-branch-type-badge branch-${b.branch_type} small`}>
            {BRANCH_TYPE_LABELS[b.branch_type] ?? b.branch_type}
          </span>
          {" "}{truncate(b.condition, 80)}
          {" "}→ {truncate(b.implication, 60)}
          {" "}
          <span className="cognitive-conviction-badge">
            {LIKELIHOOD_LABELS[b.confidence]}
          </span>
        </p>
      ))}
      {branches.length > 2 ? (
        <p className="cognitive-count-item">+{branches.length - 2} more branch{branches.length - 2 !== 1 ? "es" : ""}…</p>
      ) : null}
    </div>
  );
}

type Props = {
  snapshot: CognitiveSnapshot;
  selectedTimestamp: string | null;
  onClearSelection?: () => void;
};

export function CognitiveSnapshotPanel({
  snapshot,
  selectedTimestamp,
  onClearSelection,
}: Props) {
  const ts = selectedTimestamp
    ? new Date(selectedTimestamp).toLocaleString(undefined, {
        dateStyle: "short",
        timeStyle: "medium",
      })
    : null;

  const isRevised = snapshot.thesis?.event_type === "decision.thesis_revised";

  return (
    <div
      className="cognitive-snapshot-panel"
      aria-label="Cognitive snapshot"
      data-selected={!!selectedTimestamp}
    >
      <div className="cognitive-snapshot-panel-header">
        <p className="eyebrow">
          {ts ? `Cognitive Snapshot at ${ts}` : "Current Cognitive State"}
          {snapshot.event_count_at_snapshot > 0 ? (
            <span className="cognitive-snapshot-note">
              {" "}— {snapshot.event_count_at_snapshot} events
            </span>
          ) : null}
        </p>
        {selectedTimestamp && onClearSelection ? (
          <button
            className="thesis-list-remove-btn"
            onClick={onClearSelection}
            title="Return to current state"
            type="button"
          >
            ×
          </button>
        ) : null}
      </div>

      {snapshot.current_stage ? (
        <p className="cognitive-snapshot-stage">
          <span className="timeline-stage-tag">{snapshot.current_stage}</span>
        </p>
      ) : (
        <p className="field-no-data">No lifecycle events at this point.</p>
      )}

      {snapshot.thesis ? (
        <div className="cognitive-snapshot-section">
          <p className="thesis-context-label">
            Thesis
            {isRevised ? (
              <span className="cognitive-revised-indicator"> — Revised</span>
            ) : null}
          </p>
          <p
            className="cognitive-snapshot-narrative"
            title={snapshot.thesis.narrative}
          >
            {truncate(snapshot.thesis.narrative, 200)}
          </p>
          <div className="cognitive-snapshot-meta">
            <span className="cognitive-conviction-badge">
              {CONFIDENCE_LABELS[snapshot.thesis.confidence_level] ??
                snapshot.thesis.confidence_level}{" "}
              ({snapshot.thesis.confidence_level}/5)
            </span>
            {snapshot.thesis.regime_alignment ? (
              <span className="cognitive-regime-badge">
                {snapshot.thesis.regime_alignment}
              </span>
            ) : null}
            <span className="cognitive-count-item">
              {snapshot.thesis.catalysts.length} catalyst
              {snapshot.thesis.catalysts.length !== 1 ? "s" : ""}
            </span>
            <span className="cognitive-count-sep">·</span>
            <span className="cognitive-count-item">
              {snapshot.thesis.invalidation_conditions.length} invalidation condition
              {snapshot.thesis.invalidation_conditions.length !== 1 ? "s" : ""}
            </span>
          </div>
        </div>
      ) : snapshot.current_stage ? (
        <p className="field-no-data">No structured thesis at this point.</p>
      ) : null}

      {snapshot.plan ? (
        <div className="cognitive-snapshot-section">
          <p className="thesis-context-label">
            Plan
            {snapshot.plan.playbook_alignment ? (
              <span className="cognitive-playbook-badge">
                {" "}{snapshot.plan.playbook_alignment}
              </span>
            ) : null}
          </p>
          <p
            className="cognitive-snapshot-entry"
            title={snapshot.plan.entry_rationale}
          >
            <span className="cognitive-field-label">Entry: </span>
            {truncate(snapshot.plan.entry_rationale, 140)}
          </p>
          <p
            className="cognitive-snapshot-entry"
            title={snapshot.plan.stop_rationale}
          >
            <span className="cognitive-field-label">Stop: </span>
            {truncate(snapshot.plan.stop_rationale, 100)}
          </p>
        </div>
      ) : null}

      <BranchSummary branches={snapshot.scenario_branches} />

      <p className="cognitive-snapshot-authority">
        Derived from event payloads — not canonical truth.
      </p>
    </div>
  );
}
