import sys
import socket
import constants

from netbin_udp import *
import constants

class netbin_tcp:

	def __init__(self, port):
		self.port = port

	def tcp_listener(self):
		print "YOU ARE NOW LISTENING FOR FILE DATA ON PORT: "+self.port
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind((addr, self.port))
		sock.listen(1)

		# tell the requesting client the connection is open
		my_udp = netbin_udp(constants.LISTEN_PORT)
		my_upd.send_tcp_open_msg(self.port, addr)

		while True:
			con, file_owner_addr = sock.accept()
			try:
				while True:
					file_data = con.recv(GEN_PACKETLENGTH)
					if file_data:
						break
			finally:
				con.close()

	def tcp_send(self, file_data, fh, addr):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((addr, self.port))
		try:
			sock.sendall(fh, file_data)

		finally:
		    print "closing socket"
		    sock.close()