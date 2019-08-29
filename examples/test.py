#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import os
import time
import traceback
import sys
import abc

import sh

import jk_simpleexec
#jk_simpleexec.simpleExecEnableDebugging("/tmp/jk_simpleexec.log")


print()
print("-- Executing a regular command --")
print()

result = jk_simpleexec.invokeCmd("/bin/ls", [ "/proc/1", "-l" ])
assert isinstance(result, jk_simpleexec.CommandResult)
result.dump()











