from typing import Optional
from dataclasses import dataclass


@dataclass
class Measurement:
    name: str
    unit: str
    value: float


@dataclass
class SystemMeasurement:
    measurements: list[Measurement]


@dataclass
class SystemData:
    cpu: Optional[SystemMeasurement]
    memory: Optional[SystemMeasurement]
    storage: Optional[SystemMeasurement]
    timestamp: str
