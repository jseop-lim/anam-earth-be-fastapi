import json
from decimal import Decimal
from typing import TypedDict

from map_admin.application.repositories import NodeRepository
from map_admin.domain.entities import Node
from map_admin.domain.value_objects import Point


class FakeNodeRepository(NodeRepository):
    def get_next_id(self) -> int:
        return 3

    def get_all_nodes(self) -> list[Node]:
        return [
            Node(
                id=1,
                name="A",
                point=Point(longitude=Decimal("1.0"), latitude=Decimal("2.0")),
            ),
            Node(
                id=2,
                name="B",
                point=Point(longitude=Decimal("3.0"), latitude=Decimal("4.0")),
            ),
        ]

    def create_node(self, node: Node) -> None:
        print(f"Create node: {node}")


class FileNode(TypedDict):
    id: int
    name: str
    longitude: str
    latitude: str


class FileNodeRepository(NodeRepository):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def get_next_id(self) -> int:
        with open(self.file_path, "r") as file:
            nodes: list[FileNode] = json.load(file)

        return max((node["id"] for node in nodes), default=0) + 1

    def get_all_nodes(self) -> list[Node]:
        with open(self.file_path, "r") as file:
            nodes: list[FileNode] = json.load(file)

        return [
            Node(
                id=node["id"],
                name=node["name"],
                point=Point(
                    longitude=Decimal(node["longitude"]),
                    latitude=Decimal(node["latitude"]),
                ),
            )
            for node in nodes
        ]

    def create_node(self, node: Node) -> None:
        with open(self.file_path, "r") as file:
            nodes: list[FileNode] = json.load(file)

        nodes.append(
            {
                "id": node.id,
                "name": node.name,
                "longitude": str(node.point.longitude),
                "latitude": str(node.point.latitude),
            }
        )

        with open(self.file_path, "w") as file:
            json.dump(nodes, file, indent=4)
