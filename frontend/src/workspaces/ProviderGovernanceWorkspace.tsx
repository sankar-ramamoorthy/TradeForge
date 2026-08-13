import { DatabaseZap, Network, ShieldCheck } from "lucide-react";
import { useEffect, useState } from "react";

import {
  fetchAdvisoryModelSelection,
  fetchLLMProviderSecretInjection,
  fetchProviderGovernance,
  smokeTestAdvisoryRoute,
  updateAdvisoryModelSelection,
  type AdvisoryModelSelection,
  type AdvisoryRouteSmokeTestResponse,
  type LLMProviderSecretInjection,
  type ProviderGovernance,
} from "../api/runtime";
import { ProviderConfigurationPanel } from "./ProviderConfigurationPanel";

const llmProviderOptions = [
  { provider_id: "llm_groq", display_name: "Groq" },
  { provider_id: "llm_nvidia_nim", display_name: "NVIDIA NIM" },
  { provider_id: "llm_openai", display_name: "OpenAI" },
  { provider_id: "llm_anthropic", display_name: "Anthropic" },
  { provider_id: "llm_google", display_name: "Google" },
  { provider_id: "ollama", display_name: "Ollama" },
  { provider_id: "ollama-local", display_name: "Ollama Local" },
  { provider_id: "ollama-remote", display_name: "Ollama Remote" },
  { provider_id: "ollama-auto", display_name: "Ollama Auto" },
];

