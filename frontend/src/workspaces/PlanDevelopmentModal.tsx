import { useState, type FormEvent } from "react";
import { postCreatePlan } from "../api/runtime";
import { type WorkspaceContext } from "../workspaceRouting";

type SubmitState = "idle" | "submitting" | "error";

type Props = {
  context: Required<WorkspaceContext>;
  symbol: string;
  onSuccess: () => void;
  onCancel: () => void;
};

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

function RationaleField({
  id,
  label,
  hint,
  placeholder,
  value,
  onChange,
}: {
  id: string;
  label: string;
  hint: string;
  placeholder: string;
  value: string;
  onChange: (v: string) => void;
}) {
  return (
    <div className="thesis-field-group">
      <label className="thesis-field-label" htmlFor={id}>
        {label}
        <span className="thesis-field-required" aria-hidden="true"> *</span>
      </label>
      <p className="thesis-field-hint">{hint}</p>
      <textarea
        className="thesis-narrative-input"
        id={id}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        required
        rows={3}
        value={value}
      />
    </div>
  );
}

export function PlanDevelopmentModal({ context, symbol, onSuccess, onCancel }: Props) {
  const [entryRationale, setEntryRationale] = useState("");
  const [stopRationale, setStopRationale] = useState("");
  const [targetRationale, setTargetRationale] = useState("");
  const [sizingRationale, setSizingRationale] = useState("");
  const [executionAssumptions, setExecutionAssumptions] = useState<string[]>([""]);
  const [playbookAlignment, setPlaybookAlignment] = useState("");
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

    postCreatePlan({
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
          err instanceof Error ? err.message : "Plan creation failed.",
        );
      });
  }

  return (
    <div
      aria-labelledby="plan-modal-title"
      aria-modal="true"
      className="thesis-modal-overlay"
      role="dialog"
    >
      <div className="thesis-modal-surface">
        <div className="thesis-modal-header">
          <div>
            <p className="eyebrow">Trade Plan — {symbol}</p>
            <h2 id="plan-modal-title">Define your execution plan</h2>
            <p className="thesis-modal-description">
              Capture structured execution intent before moving to approval.
              This becomes a replayable cognitive artifact attached to the Plan event.
            </p>
          </div>
          <button
            aria-label="Cancel plan creation"
            className="thesis-modal-close"
            onClick={onCancel}
            type="button"
          >
            ×
          </button>
        </div>

        <form className="thesis-modal-form" onSubmit={handleSubmit}>
          <RationaleField
            hint="Why this entry point and price level — what confirms the setup."
            id="plan-entry"
            label="Entry Rationale"
            onChange={setEntryRationale}
            placeholder="e.g. Buy on a pullback to the 20-day MA with a close above prior resistance..."
            value={entryRationale}
          />

          <RationaleField
            hint="Why this stop level represents thesis invalidation — not arbitrary."
            id="plan-stop"
            label="Stop Rationale"
            onChange={setStopRationale}
            placeholder="e.g. Close below the 200-day MA on above-average volume invalidates the breakout..."
            value={stopRationale}
          />

          <RationaleField
            hint="Why this target represents thesis fulfillment at an acceptable risk/reward."
            id="plan-target"
            label="Target Rationale"
            onChange={setTargetRationale}
            placeholder="e.g. Prior resistance at $200 gives a 2:1 risk/reward at this entry..."
            value={targetRationale}
          />

          <RationaleField
            hint="How position size was determined relative to conviction and risk tolerance."
            id="plan-sizing"
            label="Sizing Rationale"
            onChange={setSizingRationale}
            placeholder="e.g. 2% portfolio risk at the stop distance gives approximately 150 shares..."
            value={sizingRationale}
          />

          <ListInput
            items={executionAssumptions}
            label="Execution Assumptions *"
            onChange={setExecutionAssumptions}
            placeholder="e.g. Sufficient liquidity available at entry level"
          />

          <div className="thesis-field-group">
            <label className="thesis-field-label" htmlFor="plan-playbook">
              Playbook Alignment
              <span className="thesis-field-optional"> (optional)</span>
            </label>
            <p className="thesis-field-hint">
              Which operational playbook this plan follows.
            </p>
            <input
              className="thesis-regime-input"
              id="plan-playbook"
              onChange={(e) => setPlaybookAlignment(e.target.value)}
              placeholder="e.g. swing-breakout-v1, mean-reversion, sector-rotation"
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
              {submitState === "submitting" ? "Creating plan…" : "Create Plan"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
