#!/usr/bin/python

from scapy.all import *
import sys, getopt, netifaces, os

bssidList = []
directory = "/home/herrfeder/Dokumente/Programmierung/SPSE-Course-DVD/Python/WiFi_Sniff/SSIDFile.txt"

def usage():
	print "Usage: sudo ./wifiSniffer.py <interface>"


def sniffSSID(pkt):
	global bssidList
	if pkt.haslayer(Dot11Beacon):
		if pkt.addr2 not in bssidList:
			string = pkt.sprintf("%Dot11.addr2%\t%Dot11Beacon.info%\t%Dot11Beacon.cap%")
			print string
			bssidList.append(pkt.addr3)
			SSIDFile(pkt,string)

	elif pkt.haslayer(Dot11ProbeResp):
		if pkt.addr2 not in bssidList:
			string = pkt.sprintf("%Dot11.addr2%\t%Dot11ProbeResp.info%\t%Dot11ProbeResp.cap%")
			print string
			bssidList.append(pkt.addr3)
			SSIDFile(pkt,string)



def SSIDFile(pkt,string):
	
	string = string + "\n"	
#	if os.path.exists(directory):
	try:
		if os.stat(directory).st_size == 0:
			fdesc = open(directory,"w")
			fdesc.write(string)
			fdesc.close()
		else:
			fdesc = open(directory,"r+")
			buff = fdesc.read()
			SSID_List = buff.split("\n")

			for item in SSID_List:
				ap_buff = item.split("\t")
				if ap_buff[0] != pkt.addr2:
					pass
				else:
				   fdesc.close()
				   return
			
			fdesc.write(string)
			fdesc.close()

	except OSError:
		
		fdesc = file(directory,"w")
		fdesc.write(string)
		fdesc.close()


def main(argv):
	
	try:
		opts, args = getopt.getopt(argv, "h")
	except 	getopt.GetoptError:
		usage()
		sys.exit(2)
	
	for opt, arg in opts:
		if opt in ("-h"):
			usage()
			sys.exit()

	if (len(args) > 0) and (args[0] in netifaces.interfaces()):
		sniff(iface=args[0], prn=sniffSSID, store=0)
	else:
		print "Interface not specified or wrong"

if __name__ == "__main__" :
	main(sys.argv[1:])
