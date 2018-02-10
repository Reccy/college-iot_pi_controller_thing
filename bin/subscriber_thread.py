#!/usr/bin/env python2
import os
import time
from lockfile_manager import lockfile_manager

# Thread responsible for listening for any sensor configuration changes from AWS
class subscriber_thread:
	def __init__(self, aws_controller, config_manager):
		print "Configuring Subscriber Thread..."
		self.aws_controller = aws_controller
		self.config_manager = config_manager

	def main(self):
		print "Subscriber Thread Started!"

		# Setup lockfile manager
		lockfiles = lockfile_manager()
		dir_path = os.path.dirname(os.path.realpath(__file__))
		lockfile_path = os.path.abspath(os.path.join(dir_path, "../lockfile"));

		# Subscribe to any changes with the sensor configuration
		self.aws_controller.subscribe_to_config_updates(self.handle_config_updates)

		while (True):

			# Check if the thread should keep alive
			if not lockfiles.lockfile_exists(lockfile_path, False):
				print "Stopping Subscriber Thread"
				exit(0)

	# Handles any updates to the device shadow
	def handle_config_updates(self, client, userdata, message):
		print "Config Updated"
		print message.payload
