#!/usr/bin/env python3




import os
import time
import traceback
import sys
import abc
import subprocess
import json
from io import StringIO, BytesIO
import xml.etree.ElementTree as ElementTree




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



	#
	# Returns the path used for invokation of the command.
	# @return		string			The file path.
	#
	@property
	def commandPath(self):
		return self.__cmd
	#



	#
	# Returns the arguments used for invokation of the command.
	# @return		string[]		The list of arguments (possibly an empty list or <c>None</c>).
	#
	@property
	def commandArguments(self):
		return self.__cmdArgs
	#



	#
	# The return code of the command after completion.
	# @return		int			The return code.
	#
	@property
	def returnCode(self):
		return self.__returnCode
	#



	#
	# The STDOUT output of the command.
	# @return		string[]		The output split into seperate lines. This property always returns a list, never <c>None</c>.
	#
	@property
	def stdOutLines(self):
		return self.__stdOutLines
	#


	#
	# Return the text data as a regular JSON object.
	#
	def getStdOutAsJSON(self):
		lines = '\n'.join(self.__stdOutLines)
		return json.loads(lines)
	#



	#
	# Return the text data as a regular ElemenTree object.
	#
	def getStdOutAsXML(self):
		lines = '\n'.join(self.__stdOutLines)
		xRoot = ElementTree.fromstring(lines)
		return xRoot
	#



	#
	# Return the text data as an LXML tree object.
	#
	def getStdOutAsLXML(self):
		lines = '\n'.join(self.__stdOutLines)
		try:
			from lxml import etree as lxmletree
			parser = lxmletree.XMLParser(remove_blank_text=True)
		except Exception as e:
			raise Exception("lxml module is required for getStdOutAsLXML() to work!")
		xRoot = lxmletree.parse(BytesIO(lines.encode("utf-8")), parser)
		return xRoot
	#



	#
	# The STDERR output of the command.
	# @return		string[]		The output split into seperate lines. This property always returns a list, never <c>None</c>.
	#
	@property
	def stdErrLines(self):
		return self.__stdErrLines
	#



	#
	# Returns <c>True</c> iff the return code is not zero or <c>STDERR</c> contains data
	#
	@property
	def isError(self):
		return (self.__returnCode != 0) or (len(self.__stdErrLines) > 0)
	#



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



	#
	# Write all data to STDOUT. This method is provided for debugging purposes of your software.
	#
	def dump(self, prefix = None, writeFunction = None):
		if writeFunction is None:
			writeFunction = print
		if prefix is None:
			prefix = ""
		writeFunction(prefix + "COMMAND: " + self.__cmd)
		writeFunction(prefix + "ARGUMENTS: " + str(self.__cmdArgs))
		for line in self.__stdOutLines:
			writeFunction(prefix + "STDOUT: " + line)
		for line in self.__stdErrLines:
			writeFunction(prefix + "STDERR: " + line)
		writeFunction(prefix + "RETURNCODE: " + str(self.__returnCode))
	#



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
	#



#














