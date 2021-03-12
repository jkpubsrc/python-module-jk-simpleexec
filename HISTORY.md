
* 2021-02-17
	* Refactored this module as a) other modules have evolved and b) more functionality needs to be added in this module here.
	* Removing dependency to `lxml` as using `lxml` should be optional
	* Improved debugging using `jk_prettyprintobj` instead of the old custom code
	* Added `invokeCmd1()` as a first step to migrate to a better API
	* Added `runCmd()` to even more simplify running commands (requires `fabric`)
	* Added documentation
	* Improved: `raiseExceptionOnError()`

* 2021-03-12
	* Improved `runCmd()` to not throw an unexpected exception in fabric



