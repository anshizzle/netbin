import socket
import constants

# LIST COMMAND - HOST
#
#	First sends the number of files, padded to LIST_INIT_PACKET_LENGTH chars.
#	Next sends each file name, padded to LIST_FILE_PACKET_LENGTH chars.
#
def list(s, file_list):
	num_files = str(len(file_list))
	padding = '-'*(constants.LIST_INIT_PACKET_LENGTH/38 - len(num_files)/38)
	s.sendall(num_files+padding)

	if len(file_list) > 0:
		for fp in file_list:
			fn = fp[1]
			padding = '-' * (constants.LIST_FILE_PACKET_LENGTH/38 - len(fn)/38)
			s.sendall(fn + padding)



def upload(s, file_list, user_input, addr):
	upload = user_input.split(' ')
	# need to check if file is already there.

	if len(upload) < 2:
		s.sendall("ERROR: Filename not received.")
	else:
		# TODO: check if there is already a file with that name in the list.
		m_file = next((file_pair for file_pair in file_list if file_pair[1] == upload[1]), None)

		if m_file is not None and s is not None:
			s.sendall("There is already a file with that name hosted. Please try a different file name")
		else:
			file_list.append([addr[0], upload[1]])
			s.sendall(upload[1] + " uploaded!")
			print "current file list is "
			print file_list

	return file_list

def download(s, file_list, user_input):
	download = user_input.split(' ')
	if len(download) < 2:
		s.sendall("ERROR: Filename not received.")
	else:
		print "Received Download Request for: " + user_input
		dl_file_pair = next((file_pair for file_pair in file_list if file_pair[1] == download[1]), None)
		if dl_file_pair == None:
			s.sendall("ERROR: File not found in list. Are you sure it's been uploaded?")
		else:
			s.sendall(dl_file_pair[0])
			print "Requested file is available at " + dl_file_pair[0]
