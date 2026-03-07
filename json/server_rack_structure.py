import json

server_rack = {
 "rack": [
      { "server": { "dev_id": "S10" , "server_name": "svr1" , "domain": "biasc.be", "ip-address": "10.2.3.11" ,
                     "os": "linux"  , "server_type": "vm" ,
                     "services": [   
                       {"service": "ad" , "service_type": "vm", "protocol": "tcp", "port": "389"},
                       {"service": "dns", "service_type": "vm", "protocol": "udp", "port": "53"},
                       {"service": "ntp", "service_type": "vm", "protocol": "udp", "port": "123"} 
                    ]
                  }
      },
      { "server": { "dev_id": "S20" , "server_name": "svr2" , "domain": "biasc.be", "ip-address": "10.2.3.12" ,
                    "os": "linux"  , "server_type": "vm" ,
                    "services": [   
                      {"service": "flask", "service_type": "vm", "protocol": "tcp", "port": "8089"  }, 
                      {"service": "db"   , "service_type": "vm", "protocol": "tcp", "port": "1521"  } 
                    ]     
                 }
      },
      { "server": { "dev_id": "S30" , "server_name": "svr3" ,  "domain": "biasc.be" , "ip-address": "10.2.3.13",
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

print(type(server_rack))
print(server_rack)
