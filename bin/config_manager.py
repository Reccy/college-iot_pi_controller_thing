#!/usr/bin/env python2
import os
from xml.dom import minidom

class config_manager:

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
			print "Fatal error when reading AWS config data"

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
				xml_str = xml_doc.toprettyxml()

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
				print node.firstChild.nodeValue
				if node.firstChild.nodeValue == port_id:
					existing_port_nodes.append(node)

			print "Found existing port nodes: ", len(existing_port_nodes)

			if len(existing_port_nodes) is not 0:
				existing_sensor = existing_port_nodes[0].parentNode
				sensors_node.replaceChild(new_sensor, existing_sensor)
			else:
				sensors_node.appendChild(new_sensor)

			# Write the changes to file
			xml_str = sensor_file.toprettyxml()

			with open(sensor_file_abspath, "w") as xml_file:
				xml_file.write(xml_str)
				xml_file.close()

		except Exception as e:
			print "Error when updating the Sensor config file"

			if hasattr(e, 'message') and e.message is not "":
				print e.message