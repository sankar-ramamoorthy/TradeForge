import { Activity, ArrowRight, CheckCircle, PlayCircle, PlusCircle } from "lucide-react";
import { LifecycleProgressStrip, WorkflowGuidanceNote } from "./LifecycleProgress";
import { type MouseEvent, useEffect, useState } from "react";

import {
  fetchDecisionList,
  fetchOperatingAttentionQueue,
  fetchPlaybookSummary,
  fetchWorkspaceProjection,
  type AttentionItem,
  type DecisionSummary,
  type OperatingAttentionQueue,
  type PlaybookSummary,
  type WorkspaceApiParams,
  type WorkspaceProjection,
} from "../api/runtime";
import {
  buildWorkspaceHref,
  findWorkspaceRoute,
  getRecommendedWorkspace,
  type WorkspaceContext,
} from "../workspaceRouting";
import { type ActiveDecisionRecord } from "../activeDecision";
import { DEMO_SCENARIOS, runDemoFlow, type DemoScenario } from "../demo";
import { NewTradeIdeaModal } from "./NewTradeIdeaModal";
import { PlaybookAlignmentPanel } from "./PlaybookAlignmentPanel";

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

const STAGE_GROUP: Record<string, "early" | "active" | "armed" | "position" | "done"> = {
  Idea: "early", Thesis: "early",
  Plan: "active", Approval: "active",
  Armed: "armed",
  Execution: "position", Position: "position",
  Review: "done",
};

function DecisionListPanel({
  decisions,
  onNavigate,
}: {
  decisions: DecisionSummary[];
  onNavigate: (href: string) => void;
}) {
  if (decisions.length === 0) return null;

  return (
    <div className="decision-list-panel" aria-label="All active decisions">
      <p className="eyebrow">Active Decisions</p>
      <div className="decision-list" role="list">
        {decisions.map((d) => {
          const workspaceId = d.current_stage
            ? getRecommendedWorkspace(d.current_stage)
            : "operating";
          const href = workspaceId
            ? `/workspaces/${workspaceId}?decision_id=${encodeURIComponent(d.decision_id)}`
            : null;
          const group = d.current_stage ? (STAGE_GROUP[d.current_stage] ?? "early") : "early";

          return (
            <div className="decision-list-item" key={d.decision_id} role="listitem">
              <div className="decision-list-item-main">
                <span className="decision-list-symbol">{d.symbol}</span>
                {d.current_stage ? (
                  <span
                    className={`decision-stage-badge stage-group-${group}`}
                  >
                    {d.current_stage}
                  </span>
                ) : null}
              </div>
              {href ? (
                <button
                  className="decision-list-navigate"
                  onClick={() => onNavigate(href)}
                  type="button"
                  aria-label={`Go to ${d.symbol} — ${d.current_stage ?? "unknown"} stage`}
                >
                  Continue →
                </button>
              ) : null}
            </div>
          );
        })}
      </div>
    </div>
  );
}

type OperatingWorkspaceProps = {
  context: Required<WorkspaceContext>;
  onNavigate: (event: MouseEvent<HTMLAnchorElement>, href: string) => void;
  onNavigateProgrammatic: (href: string) => void;
  onDecisionActivated: (record: ActiveDecisionRecord) => void;
  onStageLoaded?: (stage: string | null) => void;
  onStartWalkthrough?: () => Promise<void>;
};

