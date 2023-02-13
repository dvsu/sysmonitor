from dataclasses import dataclass


@dataclass
class Measurement:
    name: str
    unit: str
    value: float
