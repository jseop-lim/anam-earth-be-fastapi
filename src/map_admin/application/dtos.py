from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, kw_only=True)
class ListNodesOutputData:
    id: int
    name: str
    longitude: Decimal
    latitude: Decimal


@dataclass(frozen=True, kw_only=True)
class CreateNodeInputData:
    name: str
    longitude: Decimal
    latitude: Decimal


@dataclass(frozen=True, kw_only=True)
class CreateNodeOutputData:
    id: int


@dataclass(frozen=True, kw_only=True)
class PartialUpdateNodeInputData:
    id: int
    name: str | None
    longitude: Decimal | None
    latitude: Decimal | None


@dataclass(frozen=True, kw_only=True)
class DeleteNodeInputData:
    id: int


@dataclass(frozen=True, kw_only=True)
class ListEdgesOutputData:
    @dataclass(frozen=True, kw_only=True)
    class Node:
        id: int
        name: str

    nodes: tuple[Node, Node]
    vertical_distance: Decimal
    horizontal_distance: Decimal
    is_stair: bool
    is_step: bool
    quality: str


@dataclass(frozen=True, kw_only=True)
class CreateEdgeInputData:
    node_ids: tuple[int, int]
    vertical_distance: Decimal
    horizontal_distance: Decimal
    is_stair: bool
    is_step: bool
    quality: str
