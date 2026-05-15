export const LIFECYCLE_STAGES = [
  "Idea",
  "Thesis",
  "Plan",
  "Approval",
  "Armed",
  "Execution",
  "Position",
  "Review",
] as const;

type LifecycleStage = (typeof LIFECYCLE_STAGES)[number];

type StageGuidance = {
  meaning: string;
  guidance: string;
};

const STAGE_GUIDANCE: Record<LifecycleStage, StageGuidance> = {
  Idea: {
    meaning: "A candidate trade has been identified.",
    guidance:
      "Develop your investment thesis — why does this trade make sense, and under what conditions?",
  },
  Thesis: {
    meaning: "The reasoning behind the trade is taking shape.",
    guidance:
      "Structure a trade plan with entries, targets, and defined risk parameters.",
  },
  Plan: {
    meaning: "A structured plan is ready for deliberate review.",
    guidance:
      "Review the plan carefully and authorize it only if the conditions and risk are intentionally accepted.",
  },
  Approval: {
    meaning: "The plan is authorized. Declare trigger conditions before arming.",
    guidance:
      "Specify the market conditions that must be met before the order is placed.",
  },
  Armed: {
    meaning: "The plan is armed — watching for declared trigger conditions.",
    guidance:
      "Confirm execution only when the declared trigger conditions are satisfied.",
  },
  Execution: {
    meaning: "Execution submitted — awaiting position confirmation.",
    guidance:
      "Confirm the position is open and move into active supervision mode.",
  },
  Position: {
    meaning: "An open position is under active supervision.",
    guidance:
      "Monitor against the thesis. When the position is closed, begin the structured review.",
  },
  Review: {
    meaning: "The position is closed and review is complete.",
    guidance:
      "Capture what was learned — separate process quality from the outcome.",
  },
};

function stepState(
  index: number,
  currentIndex: number,
): "done" | "current" | "future" {
  if (index < currentIndex) return "done";
  if (index === currentIndex) return "current";
  return "future";
}

export function LifecycleProgressStrip({
  currentStage,
}: {
  currentStage: string | null;
}) {
  if (!currentStage) return null;

  const currentIndex = LIFECYCLE_STAGES.indexOf(
    currentStage as LifecycleStage,
  );
  if (currentIndex === -1) return null;

  return (
    <div
      className="lifecycle-progress-strip"
      aria-label={`Lifecycle progress: ${currentStage} stage`}
      role="list"
    >
      {LIFECYCLE_STAGES.map((stage, index) => {
        const state = stepState(index, currentIndex);
        return (
          <div
            className="lifecycle-step"
            data-state={state}
            key={stage}
            role="listitem"
            aria-current={state === "current" ? "step" : undefined}
          >
            {index > 0 ? (
              <div
                className="lifecycle-step-connector"
                data-state={state === "future" ? "future" : "done"}
                aria-hidden="true"
              />
            ) : null}
            <div className="lifecycle-step-dot" aria-hidden="true">
              {state === "done" ? "✓" : index + 1}
            </div>
            <span className="lifecycle-step-label">{stage}</span>
          </div>
        );
      })}
    </div>
  );
}

export function WorkflowGuidanceNote({
  currentStage,
}: {
  currentStage: string | null;
}) {
  if (!currentStage) return null;

  const guidance = STAGE_GUIDANCE[currentStage as LifecycleStage];
  if (!guidance) return null;

  return (
    <div className="workflow-guidance-note" aria-label="Stage guidance">
      <p className="workflow-guidance-meaning">{guidance.meaning}</p>
      <p className="workflow-guidance-action">{guidance.guidance}</p>
    </div>
  );
}
