# show platform info
import json, psutil, platform
print(json.dumps({
  "cpu":{
    "platform":platform.platform(),
    "processor":platform.processor(),
    "physical_cores":psutil.cpu_count(False),
    "logical_processors":psutil.cpu_count(True)
  },
  "memory":psutil.virtual_memory()._asdict()
}, indent=2))
