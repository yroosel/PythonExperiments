# netmiko_show_version.py
import datetime
print ("Current date and time: ")
print(datetime.datetime.now())
print("Connecting via SSH => show version")
from netmiko import ConnectHandler
sshCli = ConnectHandler(
    device_type="cisco_ios",
    host="192.168.56.xxx",
    port="22",
    username="Get username",
    password="Get password"
    )
output=sshCli.send_command("show version")
print(output)
