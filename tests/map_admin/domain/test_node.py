from decimal import Decimal

import pytest

from map_admin.domain.entities import Edge, Node
from map_admin.domain.exceptions import (
    AlreadyConnectedNodesError,
    ConnectingSameNodeError,
    NoEdgeExistsBetweenNodesError,
)
from map_admin.domain.value_objects import Point, RoadQuality


def test_eq() -> None:
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
            id=1,
            name="Node 1",
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
    }

    assert nodes[1] == nodes[2]


def test_update_name() -> None:
    node = Node(
        id=1,
        name="Node 1",
        point=Point(
            longitude=Decimal("1.0"),
            latitude=Decimal("2.0"),
        ),
    )

    node.update_name(name="Node 1 updated")

    assert node.name == "Node 1 updated"


def test_update_point() -> None:
    node = Node(
        id=1,
        name="Node 1",
        point=Point(
            longitude=Decimal("1.0"),
            latitude=Decimal("2.0"),
        ),
    )
    new_point = Point(
        longitude=Decimal("3.0"),
        latitude=Decimal("4.0"),
    )

    node.update_point(
        point=new_point,
    )

    assert node.point == new_point


def test_add_edge() -> None:
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
    new_edge = Edge(
        node_ids=(1, 2),
        vertical_distance=Decimal("1.0"),
        horizontal_distance=Decimal("2.0"),
        is_stair=False,
        is_step=False,
        quality=RoadQuality.HIGH,
    )

    nodes[1].add_edge(
        other_node=nodes[2],
        vertical_distance=Decimal("1.0"),
        horizontal_distance=Decimal("2.0"),
        is_stair=False,
        is_step=False,
        quality=RoadQuality.HIGH,
    )

    assert new_edge in nodes[1].edges
    assert new_edge in nodes[2].edges


def test_add_edge_error_with_same_node() -> None:
    node = Node(
        id=1,
        name="Node 1",
        point=Point(
            longitude=Decimal("1.0"),
            latitude=Decimal("2.0"),
        ),
        edges=[],
    )

    with pytest.raises(ConnectingSameNodeError):
        node.add_edge(
            other_node=node,
            vertical_distance=Decimal("1.0"),
            horizontal_distance=Decimal("2.0"),
            is_stair=False,
            is_step=False,
            quality=RoadQuality.HIGH,
        )


def test_add_edge_error_with_existing_edge() -> None:
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
    nodes[1].add_edge(
        other_node=nodes[2],
        vertical_distance=Decimal("1.0"),
        horizontal_distance=Decimal("2.0"),
        is_stair=False,
        is_step=False,
        quality=RoadQuality.HIGH,
    )

    with pytest.raises(AlreadyConnectedNodesError):
        nodes[1].add_edge(
            other_node=nodes[2],
            vertical_distance=Decimal("1.0"),
            horizontal_distance=Decimal("2.0"),
            is_stair=False,
            is_step=False,
            quality=RoadQuality.HIGH,
        )


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
def test_update_edge(
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
            name="Node 1",
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
            name="Node 2",
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
    new_edge = Edge(
        node_ids=(1, 2),
        vertical_distance=expected_vertical_distance,
        horizontal_distance=expected_horizontal_distance,
        is_stair=expected_is_stair,
        is_step=expected_is_step,
        quality=expected_quality,
    )

    nodes[1].update_edge(
        other_node=nodes[2],
        vertical_distance=input_vertical_distance,
        horizontal_distance=input_horizontal_distance,
        is_stair=input_is_stair,
        is_step=input_is_step,
        quality=input_quality,
    )

    assert new_edge in nodes[1].edges
    assert new_edge in nodes[2].edges


def test_update_edge_error_with_same_node() -> None:
    node = Node(
        id=1,
        name="Node 1",
        point=Point(
            longitude=Decimal("1.0"),
            latitude=Decimal("2.0"),
        ),
        edges=[],
    )

    with pytest.raises(ConnectingSameNodeError):
        node.update_edge(
            other_node=node,
            vertical_distance=Decimal("1.0"),
            horizontal_distance=Decimal("2.0"),
            is_stair=False,
            is_step=False,
            quality=RoadQuality.HIGH,
        )


def test_update_edge_error_with_no_edge_between_nodes() -> None:
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

    with pytest.raises(NoEdgeExistsBetweenNodesError):
        nodes[1].update_edge(
            other_node=nodes[2],
            vertical_distance=Decimal("1.0"),
            horizontal_distance=Decimal("2.0"),
            is_stair=False,
            is_step=False,
            quality=RoadQuality.HIGH,
        )


def test_delete_edge() -> None:
    nodes: dict[int, Node] = {
        1: Node(
            id=1,
            name="Node 1",
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
            name="Node 2",
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
    deleted_edge = Edge(
        node_ids=(1, 2),
        vertical_distance=Decimal("1.0"),
        horizontal_distance=Decimal("2.0"),
        is_stair=False,
        is_step=False,
        quality=RoadQuality.HIGH,
    )

    nodes[1].delete_edge(
        other_node=nodes[2],
    )

    assert deleted_edge not in nodes[1].edges
    assert deleted_edge not in nodes[2].edges


def test_delete_edge_error_with_same_node() -> None:
    node = Node(
        id=1,
        name="Node 1",
        point=Point(
            longitude=Decimal("1.0"),
            latitude=Decimal("2.0"),
        ),
        edges=[],
    )

    with pytest.raises(ConnectingSameNodeError):
        node.delete_edge(
            other_node=node,
        )


def test_delete_edge_error_with_no_edge_between_nodes() -> None:
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

    with pytest.raises(NoEdgeExistsBetweenNodesError):
        nodes[1].delete_edge(
            other_node=nodes[2],
        )
