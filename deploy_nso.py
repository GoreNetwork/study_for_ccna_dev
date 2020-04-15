import netmiko
from netmiko import SCPConn
from credentals import *


ubuntu_server = '192.168.0.116'
#You need the installer, use winzip or something like that to drill down till you reach it.
file = 'nso-5.3.linux.x86_64.installer.bin'
folder_name = file.split('.')[0]+'.'+file.split('.')[1]

commands = []
net_connect = netmiko.ConnectHandler(device_type='linux', ip=ubuntu_server , username=username, password=password)

def run_command_on_net_connect(net_connect,command):
	return net_connect.send_command_expect(command)


def transfer_file(net_connect,file):
	#net_connect.config_mode()
	#Assumes SCP server isn't already enabled
	net_connect.send_command('ip scp server enable')
	scp_conn = SCPConn(net_connect)
	#Source file
	s_file = file
	#Destination file
	d_file = file
	scp_conn.scp_transfer_file(s_file, d_file)
	#Takes SCP server back off the device
	net_connect.send_command('no ip scp server enable')
	net_connect.exit_config_mode()


transfer_file(net_connect,file)
#This configures NSO to start up, and start upon login

commands = [
"sh {} $HOME/{} --local-install".format(file, folder_name),
'source {}/ncsrc'.format (folder_name),
'echo source {}/ncsrc>start_nso.sh'.format (folder_name),
'ncs-setup --dest $HOME/ncs-run',
'cp -R {}/packages/neds ncs-run/packages'.format (folder_name),
'echo cd $HOME/ncs-run>>start_nso.sh',
'echo ncs>>start_nso.sh',
'echo bash start_nso.sh>>$HOME/.bashrc',
'bash start_nso.sh',
'ncs --status | grep status'
]

for command in commands:
	print (command)
	output = run_command_on_net_connect(net_connect,command)
	print (output)