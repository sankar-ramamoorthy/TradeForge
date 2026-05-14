import { X } from "lucide-react";
import type { MouseEvent, ReactNode } from "react";
import type { LucideIcon } from "lucide-react";

import {
  WORKSPACE_ROUTES,
  buildWorkspaceHref,
  type WorkspaceContext,
  type WorkspaceRouteDefinition,
} from "./workspaceRouting";
import type { ActiveDecisionRecord } from "./activeDecision";

export function AppShell({ children }: { children: ReactNode }) {
  return <main className="app-shell">{children}</main>;
}

export function WorkspaceBriefing({
  eyebrow,
  title,
  summary,
  children,
}: {
  eyebrow: string;
  title: string;
  summary: string;
  children: ReactNode;
}) {
  return (
    <section className="workspace-briefing" aria-labelledby="runtime-title">
      <div className="title-block">
        <p className="eyebrow">{eyebrow}</p>
        <h2 id="runtime-title">{title}</h2>
        <p>{summary}</p>
      </div>

      <div className="authority-strip" aria-label="Runtime authority boundaries">
        {children}
      </div>
    </section>
  );
}

export function AuthorityCue({
  Icon,
  label,
}: {
  Icon: LucideIcon;
  label: string;
}) {
  return (
    <div>
      <Icon aria-hidden="true" />
      <span>{label}</span>
    </div>
  );
}

export function WorkspaceLayout({
  sidebar,
  children,
}: {
  sidebar: ReactNode;
  children: ReactNode;
}) {
  return (
    <div className="workspace-layout">
      <div className="workspace-sidebar">{sidebar}</div>
      <div className="workspace-main">{children}</div>
    </div>
  );
}

export function WorkspaceNavigation({
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

export function ActiveDecisionBadge({
  activeDecision,
  activeStage,
  onClear,
}: {
  activeDecision: ActiveDecisionRecord | null;
  activeStage?: string | null;
  onClear: () => void;
}) {
  if (!activeDecision) {
    return (
      <aside className="active-decision-badge active-decision-empty" aria-label="Active decision">
        <p className="active-decision-hint">
          No active decision — use <strong>New Trade Idea</strong> to begin.
        </p>
      </aside>
    );
  }

  return (
    <aside className="active-decision-badge" aria-label="Active decision">
      <div className="active-decision-header">
        <span className="active-decision-label">Active Decision</span>
        <button
          aria-label="Clear active decision"
          className="active-decision-clear"
          onClick={onClear}
          title="Clear active decision"
          type="button"
        >
          <X aria-hidden="true" />
        </button>
      </div>
      <div className="active-decision-symbol">{activeDecision.symbol}</div>
      <div className="active-decision-meta">
        {activeStage ? (
          <span className="active-decision-stage">{activeStage}</span>
        ) : (
          <span className="authority-tag">in workflow</span>
        )}
        {activeDecision.is_demo ? (
          <span className="demo-badge">Demo</span>
        ) : null}
      </div>
    </aside>
  );
}

function ContextPanelItem({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div>
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

export function SessionPanel({
  sessionId,
  userId,
  displayName,
}: {
  sessionId: string;
  userId: string;
  displayName: string;
}) {
  return (
    <aside className="context-panel session-panel" aria-label="Runtime session">
      <ContextPanelItem label="User" value={displayName} />
      <ContextPanelItem label="User ID" value={userId} />
      <ContextPanelItem label="Session" value={sessionId} />
    </aside>
  );
}

export function WorkspaceSurface({
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
        <OperationalSurfaceCard
          title="Operational Question"
          body={route.operationalQuestion}
        />
        <OperationalSurfaceCard title="Context Surface" body={route.contextSurface} />
        <OperationalSurfaceCard
          title="Authority Boundary"
          body={route.authorityBoundary}
        />
      </div>
    </section>
  );
}

export function OperationalSurfaceCard({
  title,
  body,
}: {
  title: string;
  body: string;
}) {
  return (
    <article className="operational-card">
      <h2>{title}</h2>
      <p>{body}</p>
    </article>
  );
}

export function ContextLink({
  href,
  onNavigate,
  Icon,
  label,
}: {
  href: string;
  onNavigate: (event: MouseEvent<HTMLAnchorElement>, href: string) => void;
  Icon: LucideIcon;
  label: string;
}) {
  return (
    <a
      className="context-link"
      href={href}
      onClick={(event) => onNavigate(event, href)}
    >
      <span>{label}</span>
      <Icon aria-hidden="true" />
    </a>
  );
}

export function RuntimeBoundaryPanel({
  title,
  statusLabel,
  error,
  children,
  Icon,
}: {
  title: string;
  statusLabel: string;
  error: string | null;
  children: ReactNode;
  Icon: LucideIcon;
}) {
  return (
    <section className="runtime-panel" aria-labelledby="runtime-boundary-title">
      <div>
        <p className="eyebrow">Runtime Boundary</p>
        <h2 id="runtime-boundary-title">{title}</h2>
      </div>
      <div className="runtime-status">
        <Icon aria-hidden="true" />
        <span>{statusLabel}</span>
      </div>
      {error ? <p className="runtime-error">{error}</p> : null}
      <p>{children}</p>
    </section>
  );
}
