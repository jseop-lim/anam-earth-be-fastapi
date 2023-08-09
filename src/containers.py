from dependency_injector import containers, providers

from map_admin.application.use_cases import ListNodesUseCase
from map_admin.infrastructure.repositories import FileNodeRepository
from map_admin.presentation.presenters import ListNodesJsonPresenter


class Container(containers.DeclarativeContainer):
    list_nodes_json_presenter = providers.Singleton(ListNodesJsonPresenter)
    list_nodes_use_case = providers.Factory(
        ListNodesUseCase,
        node_repo=FileNodeRepository(file_path="data/nodes.json"),
        output_boundary=list_nodes_json_presenter,
    )
