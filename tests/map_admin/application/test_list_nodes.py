from decimal import Decimal
from unittest import mock

import pytest

from map_admin.application.boundaries import ListNodesOutputBoundary
from map_admin.application.dtos import ListNodesOutputData
from map_admin.application.repositories import NodeRepository
from map_admin.application.use_cases import ListNodesUseCase
from map_admin.domain.entities import Node
from map_admin.domain.value_objects import Point


@pytest.fixture()
def mock_node_repo() -> mock.Mock:
    mock_node_repo: mock.Mock = mock.Mock(spec_set=NodeRepository)
    mock_node_repo.get_all_nodes.return_value = [
        Node(name="A", point=Point(longitude=Decimal("1.0"), latitude=Decimal("2.0"))),
        Node(name="B", point=Point(longitude=Decimal("3.0"), latitude=Decimal("4.0"))),
    ]
    return mock_node_repo


@pytest.fixture()
def mock_list_nodes_presenter() -> mock.Mock:
    return mock.Mock(spec_set=ListNodesOutputBoundary)


def test_list_nodes(
    mock_node_repo: mock.Mock,
    mock_list_nodes_presenter: mock.Mock,
) -> None:
    ListNodesUseCase(
        node_repo=mock_node_repo,
    ).execute(
        output_boundary=mock_list_nodes_presenter,
    )

    assert mock_node_repo.get_all_nodes.called
    assert mock_list_nodes_presenter.present.call_args_list == [
        mock.call(
            output_data_list=[
                ListNodesOutputData(
                    name="A", longitude=Decimal("1.0"), latitude=Decimal("2.0")
                ),
                ListNodesOutputData(
                    name="B", longitude=Decimal("3.0"), latitude=Decimal("4.0")
                ),
            ],
        ),
    ]
