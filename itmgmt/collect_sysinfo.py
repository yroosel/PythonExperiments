#collect_sysinfo.py
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
        "cpu_freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
        "cpu_percent_total": psutil.cpu_percent(interval=0.1),
        "cpu_percent_per_cpu": psutil.cpu_percent(interval=0.1, percpu=True),
    }

    # Memory info
    data["memory"] = psutil.virtual_memory()._asdict()
    data["swap"] = psutil.swap_memory()._asdict()

    # Storage info (alle partities)
    storage = {}
    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
            storage[part.mountpoint] = {
                "device": part.device,
                "fstype": part.fstype,
                "opts": part.opts,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent,
            }
        except PermissionError:
            continue
    data["storage"] = storage

    # Network info
    net = {}
    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    io = psutil.net_io_counters(pernic=True)
    for iface, addr_list in addrs.items():
        net[iface] = {
            "addrs": [a._asdict() for a in addr_list],
            "stats": stats[iface]._asdict() if iface in stats else None,
            "io": io[iface]._asdict() if iface in io else None,
        }

    data["network"] = {
        "hostname": socket.gethostname(),
        "fqdn": socket.getfqdn(),
        "interfaces": net,
    }

    return data


if __name__ == "__main__":
    info = collect_system_info()
    # JSON output
    print(json.dumps(info, indent=2))

