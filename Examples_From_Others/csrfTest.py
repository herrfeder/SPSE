import mechanize
from BeautifulSoup import BeautifulSoup
import sys
import urllib

if len(sys.argv) > 1:
    url = sys.argv[1]
    
    username = 'testCsrfUser'
    password = 'password'
    data = {'csrf-token':'', 'username':username, 'password':password, 'confirm_password':password, 'my_signature':username, 'register-php-submit-button':'Create+Account'}
    
    br = mechanize.Browser()
    
    br.open(url, urllib.urlencode(data))
    
    bs = BeautifulSoup(br.response().read())
    
    successMessage = bs.findAll('h2', {'class':'success-message'})[0].getText()
    
    print successMessage
    