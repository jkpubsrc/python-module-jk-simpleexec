jk_simpleexec
=============

Introduction
------------

This python module provides a convenient interface to execute commands and catch their output.

Information about this module can be found here:

* [github.org](https://github.com/jkpubsrc/python-module-jk-simpleexec)
* [pypi.python.org](https://pypi.python.org/pypi/jk_simpleexec)

How to use this module
----------------------

### Import

To import this module use the following statement:

```python
import jk_simpleexec
```

### Example

Here is an example how to use this module:

```python
result = invokeCmd("/bin/ls", [ "/proc/1", "-l" ])
result.dump()
```

### Method(s)

```python
#
# Synchroneously invokes the specified command. Output of STDOUT and STDERR is caught.
#
# @param		string cmdPath				The (absolute) path to the program to invoke
# @param		string[] cmdArgs			A list of arguments. Specify <c>None</c> if you do not want to have any arguments.
# @param		string onErrorExceptionMsg	If you specify an error message here an exception is thrown. If <c>None</c> is specified
#											<c>None</c> will be returned and no exception will be thrown.
# @return		CommandOutput				Returns an object representing the results.
#
def invokeCmd(cmdPath, cmdArgs, bRemoveTrailingNewLinesFromStdOut = True, bRemoveTrailingNewLinesFromStdErr = True)
```

### CommandResult Object

```python
#
# The return code of the command after completion.
# @return		int			The return code.
#
@property
def returnCode(self)
```

```python
#
# The STDOUT output of the command.
# @return		string[]		The output split into seperate lines. This property always returns a list, never <c>None</c>.
#
@property
def stdOutLines(self)
```

```python
#
# The STDERR output of the command.
# @return		string[]		The output split into seperate lines. This property always returns a list, never <c>None</c>.
#
@property
def stdErrLines(self)
```

```python
#
# Returns <c>True</c> iff the return code is not zero or <c>STDERR</c> contains data
#
@property
def isError(self)
```

```python
#
# If the return code is not zero or <c>STDERR</c> contains data
# an exception is thrown using the specified exception message.
#
# @param		string exceptionMessage			The message for the exception raised.
# @return		CommandOutput					If no exception is raised the object itself is returned.
#
def raiseExceptionOnError(self, exceptionMessage)
```

```python
#
# Write all data to STDOUT. This method is provided for debugging purposes of your software.
#
def dump(self)
```

```python
#
# Returns a dictionary containing all data.
# @return		dict			Returns a dictionary with data registered at the following keys:
#								"cmd", "cmdArgs", "stdOut", "stdErr", "retCode"
#
def toJSON(self)
```

Contact Information
-------------------

This is Open Source code. That not only gives you the possibility of freely using this code it also
allows you to contribute. Feel free to contact the author(s) of this software listed below, either
for comments, collaboration requests, suggestions for improvement or reporting bugs:

* Jürgen Knauth: jknauth@uni-goettingen.de, pubsrc@binary-overflow.de

License
-------

This software is provided under the following license:

* Apache Software License 2.0



