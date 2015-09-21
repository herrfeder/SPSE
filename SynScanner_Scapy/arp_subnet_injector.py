
from scapy.all import *


for lsb in range(1,255):
	ip = "192.168.1." + str(lsb)
	arpRequest = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip, hwdst="ff:ff:ff:ff:ff:ff")
	arpResponse = srp1(arpRequest, verbose=1)
	if arpResponse:
		print "IP: " + arpResponse.psrc + "MAC: " + arpResponse.hwsrc


