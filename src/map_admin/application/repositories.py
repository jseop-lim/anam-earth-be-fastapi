from abc import ABC, abstractmethod

from map_admin.domain.entities import Node


class NodeRepository(ABC):
    @abstractmethod
    def get_next_id(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_all_nodes(self) -> list[Node]:
        raise NotImplementedError

    @abstractmethod
    def create_node(self, node: Node) -> None:
        raise NotImplementedError
