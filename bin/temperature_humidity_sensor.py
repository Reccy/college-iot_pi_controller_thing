#!/usr/bin/env python2
import json
import grovepi
from sensor import sensor

# Concrete implementation of a sensor as a temperature and humidity sensor.
class temperature_humidity_sensor(sensor):

	def read(self):
		[ temperature, humidity ] = grovepi.dht(self.real_port_id, 0)
		reading = json.dumps({"temperature": str(temperature).encode('utf8'), "humidity": str(humidity).encode('utf8')})
		print "[ PORT ", self.port_id, ", RATE", self.sample_rate,"] Temperature and Humidity Sensor Read ->", reading
		payload = json.dumps({ "sensor_type": "temperature_humidity", "port_id": self.port_id, "reading": str(reading).encode('utf8') })
		return str(payload)
