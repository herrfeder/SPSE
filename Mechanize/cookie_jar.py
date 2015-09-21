import mechanize

url = 'http://localhost/dvwa/index.php'

print "\nstarting first browser"
cookies = mechanize.CookieJar()

print "starting cookies; {0}".format(str(len(cookies)))

browser_1 = mechanize.Browser()
browser_1.set_cookiejar(cookies)

browser_1.open(url)
print "Connected to: {0}".format(browser_1.title())

browser_1.select_form(nr=0)
browser_1.form['username'] = 'admin'
browser_1.form['password'] = 'password'
browser_1.submit()

print browser_1.title()

print "cookies after authentication:{0}".format(str(len(cookies)))
for c in cookies:
	print c

print "\nstarting second browser"
ncookies = mechanize.CookieJar()

print "new cookie jar: {0}".format(str(len(ncookies)))
browser_2 = mechanize.Browser()

browser_2.set_cookiejar(cookies)

browser_2.open(url)
print browser_2.title()

for c in cookies:
	print c

