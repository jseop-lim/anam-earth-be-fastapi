from map_admin.application.boundaries import (
    CreateNodeInputBoundary,
    CreateNodeOutputBoundary,
    DeleteNodeInputBoundary,
    ListNodesInputBoundary,
    ListNodesOutputBoundary,
    PartialUpdateNodeInputBoundary,
)
from map_admin.application.dtos import (
    CreateNodeInputData,
    CreateNodeOutputData,
    DeleteNodeInputData,
    ListNodesOutputData,
    PartialUpdateNodeInputData,
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


class PartialUpdateNodeUseCase(PartialUpdateNodeInputBoundary):
    def __init__(self, node_repo: NodeRepository) -> None:
        self.node_repo = node_repo

    def execute(self, input_data: PartialUpdateNodeInputData) -> None:
        try:
            node: Node = self.node_repo.get_node_by_id(node_id=input_data.id)
        except NodeRepository.NodeNotFoundError:
            raise super().NodeNotFoundError

        if input_data.name:
            node.update_name(name=input_data.name)
        if input_data.longitude or input_data.latitude:
            node.update_point(
                point=Point(
                    longitude=input_data.longitude or node.point.longitude,
                    latitude=input_data.latitude or node.point.latitude,
                ),
            )
        self.node_repo.update_node(node=node)


class DeleteNodeUseCase(DeleteNodeInputBoundary):
    def __init__(self, node_repo: NodeRepository) -> None:
        self.node_repo = node_repo

    def execute(self, input_data: DeleteNodeInputData) -> None:
        try:
            node: Node = self.node_repo.get_node_by_id(node_id=input_data.id)
        except NodeRepository.NodeNotFoundError:
            raise super().NodeNotFoundError

        self.node_repo.delete_node(node=node)
