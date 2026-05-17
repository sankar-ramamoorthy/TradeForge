import { useEffect, useState } from "react";
import {
  fetchFundamentalsContext,
  type FundamentalsOverlay,
} from "../api/runtime";

export function FundamentalsContextPanel({ symbol }: { symbol: string }) {
  const [overlay, setOverlay] = useState<FundamentalsOverlay | null>(null);

  useEffect(() => {
    if (!symbol || symbol === "–") return;
    const controller = new AbortController();
    fetchFundamentalsContext(symbol, controller.signal)
      .then(setOverlay)
      .catch(() => setOverlay(null));
    return () => controller.abort();
  }, [symbol]);

  if (!overlay) return null;

  return (
    <section className="fundamentals-context-panel" aria-label="Fundamentals context">
      <div className="panel-heading">
        <p className="eyebrow">Fundamentals Context</p>
        <span className="field-authority-badge authority-advisory">Advisory</span>
      </div>
      {overlay.is_available ? (
        <>
          <h3>{overlay.company_name ?? overlay.symbol}</h3>
          <p>{[overlay.sector, overlay.industry].filter(Boolean).join(" / ")}</p>
          <dl>
            <div><dt>Revenue</dt><dd>{overlay.revenue ?? "Unavailable"}</dd></div>
            <div><dt>Net income</dt><dd>{overlay.net_income ?? "Unavailable"}</dd></div>
            <div><dt>P/E</dt><dd>{overlay.price_earnings ?? "Unavailable"}</dd></div>
            <div><dt>ROE</dt><dd>{overlay.return_on_equity ?? "Unavailable"}</dd></div>
          </dl>
          <p className="projection-detail">
            {overlay.selected_provider_id}
            {overlay.used_fallback ? " via fallback" : ""} / as of {overlay.data_as_of}
          </p>
        </>
      ) : (
        <p className="market-no-data">Fundamentals unavailable.</p>
      )}
    </section>
  );
}
