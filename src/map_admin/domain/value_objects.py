from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum


@dataclass(frozen=True, kw_only=True)
class Point:
    longitude: Decimal
    latitude: Decimal


class RoadQuality(StrEnum):
    HIGH = "상"
    MEDIUM = "중"
    LOW = "하"
