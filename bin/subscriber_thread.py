#!/usr/bin/env python2
import os
import time
import json
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
		print "Received Sensor Config Update"
		try:
			sensor_json = json.loads(message.payload)['message']
			port_id = sensor_json['port_id']
			sensor_type = sensor_json['sensor_type']
			display_name = sensor_json['display_name']
			sample_rate = sensor_json['sample_rate']
			is_enabled = sensor_json['is_enabled']

			print "Port ID: ", port_id
			print "Sensor Type: ", sensor_type
			print "Display Name: ", display_name
			print "Sample Rate: ", sample_rate
			print "Is Enabled: ", is_enabled

			self.config_manager.update_sensor_config(port_id, sensor_type, display_name, sample_rate, is_enabled)

		except Exception as e:
			print "An error occured when receiving sensor updates"
			
			if hasattr(e, 'message') and message is not "":
				print e.message
