print("Connecting via SSH => show interface status (brief)")
from netmiko import ConnectHandler
sshCli = ConnectHandler(
    device_type="cisco_ios",
    host="192.168.56.101",
    port="22",
    username="cisco",
    password="cisco123!"
    )
output=sshCli.send_command("show ip interface brief")
print(output)
