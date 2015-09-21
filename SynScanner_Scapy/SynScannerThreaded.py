from argparse import ArgumentParser
from scapy.all import *
import sys
import thread
import socket
import time

def scanner(dip,dport):

  try:

 # response = sr1(IP(dst=ip)/TCP(dport=port, flags="S"), timeout = 1, verbose=1)
 # if response:
 #   if response.sprintf("%TCP.flags%" == "SA"):
 #	   print "Port" + str(port) + "open"
 #   else:
 #		  print "Port" + str(port) + "closed"
 # else:
 #   print "No Response"

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((dip,dport))
    print "port %d is open \n"%dport
    s.close()

  except Exception:
    import traceback
    print traceback.format_exc()

def main():

    parser = ArgumentParser(description='Threaded SynScanner')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('Ip', metavar='Ip', type=str, help='Ip')
    parser.add_argument('minP', metavar='minP', type=int, help='minimalPort')
    parser.add_argument('maxP', metavar='maxP', type=int, help='maximalPort')

    args = parser.parse_args()

    miP = args.minP
    maP = args.maxP

    if miP >= maP:
      print('Es heisst nicht grundlos minimal und maximal')
      sys.exit(2)
    elif miP == 0 or maP == 0:
      print('Es gibt keinen nullten Port')
      sys.exit(2)

    ports = maP - miP

    for i in range(0,ports):

      thread.start_new_thread(scanner,(args.Ip,miP+i))
      time.sleep(1)

if __name__ == '__main__':
  main()
