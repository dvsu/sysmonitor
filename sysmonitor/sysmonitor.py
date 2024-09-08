from datetime import datetime, timezone

import psutil

from .models import DeviceStats, Hardware, HardwareMeasurement


class SysMonitor:
    def cpu_stats(self) -> Hardware:
        cpu_usage = psutil.cpu_percent(interval=1, percpu=True)

        return Hardware(
            measurements=[
                HardwareMeasurement(name=f"cpu_{count}_load", unit="%", value=round(usage, 2))
                for count, usage in enumerate(cpu_usage)
            ]
        )

    def ram_stats(self) -> Hardware:
        ram = psutil.virtual_memory()
        return Hardware(
            measurements=[
                HardwareMeasurement(
                    name="memory_total", unit="GB", value=round(ram.total / 10**9, 3)
                ),
                HardwareMeasurement(
                    name="memory_available", unit="GB", value=round(ram.available / 10**9, 3)
                ),
                HardwareMeasurement(
                    name="memory_used", unit="GB", value=round(ram.used / 10**9, 3)
                ),
                HardwareMeasurement(name="memory_percent", unit="%", value=round(ram.percent, 2)),
            ]
        )

    def disk_stats(self) -> Hardware:
        disk = psutil.disk_usage("/")
        return Hardware(
            measurements=[
                HardwareMeasurement(
                    name="storage_total", unit="GB", value=round(disk.total / 10**9, 3)
                ),
                HardwareMeasurement(
                    name="storage_free", unit="GB", value=round(disk.free / 10**9, 3)
                ),
                HardwareMeasurement(
                    name="storage_used", unit="GB", value=round(disk.used / 10**9, 3)
                ),
                HardwareMeasurement(name="storage_percent", unit="%", value=round(disk.percent, 2)),
            ]
        )

    def sensors_stats(self) -> Hardware:
        sensors_temperatures = psutil.sensors_temperatures()

        measurements: list[HardwareMeasurement] = []

        for device, sensors in sensors_temperatures.items():
            for sensor in sensors:
                if sensor.current > 0:
                    sensor_label = device

                    if sensor.label:
                        sensor_label += f"_{sensor.label.replace(' ', '_')}"

                    measurements.append(
                        HardwareMeasurement(
                            name=sensor_label,
                            unit="C",
                            value=sensor.current,
                        )
                    )

        return Hardware(measurements=measurements)

    def system_stats(self) -> DeviceStats:
        datetime_now = datetime.now(timezone.utc)

        utc_string = datetime_now.strftime("%Y-%m-%dT%H:%M:%SZ")

        timestamp_nanosec = int(datetime.timestamp(datetime_now) * 10**9)

        return DeviceStats(
            cpu=self.cpu_stats(),
            memory=self.ram_stats(),
            storage=self.disk_stats(),
            sensors=self.sensors_stats(),
            datetime_utc=utc_string,
            timestamp_nanosec=timestamp_nanosec,
        )
