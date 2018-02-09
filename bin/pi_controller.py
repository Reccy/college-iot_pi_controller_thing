#!/usr/bin/env python2
import os
import time
import logging
from publisher_thread import publisher_thread
from subscriber_thread import subscriber_thread
from threading import Thread
from config_manager import config_manager
from lockfile_manager import lockfile_manager
from aws_controller import aws_controller

# Responsible for orchestrating the application startup process
class pi_controller():
	owns_lock = False
	is_listening = False
	is_publishing = False

	# Load configurations and start threads
	def startup(self):
		try:
			# Get file paths
			dir_path = os.path.dirname(os.path.realpath(__file__))
			lockfile_path = os.path.abspath(os.path.join(dir_path, "../lockfile"));
			
			lockfiles = lockfile_manager()

			# Check lockfile
			self.owns_lock = lockfiles.lockfile_write(lockfile_path)['success']
			if self.owns_lock == False:
				print "This application is already running. Exiting..."
				exit(0)

			# Setup configuration
			config = config_manager()
			config.load_aws()

			# Test AWS connection
			aws = aws_controller(config.aws_client_id, config.aws_endpoint, config.aws_root_ca_path, config.aws_certificate_path, config.aws_private_key_path)
			aws.test()

			# Start threads for publishing sensor data and listening for sensor configuration changes.
			# Also pass configured aws_controller instance to threads. 
			#print "Starting Subscriber Thread..."
			#sub = subscriber_thread()
			#sub_thread = Thread(target=sub.main)
			#sub_thread.start()

			print "Starting Publisher Thread..."
			pub = publisher_thread(aws)
			pub_thread = Thread(target=pub.main)
			pub_thread.start()

			print "Startup Complete."

			# Keeps the main thread alive
			while (True):
				time.sleep(1)

		# Cleanup
		finally:
			if self.owns_lock == True:
				lockfiles.lockfile_remove(lockfile_path)

pi = pi_controller()
pi.startup()
