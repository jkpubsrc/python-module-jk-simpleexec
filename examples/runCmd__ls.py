#!/usr/bin/python3




import jk_simpleexec




cmdResult = jk_simpleexec.runCmd(
	c = None,
	command = "cd / ; ls -la"
)

cmdResult.dump()










