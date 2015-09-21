from urllib import urlopen
from bs4 import BeautifulSoup

webpage = urlopen('http://www.youtube.com/watch?v=9hIQjrMHTv4').read()

ytSoup = BeautifulSoup(webpage)

title = ytSoup.find('span',id='eow-title')
uploader = ytSoup.find('a', class_='author')
date = ytSoup.find('span', id='eow-date')


print 'title: ',title
print 'uploader: ',uploader
print 'date: ',date
