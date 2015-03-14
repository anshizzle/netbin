import sys
import socket
import os
from thread import *
import pdb
import netbin_host
from netbin_udp import netbin_udp
import client_function_handler
next_host = 0
LISTEN_PORT = 7900


def printError(error):
	print "ERROR: " + error + ' Terminating.'
	sys.exit()

def download_file(s):
	raw = s.recv(4096)
	print raw

def client_input(is_host, s):
	while 1:

		user_input = raw_input("> ")
		if user_input == "exit":
			if is_host:
				netbin_host.exit()
			else:
				break
		# before sending make sure they are sending legit files before sending
		if user_input.startswith("upload"):
			client_function_handler.upload(s, user_input)
		elif user_input == "list":
			client_function_handler.list(s)
		elif user_input.startswith("download"):
			client_function_handler.download_file(s, user_input)

		else: 
			print "Invalid command"


def start(host, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = s.connect_ex((host, port))

	if result > 0: 
		printError("Could not connect to server.")

	print "Connected to host"

	msg = s.recv(4096)

	if msg == "NEXTHOST":
		next_host=1
		print "You are going to be the next host."
	else:
		print "Welcome to netbin!"

	my_udp = netbin_udp(LISTEN_PORT)
	start_new_thread(my_udp.client_listener, ())

	client_input(False, s)

	s.close()