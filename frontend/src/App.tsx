import { ShieldCheck } from "lucide-react";
import { MouseEvent, useCallback, useEffect, useMemo, useState } from "react";

import {
  fetchRuntimeSession,
  fetchRuntimeStatus,
  type RuntimeSession,
  type RuntimeStatus,
} from "./api/runtime";
import {
  WALKTHROUGH_STEPS,
  advanceWalkthroughStep,
  clearWalkthroughSession,
  getWalkthroughSession,
  initWalkthrough,
  setWalkthroughSession,
  type WalkthroughSession,
} from "./walkthrough";
import { WalkthroughPanel } from "./workspaces/WalkthroughPanel";
import { isOnboardingComplete, markOnboardingComplete } from "./onboarding";
import { OnboardingModal } from "./workspaces/OnboardingModal";
import {
  getOperationalContext,
  syncDecisionSymbol,
  syncLastKnownStage,
  clearOperationalContext,
} from "./operationalContext";
import {
  getActiveDecision,
  setActiveDecision,
  clearActiveDecision,
  type ActiveDecisionRecord,
} from "./activeDecision";
import {
  ActiveDecisionBadge,
  AppShell,
  RuntimeBoundaryPanel,
  SessionPanel,
  WorkspaceLayout,
  WorkspaceNavigation,
  WorkspaceSurface,
} from "./operationalLayout";
import { ActivePositionWorkspace } from "./workspaces/ActivePositionWorkspace";
import { AttentionSummaryPanel } from "./workspaces/AttentionSummaryPanel";
import { ContextualBriefingPanel } from "./workspaces/ContextualBriefingPanel";
import { MarketContextPanel } from "./workspaces/MarketContextPanel";
import { OperatingWorkspace } from "./workspaces/OperatingWorkspace";
import { OpportunityWorkspace } from "./workspaces/OpportunityWorkspace";
import { PlanReviewWorkspace } from "./workspaces/PlanReviewWorkspace";
import { ReplayWorkspace } from "./workspaces/ReplayWorkspace";
import { ReviewWorkspace } from "./workspaces/ReviewWorkspace";
import "./styles.css";
import {
  findWorkspaceRoute,
  getRecommendedWorkspace,
  mergeWorkspaceContext,
  readWorkspaceContext,
  type WorkspaceContext,
} from "./workspaceRouting";

type WorkspaceLocation = {
  pathname: string;
  search: string;
};

function readCurrentLocation(): WorkspaceLocation {
  return {
    pathname: window.location.pathname,
    search: window.location.search,
  };
}

function RuntimeBoundaryStatus() {
  const [status, setStatus] = useState<RuntimeStatus | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();

    fetchRuntimeStatus(controller.signal)
      .then((runtimeStatus) => {
        setStatus(runtimeStatus);
        setError(null);
      })
      .catch((requestError: unknown) => {
        if (
          requestError instanceof DOMException &&
          requestError.name === "AbortError"
        ) {
          return;
        }

        setError(
          requestError instanceof Error
            ? requestError.message
            : "Runtime status request failed",
        );
      });

    return () => controller.abort();
  }, []);

  return (
    <RuntimeBoundaryPanel
      Icon={ShieldCheck}
      error={error}
      statusLabel={
        status ? `${status.runtime} ${status.status}` : "checking runtime"
      }
      title="HTTP API consumer"
    >
      React reads through FastAPI contracts. Canonical state remains in the
      event ledger and lifecycle services, not browser state.
    </RuntimeBoundaryPanel>
  );
}

function sessionContextDefaults(
  session: RuntimeSession | null,
): WorkspaceContext {
  if (session === null) {
    return {};
  }

  return {
    persona_id: session.active_context.persona_id,
    persona_version: session.active_context.persona_version,
    workspace_id: session.active_context.workspace_id,
    selected_workflow_id:
      session.active_context.selected_workflow_id ?? undefined,
    decision_id: session.active_context.decision_id ?? undefined,
  };
}

function activeDecisionDefaults(
  record: ActiveDecisionRecord | null,
): WorkspaceContext {
  if (record === null) return {};
  return {
    persona_id: record.persona_id,
    persona_version: record.persona_version,
    decision_id: record.decision_id,
  };
}

