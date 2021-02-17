#!/usr/bin/python3




import jk_utils
import jk_simpleexec
import jk_pwdinput

from fabric import Connection





REMOTE_HOST = "127.0.0.1"
REMOTE_PORT = 22
REMOTE_LOGIN = jk_utils.users.lookup_username()
REMOTE_PASSWORD = jk_pwdinput.readpwd("Password for " + REMOTE_LOGIN + "@" + REMOTE_HOST + ": ")
c = Connection(host=REMOTE_HOST, user=REMOTE_LOGIN, port=REMOTE_PORT, connect_kwargs={"password": REMOTE_PASSWORD})





cmdResult = jk_simpleexec.runCmd(
	c = c,
	command = "cd / ; ls -la"
)

cmdResult.dump()

c.close()








