import { useState, type FormEvent } from "react";
import { postCreateScenarioBranch, type ScenarioBranchType } from "../api/runtime";
import { type WorkspaceContext } from "../workspaceRouting";

type SubmitState = "idle" | "submitting" | "error";

const BRANCH_TYPE_OPTIONS: { value: ScenarioBranchType; label: string; description: string }[] = [
  {
    value: "primary",
    label: "Primary",
    description: "The main expected outcome if the thesis plays out",
  },
  {
    value: "alternative",
    label: "Alternative",
    description: "Another plausible outcome the operator should prepare for",
  },
  {
    value: "invalidation",
    label: "Invalidation",
    description: "What would definitively prove the thesis wrong",
  },
  {
    value: "regime_transition",
    label: "Regime Transition",
    description: "How a market regime change would affect this trade",
  },
];

const CONFIDENCE_LABELS: Record<number, string> = {
  1: "Unlikely", 2: "Possible", 3: "Likely", 4: "Probable", 5: "Expected",
};

type Props = {
  context: Required<WorkspaceContext>;
  onSuccess: () => void;
  onCancel: () => void;
};

export function ScenarioBranchModal({ context, onSuccess, onCancel }: Props) {
  const [branchType, setBranchType] = useState<ScenarioBranchType>("primary");
  const [condition, setCondition] = useState("");
  const [implication, setImplication] = useState("");
  const [confidence, setConfidence] = useState(3);
  const [notes, setNotes] = useState("");
  const [submitState, setSubmitState] = useState<SubmitState>("idle");
  const [submitError, setSubmitError] = useState<string | null>(null);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitState("submitting");
    setSubmitError(null);

    if (!condition.trim()) {
      setSubmitError("Condition is required.");
      setSubmitState("error");
      return;
    }
    if (!implication.trim()) {
      setSubmitError("Implication is required.");
      setSubmitState("error");
      return;
    }

    postCreateScenarioBranch({
      decision_id: context.decision_id,
      branch_type: branchType,
      condition: condition.trim(),
      implication: implication.trim(),
      confidence,
      notes: notes.trim(),
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
          err instanceof Error ? err.message : "Scenario branch creation failed.",
        );
      });
  }

  const selectedType = BRANCH_TYPE_OPTIONS.find((o) => o.value === branchType);

  return (
    <div
      aria-labelledby="scenario-modal-title"
      aria-modal="true"
      className="thesis-modal-overlay"
      role="dialog"
    >
      <div className="thesis-modal-surface">
        <div className="thesis-modal-header">
          <div>
            <p className="eyebrow">Scenario Branch</p>
            <h2 id="scenario-modal-title">Define a conditional reasoning pathway</h2>
            <p className="thesis-modal-description">
              Capture "if X then Y" reasoning before planning. Scenario branches
              make conditional thinking explicit and replayable.
            </p>
          </div>
          <button
            aria-label="Cancel scenario branch"
            className="thesis-modal-close"
            onClick={onCancel}
            type="button"
          >
            ×
          </button>
        </div>

        <form className="thesis-modal-form" onSubmit={handleSubmit}>
          <div className="thesis-field-group">
            <label className="thesis-field-label" htmlFor="scenario-branch-type">
              Branch Type
              <span className="thesis-field-required" aria-hidden="true"> *</span>
            </label>
            {selectedType ? (
              <p className="thesis-field-hint">{selectedType.description}</p>
            ) : null}
            <select
              className="thesis-regime-input"
              id="scenario-branch-type"
              onChange={(e) => setBranchType(e.target.value as ScenarioBranchType)}
              value={branchType}
            >
              {BRANCH_TYPE_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>

          <div className="thesis-field-group">
            <label className="thesis-field-label" htmlFor="scenario-condition">
              Condition
              <span className="thesis-field-required" aria-hidden="true"> *</span>
            </label>
            <p className="thesis-field-hint">
              What triggers this branch — the specific market or price condition.
            </p>
            <textarea
              className="thesis-narrative-input"
              id="scenario-condition"
              onChange={(e) => setCondition(e.target.value)}
              placeholder="e.g. Price closes above $185 on above-average volume..."
              required
              rows={3}
              value={condition}
            />
          </div>

          <div className="thesis-field-group">
            <label className="thesis-field-label" htmlFor="scenario-implication">
              Implication
              <span className="thesis-field-required" aria-hidden="true"> *</span>
            </label>
            <p className="thesis-field-hint">
              What you would do if this condition occurs.
            </p>
            <textarea
              className="thesis-narrative-input"
              id="scenario-implication"
              onChange={(e) => setImplication(e.target.value)}
              placeholder="e.g. Hold full position, raise stop to breakeven, target $200..."
              required
              rows={3}
              value={implication}
            />
          </div>

          <div className="thesis-field-group">
            <label className="thesis-field-label" htmlFor="scenario-confidence">
              Likelihood: {CONFIDENCE_LABELS[confidence] ?? confidence} ({confidence}/5)
            </label>
            <input
              className="thesis-confidence-slider"
              id="scenario-confidence"
              max={5}
              min={1}
              onChange={(e) => setConfidence(Number(e.target.value))}
              step={1}
              type="range"
              value={confidence}
            />
            <div className="thesis-confidence-scale" aria-hidden="true">
              <span>Unlikely</span>
              <span>Expected</span>
            </div>
          </div>

          <div className="thesis-field-group">
            <label className="thesis-field-label" htmlFor="scenario-notes">
              Notes
              <span className="thesis-field-optional"> (optional)</span>
            </label>
            <input
              className="thesis-regime-input"
              id="scenario-notes"
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Additional context or rationale for this branch..."
              type="text"
              value={notes}
            />
          </div>

          {submitError ? (
            <div className="runtime-error" role="alert">{submitError}</div>
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
              {submitState === "submitting" ? "Adding branch…" : "Add Scenario Branch"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
