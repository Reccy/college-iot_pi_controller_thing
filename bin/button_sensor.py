#!/usr/bin/env python2
import grovepi
from sensor import sensor

# Concrete implementation of a sensor as a button.
class button_sensor(sensor):

	def read(self):
		print "DIGITAL READ, RETURNING..."
		return grovepi.digitalRead(self.port_id)
