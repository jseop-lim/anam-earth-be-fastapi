import json
import os
from decimal import Decimal
from tempfile import NamedTemporaryFile
from typing import Generator

import pytest

from map_admin.domain.entities import Node
from map_admin.domain.value_objects import Point
from map_admin.infrastructure.repositories import FileNodeRepository


@pytest.fixture()
def temp_file_path() -> Generator[str, None, None]:
    with NamedTemporaryFile(mode="w", delete=False) as file:
        json.dump([], file)
        file_path: str = file.name

    yield file_path

    # cleanup after test
    os.unlink(file_path)


def test_get_all_nodes(
    temp_file_path: str,
) -> None:
    nodes: list[dict[str, str]] = [
        {"name": "Node 1", "longitude": "1.0", "latitude": "2.0"},
        {"name": "Node 2", "longitude": "3.0", "latitude": "4.0"},
    ]
    with open(temp_file_path, "w") as file:
        json.dump(nodes, file)

    node_repo = FileNodeRepository(file_path=temp_file_path)
    result = node_repo.get_all_nodes()

    assert result == [
        Node(
            name="Node 1",
            point=Point(
                longitude=Decimal("1.0"),
                latitude=Decimal("2.0"),
            ),
        ),
        Node(
            name="Node 2",
            point=Point(
                longitude=Decimal("3.0"),
                latitude=Decimal("4.0"),
            ),
        ),
    ]


def test_create_node(
    temp_file_path: str,
) -> None:
    new_node = Node(
        name="Node 3",
        point=Point(
            longitude=Decimal("5.0"),
            latitude=Decimal("6.0"),
        ),
    )

    node_repo = FileNodeRepository(file_path=temp_file_path)
    node_repo.create_node(node=new_node)

    with open(temp_file_path, "r") as file:
        result = json.load(file)
    assert result[-1] == {"name": "Node 3", "longitude": "5.0", "latitude": "6.0"}
