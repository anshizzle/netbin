import sys
import socket
import client_function_handler

from netbin_udp import *
import constants
from thread import *

def printError(error):
	print "ERROR: " + error + ' Terminating.'
	sys.exit()

def download_file(s):
	raw = s.recv(4096)
	print raw

def client_input(is_host, s, udp_socket):
	while 1:
		user_input = raw_input("> ")
		if any(user_input == cmd for cmd in constants.UPLOAD_CMDS):
			if is_host:
				netbin_host.exit()
			else:
				break
		# before sending make sure they are sending legit files before sending
		elif any(user_input.startswith(cmd) for cmd in constants.UPLOAD_CMDS):
			client_function_handler.upload(s, user_input)
		elif any(user_input.startswith(cmd) for cmd in constants.LIST_CMDS):
			print "Sending list request"
			client_function_handler.list(s)
		elif any(user_input.startswith(cmd) for cmd in constants.DOWNLOAD_CMDS):
			client_function_handler.download_file(s, user_input, udp_scoket)
		else: 
			print "Invalid command"


def start(host, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = s.connect_ex((host, port))

	if result > 0: 
		printError("Could not connect to server.")

	print "Connected to host"

	# create a udp listener for each client
	my_udp = netbin_udp(constants.LISTEN_PORT)
	start_new_thread(my_udp.listener, ())

	msg = s.recv(4096)

	if msg == "NEXTHOST":
		next_host=1
	else:
		print "Welcome to netbin!"

	client_input(False, s, my_udp)

	s.close()
	sys.exit()