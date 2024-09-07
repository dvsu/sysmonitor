from sysmonitor import SysMonitor

monitor = SysMonitor()

print(monitor.system_stats().model_dump_json(indent=2))
