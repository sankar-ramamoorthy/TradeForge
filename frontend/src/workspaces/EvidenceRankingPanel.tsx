import { AlertTriangle, CheckCircle2, Pin, PlusCircle, RefreshCw } from "lucide-react";
import { type FormEvent, useEffect, useState } from "react";

import {
  fetchEvidenceRanking,
  postWatchlistEntry,
  runEvidenceRefresh,
  type EvidenceCoverageRecord,
  type EvidenceRanking,
  type EvidenceRefreshResult,
} from "../api/runtime";
import { type WorkspaceContext } from "../workspaceRouting";

type EvidenceRankingPanelProps = {
  context: Required<WorkspaceContext>;
};

export function EvidenceRankingPanel({ context }: EvidenceRankingPanelProps) {
  const [ranking, setRanking] = useState<EvidenceRanking | null>(null);
  const [symbol, setSymbol] = useState("");
  const [rationale, setRationale] = useState("");
  const [pinned, setPinned] = useState(false);
  const [lastRefresh, setLastRefresh] = useState<EvidenceRefreshResult | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    fetchEvidenceRanking(controller.signal)
      .then((data) => {
        setRanking(data);
        setError(null);
      })
      .catch((err: unknown) => {
        if (err instanceof DOMException && err.name === "AbortError") return;
        setError(err instanceof Error ? err.message : "Failed to load ranking");
      });
    return () => controller.abort();
  }, []);

  async function reloadAfterRefresh() {
    setBusy(true);
    try {
      const refresh = await runEvidenceRefresh();
      setLastRefresh(refresh);
      setRanking(await fetchEvidenceRanking());
      setError(null);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to refresh ranking");
    } finally {
      setBusy(false);
    }
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!symbol.trim() || !rationale.trim()) return;
    setBusy(true);
    try {
      await postWatchlistEntry({
        symbol,
        rationale,
        persona_id: context.persona_id,
        workspace_id: context.workspace_id,
        pinned,
      });
      setSymbol("");
      setRationale("");
      setPinned(false);
      const refresh = await runEvidenceRefresh();
      setLastRefresh(refresh);
      setRanking(await fetchEvidenceRanking());
      setError(null);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to add watchlist item");
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="evidence-ranking-panel" aria-label="Evidence ranking">
      <div className="evidence-panel-header">
        <div>
          <p className="eyebrow">Evidence Attention</p>
          <h2>Ranked symbols</h2>
        </div>
        <button
          className="icon-text-btn"
          disabled={busy}
          onClick={() => {
            void reloadAfterRefresh();
          }}
          type="button"
        >
          <RefreshCw aria-hidden="true" />
          <span>{busy ? "Refreshing" : "Refresh"}</span>
        </button>
      </div>

      <form className="watchlist-add-form" onSubmit={handleSubmit}>
        <input
          aria-label="Symbol"
          onChange={(event) => setSymbol(event.target.value.toUpperCase())}
          placeholder="Symbol"
          value={symbol}
        />
        <input
          aria-label="Rationale"
          onChange={(event) => setRationale(event.target.value)}
          placeholder="Rationale"
          value={rationale}
        />
        <label className="watchlist-pin-toggle">
          <input
            checked={pinned}
            onChange={(event) => setPinned(event.target.checked)}
            type="checkbox"
          />
          <Pin aria-hidden="true" />
        </label>
        <button className="icon-only-submit" disabled={busy} type="submit">
          <PlusCircle aria-hidden="true" />
        </button>
      </form>

      {error ? <p className="runtime-error">{error}</p> : null}

      {lastRefresh ? (
        <CoverageSummaryBlock
          coverage={lastRefresh.coverage}
          summary={lastRefresh.coverage_summary}
        />
      ) : ranking?.coverage_summary.is_partial ? (
        <div className="evidence-coverage-summary partial" role="status">
          <AlertTriangle aria-hidden="true" />
          <div>
            <strong>{ranking.coverage_summary.summary}</strong>
            <span>{ranking.coverage_summary.next_action}</span>
          </div>
        </div>
      ) : null}

      {ranking && ranking.items.length > 0 ? (
        <div className="evidence-ranking-list" role="list">
          {ranking.items.map((item) => (
            <article className="evidence-ranking-item" key={item.symbol} role="listitem">
              <div className="evidence-rank-marker">#{item.rank}</div>
              <div className="evidence-rank-main">
                <div className="evidence-rank-topline">
                  <strong>{item.symbol}</strong>
                  <span>{item.freshness}</span>
                </div>
                <p>{item.reasons.map((reason) => reason.label).join(", ")}</p>
                {item.coverage ? <CoverageLine coverage={item.coverage} /> : null}
              </div>
              <span className="evidence-score">{item.priority_score}</span>
            </article>
          ))}
        </div>
      ) : (
        <p className="evidence-muted">No eligible symbols yet.</p>
      )}
    </section>
  );
}

type CoverageSummaryBlockProps = {
  coverage: EvidenceCoverageRecord[];
  summary: EvidenceRefreshResult["coverage_summary"];
};

function CoverageSummaryBlock({ coverage, summary }: CoverageSummaryBlockProps) {
  return (
    <div
      className={`evidence-coverage-summary ${summary.is_partial ? "partial" : "complete"}`}
      role="status"
    >
      {summary.is_partial ? (
        <AlertTriangle aria-hidden="true" />
      ) : (
        <CheckCircle2 aria-hidden="true" />
      )}
      <div>
        <strong>{summary.summary}</strong>
        <span>{summary.next_action}</span>
        <div className="evidence-coverage-symbols">
          {coverage.map((item) => (
            <span className={`coverage-pill status-${item.status}`} key={item.symbol}>
              {item.symbol}: {coverageLabel(item)}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

function CoverageLine({ coverage }: { coverage: EvidenceCoverageRecord }) {
  const providers =
    coverage.provider_ids.length > 0
      ? coverage.provider_ids.join(", ")
      : coverage.attempts.map((attempt) => attempt.provider_id).join(", ");
  const providerText = providers ? `Provider: ${providers}. ` : "";
  const missingText =
    coverage.missing_fields.length > 0
      ? `Missing: ${coverage.missing_fields.join(", ")}. `
      : "";
  return (
    <small className={`evidence-coverage-line status-${coverage.status}`}>
      {providerText}
      {missingText}
      {coverage.next_action}
    </small>
  );
}

function coverageLabel(coverage: EvidenceCoverageRecord): string {
  if (coverage.status === "provider-degraded") return "provider failed";
  if (coverage.status === "missing") return "missing";
  if (coverage.status === "stale") return "stale";
  return "refreshed";
}
