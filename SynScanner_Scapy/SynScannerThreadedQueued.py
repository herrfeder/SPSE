import threading
import socket
import Queue

class Scanner(threading.Thread):

  def __init__(self,queue):
    threading.Thread.__init__(self)
    self.queue = queue

  def run(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
      min_port = self.queue.get()
      for i in range (min_port, min_port+10):
        try:
          s.connect(('127.0.0.1',i))
          print str(i)+ " :open\n"
          s.close()
        except Exception, e:
          continue
      self.queue.task_done()

queue = Queue.Queue()

print "Scanning Started ..."

for i in range(5):
  scanner_o = Scanner(queue)
  scanner_o.setDaemon(True)
  scanner_o.start()

for i in range(1,3000,50):
  queue.put(i)

queue.join()

print "Scanning Done"
