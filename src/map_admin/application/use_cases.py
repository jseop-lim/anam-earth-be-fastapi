from map_admin.application.boundaries import (
    CreateNodeInputBoundary,
    CreateNodeOutputBoundary,
    ListNodesInputBoundary,
    ListNodesOutputBoundary,
)
from map_admin.application.dtos import (
    CreateNodeInputData,
    CreateNodeOutputData,
    ListNodesOutputData,
)
from map_admin.application.repositories import NodeRepository
from map_admin.domain.entities import Node
from map_admin.domain.value_objects import Point


class ListNodesUseCase(ListNodesInputBoundary):
    def __init__(self, node_repo: NodeRepository) -> None:
        self.node_repo = node_repo

    def execute(self, output_boundary: ListNodesOutputBoundary) -> None:
        nodes: list[Node] = self.node_repo.get_all_nodes()
        output_data_list: list[ListNodesOutputData] = [
            ListNodesOutputData(
                id=node.id,
                name=node.name,
                longitude=node.point.longitude,
                latitude=node.point.latitude,
            )
            for node in nodes
        ]
        output_boundary.present(output_data_list=output_data_list)


class CreateNodeUseCase(CreateNodeInputBoundary):
    def __init__(self, node_repo: NodeRepository) -> None:
        self.node_repo = node_repo

    def execute(
        self,
        input_data: CreateNodeInputData,
        output_boundary: CreateNodeOutputBoundary,
    ) -> None:
        node_id: int = self.node_repo.get_next_id()
        node = Node(
            id=node_id,
            name=input_data.name,
            point=Point(
                longitude=input_data.longitude,
                latitude=input_data.latitude,
            ),
        )
        self.node_repo.create_node(node=node)
        output_data = CreateNodeOutputData(
            id=node_id,
        )
        output_boundary.present(output_data=output_data)
