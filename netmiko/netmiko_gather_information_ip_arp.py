# FSM
# pip3 install netmiko ntc-templates
# export NET_TEXTFSM=$(python3 -c "import ntc_templates; print(ntc_templates.__path__[0] + '/templates')")

from netmiko import ConnectHandler
                     
def get_router_output(ip, username=None, password=None, port=22,
                      device_type=None, command=None, use_textfsm=True):                  

    conn = ConnectHandler( 
        ip, 
        username=username,
        password=password, 
        port=port,
        device_type=device_type
    ) 
    return conn.send_command(command, use_textfsm=True)

sh_ip_arp = get_router_output( 
    '192.168.56.101', 
    username='cisco', 
    password='cisco123!', 
    device_type='cisco_ios', 
    command='show ip arp' 
)

ip_arp = sh_ip_arp
print(ip_arp) 

first = ip_arp[0]
print("-" * 50) 
print('First Interface: ', first['interface'])
print('First IP: ', first['ip_address'])
print('First MAC: ', first['mac_address'])
print("-" * 50) 





