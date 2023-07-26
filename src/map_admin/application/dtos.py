from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, kw_only=True)
class ListNodesOutputData:
    name: str
    longitude: Decimal
    latitude: Decimal


@dataclass(frozen=True, kw_only=True)
class CreateNodeInputData:
    name: str
    longitude: Decimal
    latitude: Decimal
