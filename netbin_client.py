import sys
import socket
import os
from thread import *
import pdb
import netbin_host

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


def receive_message(s):
	message = ""
	file_name = ""
	addr = ""
	try:
		s.settimeout(None)
		msg, addr = s.recvfrom(1024)
		
		if msg.startsWith("REQUEST"):
			tmp = msg.split(' ')
			message = "REQUEST"
			file_name = tmp[1]
		elif msg.startsWith("NEXTHOST"):
			message = "NEXTHOST"
			file_name = ""

		else:
			message = "INVALID"
			file_name = ""


		s.sendto("ACK", addr)

	except socket.error:
		print "Failed to receive message"

	return [message, file_name,addr]



def client_listener(port):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	host = socket.gethostname()

	print "attempting to bind UDP at host " + host + " with port " + str(port)
	try:
		s.bind((host, port))
	except socket.error, msg:
		printError('Could not bind passive listener to port.')



	while 1:
		data, file_name, addr = receive_message(s)
		print data + " " + file_name + " from " + addr


def client_input(is_host):
	while 1:
		print ">"
		user_input = raw_input()

		# before sending make sure they are sending legit files before sending
		if user_input.startswith("upload"):
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

		elif user_input == "exit":
			if is_host:
				netbin_host.exit()
			else:
				break

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

	start_new_thread(client_listener, (LISTEN_PORT, ))

	client_input(False)


			

	s.close()