from typing import TypeAlias

from pydantic import BaseModel

from map_admin.application.boundaries import (
    CreateNodeOutputBoundary,
    ListNodesOutputBoundary,
)
from map_admin.application.dtos import CreateNodeOutputData, ListNodesOutputData


class NodePydanticViewModel(BaseModel):
    id: int
    name: str
    longitude: float
    latitude: float


ListNodesPydanticViewModel: TypeAlias = list[NodePydanticViewModel]


class ListNodesPydanticPresenter(ListNodesOutputBoundary):
    def present(self, output_data_list: list[ListNodesOutputData]) -> None:
        self._view_model: ListNodesPydanticViewModel = [
            NodePydanticViewModel(
                id=output_data.id,
                name=output_data.name,
                longitude=float(output_data.longitude),
                latitude=float(output_data.latitude),
            )
            for output_data in output_data_list
        ]

    def get_view_model(self) -> ListNodesPydanticViewModel:
        return self._view_model


class CreateNodePydanticViewModel(BaseModel):
    id: int


class CreateNodePydanticPresenter(CreateNodeOutputBoundary):
    def present(self, output_data: CreateNodeOutputData) -> None:
        self._view_model = CreateNodePydanticViewModel(
            id=output_data.id,
        )

    def get_view_model(self) -> CreateNodePydanticViewModel:
        return self._view_model
