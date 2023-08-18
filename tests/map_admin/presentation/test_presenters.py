from decimal import Decimal

from map_admin.application.dtos import ListNodesOutputData
from map_admin.presentation.presenters import (
    ListNodesPydanticPresenter,
    NodePydanticViewModel,
)


class TestListNodesPydanticPresneter:
    def test_present(self) -> None:
        output_data_list: list[ListNodesOutputData] = [
            ListNodesOutputData(
                name="Node 1",
                longitude=Decimal("1.0"),
                latitude=Decimal("2.0"),
            ),
            ListNodesOutputData(
                name="Node 2",
                longitude=Decimal("3.0"),
                latitude=Decimal("4.0"),
            ),
        ]

        presenter = ListNodesPydanticPresenter()
        presenter.present(output_data_list=output_data_list)

        assert presenter.get_view_model() == [
            NodePydanticViewModel(
                name="Node 1",
                longitude=1.0,
                latitude=2.0,
            ),
            NodePydanticViewModel(
                name="Node 2",
                longitude=3.0,
                latitude=4.0,
            ),
        ]
