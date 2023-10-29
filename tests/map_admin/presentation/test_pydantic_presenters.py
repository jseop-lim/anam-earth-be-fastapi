from decimal import Decimal

from map_admin.application.dtos import (
    CreateNodeOutputData,
    ListEdgesOutputData,
    ListNodesOutputData,
)
from map_admin.presentation.presenters import (
    CreateNodePydanticPresenter,
    CreateNodePydanticViewModel,
    EdgeNodePydanticViewModel,
    EdgePydanticViewModel,
    ListEdgesPydanticPresenter,
    ListNodesPydanticPresenter,
    NodePydanticViewModel,
)


def test_present_list_nodes() -> None:
    output_data_list: list[ListNodesOutputData] = [
        ListNodesOutputData(
            id=1,
            name="Node 1",
            longitude=Decimal("1.0"),
            latitude=Decimal("2.0"),
        ),
        ListNodesOutputData(
            id=2,
            name="Node 2",
            longitude=Decimal("3.0"),
            latitude=Decimal("4.0"),
        ),
    ]

    presenter = ListNodesPydanticPresenter()
    presenter.present(output_data_list=output_data_list)

    assert presenter.get_view_model() == [
        NodePydanticViewModel(
            id=1,
            name="Node 1",
            longitude=1.0,
            latitude=2.0,
        ),
        NodePydanticViewModel(
            id=2,
            name="Node 2",
            longitude=3.0,
            latitude=4.0,
        ),
    ]


def test_present_create_node() -> None:
    output_data = CreateNodeOutputData(id=1)

    presenter = CreateNodePydanticPresenter()
    presenter.present(output_data=output_data)

    assert presenter.get_view_model() == CreateNodePydanticViewModel(id=1)


def test_present_list_edges() -> None:
    output_data_list: list[ListEdgesOutputData] = [
        ListEdgesOutputData(
            nodes=(
                ListEdgesOutputData.Node(id=1, name="A"),
                ListEdgesOutputData.Node(id=2, name="B"),
            ),
            vertical_distance=Decimal("1.0"),
            horizontal_distance=Decimal("2.0"),
            is_stair=False,
            is_step=False,
            quality="상",
        ),
        ListEdgesOutputData(
            nodes=(
                ListEdgesOutputData.Node(id=1, name="A"),
                ListEdgesOutputData.Node(id=3, name="C"),
            ),
            vertical_distance=Decimal("3.0"),
            horizontal_distance=Decimal("4.0"),
            is_stair=False,
            is_step=False,
            quality="상",
        ),
    ]

    presenter = ListEdgesPydanticPresenter()
    presenter.present(output_data_list=output_data_list)

    assert presenter.get_view_model() == [
        EdgePydanticViewModel(
            nodes=(
                EdgeNodePydanticViewModel(id=1, name="A"),
                EdgeNodePydanticViewModel(id=2, name="B"),
            ),
            vertical_distance=1.0,
            horizontal_distance=2.0,
            is_stair=False,
            is_step=False,
            quality="상",
        ),
        EdgePydanticViewModel(
            nodes=(
                EdgeNodePydanticViewModel(id=1, name="A"),
                EdgeNodePydanticViewModel(id=3, name="C"),
            ),
            vertical_distance=3.0,
            horizontal_distance=4.0,
            is_stair=False,
            is_step=False,
            quality="상",
        ),
    ]
