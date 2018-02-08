#!/usr/bin/env python2
import os
from xml.dom import minidom

class config_manager:
	def load_aws(self):
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
