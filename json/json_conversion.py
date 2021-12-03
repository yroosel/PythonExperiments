### JSON CONVERSION EXERCISE ###

import json
import yaml
import datetime
print ("Current date and time: ")
print(datetime.datetime.now())

dc_container = """
{
 "rack": [
      { "server": { "dev_id": "SRV1" , "server_name": "svr-1" , "domain": "biasc.be", "ip-address": "10.2.3.1" ,
                     "os": "linux"  , "server_type": "vm" ,
                     "services": [   
                       {"service": "AD" , "service_type": "vm", "protocol": "tcp", "port": "389"},
                       {"service": "DNS", "service_type": "vm", "protocol": "udp", "port": "53"},
                       {"service": "NTP", "service_type": "vm", "protocol": "udp", "port": "123"} 
                    ]
                  }
      },
      { "server": { "dev_id": "SRV2" , "server_name": "svr-2" , "domain": "biasc.be", "ip-address": "10.2.3.2" ,
                    "os": "linux"  , "server_type": "vm" ,
                    "services": [   
                      {"service": "FLASK", "service_type": "vm", "protocol": "tcp", "port": "8089"  }, 
                      {"service": "DB"   , "service_type": "vm", "protocol": "tcp", "port": "1521"  } 
                    ]     
                 }
      },
      { "server": { "dev_id": "SRV3" , "server_name": "svr-3" ,  "domain": "biasc.be" , "ip-address": "10.2.3.3",
                    "os": "linux"  , "server_type": "vm" ,
                    "services": [   
                      {"service": "DNS" , "service_type": "vm", "protocol": "tcp", "port": "8089" }, 
                      {"service": "NTP" , "service_type": "vm", "protocol": "udp", "port": "123" },
                      {"service": "DHCP", "service_type": "docker", "protocol": "udp", "port": "67" }
                    ] 
                  }
      }
   ]
}
"""
print('------1---------')
print(type(dc_container))
#print(dc_container)
print('------2---------')
v1 = json.loads(dc_container)   ### loads: str => dict (tree)
print(type(v1))
print('------3---------')
v2 = json.dumps(v1)             ### dumps: dict => str
print(type(v2))
print('------4---------')
v3 = yaml.dump(v1)              ### dump: dict => yaml (tree)
#print(v3)
#print(dir(yaml))
### filteren kan enkel in een dict
print('------5---------')       ### using index for a list - using keys() for a dict
v4 = v1["rack"][0]
print(type(v4))
print(v4["server"]["services"][0].keys())
print('------5---------')       ### loop through list
for v5 in v1["rack"]:
    print('------5A--------')
    print(type(v5))
    #print(v5)
    #print(v5["server"]["services"][0]["service"])
    print(v5["server"]["os"])
    for v6 in v5["server"]["services"]:
        print(v6["service"], v6["port"])
print('------5---------')
print(v5["server"]["services"][0].keys())
