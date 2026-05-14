import { useState } from "react";
import { type ScenarioBranch, type ScenarioBranchList } from "../api/runtime";
import { type WorkspaceContext } from "../workspaceRouting";
import { ScenarioBranchModal } from "./ScenarioBranchModal";

const BRANCH_TYPE_LABELS: Record<string, string> = {
  primary: "Primary",
  alternative: "Alternative",
  invalidation: "Invalidation",
  regime_transition: "Regime Transition",
};

const CONFIDENCE_LABELS: Record<number, string> = {
  1: "Unlikely", 2: "Possible", 3: "Likely", 4: "Probable", 5: "Expected",
};

function BranchCard({ branch }: { branch: ScenarioBranch }) {
  const typeLabel = BRANCH_TYPE_LABELS[branch.branch_type] ?? branch.branch_type;
  const confidenceLabel = CONFIDENCE_LABELS[branch.confidence] ?? String(branch.confidence);

  return (
    <div
      className={`scenario-branch-card branch-type-${branch.branch_type}`}
      aria-label={`${typeLabel} scenario branch`}
    >
      <div className="scenario-branch-header">
        <span className={`cognitive-branch-type-badge branch-${branch.branch_type}`}>
          {typeLabel}
        </span>
        <span className="cognitive-conviction-badge">
          {confidenceLabel} ({branch.confidence}/5)
        </span>
      </div>
      <div className="scenario-branch-body">
        <p className="scenario-branch-field">
          <span className="cognitive-field-label">If: </span>
          {branch.condition}
        </p>
        <p className="scenario-branch-field">
          <span className="cognitive-field-label">Then: </span>
          {branch.implication}
        </p>
        {branch.notes ? (
          <p className="scenario-branch-notes">{branch.notes}</p>
        ) : null}
      </div>
    </div>
  );
}

type Props = {
  context: Required<WorkspaceContext>;
  branchList: ScenarioBranchList;
  canAdd: boolean;
  onBranchAdded: () => void;
};

export function ScenarioBranchPanel({
  context,
  branchList,
  canAdd,
  onBranchAdded,
}: Props) {
  const [showModal, setShowModal] = useState(false);

  const typeOrder = ["primary", "alternative", "invalidation", "regime_transition"];
  const grouped = typeOrder.reduce<Record<string, ScenarioBranch[]>>((acc, type) => {
    acc[type] = branchList.branches.filter((b) => b.branch_type === type);
    return acc;
  }, {});

  return (
    <div className="scenario-branch-panel" aria-label="Scenario branches">
      <div className="scenario-branch-panel-header">
        <p className="eyebrow">
          Scenario Branches
          {branchList.total_branches > 0 ? (
            <span className="scenario-branch-count">
              {" "}— {branchList.total_branches}
            </span>
          ) : null}
        </p>
        {canAdd ? (
          <button
            className="lifecycle-action-btn-secondary scenario-add-btn"
            onClick={() => setShowModal(true)}
            type="button"
          >
            + Add Scenario
          </button>
        ) : null}
      </div>

      {showModal ? (
        <ScenarioBranchModal
          context={context}
          onCancel={() => setShowModal(false)}
          onSuccess={() => {
            setShowModal(false);
            onBranchAdded();
          }}
        />
      ) : null}

      {branchList.total_branches === 0 ? (
        <p className="field-no-data">
          No scenario branches defined yet.
          {canAdd ? " Add branches to capture conditional reasoning before planning." : ""}
        </p>
      ) : (
        <div className="scenario-branch-groups">
          {typeOrder.map((type) => {
            const branches = grouped[type] ?? [];
            if (branches.length === 0) return null;
            return (
              <div className="scenario-branch-group" key={type}>
                {branches.map((branch, i) => (
                  <BranchCard branch={branch} key={`${type}-${i}`} />
                ))}
              </div>
            );
          })}
        </div>
      )}

      {branchList.total_branches > 0 ? (
        <p className="cognitive-snapshot-authority">
          Scenario branches are cognitive artifacts — derived from event payloads.
        </p>
      ) : null}
    </div>
  );
}
