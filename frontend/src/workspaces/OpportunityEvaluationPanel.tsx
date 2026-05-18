import { type ScenarioBranchList, type WorkspaceProjection } from "../api/runtime";

type Props = {
  projection: WorkspaceProjection;
  branchList: ScenarioBranchList | null;
};

export function OpportunityEvaluationPanel({ projection, branchList }: Props) {
  const sourceEvents = projection.source_event_count;
  const hasScenarios = (branchList?.total_branches ?? 0) > 0;
  const setupMaturity =
    sourceEvents === 0 ? "Early" : hasScenarios ? "Developing" : "Unstructured";

  return (
    <section className="opportunity-evaluation-panel" aria-label="Opportunity evaluation">
      <div className="panel-heading">
        <p className="eyebrow">Evaluate Opportunity</p>
        <span className="field-authority-badge authority-derived">Derived</span>
      </div>
      <div className="opportunity-evaluation-grid">
        <div>
          <dt>What is interesting now</dt>
          <dd>
            {sourceEvents > 0
              ? "This setup has event-backed context available for evaluation."
              : "This setup is still thinly evidenced and needs more operator review."}
          </dd>
        </div>
        <div>
          <dt>Why it matters</dt>
          <dd>It is the active setup under review before thesis formation and plan commitment.</dd>
        </div>
        <div>
          <dt>What is missing</dt>
          <dd>
            {hasScenarios
              ? "Use conditional paths and acquired context to resolve remaining uncertainty."
              : "Conditional paths have not been defined yet."}
          </dd>
        </div>
        <div>
          <dt>Setup maturity</dt>
          <dd>{setupMaturity}</dd>
        </div>
      </div>
    </section>
  );
}
