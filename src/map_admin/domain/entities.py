from dataclasses import dataclass
from decimal import Decimal

from map_admin.domain.value_objects import Point
from map_admin.domain.value_objects import RoadQuality


@dataclass(kw_only=True)
class Node:
    name: str
    point: Point


@dataclass(kw_only=True)
class Arc:
    start_node: Node
    end_node: Node
    vertical_distance: Decimal
    horizontal_distance: Decimal
    is_stair: bool
    is_step: bool
    quality: RoadQuality
