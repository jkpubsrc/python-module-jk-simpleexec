
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

* 2021-04-12
	* Added convenience methods to `CommandResult`
	* Improved `invokeCmd1()` to support logging

* 2021-12-14
	* Set `invokeCmd1()` as deprecated.
	* Replaced `invokeCmd1()` by `invokeCmd2()` to have an API that is more friendly to future changes.

* 2022-03-01
	* Added duration time measurement

* 2022-03-07
	* Improved argument type checking

* 2022-08-07
	* Improved: Type hints

