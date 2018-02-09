#!/usr/bin/env python2

# List of sensors and helper methods for accessing the sensors on the GrovePi
class sensor_array:

	# List of all sensors
	sensors = []

	def __init__(self):
		print "Initialising Sensor Array..."

	# Checks the list of sensors to find if any are scheduled to be read from.
	# If a sensor is ready to be read, its readings are sent to the payload list.
	# Once all of the sensors are read, the payload is returned
	def get_readings(self):
		payload = []
		
		# Read each sensor in the array
		for sensor in self.sensors:
			if sensor.ready():
				payload.append(sensor.read())
		
		return payload
