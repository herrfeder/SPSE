import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

import scapy
from scapy.all import *

sniff(iface="mon0", prn=lambda p: p.getlayer(Raw))
