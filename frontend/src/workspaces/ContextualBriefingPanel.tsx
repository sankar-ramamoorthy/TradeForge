import { LayoutDashboard } from "lucide-react";
import { useState } from "react";

import {
  fetchContextualSummary,
  type ContextualSummary,
  type WorkspaceApiParams,
} from "../api/runtime";
import {
  addWatchedSymbols,
  getWatchedSymbolsString,
} from "../operationalContext";

const REGIME_LABELS: Record<string, string> = {
  bull: "Bull",
  bear: "Bear",
  ranging: "Ranging",
  "high-volatility": "High Vol",
  "low-volatility": "Low Vol",
  unknown: "—",
};

type LoadState = "idle" | "loading" | "loaded" | "error";

type Props = {
  params: WorkspaceApiParams;
};

export function ContextualBriefingPanel({ params }: Props) {
  const [symbolInput, setSymbolInput] = useState(() => getWatchedSymbolsString());
  const [summary, setSummary] = useState<ContextualSummary | null>(null);
  const [loadState, setLoadState] = useState<LoadState>("idle");
  const [loadError, setLoadError] = useState<string | null>(null);

  function handleLoad() {
    const symbols = symbolInput
      .split(",")
      .map((s) => s.trim().toUpperCase())
      .filter(Boolean);

    setLoadState("loading");
    setLoadError(null);

    fetchContextualSummary(params, symbols.length > 0 ? symbols : undefined)
      .then((data) => {
        setSummary(data);
        setLoadState("loaded");
        if (symbols.length > 0) addWatchedSymbols(symbols);
      })
      .catch((err: unknown) => {
        setLoadError(
          err instanceof Error ? err.message : "Failed to load contextual summary",
        );
        setLoadState("error");
      });
  }

  return (
    <div className="contextual-briefing-panel" aria-label="Contextual operational briefing">
      <div className="contextual-briefing-header">
        <LayoutDashboard aria-hidden="true" className="briefing-icon" />
        <span className="eyebrow">Contextual Briefing</span>
      </div>
      <p className="contextual-briefing-note">
        Combined workspace state and advisory market context. Market data
        is non-authoritative and does not affect lifecycle state.
      </p>

      <div className="market-context-input-row">
        <input
          aria-label="Market symbols (optional)"
          className="symbol-input"
          disabled={loadState === "loading"}
          onChange={(e) => setSymbolInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") handleLoad();
          }}
          placeholder="Optional: AAPL,TSLA"
          type="text"
          value={symbolInput}
        />
        <button
          className="market-load-btn"
          disabled={loadState === "loading"}
          onClick={handleLoad}
          type="button"
        >
          {loadState === "loading" ? "Loading…" : "Refresh"}
        </button>
      </div>

      {loadState === "error" && loadError ? (
        <div className="runtime-error">{loadError}</div>
      ) : null}

      {summary !== null ? (
        <div className="contextual-briefing-body">
          <div className="briefing-headline" aria-label="Operational headline">
            <span className="eyebrow">Operational State</span>
            <p className="briefing-headline-text">{summary.operational_headline}</p>
          </div>

          {summary.operational_details.length > 0 ? (
            <ul className="briefing-details">
              {summary.operational_details.map((detail) => (
                <li className="briefing-detail-item" key={detail}>
                  {detail}
                </li>
              ))}
            </ul>
          ) : null}

          {summary.market_context_available &&
          summary.market_context_notes.length > 0 ? (
            <div className="briefing-market-notes" aria-label="Market context notes">
              <span className="eyebrow">Market Context</span>
              <div className="briefing-notes-grid">
                {summary.market_context_notes.map((note) => {
                  const regimeLabel =
                    REGIME_LABELS[note.regime] ?? note.regime;
                  const showRegime = note.regime !== "unknown";
                  return (
                    <div className="briefing-note-card" key={note.symbol}>
                      <span className="briefing-note-symbol">{note.symbol}</span>
                      <span className="briefing-note-close">{note.close}</span>
                      {showRegime ? (
                        <span
                          className={`regime-badge regime-${note.regime}`}
                          aria-label={`Regime: ${regimeLabel}`}
                        >
                          {regimeLabel}
                        </span>
                      ) : null}
                      <span className="field-authority-badge authority-advisory">
                        Advisory
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          ) : null}

          <div className="briefing-authority-note">
            {summary.authority_boundaries.map((b) => (
              <p className="authority-boundary" key={b}>
                {b}
              </p>
            ))}
          </div>
        </div>
      ) : null}
    </div>
  );
}
