#!/usr/bin/env python2
import time

# Represents a generic GrovePi sensor
class sensor:

	last_read_time = 0

	# Configures the sensor
	def __init__(self, port_id, sensor_type, display_name, sample_rate, is_enabled, real_port_id):
		self.port_id = port_id
		self.sensor_type = sensor_type
		self.display_name = display_name
		self.sample_rate = sample_rate
		self.is_enabled = is_enabled
		self.real_port_id = real_port_id

	# Sets the last_read_time to now.
	# Could be put into the read() function as an abstract class or something, but polymorphism in Python is a nightmare
	def update_last_read_time(self):
		self.last_read_time = (int(time.time()))

	# Returns true if the time since the last read time is greater than the sample rate
	def ready(self):

		# -1 to account for integer ceil conversion
		return ((int(time.time()) + 1) > self.last_read_time + self.sample_rate)
