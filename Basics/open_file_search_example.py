#!/usr/bin/python

fdesc = open("/var/log/dmesg","r")

for line in fdesc.readlines() :

	found = line.find("usb")

	if found != -1:

		print line

fdesc.close()
