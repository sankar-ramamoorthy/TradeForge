import {
  ArrowRight,
  GitBranch,
  History,
  ListChecks,
  ShieldCheck,
} from "lucide-react";
import { MouseEvent, useEffect, useMemo, useState } from "react";

import { fetchRuntimeStatus, type RuntimeStatus } from "./api/runtime";
import "./styles.css";
import {
  WORKSPACE_ROUTES,
  buildWorkspaceHref,
  findWorkspaceRoute,
  mergeWorkspaceContext,
  readWorkspaceContext,
  type WorkspaceContext,
  type WorkspaceRouteDefinition,
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
    <section className="runtime-panel" aria-labelledby="runtime-boundary-title">
      <div>
        <p className="eyebrow">Runtime Boundary</p>
        <h2 id="runtime-boundary-title">HTTP API consumer</h2>
      </div>
      <div className="runtime-status">
        <ShieldCheck aria-hidden="true" />
        <span>
          {status ? `${status.runtime} ${status.status}` : "checking runtime"}
        </span>
      </div>
      {error ? <p className="runtime-error">{error}</p> : null}
      <p>
        React reads through FastAPI contracts. Canonical state remains in the
        event ledger and lifecycle services, not browser state.
      </p>
    </section>
  );
}

function ContextRail({
  context,
}: {
  context: Required<WorkspaceContext>;
}) {
  return (
    <aside className="context-rail" aria-label="Selected workspace context">
      <div>
        <span>Persona</span>
        <strong>{context.persona_id}</strong>
      </div>
      <div>
        <span>Workflow</span>
        <strong>{context.selected_workflow_id}</strong>
      </div>
      <div>
        <span>Decision</span>
        <strong>{context.decision_id}</strong>
      </div>
    </aside>
  );
}

function WorkspaceNavigation({
  activeRoute,
  context,
  onNavigate,
}: {
  activeRoute: WorkspaceRouteDefinition;
  context: Required<WorkspaceContext>;
  onNavigate: (event: MouseEvent<HTMLAnchorElement>, href: string) => void;
}) {
  return (
    <nav className="workspace-nav" aria-label="Workspace routes">
      {WORKSPACE_ROUTES.map((route) => {
        const href = buildWorkspaceHref(route, context);
        const isActive = route.id === activeRoute.id;
        const Icon = route.Icon;

        return (
          <a
            aria-current={isActive ? "page" : undefined}
            className={isActive ? "active" : undefined}
            href={href}
            key={route.id}
            onClick={(event) => onNavigate(event, href)}
          >
            <Icon aria-hidden="true" />
            <span>{route.name.replace(" Workspace", "")}</span>
          </a>
        );
      })}
    </nav>
  );
}

function WorkspaceSurface({
  route,
}: {
  route: WorkspaceRouteDefinition;
}) {
  const Icon = route.Icon;

  return (
    <section className="workspace-surface" aria-labelledby="workspace-title">
      <div className="surface-title">
        <Icon aria-hidden="true" />
        <div>
          <p className="eyebrow">Workspace Route</p>
          <h1 id="workspace-title">{route.name}</h1>
        </div>
      </div>

      <div className="surface-grid">
        <article>
          <h2>Operational Question</h2>
          <p>{route.operationalQuestion}</p>
        </article>
        <article>
          <h2>Context Surface</h2>
          <p>{route.contextSurface}</p>
        </article>
        <article>
          <h2>Authority Boundary</h2>
          <p>{route.authorityBoundary}</p>
        </article>
      </div>
    </section>
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

  function handleNavigate(
    event: MouseEvent<HTMLAnchorElement>,
    href: string,
  ) {
    event.preventDefault();
    window.history.pushState(null, "", href);
    setLocation(readCurrentLocation());
  }

  return (
    <main className="app-shell">
      <section className="workspace-briefing" aria-labelledby="runtime-title">
        <div className="title-block">
          <p className="eyebrow">TradeForge</p>
          <h2 id="runtime-title">Workspace routing system</h2>
          <p>
            Route selection preserves persona, workflow, and decision context
            while remaining a derived presentation layer over runtime APIs.
          </p>
        </div>

        <div className="authority-strip" aria-label="Runtime authority boundaries">
          <div>
            <ListChecks aria-hidden="true" />
            <span>Six MVP routes</span>
          </div>
          <div>
            <GitBranch aria-hidden="true" />
            <span>Context preserved</span>
          </div>
          <div>
            <History aria-hidden="true" />
            <span>Replay-aware URLs</span>
          </div>
        </div>
      </section>

      <div className="workspace-layout">
        <div className="workspace-sidebar">
          <WorkspaceNavigation
            activeRoute={activeRoute}
            context={context}
            onNavigate={handleNavigate}
          />
          <ContextRail context={context} />
        </div>

        <div className="workspace-main">
          <WorkspaceSurface route={activeRoute} />
          <a
            className="context-link"
            href={buildWorkspaceHref(activeRoute, context)}
            onClick={(event) =>
              handleNavigate(event, buildWorkspaceHref(activeRoute, context))
            }
          >
            <span>Current routed context</span>
            <ArrowRight aria-hidden="true" />
          </a>
        </div>
      </div>

      <RuntimeBoundaryStatus />
    </main>
  );
}
