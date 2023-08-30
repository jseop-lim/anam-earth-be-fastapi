from decimal import Decimal
from unittest import mock

import pytest

from map_admin.application.boundaries import DeleteNodeInputBoundary
from map_admin.application.dtos import DeleteNodeInputData
from map_admin.application.repositories import NodeRepository
from map_admin.application.use_cases import DeleteNodeUseCase
from map_admin.domain.entities import Node
from map_admin.domain.value_objects import Point


def test_delete_node() -> None:
    mock_node_repo = mock.Mock(spec_set=NodeRepository)
    mock_node_repo.get_node_by_id.return_value = Node(
        id=1,
        name="A",
        point=Point(
            longitude=Decimal("1.0"),
            latitude=Decimal("2.0"),
        ),
    )

    DeleteNodeUseCase(
        node_repo=mock_node_repo,
    ).execute(
        input_data=DeleteNodeInputData(
            id=1,
        ),
    )

    assert mock_node_repo.delete_node.call_args_list == [
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


def test_delete_node_with_invalid_id() -> None:
    mock_node_repo = mock.Mock(spec_set=NodeRepository)
    mock_node_repo.get_node_by_id.side_effect = [NodeRepository.NodeNotFoundError]

    with pytest.raises(DeleteNodeInputBoundary.NodeNotFoundError):
        DeleteNodeUseCase(
            node_repo=mock_node_repo,
        ).execute(
            input_data=DeleteNodeInputData(
                id=1,
            ),
        )

    assert not mock_node_repo.delete_node.called
