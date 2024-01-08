from abc import ABC, abstractmethod

from map_admin.application.dtos import (
    CreateEdgeInputData,
    CreateNodeInputData,
    CreateNodeOutputData,
    DeleteNodeInputData,
    ListEdgesOutputData,
    ListNodesOutputData,
    PartialUpdateEdgeInputData,
    PartialUpdateNodeInputData,
)


class ListNodesOutputBoundary(ABC):
    @abstractmethod
    def present(self, output_data_list: list[ListNodesOutputData]) -> None:
        raise NotImplementedError


class ListNodesInputBoundary(ABC):
    @abstractmethod
    def execute(self, output_boundary: ListNodesOutputBoundary) -> None:
        raise NotImplementedError


class CreateNodeOutputBoundary(ABC):
    @abstractmethod
    def present(self, output_data: CreateNodeOutputData) -> None:
        raise NotImplementedError


class CreateNodeInputBoundary(ABC):
    @abstractmethod
    def execute(
        self,
        input_data: CreateNodeInputData,
        output_boundary: CreateNodeOutputBoundary,
    ) -> None:
        raise NotImplementedError


class PartialUpdateNodeInputBoundary(ABC):
    @abstractmethod
    def execute(self, input_data: PartialUpdateNodeInputData) -> None:
        raise NotImplementedError

    class NodeNotFoundError(Exception):
        """노드를 찾지 못할 때 발생하는 에러"""


class DeleteNodeInputBoundary(ABC):
    @abstractmethod
    def execute(self, input_data: DeleteNodeInputData) -> None:
        raise NotImplementedError

    class NodeNotFoundError(Exception):
        """노드를 찾지 못할 때 발생하는 에러"""


class ListEdgesOutputBoundary(ABC):
    @abstractmethod
    def present(self, output_data_list: list[ListEdgesOutputData]) -> None:
        raise NotImplementedError


class ListEdgesInputBoundary(ABC):
    @abstractmethod
    def execute(self, output_boundary: ListEdgesOutputBoundary) -> None:
        raise NotImplementedError


class CreateEdgeInputBoundary(ABC):
    @abstractmethod
    def execute(self, input_data: CreateEdgeInputData) -> None:
        raise NotImplementedError

    class NodeNotFoundError(Exception):
        """노드를 찾지 못할 때 발생하는 에러"""

    class ConnectingSameNodeError(Exception):
        """같은 노드끼리 간선으로 연결할 때 발생하는 에러"""

    class AlreadyConnectedNodesError(Exception):
        """이미 연결된 노드끼리 간선으로 연결할 때 발생하는 에러"""


class PartialUpdateEdgeInputBoundary(ABC):
    @abstractmethod
    def execute(self, input_data: PartialUpdateEdgeInputData) -> None:
        raise NotImplementedError

    class NodeNotFoundError(Exception):
        """노드를 찾지 못할 때 발생하는 에러"""

    class ConnectingSameNodeError(Exception):
        """같은 노드끼리 간선으로 연결할 때 발생하는 에러"""

    class EdgeNotFoundError(Exception):
        """간선을 찾지 못할 때 발생하는 에러"""
