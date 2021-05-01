import psutil


class SysMonitor:

    def __init__(self):
        self.__data = {}
    
    def get_system_stats(self):
        sensor_temp = psutil.sensors_temperatures()
        print(sensor_temp.keys())
        for thermal_data in sensor_temp['cpu_thermal']:
            cpu_temp = round(thermal_data.current, 2)
            
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        self.__data = {
            "cpu_temp": cpu_temp,
            "cpu_temp_unit": "C",
            "cpu_usage": round(psutil.cpu_percent(), 2),
            "cpu_usage_unit": "%",
            "ram_total": round(ram.total / 10**9, 3),
            "ram_available": round(ram.available / 10**9, 3), 
            "ram_used": round(ram.used / 10**9, 3),
            "ram_unit": "GB",
            "disk_total": round(disk.total / 10**9, 3), 
            "disk_free": round(disk.used / 10**9, 3), 
            "disk_used": round(disk.free / 10**9, 3),
            "disk_unit": "GB"
        }

        return self.__data
