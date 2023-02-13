from typing import Optional
from dataclasses import dataclass
from src.models.system_measurement import SystemMeasurement


@dataclass
class SystemData:
    cpu: Optional[SystemMeasurement]
    memory: Optional[SystemMeasurement]
    storage: Optional[SystemMeasurement]
