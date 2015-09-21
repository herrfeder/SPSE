#!/usr/bin/python

import threading, Queue, time, ftplib, re

class WorkerThread(threading.Thread):

        def __init__(self, queue, lock):
                threading.Thread.__init__(self)
                self.queue = queue
                self.lock = lock

        def run(self):
                while True:
                        url = self.queue.get()
                        print "Get url: %s" %url
                        list = []
                        try:
                                ftp = ftplib.FTP(url)
                                ftp.login()
                                ftp.retrlines('LIST', list.append)
                                ftp.quit()
                        except ftplib.all_errors as (errno, strerror):
                                list.append(strerror)
                        self.queue.task_done()
                        lock.acquire()
                        flist = open("ftpscan.txt", "a")
                        flist.write("Listing " + url + "\n")
                        for item in list:
                                flist.write(item + "\n")
                        flist.write("\n")
                        flist.close()
                        lock.release()

queue = Queue.Queue()
lock = threading.Lock()
flist = open("ftpscan.txt", "w")
flist.close()
ftpfile = open("ftplist.txt", "r")
ftplist = []
for url in ftpfile:
        match = re.search(r'//([\w.-]+)/', url)
        if match:
                if match.group(1) not in ftplist:
                        ftplist.append(match.group(1))
for i in range(5):
        worker = WorkerThread(queue, lock)
        worker.setDaemon(True)
        worker.start()
for url in ftplist:
        queue.put(url)
queue.join()