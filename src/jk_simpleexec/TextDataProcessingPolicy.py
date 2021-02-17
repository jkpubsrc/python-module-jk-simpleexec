

import typing

import jk_prettyprintobj



#
# This class defines the defaults for postpocessing text data recieved. 
#
class TextDataProcessingPolicy(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self,
			bRemoveLeadingEmptyLines:bool = None,
			bRemoveTrailingEmptyLines:bool = None,
			bRightTrimLines:bool = None,
		):

		self.bRightTrimLines = bRightTrimLines
		self.bRemoveLeadingEmptyLines = bRemoveLeadingEmptyLines
		self.bRemoveTrailingEmptyLines = bRemoveTrailingEmptyLines
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dumpVarNames(self) -> list:
		return [
			"bRightTrimLines",
			"bRemoveLeadingEmptyLines",
			"bRemoveTrailingEmptyLines",
		]
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def clone(self):
		return TextDataProcessingPolicy(
			self.bRemoveLeadingEmptyLines,
			self.bRemoveTrailingEmptyLines,
			self.bRightTrimLines,
		)
	#

	def override(self, overrides):
		if overrides is None:
			return self

		assert isinstance(overrides, TextDataProcessingPolicy)

		ret = self.clone()
		for attrName in [ "bRemoveLeadingEmptyLines", "bRemoveTrailingEmptyLines", "bRightTrimLines" ]:
			v = getattr(overrides, attrName)
			if v is not None:
				setattr(ret, attrName, v)
		return ret
	#

#









