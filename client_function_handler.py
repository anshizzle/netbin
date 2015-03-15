import socket
import constants
import pdb
import os
from util import *
from netbin_udp import *
# User made an upload command
# If length is less than 2, user did not add a file name.
#
def upload(s, user_input):
	fileinput = user_input.split(' ')
	if len(fileinput) < 2:
		print "USAGE: upload filename"
	else:
		if(os.path.isfile(fileinput[1])):
			s.sendall("upload "+fileinput[1])
			reply = s.recv(constants.GEN_PACKET_LENGTH)
			print reply
		else:
			print constants.INVALID_FILE_UPLOAD

def list(s):
	s.sendall("list")	

	raw = s.recv(constants.GEN_PACKET_LENGTH)
	list_data = raw.split(constants.LIST_ITEM_DELIMITER)

	try:
		num_files = int(list_data.pop(0))
	except ValueError:
		printDebug("could not parse file count", "c")
		printDebug("received data was " + raw, "c")
		return


	if num_files == 0:
		print constants.NO_FILES_STRING
	else:
		count = 0
		print constants.list_file_num_string(num_files)

		s.settimeout(None)
		while count < num_files:
			if not list_data or list_data[0] == "":
				raw = s.recv(constants.GEN_PACKET_LENGTH)
				list_data = raw.split(constants.LIST_ITEM_DELIMITER)


			file_name = list_data.pop(0)
			print file_name
			count += 1




def download_file(s, user_input, my_udp):
	fileinput = user_input.split(' ')

	if len(fileinput) < 3:
		print "USAGE: download target dest"
	else:
		s.sendall("download " + fileinput[1])
		reply = s.recv(constants.GEN_PACKET_LENGTH) #Reply is either the IP address or an error.
		if not reply.startswith("ERROR"):
			my_udp.send_request(fileinput[1], fileinput[2], reply)
		else:
			print reply
