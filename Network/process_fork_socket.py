#!/usr/bin/python

import socket
import os
import signal

def ConnectSocket(ip,port) :
	
	Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	Socket.bind((ip,int(port)))
	
	Socket.listen(1)

	return Socket


def child_process(user) :

	print "Client %d connection succeeded"%os.getpid()
	user.send("Hello.Welcome")

	data = user.recv(2048)

	print "Client %d sent:"%os.getpid(), data
	user.send(data)

	user.send("Closing Connection")
	print "Closing Connection with Client %d"%os.getpid()

	os.kill(os.getpid(), signal.SIGKILL)
        user.close()

def parent_process() :

	print "Starting Server"

	sock = ConnectSocket("0.0.0.0",8000)

	while True :
	
		(client, (ip,port)) = sock.accept()

		if client :

			childpid = os.fork()

			if childpid == 0:

				child_process(client)	

parent_process()
