
import os
import subprocess
import invoke
import typing
import time

from . import _common as _common
from .CommandResult import CommandResult
from .TextDataProcessingPolicy import TextDataProcessingPolicy

try:
	from fabric import Connection
except ImportError as ee:
	pass







#
# Run a command locally or remotely.
# If a "cat <file>" is to be invoked *and* this is to be invoked locally, this method will detect this. In that case instead of running "cat" it will fall back to a regular file read
# for efficiency. Therefore you can access data on local and remote systems in a uniform way without spending too much thoughts on efficiency.
#
# @param		fabric.Connection c				(optional) Provide a fabric connection here if you want to run a command remotely.
#												If you specify <c>None</c> here the command will be run locally.
# @param		str command						(required) The command to run. Please note that this command will be interpreted by a shell.
# @param		bool failOnNonZeroExitCode		(optional) Raises an exception if the last command executed returned with a non-zero exit code.
#
#
def runCmd(
		c,
		command:str,
		stdOutProcessing:TextDataProcessingPolicy = None,
		stdErrProcessing:TextDataProcessingPolicy = None,
		failOnNonZeroExitCode:bool = True,
	) -> CommandResult:

	stdOutProcessing = _common.DEFAULT_STDOUT_PROCESSING.override(stdOutProcessing)
	stdErrProcessing = _common.DEFAULT_STDERR_PROCESSING.override(stdErrProcessing)

	# execute command locally

	if c is None:
		if command.startswith("cat "):
			filePath = command[4:]

			if _common.debugValve:
				_common.debugValve("Using standard file reading for command: " + repr(command))

			if os.path.isfile(filePath):
				with open(filePath, "r") as f:
					return f.read(), "", 0
			else:
				raise Exception("No such file: " + repr(filePath))

		if _common.debugValve:
			_common.debugValve("Invoking via subprocess: " + repr(command))

		tStart = time.time()
		p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		binStdOut, binStdErr = p.communicate()
		tDuration = time.time() - tStart
		stdOut = binStdOut.decode("utf-8")
		stdErr = binStdErr.decode("utf-8")

		if _common.debugValve:
			_common.debugValve("exit status:", p.returncode)
			_common.debugValve("stdout:")
			for line in stdOut.split("\n"):
				_common.debugValve("\t" + repr(line))
			_common.debugValve("stderr:")
			for line in stdErr.split("\n"):
				_common.debugValve("\t" + repr(line))

		if failOnNonZeroExitCode and p.returncode > 0:
			raise Exception("Command failed with exit code " + str(p.returncode) + ": " + repr(command))

		stdOut = _common.processCmdOutput(stdOut, stdOutProcessing)
		stdErr = _common.processCmdOutput(stdErr, stdErrProcessing)

		return CommandResult(command, None, stdOut, stdErr, p.returncode, tDuration)

	# execute command remotely with fabric

	if (c.__class__.__name__ == "Connection") and (c.__class__.__module__ in [ "fabric", "fabric.connection" ]):
		if _common.debugValve:
			_common.debugValve("Invoking via fabric: " + repr(command))

		tStart = time.time()
		try:
			r = c.run(command, hide=True)
		except invoke.exceptions.UnexpectedExit as ee:
			r = ee.result
		tDuration = time.time() - tStart

		if _common.debugValve:
			_common.debugValve("exit status:", r.exited)
			_common.debugValve("stdout:")
			for line in r.stdout.split("\n"):
				_common.debugValve("\t" + repr(line))
			_common.debugValve("stderr:")
			for line in r.stderr.split("\n"):
				_common.debugValve("\t" + repr(line))

		if failOnNonZeroExitCode and r.exited > 0:
			raise Exception("Command failed with exit code " + str(r.exited) + ": " + repr(command))

		stdOut = _common.processCmdOutput(r.stdout, stdOutProcessing)
		stdErr = _common.processCmdOutput(r.stderr, stdErrProcessing)

		return CommandResult(command, None, stdOut, stdErr, r.exited, tDuration)

	# error

	raise Exception("Sorry, I don't know about " + repr(c.__class__) + " objects for parameter c.")
#












