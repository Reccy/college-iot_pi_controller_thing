#!/usr/bin/env python2
import os
from config_manager import config_manager
from lockfile_manager import lockfile_manager

# Load configurations and start threads
def main():

	try:
		# Get file paths
		dir_path = os.path.dirname(os.path.realpath(__file__))
		lockfile_path = os.path.abspath(os.path.join(dir_path, "../lockfile"));
		
		lockfiles = lockfile_manager()

		# Check lockfile
		if lockfiles.lockfile_write(lockfile_path) == False:
			print "This application is already running. Exiting..."
			exit(0)

		# Setup configuration
		config = config_manager()
		config.load_aws()
	finally:
		lockfiles.lockfile_remove(lockfile_path)

main()
