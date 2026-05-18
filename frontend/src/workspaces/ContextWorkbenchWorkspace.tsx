import { LibraryBig, RefreshCw } from "lucide-react";
import { useEffect, useMemo, useState } from "react";

import {
  fetchFundamentalsContext,
  fetchMarketContext,
  type FundamentalsOverlay,
  type MarketContextOverlay,
  type ProviderAttempt,
} from "../api/runtime";
import {
  addWatchedSymbols,
  getWatchedSymbolsString,
  upsertAdvisoryContext,
} from "../operationalContext";

type AcquisitionState = "not-requested" | "loading" | "loaded" | "unavailable";
type InstrumentKind = "equity" | "etf";

type ContextFamilyCardProps = {
  title: string;
  description: string;
  state: AcquisitionState;
  onRequest: () => void;
  disabled: boolean;
  children: React.ReactNode;
};

const STATE_LABELS: Record<AcquisitionState, string> = {
  "not-requested": "Not requested",
  loading: "Loading",
  loaded: "Loaded",
  unavailable: "Unavailable",
};

function normalizeSymbol(value: string): string {
  return value.trim().toUpperCase().split(",")[0] ?? "";
}

function ContextFamilyCard({
  title,
  description,
  state,
  onRequest,
  disabled,
  children,
}: ContextFamilyCardProps) {
  return (
    <section className="context-family-card" aria-label={title}>
      <div className="context-family-heading">
        <div>
          <p className="eyebrow">Context Family</p>
          <h2>{title}</h2>
        </div>
        <span className={`context-family-state state-${state}`}>
          {STATE_LABELS[state]}
        </span>
      </div>
      <p className="context-family-description">{description}</p>
      <button
        className="context-family-action"
        disabled={disabled || state === "loading"}
        onClick={onRequest}
        type="button"
      >
        <RefreshCw aria-hidden="true" />
        <span>{state === "not-requested" ? "Request" : "Request again"}</span>
      </button>
      {children}
    </section>
  );
}

function AttemptList({ attempts }: { attempts: ProviderAttempt[] }) {
  if (attempts.length === 0) return null;

  return (
    <dl className="context-family-results" aria-label="Provider attempts">
      {attempts.map((attempt) => (
        <div key={`${attempt.provider_id}-${attempt.attempted_at}`}>
          <dt>{attempt.provider_id}</dt>
          <dd>
            {attempt.outcome}
            {attempt.failure_reason ? `: ${attempt.failure_reason}` : ""}
          </dd>
        </div>
      ))}
    </dl>
  );
}

