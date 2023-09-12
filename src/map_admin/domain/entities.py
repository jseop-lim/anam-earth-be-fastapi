from dataclasses import dataclass, field
from decimal import Decimal
from typing import Self

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

    def add_edge(
        self,
        other_node: Self,
        vertical_distance: Decimal,
        horizontal_distance: Decimal,
        is_stair: bool,
        is_step: bool,
        quality: RoadQuality,
    ) -> None:
        if self == other_node:
            raise ValueError("Edge cannot connect to itself")

        if any(other_node in edge.nodes for edge in self.edges):
            raise ValueError("Edge already exists")

        edge = Edge(
            nodes=(self, other_node),
            vertical_distance=vertical_distance,
            horizontal_distance=horizontal_distance,
            is_stair=is_stair,
            is_step=is_step,
            quality=quality,
        )
        self.edges.add(edge)
        other_node.edges.add(edge)


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
