#!/usr/bin/python

import CGIHTTPServer

serve_addr = (("127.0.0.1",80))

handler = CGIHTTPServer.CGIHTTPRequestHandler

serve_addr = ("localhost",80)

handler.cgi_directories = ['/cgi-bin']

web = CGIHTTPServer.BaseHTTPServer.HTTPServer(serve_addr,handler)

web.serve_forever()
