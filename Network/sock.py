#!/usr/bin/python


import socket



tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
 
tcpSocket.bind(("0.0.0.0", 8000))

tcpSocket.listen(2)

print "Waiting for client"

(client, (ip,port)) = tcpSocket.accept()

print "received connection from IP %s Port %d"%(ip,port))



client.send("Hello. Welcome")

data = "dummy"

while len(data) :

	data = client.recv(2048)
	print "Client sent: ", data
	client.sent(data)


print "Closing connection ..."
client.close()
