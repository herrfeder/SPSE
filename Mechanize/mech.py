import mechanize

br = mechanize.Browser()
br.set_handle_robots(False)

br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

br.open('http://www.youtube.com')

print "Before modifying"
for form in br.forms():
	print form

br.select_form(nr=0)
br.set_all_readonly(False)
br.form['action_logout'] = '0'
print "After modifying"
for form in br.forms():
	print form


#------ interact with forms ------- #

#br.select_form(nr=0)

#br.form['q'] = 'defcon'

#br.submit()

#for link in br.links() :
#	print link.text
