import { useEffect, useMemo, useState, type FormEvent } from "react";
import {
  fetchThesisImports,
  postDevelopThesis,
  scanLocalThesisImports,
  type ThesisImportMappedFields,
  type ThesisImportPreview,
  type ThesisImportSourceReference,
} from "../api/runtime";
import { type WorkspaceContext } from "../workspaceRouting";
import { FundamentalsContextPanel } from "./FundamentalsContextPanel";

type SubmitState = "idle" | "submitting" | "error";
type ImportFieldName =
  | "narrative"
  | "catalysts"
  | "assumptions"
  | "invalidation_conditions";
type ImportFieldState = "accepted" | "edited";

type Props = {
  context: Required<WorkspaceContext>;
  symbol: string;
  onSuccess: (decisionId: string) => void;
  onCancel: () => void;
};

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
              ×
            </button>
          ) : null}
        </div>
      ))}
      <button
        className="thesis-list-add-btn"
        onClick={handleAdd}
        type="button"
      >
        + Add
      </button>
    </div>
  );
}

function ImportFieldBadge({ state }: { state: ImportFieldState }) {
  return (
    <span className="thesis-import-field-badge">
      {state === "edited" ? "Imported edited" : "Imported unchanged"}
    </span>
  );
}

function fieldHasValue(
  field: ImportFieldName,
  values: {
    narrative: string;
    catalysts: string[];
    assumptions: string[];
    invalidation_conditions: string[];
  },
) {
  if (field === "narrative") return values.narrative.trim().length > 0;
  return values[field].some((item) => item.trim());
}

function mappedFieldHasValue(field: ImportFieldName, mapped: ThesisImportMappedFields) {
  const value = mapped[field];
  return Array.isArray(value) ? value.length > 0 : Boolean(value);
}

function importedListEdited(current: string[], imported: string[] | undefined) {
  if (!imported) return false;
  const cleanCurrent = current.filter((item) => item.trim()).map((item) => item.trim());
  return JSON.stringify(cleanCurrent) !== JSON.stringify(imported);
}

