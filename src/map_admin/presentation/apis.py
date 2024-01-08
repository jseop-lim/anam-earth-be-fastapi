from decimal import Decimal
from typing import Literal

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from containers import Container
from map_admin.application.boundaries import (
    CreateEdgeInputBoundary,
    CreateNodeInputBoundary,
    DeleteEdgeInputBoundary,
    DeleteNodeInputBoundary,
    ListEdgesInputBoundary,
    ListNodesInputBoundary,
    PartialUpdateEdgeInputBoundary,
    PartialUpdateNodeInputBoundary,
)
from map_admin.application.dtos import (
    CreateEdgeInputData,
    CreateNodeInputData,
    DeleteEdgeInputData,
    DeleteNodeInputData,
    PartialUpdateEdgeInputData,
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
    name: str | None = None
    longitude: float | None = None
    latitude: float | None = None


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


class PartialUpdateEdgeRequest(BaseModel):
    vertical_distance: float | None = None
    horizontal_distance: float | None = None
    is_stair: bool | None = None
    is_step: bool | None = None
    quality: Literal["상", "중", "하"] | None = None


@router.patch(
    "/edges/{node_id_1}/{node_id_2}",
    responses={
        # TODO: Separate by defining as a new variable
        status.HTTP_404_NOT_FOUND: {
            "content": {
                "application/json": {
                    "examples": {
                        "Node Not Found": {"detail": "Invalid Node ID"},
                        "Connecting same node": {"detail": "Same node"},
                        "Edge not found": {"detail": "Edge not found"},
                    },
                },
            },
        },
    },
)
@inject
async def partial_update_edge(
    node_id_1: int,
    node_id_2: int,
    edge: PartialUpdateEdgeRequest,
    use_case: PartialUpdateEdgeInputBoundary = Depends(
        Provide[Container.partial_update_edge_use_case]
    ),
) -> None:
    try:
        use_case.execute(
            input_data=PartialUpdateEdgeInputData(
                node_ids=(node_id_1, node_id_2),
                vertical_distance=(
                    None
                    if edge.vertical_distance is None
                    else Decimal(str(edge.vertical_distance))
                ),
                horizontal_distance=(
                    None
                    if edge.horizontal_distance is None
                    else Decimal(str(edge.horizontal_distance))
                ),
                is_stair=edge.is_stair,
                is_step=edge.is_step,
                quality=edge.quality,
            ),
        )
    except PartialUpdateEdgeInputBoundary.NodeNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Node ID",
        )
    except PartialUpdateEdgeInputBoundary.ConnectingSameNodeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Same node",
        )
    except PartialUpdateEdgeInputBoundary.EdgeNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Edge not found",
        )


@router.delete(
    "/edge/{node_id_1}/{node_id_2}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        # TODO: Separate by defining as a new variable
        status.HTTP_404_NOT_FOUND: {
            "content": {
                "application/json": {
                    "examples": {
                        "Node Not Found": {"detail": "Invalid Node ID"},
                        "Connecting same node": {"detail": "Same node"},
                        "Edge not found": {"detail": "Edge not found"},
                    },
                },
            },
        },
    },
)
@inject
async def delete_edge(
    node_id_1: int,
    node_id_2: int,
    use_case: DeleteEdgeInputBoundary = Depends(
        Provide[Container.delete_edge_use_case]
    ),
) -> None:
    try:
        use_case.execute(
            input_data=DeleteEdgeInputData(
                node_ids=(node_id_1, node_id_2),
            ),
        )
    except DeleteEdgeInputBoundary.NodeNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Node ID",
        )
    except DeleteEdgeInputBoundary.ConnectingSameNodeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Same node",
        )
    except DeleteEdgeInputBoundary.EdgeNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Edge not found",
        )
