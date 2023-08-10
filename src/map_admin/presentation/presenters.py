from typing import TypeAlias

from typing_extensions import TypedDict

from map_admin.application.boundaries import ListNodesOutputBoundary
from map_admin.application.dtos import ListNodesOutputData


class NodeJsonViewModel(TypedDict):
    name: str
    longitude: float
    latitude: float


ListNodesJsonViewModel: TypeAlias = list[NodeJsonViewModel]


class ListNodesJsonPresenter(ListNodesOutputBoundary):
    def present(self, output_data_list: list[ListNodesOutputData]) -> None:
        self._view_model: ListNodesJsonViewModel = [
            NodeJsonViewModel(
                name=output_data.name,
                longitude=float(output_data.longitude),
                latitude=float(output_data.latitude),
            )
            for output_data in output_data_list
        ]

    def get_view_model(self) -> ListNodesJsonViewModel:
        return self._view_model
