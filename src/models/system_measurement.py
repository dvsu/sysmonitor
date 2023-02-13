from dataclasses import dataclass
from src.models.measurement import Measurement


@dataclass
class SystemMeasurement:
    measurement: list[Measurement]
