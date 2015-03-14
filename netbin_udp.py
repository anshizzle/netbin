import socket

def receive_message(s):
	message = ""
	file_name = ""
	addr = ""
	try:
		s.settimeout(None)
		msg, addr = s.recvfrom(1024)
		
		if msg.startsWith("REQUEST"):
			tmp = msg.split(' ')
			message = "REQUEST"
			file_name = tmp[1]
		elif msg.startsWith("NEXTHOST"):
			message = "NEXTHOST"
			file_name = ""

		else:
			message = "INVALID"
			file_name = ""
		
		s.sendto("ACK", addr) #SEND ACK

	except socket.error:
		print "Failed to receive message"

	return [message, file_name, addr]

class netbin_udp:
	def __init__(self, port):
		self.port = port
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.host = socket.gethostname()

	def listener(self):
		print "attempting to bind UDP at host " + self.host + " with port " + str(self.port)
		try:
			self.s.bind((self.host, self.port))
		except socket.error, msg:
			printError('Could not bind passive listener to port.')
		while 1:
			data, file_name, addr = receive_message(self.s)
			print data + " " + file_name + " from " + addr

	def send_request(self, fh, addr):
		#send the whole command
	    self.s.sendto(fh, addr)
	    # Get ACK from listener
	    package_acked = 0
	    count = 1 #message has already been sent once

	    s.settimeout(.500)
	    while not package_acked and count < 3:
	        print "Waiting for ACK " + msg
	        try:
	            d = s.recvfrom(1024)
	            reply = d[0]
	            if reply == "ACK":
	                package_acked = 1
	                print "PACKAGE WAS ACKED"
	        except socket.error:
	            s.sendto(msg, addr)
	            count = count + 1
	    if count >= 3:
	        printError("Failed to send message.")
