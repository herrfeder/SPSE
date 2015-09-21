#!/usr/bin/env python

import socket
import os
import time
import threading
import Queue
from ftplib import FTP


ftp_sites = ['ftp1.freebsd.org','ftp.it.freebsd.org','ftp.freshrpms.net','ftp.heanet.ie','ftp.it.freebsb.org','ftp.mirror.nl','ftp.ch.freebsb.org','ftp.lublin.pl','ftp.tc-chemitz.de','ftp.tiscali.de']

class WorkerThread(threading.Thread):

  def __init__(self,queue,id):
    threading.Thread.__init__(self)
    self.queue=queue
    self.id = id

  def run(self):
    sites=self.queue.get()
    ftp=FTP(sites)
    ftp.login()
    ftp.retrlines('LIST')
    print "finished listing of %s"%sites
    self.queue.task_done()

queue=Queue.Queue()

for i in range(5):
  print "Creating Worker Thread: %d"%i
  worker = WorkerThread(queue,i)
  worker.setDaemon(True)
  worker.start()
  print "Worker Thread %d Created"%i

for x in ftp_sites:
  queue.put(x)

queue.join()

print "All Tasks Over"
