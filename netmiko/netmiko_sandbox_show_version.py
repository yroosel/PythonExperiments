#### DEVNET SANDBOX -- ALWAYS ON
import datetime
print ("Current date and time: ")
print(datetime.datetime.now())
print("Connecting via SSH => show version")
#
from netmiko import ConnectHandler
### VAR
RTR="sandbox-iosxe-recomm-1.cisco.com"
SSH_PORT="22"
USER="Your User" 
PW="Your Pass"
### EXEC
sshCli = ConnectHandler(
    device_type="cisco_ios",
    host=RTR,
    port=SSH_PORT,
    username=USER,
    password=PW
    )
output=sshCli.send_command("show version")
print(output)
