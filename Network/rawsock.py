#!/usr/bin/python

import socket
import struct
import binascii

while True :

	rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0800)) 


	packet = rawSocket.recvfrom(2048)

	ethernetHeader = packet[0][0:14]

	eth_hdr = struct.unpack("!6s6s2s", ethernetHeader)


	binascii.hexlify(eth_hdr[0])

	ethDHost = binascii.hexlify(eth_hdr[0])
	ethSHost = binascii.hexlify(eth_hdr[1])
	ethType =  binascii.hexlify(eth_hdr[2])

	ipHeader = packet[0][14:34]

	ip_hdr = struct.unpack("!12s4s4s", ipHeader)

	tcpHeader = packet[0][34:54]

	tcp_hdr = struct.unpack("!HHII2sH2sH", tcpHeader)

	tcp_sourceport = str(tcp_hdr[0])

	tcp_destinationport = str(tcp_hdr[1])

	tcp_sequencenumber = str(tcp_hdr[2])

	tcp_data = str(tcp_hdr[5])

		
	#if int(tcp_sourceport) == 443:	
	print "EthernetDHost : " +"\t"+ ethDHost   
	print "EthernetSHost : " +"\t"+ ethSHost 

	print "Source IP address : " +"\t"+ socket.inet_ntoa(ip_hdr[1]) 
	print "Dest IP address : " +"\t"+ socket.inet_ntoa(ip_hdr[2]) 

	print "TCP_Sourceport : " +"\t"+ tcp_sourceport
	print "TCP_Destinationport : " +"\t"+ tcp_destinationport
	print "TCP_Secquencenumber : " +"\t"+ tcp_sequencenumber
	print "TCP_Data       : " +"\t"+ tcp_data + "\n"






