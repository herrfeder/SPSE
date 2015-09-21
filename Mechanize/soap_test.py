from __future__ import print_function
from bs4 import BeautifulSoup
from ZSI.auth import AUTH
from ZSI.client import Binding
from ZSI import EvaluateException
from mechanize import Browser,CookieJar
from mechanize._http import HTTPRefererProcessor
import mechanize

class CustomizedBrowser(Browser):
	def __init__(self):
		Browser.__init__(self)
		self.set_handle_redirect(True)
		self.set_handle_referer(True)
		self.set_handle_equiv(True)
		self.set_handle_robots(False)
		self.set_handle_referer(False)
		self.set_handle_refresh(HTTPRefererProcessor(),max_time=1)
		self.cookiejar = CookieJar()
		self.set_cookiejar(self.cookiejar)

	def getCookies(self):
		return self.cookie_jar

def exercise_one():
	print('<----------------Exercise 1 ------------->')
	url = 'http://127.0.0.1/webgoat/services/SoapRequest'
	binding = Binding(url=url)
	binding.SetAuth(AUTH.httpbasic,'guest','guest')
	try:
		browser = CustomizedBrowser()
		browser.add_password(url, 'guest','guest')
		browser.open('http://127.0.0.1/webgoat/services/SoapRequest?WSDL')
		soup= BeautifulSoup(browser.response().read(),'lxml')
		print("test")
		print(soup)
	except mechanize.HTTPError, response:
		pass	
	soup = BeautifulSoup(browser.response().read(),'lxml')
	print(soup)
	port_type = soup.find('wsdl:porttype')
	for operation in port_type.find_all('wsdl:operation'):
		print(getattr(binding,operation['name'])(101))

def main():
		
	exercise_one()

if __name__ == '__main__':
	main()



