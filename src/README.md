jk_simpleexec
===============================

Introduction
--------------------------------

This python module provides a convenient interface to execute commands and catch their output. Additionally it provides convenient ways of running and killing other processes.

Information about this module can be found here:

* [github.org](https://github.com/jkpubsrc/python-module-jk-simpleexec)
* [pypi.python.org](https://pypi.python.org/pypi/jk_simpleexec)

How to use this module
--------------------------------

### Import

To import this module use the following statement:

```python
import jk_simpleexec
```

### Invoking a program: Example

Here is an example how to invoke a command:

```python
cmdResult = jk_simpleexec.invokeCmd1(
	cmdPath = "/usr/bin/ls",
	cmdArgs = [
		"-la",
	],
	dataToPipeAsStdIn = None,		# this is the default; listed here only for completeness;
	workingDirectory = "/",
)

cmdResult.dump()
```

This will internally use Python's `subprocess.Popen(..)` to run the specified program and receive it's output.

The data returned by `invokeCmd(..)` is a data container for the result.
For simplicity a `cmdResult.dump()` is invoked here in order to write all received information to STDOUT.
(In a real world scenario you will likely want to process some of that data.)

NOTE: There exists an older version of `jk_simpleexec.invokeCmd1(..)` named `jk_simpleexec.invokeCmd(..)`. This `invokeCmd1(..)` was implemented as a step to
overcome limitations of the `invokeCmd(..)` API. In the future please use the more recent version `invokeCmd1(..)` instead of `invokeCmd(..)`.
Likely `invokeCmd(..)` will be removed in future versions.

API
--------------------------------

### The `invokeCmd1(..)` function

```python
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
	) -> CommandResult
```

### The `CommandResult` object returned

`CommandResult` objects are returned if commands have been executed successfully. Classes of that type will provide a set of properties and methods.

NOTE: I use signatures similiar to C-style here as this way the required types for arguments can be understood more easily.

#### Properties

* `str commandPath` : Returns the path used for invoking the command.
* `str commandArguments` : Returns the arguments used for invoking the command.
* `int returnCode` : The return code of the command after completion.
* `list stdOutLines` : The STDOUT output of the command as a list of text lines.
* `list stdErrLines` : The STDERR output of the command as a list of text lines.
* `str stdOutStr` : The STDOUT output of the command as a single string.
* `str stdErrStr` : The STDERR output of the command as a single string.
* `TextData stdOut` : Direct access to the internal `TextData` object that manages the STDOUT output.
* `TextData stdErr` : Direct access to the internal `TextData` object that manages the STDERR output.
* `bool isError` : Returns `True` if either the return code is non-zero or `STDERR` contains some data.

### Methods

* `void dump(str prefix = None, callable printFunc = None)` : Write debugging data to STDOUT (if `printFunc` is `None`, or use the specified callable as a replacement for `print(..)`).
* `dict getStdOutAsJSON()` : Interpret the text data as JSON data and return it.
* `ElementTree getStdOutAsXML()` : Interpret the text data as XML and return an ElemenTree object.
* `* getStdOutAsLXML()` : Interpret the text data as an LXML tree object and return it. (Requires `lxml` to be installed.)
* `void raiseExceptionOnError(exceptionMessage:str, bDumpStatusOnError:bool = False)` : If the return code is no-zero or <c>STDERR</c> contains data an exception is thrown using the specified exception message.
* `dict toJSON()` : Convert the whole object to a JSON dictionary.

Contact Information
--------------------------------

This is Open Source code. That not only gives you the possibility of freely using this code it also
allows you to contribute. Feel free to contact the author(s) of this software listed below, either
for comments, collaboration requests, suggestions for improvement or reporting bugs:

* Jürgen Knauth: pubsrc@binary-overflow.de

License
--------------------------------

This software is provided under the following license:

* Apache Software License 2.0



