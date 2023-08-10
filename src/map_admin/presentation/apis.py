from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from containers import Container
from map_admin.application.boundaries import ListNodesInputBoundary
from map_admin.presentation.presenters import (
    ListNodesJsonPresenter,
    ListNodesJsonViewModel,
)

router = APIRouter()


@router.get("/nodes")
@inject
async def list_nodes(
    use_case: ListNodesInputBoundary = Depends(Provide[Container.list_nodes_use_case]),
    presenter: ListNodesJsonPresenter = Depends(
        Provide[Container.list_nodes_json_presenter]
    ),
) -> ListNodesJsonViewModel:
    use_case.execute()
    return presenter.get_view_model()
