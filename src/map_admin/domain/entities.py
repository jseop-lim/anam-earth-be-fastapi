from dataclasses import dataclass, field
from decimal import Decimal

from map_admin.domain.value_objects import Point, RoadQuality


@dataclass(kw_only=True)
class Node:
    id: int
    name: str
    point: Point
    edges: set["Arc"] = field(default_factory=set, init=False)

    def update_name(self, name: str) -> None:
        self.name = name

    def update_point(self, point: Point) -> None:
        self.point = point


@dataclass(kw_only=True)
class Arc:
    nodes: tuple[Node, Node]
    vertical_distance: Decimal
    horizontal_distance: Decimal
    is_stair: bool
    is_step: bool
    quality: RoadQuality
