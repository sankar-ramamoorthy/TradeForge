import { useState, type FormEvent } from "react";
import { postCreateAnnotation, type AnnotationType } from "../api/runtime";
import { type WorkspaceContext } from "../workspaceRouting";

type SubmitState = "idle" | "submitting" | "error";

const ANNOTATION_TYPE_OPTIONS: {
  value: AnnotationType;
  label: string;
  description: string;
}[] = [
  {
    value: "observation",
    label: "Observation",
    description: "A neutral factual note about what happened at this event",
  },
  {
    value: "question",
    label: "Question",
    description: "Something you want to explore or understand in future review",
  },
  {
    value: "insight",
    label: "Insight",
    description: "A realization or learning derived from this event",
  },
  {
    value: "postmortem",
    label: "Postmortem",
    description: "Reflection on what could have been done better",
  },
];

type Props = {
  context: Required<WorkspaceContext>;
  sequence: number;
  eventType: string;
  onSuccess: () => void;
  onCancel: () => void;
};

export function AnnotationModal({
  context,
  sequence,
  eventType,
  onSuccess,
  onCancel,
}: Props) {
  const [annotationType, setAnnotationType] = useState<AnnotationType>("observation");
  const [note, setNote] = useState("");
  const [submitState, setSubmitState] = useState<SubmitState>("idle");
  const [submitError, setSubmitError] = useState<string | null>(null);

  const selectedOption = ANNOTATION_TYPE_OPTIONS.find(
    (o) => o.value === annotationType,
  );

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitState("submitting");
    setSubmitError(null);

    if (!note.trim()) {
      setSubmitError("Note is required.");
      setSubmitState("error");
      return;
    }

    postCreateAnnotation({
      decision_id: context.decision_id,
      sequence,
      annotated_event_type: eventType,
      note: note.trim(),
      annotation_type: annotationType,
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
          err instanceof Error ? err.message : "Annotation creation failed.",
        );
      });
  }

  return (
    <div
      aria-labelledby="annotation-modal-title"
      aria-modal="true"
      className="thesis-modal-overlay"
      role="dialog"
    >
      <div className="thesis-modal-surface annotation-modal-surface">
        <div className="thesis-modal-header">
          <div>
            <p className="eyebrow">
              Replay Annotation — <code className="timeline-event-type">{eventType}</code>
            </p>
            <h2 id="annotation-modal-title">Add a note</h2>
            <p className="thesis-modal-description">
              Annotations attach to this event and persist as replayable cognitive artifacts.
            </p>
          </div>
          <button
            aria-label="Cancel annotation"
            className="thesis-modal-close"
            onClick={onCancel}
            type="button"
          >
            ×
          </button>
        </div>

        <form className="thesis-modal-form" onSubmit={handleSubmit}>
          <div className="thesis-field-group">
            <label className="thesis-field-label" htmlFor="annotation-type">
              Annotation Type
            </label>
            {selectedOption ? (
              <p className="thesis-field-hint">{selectedOption.description}</p>
            ) : null}
            <select
              className="thesis-regime-input"
              id="annotation-type"
              onChange={(e) => setAnnotationType(e.target.value as AnnotationType)}
              value={annotationType}
            >
              {ANNOTATION_TYPE_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>

          <div className="thesis-field-group">
            <label className="thesis-field-label" htmlFor="annotation-note">
              Note
              <span className="thesis-field-required" aria-hidden="true"> *</span>
            </label>
            <textarea
              className="thesis-narrative-input"
              id="annotation-note"
              onChange={(e) => setNote(e.target.value)}
              placeholder="What do you want to record about this event?"
              required
              rows={4}
              value={note}
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
              {submitState === "submitting" ? "Saving…" : "Add Note"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
