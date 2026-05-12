import {
  ArrowRight,
  GitBranch,
  History,
  ListChecks,
  ShieldCheck,
} from "lucide-react";
import { MouseEvent, useEffect, useMemo, useState } from "react";

import { fetchRuntimeStatus, type RuntimeStatus } from "./api/runtime";
import {
  AppShell,
  AuthorityCue,
  ContextLink,
  ContextPanel,
  RuntimeBoundaryPanel,
  WorkspaceBriefing,
  WorkspaceLayout,
  WorkspaceNavigation,
  WorkspaceSurface,
} from "./operationalLayout";
import "./styles.css";
import {
  buildWorkspaceHref,
  findWorkspaceRoute,
  mergeWorkspaceContext,
  readWorkspaceContext,
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

export default function App() {
  const [location, setLocation] = useState<WorkspaceLocation>(() =>
    readCurrentLocation(),
  );

  useEffect(() => {
    const handlePopState = () => setLocation(readCurrentLocation());

    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, []);

  const activeRoute = useMemo(
    () => findWorkspaceRoute(location.pathname),
    [location.pathname],
  );
  const context = useMemo(
    () => mergeWorkspaceContext(readWorkspaceContext(location.search)),
    [location.search],
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

  return (
    <AppShell>
      <WorkspaceBriefing
        eyebrow="TradeForge"
        summary="Route selection preserves persona, workflow, and decision context while remaining a derived presentation layer over runtime APIs."
        title="Workspace routing system"
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
            <ContextPanel context={context} />
          </>
        }
      >
        <WorkspaceSurface route={activeRoute} />
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
