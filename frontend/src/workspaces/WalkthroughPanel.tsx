import { BookOpen, X } from "lucide-react";
import type { WalkthroughStepDef } from "../walkthrough";

type WalkthroughPanelProps = {
  step: WalkthroughStepDef;
  isAdvancing: boolean;
  error: string | null;
  onAdvance: () => void;
  onExit: () => void;
};

export function WalkthroughPanel({
  step,
  isAdvancing,
  error,
  onAdvance,
  onExit,
}: WalkthroughPanelProps) {
  const isLastStep = step.nextWorkspacePath === null;
  const displayStep = step.stepIndex + 1;

  return (
    <aside
      className="walkthrough-panel"
      aria-label={`Guided walkthrough step ${displayStep} of ${step.totalSteps}`}
    >
      <div className="walkthrough-header">
        <div className="walkthrough-header-left">
          <BookOpen aria-hidden="true" className="walkthrough-icon" />
          <span className="walkthrough-label">Guided Walkthrough</span>
          <div
            className="walkthrough-dots"
            aria-label={`Step ${displayStep} of ${step.totalSteps}`}
          >
            {Array.from({ length: step.totalSteps }, (_, i) => (
              <span
                key={i}
                className={`walkthrough-dot${
                  i < step.stepIndex
                    ? " wt-done"
                    : i === step.stepIndex
                      ? " wt-current"
                      : ""
                }`}
                aria-hidden="true"
              />
            ))}
          </div>
          <span className="walkthrough-step-count" aria-hidden="true">
            {displayStep} / {step.totalSteps}
          </span>
        </div>
        <button
          aria-label="Exit guided walkthrough"
          className="walkthrough-exit"
          onClick={onExit}
          type="button"
        >
          <X aria-hidden="true" />
          <span>Exit</span>
        </button>
      </div>

      <div className="walkthrough-body">
        <h3 className="walkthrough-step-title">{step.title}</h3>
        <p className="walkthrough-explanation">{step.explanation}</p>
        {step.glossary.length > 0 ? (
          <dl className="walkthrough-glossary">
            {step.glossary.map((item) => (
              <div key={item.term} className="walkthrough-glossary-item">
                <dt>{item.term}</dt>
                <dd>{item.definition}</dd>
              </div>
            ))}
          </dl>
        ) : null}
        {error ? (
          <p className="walkthrough-error" role="alert">
            {error}
          </p>
        ) : null}
      </div>

      <div className="walkthrough-footer">
        <button
          className={`walkthrough-advance${isLastStep ? " walkthrough-finish" : ""}`}
          disabled={isAdvancing}
          onClick={onAdvance}
          type="button"
        >
          {isAdvancing ? "Advancing…" : step.actionLabel}
        </button>
      </div>
    </aside>
  );
}
