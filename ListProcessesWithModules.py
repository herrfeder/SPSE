#!/usr/bin/env python

import immlib

DESC = "Play with Processes!"

def main(args):

	imm = immlib.Debugger()

	imm.openProcess("C://StrCpy.exe")

#### Attaching to Process ####

	imm.Attach(int(args[0]))

#### Show all Modules and their abilities ####

	

	td = imm.createTable("Module Information",['Name', 'Base', 'Entry', 'Size', 'Version'])	

	moduleList = imm.getAllModules()

	for entity in moduleList.values():
	
		td.add(0, [ entity.getName(),
			    '%08X'%entity.getBaseAddress(),
			    '%08X'%entity.getEntry(),
			    '%08X'%entity.getSize(),
			    entity.getVersion()
			    ])			
	
	imm.log(str(imm.getRes()))


	return "Success"
