import sys
import os
import socket
from thread import *
import netbin_client
import host_function_handler
import constants
from netbin_udp import *
from util import *

next_host = 0
conns = [] # Each connection stored as [Socket, Addr]
file_list = [] # Each file is stored as tuple with [IP, FileName]
host_udp = netbin_udp(constants.HOST_LISTEN_PORT, constants.HOST_COMMUNICATE_PORT, socket.gethostname())
host_ip = ""



#
# Function is given its own thread
# Used to handle an individual client.
#
def manage_client(s, addr):
	global file_list
	global conns
	s.sendall("Welcome")

	while True:
		try:
			data = s.recv(1024)
		

			if any(data.startswith(cmd) for cmd in constants.LIST_CMDS):
				host_function_handler.list(s, file_list)
			elif any(data.startswith(cmd) for cmd in constants.UPLOAD_CMDS):
				file_list = host_function_handler.upload(s, file_list, data, addr)
			elif any(data.startswith(cmd) for cmd in constants.DOWNLOAD_CMDS):
				host_function_handler.download(s, file_list, data)
			elif any(data == cmd for cmd in constants.EXIT_CMDS):
				printDebug("Closing connection with " + addr[0], "h")
				break
			else:
				s.sendall("Command unrecognized")

		except socket.error:
			printDebug("Client socket error!", "dh")
			clear_connection(s, addr)
			s.close()
			sys.exit()
			return


	clear_connection(s, addr)


	s.sendall("Closing connection")
	s.close() # close connection
	sys.exit() # terminate threa


def clear_connection(conn, addr):
	global file_list
	global conns

	# Also need to remove all files for conn from the file_list
	file_list = [file_pair for file_pair in file_list if file_pair[0] != addr[0]]	
	printDebug("New File List is ", "h")
	printDebug(str(file_list), "h")

	# also need to remove conn from conns list. 
	conns = [conn_pair for conn_pair in conns if conn_pair[1] != addr]
	printDebug("New Conns List is ", "h")
	printDebug(str(conns), "h")	


def inputthread(s):
	print "Input thread running"
	while True:
		user_input = raw_input()

		if user_input == "exit":
			print "exit received"
			exit(s)


##
#
# HOST CLIENT FUNCTIONS
#
# Functions that allow the device running the host process is 
# interacting as a standard netbin client
#
##

## If the host, as a client, calls upload.			
def upload(s, user_input):
	global file_list
	file_input = user_input.split(' ')
	if len(file_input) < 2:
		print "USAGE: upload filename"
	else:
		netbin_fh = constants.NETBIN_DIR + file_input[1]
		if os.path.isfile(netbin_fh):
			result, file_list = host_function_handler.add_file_to_file_list(netbin_fh, file_list,host_ip)
			if result == -1:
				print "There is already a file with that name hosted. Please try a different file name"
			else:
				print file_input[1] + " uploaded!"
		else:
			print constants.INVALID_FILE_UPLOAD


## Lists all files
def list(): 
	num_files = len(file_list)
	

	if num_files > 0:
		print constants.list_file_num_string(num_files)
		for fp in file_list:
			fn = host_function_handler.convert_file_pair_to_list_string(fp)
			print fn
	else:
		print constants.NO_FILES_STRING


def download(user_input, udp):
	dl_string = user_input.split(' ')	

	dl_file_pair = next((file_pair for file_pair in file_list if file_pair[1] == dl_string[1]), None)

	if dl_file_pair == None:
		print "ERROR: File not found in list. Are you sure it's been uploaded?"
	else:
		udp.send_request(dl_string[1], dl_string[2], dl_file_pair[0])



# Need to handle all clean up.
def exit(s):

	if len(conns) > 0:
		#PICK A CONNECTION TO BE THE NEXT HOST and send it all relevant info

		#Send it the info
		[conn[0].close() for conn in conns]

	s.close()
	os._exit(1)




def start(port, ip_addr):
	global host_udp
	global host_ip


	host_ip = ip_addr
	s = socket.socket()
	host = socket.gethostname()
	# Bind socket to port
	try:
	    s.bind((host, port))
	except socket.error, msg:
		constants.printError('Could not bind port. Please restart netbin')

	s.listen(5)
	printDebug('Now listening as host', "h")

	client_udp = netbin_udp(constants.LISTEN_PORT, constants.COMMUNICATE_PORT, socket.gethostname())
	# start_new_thread(netbin_client.client_input, (True, s, host_udp))

	start_new_thread(client_udp.listener, ())
	start_new_thread(host_udp.host_listener, ())

	start_new_thread(netbin_client.client_input, (True, s, client_udp, ))

	while 1:

		#Accept the connection
		conn, addr = s.accept()
		printDebug('Connected with ' + addr[0] + ':' + str(addr[1]), "h")
		conns.append([conn,addr])

		#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
		start_new_thread(manage_client ,(conn, addr, ))

		




if __name__ == '__main__':
    netbin_host()