from typing import TypeAlias

from pydantic import BaseModel

from map_admin.application.boundaries import (
    CreateNodeOutputBoundary,
    ListEdgesOutputBoundary,
    ListNodesOutputBoundary,
)
from map_admin.application.dtos import (
    CreateNodeOutputData,
    ListEdgesOutputData,
    ListNodesOutputData,
)


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


class EdgeNodePydanticViewModel(BaseModel):
    id: int
    name: str


class EdgePydanticViewModel(BaseModel):
    nodes: tuple[EdgeNodePydanticViewModel, EdgeNodePydanticViewModel]
    vertical_distance: float
    horizontal_distance: float
    is_stair: bool
    is_step: bool
    quality: str


ListEdgesPydanticViewModel: TypeAlias = list[EdgePydanticViewModel]


class ListEdgesPydanticPresenter(ListEdgesOutputBoundary):
    def present(self, output_data_list: list[ListEdgesOutputData]) -> None:
        self._view_model: ListEdgesPydanticViewModel = [
            EdgePydanticViewModel(
                nodes=(
                    EdgeNodePydanticViewModel(
                        id=output_data.nodes[0].id,
                        name=output_data.nodes[0].name,
                    ),
                    EdgeNodePydanticViewModel(
                        id=output_data.nodes[1].id,
                        name=output_data.nodes[1].name,
                    ),
                ),
                vertical_distance=float(output_data.vertical_distance),
                horizontal_distance=float(output_data.horizontal_distance),
                is_stair=output_data.is_stair,
                is_step=output_data.is_step,
                quality=output_data.quality,
            )
            for output_data in output_data_list
        ]

    def get_view_model(self) -> ListEdgesPydanticViewModel:
        return self._view_model
