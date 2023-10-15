from decimal import Decimal
from unittest import mock

import pytest

from map_admin.application.boundaries import ListEdgesOutputBoundary
from map_admin.application.dtos import ListEdgesOutputData
from map_admin.application.repositories import NodeRepository
from map_admin.application.use_cases import ListEdgesUseCase
from map_admin.domain.entities import Edge, Node
from map_admin.domain.value_objects import Point, RoadQuality


@pytest.fixture()
def mock_node_repo() -> mock.Mock:
    mock_node_repo: mock.Mock = mock.Mock(spec_set=NodeRepository)
    mock_node_repo.get_all_nodes.return_value = [
        Node(
            id=1,
            name="A",
            point=Point(longitude=Decimal("1.0"), latitude=Decimal("2.0")),
            edges=[
                Edge(
                    node_ids=(1, 2),
                    vertical_distance=Decimal("1.0"),
                    horizontal_distance=Decimal("2.0"),
                    is_stair=False,
                    is_step=False,
                    quality=RoadQuality.HIGH,
                ),
            ],
        ),
        Node(
            id=2,
            name="B",
            point=Point(longitude=Decimal("3.0"), latitude=Decimal("4.0")),
            edges=[
                Edge(
                    node_ids=(2, 1),
                    vertical_distance=Decimal("1.0"),
                    horizontal_distance=Decimal("2.0"),
                    is_stair=False,
                    is_step=False,
                    quality=RoadQuality.HIGH,
                ),
            ],
        ),
        Node(
            id=3,
            name="C",
            point=Point(longitude=Decimal("5.0"), latitude=Decimal("6.0")),
        ),
    ]
    return mock_node_repo


@pytest.fixture()
def mock_list_edges_presenter() -> mock.Mock:
    return mock.Mock(spec_set=ListEdgesOutputBoundary)


def test_list_edges(
    mock_node_repo: mock.Mock,
    mock_list_edges_presenter: mock.Mock,
) -> None:
    ListEdgesUseCase(
        node_repo=mock_node_repo,
    ).execute(
        output_boundary=mock_list_edges_presenter,
    )

    assert mock_node_repo.get_all_nodes.called
    assert mock_list_edges_presenter.present.call_args_list == [
        mock.call(
            output_data_list=[
                ListEdgesOutputData(
                    nodes=(
                        ListEdgesOutputData.Node(id=1, name="A"),
                        ListEdgesOutputData.Node(id=2, name="B"),
                    ),
                    vertical_distance=Decimal("1.0"),
                    horizontal_distance=Decimal("2.0"),
                    is_stair=False,
                    is_step=False,
                    quality=RoadQuality.HIGH.value,
                ),
            ],
        ),
    ]
