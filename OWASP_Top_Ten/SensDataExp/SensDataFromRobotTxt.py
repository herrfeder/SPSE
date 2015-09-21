from threading import Thread, Lock
from Queue import Queue, Empty
from mechanize import Browser
from bs4 import BeautifulSoup as BSoup

gLock = Lock()
queue = Queue()
threads = []
class ScapeFromRobots(Thread):
	url = "http://192.168.8.103/mutillidae/"
	robot = "robots.txt"
	threadrange = 5

	def __init__(self,queue,br):
		Thread.__init__(self)
	
		self.queue = queue
		self.br    = br

	def run(self):

		url = ScapeFromRobots.url

		while True:
			dir = None

			try:
				dir = self.queue.get(timeout=.3)

				try:
					gLock.acquire()
					self.br.set_handle_robots(False)
					self.br.open(url.rstrip("/")+ dir)

					soup = BSoup(self.br.response().read(),'lxml')
					gLock.release()

					if "Object Not Found" in soup.get_text():
						print "\t### %s doesn't exist or isn't accessible ###\n"%dir
					else:
						print "\t### Content of %s ###\n"%dir
						for line in soup.get_text():
							print line
					
				except Exception:
					raise
					print "fertig"

			except Empty:
				print "fertig"
				return

	def getRobots(self):

		robotdirs = []
		url = ScapeFromRobots.url
		robot = ScapeFromRobots.robot

		self.br.open(url+robot)

		soup = BSoup(self.br.response().read(),'lxml')
		
		for line in soup.p:

			if "Disallow: " in line:

				robotdirs.append(line.replace("Disallow: ",""))

			elif "/" in line:
				print "\t### Additional Directories found: %s ###"%line

		return robotdirs



def main():

	try:
		for i in range(ScapeFromRobots.threadrange):
			worker = ScapeFromRobots(queue,Browser(history=None))
			worker.setDaemon(True)
			worker.start()
			threads.append(worker)

		directories = worker.getRobots()
		print directories
		for dirline in directories:

			dirline = dirline.strip().split('\n')
			queue.put(dirline[0])

		queue.join()

		for item in threads:

			item.join()

	except (KeyboardInterrupt,SystemExit):
		pass

	stri = "Scan Completed"
	print "\t### %s ###\n"%(len(stri)*"#")
	print "\t### %s ###\n"%stri
	print "\t### %s ###\n"%(len(stri)*"#")    	

if __name__ == "__main__":
	main()	
