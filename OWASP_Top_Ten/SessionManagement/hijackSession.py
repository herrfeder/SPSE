from bs4 import BeautifulSoup as BSoup
import mechanize
import re

cookies = mechanize.CookieJar()
br = mechanize.Browser(factory=mechanize.DefaultFactory(i_want_broken_xhtml_support=True))
br.set_cookiejar(cookies)
br.set_handle_robots(False)
br.set_handle_refresh(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

br.set_proxies({"http":"127.0.0.1:3128"})
br.open("http://127.0.0.1/mutillidae/")

for c in cookies:
	print c
