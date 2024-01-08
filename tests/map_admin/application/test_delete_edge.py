from collections.abc import Callable
from decimal import Decimal
from unittest import mock

import pytest

from map_admin.application.dtos import DeleteEdgeInputData
from map_admin.application.repositories import NodeRepository
from map_admin.application.use_cases import DeleteEdgeUseCase
from map_admin.domain.entities import Edge, Node
from map_admin.domain.value_objects import Point, RoadQuality


def test_delete_edge() -> None:
    nodes: dict[int, Node] = {
        1: Node(
            id=1,
            name="A",
            point=Point(
                longitude=Decimal("1.0"),
                latitude=Decimal("2.0"),
            ),
            edges=[
                Edge(
                    node_ids=(1, 2),
                    vertical_distance=Decimal("1.0"),
                    horizontal_distance=Decimal("2.0"),
                    is_stair=False,
                    is_step=False,
                    quality=RoadQuality.HIGH,
                ),
            ],
        ),
        2: Node(
            id=2,
            name="B",
            point=Point(
                longitude=Decimal("3.0"),
                latitude=Decimal("4.0"),
            ),
            edges=[
                Edge(
                    node_ids=(1, 2),
                    vertical_distance=Decimal("1.0"),
                    horizontal_distance=Decimal("2.0"),
                    is_stair=False,
                    is_step=False,
                    quality=RoadQuality.HIGH,
                ),
            ],
        ),
    }
    mock_node_repo = mock.Mock(spec_set=NodeRepository)
    side_effect: Callable[[int], Node] = lambda node_id: nodes[node_id]
    mock_node_repo.get_node_by_id.side_effect = side_effect

    DeleteEdgeUseCase(
        node_repo=mock_node_repo,
    ).execute(
        input_data=DeleteEdgeInputData(
            node_ids=(1, 2),
        ),
    )

    assert mock_node_repo.update_node.call_args_list == [
        mock.call(
            node=Node(
                id=1,
                name="A",
                point=Point(
                    longitude=Decimal("1.0"),
                    latitude=Decimal("2.0"),
                ),
                edges=[],
            ),
        ),
    ]


def test_delete_edge_with_invalid_node_id() -> None:
    mock_node_repo = mock.Mock(spec_set=NodeRepository)
    mock_node_repo.get_node_by_id.side_effect = [NodeRepository.NodeNotFoundError]

    with pytest.raises(DeleteEdgeUseCase.NodeNotFoundError):
        DeleteEdgeUseCase(
            node_repo=mock_node_repo,
        ).execute(
            input_data=DeleteEdgeInputData(
                node_ids=(1, 2),
            ),
        )


def test_delete_edge_with_same_node() -> None:
    node = Node(
        id=1,
        name="A",
        point=Point(
            longitude=Decimal("1.0"),
            latitude=Decimal("2.0"),
        ),
    )
    mock_node_repo = mock.Mock(spec_set=NodeRepository)
    mock_node_repo.get_node_by_id.side_effect = [node, node]

    with pytest.raises(DeleteEdgeUseCase.ConnectingSameNodeError):
        DeleteEdgeUseCase(
            node_repo=mock_node_repo,
        ).execute(
            input_data=DeleteEdgeInputData(
                node_ids=(1, 1),
            ),
        )


def test_delete_edge_with_no_edge_between_nodes() -> None:
    nodes: dict[int, Node] = {
        1: Node(
            id=1,
            name="Node 1",
            point=Point(
                longitude=Decimal("1.0"),
                latitude=Decimal("2.0"),
            ),
            edges=[],
        ),
        2: Node(
            id=2,
            name="Node 2",
            point=Point(
                longitude=Decimal("3.0"),
                latitude=Decimal("4.0"),
            ),
            edges=[],
        ),
    }
    mock_node_repo = mock.Mock(spec_set=NodeRepository)
    side_effect: Callable[[int], Node] = lambda node_id: nodes[node_id]
    mock_node_repo.get_node_by_id.side_effect = side_effect

    with pytest.raises(DeleteEdgeUseCase.EdgeNotFoundError):
        DeleteEdgeUseCase(
            node_repo=mock_node_repo,
        ).execute(
            input_data=DeleteEdgeInputData(
                node_ids=(1, 2),
            ),
        )

    assert not mock_node_repo.update_node.called
