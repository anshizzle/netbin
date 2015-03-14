import socket
from netbin_tcp import *
import constants


def receive_host_message(s):
	message=""
	data=""
	addr = ""
	try: 
		s.settimeout(None)
		msg, addr = s.recvfrom(1024)

		if msg.startswith("ISHOST"):
			message = "ISHOST"
		elif msg.startswith("NEEDTCPPORT"):
			message = "NEEDTCPPORT"
		elif msg.startswith("RELEASINGTCPPORT"):
			tmp = msg.split(' ')
			if len(tmp) < 2:
				message="INVALID"
			else:				
				message = "RELEASINGTCPPORT"
				data = tmp[1]
		else:
			message ="INVALID"
	except socket.error:
		print "Failed to receive message"

	return [message,data,addr]


def receive_message(s):
	message = ""
	file_name = ""
	addr = ""
	try:
		s.settimeout(None)
		msg, addr = s.recvfrom(1024)
		if msg.startswith("ACK"):
			file_name = msg.split(' ')[1]
			s.sendto("ACK", addr) #SEND ACK
			return [file_name, addr]
		elif msg.startswith("TCPOPEN"):
			port = msg.split(' ')[1]
			return port
		elif msg.startswith("REQUEST"):
			tmp = msg.split(' ')
			message = "REQUEST"
			file_name = tmp[1]
		elif msg.startswith("NEXTHOST"):
			message = "NEXTHOST"

		elif msg.statswith("NEWHOST"):
			tmp = msg.split(' ')
			if len(tmp) < 2:
				message="INVALID"
			else:
				message = "NEWHOST"
				file_name = tmp[1]
		else:
			message = "INVALID"
			file_name = ""
		if message != "INVALID":
			s.sendto("ACK", addr) #SEND ACK if not invalid message

	except socket.error:
		print "Failed to receive message"

	return [message, file_name, addr]


class netbin_udp:
	def __init__(self, port):
		self.port = port
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.host = socket.gethostname()
		self.available_tcp_ports = range(constants.LISTEN_PORT+1, constants.LISTEN_PORT+11).reverse()


	def listener(self):
		print "attempting to bind UDP at host " + self.host + " with port " + str(self.port)
		try:
			self.s.bind((self.host, self.port))
		except socket.error, msg:
			printError('Could not bind passive listener to port.')
		while 1:
			file_name, addr = receive_message(self.s)
			print file_name + "\n"
			#print addr
			if file_name and addr:
				while 1:
					# need to know that the listening tcp connection is open
					tcp_port = receive_message(self.s)
					if(tcp_port):
						# now send file data to requesting netbin client
						my_tcp = netbin_tcp(tcp_port)
						while 1:
							try:
								with open(file_name, 'rb') as f:
									file_data = f.read()
									print file_data
									break

							except IOError:
								print "check that the file exists"

						if(file_data): break

					else:
						print "waiting to for tcp listener creation"


	def host_listener(self):
		print "attempting to bind UDP at host " + self.host + " with port " + str(self.port)
		try:
			self.s.bind((self.host, self.port))
		except socket.error, msg:
			printError('Could not bind passive listener to port.')
		while 1:
			msg, data, addr = receive_host_message(self.s)
			if msg == "ISHOST":
				self.s.sendto("IAMHOST", addr)
			elif msg == "NEEDTCPPORT":
				self.s.sendto(str(self.available_tcp_ports.pop()), addr)
			elif msg == "RELEASINGTCPPORT":
				try:
					released_port = int(data)
					self.available_tcp_ports.insert(0, released_port)
					self.s.sendto("RELEASESUCCESSFUL", addr)
				except ValueError:
					self.s.sendto("INVALIDPORT", addr)

				my_tcp.tcp_send(file_data, file_name, addr[0])

	def send_request(self, fh, addr):
		#send the whole command
	    self.s.sendto("ACK " + fh, (addr, constants.LISTEN_PORT))
	    # Get ACK from listener
	    package_acked = 0
	    count = 1 #message has already been sent once

	    self.s.settimeout(.500)
	    while not package_acked and count < 3:
	        print "Waiting for ACK FOR " + fh
	        try:
	            d = self.s.recvfrom(1024)
	            reply = d[0]
	            if reply == "ACK":
	                package_acked = 1
	                print fh + " ACK'D"
	                break
	        except socket.error:
				print "am i getting a socket error"
				self.s.sendto(fh, (addr, constants.LISTEN_PORT))
				count = count + 1
	    
	    if(package_acked):
			# NOW THAT YOU HAVE ACK'D SET UP TCP connect
			my_tcp = netbin_tcp(7902)
			my_tcp.tcp_listener()
	    else:
	        print "Could not locate file holder. Please try again in a little bit."


	def send_tcp_open_msg(self, port, addr):
		self.s.sendto("TCPOPEN " + port, (addr, constants.LISTEN_PORT))
