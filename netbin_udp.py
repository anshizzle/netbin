import socket
from netbin_tcp import *
import constants
from util import *


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


def receive_message(s, s_comm):
	message = ""
	file_name = ""
	addr = ""
	port = ""
	try:
		s.settimeout(None)
		msg, addr = s.recvfrom(1024)
		port = addr[1]
		if msg.startswith("ACK"):
			printDebug("received file request for >" + msg + "<", "udp")
			message = "REQUEST"
			tmp = msg.split(' ')
			file_name = tmp[1]
			port = tmp[2]
		# elif msg.startswith("REQUEST"):
		# 	tmp = msg.split(' ')
		# 	message = "REQUEST"
		# 	file_name = tmp[1]
		elif msg.startswith("NEXTHOST"):
			message = "NEXTHOST"

		elif msg.startswith("NEWHOST"):
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
			s_comm.sendto("ACK", (addr[0], port ))#SEND ACK if not invalid message

	except socket.error:
		print "Failed to receive message"

	return [message, file_name, addr, port]


class netbin_udp:
	def __init__(self, port1, port2, hostAddr):
		self.receive_port = port1
		self.communicate_port = port2
		self.hostAddr = hostAddr
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.s_comm = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.host = socket.gethostname()
		self.available_tcp_ports = range(constants.LISTEN_PORT+1, constants.LISTEN_PORT+11).reverse()


	def listener(self):
		print "attempting to bind UDP at host " + self.host + " with port " + str(self.port)
		try:
			self.s.bind((self.host, self.receive_port))
			self.s_comm.bind((self.host, self.communicate_port))
		except socket.error, msg:
			constants.printError('Could not bind passive listener to port.')
		while 1:
			message, file_name, addr, port = receive_message(self.s, self.s_comm)
			print file_name + "\n"
			#print addr
			if file_name and addr:
				
				# need to know that the listening tcp connection is open
				# tcp_port = self.receive_message(self, self.s)
				tcp_port_msg = self.s_comm.recvfrom(1024)
				tcp_port = int(tcp_port_message.split(' ')[1])

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

					if(file_data): 
						my_tcp.tcp_send(file_data, file_name, addr[0])


				else:
					print "waiting to for tcp listener creation"


	def host_listener(self):
		print "attempting to bind UDP at host " + self.host + " with port " + str(self.receive_port)
		try:
			self.s.bind((self.host, self.receive_port))
			self.s_comm.bind((self.host, self.communicate_port))
			# print "Successfully bound UDP Passive Listener for Host with Port" + str(self.port)
		except socket.error, msg:
			constants.printError('Could not bind passive listener to port.')
		while 1:
			msg, data, addr = receive_host_message(self.s)
			if msg == "ISHOST":
				print "Received ISHOST Request from " + addr[0]
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


	def send_request(self, fh, addr):
		#send the whole command


	    self.s_comm.sendto("ACK " + fh, (addr, constants.LISTEN_PORT))
	    # Get ACK from listener
	    package_acked = 0
	    count = 1 #message has already been sent once

	    self.s.settimeout(.500)
	    while not package_acked and count < 3:
	        print "Waiting for ACK FOR " + fh
	        try:
	            d, comm_addr = self.s_comm.recvfrom(1024)
	            reply = d[0]
	            if reply == "ACK":
	                package_acked = 1
	                print fh + " ACK'D"
	                break
	        except socket.error:
				print "am i getting a socket error"
				self.s_comm.sendto(fh, (addr, constants.LISTEN_PORT))
				count = count + 1
    
	    if(package_acked):
			# NOW THAT YOU HAVE ACK'D SET UP TCP connect
			port = self.get_next_free_port()
			my_tcp = netbin_tcp(comm_addr, port)
			my_tcp.tcp_listener(self.s_comm)
	    else:
	        print "Could not locate file holder. Please try again in a little bit."


	def get_next_free_port(self):
		self.s_comm.sendto("NEEDTCPPORT", (hostAddr, constants.HOST_LISTEN_PORT))
		port_str = self.s_comm.recv(1024)
		try: 
			port = int(port_str)
		except ValueError:
			port = 7999
		return port


	def send_tcp_open_msg(self, port, addr):
		self.s_comm.sendto("TCPOPEN " + str(port), addr)
