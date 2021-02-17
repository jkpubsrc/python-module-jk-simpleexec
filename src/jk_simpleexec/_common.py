




from jk_cmdoutputparsinghelper.TextData import TextData

from .TextDataProcessingPolicy import TextDataProcessingPolicy
from ._DebugValveToFile import _DebugValveToFile





DEFAULT_STDOUT_PROCESSING = TextDataProcessingPolicy(True, True, True)
DEFAULT_STDERR_PROCESSING = TextDataProcessingPolicy(True, True, True)







debugValve = None

def enableDebugging(debuggingFilePath:str):
	global debugValve
	debugValve = _DebugValveToFile(debuggingFilePath)
#






def processCmdOutput(textData:str, policy:TextDataProcessingPolicy) -> TextData:
	textData = TextData(textData)

	if policy.bRightTrimLines:
		textData.lines.rightTrimAllLines()
	if policy.bRemoveLeadingEmptyLines:
		textData.lines.removeLeadingEmptyLines()
	if policy.bRemoveTrailingEmptyLines:
		textData.lines.removeTrailingEmptyLines()

	return textData
#













