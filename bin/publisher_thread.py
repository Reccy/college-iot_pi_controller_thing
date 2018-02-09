#!/usr/bin/env python2
import os
import time
from sensor_array import sensor_array
from lockfile_manager import lockfile_manager

# Responsible for asynchronously sending sensor data to AWS
class publisher_thread:
	def __init__(self, aws):
		print "Configuring Publisher Thread..."
		self.aws_controller = aws

	def main(self):
		print "Publisher Thread Running..."

		# Setup lockfile manager
		lockfiles = lockfile_manager()
		dir_path = os.path.dirname(os.path.realpath(__file__))
		lockfile_path = os.path.abspath(os.path.join(dir_path, "../lockfile"));

		# Setup sensors
		sensors = sensor_array()

		# Main Thread Loop
		while (True):

			# Get any readings from the sensor array
			print "Checking for readings..."
			payload = sensors.get_readings()

			if len(payload) > 0:
				self.aws_controller.publish("test_topic",payload)
			
			# Check if the thread should keep alive
			if not lockfiles.lockfile_exists(lockfile_path, False):
				print "Stopping Publisher Thread"
				exit(0)

			# If the thread can be left alive, sleep for 0.5 seconds
			time.sleep(0.5)