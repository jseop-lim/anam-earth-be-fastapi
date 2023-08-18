from abc import ABC, abstractmethod

from map_admin.application.dtos import (
    CreateNodeInputData,
    CreateNodeOutputData,
    ListNodesOutputData,
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
