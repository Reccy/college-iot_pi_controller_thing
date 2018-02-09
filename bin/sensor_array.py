#!/usr/bin/env python2
from sensor import sensor
from button_sensor import button_sensor

# List of sensors and helper methods for accessing the sensors on the GrovePi
class sensor_array:

	# List of all sensors
	sensors = []

	def __init__(self):
		print "Initialising Sensor Array..."
		self.sensors.append(button_sensor(6,"button","A Button",5,True))

	# Checks the list of sensors to find if any are scheduled to be read from.
	# If a sensor is ready to be read, its readings are sent to the payload list.
	# Once all of the sensors are read, the payload is returned
	def get_readings(self):
		payload = []
		
		# Read each sensor in the array
		for sensor in self.sensors:
			if sensor.is_enabled and sensor.ready():
				sensor.update_last_read_time()
				payload.append(sensor.read())
		
		return payload
