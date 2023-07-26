from abc import ABC
from abc import abstractmethod

from map_admin.domain.entities import Node


class NodeRepository(ABC):
    @abstractmethod
    def get_all_nodes(self) -> list[Node]:
        raise NotImplementedError
