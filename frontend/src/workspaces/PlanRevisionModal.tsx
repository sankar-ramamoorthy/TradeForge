import { useState, type FormEvent } from "react";
import { type TradePlanArtifact } from "../api/runtime";
import { type WorkspaceContext } from "../workspaceRouting";

type SubmitState = "idle" | "submitting" | "error";

type RevisePlanRequest = {
  decision_id: string;
  symbol: string;
  entry_rationale: string;
  stop_rationale: string;
  target_rationale: string;
  sizing_rationale: string;
  execution_assumptions: string[];
  playbook_alignment?: string;
  persona_id: string;
  workspace_id: string;
};

type RevisePlanResponse = {
  decision_id: string;
  event_type: string;
  timestamp: string;
  revision_number: number;
};

async function postRevisePlan(
  request: RevisePlanRequest,
  signal?: AbortSignal,
): Promise<RevisePlanResponse> {
  const response = await fetch("/lifecycle/decisions/revise-plan", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
    signal,
  });

  if (!response.ok) {
    const detail = await response.json().catch(() => null);
    const message =
      typeof detail === "object" && detail !== null && "detail" in detail
        ? typeof (detail as Record<string, unknown>).detail === "object"
          ? ((detail as Record<string, { message?: string }>).detail?.message ??
            `Plan revision failed: ${response.status}`)
          : `Plan revision failed: ${response.status}`
        : `Plan revision failed: ${response.status}`;
    throw new Error(message);
  }

  return response.json() as Promise<RevisePlanResponse>;
}

function ListInput({
  label,
  items,
  onChange,
  placeholder,
}: {
  label: string;
  items: string[];
  onChange: (items: string[]) => void;
  placeholder: string;
}) {
  function handleChange(index: number, value: string) {
    const next = [...items];
    next[index] = value;
    onChange(next);
  }

  function handleAdd() {
    onChange([...items, ""]);
  }

  function handleRemove(index: number) {
    onChange(items.filter((_, i) => i !== index));
  }

  return (
    <div className="thesis-list-input">
      <label className="thesis-field-label">{label}</label>
      {items.map((item, index) => (
        <div className="thesis-list-row" key={index}>
          <input
            aria-label={`${label} item ${index + 1}`}
            className="thesis-list-item-input"
            onChange={(e) => handleChange(index, e.target.value)}
            placeholder={placeholder}
            type="text"
            value={item}
          />
          {items.length > 1 ? (
            <button
              aria-label={`Remove ${label} item ${index + 1}`}
              className="thesis-list-remove-btn"
              onClick={() => handleRemove(index)}
              type="button"
            >
              ×
            </button>
          ) : null}
        </div>
      ))}
      <button className="thesis-list-add-btn" onClick={handleAdd} type="button">
        + Add
      </button>
    </div>
  );
}

type Props = {
  context: Required<WorkspaceContext>;
  symbol: string;
  currentPlan: TradePlanArtifact;
  onSuccess: () => void;
  onCancel: () => void;
};

