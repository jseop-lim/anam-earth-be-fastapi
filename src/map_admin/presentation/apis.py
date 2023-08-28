from decimal import Decimal

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from containers import Container
from map_admin.application.boundaries import (
    CreateNodeInputBoundary,
    ListNodesInputBoundary,
    PartialUpdateNodeInputBoundary,
)
from map_admin.application.dtos import CreateNodeInputData, PartialUpdateNodeInputData
from map_admin.presentation.presenters import (
    CreateNodePydanticPresenter,
    CreateNodePydanticViewModel,
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
) -> CreateNodePydanticViewModel:
    presneter = CreateNodePydanticPresenter()
    use_case.execute(
        input_data=CreateNodeInputData(
            name=node.name,
            longitude=Decimal(str(node.longitude)),
            latitude=Decimal(str(node.latitude)),
        ),
        output_boundary=presneter,
    )
    return presneter.get_view_model()


class PartialUpdateNodeRequest(BaseModel):
    name: str | None
    longitude: float | None
    latitude: float | None


@router.patch(
    "/nodes/{node_id}",
    responses={
        # TODO: Separate by defining as a new variable
        status.HTTP_404_NOT_FOUND: {
            "content": {
                "application/json": {
                    "example": {"detail": "Node not found"},
                },
            },
        },
    },
)
@inject
async def partial_update_node(
    node_id: int,
    node: PartialUpdateNodeRequest,
    use_case: PartialUpdateNodeInputBoundary = Depends(
        Provide[Container.partial_update_node_use_case]
    ),
) -> None:
    try:
        use_case.execute(
            input_data=PartialUpdateNodeInputData(
                id=node_id,
                name=node.name,
                longitude=(
                    None if node.longitude is None else Decimal(str(node.longitude))
                ),
                latitude=(
                    None if node.latitude is None else Decimal(str(node.latitude))
                ),
            ),
        )
    # TODO: Use custom exception handler
    except PartialUpdateNodeInputBoundary.NodeNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Node not found",
        )
