#!/usr/bin/env python2
import logging
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

class aws_controller:

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
			self.client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
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
			print "Testing AWS client."
			print "Connecting..."
			self.client.connect()
			print "Sending 'Hello, World!' to test_topic..."
			self.client.publish("test_topic", "Hello, world!", 1)
			print "Unsubscribing from test_topic..."
			self.client.unsubscribe("test_topic")
			print "Disconnecting..."
			self.client.disconnect()
			print "Test complete."
		except Exception as e:
			print "Test failed."
			print "Please double check your configuration and ensure that you have a stable internet connection."

			if hasattr(e, 'message'):
				print "Error: ", e.message

			exit(1)