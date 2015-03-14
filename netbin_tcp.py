import sys
import socket
import constants

from netbin_udp import *
import constants
from util import *


class netbin_tcp:

	def __init__(self, port):
		self.port = port

	def tcp_listener(self, comm_addr, udp_sock):
		print "YOU ARE NOW LISTENING FOR FILE DATA ON PORT: "+ str(self.port)
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind((socket.gethostname(), self.port))
		sock.listen(1)

		# tell the requesting client the connection is open and what port it's on
		udp_sock.send_tcp_open_msg(self.port, comm_addr)		
		con, file_owner_addr = sock.accept()
		file_data = ""
		while not file_data.endswith(constants.FILE_END_SIGNAL):
				try:
					file_data = con.recv(constants.GEN_PACKET_LENGTH)
				except socket.error as serr:
					printDebug("Socket Error " + str(serr.errno))
				if file_data:
					print file_data
					break
		

		con.close()


	def tcp_send(self, fh, addr):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		fd = ""

		sock.connect_ex((addr, self.port))
		try:
			with open(fh, 'rb') as f:
				fd = f.read()
				print fd

		except IOError:
			print "check that the file exists"


		try:
			sock.sendall(fd + constants.FILE_END_SIGNAL)
		except socket.error:
			printDebug("Socket error", "tcp")

		finally:
		    print "closing socket"
		    sock.close()