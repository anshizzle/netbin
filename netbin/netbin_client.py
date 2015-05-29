import sys
import os
import socket
import client_function_handler

from netbin_udp import *
import constants
from thread import *
import netbin_host


def download_file(s):
	raw = s.recv(4096)
	print raw

def client_input(is_host, s, udp_socket):
	while 1:
		user_input = raw_input("netbin> ")
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
			if is_host:
				netbin_host.list()
			else:
				client_function_handler.list(s)
		elif any(user_input.startswith(cmd) for cmd in constants.DOWNLOAD_CMDS): # DOWNLOAD
			if is_host:
				netbin_host.download(user_input, udp_socket)
			else:
				client_function_handler.download_file(s, user_input, udp_socket)
		else: 
			print "Invalid command"




def start(host, port):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		result = s.connect_ex((host, port))

		if result > 0: 
			constants.printError("Could not connect to server.")

		print "Connected to host at ", host

		# create a udp listener for each client
		my_udp = netbin_udp(constants.LISTEN_PORT, constants.COMMUNICATE_PORT, host)
		start_new_thread(my_udp.listener, ())

		msg = s.recv(4096)

		print "Welcome to netbin!"

		# check for netbin folder if not located then create one
		net_dir = os.path.dirname(constants.NETBIN_DIR)
		if not os.path.exists(net_dir):
			os.makedirs(net_dir)
			printDebug("Created Netbin Directory", "ci")
		client_input(False, s, my_udp)

		s.close()
	except socket.error:
		print "Error starting netbin client"
	sys.exit()