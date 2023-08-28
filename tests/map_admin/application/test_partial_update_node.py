from decimal import Decimal
from unittest import mock

import pytest

from map_admin.application.boundaries import PartialUpdateNodeInputBoundary
from map_admin.application.dtos import PartialUpdateNodeInputData
from map_admin.application.repositories import NodeRepository
from map_admin.application.use_cases import PartialUpdateNodeUseCase
from map_admin.domain.entities import Node
from map_admin.domain.value_objects import Point


@pytest.mark.parametrize(
    "name, expected_name",
    [("A updated", "A updated"), (None, "A")],
)
@pytest.mark.parametrize(
    "longitude, expected_longitude",
    [(Decimal("5.0"), Decimal("5.0")), (None, Decimal("1.0"))],
)
@pytest.mark.parametrize(
    "latitude, expected_latitude",
    [(Decimal("6.0"), Decimal("6.0")), (None, Decimal("2.0"))],
)
def test_partial_update_node(
    name: str | None,
    longitude: Decimal | None,
    latitude: Decimal | None,
    expected_name: str,
    expected_longitude: Decimal,
    expected_latitude: Decimal,
) -> None:
    mock_node_repo = mock.Mock(spec_set=NodeRepository)
    mock_node_repo.get_node_by_id.return_value = Node(
        id=1,
        name="A",
        point=Point(
            longitude=Decimal("1.0"),
            latitude=Decimal("2.0"),
        ),
    )

    PartialUpdateNodeUseCase(
        node_repo=mock_node_repo,
    ).execute(
        input_data=PartialUpdateNodeInputData(
            id=1,
            name=name,
            longitude=longitude,
            latitude=latitude,
        ),
    )

    assert mock_node_repo.update_node.call_args_list == [
        mock.call(
            node=Node(
                id=1,
                name=expected_name,
                point=Point(
                    longitude=expected_longitude,
                    latitude=expected_latitude,
                ),
            ),
        ),
    ]


def test_partial_update_node_with_invalid_id() -> None:
    mock_node_repo = mock.Mock(spec_set=NodeRepository)
    mock_node_repo.get_node_by_id.side_effect = [NodeRepository.NodeNotFoundError]

    with pytest.raises(PartialUpdateNodeInputBoundary.NodeNotFoundError):
        PartialUpdateNodeUseCase(
            node_repo=mock_node_repo,
        ).execute(
            input_data=PartialUpdateNodeInputData(
                id=1,
                name="A updated",
                longitude=Decimal("5.0"),
                latitude=Decimal("6.0"),
            ),
        )

    assert not mock_node_repo.update_node.called
