import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

import scapy
from scapy.all import *
sniff(iface="lo", store=0, count=100, 
        lfilter=lambda p: p if p.haslayer(TCP) and p.haslayer(Raw) else False,
        prn=lambda p: p.getlayer(Raw))
