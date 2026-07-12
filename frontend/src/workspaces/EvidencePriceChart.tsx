import { type EvidenceChartPoint } from "../api/runtime";

type EvidencePriceChartProps = {
  points: EvidenceChartPoint[];
};

export function EvidencePriceChart({ points }: EvidencePriceChartProps) {
  if (points.length === 0) {
    return (
      <div className="evidence-chart-empty">
        <span>No archived snapshots yet.</span>
      </div>
    );
  }

  const closes = points.map((point) => Number(point.close));
  const min = Math.min(...closes);
  const max = Math.max(...closes);
  const span = max - min || 1;
  const width = 320;
  const height = 132;
  const pad = 14;
  const path = points
    .map((point, index) => {
      const x =
        pad +
        (index / Math.max(points.length - 1, 1)) * (width - pad * 2);
      const close = Number(point.close);
      const y = height - pad - ((close - min) / span) * (height - pad * 2);
      return `${index === 0 ? "M" : "L"} ${x.toFixed(1)} ${y.toFixed(1)}`;
    })
    .join(" ");

  return (
    <div className="evidence-chart" aria-label="Archived price snapshots">
      <svg viewBox={`0 0 ${width} ${height}`} role="img">
        <path className="evidence-chart-grid" d={`M ${pad} ${height - pad} H ${width - pad}`} />
        <path className="evidence-chart-line" d={path} />
      </svg>
      <div className="evidence-chart-scale" aria-hidden="true">
        <span>{max.toFixed(2)}</span>
        <span>{min.toFixed(2)}</span>
      </div>
    </div>
  );
}
