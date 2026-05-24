import { DatabaseZap, Network, ShieldCheck } from "lucide-react";
import { useEffect, useState } from "react";

import {
  fetchProviderGovernance,
  type ProviderGovernance,
} from "../api/runtime";
import { ProviderConfigurationPanel } from "./ProviderConfigurationPanel";

export function ProviderGovernanceWorkspace() {
  const [governance, setGovernance] = useState<ProviderGovernance | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    fetchProviderGovernance(controller.signal)
      .then((data) => {
        setGovernance(data);
        setError(null);
      })
      .catch((err: unknown) => {
        if (err instanceof DOMException && err.name === "AbortError") return;
        setError(
          err instanceof Error ? err.message : "Provider governance request failed",
        );
      });
    return () => controller.abort();
  }, []);

  return (
    <section
      className="workspace-surface provider-governance-surface"
      aria-labelledby="provider-governance-title"
    >
      <div className="surface-title">
        <ShieldCheck aria-hidden="true" />
        <div>
          <p className="eyebrow">External Systems</p>
          <h1 id="provider-governance-title">Provider Governance</h1>
        </div>
      </div>

      {error ? <div className="runtime-error">{error}</div> : null}

      {governance ? (
        <>
          <div className="provider-governance-grid">
            <section className="provider-governance-section">
              <div className="panel-heading">
                <p className="eyebrow">Overview</p>
                <span className="field-authority-badge authority-derived">
                  {governance.authority}
                </span>
              </div>
              <dl className="provider-governance-kpis">
                <div>
                  <dt>Providers</dt>
                  <dd>{governance.providers.length}</dd>
                </div>
                <div>
                  <dt>Routes</dt>
                  <dd>{governance.routes.length}</dd>
                </div>
                <div>
                  <dt>Diagnostics</dt>
                  <dd>{governance.diagnostics.status}</dd>
                </div>
              </dl>
              <div className="authority-boundary-list">
                {governance.advisory_boundary.map((boundary) => (
                  <p className="authority-boundary" key={boundary}>
                    {boundary}
                  </p>
                ))}
              </div>
            </section>

            <section className="provider-governance-section">
              <div className="panel-heading">
                <p className="eyebrow">AI Gateway</p>
                <Network aria-hidden="true" />
              </div>
              <dl className="provider-gateway-details">
                <div>
                  <dt>Status</dt>
                  <dd>{governance.ai_gateway.status}</dd>
                </div>
                <div>
                  <dt>Gateway</dt>
                  <dd>{governance.ai_gateway.gateway_url ?? "not configured"}</dd>
                </div>
                <div>
                  <dt>Route Target</dt>
                  <dd>{governance.ai_gateway.default_model ?? "not configured"}</dd>
                </div>
                <div>
                  <dt>Underlying Provider</dt>
                  <dd>
                    {governance.ai_gateway.underlying_provider_id ?? "not inferred"}
                  </dd>
                </div>
              </dl>
              <div className="provider-alias-list">
                {governance.ai_gateway.route_aliases.map((route) => (
                  <div className="provider-alias-row" key={route.alias}>
                    <strong>{route.alias}</strong>
                    <span>{route.advisory_usage_domain}</span>
                    <small>{route.availability_status}</small>
                  </div>
                ))}
              </div>
            </section>

            <section className="provider-governance-section">
              <div className="panel-heading">
                <p className="eyebrow">Diagnostics</p>
                <DatabaseZap aria-hidden="true" />
              </div>
              <p className="projection-detail">
                Retained history:{" "}
                {governance.diagnostics.retained_history_available ? "yes" : "no"}
              </p>
              <div className="diagnostic-class-list">
                {governance.diagnostics.diagnostic_classes.map((item) => (
                  <span key={item}>{item}</span>
                ))}
              </div>
            </section>
          </div>

          <ProviderConfigurationPanel />
        </>
      ) : null}
    </section>
  );
}
