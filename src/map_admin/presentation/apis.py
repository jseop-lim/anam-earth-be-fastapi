from decimal import Decimal
from typing import Literal

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from containers import Container
from map_admin.application.boundaries import (
    CreateEdgeInputBoundary,
    CreateNodeInputBoundary,
    DeleteNodeInputBoundary,
    ListEdgesInputBoundary,
    ListNodesInputBoundary,
    PartialUpdateNodeInputBoundary,
)
from map_admin.application.dtos import (
    CreateEdgeInputData,
    CreateNodeInputData,
    DeleteNodeInputData,
    PartialUpdateNodeInputData,
)
from map_admin.presentation.presenters import (
    CreateNodePydanticPresenter,
    CreateNodePydanticViewModel,
    ListEdgesPydanticPresenter,
    ListEdgesPydanticViewModel,
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


@router.delete(
    "/nodes/{node_id}",
    status_code=status.HTTP_204_NO_CONTENT,
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
async def delete_node(
    node_id: int,
    use_case: DeleteNodeInputBoundary = Depends(
        Provide[Container.delete_node_use_case]
    ),
) -> None:
    try:
        use_case.execute(
            input_data=DeleteNodeInputData(
                id=node_id,
            ),
        )
    except DeleteNodeInputBoundary.NodeNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Node not found",
        )


@router.get("/edges")
@inject
async def list_edges(
    use_case: ListEdgesInputBoundary = Depends(Provide[Container.list_edges_use_case]),
) -> ListEdgesPydanticViewModel:
    presenter = ListEdgesPydanticPresenter()
    use_case.execute(output_boundary=presenter)
    return presenter.get_view_model()


class CreateEdgeRequest(BaseModel):
    node_ids: tuple[int, int]
    vertical_distance: float
    horizontal_distance: float
    is_stair: bool
    is_step: bool
    quality: Literal["상", "중", "하"]


@router.post("/edges", status_code=status.HTTP_201_CREATED)
@inject
async def create_edge(
    edge: CreateEdgeRequest,
    use_case: CreateEdgeInputBoundary = Depends(
        Provide[Container.create_edge_use_case]
    ),
) -> str:
    try:
        use_case.execute(
            input_data=CreateEdgeInputData(
                node_ids=edge.node_ids,
                vertical_distance=Decimal(str(edge.vertical_distance)),
                horizontal_distance=Decimal(str(edge.horizontal_distance)),
                is_stair=edge.is_stair,
                is_step=edge.is_step,
                quality=edge.quality,
            ),
        )
    except CreateEdgeInputBoundary.NodeNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Node ID",
        )
    except CreateEdgeInputBoundary.ConnectingSameNodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Same node",
        )
    except CreateEdgeInputBoundary.AlreadyConnectedNodesError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already exsiting edge",
        )
    return "OK"
