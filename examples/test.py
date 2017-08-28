#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import os
import time
import traceback
import sys
import abc

import sh

from jk_simpleexec import invokeCmd, simpleExecEnableDebugging
simpleExecEnableDebugging("/tmp/jk_simpleexec.log")


print()
print("-- Executing a regular command --")
print()

result = invokeCmd("/bin/ls", [ "/proc/1", "-l" ])
result.dump()











