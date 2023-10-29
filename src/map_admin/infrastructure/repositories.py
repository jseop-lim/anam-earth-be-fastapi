import json
from decimal import Decimal
from typing import TypedDict

from map_admin.application.repositories import NodeRepository
from map_admin.domain.entities import Edge, Node
from map_admin.domain.value_objects import Point, RoadQuality


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


class FileEdge(TypedDict):
    node_ids: tuple[int, int]
    vertical_distance: str
    horizontal_distance: str
    is_stair: bool
    is_step: bool
    quality: str


class FileNodeRepository(NodeRepository):
    def __init__(
        self,
        node_file_path: str,
        edge_file_path: str,
    ) -> None:
        self.node_file_path = node_file_path
        self.edge_file_path = edge_file_path

    def get_next_id(self) -> int:
        with open(self.node_file_path, "r") as file:
            nodes: list[FileNode] = json.load(file)

        return max((node_dict["id"] for node_dict in nodes), default=0) + 1

    def get_all_nodes(self) -> list[Node]:
        with open(self.node_file_path, "r") as file:
            nodes: list[FileNode] = json.load(file)

        with open(self.edge_file_path, "r") as file:
            edges: list[FileEdge] = json.load(file)

        return [
            Node(
                id=node_dict["id"],
                name=node_dict["name"],
                point=Point(
                    longitude=Decimal(node_dict["longitude"]),
                    latitude=Decimal(node_dict["latitude"]),
                ),
                edges=[
                    Edge(
                        node_ids=edge_dict["node_ids"],
                        vertical_distance=Decimal(edge_dict["vertical_distance"]),
                        horizontal_distance=Decimal(edge_dict["horizontal_distance"]),
                        is_stair=edge_dict["is_stair"],
                        is_step=edge_dict["is_step"],
                        quality=RoadQuality(edge_dict["quality"]),
                    )
                    for edge_dict in edges
                    if node_dict["id"] in edge_dict["node_ids"]
                ],
            )
            for node_dict in nodes
        ]

    def get_node_by_id(self, node_id: int) -> Node:
        with open(self.node_file_path, "r") as file:
            nodes: list[FileNode] = json.load(file)

        try:
            node: FileNode = next(
                node_dict for node_dict in nodes if node_dict["id"] == node_id
            )
        except StopIteration:
            raise super().NodeNotFoundError

        with open(self.edge_file_path, "r") as file:
            edges: list[FileEdge] = json.load(file)

        return Node(
            id=node["id"],
            name=node["name"],
            point=Point(
                longitude=Decimal(node["longitude"]),
                latitude=Decimal(node["latitude"]),
            ),
            edges=[
                Edge(
                    node_ids=edge["node_ids"],
                    vertical_distance=Decimal(edge["vertical_distance"]),
                    horizontal_distance=Decimal(edge["horizontal_distance"]),
                    is_stair=edge["is_stair"],
                    is_step=edge["is_step"],
                    quality=RoadQuality(edge["quality"]),
                )
                for edge in edges
                if node["id"] in edge["node_ids"]
            ],
        )

    def create_node(self, node: Node) -> None:
        with open(self.node_file_path, "r") as file:
            nodes: list[FileNode] = json.load(file)

        nodes.append(
            {
                "id": node.id,
                "name": node.name,
                "longitude": str(node.point.longitude),
                "latitude": str(node.point.latitude),
            }
        )

        with open(self.node_file_path, "w") as file:
            json.dump(nodes, file, indent=4)

    def update_node(self, node: Node) -> None:
        with open(self.node_file_path, "r") as file:
            nodes: list[FileNode] = json.load(file)

        for node_dict in nodes:
            if node_dict["id"] == node.id:
                node_dict["name"] = node.name
                node_dict["longitude"] = str(node.point.longitude)
                node_dict["latitude"] = str(node.point.latitude)
                break

        with open(self.node_file_path, "w") as file:
            json.dump(nodes, file, indent=4)

        with open(self.edge_file_path, "r") as file:
            edges: list[FileEdge] = json.load(file)

        edges = [
            edge_dict for edge_dict in edges if node.id not in edge_dict["node_ids"]
        ] + [
            FileEdge(
                node_ids=edge.node_ids,
                vertical_distance=str(edge.vertical_distance),
                horizontal_distance=str(edge.horizontal_distance),
                is_stair=edge.is_stair,
                is_step=edge.is_step,
                quality=edge.quality,
            )
            for edge in node.edges
        ]

        with open(self.edge_file_path, "w") as file:
            json.dump(edges, file, indent=4)

    def delete_node(self, node: Node) -> None:
        with open(self.node_file_path, "r") as file:
            nodes: list[FileNode] = json.load(file)

        nodes = [node_dict for node_dict in nodes if node_dict["id"] != node.id]

        with open(self.node_file_path, "w") as file:
            json.dump(nodes, file, indent=4)

        with open(self.edge_file_path, "r") as file:
            edges: list[FileEdge] = json.load(file)

        edges = [
            edge_dict for edge_dict in edges if node.id not in edge_dict["node_ids"]
        ]

        with open(self.edge_file_path, "w") as file:
            json.dump(edges, file, indent=4)
