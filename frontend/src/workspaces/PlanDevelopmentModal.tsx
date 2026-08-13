import { useEffect, useMemo, useState, type FormEvent } from "react";
import {
  fetchPlanImports,
  postCreatePlan,
  scanLocalPlanImports,
  type PlanImportMappedFields,
  type PlanImportPreview,
} from "../api/runtime";
import { type WorkspaceContext } from "../workspaceRouting";

type SubmitState = "idle" | "submitting" | "error";
type ImportFieldName =
  | "entry_rationale"
  | "stop_rationale"
  | "target_rationale"
  | "risk_notes"
  | "execution_assumptions"
  | "playbook_alignment";
type ImportFieldState = "accepted" | "edited";
const IMPORT_FIELD_NAMES: ImportFieldName[] = [
  "entry_rationale",
  "stop_rationale",
  "target_rationale",
  "risk_notes",
  "execution_assumptions",
  "playbook_alignment",
];

type Props = {
  context: Required<WorkspaceContext>;
  symbol: string;
  onSuccess: () => void;
  onCancel: () => void;
};

function ImportFieldBadge({ state }: { state: ImportFieldState }) {
  return (
    <span className="thesis-import-field-badge">
      {state === "edited" ? "Imported edited" : "Imported unchanged"}
    </span>
  );
}

function ListInput({
  label,
  items,
  onChange,
  placeholder,
  importState,
}: {
  label: string;
  items: string[];
  onChange: (items: string[]) => void;
  placeholder: string;
  importState?: ImportFieldState;
}) {
  function handleChange(index: number, value: string) {
    const next = [...items];
    next[index] = value;
    onChange(next);
  }

  function handleAdd() {
    onChange([...items, ""]);
  }

  function handleRemove(index: number) {
    onChange(items.filter((_, i) => i !== index));
  }

  return (
    <div className="thesis-list-input">
      <label className="thesis-field-label">
        {label}
        {importState ? <ImportFieldBadge state={importState} /> : null}
      </label>
      {items.map((item, index) => (
        <div className="thesis-list-row" key={index}>
          <input
            aria-label={`${label} item ${index + 1}`}
            className="thesis-list-item-input"
            onChange={(e) => handleChange(index, e.target.value)}
            placeholder={placeholder}
            type="text"
            value={item}
          />
          {items.length > 1 ? (
            <button
              aria-label={`Remove ${label} item ${index + 1}`}
              className="thesis-list-remove-btn"
              onClick={() => handleRemove(index)}
              type="button"
            >
              x
            </button>
          ) : null}
        </div>
      ))}
      <button className="thesis-list-add-btn" onClick={handleAdd} type="button">
        + Add
      </button>
    </div>
  );
}

function RationaleField({
  id,
  label,
  hint,
  placeholder,
  value,
  onChange,
  importState,
}: {
  id: string;
  label: string;
  hint: string;
  placeholder: string;
  value: string;
  onChange: (v: string) => void;
  importState?: ImportFieldState;
}) {
  return (
    <div className="thesis-field-group">
      <label className="thesis-field-label" htmlFor={id}>
        {label}
        <span className="thesis-field-required" aria-hidden="true"> *</span>
        {importState ? <ImportFieldBadge state={importState} /> : null}
      </label>
      <p className="thesis-field-hint">{hint}</p>
      <textarea
        className="thesis-narrative-input"
        id={id}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        required
        rows={5}
        value={value}
      />
    </div>
  );
}

function mappedPlanFieldHasValue(field: ImportFieldName, mapped: PlanImportMappedFields) {
  const value = mapped[field];
  return Array.isArray(value) ? value.length > 0 : Boolean(value);
}

function importedListEdited(current: string[], imported: string[] | undefined) {
  if (!imported) return false;
  const cleanCurrent = current.filter((item) => item.trim()).map((item) => item.trim());
  return JSON.stringify(cleanCurrent) !== JSON.stringify(imported);
}

