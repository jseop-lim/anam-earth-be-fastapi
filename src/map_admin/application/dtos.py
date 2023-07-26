from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ListNodesOutputData:
    name: str
    longitude: Decimal
    latitude: Decimal
