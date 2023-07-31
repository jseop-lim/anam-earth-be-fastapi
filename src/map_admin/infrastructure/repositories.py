from decimal import Decimal

from map_admin.application.repositories import NodeRepository
from map_admin.domain.entities import Node
from map_admin.domain.value_objects import Point


class FakeNodeRepository(NodeRepository):
    def get_all_nodes(self) -> list[Node]:
        return [
            Node(name='A', point=Point(longitude=Decimal('1.0'), latitude=Decimal('2.0'))),
            Node(name='B', point=Point(longitude=Decimal('3.0'), latitude=Decimal('4.0'))),
        ]

    def create_node(self, node: Node) -> None:
        print(f'Create node: {node}')
