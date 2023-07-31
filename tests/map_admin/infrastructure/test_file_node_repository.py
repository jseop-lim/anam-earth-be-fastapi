import json
import os
from decimal import Decimal
from tempfile import NamedTemporaryFile

from map_admin.domain.entities import Node
from map_admin.domain.value_objects import Point
from map_admin.infrastructure.repositories import FileNodeRepository


def test_get_all_nodes() -> None:
    nodes = [
        {'name': 'Node 1', 'longitude': '1.0', 'latitude': '2.0'},
        {'name': 'Node 2', 'longitude': '3.0', 'latitude': '4.0'},
    ]
    with NamedTemporaryFile(mode='w', delete=False) as file:
        json.dump(nodes, file)
        file_path = file.name

    repo = FileNodeRepository(file_path=file_path)

    result = repo.get_all_nodes()
    assert result == [
        Node(
            name='Node 1',
            point=Point(
                longitude=Decimal('1.0'),
                latitude=Decimal('2.0'),
            ),
        ),
        Node(
            name='Node 2',
            point=Point(
                longitude=Decimal('3.0'),
                latitude=Decimal('4.0'),
            ),
        ),
    ]

    os.unlink(file_path)


def test_create_node() -> None:
    nodes = [
        {'name': 'Node 1', 'longitude': '1.0', 'latitude': '2.0'},
        {'name': 'Node 2', 'longitude': '3.0', 'latitude': '4.0'},
    ]
    with NamedTemporaryFile(mode='w', delete=False) as file:
        json.dump(nodes, file)
        file_path = file.name

    repo = FileNodeRepository(file_path=file_path)
    new_node = Node(
        name='Node 3',
        point=Point(
            longitude=Decimal('5.0'),
            latitude=Decimal('6.0'),
        ),
    )

    repo.create_node(node=new_node)

    with open(file_path, 'r') as file:
        result = json.load(file)
    assert result[-1] == {'name': 'Node 3', 'longitude': '5.0', 'latitude': '6.0'}

    os.unlink(file_path)
