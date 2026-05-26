import { useEffect, useMemo, useState } from "react";
import {
  PROVIDER_CREDENTIAL_SCHEMAS,
  fetchCredentials,
  fetchProviderConfiguration,
  revokeCredential,
  updateCredential,
  updateProviderPreference,
  validateCredential,
  type CredentialListResponse,
  type CredentialStatus,
  type ProviderConfiguration,
} from "../api/runtime";

const CREDENTIAL_PROVIDERS = [
  "polygon",
  "alpaca",
  "fmp",
  "alpha_vantage",
  "litellm",
  "llm_groq",
  "llm_nvidia_nim",
  "llm_openai",
  "llm_anthropic",
  "llm_google",
] as const;
type CredentialProvider = (typeof CREDENTIAL_PROVIDERS)[number];

export function ProviderConfigurationPanel() {
  const [config, setConfig] = useState<ProviderConfiguration | null>(null);
  const [credList, setCredList] = useState<CredentialListResponse | null>(null);
  const [expandedProvider, setExpandedProvider] = useState<string | null>(null);
  const [formValues, setFormValues] = useState<Record<string, string>>({});
  const [saving, setSaving] = useState(false);
  const [toast, setToast] = useState<string | null>(null);

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
    fetchCredentials().then(setCredList).catch(() => setCredList(null));
  }, []);

  const showToast = (message: string) => {
    setToast(message);
    setTimeout(() => setToast(null), 3000);
  };

  const credForProvider = (providerId: string): CredentialStatus | undefined =>
    credList?.credentials.find((c) => c.provider_id === providerId);

  const toggleExpand = (providerId: string) => {
    if (expandedProvider === providerId) {
      setExpandedProvider(null);
      setFormValues({});
    } else {
      setExpandedProvider(providerId);
      setFormValues({});
    }
  };

  const handleSave = async (providerId: CredentialProvider) => {
    setSaving(true);
    try {
      const schema = PROVIDER_CREDENTIAL_SCHEMAS[providerId] ?? [];
      const filteredFields = Object.fromEntries(
        Object.entries(formValues).filter(([name, value]) => {
          const field = schema.find((item) => item.name === name);
          return !field?.optional || value.trim() !== "";
        }),
      );
      const updated = await updateCredential(providerId, filteredFields);
      setCredList((prev) =>
        prev
          ? {
              ...prev,
              credentials: prev.credentials.map((c) =>
                c.provider_id === providerId ? updated : c,
              ),
            }
          : prev,
      );
      setExpandedProvider(null);
      setFormValues({});
      showToast("Credential saved. Providers reloaded.");
      fetchProviderConfiguration().then(setConfig).catch(() => undefined);
    } catch (err) {
      showToast(err instanceof Error ? err.message : "Save failed.");
    } finally {
      setSaving(false);
    }
  };

  const handleRevoke = async (providerId: string) => {
    setSaving(true);
    try {
      const updated = await revokeCredential(providerId);
      setCredList((prev) =>
        prev
          ? {
              ...prev,
              credentials: prev.credentials.map((c) =>
                c.provider_id === providerId ? updated : c,
              ),
            }
          : prev,
      );
      showToast("Credential revoked. Providers reloaded.");
      fetchProviderConfiguration().then(setConfig).catch(() => undefined);
    } catch (err) {
      showToast(err instanceof Error ? err.message : "Revoke failed.");
    } finally {
      setSaving(false);
    }
  };

  const handleValidate = async (providerId: string) => {
    setSaving(true);
    try {
      const updated = await validateCredential(providerId);
      setCredList((prev) =>
        prev
          ? {
              ...prev,
              credentials: prev.credentials.map((c) =>
                c.provider_id === providerId ? updated : c,
              ),
            }
          : prev,
      );
      showToast("Credential validation complete.");
      fetchProviderConfiguration().then(setConfig).catch(() => undefined);
    } catch (err) {
      showToast(err instanceof Error ? err.message : "Validation failed.");
    } finally {
      setSaving(false);
    }
  };

  if (!config || !price || !fundamentals) return null;

  const fundamentalsOptions = config.providers
    .filter((provider) => provider.capabilities.includes("fundamentals"))
    .map((provider) => provider.provider_id);

  const masterKeyMissing = credList !== null && !credList.master_key_configured;

  return (
    <section className="provider-configuration-panel" aria-label="Provider configuration">
      {toast && (
        <div className="credential-toast" role="status">
          {toast}
        </div>
      )}

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
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
      </label>
      <p className="projection-detail">
        Selected: {fundamentals.selected_provider_id ?? "unavailable"} / fallback order:{" "}
        {fundamentals.fallback_provider_ids.join(", ") || "none"}
      </p>

      <div className="credential-management-section">
        <p className="provider-capability-label">Credentials</p>

        {masterKeyMissing && (
          <p className="credential-master-key-warning projection-detail">
            TRADEFORGE_MASTER_KEY is not set. Credential management is unavailable.
          </p>
        )}

        <div className="credential-provider-list">
          {/* yfinance — no credentials needed */}
          <div className="credential-provider-row">
            <span className="credential-provider-id">yfinance</span>
            <span className="credential-badge credential-badge--configured">
              no credentials required
            </span>
          </div>

          {CREDENTIAL_PROVIDERS.map((providerId) => {
            const cred = credForProvider(providerId);
            const schema = PROVIDER_CREDENTIAL_SCHEMAS[providerId] ?? [];
            const isExpanded = expandedProvider === providerId;
            const isConfigured = cred?.configured === true;

            return (
              <div key={providerId} className="credential-provider-row">
                <div className="credential-provider-header">
                  <span className="credential-provider-id">{providerId}</span>
                  <span
                    className={`credential-badge ${
                      isConfigured
                        ? "credential-badge--configured"
                        : "credential-badge--missing"
                    }`}
                  >
                    {cred?.status ?? (isConfigured ? "configured" : "not configured")}
                  </span>
                  {!masterKeyMissing && (
                    <button
                      className="credential-toggle-btn"
                      onClick={() => toggleExpand(providerId)}
                      type="button"
                    >
                      {isExpanded ? "Cancel" : isConfigured ? "Update" : "Add credential"}
                    </button>
                  )}
                  {isConfigured && !masterKeyMissing && !isExpanded && (
                    <button
                      className="credential-toggle-btn"
                      disabled={saving}
                      onClick={() => {
                        void handleValidate(providerId);
                      }}
                      type="button"
                    >
                      Validate
                    </button>
                  )}
                  {isConfigured && !masterKeyMissing && !isExpanded && (
                    <button
                      className="credential-revoke-btn"
                      onClick={() => handleRevoke(providerId)}
                      type="button"
                      disabled={saving}
                    >
                      Revoke
                    </button>
                  )}
                </div>

                {/* Masked field display when configured and not editing */}
                {isConfigured && !isExpanded && cred && cred.fields.length > 0 && (
                  <div className="credential-masked-fields">
                    {cred.last_validated_at ? (
                      <span className="credential-masked-field">
                        <span className="credential-field-name">validated:</span>{" "}
                        <span className="credential-field-value">
                          {new Date(cred.last_validated_at).toLocaleString()}
                        </span>
                      </span>
                    ) : null}
                    {cred.fields.map((field) => (
                      <span key={field.name} className="credential-masked-field">
                        <span className="credential-field-name">{field.name}:</span>{" "}
                        <span className="credential-field-value">
                          {field.masked_value ?? field.display_value ?? "—"}
                        </span>
                      </span>
                    ))}
                  </div>
                )}

                {/* Inline credential form */}
                {isExpanded && (
                  <form
                    className="credential-inline-form"
                    onSubmit={(e) => {
                      e.preventDefault();
                      void handleSave(providerId);
                    }}
                  >
                    {schema.map((fieldDef) => (
                      <label key={fieldDef.name} className="credential-field-label">
                        {fieldDef.label}
                        <input
                          type={fieldDef.secret ? "password" : "text"}
                          value={formValues[fieldDef.name] ?? ""}
                          onChange={(e) =>
                            setFormValues((prev) => ({
                              ...prev,
                              [fieldDef.name]: e.target.value,
                            }))
                          }
                          placeholder={
                            fieldDef.secret ? "••••••••" : `Enter ${fieldDef.label}`
                          }
                          autoComplete={fieldDef.secret ? "new-password" : "off"}
                          required={!fieldDef.optional}
                        />
                      </label>
                    ))}
                    <button type="submit" className="credential-save-btn" disabled={saving}>
                      {saving ? "Saving…" : "Save credential"}
                    </button>
                  </form>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
