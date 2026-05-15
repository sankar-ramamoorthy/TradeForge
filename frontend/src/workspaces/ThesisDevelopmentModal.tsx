import { useState, type FormEvent } from "react";
import { postDevelopThesis } from "../api/runtime";
import { type WorkspaceContext } from "../workspaceRouting";

type SubmitState = "idle" | "submitting" | "error";

type Props = {
  context: Required<WorkspaceContext>;
  symbol: string;
  onSuccess: (decisionId: string) => void;
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
      <button
        className="thesis-list-add-btn"
        onClick={handleAdd}
        type="button"
      >
        + Add
      </button>
    </div>
  );
}

export function ThesisDevelopmentModal({ context, symbol, onSuccess, onCancel }: Props) {
  const [narrative, setNarrative] = useState("");
  const [catalysts, setCatalysts] = useState<string[]>([""]);
  const [assumptions, setAssumptions] = useState<string[]>([""]);
  const [invalidationConditions, setInvalidationConditions] = useState<string[]>([""]);
  const [confidenceLevel, setConfidenceLevel] = useState<number>(3);
  const [regimeAlignment, setRegimeAlignment] = useState("");
  const [submitState, setSubmitState] = useState<SubmitState>("idle");
  const [submitError, setSubmitError] = useState<string | null>(null);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitState("submitting");
    setSubmitError(null);

    const cleanCatalysts = catalysts.filter((c) => c.trim());
    const cleanAssumptions = assumptions.filter((a) => a.trim());
    const cleanInvalidation = invalidationConditions.filter((i) => i.trim());

    if (!narrative.trim()) {
      setSubmitError("Thesis narrative is required.");
      setSubmitState("error");
      return;
    }
    if (cleanCatalysts.length === 0) {
      setSubmitError("At least one catalyst is required.");
      setSubmitState("error");
      return;
    }
    if (cleanAssumptions.length === 0) {
      setSubmitError("At least one assumption is required.");
      setSubmitState("error");
      return;
    }
    if (cleanInvalidation.length === 0) {
      setSubmitError("At least one invalidation condition is required.");
      setSubmitState("error");
      return;
    }

    postDevelopThesis({
      decision_id: context.decision_id,
      symbol,
      narrative: narrative.trim(),
      catalysts: cleanCatalysts,
      assumptions: cleanAssumptions,
      invalidation_conditions: cleanInvalidation,
      confidence_level: confidenceLevel,
      regime_alignment: regimeAlignment.trim(),
      persona_id: context.persona_id,
      workspace_id: context.workspace_id,
    })
      .then((response) => {
        setSubmitState("idle");
        onSuccess(response.decision_id);
      })
      .catch((err: unknown) => {
        setSubmitState("error");
        setSubmitError(
          err instanceof Error ? err.message : "Thesis development failed.",
        );
      });
  }

  const CONFIDENCE_LABELS: Record<number, string> = {
    1: "Speculative",
    2: "Low",
    3: "Moderate",
    4: "High",
    5: "Conviction",
  };

  return (
    <div
      aria-labelledby="thesis-modal-title"
      aria-modal="true"
      className="thesis-modal-overlay"
      role="dialog"
    >
      <div className="thesis-modal-surface">
        <div className="thesis-modal-header">
          <div>
            <p className="eyebrow">Thesis Development — {symbol}</p>
            <h2 id="thesis-modal-title">Define your thesis</h2>
            <p className="thesis-modal-description">
              Capture the structured reasoning behind this idea. This becomes
              a replayable cognitive artifact attached to the lifecycle event.
            </p>
          </div>
          <button
            aria-label="Cancel thesis development"
            className="thesis-modal-close"
            onClick={onCancel}
            type="button"
          >
            ×
          </button>
        </div>

        <form className="thesis-modal-form" onSubmit={handleSubmit}>
          <div className="thesis-field-group">
            <label className="thesis-field-label" htmlFor="thesis-narrative">
              Thesis Narrative
              <span className="thesis-field-required" aria-hidden="true"> *</span>
            </label>
            <p className="thesis-field-hint">
              The core argument for why this idea has merit.
            </p>
            <textarea
              className="thesis-narrative-input"
              id="thesis-narrative"
              onChange={(e) => setNarrative(e.target.value)}
              placeholder="e.g. AAPL is testing the 200-day MA with strong institutional accumulation visible in the tape..."
              required
              rows={6}
              value={narrative}
            />
          </div>

          <ListInput
            items={catalysts}
            label="Catalysts *"
            onChange={setCatalysts}
            placeholder="e.g. Strong earnings guidance"
          />

          <ListInput
            items={assumptions}
            label="Assumptions *"
            onChange={setAssumptions}
            placeholder="e.g. Market remains risk-on"
          />

          <ListInput
            items={invalidationConditions}
            label="Invalidation Conditions *"
            onChange={setInvalidationConditions}
            placeholder="e.g. Break below 200-day MA on volume"
          />

          <div className="thesis-field-group">
            <label className="thesis-field-label" htmlFor="thesis-confidence">
              Conviction Level: {CONFIDENCE_LABELS[confidenceLevel]} ({confidenceLevel}/5)
            </label>
            <input
              className="thesis-confidence-slider"
              id="thesis-confidence"
              max={5}
              min={1}
              onChange={(e) => setConfidenceLevel(Number(e.target.value))}
              step={1}
              type="range"
              value={confidenceLevel}
            />
            <div className="thesis-confidence-scale" aria-hidden="true">
              <span>Speculative</span>
              <span>Conviction</span>
            </div>
          </div>

          <div className="thesis-field-group">
            <label className="thesis-field-label" htmlFor="thesis-regime">
              Regime Alignment
              <span className="thesis-field-optional"> (optional)</span>
            </label>
            <p className="thesis-field-hint">
              Market regime context at time of thesis formation.
            </p>
            <input
              className="thesis-regime-input"
              id="thesis-regime"
              onChange={(e) => setRegimeAlignment(e.target.value)}
              placeholder="e.g. risk-on momentum, range-bound, post-correction"
              type="text"
              value={regimeAlignment}
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
              {submitState === "submitting"
                ? "Creating thesis…"
                : "Develop Thesis"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
