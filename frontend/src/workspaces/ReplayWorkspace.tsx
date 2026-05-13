import { History } from "lucide-react";
import { type MouseEvent, useEffect, useState } from "react";

import {
  fetchReplayTimeline,
  fetchWorkspaceProjection,
  type ReplayTimeline,
  type ReplayTimelineEntry,
  type WorkspaceApiParams,
  type WorkspaceProjection,
} from "../api/runtime";
import { type WorkspaceContext } from "../workspaceRouting";

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
  execution: "Execution",
  review: "Review",
  system: "System",
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

function TimelineEntryRow({ entry }: { entry: ReplayTimelineEntry }) {
  const kindLabel = KIND_LABELS[entry.kind] ?? entry.kind;
  const ts = new Date(entry.timestamp).toLocaleString(undefined, {
    dateStyle: "short",
    timeStyle: "medium",
  });

  return (
    <li
      className="timeline-entry"
      data-kind={entry.kind}
      aria-label={`${kindLabel}: ${entry.event_type}`}
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
    </li>
  );
}

type ReplayWorkspaceProps = {
  context: Required<WorkspaceContext>;
  onNavigate: (event: MouseEvent<HTMLAnchorElement>, href: string) => void;
};

export function ReplayWorkspace({ context }: ReplayWorkspaceProps) {
  const [projection, setProjection] = useState<WorkspaceProjection | null>(null);
  const [timeline, setTimeline] = useState<ReplayTimeline | null>(null);
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

    return () => controller.abort();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [
    context.persona_id,
    context.persona_version,
    context.workspace_id,
    context.selected_workflow_id,
    context.decision_id,
  ]);

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
            <ol className="timeline-entries" aria-label="Replay timeline">
              {timeline.entries.map((entry) => (
                <TimelineEntryRow
                  entry={entry}
                  key={`${entry.source_sequence}-${entry.event_type}`}
                />
              ))}
            </ol>
          )}

          <p className="timeline-authority-note">
            {timeline.authority} — reconstructed from event ledger, not live APIs.
          </p>
        </div>
      ) : null}

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
