#!/usr/bin/env python2
import os
from xml.dom import minidom
from sensor_array import sensor_array

# Responsible for saving and loading configuration information
class config_manager:

	def __init__(self, sensors):
		self.sensors = sensors

	# Loads the AWS config information
	def load_aws(self):
		try:
			# Get paths for files
			this_file_path = os.path.realpath(__file__)
			aws_file_abspath = os.path.abspath(os.path.join(this_file_path, "../../config/aws.config"))
			aws_file_path = os.path.join(os.path.realpath(aws_file_abspath), "../")

			# Read AWS data
			print "Reading AWS config file", aws_file_abspath
			self.aws_file = minidom.parse(aws_file_abspath)
			self.aws_client_id = self.aws_file.getElementsByTagName("client_id")[0].firstChild.data
			self.aws_endpoint = self.aws_file.getElementsByTagName("endpoint")[0].firstChild.data
			self.aws_root_ca_path = os.path.abspath(os.path.join(aws_file_path, self.aws_file.getElementsByTagName("root_ca_path")[0].firstChild.data))
			self.aws_certificate_path = os.path.abspath(os.path.join(aws_file_path, self.aws_file.getElementsByTagName("certificate_path")[0].firstChild.data))
			self.aws_private_key_path = os.path.abspath(os.path.join(aws_file_path, self.aws_file.getElementsByTagName("private_key_path")[0].firstChild.data))
		except Exception as e:
			print "Error when reading AWS config data"

			if hasattr(e, 'message') and e.message is not "":
					print e.message

	# Loads the sensor config information
	def load_sensors(self):
		try:
			# Get paths for files
			this_file_path = os.path.realpath(__file__)
			sensor_file_abspath = os.path.abspath(os.path.join(this_file_path, "../../config/sensors.config"))
			sensor_file_path = os.path.join(os.path.realpath(sensor_file_abspath), "../")

			if not os.path.exists(sensor_file_abspath):
				print "Not loading sensor config information from local file. File does not exist."
				return

			# Read the file
			print "Reading sensor config from local file."
			xml_doc = minidom.parse(sensor_file_abspath)

			# Get list of sensor nodes
			sensors_list = xml_doc.getElementsByTagName("sensor")

			# Configure each node in the list
			for sensor_node in sensors_list:
				sensor_child_nodes = sensor_node.childNodes
				new_port_id = sensor_child_nodes[0].childNodes[0].nodeValue
				new_sensor_type = sensor_child_nodes[1].childNodes[0].nodeValue
				new_display_name = sensor_child_nodes[2].childNodes[0].nodeValue
				new_sample_rate = sensor_child_nodes[3].childNodes[0].nodeValue
				new_is_enabled = sensor_child_nodes[4].childNodes[0].nodeValue
				self.sensors.update_sensor(new_port_id, new_sensor_type, new_display_name, new_sample_rate, new_is_enabled)

			print "Finished configuring sensors."

		except Exception as e:
			print "Error when reading sensor config data."

			if hasattr(e, 'message') and e.message is not "":
					print e.message

	# Updates the local sensor configuration by creating or appending any records sorted by the port_id
	def update_sensor_config(self, port_id, sensor_type, display_name, sample_rate, is_enabled):
		# Get paths for files
		this_file_path = os.path.realpath(__file__)
		sensor_file_abspath = os.path.abspath(os.path.join(this_file_path, "../../config/sensors.config"))
		sensor_file_path = os.path.join(os.path.realpath(sensor_file_abspath), "../")

		# Create the config file if it does not already exist
		if not os.path.exists(sensor_file_abspath):
			"Creating Sensor config file", sensor_file_abspath
			try:
				xml_doc = minidom.Document()
				xml_doc.appendChild(xml_doc.createElement("sensors"))
				xml_str = xml_doc.toxml()

				with open(sensor_file_abspath, "w") as xml_file:
					xml_file.write(xml_str)
					xml_file.close()

				print "Sensor config file created"

			except Exception as e:
				print "Error when creating the Sensor config file"

				if hasattr(e, 'message') and e.message is not "":
					print e.message

		# Write config file changes
		print "Writing changes to Sensor config file"
		try:
			sensor_file = minidom.parse(sensor_file_abspath)

			sensors_node = sensor_file.getElementsByTagName("sensors")[0]

			# Create and set the elements
			new_sensor = sensor_file.createElement("sensor")
			port_id_node = sensor_file.createElement("port_id")
			port_id_node.appendChild(sensor_file.createTextNode(str(port_id)))
			sensor_type_node = sensor_file.createElement("sensor_type")
			sensor_type_node.appendChild(sensor_file.createTextNode(str(sensor_type)))
			display_name_node = sensor_file.createElement("display_name")
			display_name_node.appendChild(sensor_file.createTextNode(str(display_name)))
			sample_rate_node = sensor_file.createElement("sample_rate")
			sample_rate_node.appendChild(sensor_file.createTextNode(str(sample_rate)))
			is_enabled_node = sensor_file.createElement("is_enabled")
			is_enabled_node.appendChild(sensor_file.createTextNode(str(is_enabled)))

			# Append child nodes to the new sensor node
			new_sensor_node = sensors_node.appendChild(new_sensor)
			new_sensor_node.appendChild(port_id_node)
			new_sensor_node.appendChild(sensor_type_node)
			new_sensor_node.appendChild(display_name_node)
			new_sensor_node.appendChild(sample_rate_node)
			new_sensor_node.appendChild(is_enabled_node)

			# Check for existing Port ID and overwrite it
			port_id_nodes = sensor_file.getElementsByTagName("port_id")

			existing_port_nodes = []

			for node in port_id_nodes:
				if node.firstChild.nodeValue == port_id:
					existing_port_nodes.append(node)

			if len(existing_port_nodes) is not 0:
				existing_sensor = existing_port_nodes[0].parentNode
				sensors_node.replaceChild(new_sensor, existing_sensor)
			else:
				sensors_node.appendChild(new_sensor)

			# Write the changes to file
			xml_str = sensor_file.toxml()

			with open(sensor_file_abspath, "w") as xml_file:
				xml_file.write(xml_str)
				xml_file.close()

			# Update the sensor array in-memory
			self.sensors.update_sensor(port_id, sensor_type, display_name, sample_rate, is_enabled)

		except Exception as e:
			print "Error when updating the Sensor config file"

			if hasattr(e, 'message') and e.message is not "":
				print e.message
