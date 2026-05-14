import { Activity, ArrowRight, CheckCircle, PlusCircle } from "lucide-react";
import { LifecycleProgressStrip, WorkflowGuidanceNote } from "./LifecycleProgress";
import { type MouseEvent, useEffect, useState } from "react";

import {
  fetchOperatingAttentionQueue,
  fetchWorkspaceProjection,
  type AttentionItem,
  type OperatingAttentionQueue,
  type WorkspaceApiParams,
  type WorkspaceProjection,
} from "../api/runtime";
import {
  buildWorkspaceHref,
  findWorkspaceRoute,
  type WorkspaceContext,
} from "../workspaceRouting";
import { type ActiveDecisionRecord } from "../activeDecision";
import { ContextualBriefingPanel } from "./ContextualBriefingPanel";
import { NewTradeIdeaModal } from "./NewTradeIdeaModal";

const CATEGORY_LABELS: Record<string, string> = {
  decision: "Decision",
  risk: "Risk",
  review: "Review",
  opportunity: "Opportunity",
  context: "Context",
};

function contextToApiParams(
  context: Required<WorkspaceContext>,
): WorkspaceApiParams {
  return {
    persona_id: context.persona_id,
    persona_version: context.persona_version,
    workspace_id: context.workspace_id,
    workflow_id: context.selected_workflow_id || undefined,
    decision_id: context.decision_id || undefined,
  };
}

function AttentionItemCard({
  item,
  context,
  onNavigate,
}: {
  item: AttentionItem;
  context: Required<WorkspaceContext>;
  onNavigate: (event: MouseEvent<HTMLAnchorElement>, href: string) => void;
}) {
  const route = findWorkspaceRoute(`/workspaces/${item.route_id}`);
  const href = buildWorkspaceHref(route, context);
  const RouteIcon = route.Icon;

  return (
    <article
      className="attention-item"
      data-priority={item.priority_label}
      aria-label={`${CATEGORY_LABELS[item.category] ?? item.category} attention item`}
    >
      <div className="attention-item-header">
        <span className="attention-category-badge">
          {CATEGORY_LABELS[item.category] ?? item.category}
        </span>
        <span className={`priority-badge priority-${item.priority_label}`}>
          {item.priority_label}
        </span>
      </div>
      <p className="attention-explanation">{item.explanation}</p>
      {item.lifecycle_stage ? (
        <p className="attention-stage">
          Stage: <strong>{item.lifecycle_stage}</strong>
        </p>
      ) : null}
      <a
        className="attention-route-link"
        href={href}
        onClick={(e) => onNavigate(e, href)}
      >
        <RouteIcon aria-hidden="true" />
        <span>{route.name.replace(" Workspace", "")}</span>
        <ArrowRight aria-hidden="true" />
      </a>
    </article>
  );
}

type OperatingWorkspaceProps = {
  context: Required<WorkspaceContext>;
  onNavigate: (event: MouseEvent<HTMLAnchorElement>, href: string) => void;
  onNavigateProgrammatic: (href: string) => void;
  onDecisionActivated: (record: ActiveDecisionRecord) => void;
  onStageLoaded?: (stage: string | null) => void;
};

export function OperatingWorkspace({
  context,
  onNavigate,
  onNavigateProgrammatic,
  onDecisionActivated,
  onStageLoaded,
}: OperatingWorkspaceProps) {
  const [projection, setProjection] = useState<WorkspaceProjection | null>(
    null,
  );
  const [queue, setQueue] = useState<OperatingAttentionQueue | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [showNewIdeaModal, setShowNewIdeaModal] = useState(false);

  const params = contextToApiParams(context);

  useEffect(() => {
    const controller = new AbortController();

    Promise.all([
      fetchWorkspaceProjection("operating", params, controller.signal),
      fetchOperatingAttentionQueue(params, controller.signal),
    ])
      .then(([projectionData, queueData]) => {
        setProjection(projectionData);
        setQueue(queueData);
        setLoadError(null);
        onStageLoaded?.(projectionData.lifecycle_state?.current_stage ?? null);
      })
      .catch((err: unknown) => {
        if (err instanceof DOMException && err.name === "AbortError") return;
        setLoadError(
          err instanceof Error
            ? err.message
            : "Failed to load operating workspace",
        );
      });

    return () => controller.abort();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [
    context.persona_id,
    context.persona_version,
    context.workspace_id,
    context.selected_workflow_id,
    context.decision_id,
  ]);

  const lifecycleStage = projection?.lifecycle_state?.current_stage ?? null;

  function handleIdeaCreated(decisionId: string, symbol: string) {
    setShowNewIdeaModal(false);
    const opportunityRoute = findWorkspaceRoute("/workspaces/opportunity");
    const href = buildWorkspaceHref(opportunityRoute, {
      ...context,
      decision_id: decisionId,
    });
    onNavigateProgrammatic(href);
    void symbol;
  }

  return (
    <>
    {showNewIdeaModal ? (
      <NewTradeIdeaModal
        personaId={context.persona_id}
        personaVersion={context.persona_version}
        workspaceId={context.workspace_id}
        onCreated={handleIdeaCreated}
        onDecisionActivated={onDecisionActivated}
        onCancel={() => setShowNewIdeaModal(false)}
      />
    ) : null}
    <section
      className="workspace-surface"
      aria-labelledby="operating-workspace-title"
    >
      <div className="surface-title">
        <Activity aria-hidden="true" />
        <div>
          <p className="eyebrow">Operating Workspace</p>
          <h1 id="operating-workspace-title">
            What requires attention now?
          </h1>
        </div>
        <button
          className="new-idea-trigger"
          onClick={() => setShowNewIdeaModal(true)}
          type="button"
        >
          <PlusCircle aria-hidden="true" />
          New Trade Idea
        </button>
      </div>

      {loadError ? (
        <div className="runtime-error">{loadError}</div>
      ) : null}

      <LifecycleProgressStrip currentStage={lifecycleStage} />
      <WorkflowGuidanceNote currentStage={lifecycleStage} />

      <div className="attention-queue-section">
        <p className="eyebrow">Operational Attention</p>

        {queue === null && !loadError ? (
          <p className="attention-loading">Loading attention queue…</p>
        ) : null}

        {queue !== null && queue.items.length === 0 ? (
          <div className="attention-empty">
            <CheckCircle aria-hidden="true" />
            <span>No pending operational attention items.</span>
          </div>
        ) : null}

        {queue !== null && queue.items.length > 0 ? (
          <div className="attention-queue" role="list">
            {queue.items.map((item) => (
              <AttentionItemCard
                context={context}
                item={item}
                key={item.item_id}
                onNavigate={onNavigate}
              />
            ))}
          </div>
        ) : null}

        {queue !== null ? (
          <div className="attention-authority-note" aria-label="Authority boundaries">
            {queue.authority_boundaries.map((boundary) => (
              <p className="authority-boundary" key={boundary}>
                {boundary}
              </p>
            ))}
          </div>
        ) : null}
      </div>

      <ContextualBriefingPanel params={params} />

      {projection !== null ? (
        <div className="projection-metadata">
          <span className="eyebrow">Projection Basis</span>
          <p className="projection-detail">
            {projection.authority} — {projection.source_event_count} source
            events
          </p>
        </div>
      ) : null}
    </section>
    </>
  );
}
