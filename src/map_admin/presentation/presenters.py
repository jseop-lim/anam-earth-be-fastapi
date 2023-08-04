from typing_extensions import TypedDict

from map_admin.application.boundaries import ListNodesOutputBoundary
from map_admin.application.dtos import ListNodesOutputData


class ListNodesJsonViewModel(TypedDict):
    name: str
    longitude: str
    latitude: str


class ListNodesJsonPresenter(ListNodesOutputBoundary):
    def present(self, output_data_list: list[ListNodesOutputData]) -> None:
        self._view_model: list[ListNodesJsonViewModel] = [
            ListNodesJsonViewModel(
                name=output_data.name,
                longitude=f"{output_data.longitude:.6f}",
                latitude=f"{output_data.latitude:.6f}",
            )
            for output_data in output_data_list
        ]

    def get_view_model(self) -> list[ListNodesJsonViewModel]:
        return self._view_model
