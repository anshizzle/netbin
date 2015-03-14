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
		
		s.sendto("ACK", addr)

	except socket.error:
		print "Failed to receive message"

	return [message, file_name,addr]



class netbin_udp:
	###udp netbin###
	def __init__(self, port):
		self.port = port

	def client_listener(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		host = socket.gethostname()
		#print "attempting to bind UDP at host " + host + " with port " + str(self.port)
		try:
			s.bind((host, self.port))
		except socket.error, msg:
			printError('Could not bind passive listener to port.')
		while 1:
			data, file_name, addr = receive_message(s)
			print data + " " + file_name + " from " + addr