function SourceReferenceList({
  references,
}: {
  references: ThesisImportSourceReference[];
}) {
  if (references.length === 0) return null;

  return (
    <div className="thesis-import-source-references">
      <span className="thesis-import-field-name">Sources</span>
      <ul>
        {references.map((reference) => (
          <li key={`${reference.source_kind}:${reference.source_id}`}>
            <span>{reference.summary || reference.source_id}</span>
            {reference.source_uri ? (
              <a href={reference.source_uri} rel="noreferrer" target="_blank">
                {reference.source_uri}
              </a>
            ) : (
              <small>{reference.source_kind}: {reference.source_id}</small>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

function EvidenceLinks({ links }: { links: string[] }) {
  if (links.length === 0) return null;

  return (
    <div className="thesis-import-source-references">
      <span className="thesis-import-field-name">Evidence Links</span>
      <ul>
        {links.map((link) => (
          <li key={link}>
            <a href={link} rel="noreferrer" target="_blank">{link}</a>
          </li>
        ))}
      </ul>
    </div>
  );
}

function ThesisImportPreviewPanel({
  context,
  symbol,
  onAccept,
  onReject,
  acceptedFields,
  rejectedFields,
}: {
  context: Required<WorkspaceContext>;
  symbol: string;
  onAccept: (artifact: ThesisImportPreview, field: ImportFieldName) => void;
  onReject: (artifact: ThesisImportPreview, field: ImportFieldName) => void;
  acceptedFields: ReadonlySet<string>;
  rejectedFields: ReadonlySet<string>;
}) {
  const [imports, setImports] = useState<ThesisImportPreview[]>([]);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [scanMessage, setScanMessage] = useState<string | null>(null);
  const [scanning, setScanning] = useState(false);

  function loadImports(signal?: AbortSignal) {
    return fetchThesisImports(
      {
        persona_id: context.persona_id,
        workspace_id: context.workspace_id,
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
    loadImports(controller.signal)
      .catch((err: unknown) => {
        if (err instanceof DOMException && err.name === "AbortError") return;
        setLoadError(err instanceof Error ? err.message : "Failed to load imports.");
      });
    return () => controller.abort();
  }, [context.persona_id, context.workspace_id, symbol]);

  function handleScanLocalImports() {
    setScanning(true);
    setScanMessage(null);
    scanLocalThesisImports({
      persona_id: context.persona_id,
      workspace_id: context.workspace_id,
      symbol,
    })
      .then((result) => {
        const details = result.file_statuses
          .map((status) => `${status.file}: ${status.status} - ${status.reason}`)
          .join("\n");
        setScanMessage(
          [
            `Received ${result.received_count} file${result.received_count !== 1 ? "s" : ""}; imported ${result.imported_count}; duplicates ${result.duplicate_count}; rejected ${result.rejected_count}.`,
            details,
          ]
            .filter(Boolean)
            .join("\n"),
        );
        return loadImports();
      })
      .catch((err: unknown) => {
        setLoadError(err instanceof Error ? err.message : "Local import scan failed.");
      })
      .finally(() => setScanning(false));
  }

  const fields: { name: ImportFieldName; label: string }[] = [
    { name: "narrative", label: "Narrative" },
    { name: "catalysts", label: "Catalysts" },
    { name: "assumptions", label: "Assumptions" },
    { name: "invalidation_conditions", label: "Invalidation" },
  ];

  return (
    <aside className="thesis-import-panel" aria-label="Thesis import preview">
      <div className="thesis-import-panel-header">
        <div>
          <p className="eyebrow">Import Preview</p>
          <h3>Advisory draft context</h3>
        </div>
        <div className="thesis-import-badges">
          <span className="field-authority-badge authority-advisory">Advisory</span>
          <span className="thesis-import-noncanonical">Non-canonical</span>
        </div>
      </div>
      <div className="thesis-import-dropoff">
        <span>Drop `.tf-thesis-draft.json` transfers or legacy thesis markdown in imports/incoming. Preview is read-only; Develop Thesis is the lifecycle action.</span>
        <button
          className="thesis-import-action"
          disabled={scanning}
          onClick={handleScanLocalImports}
          type="button"
        >
          {scanning ? "Scanning..." : "Scan folder"}
        </button>
      </div>

      {loadError ? <div className="runtime-error">{loadError}</div> : null}
      {scanMessage ? <p className="thesis-import-scan-message">{scanMessage}</p> : null}
      {!loadError && imports.length === 0 ? (
        <p className="field-no-data">No eligible thesis draft artifacts for {symbol}.</p>
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
            <span>{artifact.source_references.length} source{artifact.source_references.length !== 1 ? "s" : ""}</span>
          </div>
          <SourceReferenceList references={artifact.source_references} />
          <EvidenceLinks links={artifact.mapped_fields.evidence_links} />
          {artifact.mapped_fields.notes ? (
            <div className="thesis-import-source-references">
              <span className="thesis-import-field-name">Notes</span>
              <p>{artifact.mapped_fields.notes}</p>
            </div>
          ) : null}
          {artifact.caveats.length > 0 ? (
            <ul className="thesis-import-caveats">
              {artifact.caveats.map((caveat) => (
                <li key={caveat}>{caveat}</li>
              ))}
            </ul>
          ) : null}

          <div className="thesis-import-fields">
            {fields.map((field) => {
              if (!mappedFieldHasValue(field.name, artifact.mapped_fields)) return null;
              const value = artifact.mapped_fields[field.name];
              const fieldKey = `${artifact.artifact_id}:${field.name}`;
              const accepted = acceptedFields.has(field.name);
              const rejected = rejectedFields.has(fieldKey);
              return (
                <div className="thesis-import-field" key={field.name}>
                  <div>
                    <span className="thesis-import-field-name">{field.label}</span>
                    <p>
                      {Array.isArray(value)
                        ? value.join("; ")
                        : value}
                    </p>
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

export function ThesisDevelopmentModal({ context, symbol, onSuccess, onCancel }: Props) {
  const [narrative, setNarrative] = useState("");
  const [catalysts, setCatalysts] = useState<string[]>([""]);
  const [assumptions, setAssumptions] = useState<string[]>([""]);
  const [invalidationConditions, setInvalidationConditions] = useState<string[]>([""]);
  const [confidenceLevel, setConfidenceLevel] = useState<number>(3);
  const [regimeAlignment, setRegimeAlignment] = useState("");
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
      acceptedFields.has("narrative") &&
      typeof importedBaselines.narrative === "string" &&
      narrative.trim() !== importedBaselines.narrative
    ) {
      edited.push("narrative");
    }
    if (
      acceptedFields.has("catalysts") &&
      importedListEdited(catalysts, importedBaselines.catalysts as string[] | undefined)
    ) {
      edited.push("catalysts");
    }
    if (
      acceptedFields.has("assumptions") &&
      importedListEdited(assumptions, importedBaselines.assumptions as string[] | undefined)
    ) {
      edited.push("assumptions");
    }
    if (
      acceptedFields.has("invalidation_conditions") &&
      importedListEdited(
        invalidationConditions,
        importedBaselines.invalidation_conditions as string[] | undefined,
      )
    ) {
      edited.push("invalidation_conditions");
    }
    return edited;
  }, [acceptedFields, assumptions, catalysts, importedBaselines, invalidationConditions, narrative]);

  function importFieldState(field: ImportFieldName): ImportFieldState | undefined {
    if (!acceptedFields.has(field)) return undefined;
    return editedImportFields.includes(field) ? "edited" : "accepted";
  }

  function handleAcceptImport(artifact: ThesisImportPreview, field: ImportFieldName) {
    if (sourceArtifactId && sourceArtifactId !== artifact.artifact_id) {
      window.alert("Finish or submit the current import source before using another.");
      return;
    }
    const currentValues = {
      narrative,
      catalysts,
      assumptions,
      invalidation_conditions: invalidationConditions,
    };
    const incoming = artifact.mapped_fields[field];
    if (!incoming || (Array.isArray(incoming) && incoming.length === 0)) return;

    let mode: "replace" | "append" = "replace";
    if (fieldHasValue(field, currentValues)) {
      const choice = window.prompt(
        "This draft field already has content. Type append, replace, or cancel.",
        "append",
      );
      if (choice === null || choice.toLowerCase() === "cancel") return;
      if (choice.toLowerCase() !== "append" && choice.toLowerCase() !== "replace") return;
      mode = choice.toLowerCase() as "replace" | "append";
    }

    if (field === "narrative" && typeof incoming === "string") {
      const next =
        mode === "append" && narrative.trim()
          ? `${narrative.trim()}\n\n${incoming}`
          : incoming;
      setNarrative(next);
      setImportedBaselines((prev) => ({ ...prev, narrative: next.trim() }));
    } else if (Array.isArray(incoming)) {
      const existing = currentValues[field];
      const current = Array.isArray(existing)
        ? existing.filter((item) => item.trim())
        : [];
      const next = mode === "append" ? [...current, ...incoming] : incoming;
      if (field === "catalysts") setCatalysts(next);
      if (field === "assumptions") setAssumptions(next);
      if (field === "invalidation_conditions") setInvalidationConditions(next);
      setImportedBaselines((prev) => ({ ...prev, [field]: next }));
    }
    setSourceArtifactId(artifact.artifact_id);
    setAcceptedFields((prev) => new Set([...prev, field]));
  }

  function handleRejectImport(artifact: ThesisImportPreview, field: ImportFieldName) {
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

    const cleanCatalysts = catalysts.filter((c) => c.trim());
    const cleanAssumptions = assumptions.filter((a) => a.trim());
    const cleanInvalidation = invalidationConditions.filter((i) => i.trim());

    if (!narrative.trim()) {
      setSubmitError("Thesis narrative is required.");
      setSubmitState("error");
      return;
    }
    if (narrative.trim().length < 10) {
      setSubmitError("Thesis narrative is too short — write at least a sentence explaining the core argument.");
      setSubmitState("error");
      return;
    }
    if (cleanCatalysts.length === 0) {
      setSubmitError("At least one catalyst is required.");
      setSubmitState("error");
      return;
    }
    if (cleanAssumptions.length === 0) {
      setSubmitError("At least one assumption is required.");
      setSubmitState("error");
      return;
    }
    if (cleanInvalidation.length === 0) {
      setSubmitError("At least one invalidation condition is required.");
      setSubmitState("error");
      return;
    }

    const rejectedImportFieldNames = Array.from(rejectedFields)
      .map((field) => field.split(":")[1])
      .filter((field): field is ImportFieldName =>
        ["narrative", "catalysts", "assumptions", "invalidation_conditions"].includes(field),
      );

    postDevelopThesis({
      decision_id: context.decision_id,
      symbol,
      narrative: narrative.trim(),
      catalysts: cleanCatalysts,
      assumptions: cleanAssumptions,
      invalidation_conditions: cleanInvalidation,
      confidence_level: confidenceLevel,
      regime_alignment: regimeAlignment.trim(),
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
      .then((response) => {
        setSubmitState("idle");
        onSuccess(response.decision_id);
      })
      .catch((err: unknown) => {
        setSubmitState("error");
        setSubmitError(
          err instanceof Error ? err.message : "Thesis development failed.",
        );
      });
  }

  const CONFIDENCE_LABELS: Record<number, string> = {
    1: "Speculative",
    2: "Low",
    3: "Moderate",
    4: "High",
    5: "Conviction",
  };

  return (
    <div
      aria-labelledby="thesis-modal-title"
      aria-modal="true"
      className="thesis-modal-overlay"
      role="dialog"
    >
      <div className="thesis-modal-surface">
        <div className="thesis-modal-header">
          <div>
            <p className="eyebrow">Thesis Development — {symbol}</p>
            <h2 id="thesis-modal-title">Define your thesis</h2>
            <p className="thesis-modal-description">
              Capture the structured reasoning behind this idea. This becomes
              a replayable cognitive artifact attached to the lifecycle event.
            </p>
          </div>
          <button
            aria-label="Cancel thesis development"
            className="thesis-modal-close"
            onClick={onCancel}
            type="button"
          >
            ×
          </button>
        </div>

        <FundamentalsContextPanel symbol={symbol} />

        <form className="thesis-modal-form" onSubmit={handleSubmit}>
          <div className="thesis-modal-grid">
            <div className="thesis-authoring-region">
              <div className="thesis-field-group">
            <label className="thesis-field-label" htmlFor="thesis-narrative">
              Thesis Narrative
              <span className="thesis-field-required" aria-hidden="true"> *</span>
              {importFieldState("narrative") ? (
                <ImportFieldBadge state={importFieldState("narrative")!} />
              ) : null}
            </label>
            <p className="thesis-field-hint">
              The core argument for why this idea has merit.
            </p>
            <textarea
              className="thesis-narrative-input"
              id="thesis-narrative"
              onChange={(e) => setNarrative(e.target.value)}
              placeholder="e.g. AAPL is testing the 200-day MA with strong institutional accumulation visible in the tape..."
              required
              rows={6}
              value={narrative}
            />
          </div>

              <ListInput
                items={catalysts}
                label="Catalysts *"
                onChange={setCatalysts}
                placeholder="e.g. Strong earnings guidance"
                importState={importFieldState("catalysts")}
              />

              <ListInput
                items={assumptions}
                label="Assumptions *"
                onChange={setAssumptions}
                placeholder="e.g. Market remains risk-on"
                importState={importFieldState("assumptions")}
              />

              <ListInput
                items={invalidationConditions}
                label="Invalidation Conditions *"
                onChange={setInvalidationConditions}
                placeholder="e.g. Break below 200-day MA on volume"
                importState={importFieldState("invalidation_conditions")}
              />

              <div className="thesis-field-group">
            <label className="thesis-field-label" htmlFor="thesis-confidence">
              Conviction Level: {CONFIDENCE_LABELS[confidenceLevel]} ({confidenceLevel}/5)
            </label>
            <input
              className="thesis-confidence-slider"
              id="thesis-confidence"
              max={5}
              min={1}
              onChange={(e) => setConfidenceLevel(Number(e.target.value))}
              step={1}
              type="range"
              value={confidenceLevel}
            />
            <div className="thesis-confidence-scale" aria-hidden="true">
              <span>Speculative</span>
              <span>Conviction</span>
            </div>
          </div>

              <div className="thesis-field-group">
            <label className="thesis-field-label" htmlFor="thesis-regime">
              Regime Alignment
              <span className="thesis-field-optional"> (optional)</span>
            </label>
            <p className="thesis-field-hint">
              Market regime context at time of thesis formation.
            </p>
            <input
              className="thesis-regime-input"
              id="thesis-regime"
              onChange={(e) => setRegimeAlignment(e.target.value)}
              placeholder="e.g. risk-on momentum, range-bound, post-correction"
              type="text"
              value={regimeAlignment}
            />
          </div>
            </div>

            <ThesisImportPreviewPanel
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
              {" "} {rejectedFields.size} rejected.
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
              {submitState === "submitting"
                ? "Creating thesis…"
                : "Develop Thesis"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
