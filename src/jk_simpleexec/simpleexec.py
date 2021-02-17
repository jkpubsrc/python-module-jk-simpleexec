


import os
import sys
import subprocess
import typing

from .CommandResult import CommandResult
from .TextDataProcessingPolicy import TextDataProcessingPolicy
from ._DebugValveToFile import _DebugValveToFile
from . import _common as _common






#
# Synchroneously invokes the specified command on the local machine. Output of STDOUT and STDERR is collected and returned by the <c>CommandResult</c> return object.
#
# NOTE: Despite for <c>cmdPath</c> and <c>cmdArgs</c> do <b>not</b> rely on the order of the arguments. If you need to specify them invoke them by name as they are
# intended to be invoked that way! Their order might be changed unnoticed in other versions of this API.
#
# NOTE: This method is deprecated and should no longer be called. Please use the new <c>invokeCmd1()</c> instead.
#
# @param		string cmdPath						(required) The (absolute) path to the program to invoke.
# @param		string[] cmdArgs					(required) A list of arguments. Specify <c>None</c> if you do not want to have any arguments.
#													Please note that there is no shell to interprete these commands.
# @param		string onErrorExceptionMsg			If you specify an error message here an exception is thrown. If <c>None</c> is specified
#													<c>None</c> will be returned and no exception will be thrown.
# @param		str|bytes[] dataToPipeAsStdIn		(optional) Either a string or binary data (or None) that should be passed on to the application invoked usint STDIN.
#													If string data is presented it is automatically encoded using UTF-8
# @param		str workingDirectory				(optional) If you specify a working directory here this function will change to this working directory
#													specified in <c>workingDirector</c> and return to the previous one after the command has been completed.
# @return		CommandOutput						Returns an object that contains the exit status, STDOUT and STDERR data.
#
def invokeCmd(
		cmdPath:str,
		cmdArgs:list,
		bRemoveTrailingNewLinesFromStdOut:bool = True,
		bRemoveTrailingNewLinesFromStdErr:bool = True,
		dataToPipeAsStdIn:typing.Union[str,bytes,bytearray] = None,
		workingDirectory:str = None,
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

		if _common.debugValve:
			_common.debugValve("================================================================================================================================")
			_common.debugValve("EXECUTING:", cmd)

		if dataToPipeAsStdIn:
			p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			p.stdin.write(dataToPipeAsStdIn)
		else:
			p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=None)
		(stdout, stderr) = p.communicate()

		output = []
		stdOutData = stdout.decode("utf-8")

		if _common.debugValve:
			_common.debugValve("STDOUT:")
			_common.debugValve(stdOutData)

		for line in stdOutData.split("\n"):
			output.append(line.rstrip())

		if bRemoveTrailingNewLinesFromStdOut:
			while (len(output) > 0) and (len(output[len(output) - 1]) == 0):
				del output[len(output) - 1]

		outputErr = []
		stdErrData = stderr.decode("utf-8")

		if _common.debugValve != None:
			_common.debugValve("STDERR:")
			_common.debugValve(stdErrData)

		for line in stdErrData.split("\n"):
			outputErr.append(line.rstrip())
		if bRemoveTrailingNewLinesFromStdErr:
			while (len(outputErr) > 0) and (len(outputErr[len(outputErr) - 1]) == 0):
				del outputErr[len(outputErr) - 1]

		if _common.debugValve != None:
			_common.debugValve("RETURN CODE:", p.returncode)

		return CommandResult(cmdPath, cmdArgs, output, outputErr, p.returncode)

	finally:
		if returnToDirectory:
			os.chdir(returnToDirectory)
#





#
# Synchroneously invokes the specified command on the local machine. Output of STDOUT and STDERR is collected and returned by the <c>CommandResult</c> return object.
#
# @param		string cmdPath								(required) The (absolute) path to the program to invoke.
# @param		string[] cmdArgs							(required) A list of arguments. Specify <c>None</c> if you do not want to have any arguments.
#															Please note that there is no shell to interprete these commands.
# @param		str|bytes[] dataToPipeAsStdIn				(optional) Either a string or binary data (or None) that should be passed on to the application invoked usint STDIN.
#															If string data is presented it is automatically encoded using UTF-8
# @param		str workingDirectory						(optional) If you specify a working directory here this function will change to this working directory
#															specified in <c>workingDirector</c> and return to the previous one after the command has been completed.
# @param		TextDataProcessingPolicy stdOutProcessing	(optional) If specified you can override defaults of the STDOUT preprocessing that can already be done by this function.
# @param		TextDataProcessingPolicy stdErrProcessing	(optional) If specified you can override defaults of the STDERR preprocessing that can already be done by this function.
#
# @return		CommandOutput								Returns an object that contains the exit status, (preprocessed) STDOUT and (preprocessed) STDERR data.
#
def invokeCmd1(
		cmdPath:str,
		cmdArgs:list,
		dataToPipeAsStdIn:typing.Union[str,bytes,bytearray] = None,
		workingDirectory:str = None,
		stdOutProcessing:TextDataProcessingPolicy = None,
		stdErrProcessing:TextDataProcessingPolicy = None,
	) -> CommandResult:

	stdOutProcessing = _common.DEFAULT_STDOUT_PROCESSING.override(stdOutProcessing)
	stdErrProcessing = _common.DEFAULT_STDERR_PROCESSING.override(stdErrProcessing)

	if stdErrProcessing is not None:
		assert isinstance(stdErrProcessing, TextDataProcessingPolicy)

	assert isinstance(cmdPath, str)
	if cmdArgs is not None:
		assert isinstance(cmdArgs, (list, tuple))

	if workingDirectory is not None:
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

		if _common.debugValve:
			_common.debugValve("================================================================================================================================")
			_common.debugValve("EXECUTING:", cmd)

		if dataToPipeAsStdIn:
			p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			p.stdin.write(dataToPipeAsStdIn)
		else:
			p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=None)
		(stdout, stderr) = p.communicate()

		# process stdout

		stdOutData = stdout.decode("utf-8")

		if _common.debugValve:
			_common.debugValve("STDOUT:")
			_common.debugValve(stdOutData)

		stdOutData = _common.processCmdOutput(stdOutData, stdOutProcessing)

		# process stderr

		stdErrData = stderr.decode("utf-8")

		if _common.debugValve:
			_common.debugValve("STDERR:")
			_common.debugValve(stdErrData)

		stdErrData = _common.processCmdOutput(stdErrData, stdErrProcessing)

		# ----

		if _common.debugValve != None:
			_common.debugValve("RETURN CODE:", p.returncode)

		return CommandResult(cmdPath, cmdArgs, stdOutData, stdErrData, p.returncode)

	finally:
		if returnToDirectory:
			os.chdir(returnToDirectory)
#






