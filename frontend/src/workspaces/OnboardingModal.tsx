import {
  BookOpen,
  Compass,
  GitBranch,
  History,
  Layout,
  X,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";
import { useState } from "react";

type OnboardingScreen = {
  id: string;
  Icon: LucideIcon;
  headline: string;
  body: string;
};

const SCREENS: OnboardingScreen[] = [
  {
    id: "sovereignty",
    Icon: Compass,
    headline: "A decision system, not a trading bot.",
    body:
      "TradeForge exists to support disciplined, reflective decision-making in trading " +
      "and investing. It does not execute trades, generate signals, or automate " +
      "decisions. You are always in control.",
  },
  {
    id: "lifecycle",
    Icon: GitBranch,
    headline: "Every trade follows a structured path.",
    body:
      "TradeForge enforces a canonical decision lifecycle: Idea → Thesis → Plan → " +
      "Approval → Execution → Position → Review. Each stage is explicit, event-backed, " +
      "and permanent. Skipping stages is not possible.",
  },
  {
    id: "workspaces",
    Icon: Layout,
    headline: "Workspaces are not dashboards.",
    body:
      "Each workspace is a focused cognitive environment for a specific phase of the " +
      "decision workflow. They prioritize operational context over market data, and " +
      "workflow continuity over information density.",
  },
  {
    id: "review",
    Icon: BookOpen,
    headline: "The review is as important as the trade.",
    body:
      "TradeForge treats review as a first-class workflow, not an afterthought. Review " +
      "deliberately separates decision process quality from outcome — building long-term " +
      "discipline regardless of profit or loss.",
  },
  {
    id: "replay",
    Icon: History,
    headline: "Every decision is permanently recorded.",
    body:
      "The event ledger stores every lifecycle transition immutably. Any decision can be " +
      "replayed — reconstructing exactly what was known, visible, and decided at the time. " +
      "This is the foundation of long-term operational learning.",
  },
];

type OnboardingModalProps = {
  onComplete: () => void;
};

export function OnboardingModal({ onComplete }: OnboardingModalProps) {
  const [currentIndex, setCurrentIndex] = useState(0);

  const screen = SCREENS[currentIndex];
  const isFirst = currentIndex === 0;
  const isLast = currentIndex === SCREENS.length - 1;
  const { Icon } = screen;

  return (
    <div
      className="onboarding-overlay"
      role="dialog"
      aria-modal="true"
      aria-labelledby="onboarding-headline"
    >
      <div className="onboarding-card">
        <button
          className="onboarding-skip"
          aria-label="Skip onboarding"
          onClick={onComplete}
          type="button"
        >
          <X aria-hidden="true" />
          Skip
        </button>

        <div className="onboarding-icon-wrap" aria-hidden="true">
          <Icon className="onboarding-icon" />
        </div>

        <h2 id="onboarding-headline" className="onboarding-headline">
          {screen.headline}
        </h2>
        <p className="onboarding-body">{screen.body}</p>

        <div className="onboarding-dots" aria-hidden="true">
          {SCREENS.map((s, i) => (
            <span
              key={s.id}
              className={`onboarding-dot${i === currentIndex ? " ob-current" : i < currentIndex ? " ob-done" : ""}`}
            />
          ))}
        </div>

        <div className="onboarding-footer">
          {!isFirst ? (
            <button
              className="onboarding-prev"
              onClick={() => setCurrentIndex((n) => n - 1)}
              type="button"
            >
              ← Previous
            </button>
          ) : (
            <span />
          )}
          {isLast ? (
            <button
              className="onboarding-next onboarding-finish"
              onClick={onComplete}
              type="button"
            >
              Get Started →
            </button>
          ) : (
            <button
              className="onboarding-next"
              onClick={() => setCurrentIndex((n) => n + 1)}
              type="button"
            >
              Next →
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
