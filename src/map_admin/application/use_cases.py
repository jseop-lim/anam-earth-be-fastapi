from map_admin.application.boundaries import ListNodesInputBoundary
from map_admin.application.boundaries import ListNodesOutputBoundary
from map_admin.application.dtos import ListNodesOutputData
from map_admin.application.repositories import NodeRepository
from map_admin.domain.entities import Node


class ListNodesUseCase(ListNodesInputBoundary):
    def __init__(
        self,
        node_repo: NodeRepository,
        output_boundary: ListNodesOutputBoundary,
    ) -> None:
        self.node_repo = node_repo
        self.output_boundary = output_boundary

    def execute(self) -> None:
        nodes: list[Node] = self.node_repo.get_all_nodes()
        output_data_list: list[ListNodesOutputData] = [
            ListNodesOutputData(
                name=node.name,
                longitude=node.point.longitude,
                latitude=node.point.latitude,
            )
            for node in nodes
        ]
        self.output_boundary.present(output_data_list=output_data_list)
