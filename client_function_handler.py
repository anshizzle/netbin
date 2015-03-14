import socket

# User made an upload command
# If length is less than 2, user did not add a file name.
#
def upload(s, user_input):
	fileinput = user_input.split(' ')
	if len(fileinput) < 2:
		print "USAGE: upload filename"
	else:
		if(os.path.isfile(fileinput[1])):
			s.sendall("upload "+fileinput[1])
			reply = s.recv(4096)
			print reply
		else:
			print "Invalid File Found"





def download_file(s, user_input):
	fileinput = user_input.split(' ')

	if len(fileinput) < 3:
		print "USAGE: download target dest"
	else:
		s.sendall("download " + fileinput[1])
		reply = s.recv
