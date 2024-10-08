


__author__ = "Jürgen Knauth"
__version__ = "0.2024.8.11"



from .CommandResult import CommandResult
from .TextDataProcessingPolicy import TextDataProcessingPolicy
from ._DebugValveToFile import _DebugValveToFile
from ._common import enableDebugging, DEFAULT_STDOUT_PROCESSING, DEFAULT_STDERR_PROCESSING, processCmdOutput
from .simpleexec import invokeCmd, invokeCmd1, invokeCmd2
from .invoke_utils import runCmd

import os
if os.name == "posix":
	from .WhereIs import whereis, whereisE