export function PlanRevisionModal({
  context,
  symbol,
  currentPlan,
  onSuccess,
  onCancel,
}: Props) {
  const [entryRationale, setEntryRationale] = useState(currentPlan.entry_rationale);
  const [stopRationale, setStopRationale] = useState(currentPlan.stop_rationale);
  const [targetRationale, setTargetRationale] = useState(currentPlan.target_rationale);
  const [sizingRationale, setSizingRationale] = useState(currentPlan.sizing_rationale);
  const [executionAssumptions, setExecutionAssumptions] = useState<string[]>(
    currentPlan.execution_assumptions.length > 0
      ? [...currentPlan.execution_assumptions]
      : [""],
  );
  const [playbookAlignment, setPlaybookAlignment] = useState(
    currentPlan.playbook_alignment ?? "",
  );
  const [submitState, setSubmitState] = useState<SubmitState>("idle");
  const [submitError, setSubmitError] = useState<string | null>(null);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitState("submitting");
    setSubmitError(null);

    const cleanAssumptions = executionAssumptions.filter((a) => a.trim());

    if (!entryRationale.trim()) {
      setSubmitError("Entry rationale is required.");
      setSubmitState("error");
      return;
    }
    if (!stopRationale.trim()) {
      setSubmitError("Stop rationale is required.");
      setSubmitState("error");
      return;
    }
    if (!targetRationale.trim()) {
      setSubmitError("Target rationale is required.");
      setSubmitState("error");
      return;
    }
    if (!sizingRationale.trim()) {
      setSubmitError("Sizing rationale is required.");
      setSubmitState("error");
      return;
    }
    if (cleanAssumptions.length === 0) {
      setSubmitError("At least one execution assumption is required.");
      setSubmitState("error");
      return;
    }

    postRevisePlan({
      decision_id: context.decision_id,
      symbol,
      entry_rationale: entryRationale.trim(),
      stop_rationale: stopRationale.trim(),
      target_rationale: targetRationale.trim(),
      sizing_rationale: sizingRationale.trim(),
      execution_assumptions: cleanAssumptions,
      playbook_alignment: playbookAlignment.trim(),
      persona_id: context.persona_id,
      workspace_id: context.workspace_id,
    })
      .then(() => {
        setSubmitState("idle");
        onSuccess();
      })
      .catch((err: unknown) => {
        setSubmitState("error");
        setSubmitError(
          err instanceof Error ? err.message : "Plan revision failed.",
        );
      });
  }

  return (
    <div
      aria-labelledby="plan-revision-modal-title"
      aria-modal="true"
      className="thesis-modal-overlay"
      role="dialog"
    >
      <div className="thesis-modal-surface">
        <div className="thesis-modal-header">
          <div>
            <p className="eyebrow">Plan Revision — {symbol}</p>
            <h2 id="plan-revision-modal-title">Revise your execution plan</h2>
            <p className="thesis-modal-description">
              Update your plan rationale and assumptions. Each revision creates an
              immutable snapshot — the full evolution will be visible in replay.
            </p>
          </div>
          <button
            aria-label="Cancel plan revision"
            className="thesis-modal-close"
            onClick={onCancel}
            type="button"
          >
            ×
          </button>
        </div>

        <form className="thesis-modal-form" onSubmit={handleSubmit}>
          <div className="thesis-field-group">
            <label className="thesis-field-label" htmlFor="plan-revision-entry">
              Entry Rationale
              <span className="thesis-field-required" aria-hidden="true"> *</span>
            </label>
            <textarea
              className="thesis-narrative-input"
              id="plan-revision-entry"
              onChange={(e) => setEntryRationale(e.target.value)}
              placeholder="Why this entry point and price level — what confirms the setup…"
              required
              rows={3}
              value={entryRationale}
            />
          </div>

          <div className="thesis-field-group">
            <label className="thesis-field-label" htmlFor="plan-revision-stop">
              Stop Rationale
              <span className="thesis-field-required" aria-hidden="true"> *</span>
            </label>
            <textarea
              className="thesis-narrative-input"
              id="plan-revision-stop"
              onChange={(e) => setStopRationale(e.target.value)}
              placeholder="Why this stop level represents thesis invalidation — not arbitrary…"
              required
              rows={3}
              value={stopRationale}
            />
          </div>

          <div className="thesis-field-group">
            <label className="thesis-field-label" htmlFor="plan-revision-target">
              Target Rationale
              <span className="thesis-field-required" aria-hidden="true"> *</span>
            </label>
            <textarea
              className="thesis-narrative-input"
              id="plan-revision-target"
              onChange={(e) => setTargetRationale(e.target.value)}
              placeholder="Why this target represents thesis fulfillment at an acceptable risk/reward…"
              required
              rows={3}
              value={targetRationale}
            />
          </div>

          <div className="thesis-field-group">
            <label className="thesis-field-label" htmlFor="plan-revision-sizing">
              Sizing Rationale
              <span className="thesis-field-required" aria-hidden="true"> *</span>
            </label>
            <textarea
              className="thesis-narrative-input"
              id="plan-revision-sizing"
              onChange={(e) => setSizingRationale(e.target.value)}
              placeholder="How position size was determined relative to conviction and risk tolerance…"
              required
              rows={3}
              value={sizingRationale}
            />
          </div>

          <ListInput
            items={executionAssumptions}
            label="Execution Assumptions *"
            onChange={setExecutionAssumptions}
            placeholder="e.g. Sufficient liquidity available at entry"
          />

          <div className="thesis-field-group">
            <label className="thesis-field-label" htmlFor="plan-revision-playbook">
              Playbook Alignment
              <span className="thesis-field-optional"> (optional)</span>
            </label>
            <input
              className="thesis-regime-input"
              id="plan-revision-playbook"
              onChange={(e) => setPlaybookAlignment(e.target.value)}
              placeholder="e.g. swing-breakout-v1"
              type="text"
              value={playbookAlignment}
            />
          </div>

          {submitError ? (
            <div className="runtime-error" role="alert">
              {submitError}
            </div>
          ) : null}

          <div className="thesis-modal-actions">
            <button
              className="lifecycle-action-btn-secondary"
              onClick={onCancel}
              type="button"
            >
              Cancel
            </button>
            <button
              className="lifecycle-action-btn"
              disabled={submitState === "submitting"}
              type="submit"
            >
              {submitState === "submitting" ? "Saving revision…" : "Save Revision"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
