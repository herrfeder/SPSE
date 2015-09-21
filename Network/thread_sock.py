#!/usr/bin/python

import socket
import thread
import time

def client_handler(user,id) :

	print "Client %d connection succeeded"%id
	user.send("Hello. Welcome")

	data = user.recv(2048)
	print "Client %d sent:"%id, data
	user.send(data)

	user.send("Closing Connection")
	user.close()

tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

tcpSocket.bind(("0.0.0.0",8000))

tcpSocket.listen(2)
i = 0
print "Waiting for client"

while True:

	(client, (ip,port)) = tcpSocket.accept()

	if client :
		thread.start_new_thread(client_handler, (client,i))
		i += 1
			
