import json
import os
from decimal import Decimal
from tempfile import NamedTemporaryFile
from typing import Generator

import pytest

from map_admin.application.repositories import NodeRepository
from map_admin.domain.entities import Node
from map_admin.domain.value_objects import Point
from map_admin.infrastructure.repositories import FileNode, FileNodeRepository


@pytest.fixture()
def temp_file_path() -> Generator[str, None, None]:
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
    temp_file_path: str,
    nodes: list[FileNode],
    expected_next_id: int,
) -> None:
    with open(temp_file_path, "w") as file:
        json.dump(nodes, file)

    node_repo = FileNodeRepository(file_path=temp_file_path)
    result = node_repo.get_next_id()

    assert result == expected_next_id


def test_get_all_nodes(
    temp_file_path: str,
) -> None:
    nodes: list[FileNode] = [
        {"id": 1, "name": "Node 1", "longitude": "1.0", "latitude": "2.0"},
        {"id": 2, "name": "Node 2", "longitude": "3.0", "latitude": "4.0"},
    ]
    with open(temp_file_path, "w") as file:
        json.dump(nodes, file)

    node_repo = FileNodeRepository(file_path=temp_file_path)
    result = node_repo.get_all_nodes()

    assert result == [
        Node(
            id=1,
            name="Node 1",
            point=Point(
                longitude=Decimal("1.0"),
                latitude=Decimal("2.0"),
            ),
        ),
        Node(
            id=2,
            name="Node 2",
            point=Point(
                longitude=Decimal("3.0"),
                latitude=Decimal("4.0"),
            ),
        ),
    ]


def test_get_node_by_id(
    temp_file_path: str,
) -> None:
    nodes: list[FileNode] = [
        {"id": 1, "name": "Node 1", "longitude": "1.0", "latitude": "2.0"},
    ]
    with open(temp_file_path, "w") as file:
        json.dump(nodes, file)

    node_repo = FileNodeRepository(file_path=temp_file_path)
    result = node_repo.get_node_by_id(node_id=1)

    assert result == Node(
        id=1,
        name="Node 1",
        point=Point(
            longitude=Decimal("1.0"),
            latitude=Decimal("2.0"),
        ),
    )


def test_get_node_by_id_with_invalid_id(
    temp_file_path: str,
) -> None:
    node_repo = FileNodeRepository(file_path=temp_file_path)
    with pytest.raises(NodeRepository.NodeNotFoundError):
        node_repo.get_node_by_id(node_id=2)


def test_create_node(
    temp_file_path: str,
) -> None:
    new_node = Node(
        id=3,
        name="Node 3",
        point=Point(
            longitude=Decimal("5.0"),
            latitude=Decimal("6.0"),
        ),
    )

    node_repo = FileNodeRepository(file_path=temp_file_path)
    node_repo.create_node(node=new_node)

    with open(temp_file_path, "r") as file:
        result: list[FileNode] = json.load(file)
    assert result[-1] == {
        "id": 3,
        "name": "Node 3",
        "longitude": "5.0",
        "latitude": "6.0",
    }


def test_update_node(
    temp_file_path: str,
) -> None:
    nodes: list[FileNode] = [
        {"id": 1, "name": "Node 1", "longitude": "1.0", "latitude": "2.0"},
        {"id": 2, "name": "Node 2", "longitude": "3.0", "latitude": "4.0"},
    ]
    with open(temp_file_path, "w") as file:
        json.dump(nodes, file)

    node_repo = FileNodeRepository(file_path=temp_file_path)
    node_repo.update_node(
        node=Node(
            id=1,
            name="Node 1 Updated",
            point=Point(
                longitude=Decimal("5.0"),
                latitude=Decimal("6.0"),
            ),
        ),
    )

    with open(temp_file_path, "r") as file:
        result: list[FileNode] = json.load(file)
    assert result == [
        {"id": 1, "name": "Node 1 Updated", "longitude": "5.0", "latitude": "6.0"},
        {"id": 2, "name": "Node 2", "longitude": "3.0", "latitude": "4.0"},
    ]


def test_delete_node(
    temp_file_path: str,
) -> None:
    nodes: list[FileNode] = [
        {"id": 1, "name": "Node 1", "longitude": "1.0", "latitude": "2.0"},
        {"id": 2, "name": "Node 2", "longitude": "3.0", "latitude": "4.0"},
    ]
    with open(temp_file_path, "w") as file:
        json.dump(nodes, file)

    node_repo = FileNodeRepository(file_path=temp_file_path)
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

    with open(temp_file_path, "r") as file:
        result: list[FileNode] = json.load(file)
    assert result == [
        {"id": 2, "name": "Node 2", "longitude": "3.0", "latitude": "4.0"},
    ]
