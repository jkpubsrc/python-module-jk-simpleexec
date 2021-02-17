#!/usr/bin/python3




import jk_simpleexec




cmdResult = jk_simpleexec.invokeCmd1(
	cmdPath = "/foo/bar/foobar",
	cmdArgs = [
	],
	bRemoveTrailingNewLinesFromStdOut = True,			# this is the default
	bRemoveTrailingNewLinesFromStdErr = True,			# this is the default
	dataToPipeAsStdIn = None,							# this is the default
	workingDirectory = "/",
)

cmdResult.dump()










