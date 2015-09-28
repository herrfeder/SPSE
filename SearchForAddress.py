#!/usr/bin/env python

import immlib

DESC = "find Instructions!"

def main(args) :

	imm = immlib.Debugger()

	assembledInstruction = imm.assemble('  '.join(args))

	if not assembledInsctruction:

		return "[*] No Insctruction Given!"

	addressList = imm.search(assembledInstruction)

	td = imm.createTable("Instruction Locations", ['Module', 'Base Address', 'Instruction Address', 'Instruction'])

	for address in addressList:

		module = imm.findModule(address)
		if not module:
			imm.log("Address: 0x%08X not in any module"%address)
			continue

		

	instruction = ''

	numArgs = len('  '.join(args).split('\n'))

	for count in range(0, numArgs) :
		instruction += imm.disasmForward(address, nlines=count).getDisasm() + ' '

	td.add(0, [ module[0],
		    str('0x%08X'%module[1],
		    str('0x%08X'%address),
		    instruction
		    ])
