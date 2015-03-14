import socket
import constants
import pdb
import os

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
	raw = s.recv(constants.LIST_INIT_PACKET_LENGTH)
	try:
		num_files = int(raw.rstrip('-'))
	except ValueError:
		print "Invalid Server Response: "
		print raw
		return

	if num_files == 0:
		print "No files currently on the network\n"
	else:
		print "There are " + str(num_files) + " on the network\n"
		for i in xrange(num_files):
			file_name = s.recv(constants.LIST_FILE_PACKET_LENGTH)
			print file_name.strip('-')

def download_file(s, user_input, my_udp):
	fileinput = user_input.split(' ')

	if len(fileinput) < 3:
		print "USAGE: download target dest"
	else:
		s.sendall("download " + fileinput[1])
		reply = s.recv(constants.GEN_PACKET_LENGTH) #ip address
		my_udp.send_request(fileinput[1], reply)
