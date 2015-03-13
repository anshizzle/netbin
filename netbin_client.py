import sys
import socket

next_host = 0


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
		user_input = raw_input()
		s.sendall(user_input)

		try:
			reply = s.recv(4096)
			print reply
		except socket.error:
			printError("Failed to receive the message.")