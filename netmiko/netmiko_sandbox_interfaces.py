#### DEVNET SANDBOX -- ALWAYS ON -- CHECK THE URL AND CONNECTION PARAMETERS ON developer.cisco.com
import datetime
print ("Current date and time: ")
print(datetime.datetime.now())
print("Connecting via SSH => show interface status (brief)")
#
from netmiko import ConnectHandler
### VAR
RTR="sandbox-iosxe-latest-1.cisco.com" #"sandbox-iosxe-recomm-1.cisco.com"
SSH_PORT="22"
USER="developer" 
PW="C1sco12345"
### EXEC
sshCli = ConnectHandler(
    device_type="cisco_ios",
    host=RTR,
    port=SSH_PORT,
    username=USER,
    password=PW
    )
output=sshCli.send_command("show ip interface brief")
print(output)
