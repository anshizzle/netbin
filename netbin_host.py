import sys
import os
import socket
from thread import *
import netbin_client


next_host = 0
conns = []
file_list = [] # Each file is stored as triple with [Addr, FileName]
s = socket.socket()

def printError(error):
	print "ERROR: " + error + ' Terminating.\n'
	sys.exit()






def manage_client(conn, addr):
	conn.sendall("Welcome")

	while True:
		print "waiting for request"
		data = conn.recv(1024)

		if data == "list":
			print "list request received"
			send_file_list(conn)
		elif data.startswith("upload"):
			#wait for client to send file data
			file_handle = data.split(' ')[1]
			file_list.append([conn, file_handle])
			conn.sendall("File: " + file_handle + " received")
			print "current file list is "
			print file_list
			upload = data.split(' ')
			if len(upload) < 2:
				conn.sendall("ERROR: Filename not received.")
			else:
				file_list.append([conn, addr, upload[1]])
				conn.sendall("File: " + upload[1] + " received")
				print "current file list is "
				print file_list
		elif data.startswith("download"):
			download = data.split(' ')
			if len(download) < 2:
				conn.sendall("ERROR: Filename not received.")
			else:
				dl_file_pair = next((file_pair for file_pair in file_list if file_pair[2] == download[1]), None)
				if dl_file_pair == None:
					conn.sendall("ERROR: File not found in list. Are you sure it's been uploaded?")
				else:
					conn.sendall(dl_file_pair[1][0])
		elif data == "exit":
			print "Closing connection with " + conn.gethostname()
			conn.sendall("Closing connection")
			break
		else:
			conn.sendall("Command unrecognized")




	# Also need to remove all files for conn from the file_list

	# also need to remove conn from conns list. 

	conn.close() # close connection
	sys.exit() # terminate threa


def inputthread(socket):
	print "Input thread running"
	while True:
		user_input = raw_input()

		if user_input == "exit":

			print "exit received"
			exit()

			

# Need to handle all clean up.
def exit():
	#PICK A CONNECTION TO BE THE NEXT HOST.
	#Send it the info
	[conn.close() for conn in conns]
	socket.close()
	os._exit(1)

def start(port):
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
		start_new_thread(clientthread ,(conn, addr, ))

		




if __name__ == '__main__':
    netbin_host()