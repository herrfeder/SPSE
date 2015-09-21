from bs4 import BeautifulSoup
import urllib2
import re

for site in range(1,20):
	req = urllib2.Request('http://www.movie-blog.org/page/' + str(site) +'/', headers = {'User-Agent':'Mozilla/5.0'})
	html = urllib2.urlopen(req).read()
	blogSoup = BeautifulSoup(html,'lxml')

	first_link = blogSoup.a
	all_links = first_link.find_all_next('a')

	for line in all_links:
        
		wort = str(line)
		if re.search(r'title="Permanent Link to',wort):
   			# finding movie-title	
			a = re.search(r'title="Permanent Link to ', wort)
   			startstring = a.end()
			b = re.search(r'"',wort[startstring:])
			endstring = b.start()
		
			# finding link
			a = re.search(r'href="',wort)
			startlink = a.end()
			b = re.search(r'"',wort[startlink:])
			endlink = b.start()
			print "\n"
			print wort[startlink:startlink+endlink]
			print wort[startstring:startstring+endstring]
   

