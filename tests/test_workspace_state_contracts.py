from pathlib import Path
from typing import cast

import pytest
from src.services.workspace_engine import (
    DEFAULT_WORKSPACE_ROUTE_DEFINITIONS,
    DEFAULT_WORKSPACE_STATE_CONTRACTS,
    UnknownWorkspaceStateContractError,
    WorkspaceRouteId,
    WorkspaceStateAuthority,
    WorkspaceStateContractCatalog,
)


def test_every_workspace_route_has_exactly_one_state_contract() -> None:
    assert tuple(DEFAULT_WORKSPACE_STATE_CONTRACTS) == tuple(
        DEFAULT_WORKSPACE_ROUTE_DEFINITIONS
    )

    for route_id, contract in DEFAULT_WORKSPACE_STATE_CONTRACTS.items():
        assert contract.route_id is route_id
        assert (
            contract.operational_question
            == DEFAULT_WORKSPACE_ROUTE_DEFINITIONS[route_id].operational_question
        )


def test_contracts_include_all_adr_0012_workspace_routes() -> None:
    assert set(DEFAULT_WORKSPACE_STATE_CONTRACTS) == {
        WorkspaceRouteId.OPERATING,
        WorkspaceRouteId.OPPORTUNITY,
        WorkspaceRouteId.CONTEXT_WORKBENCH,
        WorkspaceRouteId.PLAN_REVIEW,
        WorkspaceRouteId.ACTIVE_POSITION,
        WorkspaceRouteId.REPLAY,
        WorkspaceRouteId.REVIEW,
        WorkspaceRouteId.MARKET_CONTEXT,
        WorkspaceRouteId.PLAYBOOKS_DOCTRINE,
    }


def test_every_state_field_has_explicit_authority_classification() -> None:
    authorities_seen: set[WorkspaceStateAuthority] = set()

    for contract in DEFAULT_WORKSPACE_STATE_CONTRACTS.values():
        assert contract.state_fields
        for field in contract.state_fields:
            assert isinstance(field.authority, WorkspaceStateAuthority)
            assert field.description
            assert field.source_inputs
            authorities_seen.add(field.authority)

    assert authorities_seen == {
        WorkspaceStateAuthority.CANONICAL,
        WorkspaceStateAuthority.DERIVED,
        WorkspaceStateAuthority.INFERRED,
        WorkspaceStateAuthority.ADVISORY,
    }


def test_contracts_declare_event_inputs_and_replay_requirements() -> None:
    for contract in DEFAULT_WORKSPACE_STATE_CONTRACTS.values():
        assert contract.required_event_inputs
        assert contract.replay_requirements
        for replay_requirement in contract.replay_requirements:
            assert replay_requirement.description
            assert replay_requirement.required_inputs


def test_contracts_do_not_own_canonical_lifecycle_truth() -> None:
    forbidden_canonical_fields = {
        "current_lifecycle_stage",
        "current_stage",
        "approval_state",
        "execution_authority",
    }

    for contract in DEFAULT_WORKSPACE_STATE_CONTRACTS.values():
        canonical_field_names = {
            field.name
            for field in contract.state_fields
            if field.authority is WorkspaceStateAuthority.CANONICAL
        }
        assert canonical_field_names.isdisjoint(forbidden_canonical_fields)
        assert contract.authority_boundaries
        assert any(
            "lifecycle" in boundary.lower()
            for boundary in contract.authority_boundaries
        )


def test_workspace_state_contract_catalog_returns_contracts_by_route_id() -> None:
    catalog = WorkspaceStateContractCatalog()

    contract = catalog.contract_for("plan-review")

    assert contract.route_id is WorkspaceRouteId.PLAN_REVIEW


def test_workspace_state_contract_catalog_rejects_unknown_routes() -> None:
    catalog = WorkspaceStateContractCatalog()

    with pytest.raises(
        UnknownWorkspaceStateContractError,
        match="unknown workspace state contract",
    ):
        catalog.contract_for("dashboard")


def test_workspace_state_contract_catalog_is_immutable() -> None:
    with pytest.raises(TypeError):
        cast(dict[WorkspaceRouteId, object], DEFAULT_WORKSPACE_STATE_CONTRACTS)[
            WorkspaceRouteId.OPERATING
        ] = object()


def test_workspace_state_contracts_avoid_runtime_mutation_boundaries() -> None:
    module_text = Path("src/services/workspace_engine/contracts.py").read_text(
        encoding="utf-8"
    )
    forbidden_imports = (
        "src.app",
        "src.domain.events",
        "src.domain.lifecycle",
        "src.infrastructure",
        "src.services.lifecycle",
    )

    for forbidden_import in forbidden_imports:
        assert forbidden_import not in module_text
