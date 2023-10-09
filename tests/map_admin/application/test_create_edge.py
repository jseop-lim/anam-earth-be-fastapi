from decimal import Decimal
from unittest import mock

import pytest

from map_admin.application.boundaries import CreateEdgeInputBoundary
from map_admin.application.dtos import CreateEdgeInputData
from map_admin.application.repositories import NodeRepository
from map_admin.application.use_cases import CreateEdgeUseCase
from map_admin.domain.entities import Node
from map_admin.domain.value_objects import Point, RoadQuality


def test_create_edge() -> None:
    nodes: dict[int, Node] = {
        1: Node(
            id=1,
            name="A",
            point=Point(
                longitude=Decimal("1.0"),
                latitude=Decimal("2.0"),
            ),
        ),
        2: Node(
            id=2,
            name="B",
            point=Point(
                longitude=Decimal("3.0"),
                latitude=Decimal("4.0"),
            ),
        ),
    }
    mock_node_repo = mock.Mock(spec_set=NodeRepository)
    mock_node_repo.get_node_by_id.side_effect = [nodes[1], nodes[2]]

    CreateEdgeUseCase(
        node_repo=mock_node_repo,
    ).execute(
        input_data=CreateEdgeInputData(
            node_ids=(1, 2),
            vertical_distance=Decimal("1.0"),
            horizontal_distance=Decimal("2.0"),
            is_stair=False,
            is_step=False,
            quality=RoadQuality.HIGH,
        ),
    )

    assert mock_node_repo.update_node.call_args_list == [
        mock.call(node=nodes[1]),
    ]


def test_create_edge_with_invalid_node_id() -> None:
    mock_node_repo = mock.Mock(spec_set=NodeRepository)
    mock_node_repo.get_node_by_id.side_effect = [NodeRepository.NodeNotFoundError]

    with pytest.raises(CreateEdgeInputBoundary.NodeNotFoundError):
        CreateEdgeUseCase(
            node_repo=mock_node_repo,
        ).execute(
            input_data=CreateEdgeInputData(
                node_ids=(1, 2),
                vertical_distance=Decimal("1.0"),
                horizontal_distance=Decimal("2.0"),
                is_stair=False,
                is_step=False,
                quality=RoadQuality.HIGH,
            ),
        )

    assert not mock_node_repo.update_node.called
