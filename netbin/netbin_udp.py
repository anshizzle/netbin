import socket
from netbin_tcp import *
import constants
from util import *
import os


def send_udp_message(s, msg, addr):
    # DETERMINE LENGTH OF MESSAGE
    try :
        #send the whole command
        s.sendto(msg, addr)
         
        # Get ACK from client
        package_acked = 0
        count = 1 #

        s.settimeout(.500)

        while not package_acked and count < 3:
            # print "Waiting for ACK for " + msg 
            try:
                d = s.recvfrom(1024)
                reply = d[0]
                if reply == "ACK":
                    package_acked = 1
            except socket.error:
                s.sendto(msg, addr)
                count = count + 1

        if count >= 3:
            printDebug("UDP Message failed to send to " + str(addr), "udp")


    except socket.error, msg:
    	printDebug("UDP Message failed to send to " + str(addr), "udp")





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
		print "HOST UDP: Socket error"

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
			s_comm.sendto("ACK", addr) #SEND ACK if not invalid message

	except socket.error:
		print "Failed to receive message"

	return [message, file_name, addr]


class netbin_udp:
	def __init__(self, port1, port2, hostAddr):
		self.receive_port = port1
		self.communicate_port = port2
		self.hostAddr = hostAddr
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.s_comm = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.host = socket.gethostname()
		self.available_tcp_ports = range(constants.LISTEN_PORT+1, constants.LISTEN_PORT+11)


	def listener(self):
		printDebug("attempting to bind UDP Listeners, both listener and communicator", "udp")
		try:
			self.s.bind((self.host, self.receive_port))
			self.s_comm.bind((self.host, self.communicate_port))
		except socket.error, msg:
			constants.printError('Could not bind passive listener to port.')
			os._exit(1)
		while 1:
			message, file_name, addr = receive_message(self.s, self.s_comm)
			print file_name + "\n"
			#print addr
			if message == "REQUEST":
				
				# need to know that the listening tcp connection is open
				# tcp_port = self.receive_message(self, self.s)
				tcp_port_msg, addr = self.s_comm.recvfrom(1024)
				printDebug("TCP Port Message is: " + tcp_port_msg, 'd')
				tcp_port = 0
				if tcp_port_msg.startswith("TCPOPEN"):
					tmp = tcp_port_msg.split(' ')
					if len(tmp) >= 2:
						try:
							tcp_port = int(tcp_port_msg.split(' ')[1])
						except ValueError:
							tcp_port = 0
							printDebug("TCP Port Message Error - message is: " + tcp_port_msg, 'udp')



				if tcp_port > 0:
					# now send file data to requesting netbin client
					my_tcp = netbin_tcp(tcp_port)
					my_tcp.tcp_send(file_name, addr[0])


				else:
					print "waiting to for tcp listener creation"


	def host_listener(self):
		self.available_tcp_ports.reverse()
		# printDebug(str(self.available_tcp_ports), "udp")
		printDebug("binding UDP at host " + self.host + " with port " + str(self.receive_port), "udp")
		try:
			self.s.bind((self.host, self.receive_port))
			self.s_comm.bind((self.host, self.communicate_port))
			# print "Successfully bound UDP Passive Listener for Host with Port" + str(self.port)
		except socket.error, msg:
			constants.printError('Could not bind passive host listener or communicator to port.')
			os._exit(1)
		while 1:
			msg, data, addr = receive_host_message(self.s)
			if msg == "ISHOST?":
				printDebug("Received ISHOST Request from " + addr[0], "udp")
				send_udp_message(self.s, "IAMHOST", addr)
			elif msg == "NEEDTCPPORT":
				printDebug("Received request for TCP Port from " + addr[0], "udp")
				self.s_comm.sendto(str(self.available_tcp_ports.pop()), addr)
			elif msg == "RELEASINGTCPPORT":
				try:
					released_port = int(data)
					self.available_tcp_ports.insert(0, released_port)
					printDebug("Releasing TCP Port " + str(released_port), "udp")
					self.s_comm.sendto("RELEASESUCCESSFUL", addr)
				except ValueError:
					self.s_comm.sendto("INVALIDPORT", addr)


	def send_request(self, fh, fd, addr):

	    self.s_comm.sendto("ACK " + fh + " " + str(self.communicate_port), (addr, constants.LISTEN_PORT))
	    # Get ACK from listener
	    package_acked = False
	    count = 1 #message has already been sent once

	    self.s_comm.settimeout(.500)
	    while not package_acked and count < 3:
	        print "Waiting for ACK FOR " + fh
	        try:
	            reply, comm_addr = self.s_comm.recvfrom(1024)
	            
	            if reply == "ACK":
	                package_acked = True
	                print fh + " ACK'D"
	                break
	        except socket.error:
				self.s_comm.sendto(fh, (addr, constants.LISTEN_PORT))
				count = count + 1
    
	    if package_acked:
			# NOW THAT YOU HAVE ACK'D SET UP TCP connect
			printDebug("Ack logged", "udp")

			port = self.get_next_free_port()
			printDebug("Free TCP Port is " + str(port), "udp");
			my_tcp = netbin_tcp(port)
			my_tcp.tcp_listener(comm_addr, fd, self)
	    else:
	        print "Could not locate file holder. Please try again in a little bit."


	def get_next_free_port(self):
		self.s_comm.sendto("NEEDTCPPORT", (self.hostAddr, constants.HOST_LISTEN_PORT))
		port_str = self.s_comm.recv(1024)
		try: 
			port = int(port_str)
		except ValueError:
			port = 7999
		return port


	def release_tcp_port(self, port):
		self.s_comm.sendto("RELEASINGTCPPORT " + str(port), (self.hostAddr, constants.HOST_LISTEN_PORT))
		reply = self.s_comm.recv(1024)
		printDebug("TCP Release " + str(port) + " reply: " + reply, "udp")

	def send_tcp_open_msg(self, port, addr):
		self.s_comm.sendto("TCPOPEN " + str(port), addr)
