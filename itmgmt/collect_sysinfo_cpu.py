#collect_sysinfo_cpu_mem.py
import json
import psutil
import platform
import socket


def collect_system_info():
    data = {}

    # CPU info
    data["cpu"] = {
        "platform": platform.platform(),
        "processor": platform.processor(),
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_processors": psutil.cpu_count(logical=True),
    }


    return data

if __name__ == "__main__":
    info = collect_system_info()
    # JSON output
    print(json.dumps(info, indent=2))