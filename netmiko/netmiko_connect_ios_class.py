# FSM
# pip3 install netmiko ntc-templates
# export NET_TEXTFSM=$(python3 -c "import ntc_templates; print(ntc_templates.__path__[0] + '/templates')")
import netmiko
v_host = '192.168.56.101'
v_user = 'cisco'
v_pass = 'cisco123!'

class Cisco:

    def __init__(self, ip, device_type=None, username=None, password=None):

       self.conn_data = {
           'ip': ip,
           'device_type': device_type,
           'username': username,
           'password': password
       }

    def login(self):

        return netmiko.ConnectHandler(**self.conn_data)

class CiscoIOS(Cisco):

    def __init__(self, ip, username=None, password=None):

        super().__init__(ip, device_type='cisco_ios', username=username, password=password)

    def populate_interface_list(self):

        conn = self.login()
        sh_ip_int_br = conn.send_command('sh ip int br', use_textfsm=True)
        self.interface_list = []
        for interface in sh_ip_int_br:
            self.interface_list.append(interface['interface'])

csr1kv1 = CiscoIOS(v_host, username=v_user, password=v_pass)
csr1kv1.populate_interface_list()
print(csr1kv1.interface_list)
