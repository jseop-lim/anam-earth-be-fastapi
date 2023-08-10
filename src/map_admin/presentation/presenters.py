from typing import TypeAlias

from typing_extensions import TypedDict

from map_admin.application.boundaries import ListNodesOutputBoundary
from map_admin.application.dtos import ListNodesOutputData


class NodePydanticViewModel(TypedDict):
    name: str
    longitude: float
    latitude: float


ListNodesPydanticViewModel: TypeAlias = list[NodePydanticViewModel]


class ListNodesPydanticPresenter(ListNodesOutputBoundary):
    def present(self, output_data_list: list[ListNodesOutputData]) -> None:
        self._view_model: ListNodesPydanticViewModel = [
            NodePydanticViewModel(
                name=output_data.name,
                longitude=float(output_data.longitude),
                latitude=float(output_data.latitude),
            )
            for output_data in output_data_list
        ]

    def get_view_model(self) -> ListNodesPydanticViewModel:
        return self._view_model
