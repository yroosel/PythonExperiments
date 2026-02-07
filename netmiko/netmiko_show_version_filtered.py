import datetime
print ("Current date and time: ")
print(datetime.datetime.now())
print("Connecting via SSH => show version")
#
from netmiko import ConnectHandler
### VAR

### EXEC
sshCli = ConnectHandler(
    device_type="cisco_ios",
    host="192.168.56.101",
    port="22",
    username="cisco",
    password="cisco123!"
    )
output=sshCli.send_command("show version")
for line in output.splitlines():
    if 'Cisco IOS Software' in line:
        ios_version = line.strip()
    elif 'uptime' in line:
        hostname = line.split()[0]
        sys_uptime = line 
    elif 'Configuration register' in line:
        confreg = line.split()[3]
    elif 'interface' in line:
        num_interfaces = line.split()[0]
print("IOS Version")
print(ios_version)
print("Hostname: ", hostname)
print("System uptime: ", sys_uptime)
print("Configuration register: ", confreg)
print("Number of Interfaces: ", num_interfaces)


