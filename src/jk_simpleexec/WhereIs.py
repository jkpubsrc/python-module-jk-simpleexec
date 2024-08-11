

import typing

from .simpleexec import invokeCmd2




def whereis(programName:str) -> typing.Union[str,None]:
	assert isinstance(programName, str)
	assert programName

	# ----

	r = invokeCmd2(
		cmdPath="whereis",
		cmdArgs=[ "-b", programName ],
	)
	assert r.returnCode == 0
	line = r.stdOutLines[0]
	pos = line.index(":")
	s = line[pos+1:].strip()
	if not s:
		return None
	paths = s.split(" ")
	return paths[0]
#



def whereisE(programName:str) -> typing.Union[str,None]:
	path = whereis(programName)
	if not path:
		raise Exception("Not found: " + repr(programName))
	return path
#











