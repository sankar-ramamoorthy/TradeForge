import {
  ArrowRight,
  GitBranch,
  History,
  ListChecks,
  ShieldCheck,
} from "lucide-react";
import { MouseEvent, useEffect, useMemo, useState } from "react";

import {
  fetchRuntimeSession,
  fetchRuntimeStatus,
  type RuntimeSession,
  type RuntimeStatus,
} from "./api/runtime";
import {
  getActiveDecision,
  setActiveDecision,
  type ActiveDecisionRecord,
} from "./activeDecision";
import {
  AppShell,
  AuthorityCue,
  ContextLink,
  ContextPanel,
  RuntimeBoundaryPanel,
  SessionPanel,
  WorkspaceBriefing,
  WorkspaceLayout,
  WorkspaceNavigation,
  WorkspaceSurface,
} from "./operationalLayout";
import { ActivePositionWorkspace } from "./workspaces/ActivePositionWorkspace";
import { OperatingWorkspace } from "./workspaces/OperatingWorkspace";
import { OpportunityWorkspace } from "./workspaces/OpportunityWorkspace";
import { PlanReviewWorkspace } from "./workspaces/PlanReviewWorkspace";
import { ReplayWorkspace } from "./workspaces/ReplayWorkspace";
import { ReviewWorkspace } from "./workspaces/ReviewWorkspace";
import "./styles.css";
import {
  buildWorkspaceHref,
  findWorkspaceRoute,
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

  useEffect(() => {
    const handlePopState = () => setLocation(readCurrentLocation());

    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, []);
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
  const activeHref = buildWorkspaceHref(activeRoute, context);

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

  return (
    <AppShell>
      <WorkspaceBriefing
        eyebrow="TradeForge"
        summary="Session identity, persona activation, and workspace focus stay separate while the frontend consumes runtime API context."
        title="Operational session context"
      >
        <AuthorityCue Icon={ListChecks} label="Six MVP routes" />
        <AuthorityCue Icon={GitBranch} label="Context preserved" />
        <AuthorityCue Icon={History} label="Replay-aware URLs" />
      </WorkspaceBriefing>

      <WorkspaceLayout
        sidebar={
          <>
            <WorkspaceNavigation
              activeRoute={activeRoute}
              context={context}
              onNavigate={handleNavigate}
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
            <ContextPanel context={context} />
          </>
        }
      >
        {activeRoute.id === "operating" ? (
          <OperatingWorkspace
            context={context}
            onNavigate={handleNavigate}
            onNavigateProgrammatic={handleNavigateProgrammatic}
            onDecisionActivated={handleDecisionActivated}
          />
        ) : activeRoute.id === "opportunity" ? (
          <OpportunityWorkspace
            context={context}
            onNavigate={handleNavigate}
          />
        ) : activeRoute.id === "plan-review" ? (
          <PlanReviewWorkspace
            context={context}
            onNavigate={handleNavigate}
          />
        ) : activeRoute.id === "active-position" ? (
          <ActivePositionWorkspace
            context={context}
            onNavigate={handleNavigate}
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
          />
        ) : (
          <WorkspaceSurface route={activeRoute} />
        )}
        <ContextLink
          Icon={ArrowRight}
          href={activeHref}
          label="Current routed context"
          onNavigate={handleNavigate}
        />
      </WorkspaceLayout>

      <RuntimeBoundaryStatus />
    </AppShell>
  );
}
