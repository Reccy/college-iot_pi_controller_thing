#!/usr/bin/env python2
import json
import grovepi
from sensor import sensor

# Concrete implementation of a sensor as a potentiometer sensor.
class potentiometer_sensor(sensor):

	def read(self):
		reading = grovepi.analogRead(self.real_port_id)

		# Source: http://wiki.seeed.cc/Grove-Rotary_Angle_Sensor/
		# Reference voltage of ADC if 5v
		adc_ref = 5

		# Vcc of the grove interface is normally 5v
		grove_vcc = 5

		# Full value of the rotary angle is 300 degrees, as per it's specs (0 to 300)
		full_angle = 300

		# Calculate voltage
		voltage = round((float)(reading) * adc_ref / 1023, 2)

		# Calculate rotation in degrees (0 to 300)
		degrees = round((voltage * full_angle) / grove_vcc, 2)

		# Set reading to meaningful value (rotation)
		reading = degrees

		print "[ PORT ", self.port_id, ", RATE", self.sample_rate,"] Potentiometer Sensor Read ->", reading
		payload = json.dumps({ "sensor_type": "potentiometer", "port_id": self.port_id, "reading": str(reading).encode('utf8') })
		return str(payload)
