from dataclasses import dataclass
from decimal import Decimal

from map_admin.domain.value_objects import Point, RoadQuality


@dataclass(kw_only=True)
class Node:
    id: int
    name: str
    point: Point

    def update_name(self, name: str) -> None:
        self.name = name

    def update_point(self, point: Point) -> None:
        self.point = point


@dataclass(kw_only=True)
class Arc:
    start_node: Node
    end_node: Node
    vertical_distance: Decimal
    horizontal_distance: Decimal
    is_stair: bool
    is_step: bool
    quality: RoadQuality
