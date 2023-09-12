from dataclasses import dataclass, field
from decimal import Decimal

from map_admin.domain.value_objects import Point, RoadQuality


@dataclass(kw_only=True)
class Node:
    id: int
    name: str
    point: Point
    edges: set["Edge"] = field(default_factory=set, init=False)

    def update_name(self, name: str) -> None:
        self.name = name

    def update_point(self, point: Point) -> None:
        self.point = point


@dataclass(kw_only=True)
class Edge:
    nodes: tuple[Node, Node]
    vertical_distance: Decimal
    horizontal_distance: Decimal
    is_stair: bool
    is_step: bool
    quality: RoadQuality

    def __post_init__(self) -> None:
        if self.nodes[0] == self.nodes[1]:
            raise ValueError("Edge cannot connect to itself")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Edge):
            return NotImplemented
        return self.nodes == other.nodes or self.nodes == tuple(reversed(other.nodes))
