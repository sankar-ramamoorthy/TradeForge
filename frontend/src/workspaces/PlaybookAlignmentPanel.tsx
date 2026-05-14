import { type PlaybookGroup, type PlaybookSummary } from "../api/runtime";

function DecisionRow({
  decision,
}: {
  decision: { decision_id: string; symbol: string; current_stage: string | null };
}) {
  return (
    <div className="playbook-decision-row">
      <span className="playbook-decision-symbol">{decision.symbol || "—"}</span>
      {decision.current_stage ? (
        <span className="timeline-stage-tag">{decision.current_stage}</span>
      ) : null}
      <span className="playbook-decision-id" title={decision.decision_id}>
        {decision.decision_id.slice(0, 8)}…
      </span>
    </div>
  );
}

function PlaybookGroupCard({ group }: { group: PlaybookGroup }) {
  return (
    <div className="playbook-group-card" aria-label={`Playbook: ${group.playbook_name}`}>
      <div className="playbook-group-header">
        <span className="cognitive-playbook-badge">{group.playbook_name}</span>
        <span className="playbook-group-count">
          {group.decision_count} decision{group.decision_count !== 1 ? "s" : ""}
        </span>
      </div>
      <div className="playbook-decision-list">
        {group.decisions.map((d) => (
          <DecisionRow decision={d} key={d.decision_id} />
        ))}
      </div>
    </div>
  );
}

type Props = {
  summary: PlaybookSummary;
};

export function PlaybookAlignmentPanel({ summary }: Props) {
  if (summary.total_decisions_with_plan === 0) {
    return (
      <div className="playbook-alignment-panel" aria-label="Playbook alignment">
        <p className="eyebrow">Playbook Alignment</p>
        <p className="field-no-data">
          No planned decisions yet. Playbook alignment appears when decisions
          reach the Plan stage with a playbook tag.
        </p>
      </div>
    );
  }

  return (
    <div className="playbook-alignment-panel" aria-label="Playbook alignment">
      <p className="eyebrow">
        Playbook Alignment
        <span className="cognitive-snapshot-note">
          {" "}— {summary.total_decisions_with_plan} planned decision
          {summary.total_decisions_with_plan !== 1 ? "s" : ""}
        </span>
      </p>

      {summary.playbooks.length === 0 && summary.unaligned_decision_count > 0 ? (
        <p className="field-no-data">
          {summary.unaligned_decision_count} planned decision
          {summary.unaligned_decision_count !== 1 ? "s" : ""} with no playbook alignment.
          Tag decisions with a playbook when creating the plan.
        </p>
      ) : (
        <div className="playbook-group-list">
          {summary.playbooks.map((group) => (
            <PlaybookGroupCard group={group} key={group.playbook_name} />
          ))}
        </div>
      )}

      {summary.playbooks.length > 0 && summary.unaligned_decision_count > 0 ? (
        <p className="playbook-unaligned-note">
          +{summary.unaligned_decision_count} unaligned decision
          {summary.unaligned_decision_count !== 1 ? "s" : ""} (no playbook tag)
        </p>
      ) : null}

      <p className="cognitive-snapshot-authority">
        Derived from plan events — not canonical truth.
      </p>
    </div>
  );
}
