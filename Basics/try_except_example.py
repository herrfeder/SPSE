#!/usr/bin/python


class InputError(Exception) :

	def __init__(self,value):
		self.value = value

password = raw_input("Bitte gebe ein gueltiges Passwort ein")


try:
	if password != "hello":

		raise InputError(password)
	else:
		print "Password correct!"


except InputError as error:

	print "InputError:", error.value
