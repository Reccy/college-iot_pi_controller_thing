#!/usr/bin/env python2
import os
import time
from lockfile_manager import lockfile_manager

# Thread responsible for listening for any sensor configuration changes from AWS
class subscriber_thread:
	def __init__(self):
		print "Subscriber Thread Instantiated!"

	def main(self):
		print "Subscriber Thread Started!"

		# Setup lockfile manager
		lockfiles = lockfile_manager()
		dir_path = os.path.dirname(os.path.realpath(__file__))
		lockfile_path = os.path.abspath(os.path.join(dir_path, "../lockfile"));

		while (True):
			print "Subscriber Thread Running!"
			time.sleep(10)
			
			# Check if the thread should keep alive
			if not lockfiles.lockfile_exists(lockfile_path, False):
				print "Stopping Subscriber Thread"
				exit(0)
