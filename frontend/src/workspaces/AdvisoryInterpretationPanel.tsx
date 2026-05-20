import { BrainCircuit } from "lucide-react";
import { useEffect, useState } from "react";

import {
  fetchAdvisoryInterpretations,
  type AdvisoryInterpretation,
} from "../api/runtime";
import { type WorkspaceContext } from "../workspaceRouting";

type AdvisoryInterpretationPanelProps = {
  context: Required<WorkspaceContext>;
  title?: string;
};

const LABELS: Record<string, string> = {
  conflict_analysis: "Conflict",
  contextual_meaning: "Context",
  drift_signal: "Drift",
  probabilistic_summary: "Probabilistic",
  thesis_influence: "Thesis",
};

function label(value: string): string {
  return LABELS[value] ?? value.replace(/_/g, " ");
}

export function AdvisoryInterpretationPanel({
  context,
  title = "Advisory interpretations",
}: AdvisoryInterpretationPanelProps) {
  const [interpretations, setInterpretations] = useState<
    AdvisoryInterpretation[]
  >([]);
  const [loadError, setLoadError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    fetchAdvisoryInterpretations(
      {
        persona_id: context.persona_id,
        workspace_id: context.workspace_id,
        decision_id: context.decision_id || undefined,
      },
      controller.signal,
    )
      .then((result) => {
        setInterpretations(result.interpretations);
        setLoadError(null);
      })
      .catch((error: unknown) => {
        if (error instanceof DOMException && error.name === "AbortError") return;
        setLoadError(
          error instanceof Error
            ? error.message
            : "Advisory interpretations failed to load",
        );
      });
    return () => controller.abort();
  }, [context.persona_id, context.workspace_id, context.decision_id]);

  return (
    <section className="advisory-interpretation-panel" aria-label={title}>
      <div className="advisory-interpretation-heading">
        <BrainCircuit aria-hidden="true" />
        <div>
          <p className="eyebrow">Advisory / Non-canonical</p>
          <h2>{title}</h2>
        </div>
      </div>

      {loadError ? <div className="runtime-error">{loadError}</div> : null}

      {interpretations.length === 0 ? (
        <p className="field-no-data">
          No accepted interpretations are linked to this context yet.
        </p>
      ) : (
        <div className="advisory-interpretation-list">
          {interpretations.map((item) => (
            <article
              className="advisory-interpretation-item"
              key={item.interpretation_id}
            >
              <div className="advisory-interpretation-meta">
                <span>{label(item.interpretation_kind)}</span>
                <span>Influence: {label(item.thesis_influence)}</span>
                <span>Weight: {label(item.contextual_weight)}</span>
                <span>Confidence: {label(item.confidence_range)}</span>
              </div>
              <p className="advisory-interpretation-content">
                {item.content}
              </p>
              <p className="advisory-interpretation-rationale">
                {item.rationale}
              </p>
              <div className="advisory-interpretation-footer">
                <span>{item.provenance_summary}</span>
                <span>
                  {item.observation_ids.length} linked observation
                  {item.observation_ids.length !== 1 ? "s" : ""}
                </span>
              </div>
              {item.caveats.length > 0 ? (
                <ul className="advisory-caveat-list">
                  {item.caveats.map((caveat) => (
                    <li key={caveat}>{caveat}</li>
                  ))}
                </ul>
              ) : null}
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
