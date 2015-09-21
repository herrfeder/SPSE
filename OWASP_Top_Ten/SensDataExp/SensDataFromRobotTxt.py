from threading import Thread, Lock
from Queue import Queue, Empty
from mechanize import Browser
from bs4 import BeautifulSoup as BSoup
import sys
import re

gLock = Lock()
queue = Queue(10)
threads = []
class ScapeFromRobots(Thread):
	url = "http://127.0.0.1/mutillidae/"
	robot = "robots.txt"
	threadrange = 5
	def __init__(self,queue,br):
		Thread.__init__(self)
	
		self.queue = queue
		self.br    = br

	def run(self):
		
		url = ScapeFromRobots.url
					
		while True:
			dire = None

			try:
				dire = self.queue.get(timeout=.3)
				try:
					gLock.acquire()
					self.br.set_handle_robots(False)
					self.br.open(url.rstrip("/")+ dire)
					print "open Site %s"%(url.rstrip("/")+dire)
					soup = BSoup(self.br.response().read(),'lxml')
					print soup
					gLock.release()

					if "Object Not Found" in soup.get_text():
						print "\t### %s doesn't exist or isn't accessible ###\n"%dire
					else:
						print "\t### Content of %s ###\n"%dire
						for line in soup.get_text():
							print line
		
					queue.task_done()
					
				except Exception,e:
					print "Problem occured %s"%e
					sys.exit(0)

			except Empty:
				return

	def getRobots(self):

		robotdirs = []
		url = ScapeFromRobots.url
		robot = ScapeFromRobots.robot
		print "\t### Search for robots.txt in %s ###"%(url+robot)
		self.br.open(url+robot)

		soup = BSoup(self.br.response().read(),'lxml')
		stri = soup.p.string
		dir_list = stri.strip("\n")
		for line in dir_list:

			if "Disallow: " in line:

				robotdirs.append(line.replace("Disallow: ",""))

			elif "/" in line and not "Disallow: " in line:
				print "\t### Additional Directories found: %s ###"%line

		return robotdirs



def main():
	
	a = raw_input("Press ENTER to start")
	if a == "exit":
		sys.exit(0)
	else:	
		print "Start threadrange"
		for i in range(ScapeFromRobots.threadrange):
			worker = ScapeFromRobots(queue,Browser(history=None))
			worker.setDaemon(True)
			worker.start()
			threads.append(worker)
		
		directories = worker.getRobots()
		for dirline in directories:

			print "Directory: %s"%dirline
			dirline = dirline.strip().split('\n')
			
			try:
				print "Put Queue"
				queue.put(dirline[0],block=True,timeout=5)
			except:
				gLock.acquire()
				print "\t### Queue is full ###\n"
				gLock.release()
				pass	

		queue.join()

		for item in threads:

			item.join()


		stri = "Scan Completed"
		print "\t### %s ###\n"%(len(stri)*"#")
		print "\t### %s ###\n"%stri
		print "\t### %s ###\n"%(len(stri)*"#")    	

if __name__ == "__main__":
	main()	
