


import typing
import os
import subprocess
import pwd
import signal





#
# Kill a process.
#
# @param	int|dict process			A processes, either as <c>int</c> (= process ID) or as <c>dict</c>
#										as provided by <c>jk_sysinfo.get_ps()</c>.
# @param	AbstractLogger log			A logger that will receive log messages.
# @return	bool						Returns <c>true</c> on success. <c>false</c> is returned if something went wrong.
#										(In that case error log messages might have been generated, but no detailed error
#										information is returned.)
#
def killProcess(process:typing.Union[int,dict], log) -> bool:
	assert isinstance(process, (int,dict))

	# ----

	if process is None:
		if log:
			log.notice("No processes to kill.")
		return True

	ret = True

	try:
		if isinstance(process, int):
			pid = process
		else:
			assert isinstance(process, dict)
			pid = process["pid"]
			assert isinstance(pid, int)

		if log:
			log.notice("Killing: " + str(pid))
		os.kill(pid, signal.SIGTERM)
	except Exception as ee:
		if log:
			log.error(ee)
		ret = False

	return ret
#



#
# Kill a set of processes (in the order they are presented).
#
# @param	int[]|dict[] processes		A list of processes, either as <c>int[]</c> of process IDs or as <c>dict[]</c>
#										as provided by <c>jk_sysinfo.get_ps()</c>.
# @param	AbstractLogger log			A logger that will receive log messages.
# @return	bool						Returns <c>true</c> on success. <c>false</c> is returned if something went wrong.
#										(In that case error log messages might have been generated, but no detailed error
#										information is returned.)
#
def killProcesses(processes:typing.Union[list, tuple], log) -> bool:
	assert isinstance(processes, (list, tuple))

	# ----

	if (processes is None) or (not processes):
		if log:
			log.notice("No processes to kill.")
		return True

	ret = True

	for process in processes:
		try:
			if isinstance(process, int):
				pid = process
			else:
				assert isinstance(process, dict)
				pid = process["pid"]
				assert isinstance(pid, int)

			if log:
				log.notice("Killing: " + str(pid))
			os.kill(pid, signal.SIGTERM)
		except Exception as ee:
			if log:
				log.error(ee)
			ret = False

	return ret
#



def _demote(user_uid, user_gid):

	def fn():
		os.setgid(user_gid)
		os.setuid(user_uid)
	#

	return fn

#

#
# Run a process as other user and wait until it terminates. No input or output is processed.
# Of course for this to work you should be user <c>root</c>.
#
# @param	str accountName			The name of the user account under which to execute the process.
# @param	str filePath			The path of the file to execute. This can be a bash script.
# @param	str[] arguments			(optional) A list of arguments for the program to execute.
# @param	AbstractLogger log		A logger that will receive log messages.
# @return	bool					Returns <c>true</c> on success. <c>false</c> is returned if something went wrong.
#									(In that case error log messages might have been generated, but no detailed error
#									information is returned.)
#
def runProcessAsOtherUser(accountName:str, filePath:str, args:typing.Union[list,tuple], log) -> bool:
	assert isinstance(accountName, str)
	assert accountName

	assert isinstance(filePath, str)
	assert filePath
	assert os.path.isfile(filePath)

	if args is None:
		args = []
	else:
		if isinstance(args, tuple):
			args = list(args)
		else:
			assert isinstance(args, list)

	assert log

	# ----

	if log:
		log.notice("Running " + repr(filePath) + " as " + repr(accountName) + "...")

	scriptDirPath = os.path.dirname(filePath)

	pw_record = pwd.getpwnam(accountName)
	accountName = pw_record.pw_name
	user_home_dir = pw_record.pw_dir
	uid = pw_record.pw_uid
	gid = pw_record.pw_gid

	currentUserID = os.getuid()
	if currentUserID != 0:
		if uid != currentUserID:
			raise Exception("Must be root to run processes as other user!")

	env = os.environ.copy()
	env["HOME"     ]  = user_home_dir
	env["LOGNAME"  ]  = accountName
	env["PWD"      ]  = scriptDirPath
	env["USER"     ]  = accountName

	ret = True

	try:
		process = subprocess.Popen(
			[ filePath ] + args,
			preexec_fn = _demote(uid, gid),
			cwd =  scriptDirPath,
			env = env,
		)
		exitCode = process.wait()

		if exitCode != 0:
			if log:
				log.error("Script " + repr(filePath) + " terminated with exit code: " + str(exitCode))
			ret = False
		else:
			if log:
				log.notice("Done running " + repr(filePath) + ".")

	except Exception as ee:
		if log:
			log.error(ee)
		ret = False

	return ret
#






