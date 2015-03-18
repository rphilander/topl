#! /usr/bin/python

from Queue import Queue
from threading import Thread

import shlex
import sys
import traceback


# ########################
# stdout

stdout_outbound = Queue() # items: (ident, val)
stdout_inbound = Queue() # items: (ident, success)

class StdoutMessage(object):
	def __init__(self, ident, val, shutdown):
		self.ident = ident
		self.val  = val
		self.shutdown = shutdown

class StdoutResponse(object):
	def __init__(self, ident, success):
		self.ident = ident
		self.success = success

def stdout():
	while True:
		message = stdout_outbound.get()
		if message.shutdown:
			break
		stdout_outbound.task_done()
		sys.stdout.write(unescape(message.val))
		response = StdoutResponse(message.ident, True)
		stdout_inbound.put(response)

#
##########################



##########################
# stdin

stdin_outbound = Queue() # items: ident
stdin_inbound = Queue() # items: (ident, val)

class StdinMessage(object):
	def __init__(self, ident, shutdown):
		self.ident = ident
		self.shutdown = shutdown

class StdinResponse(object):
	def __init__(self, ident, val):
		self.ident = ident
		self.val =val

def stdin():
	while True:
		message = stdin_outbound.get()
		if message.shutdown:
			break
		stdin_outbound.task_done()
		val = sys.stdin.readline()
		stdin_inbound.put(StdinResponse(ident, val))

#
##########################


##########################
# helpers

def unescape(s):
	return s.replace("\\n", "\n")

# 
##########################





##########################
# main

# create threads
stdout_thread = Thread(target=stdout)
stdin_thread = Thread(target=stdin)

# run threads
stdout_thread.start()
stdin_thread.start()

# do computations
try:
	filename = sys.argv[1]
	codefile = open(filename)
	for line in codefile.readlines():
		if line[0] == '#':
			continue
		fields = shlex.split(line)
		num = fields[0]
		command = fields[1]
		seen_pipe = False
		args = []
		dependencies = []
		for fld in fields[2:]:
			if seen_pipe:
				dependencies.append(fld)
			else:
				args.append(fld)
		if command == "@stdin":
			stdin_outbound.put(StdinMessage(0, False))
		elif command == "@stdout":
			stdout_outbound.put(StdoutMessage(0, args[0], False))

except:
	e = sys.exc_info()[0]
  	sys.stderr.write(traceback.format_exc())

# shutdown threads
stdin_outbound.put(StdinMessage(0, True))
stdout_outbound.put(StdoutMessage(0, "", True))

stdin_thread.join()
stdout_thread.join()

#
##########################









