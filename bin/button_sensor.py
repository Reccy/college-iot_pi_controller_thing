#!/usr/bin/env python2
import grovepi
from sensor import sensor

# Concrete implementation of a sensor as a button.
class button_sensor(sensor):

	def read(self):
		reading = grovepi.digitalRead(self.port_id)
		print "[ PORT ", self.port_id, "] Button Read ->", reading
		return reading
