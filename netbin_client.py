import sys
import socket
import os
from thread import *
import pdb
import netbin_host
from netbin_udp import netbin_udp
next_host = 0
LISTEN_PORT = 7900

def printError(error):
	print "ERROR: " + error + ' Terminating.'
	sys.exit()

def receive_file_list(s):
	raw = s.recv(4096)
	try:
		num_files = int(raw)
	except ValueError:
		num_files = 0
	if num_files == 0:
		print "No files currently on the network\n"
	else:
		print "There are " + str(num_files) + " on the network\n"
		file_list = s.recv(4096)
		print file_list

def download_file(s):
	raw = s.recv(4096)
	print raw

def client_input(is_host, s):
	while 1:
		print ">"
		user_input = raw_input()
		if user_input == "exit":
			if is_host:
				netbin_host.exit()
			else:
				break
		# before sending make sure they are sending legit files before sending
		elif user_input.startswith("upload"):
			fileinput = user_input.split(' ')
			if len(fileinput) < 2:
				print "USAGE: Upload requires a filehandle"
			else:
				if(os.path.isfile(fileinput[1])):
					s.sendall("upload "+fileinput[1])
					with open(fileinput[1], "r+") as content_file:
						file_data = content_file.read()
					print file_data
					#TODO host file data
					#s.sendall(file_data)
				else:
					print "Invalid File Found"
		elif user_input == "list":
			receive_file_list(s)
		elif user_input.startswith("download"):
			download_file(s)

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