function PlanImportPreviewPanel({
  context,
  symbol,
  onAccept,
  onReject,
  acceptedFields,
  rejectedFields,
}: {
  context: Required<WorkspaceContext>;
  symbol: string;
  onAccept: (artifact: PlanImportPreview, field: ImportFieldName) => void;
  onReject: (artifact: PlanImportPreview, field: ImportFieldName) => void;
  acceptedFields: ReadonlySet<string>;
  rejectedFields: ReadonlySet<string>;
}) {
  const [imports, setImports] = useState<PlanImportPreview[]>([]);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [scanMessage, setScanMessage] = useState<string | null>(null);
  const [scanning, setScanning] = useState(false);

  function loadImports(signal?: AbortSignal) {
    return fetchPlanImports(
      {
        persona_id: context.persona_id,
        workspace_id: context.workspace_id,
        decision_id: context.decision_id,
        symbol,
      },
      signal,
    ).then((response) => {
      setImports(response.imports);
      setLoadError(null);
      return response;
    });
  }

  useEffect(() => {
    const controller = new AbortController();
    loadImports(controller.signal).catch((err: unknown) => {
      if (err instanceof DOMException && err.name === "AbortError") return;
      setLoadError(err instanceof Error ? err.message : "Failed to load imports.");
    });
    return () => controller.abort();
  }, [context.persona_id, context.workspace_id, context.decision_id, symbol]);

  function handleScanLocalImports() {
    setScanning(true);
    setScanMessage(null);
    scanLocalPlanImports({
      persona_id: context.persona_id,
      workspace_id: context.workspace_id,
      decision_id: context.decision_id,
      symbol,
    })
      .then((result) => {
        setScanMessage(
          `Scanned ${result.scanned_count} file${result.scanned_count !== 1 ? "s" : ""}; imported ${result.imported_count}.`,
        );
        return loadImports();
      })
      .catch((err: unknown) => {
        setLoadError(err instanceof Error ? err.message : "Local import scan failed.");
      })
      .finally(() => setScanning(false));
  }

  const fields: { name: ImportFieldName; label: string }[] = [
    { name: "entry_rationale", label: "Entry Rationale" },
    { name: "stop_rationale", label: "Stop Rationale" },
    { name: "target_rationale", label: "Target Rationale" },
    { name: "risk_notes", label: "Risk Notes" },
    { name: "execution_assumptions", label: "Execution Assumptions" },
    { name: "playbook_alignment", label: "Playbook Alignment" },
  ];

  return (
    <aside className="thesis-import-panel" aria-label="Plan import preview">
      <div className="thesis-import-panel-header">
        <div>
          <p className="eyebrow">Import Preview</p>
          <h3>Advisory plan context</h3>
        </div>
        <div className="thesis-import-badges">
          <span className="field-authority-badge authority-advisory">Advisory</span>
          <span className="thesis-import-noncanonical">No execution authority</span>
        </div>
      </div>
      <div className="thesis-import-dropoff">
        <span>Drop plan markdown in imports/incoming.</span>
        <button
          className="thesis-import-action"
          disabled={scanning}
          onClick={handleScanLocalImports}
          type="button"
        >
          {scanning ? "Scanning..." : "Scan folder"}
        </button>
      </div>
      <p className="thesis-import-scan-message">
        Import cannot populate sizing, approve this plan, or authorize execution.
      </p>

      {loadError ? <div className="runtime-error">{loadError}</div> : null}
      {scanMessage ? <p className="thesis-import-scan-message">{scanMessage}</p> : null}
      {!loadError && imports.length === 0 ? (
        <p className="field-no-data">No eligible plan draft artifacts for {symbol}.</p>
      ) : null}

      {imports.map((artifact) => (
        <div className="thesis-import-card" key={artifact.artifact_id}>
          <div className="thesis-import-source">
            <strong>{artifact.title}</strong>
            <span>{artifact.source}</span>
            <span>{new Date(artifact.captured_at).toLocaleString()}</span>
          </div>
          <p className="thesis-import-provenance">{artifact.provenance_summary}</p>
          <div className="thesis-import-meta">
            <span>Uncertainty: {artifact.uncertainty_band}</span>
            <span>{artifact.caveats.length} caveat{artifact.caveats.length !== 1 ? "s" : ""}</span>
          </div>
          {artifact.caveats.length > 0 ? (
            <ul className="thesis-import-caveats">
              {artifact.caveats.map((caveat) => (
                <li key={caveat}>{caveat}</li>
              ))}
            </ul>
          ) : null}

          <div className="thesis-import-fields">
            {fields.map((field) => {
              if (!mappedPlanFieldHasValue(field.name, artifact.mapped_fields)) return null;
              const value = artifact.mapped_fields[field.name];
              const fieldKey = `${artifact.artifact_id}:${field.name}`;
              const accepted = acceptedFields.has(field.name);
              const rejected = rejectedFields.has(fieldKey);
              return (
                <div className="thesis-import-field" key={field.name}>
                  <div>
                    <span className="thesis-import-field-name">{field.label}</span>
                    <p>{Array.isArray(value) ? value.join("; ") : value}</p>
                  </div>
                  <div className="thesis-import-field-actions">
                    <button
                      className="thesis-import-action"
                      disabled={accepted}
                      onClick={() => onAccept(artifact, field.name)}
                      type="button"
                    >
                      {accepted ? "Accepted" : "Accept"}
                    </button>
                    <button
                      className="thesis-import-action secondary"
                      disabled={rejected}
                      onClick={() => onReject(artifact, field.name)}
                      type="button"
                    >
                      {rejected ? "Rejected" : "Reject"}
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ))}
    </aside>
  );
}

export function PlanDevelopmentModal({ context, symbol, onSuccess, onCancel }: Props) {
  const [entryRationale, setEntryRationale] = useState("");
  const [stopRationale, setStopRationale] = useState("");
  const [targetRationale, setTargetRationale] = useState("");
  const [sizingRationale, setSizingRationale] = useState("");
  const [executionAssumptions, setExecutionAssumptions] = useState<string[]>([""]);
  const [playbookAlignment, setPlaybookAlignment] = useState("");
  const [submitState, setSubmitState] = useState<SubmitState>("idle");
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [sourceArtifactId, setSourceArtifactId] = useState<string | null>(null);
  const [acceptedFields, setAcceptedFields] = useState<Set<ImportFieldName>>(new Set());
  const [rejectedFields, setRejectedFields] = useState<Set<string>>(new Set());
  const [importedBaselines, setImportedBaselines] = useState<
    Partial<Record<ImportFieldName, string | string[]>>
  >({});

  const editedImportFields = useMemo(() => {
    const edited: ImportFieldName[] = [];
    if (
      acceptedFields.has("entry_rationale") &&
      typeof importedBaselines.entry_rationale === "string" &&
      entryRationale.trim() !== importedBaselines.entry_rationale
    ) {
      edited.push("entry_rationale");
    }
    if (
      acceptedFields.has("stop_rationale") &&
      typeof importedBaselines.stop_rationale === "string" &&
      stopRationale.trim() !== importedBaselines.stop_rationale
    ) {
      edited.push("stop_rationale");
    }
    if (
      acceptedFields.has("target_rationale") &&
      typeof importedBaselines.target_rationale === "string" &&
      targetRationale.trim() !== importedBaselines.target_rationale
    ) {
      edited.push("target_rationale");
    }
    if (
      acceptedFields.has("risk_notes") &&
      importedListEdited(
        executionAssumptions,
        importedBaselines.risk_notes as string[] | undefined,
      )
    ) {
      edited.push("risk_notes");
    }
    if (
      acceptedFields.has("execution_assumptions") &&
      importedListEdited(
        executionAssumptions,
        importedBaselines.execution_assumptions as string[] | undefined,
      )
    ) {
      edited.push("execution_assumptions");
    }
    if (
      acceptedFields.has("playbook_alignment") &&
      typeof importedBaselines.playbook_alignment === "string" &&
      playbookAlignment.trim() !== importedBaselines.playbook_alignment
    ) {
      edited.push("playbook_alignment");
    }
    return edited;
  }, [
    acceptedFields,
    entryRationale,
    executionAssumptions,
    importedBaselines,
    playbookAlignment,
    stopRationale,
    targetRationale,
  ]);

  function importFieldState(field: ImportFieldName): ImportFieldState | undefined {
    if (!acceptedFields.has(field)) return undefined;
    return editedImportFields.includes(field) ? "edited" : "accepted";
  }

  function fieldHasValue(field: ImportFieldName) {
    if (field === "entry_rationale") return entryRationale.trim().length > 0;
    if (field === "stop_rationale") return stopRationale.trim().length > 0;
    if (field === "target_rationale") return targetRationale.trim().length > 0;
    if (field === "playbook_alignment") return playbookAlignment.trim().length > 0;
    return executionAssumptions.some((item) => item.trim());
  }

  function handleAcceptImport(artifact: PlanImportPreview, field: ImportFieldName) {
    if (sourceArtifactId && sourceArtifactId !== artifact.artifact_id) {
      window.alert("Finish or submit the current import source before using another.");
      return;
    }
    const incoming = artifact.mapped_fields[field];
    if (!incoming || (Array.isArray(incoming) && incoming.length === 0)) return;

    let mode: "replace" | "append" = "replace";
    if (fieldHasValue(field)) {
      const choice = window.prompt(
        "This draft field already has content. Type append, replace, or cancel.",
        "append",
      );
      if (choice === null || choice.toLowerCase() === "cancel") return;
      if (choice.toLowerCase() !== "append" && choice.toLowerCase() !== "replace") return;
      mode = choice.toLowerCase() as "replace" | "append";
    }

    if (field === "entry_rationale" && typeof incoming === "string") {
      const next = mode === "append" && entryRationale.trim()
        ? `${entryRationale.trim()}\n\n${incoming}`
        : incoming;
      setEntryRationale(next);
      setImportedBaselines((prev) => ({ ...prev, entry_rationale: next.trim() }));
    }
    if (field === "stop_rationale" && typeof incoming === "string") {
      const next = mode === "append" && stopRationale.trim()
        ? `${stopRationale.trim()}\n\n${incoming}`
        : incoming;
      setStopRationale(next);
      setImportedBaselines((prev) => ({ ...prev, stop_rationale: next.trim() }));
    }
    if (field === "target_rationale" && typeof incoming === "string") {
      const next = mode === "append" && targetRationale.trim()
        ? `${targetRationale.trim()}\n\n${incoming}`
        : incoming;
      setTargetRationale(next);
      setImportedBaselines((prev) => ({ ...prev, target_rationale: next.trim() }));
    }
    if (field === "risk_notes" && Array.isArray(incoming)) {
      const current = executionAssumptions.filter((item) => item.trim());
      const next = mode === "append" ? [...current, ...incoming] : incoming;
      setExecutionAssumptions(next);
      setImportedBaselines((prev) => ({ ...prev, risk_notes: next }));
    }
    if (field === "execution_assumptions" && Array.isArray(incoming)) {
      const current = executionAssumptions.filter((item) => item.trim());
      const next = mode === "append" ? [...current, ...incoming] : incoming;
      setExecutionAssumptions(next);
      setImportedBaselines((prev) => ({ ...prev, execution_assumptions: next }));
    }
    if (field === "playbook_alignment" && typeof incoming === "string") {
      const next = mode === "append" && playbookAlignment.trim()
        ? `${playbookAlignment.trim()}; ${incoming}`
        : incoming;
      setPlaybookAlignment(next);
      setImportedBaselines((prev) => ({ ...prev, playbook_alignment: next.trim() }));
    }

    setSourceArtifactId(artifact.artifact_id);
    setAcceptedFields((prev) => new Set([...prev, field]));
  }

  function handleRejectImport(artifact: PlanImportPreview, field: ImportFieldName) {
    if (sourceArtifactId && sourceArtifactId !== artifact.artifact_id) {
      window.alert("Finish or submit the current import source before using another.");
      return;
    }
    setSourceArtifactId(artifact.artifact_id);
    setRejectedFields((prev) => new Set([...prev, `${artifact.artifact_id}:${field}`]));
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitState("submitting");
    setSubmitError(null);

    const cleanAssumptions = executionAssumptions.filter((a) => a.trim());

    if (!entryRationale.trim()) {
      setSubmitError("Entry rationale is required.");
      setSubmitState("error");
      return;
    }
    if (!stopRationale.trim()) {
      setSubmitError("Stop rationale is required.");
      setSubmitState("error");
      return;
    }
    if (!targetRationale.trim()) {
      setSubmitError("Target rationale is required.");
      setSubmitState("error");
      return;
    }
    if (!sizingRationale.trim()) {
      setSubmitError("Sizing rationale is required.");
      setSubmitState("error");
      return;
    }
    if (cleanAssumptions.length === 0) {
      setSubmitError("At least one execution assumption is required.");
      setSubmitState("error");
      return;
    }

    const rejectedImportFieldNames = Array.from(rejectedFields)
      .map((field) => field.split(":")[1])
      .filter((field): field is ImportFieldName =>
        IMPORT_FIELD_NAMES.includes(field as ImportFieldName),
      );

    postCreatePlan({
      decision_id: context.decision_id,
      symbol,
      entry_rationale: entryRationale.trim(),
      stop_rationale: stopRationale.trim(),
      target_rationale: targetRationale.trim(),
      sizing_rationale: sizingRationale.trim(),
      execution_assumptions: cleanAssumptions,
      playbook_alignment: playbookAlignment.trim(),
      persona_id: context.persona_id,
      workspace_id: context.workspace_id,
      source_advisory_artifact_id: sourceArtifactId ?? undefined,
      accepted_import_fields: Array.from(acceptedFields),
      edited_import_fields: editedImportFields,
      rejected_import_fields: Array.from(new Set(rejectedImportFieldNames)),
      import_acceptance_intent: sourceArtifactId
        ? "operator_selectively_incorporates_advisory_cognition"
        : undefined,
    })
      .then(() => {
        setSubmitState("idle");
        onSuccess();
      })
      .catch((err: unknown) => {
        setSubmitState("error");
        setSubmitError(
          err instanceof Error ? err.message : "Plan creation failed.",
        );
      });
  }

  return (
    <div
      aria-labelledby="plan-modal-title"
      aria-modal="true"
      className="thesis-modal-overlay"
      role="dialog"
    >
      <div className="thesis-modal-surface">
        <div className="thesis-modal-header">
          <div>
            <p className="eyebrow">Trade Plan - {symbol}</p>
            <h2 id="plan-modal-title">Define your execution plan</h2>
            <p className="thesis-modal-description">
              Capture structured execution intent before moving to approval.
              This becomes a replayable cognitive artifact attached to the Plan event.
            </p>
          </div>
          <button
            aria-label="Cancel plan creation"
            className="thesis-modal-close"
            onClick={onCancel}
            type="button"
          >
            x
          </button>
        </div>

        <form className="thesis-modal-form" onSubmit={handleSubmit}>
          <div className="thesis-modal-grid">
            <div className="thesis-authoring-region">
              <RationaleField
                hint="Why this entry point and price level - what confirms the setup."
                id="plan-entry"
                importState={importFieldState("entry_rationale")}
                label="Entry Rationale"
                onChange={setEntryRationale}
                placeholder="e.g. Buy on a pullback to the 20-day MA with a close above prior resistance..."
                value={entryRationale}
              />

              <RationaleField
                hint="Why this stop level represents thesis invalidation - not arbitrary."
                id="plan-stop"
                importState={importFieldState("stop_rationale")}
                label="Stop Rationale"
                onChange={setStopRationale}
                placeholder="e.g. Close below the 200-day MA on above-average volume invalidates the breakout..."
                value={stopRationale}
              />

              <RationaleField
                hint="Why this target represents thesis fulfillment at an acceptable risk/reward."
                id="plan-target"
                importState={importFieldState("target_rationale")}
                label="Target Rationale"
                onChange={setTargetRationale}
                placeholder="e.g. Prior resistance at $200 gives a 2:1 risk/reward at this entry..."
                value={targetRationale}
              />

              <RationaleField
                hint="How position size was determined relative to conviction and risk tolerance."
                id="plan-sizing"
                label="Sizing Rationale"
                onChange={setSizingRationale}
                placeholder="e.g. 2% portfolio risk at the stop distance gives approximately 150 shares..."
                value={sizingRationale}
              />

              <ListInput
                importState={
                  importFieldState("execution_assumptions")
                  ?? importFieldState("risk_notes")
                }
                items={executionAssumptions}
                label="Execution Assumptions *"
                onChange={setExecutionAssumptions}
                placeholder="e.g. Sufficient liquidity available at entry level"
              />

              <div className="thesis-field-group">
                <label className="thesis-field-label" htmlFor="plan-playbook">
                  Playbook Alignment
                  <span className="thesis-field-optional"> (optional)</span>
                  {importFieldState("playbook_alignment") ? (
                    <ImportFieldBadge
                      state={importFieldState("playbook_alignment") ?? "accepted"}
                    />
                  ) : null}
                </label>
                <p className="thesis-field-hint">
                  Which operational playbook this plan follows.
                </p>
                <input
                  className="thesis-regime-input"
                  id="plan-playbook"
                  onChange={(e) => setPlaybookAlignment(e.target.value)}
                  placeholder="e.g. swing-breakout-v1, mean-reversion, sector-rotation"
                  type="text"
                  value={playbookAlignment}
                />
              </div>
            </div>

            <PlanImportPreviewPanel
              acceptedFields={acceptedFields}
              context={context}
              onAccept={handleAcceptImport}
              onReject={handleRejectImport}
              rejectedFields={rejectedFields}
              symbol={symbol}
            />
          </div>

          {submitError ? (
            <div className="runtime-error" role="alert">
              {submitError}
            </div>
          ) : null}

          {sourceArtifactId ? (
            <p className="thesis-import-submit-summary">
              Provenance: {acceptedFields.size} accepted, {editedImportFields.length} edited,
              {" "} {rejectedFields.size} rejected. Sizing remains manually authored.
            </p>
          ) : null}

          <div className="thesis-modal-actions">
            <button
              className="lifecycle-action-btn-secondary"
              onClick={onCancel}
              type="button"
            >
              Cancel
            </button>
            <button
              className="lifecycle-action-btn"
              disabled={submitState === "submitting"}
              type="submit"
            >
              {submitState === "submitting" ? "Creating plan..." : "Create Plan"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
