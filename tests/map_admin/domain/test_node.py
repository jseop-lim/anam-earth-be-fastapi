from decimal import Decimal

from map_admin.domain.entities import Edge, Node
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
