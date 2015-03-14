import sys
import os
import socket
from thread import *
import netbin_client
import host_function_handler
import constants
from netbin_udp import *


next_host = 0
conns = []
file_list = [] # Each file is stored as triple with [Addr, FileName]
host_udp = netbin_udp(constants.LISTEN_PORT)


def printError(error):
	print "ERROR: " + error + ' Terminating.\n'
	sys.exit()


#
# Function is given its own thread
# Used to handle an individual client.
#
def manage_client(s, addr):
	global file_list
	s.sendall("Welcome")

	while True:
		print "waiting for request"
		data = s.recv(1024)

		if any(user_input.startswith(cmd) for cmd in constants.LIST_CMDS):
			print "list request received"
			host_function_handler.list(s, file_list)
		elif any(user_input.startswith(cmd) for cmd in constants.UPLOAD_CMDS):
			file_list = host_function_handler.upload(s, file_list, data, addr)
		elif any(user_input.startswith(cmd) for cmd in constants.DOWNLOAD_CMDS):
			host_function_handler.download(s, file_list, data)
		elif any(user_input == cmd for cmd in constants.EXIT_CMDS):
			print "Closing connection with " + addr[0]
			s.sendall("Closing connection")
			break
		else:
			s.sendall("Command unrecognized")




	# Also need to remove all files for conn from the file_list
	tmp = [file_pair for file_pair in file_list if file_list[0] != addr[0]]
	file_list = tmp

	# also need to remove conn from conns list. 
	tmp = [conn_pair for conn_pair in conns if conns[0] != addr]
	conns = tmp

	
	s.close() # close connection
	sys.exit() # terminate threa


def inputthread(s):
	print "Input thread running"
	while True:
		user_input = raw_input()

		if user_input == "exit":
			print "exit received"
			exit(s)

			
def upload(s, user_input):
	global file_list
	file_input = user_input.split(' ')
	if len(file_input) < 2:
		print "USAGE: upload filename"
	else:
		if os.path.isfile(file_input[1]):
			file_list = host_function_handler.upload(s,file_list, data, addr)
		else:
			print consants.INVALID_FILE_UPLOAD

# Need to handle all clean up.
def exit(s):

	if len(conns) > 0:
		#PICK A CONNECTION TO BE THE NEXT HOST and send it all relevant info

		#Send it the info
		[conn[0].close() for conn in conns]

	s.close()
	os._exit(1)




def start(port):
	global host_udp
	s = socket.socket()
	host = socket.gethostname()
	# Bind socket to port
	try:
	    s.bind((host, port))
	except socket.error, msg:
		printError('Could not bind port. Please restart netbin')

	s.listen(5)
	print 'Now listening '

	# start_new_thread(netbin_client.client_input, (True, s, host_udp))
	start_new_thread(inputthread, (s, ))
	start_new_thread(host_udp.listener, ())

	while 1:

		#Accept the connection
		conn, addr = s.accept()
		print 'Connected with ' + addr[0] + ':' + str(addr[1])
		conns.append([conn,addr])

		#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
		start_new_thread(manage_client ,(conn, addr, ))

		




if __name__ == '__main__':
    netbin_host()