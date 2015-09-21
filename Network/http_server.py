#!/usr/bin/python

import SocketServer
import SimpleHTTPServer





class HTTPRequestHandler (SimpleHTTPServer.SimpleHTTPRequestHandler) :

	def do_GET(self) :

		if self.path == "/admin" :
			self.wfile.write('This page is only for Admins!')
			self.wfile.write(self.headers)

		else:	
			SimpleHTTP.Server.SimpleHTTPRequestHandler.do_GET(self)


httpServer = SocketServer.TCPServer(('', 80), HTTPRequestHandler)

httpServer.serve_forever()
