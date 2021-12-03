### ENABLE LOGGING MONITOR
from netmiko import ConnectHandler
IP_ADDRESS = "Get IP Address"
sshCli = ConnectHandler(
    device_type="cisco_ios",
    host=IP_ADDRESS,
    port="22",
    username="Get Username",
    password="Get Password"
    )
config_commands = (
    'logging monitor' ,
    )
output=sshCli.send_config_set(config_commands)
output=sshCli.send_command("show logging")
print(output)