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

		while True:
			con, file_owner_addr = sock.accept()
			try:
				while True:
					file_data = con.recv(GEN_PACKETLENGTH)
					if file_data:
						print file_data
						break
			finally:
				con.close()

	def tcp_send(self, file_data, fh, addr):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((addr, self.port))
		try:
			sock.sendall(file_data)
		except socket.error:
			printDebug("Socket error", "tcp")

		finally:
		    print "closing socket"
		    sock.close()