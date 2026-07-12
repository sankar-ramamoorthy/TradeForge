import { Database, RefreshCw } from "lucide-react";
import { useEffect, useState } from "react";

import {
  fetchSymbolEvidence,
  runEvidenceRefresh,
  type EvidencePanel,
} from "../api/runtime";
import { EvidencePriceChart } from "./EvidencePriceChart";

type SymbolEvidencePanelProps = {
  symbol: string;
};

export function SymbolEvidencePanel({ symbol }: SymbolEvidencePanelProps) {
  const [panel, setPanel] = useState<EvidencePanel | null>(null);
  const [loading, setLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!symbol || symbol === "-") return;
    const controller = new AbortController();
    setLoading(true);
    fetchSymbolEvidence(symbol, controller.signal)
      .then((data) => {
        setPanel(data);
        setError(null);
      })
      .catch((err: unknown) => {
        if (err instanceof DOMException && err.name === "AbortError") return;
        setError(err instanceof Error ? err.message : "Failed to load evidence");
      })
      .finally(() => setLoading(false));
    return () => controller.abort();
  }, [symbol]);

  if (!symbol || symbol === "-") return null;

  async function handleRefresh() {
    setRefreshing(true);
    try {
      await runEvidenceRefresh();
      const next = await fetchSymbolEvidence(symbol);
      setPanel(next);
      setError(null);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to refresh evidence");
    } finally {
      setRefreshing(false);
    }
  }

  return (
    <section className="evidence-panel" aria-label={`${symbol} evidence`}>
      <div className="evidence-panel-header">
        <div>
          <p className="eyebrow">Evidence Density</p>
          <h2>{symbol}</h2>
        </div>
        <button
          className="icon-text-btn"
          disabled={refreshing}
          onClick={handleRefresh}
          type="button"
        >
          <RefreshCw aria-hidden="true" />
          <span>{refreshing ? "Refreshing" : "Refresh"}</span>
        </button>
      </div>

      {loading ? <p className="evidence-muted">Loading evidence...</p> : null}
      {error ? <p className="runtime-error">{error}</p> : null}

      {panel ? (
        <>
          <div className="evidence-fact-grid">
            {panel.facts.map((fact) => (
              <div className="evidence-fact" key={fact.key}>
                <span>{fact.label}</span>
                <strong>{fact.value ?? "Missing"}</strong>
                <small>{fact.freshness}</small>
              </div>
            ))}
          </div>

          <EvidencePriceChart points={panel.chart_points} />

          <div className="evidence-reason-row">
            <Database aria-hidden="true" />
            <span>
              {panel.ranking_item
                ? panel.ranking_item.reasons.map((r) => r.label).join(", ")
                : "No ranking reasons yet"}
            </span>
          </div>
        </>
      ) : null}
    </section>
  );
}
