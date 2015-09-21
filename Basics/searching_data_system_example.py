#! /usr/bin/python

import os

directory = "/home/herrfeder/Dokumente/Programmierung/"


def print_directory(pfad,level):

	for name in os.listdir(pfad):

		if os.path.isfile(pfad+name):
			
	 		print level*"--" + name

		elif os.path.isdir(pfad+name):

			print level*"--" + name
			level=level+1
			print_directory(pfad+name+"/",level)

print_directory(directory,1)
