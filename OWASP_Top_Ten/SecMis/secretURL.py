import urllib
import mechanize
from bs4 import BeautifulSoup as BSoup

class SecMis():
	pageNames = ['phpinfo.php', 'admin.php', 'info.php', 'console.php', 'getdate.php']
	dataDirs = ['passwords','documentation','includes']
	url = "http://192.168.8.103/mutillidae"

	def __init__(self):
	
		try:

			self.br = mechanize.Browser(factory=mechanize.DefaultFactory(i_want_broken_xhtml_support=True))
                	self.br.set_handle_robots(False)
                	self.br.set_handle_refresh(False)
                	self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
                	self.br.set_proxies({"http":"127.0.0.1:3128"})

		except Exception,e:

			print "### Wasn't able to create browser, because of : %s ###"%e


	def close(self):

		self.br.close()

	def attack(self):

		if self.br == None:
			return
		url = SecMis.url
		dataDirs = SecMis.dataDirs
		pages = SecMis.pageNames

	#	Directories = getDirectories(dataDirs,self.url)

		for file in pages:

			extension = {'page':file}

			response = self.br.open(url+"/index.php",urllib.urlencode(extension))

			soup = BSoup(response.read(),'lxml')

			responseMessage = soup.getText()

			if "404 - Page Not Found" not in responseMessage:	
				print extension


def main():
	
	attacker = SecMis()
	attacker.attack()
	attacker.close()


if __name__ == "__main__":

	main()
