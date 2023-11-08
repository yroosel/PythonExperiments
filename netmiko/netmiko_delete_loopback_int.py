### ENABLE LOGGING MONITOR
from netmiko import ConnectHandler
IP_ADDRESS = "192.168.56.101" #"Get IP Address"
sshCli = ConnectHandler(
    device_type="cisco_ios",
    host=IP_ADDRESS,
    port="22",
    
    username="cisco",
    password="cisco123!"
    )
config_commands = (
    'no interface loopback 101' ,
    )
output=sshCli.send_command("show ip interface brief")
print(output)
output=sshCli.send_config_set(config_commands)
print(output)
output=sshCli.send_command("show ip interface brief")
print(output)
