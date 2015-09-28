#!/usr/bin/env python

import immlib
from immlib import AllExceptHook

class DemoHook (AllExpectHook) :

	def __init__(self) :

		AllExceptHook.__init__(self)

	def run(self, regs) :

		imm = immlib.Debugger()
		eip = regs['EIP']
		esp = regs['ESP']

		imm.log('EIP: 0x%08X ESP: 0x%08X'%(eip, esp))

		buf = imm.readString(esp)

		if len(buf) :
		
			imm.log('String len at ESP: %d\n\s'%(len(buf),buf))

def main(args):

	imm = immlib.Debugger()

	newHook = DemoHook()

	newHook.add("Demo Hook")

	return "SPSE Hook Command"
		
