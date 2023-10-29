from decimal import Decimal

import pytest

from map_admin.domain.entities import Edge
from map_admin.domain.exceptions import ConnectingSameNodeError
from map_admin.domain.value_objects import RoadQuality


def test_validate_edge_connecting_different_nodes() -> None:
    with pytest.raises(ConnectingSameNodeError):
        Edge(
            node_ids=(1, 1),
            vertical_distance=Decimal("1.0"),
            horizontal_distance=Decimal("2.0"),
            is_stair=False,
            is_step=False,
            quality=RoadQuality.HIGH,
        )


def test_eq() -> None:
    edges: dict[int, Edge] = {
        1: Edge(
            node_ids=(1, 2),
            vertical_distance=Decimal("1.0"),
            horizontal_distance=Decimal("2.0"),
            is_stair=False,
            is_step=False,
            quality=RoadQuality.HIGH,
        ),
        2: Edge(
            node_ids=(2, 1),
            vertical_distance=Decimal("1.0"),
            horizontal_distance=Decimal("2.0"),
            is_stair=False,
            is_step=False,
            quality=RoadQuality.HIGH,
        ),
    }

    assert edges[1] == edges[2]


def test_update_vertical_distance() -> None:
    edge = Edge(
        node_ids=(1, 2),
        vertical_distance=Decimal("1.0"),
        horizontal_distance=Decimal("2.0"),
        is_stair=False,
        is_step=False,
        quality=RoadQuality.HIGH,
    )

    edge.update_vertical_distance(vertical_distance=Decimal("3.0"))

    assert edge.vertical_distance == Decimal("3.0")


def test_update_horizontal_distance() -> None:
    edge = Edge(
        node_ids=(1, 2),
        vertical_distance=Decimal("1.0"),
        horizontal_distance=Decimal("2.0"),
        is_stair=False,
        is_step=False,
        quality=RoadQuality.HIGH,
    )

    edge.update_horizontal_distance(horizontal_distance=Decimal("4.0"))

    assert edge.horizontal_distance == Decimal("4.0")


def test_update_is_stair() -> None:
    edge = Edge(
        node_ids=(1, 2),
        vertical_distance=Decimal("1.0"),
        horizontal_distance=Decimal("2.0"),
        is_stair=False,
        is_step=False,
        quality=RoadQuality.HIGH,
    )

    edge.update_is_stair(is_stair=True)

    assert edge.is_stair is True


def test_update_is_step() -> None:
    edge = Edge(
        node_ids=(1, 2),
        vertical_distance=Decimal("1.0"),
        horizontal_distance=Decimal("2.0"),
        is_stair=False,
        is_step=False,
        quality=RoadQuality.HIGH,
    )

    edge.update_is_step(is_step=True)

    assert edge.is_step is True


def test_update_quality() -> None:
    edge = Edge(
        node_ids=(1, 2),
        vertical_distance=Decimal("1.0"),
        horizontal_distance=Decimal("2.0"),
        is_stair=False,
        is_step=False,
        quality=RoadQuality.HIGH,
    )

    edge.update_quality(quality=RoadQuality.LOW)

    assert edge.quality == RoadQuality.LOW
