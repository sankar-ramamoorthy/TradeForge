import { PlusCircle, X } from "lucide-react";
import { type FormEvent, useRef, useState } from "react";

import { initNewTradeIdea } from "../api/runtime";

type NewTradeIdeaModalProps = {
  personaId: string;
  workspaceId: string;
  onCreated: (decisionId: string, symbol: string) => void;
  onCancel: () => void;
};

export function NewTradeIdeaModal({
  personaId,
  workspaceId,
  onCreated,
  onCancel,
}: NewTradeIdeaModalProps) {
  const [symbol, setSymbol] = useState("");
  const [initialThesis, setInitialThesis] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const symbolRef = useRef<HTMLInputElement>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmedSymbol = symbol.trim().toUpperCase();
    if (!trimmedSymbol) {
      setError("Symbol is required.");
      symbolRef.current?.focus();
      return;
    }

    setSubmitting(true);
    setError(null);

    try {
      const result = await initNewTradeIdea({
        symbol: trimmedSymbol,
        initial_thesis: initialThesis.trim() || undefined,
        persona_id: personaId,
        workspace_id: workspaceId,
      });
      onCreated(result.decision_id, result.symbol);
    } catch (err: unknown) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to initialize trade idea. Please try again.",
      );
      setSubmitting(false);
    }
  }

  return (
    <div className="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="new-idea-title">
      <div className="modal-dialog">
        <div className="modal-header">
          <PlusCircle aria-hidden="true" />
          <h2 id="new-idea-title">New Trade Idea</h2>
          <button
            aria-label="Cancel"
            className="modal-close-btn"
            disabled={submitting}
            onClick={onCancel}
            type="button"
          >
            <X aria-hidden="true" />
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            <p className="modal-authority-note">
              Initializes a canonical lifecycle event. Lifecycle authority remains
              with the Decision Lifecycle Engine.
            </p>

            <div className="form-field">
              <label className="form-label" htmlFor="idea-symbol">
                Symbol <span aria-hidden="true">*</span>
              </label>
              <input
                autoFocus
                className="form-input"
                disabled={submitting}
                id="idea-symbol"
                maxLength={10}
                onChange={(e) => setSymbol(e.target.value.toUpperCase())}
                placeholder="e.g. AAPL"
                ref={symbolRef}
                required
                type="text"
                value={symbol}
              />
            </div>

            <div className="form-field">
              <label className="form-label" htmlFor="idea-thesis">
                Initial thesis notes <span className="form-optional">(optional)</span>
              </label>
              <textarea
                className="form-textarea"
                disabled={submitting}
                id="idea-thesis"
                maxLength={2000}
                onChange={(e) => setInitialThesis(e.target.value)}
                placeholder="Brief rationale or setup observation…"
                rows={4}
                value={initialThesis}
              />
            </div>

            {error ? (
              <div className="modal-error" role="alert">
                {error}
              </div>
            ) : null}
          </div>

          <div className="modal-footer">
            <button
              className="btn-secondary"
              disabled={submitting}
              onClick={onCancel}
              type="button"
            >
              Cancel
            </button>
            <button
              className="btn-primary"
              disabled={submitting || !symbol.trim()}
              type="submit"
            >
              {submitting ? "Initializing…" : "Start Workflow"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
