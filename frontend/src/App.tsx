import {
  Activity,
  GitBranch,
  History,
  ListChecks,
  ShieldCheck,
} from "lucide-react";
import { useEffect, useState } from "react";

import { fetchRuntimeStatus, type RuntimeStatus } from "./api/runtime";
import "./styles.css";

const workspaceReadiness = [
  {
    label: "Operating",
    status: "projection-ready",
    detail: "Decision queues and active exposure will consume workspace APIs.",
  },
  {
    label: "Opportunity",
    status: "next routing",
    detail: "Scenario development remains separate from signal generation.",
  },
  {
    label: "Replay",
    status: "API-backed",
    detail: "Historical reconstruction stays event-derived and deterministic.",
  },
];

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
        if (requestError instanceof DOMException && requestError.name === "AbortError") {
          return;
        }

        setError(
          requestError instanceof Error
            ? requestError.message
            : "Runtime status request failed"
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
        <span>{status ? `${status.runtime} ${status.status}` : "checking runtime"}</span>
      </div>
      {error ? <p className="runtime-error">{error}</p> : null}
      <p>
        React reads through FastAPI contracts. Canonical state remains in the
        event ledger and lifecycle services, not browser state.
      </p>
    </section>
  );
}

export default function App() {
  return (
    <main className="app-shell">
      <section className="workspace-briefing" aria-labelledby="workspace-title">
        <div className="title-block">
          <p className="eyebrow">TradeForge</p>
          <h1 id="workspace-title">Workspace runtime foundation</h1>
          <p>
            A React and TypeScript boundary for persona-scoped operational
            workspaces. This scaffold is prepared for derived API read models,
            not direct event-ledger ownership.
          </p>
        </div>

        <div className="authority-strip" aria-label="Runtime authority boundaries">
          <div>
            <Activity aria-hidden="true" />
            <span>Derived surfaces</span>
          </div>
          <div>
            <ListChecks aria-hidden="true" />
            <span>Lifecycle APIs</span>
          </div>
          <div>
            <History aria-hidden="true" />
            <span>Replay-ready</span>
          </div>
          <div>
            <GitBranch aria-hidden="true" />
            <span>Typed frontend</span>
          </div>
        </div>
      </section>

      <section className="workspace-grid" aria-label="Workspace readiness">
        {workspaceReadiness.map((workspace) => (
          <article className="workspace-card" key={workspace.label}>
            <div>
              <h2>{workspace.label}</h2>
              <span>{workspace.status}</span>
            </div>
            <p>{workspace.detail}</p>
          </article>
        ))}
      </section>

      <RuntimeBoundaryStatus />
    </main>
  );
}