export default function App() {
  const [location, setLocation] = useState<WorkspaceLocation>(() =>
    readCurrentLocation(),
  );
  const [session, setSession] = useState<RuntimeSession | null>(null);
  const [sessionError, setSessionError] = useState<string | null>(null);
  const [activeDecision, setActiveDecisionState] =
    useState<ActiveDecisionRecord | null>(() => getActiveDecision());
  const [activeStage, setActiveStage] = useState<string | null>(
    () => getOperationalContext().last_known_stage,
  );
  const [walkthroughSession, setWalkthroughSessionState] =
    useState<WalkthroughSession | null>(() => getWalkthroughSession());
  const [walkthroughAdvancing, setWalkthroughAdvancing] = useState(false);
  const [walkthroughError, setWalkthroughError] = useState<string | null>(null);
  const [onboardingDone, setOnboardingDone] = useState<boolean>(
    () => isOnboardingComplete(),
  );

  useEffect(() => {
    const handlePopState = () => setLocation(readCurrentLocation());

    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, []);

  useEffect(() => {
    syncDecisionSymbol(activeDecision?.symbol ?? null);
  }, [activeDecision?.symbol]);
  useEffect(() => {
    const controller = new AbortController();

    fetchRuntimeSession(controller.signal)
      .then((runtimeSession) => {
        setSession(runtimeSession);
        setSessionError(null);
      })
      .catch((requestError: unknown) => {
        if (
          requestError instanceof DOMException &&
          requestError.name === "AbortError"
        ) {
          return;
        }

        setSessionError(
          requestError instanceof Error
            ? requestError.message
            : "Runtime session request failed",
        );
      });

    return () => controller.abort();
  }, []);

  const activeRoute = useMemo(
    () => findWorkspaceRoute(location.pathname),
    [location.pathname],
  );
  const recommendedRouteId = useMemo(
    () => getRecommendedWorkspace(activeStage),
    [activeStage],
  );
  const context = useMemo(
    () =>
      mergeWorkspaceContext(
        readWorkspaceContext(location.search),
        {
          ...sessionContextDefaults(session),
          ...activeDecisionDefaults(activeDecision),
        },
      ),
    [location.search, session, activeDecision],
  );
  function handleNavigate(
    event: MouseEvent<HTMLAnchorElement>,
    href: string,
  ) {
    event.preventDefault();
    window.history.pushState(null, "", href);
    setLocation(readCurrentLocation());
  }

  function handleNavigateProgrammatic(href: string) {
    window.history.pushState(null, "", href);
    setLocation(readCurrentLocation());
  }

  function handleDecisionActivated(record: ActiveDecisionRecord) {
    setActiveDecision(record);
    setActiveDecisionState(record);
  }

  function handleClearDecision() {
    clearActiveDecision();
    clearWalkthroughSession();
    clearOperationalContext();
    setActiveDecisionState(null);
    setWalkthroughSessionState(null);
    setActiveStage(null);
    const operatingRoute = findWorkspaceRoute("/workspaces/operating");
    handleNavigateProgrammatic(operatingRoute.path);
  }

  async function handleStartWalkthrough() {
    const result = await initWalkthrough({
      personaId: context.persona_id,
      personaVersion: context.persona_version,
      workspaceId: context.workspace_id,
    });
    const record = getActiveDecision();
    if (record) setActiveDecisionState(record);
    setWalkthroughSessionState(result.session);
    setWalkthroughError(null);
    handleNavigateProgrammatic(WALKTHROUGH_STEPS[0].workspacePath);
  }

  async function handleWalkthroughAdvance() {
    if (!walkthroughSession) return;
    const step = WALKTHROUGH_STEPS[walkthroughSession.current_step_index];
    if (!step) return;

    if (step.nextWorkspacePath === null) {
      clearWalkthroughSession();
      setWalkthroughSessionState(null);
      return;
    }

    setWalkthroughAdvancing(true);
    setWalkthroughError(null);
    try {
      await advanceWalkthroughStep(walkthroughSession, step);
      const nextIndex = walkthroughSession.current_step_index + 1;
      const updated: WalkthroughSession = {
        ...walkthroughSession,
        current_step_index: nextIndex,
      };
      setWalkthroughSession(updated);
      setWalkthroughSessionState(updated);
      handleNavigateProgrammatic(step.nextWorkspacePath);
    } catch (err: unknown) {
      setWalkthroughError(
        err instanceof Error
          ? err.message
          : "Failed to advance walkthrough. Please try again.",
      );
    } finally {
      setWalkthroughAdvancing(false);
    }
  }

  function handleExitWalkthrough() {
    clearWalkthroughSession();
    setWalkthroughSessionState(null);
    setWalkthroughError(null);
  }

  function handleOnboardingComplete() {
    markOnboardingComplete();
    setOnboardingDone(true);
  }

  const handleStageLoaded = useCallback((stage: string | null) => {
    setActiveStage(stage);
    syncLastKnownStage(stage);
  }, []);

  const contextRail =
    activeRoute.id === "operating" ? (
      <ContextualBriefingPanel
        params={{
          persona_id: context.persona_id,
          persona_version: context.persona_version,
          workspace_id: context.workspace_id,
          workflow_id: context.selected_workflow_id || undefined,
          decision_id: context.decision_id || undefined,
        }}
      />
    ) : activeRoute.id === "opportunity" ||
      activeRoute.id === "active-position" ? (
      <MarketContextPanel />
    ) : undefined;

  return (
    <>
      {!onboardingDone ? (
        <OnboardingModal onComplete={handleOnboardingComplete} />
      ) : null}
    <AppShell>
      <WorkspaceLayout
        sidebar={
          <>
            <WorkspaceNavigation
              activeRoute={activeRoute}
              context={context}
              onNavigate={handleNavigate}
              recommendedRouteId={recommendedRouteId}
            />
            <ActiveDecisionBadge
              activeDecision={activeDecision}
              activeStage={activeStage}
              onClear={handleClearDecision}
            />
            <AttentionSummaryPanel
              params={{
                persona_id: context.persona_id,
                persona_version: context.persona_version,
                workspace_id: context.workspace_id,
                workflow_id: context.selected_workflow_id || undefined,
                decision_id: context.decision_id || undefined,
              }}
              onNavigateToOperating={() =>
                handleNavigateProgrammatic("/workspaces/operating")
              }
            />
            {session ? (
              <SessionPanel
                displayName={session.user.display_name}
                sessionId={session.session_id}
                userId={session.user.user_id}
              />
            ) : null}
            {sessionError ? (
              <div className="runtime-error">{sessionError}</div>
            ) : null}
          </>
        }
        contextRail={contextRail}
      >
        {walkthroughSession?.active &&
        WALKTHROUGH_STEPS[walkthroughSession.current_step_index] ? (
          <WalkthroughPanel
            error={walkthroughError}
            isAdvancing={walkthroughAdvancing}
            onAdvance={() => {
              void handleWalkthroughAdvance();
            }}
            onExit={handleExitWalkthrough}
            step={WALKTHROUGH_STEPS[walkthroughSession.current_step_index]!}
          />
        ) : null}
        {activeRoute.id === "operating" ? (
          <OperatingWorkspace
            context={context}
            onNavigate={handleNavigate}
            onNavigateProgrammatic={handleNavigateProgrammatic}
            onDecisionActivated={handleDecisionActivated}
            onStageLoaded={handleStageLoaded}
            onStartWalkthrough={() => handleStartWalkthrough()}
          />
        ) : activeRoute.id === "opportunity" ? (
          <OpportunityWorkspace
            context={context}
            onNavigate={handleNavigate}
            onNavigateProgrammatic={handleNavigateProgrammatic}
            onStageLoaded={handleStageLoaded}
          />
        ) : activeRoute.id === "plan-review" ? (
          <PlanReviewWorkspace
            context={context}
            onNavigate={handleNavigate}
            onNavigateProgrammatic={handleNavigateProgrammatic}
            onStageLoaded={handleStageLoaded}
          />
        ) : activeRoute.id === "active-position" ? (
          <ActivePositionWorkspace
            context={context}
            onNavigate={handleNavigate}
            onNavigateProgrammatic={handleNavigateProgrammatic}
            onStageLoaded={handleStageLoaded}
          />
        ) : activeRoute.id === "replay" ? (
          <ReplayWorkspace
            context={context}
            onNavigate={handleNavigate}
          />
        ) : activeRoute.id === "review" ? (
          <ReviewWorkspace
            context={context}
            onNavigate={handleNavigate}
            onStageLoaded={handleStageLoaded}
          />
        ) : (
          <WorkspaceSurface route={activeRoute} />
        )}
      </WorkspaceLayout>

      <RuntimeBoundaryStatus />
    </AppShell>
    </>
  );
}
