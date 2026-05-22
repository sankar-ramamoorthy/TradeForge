import { Eye, Lightbulb, X } from "lucide-react";
import { useEffect, useState } from "react";

import {
  fetchCandidateReviewQueue,
  type AdvisoryCandidate,
  type CandidateReviewQueue,
} from "../api/runtime";
import { type WorkspaceContext } from "../workspaceRouting";

type CandidateReviewQueuePanelProps = {
  context: Required<WorkspaceContext>;
  onBeginPromotion: (candidate: AdvisoryCandidate) => void;
};

export function CandidateReviewQueuePanel({
  context,
  onBeginPromotion,
}: CandidateReviewQueuePanelProps) {
  const [queue, setQueue] = useState<CandidateReviewQueue | null>(null);
  const [expandedCandidateId, setExpandedCandidateId] = useState<string | null>(null);
  const [dismissedCandidateIds, setDismissedCandidateIds] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    fetchCandidateReviewQueue(
      {
        persona_id: context.persona_id,
        workspace_id: context.workspace_id,
        dismissed_candidate_ids: dismissedCandidateIds,
      },
      controller.signal,
    )
      .then((data) => {
        setQueue(data);
        setError(null);
      })
      .catch((err: unknown) => {
        if (err instanceof DOMException && err.name === "AbortError") return;
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load advisory candidates",
        );
      });
    return () => controller.abort();
  }, [context.persona_id, context.workspace_id, dismissedCandidateIds]);

  function dismiss(candidateId: string) {
    setDismissedCandidateIds((current) =>
      current.includes(candidateId) ? current : [...current, candidateId],
    );
    setExpandedCandidateId((current) => (current === candidateId ? null : current));
  }

  return (
    <section className="panel-block" aria-labelledby="candidate-review-title">
      <div className="panel-heading">
        <Lightbulb aria-hidden="true" />
        <div>
          <p className="eyebrow">Advisory Candidate Queue</p>
          <h2 id="candidate-review-title">Review surfaced setups</h2>
        </div>
      </div>

      {error ? <div className="runtime-error">{error}</div> : null}

      {queue && queue.candidates.length === 0 ? (
        <p className="empty-state">
          No advisory candidates are waiting in this workspace.
        </p>
      ) : null}

      {queue?.candidates.map((candidate) => {
        const expanded = expandedCandidateId === candidate.candidate_id;
        return (
          <article className="attention-item" key={candidate.candidate_id}>
            <div className="attention-item-header">
              <div>
                <span className="stage-badge stage-idea">{candidate.symbol}</span>
                <h3>{candidate.summary}</h3>
              </div>
              <span className="field-authority-badge authority-advisory">
                Advisory
              </span>
            </div>
            <p>{candidate.rationale}</p>
            <p className="projection-detail">
              {candidate.capture_origin.replace(/_/g, " ")} - uncertainty{" "}
              {candidate.uncertainty_band}
            </p>
            <div className="decision-actions">
              <button
                className="btn-secondary"
                onClick={() =>
                  setExpandedCandidateId(expanded ? null : candidate.candidate_id)
                }
                type="button"
              >
                <Eye aria-hidden="true" />
                {expanded ? "Hide Details" : "Inspect"}
              </button>
              <button
                className="btn-secondary"
                onClick={() => dismiss(candidate.candidate_id)}
                type="button"
              >
                <X aria-hidden="true" />
                Dismiss
              </button>
              <button
                className="btn-primary"
                onClick={() => onBeginPromotion(candidate)}
                type="button"
              >
                Start Workflow
              </button>
            </div>
            {expanded ? (
              <div className="field-surfaces-grid">
                <div className="field-surface" data-authority="advisory">
                  <div className="field-surface-header">
                    <span className="field-surface-name">Provenance</span>
                    <span className="field-authority-badge authority-advisory">
                      Advisory
                    </span>
                  </div>
                  <p className="field-surface-desc">
                    {candidate.provenance_summary}
                  </p>
                  <div className="source-event-types">
                    <code className="event-type-tag">
                      candidate: {candidate.candidate_id}
                    </code>
                    <code className="event-type-tag">
                      artifact event: {candidate.canonical_event_type}
                    </code>
                    <code className="event-type-tag">
                      captured: {new Date(candidate.captured_at).toLocaleString()}
                    </code>
                  </div>
                  {candidate.caveats.map((caveat) => (
                    <p className="authority-boundary" key={caveat}>
                      {caveat}
                    </p>
                  ))}
                </div>
                <div className="field-surface" data-authority="derived">
                  <div className="field-surface-header">
                    <span className="field-surface-name">Evidence</span>
                    <span className="field-authority-badge authority-derived">
                      Derived
                    </span>
                  </div>
                  <div className="source-event-types">
                    {candidate.evidence.map((evidence) => (
                      <code className="event-type-tag" key={evidence.evidence_id}>
                        {evidence.source_kind}: {evidence.source_id}
                        {evidence.artifact_id ? ` / ${evidence.artifact_id}` : ""}
                      </code>
                    ))}
                  </div>
                  <p className="field-surface-desc">
                    Provenance is read-only advisory context. It does not include
                    scores, execution authority, or lifecycle commands.
                  </p>
                </div>
              </div>
            ) : null}
          </article>
        );
      })}
    </section>
  );
}