export function ProviderGovernanceWorkspace() {
  const [governance, setGovernance] = useState<ProviderGovernance | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [smokeTest, setSmokeTest] =
    useState<AdvisoryRouteSmokeTestResponse | null>(null);
  const [modelSelection, setModelSelection] =
    useState<AdvisoryModelSelection | null>(null);
  const [primaryProviderId, setPrimaryProviderId] = useState("llm_groq");
  const [primaryModel, setPrimaryModel] = useState("");
  const [fallbackProviderId, setFallbackProviderId] = useState("");
  const [fallbackModel, setFallbackModel] = useState("");
  const [modelSelectionSaving, setModelSelectionSaving] = useState(false);
  const [modelSelectionError, setModelSelectionError] = useState<string | null>(
    null,
  );
  const [secretInjection, setSecretInjection] =
    useState<LLMProviderSecretInjection | null>(null);
  const [smokeTestRunning, setSmokeTestRunning] = useState(false);
  const [smokeTestError, setSmokeTestError] = useState<string | null>(null);

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
    fetchAdvisoryModelSelection(controller.signal)
      .then((data) => {
        setModelSelection(data);
        setPrimaryProviderId(data.selected_primary_provider_id ?? "llm_groq");
        setPrimaryModel(data.selected_primary_model ?? "");
        setFallbackProviderId(data.selected_fallback_provider_id ?? "");
        setFallbackModel(data.selected_fallback_model ?? "");
        setModelSelectionError(null);
      })
      .catch((err: unknown) => {
        if (err instanceof DOMException && err.name === "AbortError") return;
        setModelSelectionError(
          err instanceof Error ? err.message : "Advisory model discovery failed",
        );
      });
    fetchLLMProviderSecretInjection(controller.signal)
      .then(setSecretInjection)
      .catch(() => setSecretInjection(null));
    return () => controller.abort();
  }, []);

  const refreshGovernance = () => {
    fetchProviderGovernance()
      .then((data) => setGovernance(data))
      .catch(() => undefined);
    fetchLLMProviderSecretInjection()
      .then(setSecretInjection)
      .catch(() => undefined);
  };

  const handleModelSelectionSave = () => {
    if (!primaryModel) return;
    setModelSelectionSaving(true);
    setModelSelectionError(null);
    updateAdvisoryModelSelection({
      primary_provider_id: primaryProviderId,
      primary_model: primaryModel,
      fallback_provider_id: fallbackModel ? fallbackProviderId || primaryProviderId : null,
      fallback_model: fallbackModel || null,
    })
      .then((result) => {
        setModelSelection(result);
        setPrimaryProviderId(result.selected_primary_provider_id ?? "llm_groq");
        setPrimaryModel(result.selected_primary_model ?? "");
        setFallbackProviderId(result.selected_fallback_provider_id ?? "");
        setFallbackModel(result.selected_fallback_model ?? "");
        refreshGovernance();
      })
      .catch((err: unknown) => {
        setModelSelectionError(
          err instanceof Error ? err.message : "Advisory model selection failed",
        );
      })
      .finally(() => setModelSelectionSaving(false));
  };

  const handleSmokeTest = () => {
    setSmokeTestRunning(true);
    setSmokeTestError(null);
    setSmokeTest(null);
    smokeTestAdvisoryRoute()
      .then((result) => {
        setSmokeTest(result);
        setSmokeTestError(null);
      })
      .catch((err: unknown) => {
        setSmokeTestError(
          err instanceof Error ? err.message : "Advisory route smoke test failed",
        );
      })
      .finally(() => setSmokeTestRunning(false));
  };

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
                  <dt>Fallback</dt>
                  <dd>{governance.ai_gateway.fallback_model ?? "not configured"}</dd>
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
              {modelSelection ? (
                <div className="provider-model-selection">
                  <div className="panel-heading">
                    <p className="eyebrow">Model Selection</p>
                    <span>{modelSelection.discovery_status}</span>
                  </div>
                  <label>
                    Primary Provider
                    <select
                      disabled={modelSelectionSaving}
                      onChange={(event) => setPrimaryProviderId(event.target.value)}
                      value={primaryProviderId}
                    >
                      {llmProviderOptions.map((provider) => (
                        <option key={provider.provider_id} value={provider.provider_id}>
                          {provider.display_name}
                        </option>
                      ))}
                    </select>
                  </label>
                  <label>
                    Primary Model
                    <input
                      disabled={modelSelectionSaving}
                      onChange={(event) => setPrimaryModel(event.target.value)}
                      value={primaryModel}
                    />
                  </label>
                  <label>
                    Fallback Provider
                    <select
                      disabled={modelSelectionSaving || !fallbackModel}
                      onChange={(event) => setFallbackProviderId(event.target.value)}
                      value={fallbackProviderId}
                    >
                      <option value="">None</option>
                      {llmProviderOptions.map((provider) => (
                        <option key={provider.provider_id} value={provider.provider_id}>
                          {provider.display_name}
                        </option>
                      ))}
                    </select>
                  </label>
                  <label>
                    Fallback Model
                    <input
                      disabled={modelSelectionSaving}
                      onChange={(event) => setFallbackModel(event.target.value)}
                      value={fallbackModel}
                    />
                  </label>
                  <button
                    className="lifecycle-action-btn"
                    disabled={!primaryModel || modelSelectionSaving}
                    onClick={handleModelSelectionSave}
                    type="button"
                  >
                    {modelSelectionSaving ? "Saving..." : "Save Model Selection"}
                  </button>
                </div>
              ) : null}
              {modelSelectionError ? (
                <div className="runtime-error">{modelSelectionError}</div>
              ) : null}
              {secretInjection ? (
                <div className="provider-secret-injection-list">
                  <div className="panel-heading">
                    <p className="eyebrow">Provider Secrets</p>
                    <span>{secretInjection.runtime_decryption_boundary}</span>
                  </div>
                  {secretInjection.provider_secrets.map((item) => (
                    <div className="provider-alias-row" key={item.provider_id}>
                      <strong>{item.display_name}</strong>
                      <span>{item.litellm_environment_variable}</span>
                      <small>
                        {item.available_for_runtime_injection
                          ? "ready"
                          : item.configured
                            ? "configured"
                            : "missing"}
                      </small>
                    </div>
                  ))}
                </div>
              ) : null}
              <div className="provider-governance-action">
                <button
                  className="lifecycle-action-btn"
                  disabled={smokeTestRunning}
                  onClick={handleSmokeTest}
                  type="button"
                >
                  {smokeTestRunning ? "Testing advisory route..." : "Test Advisory Route"}
                </button>
                {smokeTestError ? (
                  <div className="runtime-error">{smokeTestError}</div>
                ) : null}
                {smokeTest ? (
                  <div className="projection-detail">
                    <p>Status: {smokeTest.status}</p>
                    <p>{smokeTest.diagnostic_message}</p>
                    {smokeTest.model_id ? <p>Model: {smokeTest.model_id}</p> : null}
                  </div>
                ) : null}
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
