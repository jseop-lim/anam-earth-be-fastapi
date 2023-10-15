import json
import os
from decimal import Decimal
from tempfile import NamedTemporaryFile
from typing import Generator

import pytest

from map_admin.application.repositories import NodeRepository
from map_admin.domain.entities import Edge, Node
from map_admin.domain.value_objects import Point, RoadQuality
from map_admin.infrastructure.repositories import FileEdge, FileNode, FileNodeRepository


@pytest.fixture()
def temp_node_file_path() -> Generator[str, None, None]:
    with NamedTemporaryFile(mode="w", delete=False) as file:
        json.dump([], file)
        file_path: str = file.name

    yield file_path

    # cleanup after test
    os.unlink(file_path)


@pytest.fixture()
def temp_edge_file_path() -> Generator[str, None, None]:
    with NamedTemporaryFile(mode="w", delete=False) as file:
        json.dump([], file)
        file_path: str = file.name

    yield file_path

    # cleanup after test
    os.unlink(file_path)


@pytest.mark.parametrize(
    "nodes, expected_next_id",
    [
        (
            [],
            1,
        ),
        (
            [
                {"id": 1, "name": "Node 1", "longitude": "1.0", "latitude": "2.0"},
                {"id": 3, "name": "Node 3", "longitude": "3.0", "latitude": "4.0"},
            ],
            4,
        ),
    ],
)
def test_get_next_id(
    temp_node_file_path: str,
    nodes: list[FileNode],
    expected_next_id: int,
) -> None:
    with open(temp_node_file_path, "w") as file:
        json.dump(nodes, file)

    node_repo = FileNodeRepository(
        node_file_path=temp_node_file_path,
        edge_file_path="",
    )
    result = node_repo.get_next_id()

    assert result == expected_next_id


def test_get_all_nodes(
    temp_node_file_path: str,
    temp_edge_file_path: str,
) -> None:
    nodes: list[FileNode] = [
        {"id": 1, "name": "Node 1", "longitude": "1.0", "latitude": "2.0"},
        {"id": 2, "name": "Node 2", "longitude": "3.0", "latitude": "4.0"},
        {"id": 3, "name": "Node 3", "longitude": "5.0", "latitude": "6.0"},
    ]
    edges: list[FileEdge] = [
        {
            "node_ids": (2, 1),
            "vertical_distance": "1.0",
            "horizontal_distance": "2.0",
            "is_stair": False,
            "is_step": False,
            "quality": "상",
        },
    ]
    with open(temp_node_file_path, "w") as file:
        json.dump(nodes, file)
    with open(temp_edge_file_path, "w") as file:
        json.dump(edges, file)

    node_repo = FileNodeRepository(
        node_file_path=temp_node_file_path,
        edge_file_path=temp_edge_file_path,
    )
    result = node_repo.get_all_nodes()

    assert result == [
        Node(
            id=1,
            name="Node 1",
            point=Point(
                longitude=Decimal("1.0"),
                latitude=Decimal("2.0"),
            ),
            edges=[
                Edge(
                    node_ids=(2, 1),
                    vertical_distance=Decimal("1.0"),
                    horizontal_distance=Decimal("2.0"),
                    is_stair=False,
                    is_step=False,
                    quality=RoadQuality.HIGH,
                ),
            ],
        ),
        Node(
            id=2,
            name="Node 2",
            point=Point(
                longitude=Decimal("3.0"),
                latitude=Decimal("4.0"),
            ),
            edges=[
                Edge(
                    node_ids=(2, 1),
                    vertical_distance=Decimal("1.0"),
                    horizontal_distance=Decimal("2.0"),
                    is_stair=False,
                    is_step=False,
                    quality=RoadQuality.HIGH,
                ),
            ],
        ),
        Node(
            id=3,
            name="Node 3",
            point=Point(
                longitude=Decimal("5.0"),
                latitude=Decimal("6.0"),
            ),
            edges=[],
        ),
    ]


def test_get_node_by_id(
    temp_node_file_path: str,
    temp_edge_file_path: str,
) -> None:
    nodes: list[FileNode] = [
        {"id": 1, "name": "Node 1", "longitude": "1.0", "latitude": "2.0"},
        {"id": 2, "name": "Node 2", "longitude": "3.0", "latitude": "4.0"},
    ]
    edges: list[FileEdge] = [
        {
            "node_ids": (1, 2),
            "vertical_distance": "1.0",
            "horizontal_distance": "2.0",
            "is_stair": False,
            "is_step": False,
            "quality": "상",
        },
    ]
    with open(temp_node_file_path, "w") as file:
        json.dump(nodes, file)
    with open(temp_edge_file_path, "w") as file:
        json.dump(edges, file)

    node_repo = FileNodeRepository(
        node_file_path=temp_node_file_path,
        edge_file_path=temp_edge_file_path,
    )
    result = node_repo.get_node_by_id(node_id=1)

    assert result == Node(
        id=1,
        name="Node 1",
        point=Point(
            longitude=Decimal("1.0"),
            latitude=Decimal("2.0"),
        ),
    )
    assert result.edges == [
        Edge(
            node_ids=(1, 2),
            vertical_distance=Decimal("1.0"),
            horizontal_distance=Decimal("2.0"),
            is_stair=False,
            is_step=False,
            quality=RoadQuality.HIGH,
        ),
    ]


