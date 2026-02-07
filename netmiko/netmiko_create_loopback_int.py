from netmiko import ConnectHandler

# variables
HOST="192.168.56.xxx"; USER="Get Username"; PASS="Get Password"; PORT=22; DEV="cisco_ios"
INTF="loopback 111"; IP="10.11.111.1"; MASK="255.255.255.255"
SHOW="show ip interface brief"; CMDS=[f"int {INTF}", f"ip address {IP} {MASK}"]

ssh=ConnectHandler(device_type=DEV, host=HOST, port=PORT, username=USER, password=PASS)

print("BEFORE"); print(ssh.send_command(SHOW))
ssh.send_config_set(CMDS)
print("AFTER"); print(ssh.send_command(SHOW))

ssh.disconnect()
