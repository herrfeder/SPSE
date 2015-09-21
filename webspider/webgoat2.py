import MySQLdb as mdb
from bs4 import BeautifulSoup as BSoup
import mechanize
import argparse
import re

	
def connecting(url):

	if not url.startswith("http://"):
		url = "http://" + url

	
	br = mechanize.Browser(factory=mechanize.DefaultFactory(i_want_broken_xhtml_support=True))
	br.set_handle_robots(False)
	br.set_handle_refresh(False)
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	

	if re.search(r'webgoat',url):
		br.add_password(url,'guest','guest')
		br.set_proxies({"http":"127.0.0.1:3128"})
		br.open(url)
		br.select_form(nr=0)
		sub = br.click(type="submit",nr=0)
		br.open(sub)
	
	br.open(url)

	return br

def openDB():

	con = mdb.connect('localhost','testuser','testuser1','testdb')  
	cur = con.cursor()
	cur.execute("DROP TABLE IF EXISTS Spider")
	cur.execute("CREATE TABLE Spider(URL VARCHAR(100), HTML VARCHAR(10000), FORM VARCHAR(1000))")
	
	return con
#########################################################
def searchingTree(depth,con,br,root_url,link_list):
	print "Looking into %s"%str(br.geturl())
	cur = con.cursor()

	while True:
		try:	
			br.select_form(nr=0)
			
			formstring=findForms(br)
		
		except  mechanize._mechanize.FormNotFoundError,mechanize._mechanize.BrowserStateError:
			
			formstring = "No Forms on this Site"
		
		soup = BSoup(br.response().read(),'lxml')
		cur.execute("INSERT INTO Spider(URL,HTML,FORM) VALUES(%s,%s,%s)",(str(br.geturl()),'A',str(formstring)))
		con.commit()
			
			
		for link in br.links():
			####### preedit links in a own beautifulSoup-Function ####### 
			####### here work only soup-list of links without if-structures #######				
			link = str(link.url)
			link = link.lstrip("attack")
		
			if link.startswith(root_url):
				
				if link in link_list:
				        continue
				link_list.append(link)

				br.open(link)
			##### give new site to a new thread, without recursive function #####
				searchingTree(depth,con,br,root_url,link_list)

			elif link.startswith("/") and (link.endswith("/") or link.endswith("html")):
				url=str(root_url)
				new_link = url + link
				
				if new_link in link_list:
					continue
				link_list.append(new_link)

				try:
					br.open(new_link)
				except:
					continue

				searchingTree(depth,con,br,root_url,link_list)

			elif re.search(r'[?=&]',link) and not re.search(r'javascript',link):
				url=str(root_url)
				new_link = url + link
			

					
				if new_link in link_list:
                                       continue
				link_list.append(new_link)
				try:
					
					br.open(new_link)
				except:
					continue
				searchingTree(depth,con,br,root_url,link_list)
			
			
		

################################################
def findForms(br):
	
	try:
		formstring=[]
		for formnumber in range(0,10):
			br.select_form(nr=formnumber)
			#formstring.append(str(br.form))
			formstring.append("\n")
			try:
				for control in br.form.controls:
					formstring.append(" %s \n\t %s \n\t %s \n" % (control.type,control.name,br[control.name]))
			except ValueError:
				pass
	except mechanize._mechanize.FormNotFoundError:
		return formstring

#################################################
					


if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument('-u',dest='url')
        parser.add_argument('-d',dest='depth')
        args = parser.parse_args()
  	
	br = connecting(args.url)
	con = openDB()
	
	root_url = args.url
	link_list =[]
	searchingTree(args.depth,con,br,root_url,link_list)	
