from dependency_injector import containers, providers

from map_admin.application.use_cases import ListNodesUseCase
from map_admin.infrastructure.repositories import FileNodeRepository
from map_admin.presentation.presenters import ListNodesJsonPresenter


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(
        strict=True,
    )

    list_nodes_json_presenter = providers.Singleton(
        ListNodesJsonPresenter,
    )
    node_repository = providers.Factory(
        FileNodeRepository,
        file_path=config.file.path,
    )
    list_nodes_use_case = providers.Factory(
        ListNodesUseCase,
        node_repo=node_repository,
        output_boundary=list_nodes_json_presenter,
    )
