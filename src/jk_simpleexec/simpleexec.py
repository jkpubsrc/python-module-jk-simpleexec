#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import os
import time
import traceback
import sys
import abc
import subprocess
from io import StringIO, BytesIO
import xml.etree.ElementTree as ElementTree
from lxml import etree as lxmletree

import sh




#
# Objects of this class represent the processing result of a command.
#
class CommandResult(object):

	def __init__(self, cmd, cmdArgs, stdOutLines, stdErrLines, returnCode):
		self.__cmd = cmd
		self.__cmdArgs = cmdArgs
		self.__stdOutLines = stdOutLines
		self.__stdErrLines = stdErrLines
		self.__returnCode = returnCode



	#
	# Returns the path used for invokation of the command.
	# @return		string			The file path.
	#
	@property
	def commandPath(self):
		return self.__cmd



	#
	# Returns the arguments used for invokation of the command.
	# @return		string[]		The list of arguments (possibly an empty list or <c>None</c>).
	#
	@property
	def commandArguments(self):
		return self.__cmdArgs



	#
	# The return code of the command after completion.
	# @return		int			The return code.
	#
	@property
	def returnCode(self):
		return self.__returnCode



	#
	# The STDOUT output of the command.
	# @return		string[]		The output split into seperate lines. This property always returns a list, never <c>None</c>.
	#
	@property
	def stdOutLines(self):
		return self.__stdOutLines



	#
	# Return the text data as a regular ElemenTree object.
	#
	def getStdOutAsXML(self):
		lines = '\n'.join(self.__stdOutLines)
		xRoot = ElementTree.fromstring(lines)
		return xRoot



	#
	# Return the text data as an LXML tree object.
	#
	def getStdOutAsLXML(self):
		lines = '\n'.join(self.__stdOutLines)
		parser = lxmletree.XMLParser(remove_blank_text=True)
		xRoot = lxmletree.parse(BytesIO(lines.encode("utf-8")), parser)
		return xRoot



	#
	# The STDERR output of the command.
	# @return		string[]		The output split into seperate lines. This property always returns a list, never <c>None</c>.
	#
	@property
	def stdErrLines(self):
		return self.__stdErrLines



	#
	# Returns <c>True</c> iff the return code is not zero or <c>STDERR</c> contains data
	#
	@property
	def isError(self):
		return (self.__returnCode != 0) or (len(self.__stdErrLines) > 0)



	#
	# If the return code is not zero or <c>STDERR</c> contains data
	# an exception is thrown using the specified exception message.
	#
	# @param		string exceptionMessage			The message for the exception raised.
	# @return		CommandOutput					If no exception is raised the object itself is returned.
	#
	def raiseExceptionOnError(self, exceptionMessage, bDumpStatusOnError = False):
		if self.isError:
			if bDumpStatusOnError:
				self.dump()
			raise Exception(exceptionMessage)
		else:
			return self



	#
	# Write all data to STDOUT. This method is provided for debugging purposes of your software.
	#
	def dump(self, prefix = None):
		if prefix is None:
			prefix = ""
		print(prefix + "COMMAND: " + self.__cmd)
		print(prefix + "ARGUMENTS: " + str(self.__cmdArgs))
		for line in self.__stdOutLines:
			print(prefix + "STDOUT: " + line)
		for line in self.__stdErrLines:
			print(prefix + "STDERR: " + line)
		print(prefix + "RETURNCODE: " + str(self.__returnCode))



	#
	# Returns a dictionary containing all data.
	# @return		dict			Returns a dictionary with data registered at the following keys:
	#								"cmd", "cmdArgs", "stdOut", "stdErr", "retCode"
	#
	def toJSON(self):
		return {
			"cmd": self.__cmd,
			"cmdArgs" : self.__cmdArgs,
			"stdOut" : self.__stdOutLines,
			"stdErr" : self.__stdErrLines,
			"retCode" : self.__returnCode,
		}








this = sys.modules[__name__]
this.debugFilePath = None


def simpleExecEnableDebugging(debuggingFilePath):
	this.debugFilePath = debuggingFilePath






#
# Synchroneously invokes the specified command. Output of STDOUT and STDERR is caught.
#
# @param		string cmdPath				The (absolute) path to the program to invoke
# @param		string[] cmdArgs			A list of arguments. Specify <c>None</c> if you do not want to have any arguments.
# @param		string onErrorExceptionMsg	If you specify an error message here an exception is thrown. If <c>None</c> is specified
#											<c>None</c> will be returned and no exception will be thrown.
# @return		CommandOutput				Returns an object representing the results.
#
def invokeCmd(cmdPath, cmdArgs, bRemoveTrailingNewLinesFromStdOut = True, bRemoveTrailingNewLinesFromStdErr = True):
	assert isinstance(cmdPath, str)
	if cmdArgs is not None:
		assert isinstance(cmdArgs, list)

	cmd = []
	cmd.append(cmdPath)
	if cmdArgs is not None:
		cmd.extend(cmdArgs)

	if this.debugFilePath != None:
		with open(this.debugFilePath, 'a') as f:
			f.write("================================================================================================================================\n")
			f.write('EXECUTING: ' + str(cmd) + "\n")

	p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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






