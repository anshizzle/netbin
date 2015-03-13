import sys
import socket


next_host = 0


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



def start(host, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = s.connect_ex((host, port))

	if result > 0: 
		printError("Could not connect to server.")

	print "Connected to host"

	msg = s.recv(4096)

	if msg == "NEXTHOST":
		next_host=1
	else:
		print "Welcome to netbin!"


	while 1:
		print ">"
		user_input = raw_input()
		s.sendall(user_input)

		if user_input == "list":
			receive_file_list(s)

		elif user_input == "exit": 
			break
		else:
			try:
				reply = s.recv(4096)
				print reply
			except socket.error:
				printError("Failed to receive the message.")

	s.close()