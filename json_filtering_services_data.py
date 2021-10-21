### JSON FILTERING -- SERVICES DATA ###

import json

devices_struc = {
 "rack": [
      { "server": { "dev_id": "S1" , "server_name": "svr1" , "domain": "biasc.be", "ip-address": "10.2.3.1" ,
                     "os": "linux"  , "server_type": "vm" ,
                     "services": [   
                       {"service": "ad" , "service_type": "vm", "protocol": "tcp", "port": "389"},
                       {"service": "dns", "service_type": "vm", "protocol": "udp", "port": "53"},
                       {"service": "ntp", "service_type": "vm", "protocol": "udp", "port": "123"} 
                    ]
                  }
      },
      { "server": { "dev_id": "S2" , "server_name": "svr2" , "domain": "biasc.be", "ip-address": "10.2.3.2" ,
                    "os": "linux"  , "server_type": "vm" ,
                    "services": [   
                      {"service": "flask", "service_type": "vm", "protocol": "tcp", "port": "8089"  }, 
                      {"service": "db"   , "service_type": "vm", "protocol": "tcp", "port": "1521"  } 
                    ]     
                 }
      },
      { "server": { "dev_id": "S3" , "server_name": "svr3" ,  "domain": "biasc.be" , "ip-address": "10.2.3.3",
                    "os": "linux"  , "server_type": "vm" ,
                    "services": [   
                      {"service": "dns" , "service_type": "vm", "protocol": "tcp", "port": "8089" }, 
                      {"service": "ntp" , "service_type": "vm", "protocol": "udp", "port": "123" },
                      {"service": "dhcp", "service_type": "docker", "protocol": "udp", "port": "67" }
                    ] 
                  }
      }
   ]
}

print('------1---------')
print(type(devices_struc))
print(devices_struc)
print('------1A--------')
js_groups = json.dumps(devices_struc)
print(type(js_groups))
print(js_groups)
print('------1B--------')
print(json.dumps(devices_struc, indent=2))

print('------2---------')
for g in devices_struc["rack"]:
    print('------2A--------')
    print(type(g))
    print(g)
    print(g["server"]["services"])
    for p in g["server"]["services"]:
        print(p)
            
print('------3---------')
print(devices_struc.keys())
print('------3A---------')
print(devices_struc["rack"][0].keys())
print('------3B---------')
print(devices_struc["rack"][0]["server"].keys())
print('------3C---------')
print(devices_struc["rack"][0]["server"]["services"][0].keys())