export function ContextWorkbenchWorkspace() {
  const [symbolInput, setSymbolInput] = useState(() => getWatchedSymbolsString());
  const [instrumentKind, setInstrumentKind] = useState<InstrumentKind>("equity");
  const symbol = useMemo(() => normalizeSymbol(symbolInput), [symbolInput]);
  const [priceState, setPriceState] =
    useState<AcquisitionState>("not-requested");
  const [fundamentalsState, setFundamentalsState] =
    useState<AcquisitionState>("not-requested");
  const [priceOverlay, setPriceOverlay] = useState<MarketContextOverlay | null>(
    null,
  );
  const [fundamentalsOverlay, setFundamentalsOverlay] =
    useState<FundamentalsOverlay | null>(null);
  const [priceError, setPriceError] = useState<string | null>(null);
  const [fundamentalsError, setFundamentalsError] = useState<string | null>(null);

  useEffect(() => {
    setPriceState("not-requested");
    setFundamentalsState("not-requested");
    setPriceOverlay(null);
    setFundamentalsOverlay(null);
    setPriceError(null);
    setFundamentalsError(null);
  }, [symbol]);

  async function handleRequestPriceContext() {
    if (!symbol) return;
    setPriceState("loading");
    setPriceError(null);

    try {
      const overlay = await fetchMarketContext([symbol]);
      setPriceOverlay(overlay);
      setPriceState(overlay.available.length > 0 ? "loaded" : "unavailable");
      addWatchedSymbols([symbol]);
      const snapshot = overlay.available[0];
      upsertAdvisoryContext(symbol, {
        price_regime: snapshot?.regime ?? null,
        price_provider_id: snapshot?.provider_id ?? null,
        price_data_as_of: snapshot?.data_as_of ?? null,
      });
    } catch (error: unknown) {
      setPriceOverlay(null);
      setPriceError(
        error instanceof Error ? error.message : "Price context request failed",
      );
      setPriceState("unavailable");
    }
  }

  async function handleRequestFundamentals() {
    if (!symbol) return;
    setFundamentalsState("loading");
    setFundamentalsError(null);

    try {
      const overlay = await fetchFundamentalsContext(symbol, instrumentKind);
      setFundamentalsOverlay(overlay);
      setFundamentalsState(
        overlay.coverage_status === "available" ? "loaded" : "unavailable",
      );
      addWatchedSymbols([symbol]);
      upsertAdvisoryContext(symbol, {
        fundamentals_coverage_status: overlay.coverage_status,
        fundamentals_provider_id: overlay.selected_provider_id,
        fundamentals_company_name: overlay.company_name,
        fundamentals_sector: overlay.sector,
      });
    } catch (error: unknown) {
      setFundamentalsOverlay(null);
      setFundamentalsError(
        error instanceof Error
          ? error.message
          : "Fundamentals context request failed",
      );
      setFundamentalsState("unavailable");
    }
  }

  const priceSnapshot = priceOverlay?.available[0] ?? null;

  return (
    <section className="workspace-surface context-workbench-surface" aria-labelledby="context-workbench-title">
      <div className="surface-title">
        <LibraryBig aria-hidden="true" />
        <div>
          <p className="eyebrow">Workspace Route</p>
          <h1 id="context-workbench-title">Context Workbench</h1>
        </div>
      </div>

      <div className="context-workbench-toolbar">
        <label>
          Instrument
          <input
            aria-label="Instrument symbol"
            className="symbol-input"
            onChange={(event) => setSymbolInput(event.target.value)}
            placeholder="e.g. INTC"
            type="text"
            value={symbolInput}
          />
        </label>
        <label>
          Instrument type
          <select
            onChange={(event) => setInstrumentKind(event.target.value as InstrumentKind)}
            value={instrumentKind}
          >
            <option value="equity">Equity</option>
            <option value="etf">ETF</option>
          </select>
        </label>
        <p>
          Advisory acquisition only. Request the context families you want to
          inspect for this instrument.
        </p>
      </div>

      <div className="context-family-grid">
        <ContextFamilyCard
          description="Latest provider-backed price snapshot and basic technical regime."
          disabled={!symbol}
          onRequest={() => void handleRequestPriceContext()}
          state={priceState}
          title="Price / Technical"
        >
          {priceError ? <div className="runtime-error">{priceError}</div> : null}
          {priceSnapshot ? (
            <dl className="context-family-results">
              <div><dt>Provider</dt><dd>{priceSnapshot.provider_id}</dd></div>
              <div><dt>Interpretation</dt><dd>{priceSnapshot.interpretation_headline}</dd></div>
              <div><dt>Close</dt><dd>{priceSnapshot.close}</dd></div>
              <div><dt>Regime</dt><dd>{priceSnapshot.regime}</dd></div>
              <div><dt>Data as of</dt><dd>{priceSnapshot.data_as_of}</dd></div>
            </dl>
          ) : priceState === "unavailable" ? (
            <p className="market-no-data">
              Price context request did not return usable data. You can continue,
              but current technical context is incomplete.
            </p>
          ) : null}
          <AttemptList attempts={priceOverlay?.attempts ?? []} />
        </ContextFamilyCard>

        <ContextFamilyCard
          description="Company fundamentals returned by the configured fundamentals provider path."
          disabled={!symbol}
          onRequest={() => void handleRequestFundamentals()}
          state={fundamentalsState}
          title="Fundamentals"
        >
          {fundamentalsError ? (
            <div className="runtime-error">{fundamentalsError}</div>
          ) : null}
          {fundamentalsOverlay?.is_available ? (
            <dl className="context-family-results">
              <div><dt>Provider</dt><dd>{fundamentalsOverlay.selected_provider_id}</dd></div>
              <div><dt>Company</dt><dd>{fundamentalsOverlay.company_name ?? symbol}</dd></div>
              <div><dt>Sector</dt><dd>{fundamentalsOverlay.sector ?? "Unavailable"}</dd></div>
              <div><dt>Data as of</dt><dd>{fundamentalsOverlay.data_as_of ?? "Unavailable"}</dd></div>
            </dl>
          ) : fundamentalsOverlay?.coverage_status === "unsupported" ? (
            <p className="market-no-data">
              Company fundamentals do not describe an ETF. ETF-specific context
              is the relevant next family for holdings, exposure, and macro
              sensitivity.
            </p>
          ) : fundamentalsState === "unavailable" ? (
            <p className="market-no-data">
              Fundamentals request did not return usable data. You can continue
              technical evaluation, but valuation context is incomplete.
            </p>
          ) : null}
          <AttemptList attempts={fundamentalsOverlay?.attempts ?? []} />
        </ContextFamilyCard>
      </div>
    </section>
  );
}
