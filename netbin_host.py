import sys
import os
import socket
from thread import *
import netbin_client
import host_function_handler


next_host = 0
conns = []
file_list = [] # Each file is stored as triple with [Addr, FileName]

def printError(error):
	print "ERROR: " + error + ' Terminating.\n'
	sys.exit()






def manage_client(s, addr):
	global file_list
	s.sendall("Welcome")

	while True:
		print "waiting for request"
		data = s.recv(1024)

		if data == "list":
			print "list request received"
			host_function_handler.list(s, file_list)
		elif data.startswith("upload"):
			file_list = host_function_handler.upload(s, file_list, data, addr)
		elif data.startswith("download"):
			host_function_handler.download(s, file_list, data)
		elif data == "exit":
			print "Closing connection with " + addr[0]
			s.sendall("Closing connection")
			break
		else:
			s.sendall("Command unrecognized")




	# Also need to remove all files for conn from the file_list

	# also need to remove conn from conns list. 

	s.close() # close connection
	sys.exit() # terminate threa


def inputthread(s):
	print "Input thread running"
	while True:
		user_input = raw_input()

		if user_input == "exit":

			print "exit received"
			exit(s)

			

# Need to handle all clean up.
def exit(s):
	#PICK A CONNECTION TO BE THE NEXT HOST.
	#Send it the info
	[conn.close() for conn in conns]
	s.close()
	os._exit(1)

def start(port):
	s = socket.socket()
	host = socket.gethostname()
	# Bind socket to port
	try:
	    s.bind((host, port))
	except socket.error, msg:
		printError('Could not bind port.')

	s.listen(5)
	print 'Now listening '

	start_new_thread(inputthread, (s, ))



	while 1:

		#Accept the connection
		conn, addr = s.accept()
		print 'Connected with ' + addr[0] + ':' + str(addr[1])
		conns.append(conn)

		#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
		start_new_thread(manage_client ,(conn, addr, ))

		




if __name__ == '__main__':
    netbin_host()