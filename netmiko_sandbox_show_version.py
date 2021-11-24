#### DEVNET SANDBOX -- ALWAYS ON
import datetime
print ("Current date and time: ")
print(datetime.datetime.now())
print("Connecting via SSH => show version")
#
from netmiko import ConnectHandler
sshCli = ConnectHandler(
    device_type="cisco_ios",
    host="sandbox-iosxe-recomm-1.cisco.com",
    port="22",
    username="developer",
    password="C1sco12345"
    )
output=sshCli.send_command("show version")
print(output)