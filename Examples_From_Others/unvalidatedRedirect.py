import argparse
import re
from scapy.all import *


def httpCapture(packet):
    """
    This is used to capture HTTP GET requests made to google.com... Useful for detecting an unvalidated redirect
    """
    if packet.haslayer(Raw):
        rawPacket = packet.getlayer(Raw).load
        line = rawPacket.split("\line\n")           # store array of lines in packet
        
        if "GET / HTTP/1.1\r\nHost: www.google.com" in line[0]:    # only search login page
            print "redirect to google detected"
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("iface")    # positional agrument
    args = parser.parse_args()
    
    # sniff HTTP traffic
    pkts = sniff(iface=args.iface, filter="tcp port 80", prn=httpCapture)