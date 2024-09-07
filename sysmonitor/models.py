from pydantic import BaseModel


class HardwareMeasurement(BaseModel):
    name: str
    unit: str
    value: float


class Hardware(BaseModel):
    measurements: list[HardwareMeasurement]


class DeviceStats(BaseModel):
    cpu: Hardware | None = None
    memory: Hardware | None = None
    storage: Hardware | None = None
    datetime_utc: str
    timestamp_nanosec: int
