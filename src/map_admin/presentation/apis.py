from decimal import Decimal

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from containers import Container
from map_admin.application.boundaries import (
    CreateNodeInputBoundary,
    ListNodesInputBoundary,
)
from map_admin.application.dtos import CreateNodeInputData
from map_admin.presentation.presenters import (
    ListNodesPydanticPresenter,
    ListNodesPydanticViewModel,
)

router = APIRouter()


@router.get("/nodes")
@inject
async def list_nodes(
    use_case: ListNodesInputBoundary = Depends(Provide[Container.list_nodes_use_case]),
) -> ListNodesPydanticViewModel:
    presenter = ListNodesPydanticPresenter()
    use_case.execute(output_boundary=presenter)
    return presenter.get_view_model()


class CreateNodeRequest(BaseModel):
    name: str
    longitude: float
    latitude: float


@router.post("/nodes", status_code=status.HTTP_201_CREATED)
@inject
async def create_node(
    node: CreateNodeRequest,
    use_case: CreateNodeInputBoundary = Depends(
        Provide[Container.create_node_use_case]
    ),
) -> str:
    use_case.execute(
        input_data=CreateNodeInputData(
            name=node.name,
            longitude=Decimal(str(node.longitude)),
            latitude=Decimal(str(node.latitude)),
        ),
    )
    return "Success"
