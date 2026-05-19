import { getAdvisoryContext } from "../operationalContext";

const REGIME_LABELS: Record<string, string> = {
  bull: "bullish",
  bear: "bearish",
  ranging: "range-bound",
  "high-volatility": "high-volatility",
  "low-volatility": "low-volatility",
  unknown: "unclear",
};

export function OpportunitySynthesisPanel({ symbol }: { symbol: string }) {
  const context = getAdvisoryContext(symbol);
  if (!context) return null;

  const regime =
    context.price_regime === null
      ? null
      : (REGIME_LABELS[context.price_regime] ?? context.price_regime);
  const missingEvidence =
    context.fundamentals_coverage_status === "available"
      ? null
      : context.fundamentals_coverage_status === "unsupported"
        ? "Company fundamentals are not the right context family for this instrument."
        : "Fundamental evidence has not been established for this opportunity.";

  return (
    <section className="opportunity-synthesis-panel" aria-label="Opportunity synthesis">
      <div className="panel-heading">
        <p className="eyebrow">Advisory Synthesis</p>
        <span className="field-authority-badge authority-advisory">Advisory</span>
      </div>
      <h2>{symbol} context handoff</h2>
      <dl>
        <div>
          <dt>Current interpretation</dt>
          <dd>
            {regime
              ? `Price context currently reads as ${regime}.`
              : "No acquired price interpretation has been handed off yet."}
          </dd>
        </div>
        <div>
          <dt>Missing evidence</dt>
          <dd>{missingEvidence ?? "Company fundamentals are available for review."}</dd>
        </div>
        <div>
          <dt>Thesis implication</dt>
          <dd>
            {missingEvidence
              ? "Use this context as an input to operator judgment before thesis formation."
              : "Price and fundamentals context are both available to inform thesis development."}
          </dd>
        </div>
      </dl>
      <p className="projection-detail">
        Provider data remains advisory and does not alter lifecycle authority.
      </p>
    </section>
  );
}
