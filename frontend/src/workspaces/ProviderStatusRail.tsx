import { Settings } from "lucide-react";
import { useEffect, useMemo, useState } from "react";

import {
  fetchProviderConfiguration,
  fetchProviderGovernanceAiGateway,
  type ProviderConfiguration,
  type ProviderGovernanceAiGateway,
} from "../api/runtime";

export function ProviderStatusRail({
  onNavigate,
}: {
  onNavigate: (href: string) => void;
}) {
  const [config, setConfig] = useState<ProviderConfiguration | null>(null);
  const [gateway, setGateway] = useState<ProviderGovernanceAiGateway | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    fetchProviderConfiguration(controller.signal)
      .then(setConfig)
      .catch(() => setConfig(null));
    fetchProviderGovernanceAiGateway(controller.signal)
      .then(setGateway)
      .catch(() => setGateway(null));
    return () => controller.abort();
  }, []);

  const price = useMemo(
    () => config?.resolutions.find((item) => item.capability === "price"),
    [config],
  );
  const fundamentals = useMemo(
    () => config?.resolutions.find((item) => item.capability === "fundamentals"),
    [config],
  );

  return (
    <section className="provider-status-rail" aria-label="Provider status">
      <div className="panel-heading">
        <p className="eyebrow">Provider Status</p>
        <span className="field-authority-badge authority-advisory">Operational</span>
      </div>

      <div className="provider-status-list">
        <ProviderStatusItem
          label="Price"
          selected={price?.selected_provider_id ?? "unavailable"}
          fallback={price?.fallback_provider_ids ?? []}
        />
        <ProviderStatusItem
          label="Fundamentals"
          selected={fundamentals?.selected_provider_id ?? "unavailable"}
          fallback={fundamentals?.fallback_provider_ids ?? []}
        />
        <ProviderStatusItem
          label="AI Gateway"
          selected={gateway?.status ?? "unknown"}
          fallback={gateway?.route_aliases.map((route) => route.alias) ?? []}
        />
      </div>

      <p className="projection-detail">
        Provider state is operational context. It does not own lifecycle truth.
      </p>

      <button
        className="provider-governance-link"
        onClick={() => onNavigate("/workspaces/provider-governance")}
        type="button"
      >
        <Settings aria-hidden="true" />
        <span>Provider Governance</span>
      </button>
    </section>
  );
}

function ProviderStatusItem({
  label,
  selected,
  fallback,
}: {
  label: string;
  selected: string;
  fallback: string[];
}) {
  return (
    <div className="provider-status-item">
      <span>{label}</span>
      <strong>{selected}</strong>
      <small>{fallback.length > 0 ? fallback.join(", ") : "no fallback"}</small>
    </div>
  );
}
