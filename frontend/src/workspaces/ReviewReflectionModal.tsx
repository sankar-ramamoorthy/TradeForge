import { useState, type FormEvent } from "react";
import { postCompleteReview } from "../api/runtime";
import { type WorkspaceContext } from "../workspaceRouting";

type SubmitState = "idle" | "submitting" | "error";

const QUALITY_LABELS: Record<number, string> = {
  1: "Poor", 2: "Below average", 3: "Adequate", 4: "Good", 5: "Excellent",
};

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
              onClick={() => onChange(items.filter((_, i) => i !== index))}
              type="button"
            >
              ×
            </button>
          ) : null}
        </div>
      ))}
      <button
        className="thesis-list-add-btn"
        onClick={() => onChange([...items, ""])}
        type="button"
      >
        + Add
      </button>
    </div>
  );
}

function QualitySlider({
  id,
  label,
  hint,
  value,
  onChange,
}: {
  id: string;
  label: string;
  hint: string;
  value: number;
  onChange: (v: number) => void;
}) {
  return (
    <div className="thesis-field-group">
      <label className="thesis-field-label" htmlFor={id}>
        {label}: {QUALITY_LABELS[value] ?? value} ({value}/5)
        <span className="thesis-field-required" aria-hidden="true"> *</span>
      </label>
      <p className="thesis-field-hint">{hint}</p>
      <input
        className="thesis-confidence-slider"
        id={id}
        max={5}
        min={1}
        onChange={(e) => onChange(Number(e.target.value))}
        step={1}
        type="range"
        value={value}
      />
      <div className="thesis-confidence-scale" aria-hidden="true">
        <span>Poor</span>
        <span>Excellent</span>
      </div>
    </div>
  );
}

export function ReviewReflectionModal({ context, symbol, onSuccess, onCancel }: Props) {
  const [thesisVsOutcome, setThesisVsOutcome] = useState("");
  const [decisionQuality, setDecisionQuality] = useState(3);
  const [executionQuality, setExecutionQuality] = useState(3);
  const [disciplineObservations, setDisciplineObservations] = useState("");
  const [lessonsLearned, setLessonsLearned] = useState<string[]>([""]);
  const [behavioralObservations, setBehavioralObservations] = useState("");
  const [submitState, setSubmitState] = useState<SubmitState>("idle");
  const [submitError, setSubmitError] = useState<string | null>(null);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitState("submitting");
    setSubmitError(null);

    const cleanLessons = lessonsLearned.filter((l) => l.trim());

    if (!thesisVsOutcome.trim()) {
      setSubmitError("Thesis vs outcome comparison is required.");
      setSubmitState("error");
      return;
    }
    if (!disciplineObservations.trim()) {
      setSubmitError("Discipline observations are required.");
      setSubmitState("error");
      return;
    }
    if (cleanLessons.length === 0) {
      setSubmitError("At least one lesson learned is required.");
      setSubmitState("error");
      return;
    }

    postCompleteReview({
      decision_id: context.decision_id,
      symbol,
      thesis_vs_outcome: thesisVsOutcome.trim(),
      decision_quality: decisionQuality,
      execution_quality: executionQuality,
      discipline_observations: disciplineObservations.trim(),
      lessons_learned: cleanLessons,
      behavioral_observations: behavioralObservations.trim(),
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
          err instanceof Error ? err.message : "Review completion failed.",
        );
      });
  }

  return (
    <div
      aria-labelledby="review-modal-title"
      aria-modal="true"
      className="thesis-modal-overlay"
      role="dialog"
    >
      <div className="thesis-modal-surface">
        <div className="thesis-modal-header">
          <div>
            <p className="eyebrow">Review Reflection — {symbol}</p>
            <h2 id="review-modal-title">Record your review</h2>
            <p className="thesis-modal-description">
              Capture what happened, how the process held up, and what you learned.
              This becomes a durable replayable learning artifact.
            </p>
          </div>
          <button
            aria-label="Cancel review"
            className="thesis-modal-close"
            onClick={onCancel}
            type="button"
          >
            ×
          </button>
        </div>

        <form className="thesis-modal-form" onSubmit={handleSubmit}>
          <div className="thesis-field-group">
            <label className="thesis-field-label" htmlFor="review-thesis-vs-outcome">
              Thesis vs Outcome
              <span className="thesis-field-required" aria-hidden="true"> *</span>
            </label>
            <p className="thesis-field-hint">
              What actually happened compared to what you originally expected.
              Separate the market outcome from your process quality.
            </p>
            <textarea
              className="thesis-narrative-input"
              id="review-thesis-vs-outcome"
              onChange={(e) => setThesisVsOutcome(e.target.value)}
              placeholder="e.g. The thesis held — accumulation pattern resolved higher as expected.
Market remained risk-on. Target reached within 3 weeks..."
              required
              rows={4}
              value={thesisVsOutcome}
            />
          </div>

          <QualitySlider
            hint="How sound was your reasoning process — independent of whether the trade worked."
            id="review-decision-quality"
            label="Decision Quality"
            onChange={setDecisionQuality}
            value={decisionQuality}
          />

          <QualitySlider
            hint="How well did you follow the stated plan — independent of PnL."
            id="review-execution-quality"
            label="Execution Quality"
            onChange={setExecutionQuality}
            value={executionQuality}
          />

          <div className="thesis-field-group">
            <label className="thesis-field-label" htmlFor="review-discipline">
              Discipline Observations
              <span className="thesis-field-required" aria-hidden="true"> *</span>
            </label>
            <p className="thesis-field-hint">
              Notes on process adherence, stop discipline, and plan execution.
            </p>
            <textarea
              className="thesis-narrative-input"
              id="review-discipline"
              onChange={(e) => setDisciplineObservations(e.target.value)}
              placeholder="e.g. Held to the plan. Did not move the stop prematurely. Exited at the stated target..."
              required
              rows={3}
              value={disciplineObservations}
            />
          </div>

          <ListInput
            items={lessonsLearned}
            label="Lessons Learned *"
            onChange={setLessonsLearned}
            placeholder="e.g. Wait for the close above resistance before entering"
          />

          <div className="thesis-field-group">
            <label className="thesis-field-label" htmlFor="review-behavioral">
              Behavioral Observations
              <span className="thesis-field-optional"> (optional)</span>
            </label>
            <p className="thesis-field-hint">
              Patterns or tendencies you noticed in your own behavior.
            </p>
            <textarea
              className="thesis-narrative-input"
              id="review-behavioral"
              onChange={(e) => setBehavioralObservations(e.target.value)}
              placeholder="e.g. Tendency to take profits early — resisted this time..."
              rows={2}
              value={behavioralObservations}
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
              {submitState === "submitting" ? "Recording review…" : "Complete Review"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
