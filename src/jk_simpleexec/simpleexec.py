#!/usr/bin/env python3



from typing import Union,Sequence
import os
import time
import traceback
import sys
import abc
import subprocess
import json
from io import StringIO, BytesIO
import xml.etree.ElementTree as ElementTree
from lxml import etree as lxmletree

from .CommandResult import CommandResult





this = sys.modules[__name__]
this.debugFilePath = None


def simpleExecEnableDebugging(debuggingFilePath):
	this.debugFilePath = debuggingFilePath
#





#
# Synchroneously invokes the specified command. Output of STDOUT and STDERR is caught.
#
# @param		string cmdPath				The (absolute) path to the program to invoke
# @param		string[] cmdArgs			A list of arguments. Specify <c>None</c> if you do not want to have any arguments.
# @param		string onErrorExceptionMsg	If you specify an error message here an exception is thrown. If <c>None</c> is specified
#											<c>None</c> will be returned and no exception will be thrown.
# @param		mixed inputData				Either a string or binary data (or None) that should be passed on to the application invoked usint STDIN.
#											If string data is presented it is automatically encoded using UTF-8
# @return		CommandOutput				Returns an object representing the results.
#
def invokeCmd(
	cmdPath:str,
	cmdArgs:list,
	bRemoveTrailingNewLinesFromStdOut:bool = True,
	bRemoveTrailingNewLinesFromStdErr:bool = True,
	dataToPipeAsStdIn:Union[str,bytes,bytearray] = None,
	workingDirectory:str = None
	) -> CommandResult:

	assert isinstance(cmdPath, str)
	if cmdArgs is not None:
		assert isinstance(cmdArgs, (list, tuple))

	if workingDirectory:
		assert isinstance(workingDirectory, str)
		returnToDirectory = os.getcwd()
	else:
		returnToDirectory = None

	try:
		if workingDirectory:
			os.chdir(workingDirectory)

		if dataToPipeAsStdIn:
			if isinstance(dataToPipeAsStdIn, str):
				dataToPipeAsStdIn = dataToPipeAsStdIn.encode("utf-8")
			elif isinstance(dataToPipeAsStdIn, (bytes, bytearray)):
				pass
			else:
				raise Exception("Can only pipe string data and byte arrays!")

		cmd = []
		cmd.append(cmdPath)
		if cmdArgs is not None:
			cmd.extend(cmdArgs)

		if this.debugFilePath != None:
			with open(this.debugFilePath, 'a') as f:
				f.write("================================================================================================================================\n")
				f.write('EXECUTING: ' + str(cmd) + "\n")

		if dataToPipeAsStdIn:
			p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			p.stdin.write(dataToPipeAsStdIn)
		else:
			p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=None)
		(stdout, stderr) = p.communicate()

		output = []
		stdOutData = stdout.decode("utf-8")

		if this.debugFilePath != None:
			with open(this.debugFilePath, 'a') as f:
				f.write("STDOUT:\n")
				f.write(stdOutData + "\n")

		for line in stdOutData.split("\n"):
			output.append(line.rstrip())

		if bRemoveTrailingNewLinesFromStdOut:
			while (len(output) > 0) and (len(output[len(output) - 1]) == 0):
				del output[len(output) - 1]

		outputErr = []
		stdErrData = stderr.decode("utf-8")

		if this.debugFilePath != None:
			with open(this.debugFilePath, 'a') as f:
				f.write("STDERR:\n")
				f.write(stdErrData + "\n")

		for line in stdErrData.split("\n"):
			outputErr.append(line.rstrip())
		if bRemoveTrailingNewLinesFromStdErr:
			while (len(outputErr) > 0) and (len(outputErr[len(outputErr) - 1]) == 0):
				del outputErr[len(outputErr) - 1]

		return CommandResult(cmdPath, cmdArgs, output, outputErr, p.returncode)
	
	finally:
		if returnToDirectory:
			os.chdir(returnToDirectory)
#






