from decimal import Decimal
from typing import Callable
from unittest import mock

import pytest

from map_admin.application.dtos import PartialUpdateEdgeInputData
from map_admin.application.repositories import NodeRepository
from map_admin.application.use_cases import PartialUpdateEdgeUseCase
from map_admin.domain.entities import Edge, Node
from map_admin.domain.value_objects import Point, RoadQuality


@pytest.mark.parametrize(
    "input_vertical_distance, expected_vertical_distance",
    [(Decimal("3.0"), Decimal("3.0")), (None, Decimal("1.0"))],
)
@pytest.mark.parametrize(
    "input_horizontal_distance, expected_horizontal_distance",
    [(Decimal("4.0"), Decimal("4.0")), (None, Decimal("2.0"))],
)
@pytest.mark.parametrize(
    "input_is_stair, expected_is_stair",
    [(True, True), (None, False)],
)
@pytest.mark.parametrize(
    "input_is_step, expected_is_step",
    [(True, True), (None, False)],
)
@pytest.mark.parametrize(
    "input_quality, expected_quality",
    [(RoadQuality.LOW, RoadQuality.LOW), (None, RoadQuality.HIGH)],
)
def test_partial_update_edge(
    input_vertical_distance: Decimal | None,
    input_horizontal_distance: Decimal | None,
    input_is_stair: bool | None,
    input_is_step: bool | None,
    input_quality: RoadQuality | None,
    expected_vertical_distance: Decimal,
    expected_horizontal_distance: Decimal,
    expected_is_stair: bool,
    expected_is_step: bool,
    expected_quality: RoadQuality,
) -> None:
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

    PartialUpdateEdgeUseCase(
        node_repo=mock_node_repo,
    ).execute(
        input_data=PartialUpdateEdgeInputData(
            node_ids=(1, 2),
            vertical_distance=input_vertical_distance,
            horizontal_distance=input_horizontal_distance,
            is_stair=input_is_stair,
            is_step=input_is_step,
            quality=input_quality,
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
                edges=[
                    Edge(
                        node_ids=(1, 2),
                        vertical_distance=expected_vertical_distance,
                        horizontal_distance=expected_horizontal_distance,
                        is_stair=expected_is_stair,
                        is_step=expected_is_step,
                        quality=expected_quality,
                    ),
                ],
            ),
        ),
    ]


def test_partial_update_edge_with_invalid_node_id() -> None:
    mock_node_repo = mock.Mock(spec_set=NodeRepository)
    mock_node_repo.get_node_by_id.side_effect = [NodeRepository.NodeNotFoundError]

    with pytest.raises(PartialUpdateEdgeUseCase.NodeNotFoundError):
        PartialUpdateEdgeUseCase(
            node_repo=mock_node_repo,
        ).execute(
            input_data=PartialUpdateEdgeInputData(
                node_ids=(1, 2),
                vertical_distance=Decimal("1.0"),
                horizontal_distance=Decimal("2.0"),
                is_stair=False,
                is_step=False,
                quality=RoadQuality.HIGH,
            ),
        )

    assert not mock_node_repo.update_node.called


def test_partial_update_edge_with_same_node() -> None:
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

    with pytest.raises(PartialUpdateEdgeUseCase.ConnectingSameNodeError):
        PartialUpdateEdgeUseCase(
            node_repo=mock_node_repo,
        ).execute(
            input_data=PartialUpdateEdgeInputData(
                node_ids=(1, 1),
                vertical_distance=Decimal("1.0"),
                horizontal_distance=Decimal("2.0"),
                is_stair=False,
                is_step=False,
                quality=RoadQuality.HIGH,
            ),
        )

    assert not mock_node_repo.update_node.called


def test_partial_update_edge_with_no_edge_between_nodes() -> None:
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

    with pytest.raises(PartialUpdateEdgeUseCase.EdgeNotFoundError):
        PartialUpdateEdgeUseCase(
            node_repo=mock_node_repo,
        ).execute(
            input_data=PartialUpdateEdgeInputData(
                node_ids=(1, 2),
                vertical_distance=Decimal("1.0"),
                horizontal_distance=Decimal("2.0"),
                is_stair=False,
                is_step=False,
                quality=RoadQuality.HIGH,
            ),
        )

    assert not mock_node_repo.update_node.called
