from dataclasses import dataclass, field
from decimal import Decimal
from typing import Self

from map_admin.domain.exceptions import (
    AlreadyConnectedNodesError,
    ConnectingSameNodeError,
    NoEdgeExistsBetweenNodesError,
)
from map_admin.domain.value_objects import Point, RoadQuality


@dataclass(kw_only=True)
class Node:
    id: int
    name: str
    point: Point
    edges: list["Edge"] = field(default_factory=list)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return NotImplemented
        return all(
            [
                self.id == other.id,
                self.name == other.name,
                self.point == other.point,
            ]
        )

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
            raise ConnectingSameNodeError

        if any(other_node.id in edge.node_ids for edge in self.edges):
            raise AlreadyConnectedNodesError

        edge = Edge(
            node_ids=(self.id, other_node.id),
            vertical_distance=vertical_distance,
            horizontal_distance=horizontal_distance,
            is_stair=is_stair,
            is_step=is_step,
            quality=quality,
        )
        self.edges.append(edge)
        other_node.edges.append(edge)

    def update_edge(
        self,
        other_node: Self,
        vertical_distance: Decimal | None = None,
        horizontal_distance: Decimal | None = None,
        is_stair: bool | None = None,
        is_step: bool | None = None,
        quality: RoadQuality | None = None,
    ) -> None:
        if self == other_node:
            raise ConnectingSameNodeError
        try:
            edge: Edge = next(
                edge for edge in self.edges if other_node.id in edge.node_ids
            )
        except StopIteration:
            raise NoEdgeExistsBetweenNodesError

        if vertical_distance is not None:
            edge.update_vertical_distance(vertical_distance)
        if horizontal_distance is not None:
            edge.update_horizontal_distance(horizontal_distance)
        if is_stair is not None:
            edge.update_is_stair(is_stair)
        if is_step is not None:
            edge.update_is_step(is_step)
        if quality is not None:
            edge.update_quality(quality)

        other_node.edges = [
            edge for edge in other_node.edges if self.id not in edge.node_ids
        ] + [edge]

    def delete_edge(
        self,
        other_node: Self,
    ) -> None:
        if self == other_node:
            raise ConnectingSameNodeError
        try:
            edge: Edge = next(
                edge for edge in self.edges if other_node.id in edge.node_ids
            )
        except StopIteration:
            raise NoEdgeExistsBetweenNodesError

        self.edges.remove(edge)
        other_node.edges.remove(edge)


@dataclass(kw_only=True)
class Edge:
    node_ids: tuple[int, int]
    vertical_distance: Decimal
    horizontal_distance: Decimal
    is_stair: bool
    is_step: bool
    quality: RoadQuality

    def __post_init__(self) -> None:
        if self.node_ids[0] == self.node_ids[1]:
            raise ConnectingSameNodeError

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Edge):
            return NotImplemented
        return all(
            [
                sorted(self.node_ids) == sorted(other.node_ids),
                self.vertical_distance == other.vertical_distance,
                self.horizontal_distance == other.horizontal_distance,
                self.is_stair == other.is_stair,
                self.is_step == other.is_step,
                self.quality == other.quality,
            ]
        )

    def update_vertical_distance(self, vertical_distance: Decimal) -> None:
        self.vertical_distance = vertical_distance

    def update_horizontal_distance(self, horizontal_distance: Decimal) -> None:
        self.horizontal_distance = horizontal_distance

    def update_is_stair(self, is_stair: bool) -> None:
        self.is_stair = is_stair

    def update_is_step(self, is_step: bool) -> None:
        self.is_step = is_step

    def update_quality(self, quality: RoadQuality) -> None:
        self.quality = quality
