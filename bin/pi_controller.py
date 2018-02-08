#!/usr/bin/env python2
import os
import logging
from config_manager import config_manager
from lockfile_manager import lockfile_manager
from aws_controller import aws_controller

class pi_controller():
	# Load configurations and start threads
	def startup(self):
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

			# Test AWS connection, which calls back to main
			aws = aws_controller(config.aws_client_id, config.aws_endpoint, config.aws_root_ca_path, config.aws_certificate_path, config.aws_private_key_path)
			aws.test()

			# Start threads for publishing sensor data and listening for sensor configuration changes

		finally:
			lockfiles.lockfile_remove(lockfile_path)

pi = pi_controller()
pi.startup()
