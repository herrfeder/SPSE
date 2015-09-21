#!/usr/bin/python

import signal


def ctrlc_handler(signum, frm) :

	print "Haha! You cannot kill me!"


print "Installing singal handler ...."
signal.signal(signal.SIGINT, ctrlc_handler)

print "Done!"


while True :

	pass
