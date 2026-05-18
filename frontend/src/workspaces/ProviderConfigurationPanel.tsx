import { useEffect, useMemo, useState } from "react";
import {
  fetchProviderConfiguration,
  updateProviderPreference,
  type ProviderConfiguration,
} from "../api/runtime";

export function ProviderConfigurationPanel() {
  const [config, setConfig] = useState<ProviderConfiguration | null>(null);
  const price = useMemo(
    () => config?.resolutions.find((item) => item.capability === "price"),
    [config],
  );
  const fundamentals = useMemo(
    () => config?.resolutions.find((item) => item.capability === "fundamentals"),
    [config],
  );

  useEffect(() => {
    fetchProviderConfiguration().then(setConfig).catch(() => setConfig(null));
  }, []);

  if (!config || !price || !fundamentals) return null;

  const fundamentalsOptions = config.providers
    .filter((provider) => provider.capabilities.includes("fundamentals"))
    .map((provider) => provider.provider_id);

  return (
    <section className="provider-configuration-panel" aria-label="Provider configuration">
      <div className="panel-heading">
        <p className="eyebrow">Provider Configuration</p>
        <span className="field-authority-badge authority-advisory">Advisory</span>
      </div>
      <div className="provider-capability-section">
        <p className="provider-capability-label">Price provider</p>
        <p className="projection-detail">
          Selected: {price.selected_provider_id ?? "unavailable"} / fallback order:{" "}
          {price.fallback_provider_ids.join(", ") || "none"}
        </p>
      </div>
      <label>
        Fundamentals provider
        <select
          value={fundamentals.preferred_provider_id}
          onChange={(event) => {
            const preferred = event.target.value;
            const fallbacks = fundamentalsOptions.filter((item) => item !== preferred);
            updateProviderPreference("fundamentals", preferred, fallbacks)
              .then(setConfig)
              .catch(() => undefined);
          }}
        >
          {fundamentalsOptions.map((option) => (
            <option key={option} value={option}>{option}</option>
          ))}
        </select>
      </label>
      <p className="projection-detail">
        Selected: {fundamentals.selected_provider_id ?? "unavailable"} / fallback order:{" "}
        {fundamentals.fallback_provider_ids.join(", ") || "none"}
      </p>
    </section>
  );
}
