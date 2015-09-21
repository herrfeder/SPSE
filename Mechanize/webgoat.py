from bs4 import BeautifulSoup
from mechanize import Browser
import re
import mechanize

url = "http://127.0.0.1/webgoat/attack"

br = Browser()
br.set_handle_robots(False)

br.add_password(url,"guest","guest")

br.open(url)

br.select_form(nr=0)
sub = br.click(type="submit",nr=0)
br.open(sub)

soup = BeautifulSoup(br.response().read(),'lxml')

link = soup.a

all_links = link.find_all_next('a')

print "Welche SQL-Operation?\n"
i = 0
SQL_links=[]
for link in all_links:
	if re.search(r'menu=1200',str(link)):
		i = i + 1
		SQL_links.append(str(link['href']))	
		print (str(i)+link.string)

number = raw_input("Auswahl:")

link_temp = url.rstrip("attack")+"/"+SQL_links[int(number)-1]
br.open(link_temp)

soup = BeautifulSoup(br.response().read(),'lxml')

textform = {}

try:
	i = 0
	for formnumber in range(0,10): 	
		br.select_form(nr=formnumber)	
		for control in br.form.controls:
			
			if control.type=="text":
				i = i+1
				print "\n%d name=%s value=%s" % (i,control.name, br[control.name])
				textform[str(formnumber)] = str(control.name)			
except mechanize._mechanize.FormNotFoundError:
	pass
print textform

retry = "yes"
while retry=="yes" or retry=="Yes":
	textnumber = raw_input("Welches Textfeld:")
	SQLi = raw_input("Give SQLi-String:")
			
	br.select_form(nr=int(textnumber))
	print SQLi
	br.form[textform[str(textnumber)]]=SQLi

	soup = BeautifulSoup(br.response().read(),'lxml')

	lesson_content = soup.find_all("div",id="lessonContent")
	form = lesson_content[0].find_next("form")
	

	print form
	print "\n"
#	print table
	


