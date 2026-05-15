import { useState, type FormEvent } from "react";
import { type WorkspaceContext } from "../workspaceRouting";

type SubmitState = "idle" | "submitting" | "error";

type ArmPlanRequest = {
  decision_id: string;
  symbol: string;
  trigger_conditions: string[];
  persona_id: string;
  workspace_id: string;
};

type ArmPlanResponse = {
  decision_id: string;
  event_type: string;
  timestamp: string;
};

async function postArmPlan(
  request: ArmPlanRequest,
  signal?: AbortSignal,
): Promise<ArmPlanResponse> {
  const response = await fetch("/lifecycle/decisions/arm-plan", {
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
            `Arm plan failed: ${response.status}`)
          : `Arm plan failed: ${response.status}`
        : `Arm plan failed: ${response.status}`;
    throw new Error(message);
  }

  return response.json() as Promise<ArmPlanResponse>;
}

type Props = {
  context: Required<WorkspaceContext>;
  symbol: string;
  onSuccess: () => void;
  onCancel: () => void;
};

export function ArmPlanModal({ context, symbol, onSuccess, onCancel }: Props) {
  const [triggerConditions, setTriggerConditions] = useState<string[]>([""]);
  const [submitState, setSubmitState] = useState<SubmitState>("idle");
  const [submitError, setSubmitError] = useState<string | null>(null);

  function handleConditionChange(index: number, value: string) {
    const next = [...triggerConditions];
    next[index] = value;
    setTriggerConditions(next);
  }

  function handleAdd() {
    setTriggerConditions([...triggerConditions, ""]);
  }

  function handleRemove(index: number) {
    setTriggerConditions(triggerConditions.filter((_, i) => i !== index));
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitState("submitting");
    setSubmitError(null);

    const clean = triggerConditions.filter((c) => c.trim());
    if (clean.length === 0) {
      setSubmitError("At least one trigger condition is required.");
      setSubmitState("error");
      return;
    }

    postArmPlan({
      decision_id: context.decision_id,
      symbol,
      trigger_conditions: clean,
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
          err instanceof Error ? err.message : "Arm plan failed.",
        );
      });
  }

  return (
    <div
      aria-labelledby="arm-plan-modal-title"
      aria-modal="true"
      className="thesis-modal-overlay"
      role="dialog"
    >
      <div className="thesis-modal-surface">
        <div className="thesis-modal-header">
          <div>
            <p className="eyebrow">Arm Plan — {symbol}</p>
            <h2 id="arm-plan-modal-title">Declare trigger conditions</h2>
            <p className="thesis-modal-description">
              Specify the market conditions that must be met before execution.
              These conditions become a replayable record of your entry logic.
            </p>
          </div>
          <button
            aria-label="Cancel arm plan"
            className="thesis-modal-close"
            onClick={onCancel}
            type="button"
          >
            ×
          </button>
        </div>

        <form className="thesis-modal-form" onSubmit={handleSubmit}>
          <div className="thesis-list-input">
            <label className="thesis-field-label">
              Trigger Conditions
              <span className="thesis-field-required" aria-hidden="true"> *</span>
            </label>
            <p className="thesis-field-hint">
              What must happen in the market before you place the order?
            </p>
            {triggerConditions.map((condition, index) => (
              <div className="thesis-list-row" key={index}>
                <input
                  aria-label={`Trigger condition ${index + 1}`}
                  className="thesis-list-item-input"
                  onChange={(e) => handleConditionChange(index, e.target.value)}
                  placeholder="e.g. Daily close above 585 on rising volume"
                  type="text"
                  value={condition}
                />
                {triggerConditions.length > 1 ? (
                  <button
                    aria-label={`Remove trigger condition ${index + 1}`}
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
              {submitState === "submitting" ? "Arming plan…" : "Arm Plan"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
