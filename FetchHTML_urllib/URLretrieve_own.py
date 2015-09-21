#!/usr/env/python

from urllib import urlretrieve
import sys
import getopt
from os.path import exists,normpath,sep
import os
import re

DEFAULT_FILE_LOC = "."

class DownloadFile(object):

	def __init__(self, site, location=DEFAULT_FILE_LOC, filename=None):

		self.__url__ = site
		self.__url__ = self.__url__.rstrip(sep)
		self.__location__ = location
		self.filename = "{0}{1}{2}".format(self.__location__,"/", self.__url__.split(sep)[-1])
			
	def textprogress(self, count, blockSize, totalSize):
		try:
			frac = float(count*blockSize)/float(totalSize)
		except:
			frac = 0

		bar = "." * int(float(count*blockSize)/float(totalSize))*100
	
		sys.stdout.write("\r%-25.25s%d"%self.filename,frac)
		sys.stdout.flush()

	def perform(self):
		try:
			urlretrieve(self.__url__, self.filename, reporthook=self.textprogress)
		except KeyboardInterrupt:
			raise
		finally:
			sys.stdout.write("\n")

def process_args(args):
	url = " "
	loc = DEFAULT_FILE_LOC

	try:
		opts,args = getopt.getopt(args,"u:o:")
	
		for opt,arg in opts:
			if opt == "-u":
				url = arg
			elif opt == "-o":
				loc = arg
				print "3%s"%loc				
	except TypeError:
		raise
	except getopt.GetoptError:
		raise("invalid argument")

	return (url, loc)
			

if __name__ == "__main__":

	try:
		(url, loc) = process_args(sys.argv[1:])
		

		if url is None:
			raise TypeError('missing url')
		if loc is None or loc == "." or  not exists(loc):
			loc = os.getcwd()
		f = DownloadFile(site=url,location=loc)
		f.perform()
	
	except KeyboardInterrupt:
		sys.stdout.write("\n")
		print "download interrupted"
		sys.exit(0)
	else:
		print "{0} download complete".format(f.filename)
		sys.exit(0)	

