from abc import ABC
from abc import abstractmethod

from map_admin.application.dtos import CreateNodeInputData
from map_admin.application.dtos import ListNodesOutputData


class ListNodesInputBoundary(ABC):
    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError


class ListNodesOutputBoundary(ABC):
    @abstractmethod
    def present(self, output_data_list: list[ListNodesOutputData]) -> None:
        raise NotImplementedError


class CreateNodeInputBoundary(ABC):
    @abstractmethod
    def execute(self, input_data: CreateNodeInputData) -> None:
        raise NotImplementedError