def test_get_node_by_id_with_invalid_id(
    temp_node_file_path: str,
    temp_edge_file_path: str,
) -> None:
    node_repo = FileNodeRepository(
        node_file_path=temp_node_file_path,
        edge_file_path=temp_edge_file_path,
    )
    with pytest.raises(NodeRepository.NodeNotFoundError):
        node_repo.get_node_by_id(node_id=2)


def test_create_node(
    temp_node_file_path: str,
) -> None:
    new_node = Node(
        id=3,
        name="Node 3",
        point=Point(
            longitude=Decimal("5.0"),
            latitude=Decimal("6.0"),
        ),
    )

    node_repo = FileNodeRepository(
        node_file_path=temp_node_file_path,
        edge_file_path="",
    )
    node_repo.create_node(node=new_node)

    with open(temp_node_file_path, "r") as file:
        result: list[FileNode] = json.load(file)
    assert result[-1] == {
        "id": 3,
        "name": "Node 3",
        "longitude": "5.0",
        "latitude": "6.0",
    }


def test_update_node(
    temp_node_file_path: str,
    temp_edge_file_path: str,
) -> None:
    nodes: list[FileNode] = [
        {"id": 1, "name": "Node 1", "longitude": "1.0", "latitude": "2.0"},
        {"id": 2, "name": "Node 2", "longitude": "3.0", "latitude": "4.0"},
        {"id": 3, "name": "Node 3", "longitude": "5.0", "latitude": "6.0"},
    ]
    edges: list[FileEdge] = [
        {
            "node_ids": (1, 2),
            "vertical_distance": "1.0",
            "horizontal_distance": "2.0",
            "is_stair": False,
            "is_step": False,
            "quality": "상",
        },
        {
            "node_ids": (1, 3),
            "vertical_distance": "3.0",
            "horizontal_distance": "4.0",
            "is_stair": False,
            "is_step": False,
            "quality": "상",
        },
        {
            "node_ids": (2, 3),
            "vertical_distance": "5.0",
            "horizontal_distance": "6.0",
            "is_stair": False,
            "is_step": False,
            "quality": "상",
        },
    ]
    with open(temp_node_file_path, "w") as file:
        json.dump(nodes, file)
    with open(temp_edge_file_path, "w") as file:
        json.dump(edges, file)

    node_repo = FileNodeRepository(
        node_file_path=temp_node_file_path,
        edge_file_path=temp_edge_file_path,
    )
    node_repo.update_node(
        node=Node(
            id=1,
            name="Node 1 Updated",
            point=Point(
                longitude=Decimal("5.0"),
                latitude=Decimal("6.0"),
            ),
            edges=[
                Edge(
                    node_ids=(1, 2),
                    vertical_distance=Decimal("11.0"),
                    horizontal_distance=Decimal("12.0"),
                    is_stair=True,
                    is_step=True,
                    quality=RoadQuality.LOW,
                ),
            ],
        ),
    )

    with open(temp_node_file_path, "r") as file:
        node_result: list[FileNode] = json.load(file)
    with open(temp_edge_file_path, "r") as file:
        edge_result: list[FileEdge] = json.load(file)
    assert node_result == [
        {"id": 1, "name": "Node 1 Updated", "longitude": "5.0", "latitude": "6.0"},
        {"id": 2, "name": "Node 2", "longitude": "3.0", "latitude": "4.0"},
        {"id": 3, "name": "Node 3", "longitude": "5.0", "latitude": "6.0"},
    ]
    assert edge_result == [
        {
            "node_ids": [2, 3],
            "vertical_distance": "5.0",
            "horizontal_distance": "6.0",
            "is_stair": False,
            "is_step": False,
            "quality": "상",
        },
        {
            "node_ids": [1, 2],
            "vertical_distance": "11.0",
            "horizontal_distance": "12.0",
            "is_stair": True,
            "is_step": True,
            "quality": "하",
        },
    ]


def test_delete_node(
    temp_node_file_path: str,
    temp_edge_file_path: str,
) -> None:
    nodes: list[FileNode] = [
        {"id": 1, "name": "Node 1", "longitude": "1.0", "latitude": "2.0"},
        {"id": 2, "name": "Node 2", "longitude": "3.0", "latitude": "4.0"},
    ]
    edges: list[FileEdge] = [
        {
            "node_ids": (1, 2),
            "vertical_distance": "1.0",
            "horizontal_distance": "2.0",
            "is_stair": False,
            "is_step": False,
            "quality": "상",
        },
    ]
    with open(temp_edge_file_path, "w") as file:
        json.dump(edges, file)
    with open(temp_node_file_path, "w") as file:
        json.dump(nodes, file)

    node_repo = FileNodeRepository(
        node_file_path=temp_node_file_path,
        edge_file_path=temp_edge_file_path,
    )
    node_repo.delete_node(
        node=Node(
            id=1,
            name="Node 1",
            point=Point(
                longitude=Decimal("1.0"),
                latitude=Decimal("2.0"),
            ),
        ),
    )

    with open(temp_node_file_path, "r") as file:
        node_result: list[FileNode] = json.load(file)
    with open(temp_edge_file_path, "r") as file:
        edge_result: list[FileEdge] = json.load(file)
    assert node_result == [
        {"id": 2, "name": "Node 2", "longitude": "3.0", "latitude": "4.0"},
    ]
    assert edge_result == []
