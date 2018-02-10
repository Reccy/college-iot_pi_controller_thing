#!/usr/bin/env python2
import sys
import logging
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient, AWSIoTMQTTShadowClient

class aws_controller:

	# If the test is complete
	ready = False

	# If connected to AWS
	connected = False

	# Sets up the configuration for the AWS client
	def __init__(self, client_id, endpoint, root_ca_path, certificate_path, private_key_path):
		try:
			print "Initiating AWS client."
			print "Client ID: ", client_id
			print "Endpoint: ", endpoint
			print "Root CA Path", root_ca_path
			print "Certificate Path:", certificate_path
			print "Private Key Path:", private_key_path

			# Set class variables
			self.client_id = client_id
			self.endpoint = endpoint
			self.root_ca_path = root_ca_path
			self.certificate_path = certificate_path
			self.private_key_path = private_key_path

			# Configure the client
			self.client = AWSIoTMQTTClient(client_id)
			self.client.configureEndpoint(endpoint, 8883)
			self.client.configureCredentials(root_ca_path, private_key_path, certificate_path)
			self.client.configureDrainingFrequency(2)  # Draining: 2 Hz
			self.client.configureConnectDisconnectTimeout(10)  # 10 sec
			self.client.configureMQTTOperationTimeout(5)  # 5 sec

			# Configure logging
			logger = logging.getLogger("AWSIoTPythonSDK.core")
			logger.setLevel(logging.DEBUG)
			streamHandler = logging.StreamHandler()
			formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
			streamHandler.setFormatter(formatter)
			logger.addHandler(streamHandler)

			print "AWS client configured."
		except Exception as e:
			print "Error configuring AWS client: ", e
			exit(1)

	# Performs a self-test to ensure that the application can connect to AWS IoT Core
	def test(self):
		try:
			self.connected = False
			print "Testing AWS client."
			print "Connecting..."
			self.client.connect()
			print "Subscribing to test_topic..."
			self.client.subscribe("test_topic", 1, self.print_message)
			print "Sending 'Hello, World!' to test_topic..."
			self.client.publish("test_topic", "Hello, world!", 1)
			print "Unsubscribing from test_topic..."
			self.client.unsubscribe("test_topic")
			print "Disconnecting..."
			self.client.disconnect()
			print "Test complete."
			self.ready = True
		except Exception as e:
			print "Test failed."
			print "Please double check your configuration and ensure that you have a stable internet connection."

			if hasattr(e, 'message'):
				print "Error: ", e.message

			exit(1)

	# Connects the client to the network
	def connect(self):
		print "Connecting to AWS IoT Core..."
		self.client.connect()
		self.connected = True
		print "Connected."

	def disconnect(self):
		print "Disconnecting from AWS IoT Core..."
		self.client.disconnect()
		self.connected = False
		print "Disconnected."

	# Prints the message from a subscribe callback
	def print_message(self, client, userdata, message):
		print message

	# Publishes a payload to the passed in topic 
	def publish(self, topic, payload):
		print "DUMMY PUBLISH: ", payload, "TO", topic

	# Subscribes to the sensor_config channel with the passed in callback
	def subscribe_to_config_updates(self, callback):
		print "Subscribed to config updates."
		self.client.subscribe("sensor_config", 1, callback)
