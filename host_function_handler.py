import socket
import constants

# LIST COMMAND - HOST
#
#	First sends the number of files, padded to LIST_INIT_PACKET_LENGTH chars.
#	Next sends each file name, padded to LIST_FILE_PACKET_LENGTH chars.
#
def list(s, file_list):
	num_files = str(len(file_list))
	padding = '-'*(LIST_INIT_PACKET_LENGTH - len(num_files))
	conn.sendall(num_files+padding)

	if len(file_list) > 0:
		for fp in file_list:






def send_file_list(conn):

	conn.sendall(str(len(file_list)))
	
	if len(file_list) > 0:
		files = [file_pair[2] for file_pair in file_list]
		response = str(files).strip('[]')
		conn.sendall(response)