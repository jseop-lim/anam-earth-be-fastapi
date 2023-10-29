from decimal import Decimal

from map_admin.application.dtos import CreateNodeOutputData, ListNodesOutputData
from map_admin.presentation.presenters import (
    CreateNodePydanticPresenter,
    CreateNodePydanticViewModel,
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