export function OperatingWorkspace({
  context,
  onNavigate,
  onNavigateProgrammatic,
  onDecisionActivated,
  onStageLoaded,
  onStartWalkthrough,
}: OperatingWorkspaceProps) {
  const [projection, setProjection] = useState<WorkspaceProjection | null>(
    null,
  );
  const [queue, setQueue] = useState<OperatingAttentionQueue | null>(null);
  const [playbookSummary, setPlaybookSummary] = useState<PlaybookSummary | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [decisions, setDecisions] = useState<DecisionSummary[]>([]);
  const [showNewIdeaModal, setShowNewIdeaModal] = useState(false);
  const [demoLoading, setDemoLoading] = useState(false);
  const [activeScenarioId, setActiveScenarioId] = useState<string | null>(null);
  const [demoError, setDemoError] = useState<string | null>(null);
  const [walkthroughStarting, setWalkthroughStarting] = useState(false);
  const [walkthroughStartError, setWalkthroughStartError] = useState<string | null>(null);

  const params = contextToApiParams(context);

  useEffect(() => {
    const controller = new AbortController();

    fetchPlaybookSummary(controller.signal)
      .then(setPlaybookSummary)
      .catch((err: unknown) => {
        if (err instanceof DOMException && err.name === "AbortError") return;
      });

    fetchDecisionList(controller.signal)
      .then((data) => setDecisions(data.decisions))
      .catch((err: unknown) => {
        if (err instanceof DOMException && err.name === "AbortError") return;
      });

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
    fetchDecisionList().then((data) => setDecisions(data.decisions)).catch(() => {});
    const opportunityRoute = findWorkspaceRoute("/workspaces/opportunity");
    const href = buildWorkspaceHref(opportunityRoute, {
      ...context,
      decision_id: decisionId,
    });
    onNavigateProgrammatic(href);
    void symbol;
  }

  async function handleStartDemo(scenario: DemoScenario) {
    setDemoLoading(true);
    setActiveScenarioId(scenario.id);
    setDemoError(null);
    try {
      const result = await runDemoFlow(scenario, {
        personaId: context.persona_id,
        personaVersion: context.persona_version,
        workspaceId: context.workspace_id,
      });
      onDecisionActivated(result.record);
      const href =
        scenario.landingPath +
        `?decision_id=${encodeURIComponent(result.decisionId)}`;
      onNavigateProgrammatic(href);
    } catch (err: unknown) {
      setDemoError(
        err instanceof Error ? err.message : "Failed to start demo. Please try again.",
      );
      setDemoLoading(false);
      setActiveScenarioId(null);
    }
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

        {queue !== null && queue.items.length === 0 && !lifecycleStage ? (
          <div className="demo-scenario-panel" aria-label="Demo scenarios">
            <div className="demo-invite-header">
              <PlayCircle aria-hidden="true" />
              <span>Explore a demo scenario</span>
            </div>
            <p className="demo-scenario-intro">
              Select a scenario to experience TradeForge in action. Each
              illustrates a different aspect of the decision workflow lifecycle.
            </p>
            {demoError ? (
              <p className="demo-invite-error" role="alert">{demoError}</p>
            ) : null}
            <div className="demo-scenario-grid">
              {DEMO_SCENARIOS.map((scenario) => (
                <div
                  className="demo-scenario-card"
                  key={scenario.id}
                  aria-label={`Demo: ${scenario.name}`}
                >
                  <div className="demo-scenario-card-header">
                    <strong className="demo-scenario-symbol">
                      {scenario.symbol}
                    </strong>
                    <span
                      className={`demo-stage-badge demo-stage-${scenario.targetStage.toLowerCase()}`}
                    >
                      → {scenario.targetStage}
                    </span>
                  </div>
                  <p className="demo-scenario-name">{scenario.name}</p>
                  <p className="demo-scenario-desc">{scenario.description}</p>
                  <button
                    className="demo-invite-btn"
                    disabled={demoLoading}
                    onClick={() => {
                      void handleStartDemo(scenario);
                    }}
                    type="button"
                  >
                    {demoLoading && activeScenarioId === scenario.id
                      ? "Setting up…"
                      : "Start"}
                  </button>
                </div>
              ))}
            </div>
            {onStartWalkthrough ? (
              <div className="walkthrough-invite">
                <hr className="demo-section-divider" aria-hidden="true" />
                <p className="walkthrough-invite-text">
                  Prefer a step-by-step guided tour?
                </p>
                {walkthroughStartError ? (
                  <p className="demo-invite-error" role="alert">
                    {walkthroughStartError}
                  </p>
                ) : null}
                <button
                  className="walkthrough-invite-btn"
                  disabled={demoLoading || walkthroughStarting}
                  onClick={() => {
                    setWalkthroughStarting(true);
                    setWalkthroughStartError(null);
                    onStartWalkthrough()
                      .catch((err: unknown) => {
                        setWalkthroughStartError(
                          err instanceof Error
                            ? err.message
                            : "Failed to start walkthrough.",
                        );
                      })
                      .finally(() => setWalkthroughStarting(false));
                  }}
                  type="button"
                >
                  {walkthroughStarting
                    ? "Initializing…"
                    : "Start Guided Walkthrough →"}
                </button>
              </div>
            ) : null}
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

      <div className="operating-panel-grid">
        <DecisionListPanel
          decisions={decisions}
          onNavigate={onNavigateProgrammatic}
        />

        {playbookSummary ? (
          <PlaybookAlignmentPanel summary={playbookSummary} />
        ) : null}
      </div>

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
