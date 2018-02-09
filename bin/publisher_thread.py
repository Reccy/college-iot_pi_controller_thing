#!/usr/bin/env python2
import os
import time
from lockfile_manager import lockfile_manager

# Responsible for asynchronously sending sensor data to AWS
class publisher_thread:
	def __init__(self):
		print "Publisher Thread Instantiated!"

	def main(self):
		print "Publisher Thread Started!"

		# Setup lockfile manager
		lockfiles = lockfile_manager()
		dir_path = os.path.dirname(os.path.realpath(__file__))
		lockfile_path = os.path.abspath(os.path.join(dir_path, "../lockfile"));

		while (True):
			print "Publisher Thread Running!"
			time.sleep(1)
			
			# Check if the thread should keep alive
			if not lockfiles.lockfile_exists(lockfile_path, False):
				print "Stopping Publisher Thread"
				exit(0)