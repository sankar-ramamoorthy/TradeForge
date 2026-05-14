import { AlertCircle, CheckCircle } from "lucide-react";
import { useEffect, useState } from "react";

import {
  fetchOperatingAttentionQueue,
  type OperatingAttentionQueue,
  type WorkspaceApiParams,
} from "../api/runtime";

type Props = {
  params: WorkspaceApiParams;
  onNavigateToOperating: () => void;
};

export function AttentionSummaryPanel({ params, onNavigateToOperating }: Props) {
  const [queue, setQueue] = useState<OperatingAttentionQueue | null>(null);

  useEffect(() => {
    if (!params.decision_id) {
      setQueue(null);
      return;
    }

    const controller = new AbortController();

    fetchOperatingAttentionQueue(params, controller.signal)
      .then(setQueue)
      .catch(() => {
        // fail silently — summary panel is advisory
      });

    return () => controller.abort();
  }, [params.decision_id, params.persona_id, params.workspace_id]);

  if (!params.decision_id || queue === null) return null;

  const { items } = queue;
  const totalCount = items.length;

  if (totalCount === 0) {
    return (
      <aside
        className="attention-summary-panel attention-summary-clear"
        aria-label="Attention queue state"
      >
        <CheckCircle aria-hidden="true" className="attention-summary-icon" />
        <span>Queue clear</span>
      </aside>
    );
  }

  const urgentCount = items.filter(
    (i) => i.priority_label === "critical" || i.priority_label === "high",
  ).length;
  const topItem = items[0];

  return (
    <aside
      className="attention-summary-panel"
      aria-label={`${totalCount} attention item${totalCount !== 1 ? "s" : ""} pending`}
    >
      <div className="attention-summary-header">
        <AlertCircle aria-hidden="true" className="attention-summary-icon" />
        <span className="attention-summary-count">
          {totalCount} pending item{totalCount !== 1 ? "s" : ""}
        </span>
        {urgentCount > 0 ? (
          <span className="attention-summary-urgent-badge">
            {urgentCount} urgent
          </span>
        ) : null}
      </div>

      {topItem ? (
        <p className="attention-summary-top">{topItem.explanation}</p>
      ) : null}

      <button
        className="attention-summary-link"
        onClick={onNavigateToOperating}
        type="button"
      >
        View full queue →
      </button>
    </aside>
  );
}
