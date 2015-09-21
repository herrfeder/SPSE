import threading,Queue

threadrange = 3
queue = Queue.Queue(5)
gLock = threading.Lock()

inputlist = [(1,1),(2,2),(3,3),(4,4),(5,5)]

def main(inputlist):

	print "\t### Inputlist received:\n ###"

	print "Spawning the {0} threads.".format(threadrange)

	for x in xrange(threadrange):
		print "Thread {0} started.".format(x)
		workerbee().start()

	print "Putting stuff in queue"
	for i in inputlist:

		try:
			queue.put(i,block=True,timeout=5)
		except:
			gLock.acquire()
			print "Queue is full"
			gLock.release()

	gLock.acquire()
	print "Waiting for threads to finish"
	gLock.release()
	queue.join()

class workerbee(threading.Thread):
	print "test"	
	def run(self):
		print "test"
		while 1:
			try:
				job = queue.get(True,1)
				gLock.acquire()
				print "Multiplication of {0} with {1} gives {2}".format(job[0],job[1],(job[0]*job[1]))
				gLock.release()
				queue.task_done()
			except:
				break


if __name__ == '__main__':
	main(inputlist)
