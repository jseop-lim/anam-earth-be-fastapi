from dependency_injector import containers, providers

from map_admin.application.use_cases import (
    CreateNodeUseCase,
    DeleteNodeUseCase,
    ListNodesUseCase,
    PartialUpdateNodeUseCase,
)
from map_admin.infrastructure.repositories import FileNodeRepository


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(
        strict=True,
    )

    node_repository = providers.Factory(
        FileNodeRepository,
        file_path=config.file.path,
    )
    list_nodes_use_case = providers.Factory(
        ListNodesUseCase,
        node_repo=node_repository,
    )
    create_node_use_case = providers.Factory(
        CreateNodeUseCase,
        node_repo=node_repository,
    )
    partial_update_node_use_case = providers.Factory(
        PartialUpdateNodeUseCase,
        node_repo=node_repository,
    )
    delete_node_use_case = providers.Factory(
        DeleteNodeUseCase,
        node_repo=node_repository,
    )
