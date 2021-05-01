import psutil


class SysMonitor:

    def __init__(self):
        self.__data = {
            "sensors": {},
            "cpu": {},
            "ram": {},
            "disk": {}
        }
    
    def get_system_stats(self):

        for hw_temp, temp_points in psutil.sensors_temperatures().items():
            self.__data["sensors"][hw_temp] = {}
            for temp in temp_points:
                temp_name = temp.label.replace(' ','_').lower() if temp.label else "temp"
                self.__data["sensors"][hw_temp][temp_name] = round(temp.current, 2)
        
            self.__data["sensors"][hw_temp]["unit"] = "C"

        cpu_usage = psutil.cpu_percent(interval=1, percpu=True)

        self.__data["cpu"]["usage"] = {f"cpu_{count}": round(usage, 2) for count, usage in enumerate(cpu_usage)}
        self.__data["cpu"]["usage"]["unit"] = "%"

        ram = psutil.virtual_memory()

        self.__data["ram"]["virtual"] = {
            "total": round(ram.total / 10**9, 3),
            "available": round(ram.available / 10**9, 3), 
            "used": round(ram.used / 10**9, 3),
            "unit": "GB"
        }

        disk = psutil.disk_usage('/')

        self.__data["disk"]["usage"] = {
            "total": round(disk.total / 10**9, 3), 
            "free": round(disk.used / 10**9, 3), 
            "used": round(disk.free / 10**9, 3),
            "unit": "GB" 
        }

        return self.__data
