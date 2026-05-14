import { type PlanReadiness, type ReadinessCheck } from "../api/runtime";

function CheckRow({ check }: { check: ReadinessCheck }) {
  const icon = check.passed
    ? "✓"
    : check.advisory
    ? "⚠"
    : "✕";

  const rowClass = check.passed
    ? "readiness-check-row passed"
    : check.advisory
    ? "readiness-check-row advisory"
    : "readiness-check-row failed";

  return (
    <div className={rowClass} role="listitem">
      <span className="readiness-check-icon" aria-hidden="true">{icon}</span>
      <div className="readiness-check-content">
        <span className="readiness-check-label">
          {check.label}
          {check.advisory ? (
            <span className="readiness-advisory-badge"> Advisory</span>
          ) : null}
        </span>
        <p className="readiness-check-message">{check.message}</p>
      </div>
    </div>
  );
}

type Props = {
  readiness: PlanReadiness;
};

export function PlanReadinessPanel({ readiness }: Props) {
  const blockers = readiness.checks.filter((c) => !c.advisory && !c.passed);
  const advisories = readiness.checks.filter((c) => c.advisory && !c.passed);
  const allPassed = readiness.checks.filter((c) => c.passed);

  const summaryLabel = readiness.can_proceed_to_approval
    ? "Ready for authorization"
    : blockers.length > 0
    ? `${blockers.length} item${blockers.length !== 1 ? "s" : ""} required before authorization`
    : "Review advisory items before proceeding";

  const summaryClass = readiness.can_proceed_to_approval
    ? "readiness-summary ready"
    : blockers.length > 0
    ? "readiness-summary blocked"
    : "readiness-summary advisory";

  return (
    <div className="plan-readiness-panel" aria-label="Plan readiness">
      <p className="eyebrow">
        Plan Readiness
        {readiness.next_allowed_transition ? (
          <span className="readiness-next-transition">
            {" "}— next: {readiness.next_allowed_transition}
          </span>
        ) : null}
      </p>

      <div className={summaryClass} role="status">
        {summaryLabel}
      </div>

      <div className="readiness-checks" role="list">
        {readiness.checks.map((check) => (
          <CheckRow check={check} key={check.check_id} />
        ))}
      </div>

      {readiness.can_proceed_to_approval ? null : (
        <div className="readiness-footer">
          <p className="authority-boundary">
            This readiness check is derived — it does not authorize the plan or
            bypass lifecycle validation.
          </p>
        </div>
      )}

      {(blockers.length === 0 && (advisories.length > 0 || allPassed.length > 0)) ? (
        <p className="readiness-footer-note">
          {advisories.length > 0
            ? `${advisories.length} advisory item${advisories.length !== 1 ? "s" : ""} — review before proceeding.`
            : "All checks passed."}
        </p>
      ) : null}
    </div>
  );
}
