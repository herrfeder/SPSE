#!/usr/bin/env python

# Copyright (C) 2015 ShRP
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from sys import argv
from socket import error
from scapy.all import *

print '--------------------------------------------------------------------------------'
print '\t\t\t\tWIFI Scanner'
print '--------------------------------------------------------------------------------'

aps = []


def wifiscan(pkt):

    if pkt.haslayer(Dot11Beacon) or pkt.haslayer(Dot11ProbeResp):

        if pkt[Dot11].addr3 not in aps:
            aps.append(pkt[Dot11].addr3)

            print 'BSSID; {0} \tESSID; {1}'.format(pkt[Dot11].addr3, pkt[Dot11Elt].info)

        else:
            pass
    else:
        pass

if __name__ == '__main__':

    try:
        sniff(iface=argv[1], prn=wifiscan)

    except error:
        print 'Are you root;'

    except IndexError:
        print 'Specify an interface'
