from scapy.all import *

netface = "lo"

def printHttpData(pkt):

	httpLoad = pkt.sprintf("%Raw.load%")
	print pkt.summary()
	if httpLoad.startswith("'GET") or httpLoad.startswith("'POST"):
		httpData = httpLoad.split("\\r\\n")
	
		print "GET/POST data: ", httpData[0]
		del httpData[0]
		for item in httpData:
			print item
	elif httpLoad.startswith("'HTTP"):
		httpData = httpLoad.split("\\r\\n")
		del httpData[0]
		for item in httpData:
			print item

	print "-------------------------------------------------------------"

sniff(iface=netface,prn=printHttpData)

