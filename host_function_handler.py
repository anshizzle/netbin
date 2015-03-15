import socket
import constants
from util import *


## Returns a pair SUCCESS, file_list
# Success is 1 if the file was added successfully
# 	is -1 if there was already a file with that name in the list

def add_file_to_file_list(file_name, file_list, addr):
	# Check if there is a file with that name already in the file_list
	m_file = next((file_pair for file_pair in file_list if file_pair[1] == file_name), None)

	if m_file is not None:
		return [-1, file_list]
	else:
		file_list.append([addr, file_name])
		return [1, file_list]


# Currently file_pair is [addr, file_name]
# Returns file_name
# Created this function so that as we add information to a file "pair", we won't have to edit
# this conversion in multiple places (netbin_host#list, host_function_handler#list)

def convert_file_pair_to_list_string(file_pair):
	return file_pair[1]

# LIST COMMAND - HOST
#
#	uses delimiter to separate each segment of information
#
def list(s, file_list):
	try:
		num_files = str(len(file_list))
		
		s.sendall(num_files+constants.LIST_ITEM_DELIMITER)

		if len(file_list) > 0:
			for fp in file_list:
				fn = convert_file_pair_to_list_string(fp)
				s.sendall(fn + constants.LIST_ITEM_DELIMITER)

	except socket.error:
		print constants.HOST_COMM_ERROR
		return



def upload(s, file_list, user_input, addr):
	try:
		upload = user_input.split(' ')

		if len(upload) < 2:
			s.sendall("ERROR: Filename not received.")
		else:
			result, file_list = add_file_to_file_list(upload[1], file_list, addr[0])
			

			if result == -1:
				s.sendall("There is already a file with that name hosted. Please try a different file name")
			elif result == 1:
				s.sendall(upload[1] + " uploaded!")
				printDebug("current file list is ", "h")
				printDebug(str(file_list), "h")
			else:
				s.sendall("Unidentified error occurred, Code " + str(result))

	except socket.error:
		print constants.HOST_COMM_ERROR

	return file_list

	
def download(s, file_list, user_input):
	try:
		download = user_input.split(' ')
		if len(download) < 2:
			s.sendall("ERROR: Filename not received.")
		else:
			printDebug("Received Download Request for: " + user_input, "h")
			dl_file_pair = next((file_pair for file_pair in file_list if file_pair[1] == download[1]), None)
			if dl_file_pair == None:
				s.sendall("ERROR: File not found in list. Are you sure it's been uploaded?")
			else:
				s.sendall(dl_file_pair[0])
				printDebug("Requested file is available at " + dl_file_pair[0], "h")
	except socket.error:
		print constants.HOST_COMM_ERROR
		return
