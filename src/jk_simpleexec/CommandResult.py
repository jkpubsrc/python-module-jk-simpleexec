

import typing
import os
import time
import traceback
import sys
import abc
import subprocess
import json
from io import StringIO, BytesIO
import xml.etree.ElementTree as ElementTree

import jk_prettyprintobj
from jk_cmdoutputparsinghelper.TextData import TextData






#
# Objects of this class represent the processing result of a command.
#
class CommandResult(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self,
			cmd:str,
			cmdArgs:list,
			stdOut:typing.Union[list,tuple,str,TextData],
			stdErr:typing.Union[list,tuple,str,TextData],
			returnCode:int,
			duration:float = -1,
		):

		self.__cmd = cmd
		self.__cmdArgs = cmdArgs
		self.__stdOut = stdOut if isinstance(stdOut, TextData) else TextData(stdOut)
		self.__stdErr = stdErr if isinstance(stdErr, TextData) else TextData(stdErr)
		self.__returnCode = returnCode
		self.__duration = duration
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	#
	# Returns the path used for invoking the command.
	#
	# @return		str			The file path.
	#
	@property
	def commandPath(self) -> str:
		return self.__cmd
	#

	#
	# Returns the arguments used for invoking the command.
	#
	# @return		str[]		The list of arguments (possibly an empty list or <c>None</c>).
	#
	@property
	def commandArguments(self) -> typing.List[str]:
		return self.__cmdArgs
	#

	#
	# The return code of the command after completion.
	#
	# @return		int			The return code.
	#
	@property
	def returnCode(self) -> int:
		return self.__returnCode
	#

	#
	# The STDOUT output of the command as a list of text lines.
	# This is the same as invoking <c>stdOut.lines</c>.
	#
	# @return		str[]		The output split into seperate lines. This property always returns a list, never <c>None</c>.
	#
	@property
	def stdOutLines(self) -> typing.List[str]:
		return self.__stdOut.lines
	#

	#
	# The STDERR output of the command as a list of text lines.
	# This is the same as invoking <c>stdErr.lines</c>.
	#
	# @return		str[]		The output split into seperate lines. This property always returns a list, never <c>None</c>.
	#
	@property
	def stdErrLines(self) -> typing.List[str]:
		return self.__stdErr.lines
	#

	#
	# The STDOUT output of the command as a single string.
	# This is the same as invoking <c>stdOut.text</c>.
	#
	# @return		str[]		The output as <c>str</c>. This property always returns a list, never <c>None</c>.
	#
	@property
	def stdOutStr(self) -> str:
		return self.__stdOut.text
	#

	#
	# The STDERR output of the command as a single string.
	# This is the same as invoking <c>stdErr.text</c>.
	#
	# @return		str[]		The output as <c>str</c>. This property always returns a list, never <c>None</c>.
	#
	@property
	def stdErrStr(self) -> str:
		return self.__stdErr.text
	#

	#
	# Direct access to the internal `TextData` object that manages the STDOUT output.
	#
	# @return		jk_cmdoutputparsinghelper.TextData			The TextData object that holds the text data.
	#
	@property
	def stdOut(self) -> TextData:
		return self.__stdOut
	#

	#
	# Direct access to the internal `TextData` object that manages the STDERR output.
	#
	# @return		jk_cmdoutputparsinghelper.TextData			The TextData object that holds the text data.
	#
	@property
	def stdErr(self) -> TextData:
		return self.__stdErr
	#

	#
	# Returns <c>True</c> if either the return code is non-zero or <c>STDERR</c> contains some data.
	#
	@property
	def isError(self) -> bool:
		return (self.__returnCode != 0) or (len(self.__stdErr.lines) > 0)
	#

	#
	# Returns <c>True</c> if the return code is non-zero.
	#
	@property
	def isErrorRC(self) -> bool:
		return self.__returnCode != 0
	#

	@property
	def duration(self) -> float:
		return self.__duration
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dumpVarNames(self) -> list:
		return [
			"commandPath",
			"commandArguments",
			"stdOutLines",
			"stdErrLines",
			"returnCode",
			"isError",
			"isErrorRC",
			"duration",
		]
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	#
	# If the return code is non-zero
	# an exception is thrown using the specified exception message.
	# This is a convenience function very similar to raiseExceptionOnError().
	#
	def assertSuccess(self, logOrLogFunction = None):
		if self.__returnCode != 0:
			if logOrLogFunction:
				printFunc = getattr(logOrLogFunction, "warn", None)
				if printFunc is None:
					printFunc = getattr(logOrLogFunction, "info", None)
				if printFunc is None:
					assert callable(logOrLogFunction)
					printFunc = logOrLogFunction
				self.dump(printFunc=printFunc)
			raise Exception("Failed to execute command: " + self.__cmd)

		return self
	#

	#
	#
	# Interpret the text data as JSON data and return it.
	#
	def getStdOutAsJSON(self):
		return json.loads(self.__stdOut.text)
	#

	#
	# Interpret the text data as XML and return an ElemenTree object.
	#
	def getStdOutAsXML(self):
		xRoot = ElementTree.fromstring(self.__stdOut.text)
		return xRoot
	#

	#
	# Interpret the text data as an LXML tree object and return it.
	#
	# NOTE: Invoking this method requires the python module "<c>lxml</c>" to be installed.
	#
	def getStdOutAsLXML(self):
		try:
			from lxml import etree as lxmletree
			parser = lxmletree.XMLParser(remove_blank_text=True)
		except Exception as e:
			raise Exception("lxml module is required for getStdOutAsLXML() to work!")
		xRoot = lxmletree.parse(BytesIO(self.__stdOut.text.encode("utf-8")), parser)
		return xRoot
	#

	#
	# If the return code is non-zero or <c>STDERR</c> contains data
	# an exception is thrown using the specified exception message.
	#
	# @param		str exceptionMessage			The message for the exception raised.
	# @return		CommandOutput					If no exception is raised the object itself is returned.
	#
	def raiseExceptionOnError(self, exceptionMessage:str, bDumpStatusOnError:bool = False, printFunc = None):
		if self.isError:
			if bDumpStatusOnError:
				self.dump(printFunc = printFunc)
			raise Exception(exceptionMessage)

		return self
	#

	"""
	NOTE: this method dump() has been replaced by the version in `jk_prettyprintobj.DumpMixin`.

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
		for line in self.__stdOut:
			writeFunction(prefix + "STDOUT: " + repr(line))
		for line in self.__stdErr:
			writeFunction(prefix + "STDERR: " + repr(line))
		writeFunction(prefix + "RETURNCODE: " + str(self.__returnCode))
	#
	"""

	#
	# Convert the whole object to a JSON dictionary.
	#
	# @return		dict			Returns a dictionary with data registered at the following keys:
	#								"cmd", "cmdArgs", "stdOut", "stdErr", "retCode"
	#
	def toJSON(self):
		return {
			"cmd": self.__cmd,
			"cmdArgs" : self.__cmdArgs,
			"stdOut" : self.__stdOut.lines,
			"stdErr" : self.__stdErr.lines,
			"retCode" : self.__returnCode,
			"duration": self.__duration,
		}
	#

#












