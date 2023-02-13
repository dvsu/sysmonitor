import psutil
from dataclasses import asdict
from sysmonitor.dependencies.models import SystemData, SystemMeasurement, Measurement


class SysMonitor:

    def cpu_stats(self) -> SystemMeasurement:
        cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
        cpu_thermal = psutil.sensors_temperatures().get("cpu_thermal")

        sensor_measurements = []
        if cpu_thermal and len(cpu_thermal) > 0:
            sensor_measurements = [Measurement(
                name=f"cpu_thermal{temp.label}", unit="c", value=temp.current)
                for temp in cpu_thermal]

        return SystemMeasurement(measurement=[
            Measurement(name=f"cpu_{count}_load", unit="%", value=round(usage, 2))
            for count, usage in enumerate(cpu_usage)] + sensor_measurements)

    def ram_stats(self) -> SystemMeasurement:
        ram = psutil.virtual_memory()
        return SystemMeasurement(measurement=[
            Measurement(name="memory_total", unit="GB", value=round(ram.total / 10**9, 3)),
            Measurement(name="memory_available", unit="GB", value=round(ram.available / 10**9, 3)),
            Measurement(name="memory_used", unit="GB", value=round(ram.used / 10**9, 3)),
            Measurement(name="memory_percent", unit="%", value=round(ram.percent, 2))
        ])

    def disk_stats(self) -> dict:
        disk = psutil.disk_usage('/')
        return SystemMeasurement(measurement=[
            Measurement(name="storage_total", unit="GB", value=round(disk.total / 10**9, 3)),
            Measurement(name="storage_free", unit="GB", value=round(disk.free / 10**9, 3)),
            Measurement(name="storage_used", unit="GB", value=round(disk.used / 10**9, 3)),
            Measurement(name="storage_percent", unit="%", value=round(disk.percent, 2))
        ])

    def system_stats(self, as_dict: bool = False) -> SystemData:
        data = SystemData(cpu=self.cpu_stats(),
                          memory=self.ram_stats(),
                          storage=self.disk_stats())

        if as_dict == True:
            return asdict(data)

        return data
