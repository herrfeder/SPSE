import mechanize


cj = mechanize.LWPCookieJar()
cj.revert("cookie3.txt")
opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cj))
r = opener.open("http://localhost/dvwa")
cj.save("cookie3.txt")
