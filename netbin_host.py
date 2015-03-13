import sys
import socket
from thread import *


next_host = 0
file_list = []


def printError(error):
	print "ERROR: " + error + ' Terminating.\n'
	sys.exit()




def clientthread(conn):
	if next_host != 0:
		conn.sendall("NEXTHOST")
	else:
		conn.sendall("Welcome")

	while True:
		data = conn.recv(1024)
		reply = 'OK...' + data
		if not data:
			break
		conn.sendall(reply)
		print "Response sent: "
		print reply


	conn.close()

def inputthread():
	user_input = raw_input()

	if user_input == "exit":
		sys.exit()



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



	while 1:

		#Accept the connection
		conn, addr = s.accept()
		print 'Connected with ' + addr[0] + ':' + str(addr[1])

		#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
		start_new_thread(clientthread ,(conn,))

		

	s.close()



if __name__ == '__main__':
    netbin_host()