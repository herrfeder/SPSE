#!/usr/bin/env/python



import BaseHTTPServer,CGIHTTPServer,cgitb,sys

cgitb.enable() #cgi error reporting

ip = sys.argv[1]

port = int(sys.argv[2])

print "usage <ip> <port>"

serverAdd = (ip,port)
server = BaseHTTPServer.HTTPServer
handler = CGIHTTPServer.CGIHTTPRequestHandler
handler.cgi_directories= ['/cgi-bin', '/htbin']
		

httpd =server(serverAdd,handler)

print "Serving at port ", serverAdd[1]

httpd.serve_forever()

