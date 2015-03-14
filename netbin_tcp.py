import sys
import socket

class netbin_tcp:

	def __init__(self, port):
		this.port = port

	def tcp_listener(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind((addr, self.port))
		sock.listen(1)

		while True:
			con, file_owner_addr = sock.accept()
		try:
			while True:
				file_data = connection.recv(GEN_PACKETLENGTH)
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
		    print >>sys.stderr, 'closing socket'
		    sock.close()