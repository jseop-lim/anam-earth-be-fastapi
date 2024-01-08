from map_admin.application.boundaries import (
    CreateEdgeInputBoundary,
    CreateNodeInputBoundary,
    CreateNodeOutputBoundary,
    DeleteNodeInputBoundary,
    ListEdgesInputBoundary,
    ListEdgesOutputBoundary,
    ListNodesInputBoundary,
    ListNodesOutputBoundary,
    PartialUpdateEdgeInputBoundary,
    PartialUpdateNodeInputBoundary,
)
from map_admin.application.dtos import (
    CreateEdgeInputData,
    CreateNodeInputData,
    CreateNodeOutputData,
    DeleteNodeInputData,
    ListEdgesOutputData,
    ListNodesOutputData,
    PartialUpdateEdgeInputData,
    PartialUpdateNodeInputData,
)
from map_admin.application.repositories import NodeRepository
from map_admin.domain.entities import Edge, Node
from map_admin.domain.exceptions import (
    AlreadyConnectedNodesError,
    ConnectingSameNodeError,
    NoEdgeExistsBetweenNodesError,
)
from map_admin.domain.value_objects import Point, RoadQuality


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

        if input_data.name is not None:
            node.update_name(name=input_data.name)
        if input_data.longitude is not None or input_data.latitude is not None:
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


class ListEdgesUseCase(ListEdgesInputBoundary):
    def __init__(self, node_repo: NodeRepository) -> None:
        self.node_repo = node_repo

    def execute(self, output_boundary: ListEdgesOutputBoundary) -> None:
        nodes: list[Node] = self.node_repo.get_all_nodes()
        node_dict: dict[int, Node] = {node.id: node for node in nodes}
        edge_dict: dict[tuple[int, ...], Edge] = {
            tuple(sorted(edge.node_ids)): edge for node in nodes for edge in node.edges
        }
        output_data_list: list[ListEdgesOutputData] = [
            ListEdgesOutputData(
                nodes=(
                    ListEdgesOutputData.Node(
                        id=node_dict[node_ids[0]].id,
                        name=node_dict[node_ids[0]].name,
                    ),
                    ListEdgesOutputData.Node(
                        id=node_dict[node_ids[1]].id,
                        name=node_dict[node_ids[1]].name,
                    ),
                ),
                vertical_distance=edge.vertical_distance,
                horizontal_distance=edge.horizontal_distance,
                is_stair=edge.is_stair,
                is_step=edge.is_step,
                quality=edge.quality.value,
            )
            for node_ids, edge in edge_dict.items()
        ]
        output_boundary.present(output_data_list=output_data_list)


class CreateEdgeUseCase(CreateEdgeInputBoundary):
    def __init__(self, node_repo: NodeRepository) -> None:
        self.node_repo = node_repo

    def execute(self, input_data: CreateEdgeInputData) -> None:
        try:
            nodes: tuple[Node, Node] = (
                self.node_repo.get_node_by_id(node_id=input_data.node_ids[0]),
                self.node_repo.get_node_by_id(node_id=input_data.node_ids[1]),
            )
        except NodeRepository.NodeNotFoundError:
            raise super().NodeNotFoundError

        try:
            nodes[0].add_edge(
                other_node=nodes[1],
                vertical_distance=input_data.vertical_distance,
                horizontal_distance=input_data.horizontal_distance,
                is_stair=input_data.is_stair,
                is_step=input_data.is_step,
                quality=RoadQuality(input_data.quality),
            )
        except ConnectingSameNodeError:
            raise super().ConnectingSameNodeError
        except AlreadyConnectedNodesError:
            raise super().AlreadyConnectedNodesError

        self.node_repo.update_node(node=nodes[0])


class PartialUpdateEdgeUseCase(PartialUpdateEdgeInputBoundary):
    def __init__(self, node_repo: NodeRepository) -> None:
        self.node_repo = node_repo

    def execute(self, input_data: PartialUpdateEdgeInputData) -> None:
        try:
            nodes: tuple[Node, Node] = (
                self.node_repo.get_node_by_id(node_id=input_data.node_ids[0]),
                self.node_repo.get_node_by_id(node_id=input_data.node_ids[1]),
            )
        except NodeRepository.NodeNotFoundError:
            raise super().NodeNotFoundError

        try:
            nodes[0].update_edge(
                other_node=nodes[1],
                vertical_distance=input_data.vertical_distance,
                horizontal_distance=input_data.horizontal_distance,
                is_stair=input_data.is_stair,
                is_step=input_data.is_step,
                quality=(
                    None
                    if input_data.quality is None
                    else RoadQuality(input_data.quality)
                ),
            )
        except ConnectingSameNodeError:
            raise super().ConnectingSameNodeError
        except NoEdgeExistsBetweenNodesError:
            raise super().EdgeNotFoundError

        self.node_repo.update_node(node=nodes[0])
