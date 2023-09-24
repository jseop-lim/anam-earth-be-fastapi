from decimal import Decimal

import pytest

from map_admin.domain.entities import Edge
from map_admin.domain.value_objects import RoadQuality


def test_validate_edge_connecting_different_nodes() -> None:
    with pytest.raises(ValueError, match="Edge cannot connect to itself"):
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
