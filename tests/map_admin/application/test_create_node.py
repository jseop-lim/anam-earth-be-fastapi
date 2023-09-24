from decimal import Decimal
from unittest import mock

import pytest

from map_admin.application.boundaries import CreateNodeOutputBoundary
from map_admin.application.dtos import CreateNodeInputData, CreateNodeOutputData
from map_admin.application.repositories import NodeRepository
from map_admin.application.use_cases import CreateNodeUseCase
from map_admin.domain.entities import Node
from map_admin.domain.value_objects import Point


@pytest.fixture()
def mock_node_repo() -> mock.Mock:
    mock_node_repo = mock.Mock(spec_set=NodeRepository)
    mock_node_repo.get_next_id.side_effect = [1]
    return mock_node_repo


@pytest.fixture()
def mock_create_node_presenter() -> mock.Mock:
    return mock.Mock(spec_set=CreateNodeOutputBoundary)


def test_create_node(
    mock_node_repo: mock.Mock,
    mock_create_node_presenter: mock.Mock,
) -> None:
    CreateNodeUseCase(
        node_repo=mock_node_repo,
    ).execute(
        input_data=CreateNodeInputData(
            name="A",
            longitude=Decimal("1.0"),
            latitude=Decimal("2.0"),
        ),
        output_boundary=mock_create_node_presenter,
    )

    assert mock_node_repo.create_node.call_args_list == [
        mock.call(
            node=Node(
                id=1,
                name="A",
                point=Point(
                    longitude=Decimal("1.0"),
                    latitude=Decimal("2.0"),
                ),
            ),
        ),
    ]
    assert mock_create_node_presenter.present.call_args_list == [
        mock.call(
            output_data=CreateNodeOutputData(
                id=1,
            ),
        ),
    ]
