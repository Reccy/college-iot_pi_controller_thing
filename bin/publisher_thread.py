#!/usr/bin/env python2
import os
import time
from sensor_array import sensor_array
from lockfile_manager import lockfile_manager

# Responsible for asynchronously sending sensor data to AWS
class publisher_thread:
	def __init__(self, aws_controller, config_manager, sensors):
		print "Configuring Publisher Thread..."
		self.aws_controller = aws_controller
		self.config_manager = config_manager
		self.sensors = sensors

	def main(self):
		print "Publisher Thread Running..."

		# Setup lockfile manager
		lockfiles = lockfile_manager()
		dir_path = os.path.dirname(os.path.realpath(__file__))
		lockfile_path = os.path.abspath(os.path.join(dir_path, "../lockfile"));

		# Main Thread Loop
		while (True):

			# Get any readings from the sensor array
			payload = self.sensors.get_readings()

			for p in payload:
				self.aws_controller.publish("readings", p)

			# Check if the thread should keep alive
			if not lockfiles.lockfile_exists(lockfile_path, False):
				print "Stopping Publisher Thread"
				exit(0)
