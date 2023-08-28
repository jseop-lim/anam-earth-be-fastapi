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

    def get_node_by_id(self, node_id: int) -> Node:
        if node_id == 1:
            return Node(
                id=1,
                name="A",
                point=Point(longitude=Decimal("1.0"), latitude=Decimal("2.0")),
            )
        elif node_id == 2:
            return Node(
                id=2,
                name="B",
                point=Point(longitude=Decimal("3.0"), latitude=Decimal("4.0")),
            )
        else:
            raise super().NodeNotFoundError

    def create_node(self, node: Node) -> None:
        print(f"Create node: {node}")

    def update_node(self, node: Node) -> None:
        print(f"Update node: {node}")

    def delete_node(self, node: Node) -> None:
        print(f"Delete node: {node}")


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

        return max((node_dict["id"] for node_dict in nodes), default=0) + 1

    def get_all_nodes(self) -> list[Node]:
        with open(self.file_path, "r") as file:
            nodes: list[FileNode] = json.load(file)

        return [
            Node(
                id=node_dict["id"],
                name=node_dict["name"],
                point=Point(
                    longitude=Decimal(node_dict["longitude"]),
                    latitude=Decimal(node_dict["latitude"]),
                ),
            )
            for node_dict in nodes
        ]

    def get_node_by_id(self, node_id: int) -> Node:
        with open(self.file_path, "r") as file:
            nodes: list[FileNode] = json.load(file)

        try:
            node: FileNode = next(
                node_dict for node_dict in nodes if node_dict["id"] == node_id
            )
        except StopIteration:
            raise super().NodeNotFoundError

        return Node(
            id=node["id"],
            name=node["name"],
            point=Point(
                longitude=Decimal(node["longitude"]),
                latitude=Decimal(node["latitude"]),
            ),
        )

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

    def update_node(self, node: Node) -> None:
        with open(self.file_path, "r") as file:
            nodes: list[FileNode] = json.load(file)

        for node_dict in nodes:
            if node_dict["id"] == node.id:
                node_dict["name"] = node.name
                node_dict["longitude"] = str(node.point.longitude)
                node_dict["latitude"] = str(node.point.latitude)
                break

        with open(self.file_path, "w") as file:
            json.dump(nodes, file, indent=4)

    def delete_node(self, node: Node) -> None:
        with open(self.file_path, "r") as file:
            nodes: list[FileNode] = json.load(file)

        nodes = [node_dict for node_dict in nodes if node_dict["id"] != node.id]

        with open(self.file_path, "w") as file:
            json.dump(nodes, file, indent=4)
