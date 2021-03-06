#!/usr/bin/env python2
import json
import grovepi
from sensor import sensor

# Concrete implementation of a sensor as a button.
class button_sensor(sensor):

	def read(self):
		reading = grovepi.digitalRead(self.real_port_id)
		print "[ PORT ", self.port_id, ", RATE", self.sample_rate,"] Button Read ->", reading
		payload = json.dumps({ "sensor_type": "button", "port_id": self.port_id, "reading": str(reading).encode('utf8') })
		return str(payload)
