#!/usr/bin/env python2

# Represents a generic GrovePi sensor
def sensor:

	# Configures the sensor
	def __init__(self, port_id, sensor_type, display_name, sample_rate, is_enabled):
		self.port_id = port_id
		self.sensor_type = sensor_type
		self.display_name = display_name
		self.sample_rate = sample_rate
		self.is_enabled = is_enabled