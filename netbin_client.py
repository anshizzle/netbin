import sys
import socket
import client_function_handler

from netbin_udp import *
import constants
from thread import *



def download_file(s):
	raw = s.recv(4096)
	print raw

def client_input(is_host, s, udp_socket):
	while 1:
		user_input = raw_input("> ")
		if any(user_input == cmd for cmd in constants.EXIT_CMDS):
			if is_host:
				netbin_host.exit(s)
			else:
				s.sendall("exit")
				response = s.recv(constants.GEN_PACKET_LENGTH)
				print response
				break
		# before sending make sure they are sending legit files before sending
		elif any(user_input.startswith(cmd) for cmd in constants.UPLOAD_CMDS): #UPLOAD
			if is_host:
				netbin_host.upload(s,user_input)
			else:
				client_function_handler.upload(s, user_input)
		elif any(user_input.startswith(cmd) for cmd in constants.LIST_CMDS): # LIST
			print "Sending list request"
			client_function_handler.list(s)
		elif any(user_input.startswith(cmd) for cmd in constants.DOWNLOAD_CMDS): # DOWNLOAD
			client_function_handler.download_file(s, user_input, udp_socket)
		else: 
			print "Invalid command"




def start(host, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = s.connect_ex((host, port))

	if result > 0: 
		constants.printError("Could not connect to server.")

	print "Connected to host"

	# create a udp listener for each client
	my_udp = netbin_udp(constants.LISTEN_PORT, constants.COMMUNICATE_PORT, host)
	start_new_thread(my_udp.listener, ())

	msg = s.recv(4096)

	print "Welcome to netbin!"

	client_input(False, s, my_udp)

	s.close()
	sys.exit()