from argparse import ArgumentParser
from re import match
from scapy.all import *
from sys import argv



class HTTPSniffer:

	def __init__(self, interface, filter):

		self.interface = interface
		self.filter = filter

	def sniff(self):

		print '(!) Sniffing on: {0}, filter: {1}\n'.format(self.interface,self.filter)

		while True:

			pkt = sniff(iface = self.interface, filter = self.filter, count = 10)

			if pkt[0].haslayer(Raw):
				packet = str(pkt[0]['Raw'])
				header = packet.split('\r\n')

				if match('^GET.+', header[0]):
					print '(+) {0}\n'.format(header)

				elif match('^POST.+', header[0]):
                                        print '(+) {0}\n'.format(header)

				elif match('^HTTP.+', header[0]):
                                        del header[len(header)-1]
					print '(+) {0}\n'.format(header)

				else:
					pass


def main():

	parser = ArgumentParser(description='HTTP Sniffer')
	parser.add_argument('Interface', metavar='Interface', type=str, help='Interface')
	parser.add_argument('Filter', metavar='Filter', type=str, help='Filter')
	args = parser.parse_args()

	worker = HTTPSniffer(argv[1], argv[2])
	worker.sniff()

if __name__ == '__main__':
	main()
