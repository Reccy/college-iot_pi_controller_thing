#!/usr/bin/env python2
from sensor import sensor
from button_sensor import button_sensor
from rangefinder_sensor import rangefinder_sensor
from sound_sensor import sound_sensor
from temperature_humidity_sensor import temperature_humidity_sensor

# List of sensors and helper methods for accessing the sensors on the GrovePi
class sensor_array:

	# List of all sensors
	sensors = []

	# Updates sensor array based on passed in data
	def update_sensor(self, port_id, sensor_type, display_name, sample_rate, is_enabled):

		# If is_enabled is a string, make sure it's converted to the correct boolean value
		if type(is_enabled) is str or type(is_enabled) is unicode:
			if is_enabled == "True" or is_enabled == "true":
				is_enabled = True
			else:
				is_enabled = False

		# Remove any sensors on the port_id
		for sensor in self.sensors:
			if sensor.port_id == str(port_id):
				print "Replacing sensor on port", port_id 
				self.sensors.remove(sensor)

		# Add implemented sensor to list of sensors
		if sensor_type == "button":
			print "Configuring button on port", port_id
			self.sensors.append(button_sensor(port_id, sensor_type, display_name, int(sample_rate), is_enabled, self.get_real_port_id(port_id, True)))
		elif sensor_type == "rangefinder":
			print "Configuring rangefinder on port", port_id
			self.sensors.append(rangefinder_sensor(port_id, sensor_type, display_name, int(sample_rate), is_enabled, self.get_real_port_id(port_id, True)))
		elif sensor_type == "sound":
			print "Configuring sound sensor on port", port_id
			self.sensors.append(sound_sensor(port_id, sensor_type, display_name, int(sample_rate), is_enabled, self.get_real_port_id(port_id, False)))
		elif sensor_type == "temperature_humidity":
			print "Configuring temperature and humidty sensor on port", port_id
			self.sensors.append(temperature_humidity_sensor(port_id, sensor_type, display_name, int(sample_rate), is_enabled, self.get_real_port_id(port_id, True)))
		else:
			print "Sensor not implemented:", sensor_type

	# Returns the mapped integer value of the port_id string and if the sensor is analog/digital
	# NOTE: Only A prefix ports can read digital signals.
	def get_real_port_id(self, port_id, is_digital):
		if is_digital:
			if port_id == "A0":
				return 14
			if port_id == "A1":
				return 15
			if port_id == "A2":
				return 16
			if port_id == "D2":
				return 2
			if port_id == "D3":
				return 3
			if port_id == "D4":
				return 4
			if port_id == "D5":
				return 5
			if port_id == "D6":
				return 6
			if port_id == "D7":
				return 7
			if port_id == "D8":
				return 8
			else:
				print "ERROR: Digital port", port_id, "does not exist!"
		else:
			if port_id == "A0":
				return 0
			if port_id == "A1":
				return 1
			if port_id == "A2":
				return 2
			else:
				print "ERROR: Analog port", port_id, "does not exist!"

		return -1

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
