import sys
import socket
import constants

from netbin_udp import *
import constants
from util import *



class netbin_tcp:

	def __init__(self, port):
		self.port = port

	def tcp_listener(self, comm_addr, fh,  udp_sock):
		printDebug("YOU ARE NOW LISTENING FOR FILE DATA ON PORT: "+ str(self.port), "tcp")
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind((socket.gethostname(), self.port))
		sock.listen(1)

		# tell the requesting client the connection is open and what port it's on
		udp_sock.send_tcp_open_msg(self.port, comm_addr)		
		con, file_owner_addr = sock.accept()

		# actually read the data
		file_data = ""

		try:
			f = open(fh, 'wb')
		except IOError:
			printDebug("check that file exists", "tcp")

		count = 0

		while not file_data.endswith(constants.FILE_END_SIGNAL):
				try:
					count = count +1
					file_data = con.recv(constants.GEN_PACKET_LENGTH)
					if file_data.endswith(constants.FILE_END_SIGNAL):
						file_data = file_data.replace(constants.FILE_END_SIGNAL, "")
						f.write(file_data)
						break
					f.write(file_data)
				except socket.error as serr:
					printDebug("Socket Error " + str(serr.errno), "tcp")		


		f.close()
		con.close()

		printDebug("REACHED END OF TRANSMISSON", "f")
		printDebug("Number of transmissions: " + str(count), "f")

	def tcp_send(self, fh, addr):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		fd = ""

		sock.connect_ex((addr, self.port))
		try:
			with open(fh, 'rb') as f:
				while True:
					fd = f.read(constants.GEN_PACKET_LENGTH)
					print fd
					try:
						sock.sendall(fd)
					except socket.error:
						printDebug("socket error", "tcp")
					if not fd:
						break

		except IOError:
			printDebug("check that the file exists","tcp")

		try:
			sock.sendall(constants.FILE_END_SIGNAL)
		except socket.error:
			printDebug("Socket error", "tcp")
		

		finally:
		    printDebug( "closing TCP socket", "tcp")
		    sock.close()