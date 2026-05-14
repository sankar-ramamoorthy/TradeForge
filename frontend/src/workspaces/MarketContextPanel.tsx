import { TrendingUp } from "lucide-react";
import { useState } from "react";

import {
  fetchMarketContext,
  type MarketContextOverlay,
  type MarketSnapshotOverlay,
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

function SnapshotRow({ snap }: { snap: MarketSnapshotOverlay }) {
  const dataAsOf = new Date(snap.data_as_of).toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
  const regimeLabel = REGIME_LABELS[snap.regime] ?? snap.regime;
  const showRegime = snap.regime !== "unknown";

  return (
    <div className="market-snapshot" aria-label={`Market snapshot for ${snap.symbol}`}>
      <div className="snapshot-symbol-row">
        <span className="snapshot-symbol">{snap.symbol}</span>
        {showRegime ? (
          <span className={`regime-badge regime-${snap.regime}`} aria-label={`Regime: ${regimeLabel}`}>
            {regimeLabel}
          </span>
        ) : null}
        <span className="field-authority-badge authority-advisory">Advisory</span>
      </div>
      <div className="snapshot-ohlcv">
        <span className="ohlcv-item">
          <span className="ohlcv-label">O</span>
          {snap.open}
        </span>
        <span className="ohlcv-item">
          <span className="ohlcv-label">H</span>
          {snap.high}
        </span>
        <span className="ohlcv-item">
          <span className="ohlcv-label">L</span>
          {snap.low}
        </span>
        <span className="ohlcv-item">
          <span className="ohlcv-label">C</span>
          {snap.close}
        </span>
        <span className="ohlcv-item">
          <span className="ohlcv-label">Vol</span>
          {snap.volume.toLocaleString()}
        </span>
      </div>
      <div className="snapshot-provenance">
        <code className="provenance-detail">
          {snap.provider_id} · data as of {dataAsOf}
        </code>
      </div>
    </div>
  );
}

type LoadState = "idle" | "loading" | "loaded" | "error";

export function MarketContextPanel() {
  const [inputValue, setInputValue] = useState(() => getWatchedSymbolsString());
  const [overlay, setOverlay] = useState<MarketContextOverlay | null>(null);
  const [loadState, setLoadState] = useState<LoadState>("idle");
  const [loadError, setLoadError] = useState<string | null>(null);

  function handleLoad() {
    const symbols = inputValue
      .split(",")
      .map((s) => s.trim().toUpperCase())
      .filter(Boolean);

    if (symbols.length === 0) return;

    setLoadState("loading");
    setLoadError(null);

    fetchMarketContext(symbols)
      .then((data) => {
        setOverlay(data);
        setLoadState("loaded");
        addWatchedSymbols(symbols);
      })
      .catch((err: unknown) => {
        setLoadError(
          err instanceof Error ? err.message : "Failed to load market context",
        );
        setLoadState("error");
      });
  }

  return (
    <div className="market-context-panel" aria-label="Market context overlay">
      <div className="market-context-header">
        <TrendingUp aria-hidden="true" className="market-context-icon" />
        <span className="eyebrow">Market Context</span>
      </div>
      <p className="market-context-note">
        Advisory price data from market provider. Non-authoritative — does not
        affect lifecycle state or canonical truth.
      </p>

      <div className="market-context-input-row">
        <input
          aria-label="Ticker symbol"
          className="symbol-input"
          disabled={loadState === "loading"}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") handleLoad();
          }}
          placeholder="e.g. AAPL or AAPL,TSLA"
          type="text"
          value={inputValue}
        />
        <button
          className="market-load-btn"
          disabled={loadState === "loading" || inputValue.trim() === ""}
          onClick={handleLoad}
          type="button"
        >
          {loadState === "loading" ? "Loading…" : "Load"}
        </button>
      </div>

      {loadState === "error" && loadError ? (
        <div className="runtime-error">{loadError}</div>
      ) : null}

      {overlay !== null ? (
        <div className="market-context-results">
          {overlay.available.map((snap) => (
            <SnapshotRow key={snap.symbol} snap={snap} />
          ))}
          {overlay.unavailable_symbols.length > 0 ? (
            <div className="market-unavailable">
              <span className="eyebrow">Unavailable</span>
              <p className="market-unavailable-list">
                {overlay.unavailable_symbols.join(", ")}
              </p>
            </div>
          ) : null}
          {overlay.is_empty ? (
            <p className="market-no-data">
              No data available from provider. Symbol may be invalid or
              provider unavailable.
            </p>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}
