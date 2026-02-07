print("Connecting via SSH => show interface status (brief)")
from netmiko import ConnectHandler
sshCli = ConnectHandler(
    device_type="cisco_ios",
    host="192.168.56.xxx",
    port="22",
    username="Get username",
    password="Get password"
    )
output=sshCli.send_command("show ip interface brief")
print(output)
